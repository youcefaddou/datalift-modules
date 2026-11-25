"""DL-113: links, actions, identity map and flow definition (ADR-005)."""

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from contracts import Employee, SupplierInvoice, TimeEntry
from contracts.v1.ontology import (
    ACTIONS,
    LINKS,
    SILVER_IDENTITY_MAP_DDL,
    ActionContext,
    FlowDefinition,
    IdentityMap,
    IdentityMapRow,
)

NOW = datetime(2026, 11, 25, 9, 0, tzinfo=UTC)


def lineage(source_system: str, n: int) -> dict:
    return {
        "datalift_id": f"dl-{n}",
        "source_system": source_system,
        "source_id": str(n),
        "extracted_at": NOW,
    }


def invoice(po: str | None = "dl-po", net: str = "100.00") -> SupplierInvoice:
    return SupplierInvoice(
        **lineage("yooz", 1), Company="C1", InvoiceId="1", Identity="SUP-1", InvoiceNo="F-1",
        InvoiceDate=date(2026, 11, 2), Currency="EUR", NetCurrAmount=Decimal(net),
        supplier_datalift_id="dl-sup", purchase_order_datalift_id=po,
    )  # fmt: skip


def time_entry() -> TimeEntry:
    return TimeEntry(
        **lineage("progessi", 2), timeEntryId="TSH-1000-001", workEffortId="WE-1001",
        fromDate=NOW, thruDate=NOW, hours=Decimal(7),
        employee_datalift_id="dl-emp", project_datalift_id="dl-prj",
    )  # fmt: skip


def ctx(**kw) -> ActionContext:
    return ActionContext(identity_map=kw.pop("identity_map", IdentityMap()), **kw)


# Links -------------------------------------------------------------------------


def test_six_links_with_existing_join_fields() -> None:
    assert len(LINKS) == 6
    for link in LINKS:
        assert link.fk_field in link.fk_model.model_fields, link
        assert link.cardinality in {"N:1", "1:N"} and link.match_on, link
    optional = {(lk.source.__name__, lk.name) for lk in LINKS if not lk.required}
    assert optional == {("SupplierInvoice", "purchase_order")}


# Actions -----------------------------------------------------------------------


def test_three_actions_declared() -> None:
    assert set(ACTIONS) == {"send_invoice_to_ifs", "sync_employee_to_ifs", "send_time_entry_to_ifs"}
    assert all(a.target == "ifs" and a.preconditions for a in ACTIONS.values())


def test_invoice_passes_when_validated_linked_and_matching() -> None:
    c = ctx(approved={"dl-1"}, order_totals={"dl-po": Decimal("100.00")})
    assert ACTIONS["send_invoice_to_ifs"].failed(invoice(), c) == []


def test_invoice_not_validated_in_yooz_is_set_aside() -> None:
    c = ctx(order_totals={"dl-po": Decimal("100.00")})
    assert ACTIONS["send_invoice_to_ifs"].failed(invoice(), c) == ["validated_in_yooz"]


def test_invoice_without_order_is_set_aside() -> None:
    failed = ACTIONS["send_invoice_to_ifs"].failed(invoice(po=None), ctx(approved={"dl-1"}))
    assert failed == ["linked_to_order", "matches_order"]


def test_invoice_with_amount_gap_is_set_aside() -> None:
    c = ctx(approved={"dl-1"}, order_totals={"dl-po": Decimal("90.00")})
    assert ACTIONS["send_invoice_to_ifs"].failed(invoice(), c) == ["matches_order"]


def test_employee_must_come_from_lucca() -> None:
    lucca = Employee(**lineage("lucca", 3))
    ifs = Employee(**lineage("ifs", 4))
    action = ACTIONS["sync_employee_to_ifs"]
    assert action.failed(lucca, ctx()) == []
    assert action.failed(ifs, ctx()) == ["from_lucca"]


def test_time_entry_needs_approved_sheet_and_employee_in_ifs() -> None:
    ids = IdentityMap()
    ids.add(
        IdentityMapRow(
            object_type="Employee", datalift_id="dl-emp", source_system="ifs", source_id="EMP-0001"
        )
    )
    action = ACTIONS["send_time_entry_to_ifs"]
    assert action.failed(time_entry(), ctx(identity_map=ids, approved={"dl-2"})) == []
    assert action.failed(time_entry(), ctx(approved={"dl-2"})) == ["employee_in_ifs"]
    assert action.failed(time_entry(), ctx(identity_map=ids)) == ["timesheet_approved"]


def test_action_refuses_the_wrong_object_type() -> None:
    with pytest.raises(TypeError):
        ACTIONS["sync_employee_to_ifs"].failed(time_entry(), ctx())


# Identity map ------------------------------------------------------------------


def test_identity_map_resolves_one_id_across_software() -> None:
    ids = IdentityMap()
    for system, sid in (("lucca", "42"), ("progessi", "EMP-0001"), ("ifs", "EMP-0001")):
        ids.add(
            IdentityMapRow(
                object_type="Employee", datalift_id="dl-emp", source_system=system, source_id=sid
            )
        )
    assert ids.resolve("Employee", "lucca", "42") == "dl-emp"
    assert ids.exists_in("dl-emp", "ifs") and not ids.exists_in("dl-emp", "yooz")
    assert ids.resolve("Employee", "lucca", "999") is None


def test_identity_map_refuses_two_ids_for_one_source_record() -> None:
    ids = IdentityMap()
    ids.add(
        IdentityMapRow(
            object_type="Employee", datalift_id="dl-1", source_system="lucca", source_id="42"
        )
    )
    ids.add(
        IdentityMapRow(
            object_type="Employee", datalift_id="dl-1", source_system="lucca", source_id="42"
        )
    )
    with pytest.raises(ValueError):
        ids.add(
            IdentityMapRow(
                object_type="Employee", datalift_id="dl-2", source_system="lucca", source_id="42"
            )
        )


def test_identity_map_table_has_its_columns_and_unique_key() -> None:
    for col in ("object_type", "datalift_id", "source_system", "source_id"):
        assert col in SILVER_IDENTITY_MAP_DDL
    assert "UNIQUE (object_type, source_system, source_id)" in SILVER_IDENTITY_MAP_DDL


# Flow definition ---------------------------------------------------------------


def test_flow_references_a_known_action_and_needs_validation() -> None:
    flow = FlowDefinition(
        name="Factures Yooz vers IFS", source_system="yooz", object_type="SupplierInvoice",
        mappings={"invoiceNumber": "InvoiceNo"}, action="send_invoice_to_ifs",
    )  # fmt: skip
    assert flow.validation_status == "proposed" and not flow.executable
    assert flow.model_copy(update={"validation_status": "validated"}).executable
    with pytest.raises(ValidationError):
        FlowDefinition(
            name="x", source_system="yooz", object_type="SupplierInvoice", action="delete_all"
        )


def test_flow_object_must_match_the_action_object() -> None:
    with pytest.raises(ValidationError):
        FlowDefinition(
            name="x", source_system="lucca", object_type="Employee", action="send_invoice_to_ifs"
        )
