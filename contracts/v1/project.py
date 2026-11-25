"""Project contract based on the Progessi/OFBiz WorkEffort source model."""

from pydantic import Field

from contracts.v1.base import CommonModel


class Project(CommonModel):
    work_effort_id: str = Field(alias="workEffortId", min_length=1, json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: WorkEffort"})
    work_effort_type_id: str | None = Field(default=None, alias="workEffortTypeId", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: WorkEffort"})
    work_effort_parent_id: str | None = Field(default=None, alias="workEffortParentId", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: WorkEffort"})
    work_effort_name: str | None = Field(default=None, alias="workEffortName", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: WorkEffort"})
    current_status_id: str | None = Field(default=None, alias="currentStatusId", json_schema_extra={"source": "mocks/specs/progessi/SOURCE.md: WorkEffort"})
    reference: str | None = Field(default=None, json_schema_extra={"source": "mocks/progessi/seed.json: projects"})
