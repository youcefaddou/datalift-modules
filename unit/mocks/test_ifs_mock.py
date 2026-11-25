from fastapi.testclient import TestClient

from mocks.ifs.app import CLIENT_ID, CLIENT_SECRET, ENTITY_SETS, TOKEN_PATH, create_app

ROOT = "/main/ifsapplications/projection/v1"
PROJECTS = f"{ROOT}/ProjectManagementHandling.svc/ProjectSet"
ORDERS = f"{ROOT}/PurchaseOrderHandling.svc/PurchaseOrderSet"
INVOICES = f"{ROOT}/ManualSupplierInvoiceHandling.svc/ManSuppInvoiceSet"
CUSTOMERS = f"{ROOT}/CustomerHandling.svc/CustomerInfoSet"
PO_STATE = "IfsApp.PurchaseOrderHandling.PurchaseOrderState"


def token(c: TestClient) -> str:
    form = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    return c.post(TOKEN_PATH, data=form).json()["access_token"]


def client() -> TestClient:
    c = TestClient(create_app())
    c.headers["Authorization"] = f"Bearer {token(c)}"
    return c


# Authentication


def test_requests_without_valid_token_are_401() -> None:
    c = TestClient(create_app())
    assert c.get(PROJECTS).status_code == 401
    assert c.get(PROJECTS, headers={"Authorization": "Bearer nope"}).status_code == 401


def test_token_endpoint_rejects_bad_credentials_and_is_discoverable() -> None:
    c = TestClient(create_app())
    bad = {"grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": "x"}
    assert c.post(TOKEN_PATH, data=bad).status_code == 401
    config = c.get(
        TOKEN_PATH.replace("protocol/openid-connect/token", ".well-known/openid-configuration")
    )
    assert config.json()["token_endpoint"].endswith(TOKEN_PATH)
    assert (
        c.post(TOKEN_PATH, data={**bad, "client_secret": CLIENT_SECRET}).json()["expires_in"]
        == 3600
    )


# Reading


def test_service_document_lists_entity_sets() -> None:
    names = [s["name"] for s in client().get(f"{ROOT}/PurchaseOrderHandling.svc/").json()["value"]]
    assert names == ["PurchaseOrderSet", "PurchaseOrderLineNopartSet"]


def test_list_returns_odata_envelope_and_next_link() -> None:
    c = client()
    body = c.get(PROJECTS, params={"$top": 1}).json()
    assert body["@odata.context"].endswith("$metadata#ProjectSet")
    assert len(body["value"]) == 1 and "$skip=1" in body["@odata.nextLink"]
    assert "@odata.nextLink" not in c.get(PROJECTS, params={"$top": 100}).json()


def test_filter_select_and_orderby() -> None:
    params = {"$filter": "Company eq 'DL01'", "$select": "ProjectId", "$orderby": "ProjectId desc"}
    rows = client().get(PROJECTS, params=params).json()["value"]
    assert rows == [{"ProjectId": "PRJ-0002"}, {"ProjectId": "PRJ-0001"}]


def test_enum_filter_requires_qualified_type() -> None:
    c = client()
    ok = c.get(ORDERS, params={"$filter": f"Objstate eq {PO_STATE}'Released'"})
    assert ok.status_code == 200 and ok.json()["value"]
    assert c.get(ORDERS, params={"$filter": "Objstate eq 'Released'"}).status_code == 400


def test_expand_is_not_implemented_like_ifs() -> None:
    response = client().get(INVOICES, params={"$expand": "ManSuppInvoiceItems"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "ODP_NOT_IMPLEMENTED"


def test_unsupported_filter_is_rejected() -> None:
    assert client().get(PROJECTS, params={"$filter": "contains(Name,'x')"}).status_code == 400


def test_get_by_composite_numeric_key_and_navigation() -> None:
    c = client()
    invoice = c.get(f"{INVOICES}(Company='DL01',InvoiceId=1001)").json()
    assert invoice["InvoiceNo"] == "FAC-FICT-0001" and "ManSuppInvoiceItems" not in invoice
    items = c.get(f"{INVOICES}(Company='DL01',InvoiceId=1001)/ManSuppInvoiceItems").json()
    assert len(items["value"]) == 2
    assert c.get(f"{INVOICES}(Company='DL01',InvoiceId=1001)/Nope").status_code == 404
    assert c.get(f"{PROJECTS}(ProjectId='NOPE')").status_code == 404
    assert c.get(f"{ROOT}/ProjectManagementHandling.svc/Unknown").status_code == 404


def test_every_declared_entity_set_is_served() -> None:
    c = client()
    for projection, entity_set in ENTITY_SETS:
        assert c.get(f"{ROOT}/{projection}.svc/{entity_set}").json()["value"], entity_set


# Writing

CUSTOMER = {
    "Name": "Client Fictif",
    "CreationDate": "2026-10-15",
    "DefaultDomain": True,
    "DefaultLanguage": "fr",
    "Country": "FR",
    "PartyType": "Customer",
    "OneTime": False,
    "CustomerCategory": "Prospect",
    "B2bCustomer": False,
    "ValidDataProcessingPurpose": True,
    "CountryCode": "FR",
}


def test_rows_carry_ifs_metadata() -> None:
    invoice = client().get(f"{INVOICES}(Company='DL01',InvoiceId=1001)").json()
    assert invoice["luname"] == "ManSuppInvoice"
    assert invoice["keyref"] == "COMPANY=DL01^INVOICE_ID=1001^"
    assert invoice["@odata.etag"].startswith('W/"') and invoice["Objgrants"] is None


def test_create_customer_like_ifs() -> None:
    c = client()
    created = c.post(CUSTOMERS, json=CUSTOMER)
    body = created.json()
    assert created.status_code == 201
    assert body["@odata.context"].endswith("$metadata#CustomerInfoSet/$entity")
    assert body["CustomerId"] and body["keyref"] == f"CUSTOMER_ID={body['CustomerId']}^"
    assert body["IdentifierRefValidation"] == "None"
    duplicate = c.post(CUSTOMERS, json={**CUSTOMER, "CustomerId": body["CustomerId"]})
    assert duplicate.status_code == 500 and duplicate.json()["error"]["code"] == "DATABASE_ERROR"


def test_missing_mandatory_field_is_an_ifs_database_error() -> None:
    response = client().post(CUSTOMERS, json={**CUSTOMER, "Name": None})
    error = response.json()["error"]
    assert response.status_code == 500 and error["code"] == "DATABASE_ERROR"
    assert error["details"][0] == {
        "code": 20124,
        "message": "ORA-20124: Error.NULLVALUE: Field [Name] is mandatory for Customer Info "
        "and requires a value.",
    }


def test_unknown_enum_value_is_rejected() -> None:
    assert client().post(CUSTOMERS, json={**CUSTOMER, "PartyType": "Alien"}).status_code == 400


def test_patch_requires_if_match_etag() -> None:
    c = client()
    url = f"{INVOICES}(Company='DL01',InvoiceId=1001)"
    assert c.patch(url, json={"PayTermId": "45"}).status_code == 428
    etag = c.get(url).json()["@odata.etag"]
    patched = c.patch(url, json={"PayTermId": "45"}, headers={"If-Match": etag})
    assert patched.status_code == 200 and patched.json()["PayTermId"] == "45"
    assert c.patch(url, json={"PayTermId": "60"}, headers={"If-Match": etag}).status_code == 412
    assert c.patch(url, json={"PayTermId": "60"}, headers={"If-Match": "*"}).status_code == 200


def test_create_invoice_item() -> None:
    c = client()
    url = f"{INVOICES}(Company='DL01',InvoiceId=1001)/ManSuppInvoiceItems"
    item = {"ItemId": 3, "Description": "Ligne fictive", "NetCurrAmount": 10}
    assert c.post(url, json=item).status_code == 201
    assert len(c.get(url).json()["value"]) == 3


def test_error_codes_match_ifs() -> None:
    c = client()
    missing = c.get(f"{PROJECTS}(ProjectId='NOPE')").json()["error"]["code"]
    assert missing == "ODP_RESOURCE_NOTFOUND"
    bad_body = c.post(CUSTOMERS, content="not json", headers={"Content-Type": "application/json"})
    assert bad_body.json() == {
        "error": {
            "code": "ODP_DESERIALIZATION_ERROR",
            "message": "Error while de-serializing contents.",
        }
    }
    assert c.patch(PROJECTS, json={}).json()["error"]["code"] == "ODP_NOT_ALLOWED"
