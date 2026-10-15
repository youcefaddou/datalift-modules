# Mock IFS Cloud

API OData simulée, construite à partir de la structure publique d'IFS Cloud. Ce qui est vérifié et ce qui est reconstitué : `mocks/specs/ifs/SOURCE.md`.

```bash
uv run uvicorn mocks.ifs.app:app --port 8001
TOKEN=$(curl -s -d grant_type=client_credentials -d client_id=datalift-mock -d client_secret=datalift-mock-secret \
  http://localhost:8001/auth/realms/datalift/protocol/openid-connect/token | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8001/main/ifsapplications/projection/v1/PurchaseOrderHandling.svc/PurchaseOrderSet?\$top=2"
```

Authentification OAuth2 *client credentials* comme IFS (jeton valable 1 h, découverte via `/auth/realms/datalift/.well-known/openid-configuration`). Identifiants du mock modifiables par `IFS_MOCK_CLIENT_ID` / `IFS_MOCK_CLIENT_SECRET`.

Collections : clients, fournisseurs, commandes d'achat et lignes, factures fournisseurs manuelles, personnes, collaborateurs, projets (détail dans `SOURCE.md`). Ajouter une collection : une entrée dans `ENTITY_SETS` (`app.py`) et ses données fictives dans `seed.json`.

Pris en charge : document de service `{Projection}.svc/`, liste avec `$filter` (`Champ eq valeur` reliés par `and`, énumérations au format `IfsApp.<Projection>.<Type>'Valeur'`), `$select`, `$orderby`, `$top`, `$skip` et `@odata.nextLink`, `$expand` refusé (`ODP_NOT_IMPLEMENTED`) comme dans IFS ; lecture par clé `ManSuppInvoiceSet(Company='DL01',InvoiceId=1001)` ; navigation `.../ManSuppInvoiceItems` ; `POST` (champs obligatoires, identifiant auto-généré, doublon refusé, erreurs `DATABASE_ERROR` / `ORA-…` comme IFS) ; `PATCH` avec `If-Match` obligatoire (ETag lu par un `GET` sur la clé, ou `*`). Chaque ligne porte `@odata.etag`, `luname`, `keyref` et `Objgrants`. Données en mémoire, remises à zéro à chaque démarrage.
