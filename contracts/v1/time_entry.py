"""Time entry contract based on the Progessi/OFBiz TimeEntry source model."""

from datetime import datetime
from decimal import Decimal
from pydantic import Field

from contracts.v1.base import CommonModel


class TimeEntry(CommonModel):
    time_entry_id: str = Field(alias="timeEntryId", min_length=1, json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: TimeEntry"})
    timesheet_id: str | None = Field(default=None, alias="timesheetId", json_schema_extra={"source": "mocks/progessi/app.py: expanded Timesheet/TimeEntry response"})
    party_id: str | None = Field(default=None, alias="partyId", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: Timesheet.partyId"})
    work_effort_id: str = Field(alias="workEffortId", min_length=1, json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: TimeEntry"})
    from_date: datetime = Field(alias="fromDate", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: TimeEntry"})
    thru_date: datetime = Field(alias="thruDate", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: TimeEntry"})
    hours: Decimal = Field(ge=0, json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: TimeEntry; docs/CONVENTIONS.md (decimal values)"})
    employee_datalift_id: str = Field(min_length=1, description="Relation time entry → employee (ADR-005).", json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"})
    project_datalift_id: str = Field(min_length=1, description="Relation time entry → project (ADR-005).", json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"})
