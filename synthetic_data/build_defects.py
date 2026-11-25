"""Build the synthetic dataset v1 with injected defects and its ground truth.

Clean data comes from the generator, unchanged. This script converts it to
dicts, injects the known defects with the same seed, then writes the altered files
and ground_truth.json. Catalog of defects: synthetic_data/DEFECTS.md.

    uv run python -m synthetic_data.build_defects --seed 42
"""

import argparse
import json
from pathlib import Path
from typing import Any

from synthetic_data.defects import DefectInjector
from synthetic_data.generator import DEFAULT_SEED, generate

DEFAULT_OUTPUT = Path(__file__).parent / "output" / "v1_defects"
GROUND_TRUTH_FILE = "ground_truth.json"
# Stable DataLift identity carried by every silver object (ADR-005): used as record id.
ID = "datalift_id"


def inject(dataset: dict[str, list[dict[str, Any]]], seed: int) -> DefectInjector:
    """Inject the 7 defect types into the dicts of `dataset` (replaced in place)."""
    injector = DefectInjector(seed)
    supplier_ids = {s[ID] for s in dataset["suppliers"]}
    employee_ids = {e[ID] for e in dataset["employees"]}

    # Flow 1: Yooz invoices to IFS.
    obj = "supplier_invoices"
    rows = dataset[obj]
    rows = injector.duplicates(rows, flow=1, obj=obj, id_field=ID)
    rows = injector.amount_mismatches(rows, obj=obj, id_field=ID, amount_field="gross_curr_amount")
    rows = injector.invoices_without_po(
        rows, obj=obj, id_field=ID, po_field="purchase_order_datalift_id"
    )
    rows = injector.unknown_suppliers(
        rows, obj=obj, id_field=ID, supplier_field="supplier_datalift_id", known_ids=supplier_ids
    )
    rows = injector.missing_fields(rows, flow=1, obj=obj, id_field=ID, field="invoice_no")
    dataset[obj] = rows

    # Flow 2: Lucca employees to IFS.
    obj = "employees"
    rows = dataset[obj]
    rows = injector.duplicates(rows, flow=2, obj=obj, id_field=ID)
    rows = injector.missing_fields(rows, flow=2, obj=obj, id_field=ID, field="family_name")
    dataset[obj] = rows

    # Flow 3: Progessi time entries to IFS.
    obj = "time_entries"
    rows = dataset[obj]
    rows = injector.duplicates(rows, flow=3, obj=obj, id_field=ID)
    rows = injector.unknown_employees(
        rows, obj=obj, id_field=ID, employee_field="employee_datalift_id", known_ids=employee_ids
    )
    rows = injector.hours_out_of_range(rows, obj=obj, id_field=ID, hours_field="hours")
    rows = injector.missing_fields(rows, flow=3, obj=obj, id_field=ID, field="work_effort_id")
    dataset[obj] = rows

    return injector


def build(seed: int, out_dir: Path) -> list[Path]:
    """Generate clean data, inject defects, write the data files and the ground truth."""
    clean = generate(seed)
    # Pydantic objects refuse some defects (e.g. negative hours): inject into plain dicts.
    dataset = {name: [o.model_dump(mode="json") for o in objs] for name, objs in clean.items()}
    injector = inject(dataset, seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, rows in dataset.items():
        path = out_dir / f"{name}.json"
        # default=str: injected Decimals are written as strings, like the generator does.
        text = json.dumps(rows, ensure_ascii=False, indent=2, default=str)
        path.write_text(text + "\n", encoding="utf-8")
        paths.append(path)
    ground_truth = out_dir / GROUND_TRUTH_FILE
    injector.write_ground_truth(ground_truth)
    paths.append(ground_truth)
    return paths


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build synthetic data v1 with known defects.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    for path in build(args.seed, args.out):
        print(path)


if __name__ == "__main__":
    main()
