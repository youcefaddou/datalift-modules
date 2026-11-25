"""Contract checks every connector must pass (DL-36). Call them from each connector's tests."""

from collections.abc import Sequence

from contracts.connector import Connector, HealthStatus, Record, WriteResult


def assert_connector_contract(
    connector: Connector, object_type: str, records: Sequence[Record], id_field: str
) -> None:
    """Check `connector` against the interface, using `records` (at least 3, unique `id_field`)."""
    assert len(records) >= 3, "need at least 3 records to exercise pagination"
    assert connector.source_system, "source_system must be set"

    health = connector.health_check()
    assert isinstance(health, HealthStatus) and health.ok, health

    schema = connector.describe_schema(object_type)
    assert schema.get("type") == "object" and id_field in schema.get("properties", {}), schema

    before = {r[id_field] for r in connector.read(object_type)}
    result = connector.write(object_type, records)
    assert isinstance(result, WriteResult)
    assert set(result.written) == {str(r[id_field]) for r in records}, result

    replay = connector.write(object_type, records)
    assert not replay.rejected, replay
    ids = [r[id_field] for r in connector.read(object_type, page_size=2)]
    assert len(ids) == len(set(ids)), "replaying a write created duplicates (rule 5)"
    assert set(ids) == before | {r[id_field] for r in records}, ids
