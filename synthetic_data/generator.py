"""Reproducible synthetic dataset v1 for the 3 M1 flows, in silver format (contracts/v1).

Flow 1 (Yooz -> IFS): suppliers, purchase orders, supplier invoices with lines.
Flow 2 (Lucca -> IFS): employees.
Flow 3 (Progessi -> IFS): projects, time entries.

Same seed => byte-identical output. No real data: names are obviously fictitious and
emails use the reserved `exemple.invalid` domain (docs/DATA_POLICY.md).
"""

from __future__ import annotations

import argparse
import json
import random
import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from contracts.v1 import (
    CommonModel,
    Employee,
    InvoiceLine,
    Project,
    PurchaseOrder,
    Supplier,
    SupplierInvoice,
    TimeEntry,
)

DEFAULT_SEED = 42
DEFAULT_OUTPUT = Path(__file__).parent / "output" / "v1"
EMAIL_DOMAIN = "exemple.invalid"
COMPANY = "DL01"
CENT = Decimal("0.01")
VAT_RATE = Decimal("0.20")

# Fixed dates: output must not depend on the day the generator runs.
EXTRACTED_AT = datetime(2026, 11, 2, 6, 0, tzinfo=UTC)
ORDER_PERIOD = (
    date(2026, 8, 1),
    date(2026, 9, 30),
)  # invoices (+5..30 days) stay before EXTRACTED_AT
TIMESHEET_START = date(2026, 10, 5)  # Monday

# Stable namespace for datalift_id (uuid5 of object type + source system + source id).
DATALIFT_NAMESPACE = uuid.UUID("5d1f3c0e-7a52-4c1b-9a0e-6f2b8d4e1a37")

GIVEN_NAMES = [
    "Alex", "Camille", "Dominique", "Sacha", "Charlie", "Morgan", "Lou", "Noa",
    "Eden", "Robin", "Sam", "Jessie", "Ange", "Claude", "Maxime", "Andrea",
]  # fmt: skip
FAMILY_NAMES = [
    "Fictif", "Exemple", "Test", "Imaginaire", "Invente", "Factice", "Modele",
    "Simule", "Demo", "Prototype",
]  # fmt: skip
SUBPROJECTS = ["Migration", "Integration", "Support", "Audit"]
INVOICE_ITEMS = ["Prestation fictive", "Licence fictive", "Materiel fictif", "Formation fictive"]
SUPPLIER_COUNTRIES = [("FR", "fr")] * 6 + [("BE", "fr"), ("DE", "de")]
DAILY_HOURS = [Decimal(7), Decimal("7.5"), Decimal(8)]


@dataclass(frozen=True)
class Volumes:
    suppliers: int = 20
    purchase_orders: int = 60
    invoices: int = 50  # each invoice matches a distinct purchase order
    employees: int = 40
    clients: int = 4  # each client project has one sub-project => 2 * clients projects
    timesheet_weeks: int = 4


def datalift_id(object_type: str, source_system: str, source_id: str) -> str:
    return str(uuid.uuid5(DATALIFT_NAMESPACE, f"{object_type}:{source_system}:{source_id}"))


def _lineage(object_type: str, source_system: str, source_id: str) -> dict:
    return {
        "datalift_id": datalift_id(object_type, source_system, source_id),
        "source_system": source_system,
        "source_id": source_id,
        "extracted_at": EXTRACTED_AT,
    }


def _random_date(rng: random.Random, start: date, end: date) -> date:
    return start + timedelta(days=rng.randint(0, (end - start).days))


def _amount(rng: random.Random, low: int, high: int) -> Decimal:
    return Decimal(rng.randint(low * 100, high * 100)) / 100


def generate_suppliers(rng: random.Random, volumes: Volumes) -> list[Supplier]:
    suppliers = []
    for n in range(1, volumes.suppliers + 1):
        code = f"SUP-{n:04d}"
        country, language = rng.choice(SUPPLIER_COUNTRIES)
        suppliers.append(
            Supplier(
                **_lineage("supplier", "ifs", code),
                supplier_id=code,
                name=f"Fournisseur Fictif {n:02d}",
                country=country,
                default_language=language,
            )
        )
    return suppliers


def generate_purchase_orders(
    rng: random.Random, volumes: Volumes, suppliers: list[Supplier]
) -> list[PurchaseOrder]:
    orders = []
    for n in range(1, volumes.purchase_orders + 1):
        code = f"PO-{n:04d}"
        supplier = rng.choice(suppliers)
        orders.append(
            PurchaseOrder(
                **_lineage("purchase_order", "ifs", code),
                order_no=code,
                vendor_no=supplier.supplier_id,
                order_date=_random_date(rng, *ORDER_PERIOD),
                objstate="Released",
                contract=COMPANY,
                buyer_code=f"BUY-{rng.randint(1, 3):02d}",
                authorize_code="AUT-01",
                currency_code="EUR",
                company=COMPANY,
                supplier_datalift_id=supplier.datalift_id,
            )
        )
    return orders


def generate_invoices(
    rng: random.Random, volumes: Volumes, orders: list[PurchaseOrder]
) -> list[SupplierInvoice]:
    if volumes.invoices > len(orders):
        raise ValueError("invoices cannot exceed purchase_orders: one order per invoice")
    invoices = []
    for n, order in enumerate(rng.sample(orders, volumes.invoices), start=1):
        invoice_no = f"FAC-FICT-{n:04d}"
        invoice_dl_id = datalift_id("supplier_invoice", "yooz", invoice_no)
        lines = []
        for item in range(1, rng.randint(1, 3) + 1):
            line_source_id = f"{invoice_no}-{item}"
            lines.append(
                InvoiceLine(
                    **_lineage("invoice_line", "yooz", line_source_id),
                    item_id=item,
                    description=rng.choice(INVOICE_ITEMS),
                    net_curr_amount=_amount(rng, 100, 5000),
                    vat_code="TVA20",
                    supplier_invoice_datalift_id=invoice_dl_id,
                )
            )
        net = sum((line.net_curr_amount for line in lines), Decimal(0))
        vat = (net * VAT_RATE).quantize(CENT)
        invoice_date = order.order_date + timedelta(days=rng.randint(5, 30))
        invoices.append(
            SupplierInvoice(
                **_lineage("supplier_invoice", "yooz", invoice_no),
                company=COMPANY,
                invoice_id=1000 + n,
                identity=order.vendor_no,
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                currency="EUR",
                due_date=invoice_date + timedelta(days=30),
                net_curr_amount=net,
                vat_curr_amount=vat,
                gross_curr_amount=net + vat,
                objstate="PrelPosted",
                supplier_datalift_id=order.supplier_datalift_id,
                purchase_order_datalift_id=order.datalift_id,
                lines=lines,
            )
        )
    return invoices


def generate_employees(rng: random.Random, volumes: Volumes) -> list[Employee]:
    employees = []
    for n in range(1, volumes.employees + 1):
        given, family = rng.choice(GIVEN_NAMES), rng.choice(FAMILY_NAMES)
        emp_no = f"EMP-{n:04d}"
        employees.append(
            Employee(
                **_lineage("employee", "lucca", str(n)),
                lucca_id=str(n),
                employee_number=emp_no,
                given_name=given,
                family_name=family,
                email=f"{given.lower()}.{family.lower()}.{n:04d}@{EMAIL_DOMAIN}",
                phone_number=f"0100{n:06d}",
                status="active",
                company_id=COMPANY,
                emp_no=emp_no,
                person_id=f"PERS-{n:04d}",
                date_of_employment=_random_date(rng, date(2018, 1, 1), date(2026, 9, 1)),
            )
        )
    return employees


def generate_projects(volumes: Volumes) -> list[Project]:
    projects = []
    for c in range(1, volumes.clients + 1):
        parent_id = f"WE-{c}000"
        child_id = f"WE-{c}001"
        parent = Project(
            **_lineage("project", "progessi", parent_id),
            work_effort_id=parent_id,
            work_effort_type_id="PROJECT",
            work_effort_name=f"Client-{c:02d}",
            current_status_id="PRJ_ACTIVE",
            reference=f"PRJ-{c:04d}",
        )
        sub = SUBPROJECTS[(c - 1) % len(SUBPROJECTS)]
        child = Project(
            **_lineage("project", "progessi", child_id),
            work_effort_id=child_id,
            work_effort_type_id="PROJECT",
            work_effort_parent_id=parent_id,
            work_effort_name=sub,
            current_status_id="PRJ_ACTIVE",
            reference=f"PRJ-{c:04d}-{sub[:3].upper()}",
        )
        projects += [parent, child]
    return projects


def generate_time_entries(
    rng: random.Random, volumes: Volumes, employees: list[Employee], projects: list[Project]
) -> list[TimeEntry]:
    """One entry per employee and working day, on 1 or 2 assigned sub-projects."""
    sub_projects = [p for p in projects if p.work_effort_parent_id is not None]
    working_days = [
        TIMESHEET_START + timedelta(days=d)
        for d in range(volumes.timesheet_weeks * 7)
        if (TIMESHEET_START + timedelta(days=d)).weekday() < 5
    ]
    entries = []
    for n, employee in enumerate(employees, start=1):
        party_id = str(10000 + n)
        assigned = rng.sample(sub_projects, min(len(sub_projects), rng.randint(1, 2)))
        for day in working_days:
            project = rng.choice(assigned)
            hours = rng.choice(DAILY_HOURS)
            start = datetime.combine(day, datetime.min.time(), UTC) + timedelta(hours=9)
            entry_id = f"TE-{party_id}-{day:%Y%m%d}"
            entries.append(
                TimeEntry(
                    **_lineage("time_entry", "progessi", entry_id),
                    time_entry_id=entry_id,
                    timesheet_id=f"TSH-{party_id}-{day:%Y%m}",
                    party_id=party_id,
                    work_effort_id=project.work_effort_id,
                    from_date=start,
                    thru_date=start + timedelta(hours=float(hours)),
                    hours=hours,
                    employee_datalift_id=employee.datalift_id,
                    project_datalift_id=project.datalift_id,
                )
            )
    return entries


def generate(seed: int = DEFAULT_SEED, volumes: Volumes | None = None) -> dict[str, list]:
    """Build the full dataset. Keys are silver object names (file names on disk)."""
    volumes = volumes or Volumes()
    rng = random.Random(seed)
    suppliers = generate_suppliers(rng, volumes)
    orders = generate_purchase_orders(rng, volumes, suppliers)
    invoices = generate_invoices(rng, volumes, orders)
    employees = generate_employees(rng, volumes)
    projects = generate_projects(volumes)
    time_entries = generate_time_entries(rng, volumes, employees, projects)
    return {
        "suppliers": suppliers,
        "purchase_orders": orders,
        "supplier_invoices": invoices,
        "employees": employees,
        "projects": projects,
        "time_entries": time_entries,
    }


def to_json(objects: list[CommonModel]) -> str:
    return json.dumps([o.model_dump(mode="json") for o in objects], ensure_ascii=False, indent=2)


def write(dataset: dict[str, list], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, objects in dataset.items():
        path = out_dir / f"{name}.json"
        path.write_text(to_json(objects) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate DataLift synthetic data v1.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    dataset = generate(args.seed)
    for path in write(dataset, args.out):
        print(f"{path} ({len(dataset[path.stem])} objects)")


if __name__ == "__main__":
    main()
