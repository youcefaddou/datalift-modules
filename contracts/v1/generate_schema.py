"""Regenerate the checked-in JSON Schema for common contracts v1."""

import json
from pathlib import Path

from contracts.v1 import (
    CONTRACT_VERSION,
    Employee,
    InvoiceLine,
    Project,
    PurchaseOrder,
    Supplier,
    SupplierInvoice,
    TimeEntry,
)

MODELS = {
    model.__name__: model
    for model in (
        Supplier,
        PurchaseOrder,
        SupplierInvoice,
        InvoiceLine,
        Employee,
        Project,
        TimeEntry,
    )
}


def main() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "DataLift common contracts v1",
        "version": CONTRACT_VERSION,
        "models": {name: model.model_json_schema(by_alias=True) for name, model in MODELS.items()},
    }
    output = Path(__file__).with_name("schema.json")
    output.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
