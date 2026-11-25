"""Ontology of the common model: links, actions, identity map, flow definition (ADR-005, DL-113).

Links say how silver objects join (foreign key to the linked object's datalift_id).
Actions are the only writes to a target software: an object failing a precondition is set
aside with the precondition's name as reason. A flow references an action, never a free target.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from contracts.v1.base import CommonModel
from contracts.v1.employee import Employee
from contracts.v1.project import Project
from contracts.v1.purchase_order import PurchaseOrder
from contracts.v1.supplier import Supplier
from contracts.v1.supplier_invoice import InvoiceLine, SupplierInvoice
from contracts.v1.time_entry import TimeEntry

# Identity map -------------------------------------------------------------------

SILVER_IDENTITY_MAP_DDL = """
CREATE TABLE IF NOT EXISTS silver_identity_map (
    object_type   text        NOT NULL,
    datalift_id   text        NOT NULL,
    source_system text        NOT NULL,
    source_id     text        NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (object_type, datalift_id, source_system),
    UNIQUE (object_type, source_system, source_id)
);
"""


class IdentityMapRow(BaseModel):
    """One row of silver_identity_map: a source record and the DataLift id it belongs to."""

    object_type: str = Field(min_length=1)
    datalift_id: str = Field(min_length=1)
    source_system: str = Field(min_length=1)
    source_id: str = Field(min_length=1)


class IdentityMap:
    """In-memory view of silver_identity_map, with the same uniqueness rule as the table."""

    def __init__(self) -> None:
        self._ids: dict[tuple[str, str, str], str] = {}

    def add(self, row: IdentityMapRow) -> None:
        key = (row.object_type, row.source_system, row.source_id)
        known = self._ids.get(key)
        if known is not None and known != row.datalift_id:
            raise ValueError(f"{key} already mapped to {known}, not {row.datalift_id}")
        self._ids[key] = row.datalift_id

    def resolve(self, object_type: str, source_system: str, source_id: str) -> str | None:
        return self._ids.get((object_type, source_system, source_id))

    def exists_in(self, datalift_id: str, source_system: str) -> bool:
        return any(dl == datalift_id and k[1] == source_system for k, dl in self._ids.items())


# Links --------------------------------------------------------------------------


@dataclass(frozen=True)
class Link:
    name: str
    source: type[CommonModel]
    target: type[CommonModel]
    cardinality: Literal["N:1", "1:N"]
    required: bool
    fk_model: type[CommonModel]  # model holding the foreign key column
    fk_field: str
    match_on: str  # source fields used to resolve the link, from the specs


LINKS: list[Link] = [
    Link("supplier", SupplierInvoice, Supplier, "N:1", True, SupplierInvoice, "supplier_datalift_id",
         "IFS ManSuppInvoice.Identity = SupplierInfoGeneral.SupplierId"),
    Link("purchase_order", SupplierInvoice, PurchaseOrder, "N:1", False, SupplierInvoice,
         "purchase_order_datalift_id", "Yooz order number = IFS PurchaseOrder.OrderNo"),
    Link("lines", SupplierInvoice, InvoiceLine, "1:N", True, InvoiceLine, "supplier_invoice_datalift_id",
         "IFS navigation ManSuppInvoiceItems"),
    Link("supplier", PurchaseOrder, Supplier, "N:1", True, PurchaseOrder, "supplier_datalift_id",
         "IFS PurchaseOrder.VendorNo = SupplierInfoGeneral.SupplierId"),
    Link("employee", TimeEntry, Employee, "N:1", True, TimeEntry, "employee_datalift_id",
         "Progessi partyIdentifications PAYROLL_ID = IFS CompanyPerson.EmpNo"),
    Link("project", TimeEntry, Project, "N:1", True, TimeEntry, "project_datalift_id",
         "Progessi WorkEffort.reference = IFS Project.ProjectId"),
]  # fmt: skip


# Actions ------------------------------------------------------------------------


@dataclass
class ActionContext:
    """Facts the pipeline gives the preconditions, beyond the object itself."""

    identity_map: IdentityMap
    approved: set[str] = field(default_factory=set)  # datalift_ids approved in their source
    order_totals: dict[str, Decimal] = field(default_factory=dict)  # PO datalift_id -> net amount


@dataclass(frozen=True)
class Precondition:
    name: str  # also the reason given when the object is set aside
    check: Callable[[CommonModel, ActionContext], bool]


@dataclass(frozen=True)
class Action:
    name: str
    object_type: type[CommonModel]
    target: str
    effect: str
    preconditions: tuple[Precondition, ...]

    def failed(self, obj: CommonModel, ctx: ActionContext) -> list[str]:
        """Names of the preconditions `obj` fails; empty list = the action can run."""
        if not isinstance(obj, self.object_type):
            raise TypeError(f"{self.name} applies to {self.object_type.__name__}")
        return [p.name for p in self.preconditions if not p.check(obj, ctx)]


ACTIONS: dict[str, Action] = {
    a.name: a
    for a in (
        Action("send_invoice_to_ifs", SupplierInvoice, "ifs", "Create the supplier invoice in IFS", (
            Precondition("validated_in_yooz", lambda o, c: o.datalift_id in c.approved),
            Precondition("linked_to_order", lambda o, c: o.purchase_order_datalift_id is not None),
            Precondition("matches_order", lambda o, c: o.net_curr_amount is not None
                         and c.order_totals.get(o.purchase_order_datalift_id) == o.net_curr_amount),
        )),
        Action("sync_employee_to_ifs", Employee, "ifs", "Create, update or close the employee in IFS", (
            Precondition("from_lucca", lambda o, c: o.source_system == "lucca"),
        )),
        Action("send_time_entry_to_ifs", TimeEntry, "ifs", "Create the time entry in IFS", (
            Precondition("timesheet_approved", lambda o, c: o.datalift_id in c.approved),
            Precondition("employee_in_ifs", lambda o, c: c.identity_map.exists_in(o.employee_datalift_id, "ifs")),
        )),
    )
}  # fmt: skip


# Flow definition ----------------------------------------------------------------


class FlowDefinition(BaseModel):
    """A flow points to an action (ADR-005) and runs only once validated by a human (rule 4)."""

    name: str = Field(min_length=1)
    source_system: str = Field(min_length=1)
    object_type: str = Field(min_length=1)
    filter: dict[str, str] = Field(default_factory=dict)
    mappings: dict[str, str] = Field(default_factory=dict)  # source field -> common model field
    action: str
    schedule: str | None = None  # cron expression, None = run on demand
    validation_status: Literal["proposed", "validated", "rejected"] = "proposed"

    @model_validator(mode="after")
    def _known_action(self) -> "FlowDefinition":
        action = ACTIONS.get(self.action)
        if action is None:
            raise ValueError(f"unknown action {self.action!r}; known: {sorted(ACTIONS)}")
        if action.object_type.__name__ != self.object_type:
            raise ValueError(
                f"{self.action} applies to {action.object_type.__name__}, not {self.object_type}"
            )
        return self

    @property
    def executable(self) -> bool:
        return self.validation_status == "validated"
