"""Purchase order contract based on the documented IFS PurchaseOrderSet fields."""

from datetime import date

from pydantic import Field

from contracts.v1.base import CommonModel


class PurchaseOrder(CommonModel):
    order_no: str = Field(
        alias="OrderNo",
        min_length=1,
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    vendor_no: str = Field(
        alias="VendorNo",
        min_length=1,
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    order_date: date | None = Field(
        default=None,
        alias="OrderDate",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    objstate: str | None = Field(
        default=None,
        alias="Objstate",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    contract: str | None = Field(
        default=None,
        alias="Contract",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    buyer_code: str | None = Field(
        default=None,
        alias="BuyerCode",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    authorize_code: str | None = Field(
        default=None,
        alias="AuthorizeCode",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    currency_code: str | None = Field(
        default=None,
        alias="CurrencyCode",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    company: str | None = Field(
        default=None,
        alias="Company",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: PurchaseOrderHandling/PurchaseOrderSet"
        },
    )
    supplier_datalift_id: str = Field(
        min_length=1,
        description="Relation purchase_order → supplier (ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )
