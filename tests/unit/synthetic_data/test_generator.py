"""Tests for the synthetic dataset v1 generator (DL-37)."""

import json
from collections import Counter
from datetime import datetime
from decimal import Decimal

import pytest

from contracts.v1 import Employee, Project, PurchaseOrder, Supplier, SupplierInvoice, TimeEntry
from synthetic_data.generator import (
    EMAIL_DOMAIN,
    EXTRACTED_AT,
    Volumes,
    generate,
    to_json,
    write,
)

MODELS = {
    "suppliers": Supplier,
    "purchase_orders": PurchaseOrder,
    "supplier_invoices": SupplierInvoice,
    "employees": Employee,
    "projects": Project,
    "time_entries": TimeEntry,
}


@pytest.fixture(scope="module")
def dataset():
    return generate()


def _dump(data):
    return {name: to_json(objects) for name, objects in data.items()}


def test_same_seed_gives_identical_output(dataset):
    assert _dump(generate()) == _dump(dataset)


def test_other_seed_gives_different_output(dataset):
    assert _dump(generate(seed=7)) != _dump(dataset)


def test_default_volumes(dataset):
    v = Volumes()
    assert len(dataset["suppliers"]) == v.suppliers
    assert len(dataset["purchase_orders"]) == v.purchase_orders
    assert len(dataset["supplier_invoices"]) == v.invoices
    assert len(dataset["employees"]) == v.employees
    assert len(dataset["projects"]) == 2 * v.clients
    working_days = v.timesheet_weeks * 5
    assert len(dataset["time_entries"]) == v.employees * working_days


def test_custom_volumes():
    data = generate(volumes=Volumes(suppliers=2, purchase_orders=3, invoices=3, employees=1))
    assert len(data["supplier_invoices"]) == 3
    assert len(data["time_entries"]) == 20


def test_more_invoices_than_orders_is_rejected():
    with pytest.raises(ValueError):
        generate(volumes=Volumes(purchase_orders=2, invoices=3))


@pytest.mark.parametrize("name", MODELS)
def test_json_round_trips_through_contracts(dataset, name):
    for record in json.loads(to_json(dataset[name])):
        MODELS[name].model_validate(record)


@pytest.mark.parametrize("name", MODELS)
def test_identities_are_unique(dataset, name):
    objects = dataset[name]
    assert len({o.datalift_id for o in objects}) == len(objects)
    assert len({o.source_id for o in objects}) == len(objects)


def test_purchase_orders_reference_existing_suppliers(dataset):
    suppliers = {s.datalift_id: s for s in dataset["suppliers"]}
    for order in dataset["purchase_orders"]:
        assert suppliers[order.supplier_datalift_id].supplier_id == order.vendor_no


def test_each_invoice_matches_its_own_order_and_supplier(dataset):
    orders = {o.datalift_id: o for o in dataset["purchase_orders"]}
    invoices = dataset["supplier_invoices"]
    assert all(c == 1 for c in Counter(i.purchase_order_datalift_id for i in invoices).values())
    for invoice in invoices:
        order = orders[invoice.purchase_order_datalift_id]
        assert invoice.supplier_datalift_id == order.supplier_datalift_id
        assert invoice.identity == order.vendor_no
        assert invoice.invoice_date > order.order_date


def test_invoice_amounts_are_consistent(dataset):
    for invoice in dataset["supplier_invoices"]:
        assert 1 <= len(invoice.lines) <= 3
        assert all(
            line.supplier_invoice_datalift_id == invoice.datalift_id for line in invoice.lines
        )
        assert invoice.net_curr_amount == sum(line.net_curr_amount for line in invoice.lines)
        assert invoice.vat_curr_amount == (invoice.net_curr_amount * Decimal("0.20")).quantize(
            Decimal("0.01")
        )
        assert invoice.gross_curr_amount == invoice.net_curr_amount + invoice.vat_curr_amount


def test_time_entries_reference_employees_and_sub_projects(dataset):
    employees = {e.datalift_id for e in dataset["employees"]}
    sub_projects = {p.datalift_id: p for p in dataset["projects"] if p.work_effort_parent_id}
    for entry in dataset["time_entries"]:
        assert entry.employee_datalift_id in employees
        assert sub_projects[entry.project_datalift_id].work_effort_id == entry.work_effort_id


def test_time_entries_are_on_working_days_with_coherent_hours(dataset):
    for entry in dataset["time_entries"]:
        assert entry.from_date.weekday() < 5
        assert Decimal(7) <= entry.hours <= Decimal(8)
        duration_h = Decimal((entry.thru_date - entry.from_date).total_seconds()) / 3600
        assert duration_h == entry.hours


def test_project_parents_exist(dataset):
    ids = {p.work_effort_id for p in dataset["projects"]}
    for project in dataset["projects"]:
        assert project.work_effort_parent_id in (None, *ids)


def test_no_date_after_extraction(dataset):
    for invoice in dataset["supplier_invoices"]:
        assert invoice.invoice_date <= EXTRACTED_AT.date()
    for entry in dataset["time_entries"]:
        assert entry.thru_date <= EXTRACTED_AT
    for employee in dataset["employees"]:
        assert employee.date_of_employment <= EXTRACTED_AT.date()


def test_extracted_at_is_fixed_utc(dataset):
    for objects in dataset.values():
        for o in objects:
            assert o.extracted_at == EXTRACTED_AT
            assert isinstance(o.extracted_at, datetime) and o.extracted_at.tzinfo is not None


def test_people_data_is_obviously_fictitious(dataset):
    for employee in dataset["employees"]:
        assert employee.email.endswith(f"@{EMAIL_DOMAIN}")
    for supplier in dataset["suppliers"]:
        assert "Fictif" in supplier.name


def test_write_creates_one_file_per_object(dataset, tmp_path):
    paths = write(dataset, tmp_path)
    assert {p.stem for p in paths} == set(MODELS)
    for path in paths:
        assert len(json.loads(path.read_text(encoding="utf-8"))) == len(dataset[path.stem])
