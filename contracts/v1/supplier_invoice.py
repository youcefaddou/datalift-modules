"""Supplier invoice and line contracts based on IFS manual supplier invoice resources."""

from datetime import date
from decimal import Decimal

from pydantic import Field

from contracts.v1.base import CommonModel


class InvoiceLine(CommonModel):
    item_id: int | str = Field(
        alias="ItemId", json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceItems"}
    )
    description: str | None = Field(
        default=None,
        alias="Description",
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceItems"},
    )
    net_curr_amount: Decimal | None = Field(
        default=None,
        alias="NetCurrAmount",
        json_schema_extra={
            "source": "mocks/ifs/seed.json: ManSuppInvoiceItems; docs/CONVENTIONS.md (Decimal)"
        },
    )
    vat_code: str | None = Field(
        default=None,
        alias="VatCode",
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceItems"},
    )
    supplier_invoice_datalift_id: str = Field(
        min_length=1,
        description="Relation invoice_line → supplier_invoice (ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )


class SupplierInvoice(CommonModel):
    company: str = Field(
        alias="Company",
        min_length=1,
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"},
    )
    invoice_id: int | str = Field(
        alias="InvoiceId",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: ManSuppInvoiceSet; mocks/ifs/seed.json"
        },
    )
    identity: str = Field(
        alias="Identity",
        min_length=1,
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"},
    )
    invoice_no: str = Field(
        alias="InvoiceNo",
        min_length=1,
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"},
    )
    invoice_date: date = Field(
        alias="InvoiceDate", json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"}
    )
    currency: str = Field(
        alias="Currency",
        min_length=1,
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"},
    )
    due_date: date | None = Field(
        default=None,
        alias="DueDate",
        json_schema_extra={"source": "mocks/ifs/seed.json: ManSuppInvoiceSet"},
    )
    net_curr_amount: Decimal | None = Field(
        default=None,
        alias="NetCurrAmount",
        json_schema_extra={
            "source": "mocks/ifs/seed.json: ManSuppInvoiceSet; docs/CONVENTIONS.md (Decimal)"
        },
    )
    vat_curr_amount: Decimal | None = Field(
        default=None,
        alias="VatCurrAmount",
        json_schema_extra={
            "source": "mocks/ifs/seed.json: ManSuppInvoiceSet; docs/CONVENTIONS.md (Decimal)"
        },
    )
    gross_curr_amount: Decimal | None = Field(
        default=None,
        alias="GrossCurrAmount",
        json_schema_extra={
            "source": "mocks/ifs/seed.json: ManSuppInvoiceSet; docs/CONVENTIONS.md (Decimal)"
        },
    )
    objstate: str | None = Field(
        default=None,
        alias="Objstate",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: ManSuppInvoiceSet; mocks/ifs/seed.json"
        },
    )
    supplier_datalift_id: str = Field(
        min_length=1,
        description="Required relation invoice → supplier (ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )
    purchase_order_datalift_id: str | None = Field(
        default=None,
        description="Optional relation invoice → purchase order (ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )
    lines: list[InvoiceLine] = Field(
        default_factory=list,
        description="Invoice lines (1:N relation, ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )
