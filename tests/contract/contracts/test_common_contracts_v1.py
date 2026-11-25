"""Contract tests for DataLift common schema v1."""

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from contracts import (
    CONTRACT_VERSION,
    Employee,
    InvoiceLine,
    Project,
    PurchaseOrder,
    Supplier,
    SupplierInvoice,
    TimeEntry,
)

LINEAGE = {
    "datalift_id": "dl:employee:stable-001",
    "source_system": "lucca",
    "source_id": "42",
    "extracted_at": datetime(2026, 11, 25, 9, 0, tzinfo=UTC),
}


def test_schema_is_versioned() -> None:
    assert CONTRACT_VERSION == "1.0.0"


def test_supplier_uses_source_aliases_and_lineage() -> None:
    supplier = Supplier(**LINEAGE, SupplierId="SUP-1", Name="Example")
    assert supplier.supplier_id == "SUP-1"
    assert supplier.model_dump(by_alias=True)["SupplierId"] == "SUP-1"
    assert supplier.datalift_id == LINEAGE["datalift_id"]


def test_purchase_order_requires_supplier_relation() -> None:
    order = PurchaseOrder(
        **LINEAGE,
        OrderNo="PO-1",
        VendorNo="SUP-1",
        supplier_datalift_id="dl:supplier:1",
        OrderDate=date(2026, 11, 1),
    )
    assert order.supplier_datalift_id == "dl:supplier:1"


def test_invoice_has_required_supplier_optional_order_and_lines() -> None:
    line = InvoiceLine(
        **{**LINEAGE, "datalift_id": "dl:line:1", "source_id": "line-1"},
        ItemId=1,
        NetCurrAmount=Decimal("12.50"),
        supplier_invoice_datalift_id="dl:invoice:1",
    )
    invoice = SupplierInvoice(
        **{**LINEAGE, "datalift_id": "dl:invoice:1", "source_id": "inv-1"},
        Company="DL01",
        InvoiceId=1001,
        Identity="SUP-1",
        InvoiceNo="INV-1",
        InvoiceDate=date(2026, 11, 1),
        Currency="EUR",
        supplier_datalift_id="dl:supplier:1",
        lines=[line],
    )
    assert invoice.purchase_order_datalift_id is None
    assert invoice.lines[0].net_curr_amount == Decimal("12.50")


def test_invoice_amounts_are_decimal_not_float() -> None:
    invoice = SupplierInvoice(
        **{**LINEAGE, "datalift_id": "dl:invoice:2", "source_id": "inv-2"},
        Company="DL01",
        InvoiceId=1002,
        Identity="SUP-1",
        InvoiceNo="INV-2",
        InvoiceDate=date(2026, 11, 1),
        Currency="EUR",
        NetCurrAmount="12.30",
        supplier_datalift_id="dl:supplier:1",
    )
    assert invoice.net_curr_amount == Decimal("12.30")


def test_employee_accepts_lucca_and_ifs_source_fields() -> None:
    employee = Employee(
        **LINEAGE,
        id=42,
        remoteId="remote-42",
        employeeNumber="E-42",
        givenName="Ada",
        familyName="Lovelace",
        CompanyId="DL01",
        EmpNo="E-42",
        PersonId="P-42",
    )
    assert employee.employee_number == "E-42"


def test_project_uses_ofbiz_work_effort_fields() -> None:
    project = Project(
        **{**LINEAGE, "datalift_id": "dl:project:1", "source_id": "WE-1"},
        workEffortId="WE-1",
        workEffortTypeId="PROJECT",
        workEffortName="Project A",
        currentStatusId="PRJ_ACTIVE",
    )
    assert project.work_effort_id == "WE-1"


def test_time_entry_requires_employee_and_project_relations() -> None:
    entry = TimeEntry(
        **{**LINEAGE, "datalift_id": "dl:time:1", "source_id": "TE-1"},
        timeEntryId="TE-1",
        workEffortId="WE-1",
        fromDate="2026-11-01T00:00:00Z",
        thruDate="2026-11-01T23:59:59Z",
        hours="7.00",
        employee_datalift_id="dl:employee:1",
        project_datalift_id="dl:project:1",
    )
    assert entry.hours == Decimal("7.00")
    assert entry.from_date.tzinfo is not None


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        Supplier(**LINEAGE, SupplierId="SUP-1", invented_field="no")


def test_lineage_is_required() -> None:
    with pytest.raises(ValidationError):
        Supplier(SupplierId="SUP-1")


def test_every_declared_field_has_source_metadata() -> None:
    models = (Supplier, PurchaseOrder, SupplierInvoice, InvoiceLine, Employee, Project, TimeEntry)
    for model in models:
        for field in model.model_fields.values():
            source = (field.json_schema_extra or {}).get("source")
            assert source, f"{model.__name__}.{field.name} has no source metadata"


def test_checked_in_json_schema_contains_all_contracts() -> None:
    import json
    from pathlib import Path

    schema_path = Path("contracts/v1/schema.json")
    schema = json.loads(schema_path.read_text())
    assert schema["version"] == CONTRACT_VERSION
    assert set(schema["models"]) == {
        "Supplier",
        "PurchaseOrder",
        "SupplierInvoice",
        "InvoiceLine",
        "Employee",
        "Project",
        "TimeEntry",
    }
