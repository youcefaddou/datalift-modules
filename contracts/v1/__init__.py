"""DataLift common data contracts, schema version 1."""

from contracts.v1.base import CommonModel
from contracts.v1.employee import Employee
from contracts.v1.project import Project
from contracts.v1.purchase_order import PurchaseOrder
from contracts.v1.supplier import Supplier
from contracts.v1.supplier_invoice import InvoiceLine, SupplierInvoice
from contracts.v1.time_entry import TimeEntry

__all__ = [
    "CommonModel",
    "Employee",
    "InvoiceLine",
    "Project",
    "PurchaseOrder",
    "Supplier",
    "SupplierInvoice",
    "TimeEntry",
]

CONTRACT_VERSION = "1.0.0"
