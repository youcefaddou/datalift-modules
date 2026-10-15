from datetime import datetime

from fastapi.testclient import TestClient

from mocks.progessi.app import HOURS_PER_DAY, create_app

BASE = "/api/control/rest"


def client() -> TestClient:
    return TestClient(create_app())


def test_get_list_filters_on_dotted_paths() -> None:
    body = client().get(f"{BASE}/profiles", params={"partyIdentifications.idValue": "EMP-0003"})
    assert [p["partyId"] for p in body.json()] == ["10002"]


def test_get_one_and_404() -> None:
    c = client()
    assert c.get(f"{BASE}/profiles/10000").json()["lastName"] == "Fictif"
    assert c.get(f"{BASE}/profiles/99999").status_code == 404
    assert c.get(f"{BASE}/unknown").status_code == 404


def test_timesheet_has_one_entry_per_worked_day() -> None:
    sheet = client().get(f"{BASE}/timesheets/TSH-1000").json()
    assert sheet["fromDate"] == "2026-10-01T00:00:00Z"
    assert sheet["thruDate"] == "2026-10-31T23:59:59Z"
    assert len(sheet["timeEntries"]) == 10
    assert {e["hours"] for e in sheet["timeEntries"]} == {HOURS_PER_DAY}


def test_post_search_with_filter_sort_and_paging() -> None:
    body = {
        "filterModel": {
            "statusId": {"filterType": "text", "type": "equals", "filter": "TIMESHEET_APPROVED"}
        },
        "sortModel": [{"colId": "partyId", "sort": "desc"}],
    }
    page0 = client().post(f"{BASE}/timesheets", params={"pageNumber": 0, "pageSize": 2}, json=body)
    assert [t["partyId"] for t in page0.json()] == ["10002", "10001"]
    page1 = client().post(f"{BASE}/timesheets", params={"pageNumber": 1, "pageSize": 2}, json=body)
    assert [t["partyId"] for t in page1.json()] == ["10000"]


def test_unsupported_filter_type_is_rejected() -> None:
    body = {"filterModel": {"partyId": {"filterType": "text", "type": "contains", "filter": "1"}}}
    assert client().post(f"{BASE}/timesheets", json=body).status_code == 400


def test_seed_respects_progessi_rules() -> None:
    c = client()
    assigned = {
        (p["workEffortId"], a["partyId"])
        for p in c.get(f"{BASE}/projects").json()
        for a in p["partyAssignments"]
    }
    for sheet in c.get(f"{BASE}/timesheets").json():
        month = sheet["fromDate"][:7]
        for entry in sheet["timeEntries"]:
            assert (entry["workEffortId"], sheet["partyId"]) in assigned, entry
            day = datetime.fromisoformat(entry["fromDate"])
            assert entry["fromDate"].startswith(month) and day.weekday() < 5, entry
