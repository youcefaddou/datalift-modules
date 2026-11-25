"""Tests of the dataset with injected defects: generator + injector wired together."""

import json
from collections import Counter
from pathlib import Path

import pytest

from synthetic_data.build_defects import GROUND_TRUTH_FILE, build
from synthetic_data.defects import DefectType
from synthetic_data.generator import generate, write

SEED = 42


def load(directory: Path, name: str) -> list[dict]:
    """Read one written data file, e.g. load(out, "employees") -> list of employee dicts."""
    return json.loads((directory / f"{name}.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def built(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Dataset with defects, built once for all tests of this module."""
    out = tmp_path_factory.mktemp("v1_defects")
    build(SEED, out)
    return out


@pytest.fixture(scope="module")
def ground_truth(built: Path) -> dict:
    """Content of ground_truth.json written next to the data: {"seed": ..., "defects": [...]}."""
    return json.loads((built / GROUND_TRUTH_FILE).read_text(encoding="utf-8"))


def test_every_defect_type_is_present_with_unique_ids(ground_truth: dict) -> None:
    defects = ground_truth["defects"]
    assert ground_truth["seed"] == SEED
    assert {d["defect_type"] for d in defects} == {t.value for t in DefectType}
    assert len({d["defect_id"] for d in defects}) == len(defects)


def test_each_defect_is_flagged_on_its_flow(ground_truth: dict) -> None:
    flows = {(d["object"], d["flow"]) for d in ground_truth["defects"]}
    assert flows == {("supplier_invoices", 1), ("employees", 2), ("time_entries", 3)}


def test_ground_truth_matches_the_written_files(built: Path, ground_truth: dict) -> None:
    for defect in ground_truth["defects"]:
        rows = {r["datalift_id"]: r for r in load(built, defect["object"])}
        record = rows[defect["record_id"]]
        assert record[defect["field"]] == defect["injected_value"], defect["defect_id"]


def test_unknown_references_point_to_nothing(built: Path, ground_truth: dict) -> None:
    supplier_ids = {s["datalift_id"] for s in load(built, "suppliers")}
    employee_ids = {e["datalift_id"] for e in load(built, "employees")}
    for d in ground_truth["defects"]:
        if d["defect_type"] == DefectType.UNKNOWN_SUPPLIER:
            assert d["injected_value"] not in supplier_ids
        if d["defect_type"] == DefectType.UNKNOWN_EMPLOYEE:
            assert d["injected_value"] not in employee_ids


def test_only_duplicates_add_rows(built: Path, ground_truth: dict) -> None:
    # Other defects alter a field in place, so each file has: clean rows + its duplicates.
    clean = generate(SEED)
    duplicates = Counter(
        d["object"] for d in ground_truth["defects"] if d["defect_type"] == DefectType.DUPLICATE
    )
    for name, objects in clean.items():
        assert len(load(built, name)) == len(objects) + duplicates[name], name


def test_files_without_defects_are_identical_to_the_clean_dataset(
    built: Path, tmp_path: Path
) -> None:
    write(generate(SEED), tmp_path)
    for name in ("suppliers", "purchase_orders", "projects"):
        assert (built / f"{name}.json").read_bytes() == (tmp_path / f"{name}.json").read_bytes()


def test_same_seed_gives_identical_files(built: Path, tmp_path: Path) -> None:
    build(SEED, tmp_path)
    for path in built.iterdir():
        assert path.read_bytes() == (tmp_path / path.name).read_bytes(), path.name
