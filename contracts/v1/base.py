"""Base fields shared by all silver contract objects."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommonModel(BaseModel):
    """Common silver identity and lineage fields (ADR-005, conventions)."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    datalift_id: str = Field(
        min_length=1,
        description="Stable DataLift identity; resolved through silver_identity_map (ADR-005).",
        json_schema_extra={"source": "docs/decisions/ADR-005-ontologie-liens-actions.md"},
    )
    source_system: str = Field(
        min_length=1,
        description="Source software identifier.",
        json_schema_extra={"source": "docs/CONVENTIONS.md"},
    )
    source_id: str = Field(
        min_length=1,
        description="Identifier of the record in its source software.",
        json_schema_extra={"source": "docs/CONVENTIONS.md"},
    )
    extracted_at: datetime = Field(
        description="UTC timestamp of extraction (ISO 8601).",
        json_schema_extra={"source": "docs/CONVENTIONS.md"},
    )
