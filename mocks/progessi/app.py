"""Progessi read API mock, modelled on the public Apache OFBiz data model.

What is verified vs reconstructed: mocks/specs/progessi/SOURCE.md.
"""

import calendar
import copy
import json
from pathlib import Path
from typing import Annotated, Any

from fastapi import Body, FastAPI, HTTPException, Request

BASE = "/api/control/rest"
HOURS_PER_DAY = 7.0
DEFAULT_PAGE_SIZE = 100
ID_FIELDS = {"profiles": "partyId", "projects": "workEffortId", "timesheets": "timesheetId"}


def _timesheet(raw: dict[str, Any]) -> dict[str, Any]:
    """Expand a compact monthly sheet (lines of worked days) into OFBiz TimeEntry rows."""
    year, month = raw["year"], raw["month"]
    prefix = f"{year}-{month:02d}"
    days = [(line["workEffortId"], day) for line in raw["lines"] for day in line["days"]]
    entries = [
        {
            "timeEntryId": f"{raw['timesheetId']}-{n:03d}",
            "timesheetId": raw["timesheetId"],
            "partyId": raw["partyId"],
            "workEffortId": work_effort_id,
            "fromDate": f"{prefix}-{day:02d}T00:00:00Z",
            "thruDate": f"{prefix}-{day:02d}T23:59:59Z",
            "hours": HOURS_PER_DAY,
        }
        for n, (work_effort_id, day) in enumerate(days, start=1)
    ]
    return {
        "timesheetId": raw["timesheetId"],
        "partyId": raw["partyId"],
        "fromDate": f"{prefix}-01T00:00:00Z",
        "thruDate": f"{prefix}-{calendar.monthrange(year, month)[1]:02d}T23:59:59Z",
        "statusId": raw["statusId"],
        "timeEntries": entries,
    }


def _load_seed() -> dict[str, list[dict[str, Any]]]:
    data = json.loads((Path(__file__).parent / "seed.json").read_text())
    data["timesheets"] = [_timesheet(t) for t in data["timesheets"]]
    return data


SEED = _load_seed()


def _values(obj: Any, path: list[str]) -> list[Any]:
    """Values at a dotted path, flattening lists (`partyIdentifications.idValue`)."""
    if isinstance(obj, list):
        return [v for item in obj for v in _values(item, path)]
    if not path:
        return [obj]
    if not isinstance(obj, dict):
        return []
    return _values(obj.get(path[0]), path[1:])


def _matches(row: dict[str, Any], path: str, value: str) -> bool:
    return value in {str(v) for v in _values(row, path.split("."))}


def _paginate(rows: list[dict[str, Any]], page_number: int, page_size: int) -> list[dict[str, Any]]:
    start = page_number * page_size
    return rows[start : start + page_size]


def create_app() -> FastAPI:
    store = copy.deepcopy(SEED)
    app = FastAPI(title="Progessi read API mock (reconstructed from OFBiz)")

    def rows_of(resource: str) -> list[dict[str, Any]]:
        if resource not in store:
            raise HTTPException(404, f"Unknown resource: {resource}")
        return store[resource]

    @app.get(BASE + "/{resource}")
    def list_all(resource: str, request: Request) -> list[dict[str, Any]]:
        params = dict(request.query_params)
        page_number = int(params.pop("pageNumber", 0))
        page_size = int(params.pop("pageSize", DEFAULT_PAGE_SIZE))
        rows = [r for r in rows_of(resource) if all(_matches(r, p, v) for p, v in params.items())]
        return _paginate(rows, page_number, page_size)

    @app.post(BASE + "/{resource}")
    def search(
        resource: str,
        body: Annotated[dict[str, Any] | None, Body()] = None,
        pageNumber: int = 0,
        pageSize: int = DEFAULT_PAGE_SIZE,
    ) -> list[dict[str, Any]]:
        rows, body = rows_of(resource), body or {}
        for path, condition in (body.get("filterModel") or {}).items():
            # ponytail: AG Grid "equals" only; add other filter types when a connector needs them.
            if condition.get("type") != "equals":
                raise HTTPException(400, f"Unsupported filter type: {condition.get('type')}")
            rows = [r for r in rows if _matches(r, path, str(condition.get("filter")))]
        for sort in reversed(body.get("sortModel") or []):
            rows = sorted(
                rows,
                key=lambda r, col=sort["colId"]: str((_values(r, col.split(".")) or [""])[0]),
                reverse=sort.get("sort") == "desc",
            )
        return _paginate(rows, pageNumber, pageSize)

    @app.get(BASE + "/{resource}/{item_id}")
    def get_one(resource: str, item_id: str) -> dict[str, Any]:
        id_field = ID_FIELDS.get(resource, "")
        for row in rows_of(resource):
            if str(row.get(id_field)) == item_id:
                return row
        raise HTTPException(404, f"{resource}/{item_id} not found")

    return app


app = create_app()
