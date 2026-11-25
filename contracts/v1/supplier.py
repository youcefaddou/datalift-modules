"""Supplier contract. Source fields follow the IFS SupplierInfoGeneralSet mock schema."""

from pydantic import Field

from contracts.v1.base import CommonModel


class Supplier(CommonModel):
    """Supplier master data. Keep only fields present in the checked-in source schema."""

    supplier_id: str = Field(
        alias="SupplierId",
        min_length=1,
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: SuppliersHandling/SupplierInfoGeneralSet; mocks/ifs/seed.json"
        },
    )
    name: str | None = Field(
        default=None,
        alias="Name",
        json_schema_extra={"source": "mocks/ifs/seed.json: SupplierInfoGeneralSet"},
    )
    country: str | None = Field(
        default=None,
        alias="Country",
        json_schema_extra={"source": "mocks/ifs/seed.json: SupplierInfoGeneralSet"},
    )
    default_language: str | None = Field(
        default=None,
        alias="DefaultLanguage",
        json_schema_extra={"source": "mocks/ifs/seed.json: SupplierInfoGeneralSet"},
    )
