"""Tests of the defect injector.

The datasets below are small fake inputs built for the tests only. They stand in
for the synthetic data generator and use simple field names on purpose.
"""

import dataclasses
import json
from decimal import Decimal
from pathlib import Path

import pytest

from synthetic_data.defects import Defect, DefectInjector, DefectType

SUPPLIERS = {"S1", "S2", "S3"}


def invoices(count: int = 40) -> list[dict]:
    """Clean invoices: known supplier, a purchase order and the same total for all."""
    return [
        {
            "id": f"INV-{i:03d}",
            "supplier": f"S{i % 3 + 1}",
            "po": f"PO-{i:03d}",
            "total": Decimal("120.00"),
        }
        for i in range(count)
    ]


def time_entries(count: int = 40) -> list[dict]:
    """Clean time entries: known employee E1 and 7.5 hours each."""
    return [{"id": f"T-{i:03d}", "employee": "E1", "hours": Decimal("7.5")} for i in range(count)]


def run_all(seed: int) -> tuple[list[dict], list[dict], DefectInjector]:
    """Inject the 7 defect types with one injector, as the generator will do."""
    injector = DefectInjector(seed)
    inv = invoices()
    inv = injector.duplicates(inv, flow=1, obj="invoice", id_field="id")
    inv = injector.amount_mismatches(inv, obj="invoice", id_field="id", amount_field="total")
    inv = injector.invoices_without_po(inv, obj="invoice", id_field="id", po_field="po")
    inv = injector.unknown_suppliers(
        inv, obj="invoice", id_field="id", supplier_field="supplier", known_ids=SUPPLIERS
    )
    inv = injector.missing_fields(inv, flow=1, obj="invoice", id_field="id", field="supplier")
    tim = time_entries()
    tim = injector.unknown_employees(
        tim, obj="time_entry", id_field="id", employee_field="employee", known_ids={"E1"}
    )
    tim = injector.hours_out_of_range(tim, obj="time_entry", id_field="id", hours_field="hours")
    return inv, tim, injector


# Vocabulary


def test_the_seven_defect_types_of_the_ticket_exist() -> None:
    assert [t.value for t in DefectType] == [
        "DUPLICATE",
        "AMOUNT_MISMATCH",
        "INVOICE_WITHOUT_PO",
        "UNKNOWN_SUPPLIER",
        "UNKNOWN_EMPLOYEE",
        "HOURS_OUT_OF_RANGE",
        "MISSING_FIELD",
    ]


def test_a_ground_truth_line_cannot_be_modified() -> None:
    defect = Defect("DEF-0001", DefectType.MISSING_FIELD, 1, "invoice", "INV-1", "po", "PO-1", None)
    with pytest.raises(dataclasses.FrozenInstanceError):
        defect.record_id = "INV-2"  # type: ignore[misc]


# Reproducibility


def test_same_seed_gives_same_data_and_ground_truth() -> None:
    first, second = run_all(seed=42), run_all(seed=42)
    assert first[0] == second[0] and first[1] == second[1]
    assert first[2].ground_truth() == second[2].ground_truth()


def test_different_seed_changes_the_chosen_records() -> None:
    assert run_all(seed=1)[2].ground_truth() != run_all(seed=2)[2].ground_truth()


# Injection


def test_every_defect_type_is_injected_once_per_record_with_unique_ids() -> None:
    defects = run_all(seed=42)[2].defects
    assert {d.defect_type for d in defects} == set(DefectType)
    assert len({d.defect_id for d in defects}) == len(defects)
    assert len({(d.object, d.record_id) for d in defects}) == len(defects)


def test_ground_truth_matches_the_altered_records() -> None:
    inv, tim, injector = run_all(seed=42)
    by_id = {r["id"]: r for r in inv} | {r["id"]: r for r in tim}
    for defect in injector.defects:
        assert by_id[defect.record_id][defect.field] == defect.injected_value


def test_untouched_records_are_unchanged_and_input_is_not_mutated() -> None:
    original = invoices()
    injector = DefectInjector(7)
    result = injector.amount_mismatches(
        original, obj="invoice", id_field="id", amount_field="total"
    )
    assert original == invoices()
    touched = {d.record_id for d in injector.defects}
    assert all(r["total"] == Decimal("120.00") for r in result if r["id"] not in touched)


def test_duplicate_keeps_content_with_a_new_id() -> None:
    injector = DefectInjector(3)
    result = injector.duplicates(invoices(), flow=1, obj="invoice", id_field="id", rate=0.1)
    assert len(result) == 44
    by_id = {r["id"]: r for r in result}
    for defect in injector.defects:
        copy, source = by_id[defect.record_id], by_id[defect.original_value]
        assert {**copy, "id": source["id"]} == source


def test_values_follow_the_defect_rules() -> None:
    injector = run_all(seed=42)[2]
    for d in injector.defects:
        if d.defect_type is DefectType.AMOUNT_MISMATCH:
            assert abs(d.injected_value - d.original_value) == Decimal("10.00")
        if d.defect_type is DefectType.HOURS_OUT_OF_RANGE:
            assert d.injected_value < 0 or d.injected_value > 24
        if d.defect_type is DefectType.UNKNOWN_SUPPLIER:
            assert d.injected_value not in SUPPLIERS
        if d.defect_type is DefectType.UNKNOWN_EMPLOYEE:
            assert d.injected_value != "E1"
        if d.defect_type in (DefectType.INVOICE_WITHOUT_PO, DefectType.MISSING_FIELD):
            assert d.injected_value is None and d.original_value is not None


def test_rate_controls_the_number_of_defects() -> None:
    no_defect = DefectInjector(1).duplicates(invoices(), flow=1, obj="i", id_field="id", rate=0)
    assert no_defect == invoices()
    injector = DefectInjector(1)
    injector.missing_fields(invoices(), flow=1, obj="i", id_field="id", field="po", rate=0.25)
    assert len(injector.defects) == 10


# Ground truth file


def test_ground_truth_file_is_valid_json(tmp_path: Path) -> None:
    injector = run_all(seed=42)[2]
    target = tmp_path / "out" / "ground_truth.json"
    injector.write_ground_truth(target)
    content = json.loads(target.read_text(encoding="utf-8"))
    assert content["seed"] == 42
    assert len(content["defects"]) == len(injector.defects)
    assert content["defects"][0]["defect_id"] == "DEF-0001"
    assert {d["defect_type"] for d in content["defects"]} == {t.value for t in DefectType}
