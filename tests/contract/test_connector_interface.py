"""DL-36: a fake in-memory connector implements the interface and passes the contract."""

from collections.abc import Sequence
from typing import Any

import pytest

from contracts.connector import (
    Connector,
    ConnectorError,
    HealthStatus,
    Page,
    RateLimitError,
    Record,
    UnknownObjectTypeError,
    WriteResult,
)
from contracts.connector_contract import assert_connector_contract

SUPPLIER_SCHEMA = {
    "type": "object",
    "properties": {"SupplierId": {"type": "string"}, "Name": {"type": "string"}},
    "required": ["SupplierId"],
}


class FakeConnector(Connector):
    """In-memory connector: upserts on SupplierId, offset cursor pagination."""

    source_system = "fake"

    def __init__(self) -> None:
        self.rows: dict[str, Record] = {}

    def _check(self, object_type: str) -> None:
        if object_type != "suppliers":
            raise UnknownObjectTypeError(object_type)

    def read_page(self, object_type: str, cursor: str | None = None, page_size: int = 100) -> Page:
        self._check(object_type)
        start = int(cursor or 0)
        rows = list(self.rows.values())
        end = start + page_size
        return Page(rows[start:end], str(end) if end < len(rows) else None)

    def write(self, object_type: str, records: Sequence[Record]) -> WriteResult:
        self._check(object_type)
        written, rejected = [], {}
        for r in records:
            if not r.get("Name"):
                rejected[str(r["SupplierId"])] = "Name is mandatory"
                continue
            self.rows[str(r["SupplierId"])] = dict(r)
            written.append(str(r["SupplierId"]))
        return WriteResult(written, rejected)

    def describe_schema(self, object_type: str) -> dict[str, Any]:
        self._check(object_type)
        return SUPPLIER_SCHEMA

    def health_check(self) -> HealthStatus:
        return HealthStatus(ok=True)


RECORDS = [{"SupplierId": f"SUP-{n}", "Name": f"Fournisseur fictif {n}"} for n in range(1, 6)]


def test_fake_connector_passes_the_contract() -> None:
    assert_connector_contract(FakeConnector(), "suppliers", RECORDS, "SupplierId")


def test_read_follows_cursors_across_pages() -> None:
    c = FakeConnector()
    c.write("suppliers", RECORDS)
    first = c.read_page("suppliers", page_size=2)
    assert len(first.records) == 2 and first.next_cursor == "2"
    assert [r["SupplierId"] for r in c.read("suppliers", page_size=2)] == [
        r["SupplierId"] for r in RECORDS
    ]


def test_write_reports_rejected_records() -> None:
    result = FakeConnector().write("suppliers", [{"SupplierId": "SUP-9", "Name": ""}])
    assert result.written == [] and result.rejected == {"SUP-9": "Name is mandatory"}


def test_errors_are_typed_and_say_if_retry_can_help() -> None:
    with pytest.raises(UnknownObjectTypeError):
        FakeConnector().read_page("invoices")
    assert RateLimitError.retryable and not UnknownObjectTypeError.retryable
    assert issubclass(RateLimitError, ConnectorError)


def test_interface_cannot_be_instantiated_without_all_operations() -> None:
    class Incomplete(Connector):
        source_system = "x"

    with pytest.raises(TypeError):
        Incomplete()  # type: ignore[abstract]


def test_contract_catches_a_non_idempotent_write() -> None:
    class Duplicating(FakeConnector):
        def write(self, object_type: str, records: Sequence[Record]) -> WriteResult:
            for r in records:
                self.rows[f"{r['SupplierId']}-{len(self.rows)}"] = dict(r)
            return WriteResult([str(r["SupplierId"]) for r in records])

    with pytest.raises(AssertionError, match="duplicates"):
        assert_connector_contract(Duplicating(), "suppliers", RECORDS, "SupplierId")
