# Mock Progessi

API de lecture simulée de Progessi (source du flux 3), calquée sur le modèle de données d'Apache OFBiz. Ce qui est vérifié et ce qui est reconstitué : `mocks/specs/progessi/SOURCE.md`.

```bash
uv run uvicorn mocks.progessi.app:app --port 8002
curl "http://localhost:8002/api/control/rest/timesheets?statusId=TIMESHEET_APPROVED"
curl "http://localhost:8002/api/control/rest/profiles?partyIdentifications.idValue=EMP-0001"
```

Ressources : `profiles`, `projects` (projets et sous-projets, avec affectations), `timesheets` (feuilles mensuelles, une ligne `timeEntries` par jour pointé de 7 h). Lecture par identifiant : `/{ressource}/{id}`. Recherche : `POST /{ressource}?pageNumber=0&pageSize=50` avec `filterModel` (`equals`) et `sortModel`.

Données fictives dans `seed.json`, remises à zéro à chaque démarrage. Les feuilles y sont décrites en compact (jours pointés par projet) puis développées en lignes OFBiz. Cohérence avec le mock IFS : `reference` `PRJ-0001` / `PRJ-0002` = `ProjectId` IFS, matricules `EMP-0001` / `EMP-0002` présents dans IFS, `EMP-0003` absent (cas « mise de côté » du flux 3).
