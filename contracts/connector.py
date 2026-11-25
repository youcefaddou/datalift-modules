"""Connector interface shared by every DataLift connector (ADR-004).

A connector reads raw records from one software API (they land in bronze) and writes
records to it (flow targets). It knows nothing about the common model: mapping to silver
happens in the pipelines. Adding a software = one new subclass, no change to the core.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

Record = dict[str, Any]
"""One raw record, with the field names of the source API."""


class ConnectorError(Exception):
    """Base connector error. `retryable` tells the orchestrator whether retrying can succeed."""

    retryable = False


class AuthenticationError(ConnectorError):
    """Credentials missing, invalid or expired."""


class RateLimitError(ConnectorError):
    """The API asked to slow down."""

    retryable = True


class SourceUnavailableError(ConnectorError):
    """Network error, timeout or 5xx answer."""

    retryable = True


class UnknownObjectTypeError(ConnectorError):
    """The connector does not handle this object type."""


@dataclass(frozen=True)
class Page:
    """One page of a read. `next_cursor` is None on the last page."""

    records: list[Record]
    next_cursor: str | None = None


@dataclass(frozen=True)
class WriteResult:
    """Outcome of a write, per source id: accepted, or rejected with the target's reason."""

    written: list[str] = field(default_factory=list)
    rejected: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class HealthStatus:
    ok: bool
    detail: str = ""


class Connector(ABC):
    """Base class of all connectors. Subclasses set `source_system` (e.g. "ifs")."""

    source_system: str

    @abstractmethod
    def read_page(self, object_type: str, cursor: str | None = None, page_size: int = 100) -> Page:
        """Read one page. `cursor` is None for the first page, then the previous `next_cursor`."""

    def read(self, object_type: str, page_size: int = 100) -> Iterator[Record]:
        """Read every record of `object_type`, page after page."""
        cursor = None
        while True:
            page = self.read_page(object_type, cursor, page_size)
            yield from page.records
            if page.next_cursor is None:
                return
            cursor = page.next_cursor

    @abstractmethod
    def write(self, object_type: str, records: Sequence[Record]) -> WriteResult:
        """Write records to the target. Must be idempotent: replaying a write creates no
        duplicate (rule 5), e.g. by upserting on the source id."""

    @abstractmethod
    def describe_schema(self, object_type: str) -> dict[str, Any]:
        """JSON Schema of the raw records of `object_type`, as the API exposes them."""

    @abstractmethod
    def health_check(self) -> HealthStatus:
        """Cheap call telling whether the API is reachable with the current credentials."""
