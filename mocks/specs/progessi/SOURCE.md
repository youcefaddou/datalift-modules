# Source de la spécification

- Éditeur : Progessi (bâti sur Apache OFBiz)
- Format : **reconstitué** à partir du modèle de données public d'Apache OFBiz et de la description fonctionnelle de Youcef Addou (utilisateur quotidien)
- Lien vers la documentation officielle : aucune doc d'API publique ; modèle OFBiz : https://github.com/apache/ofbiz-framework/tree/trunk/applications/datamodel (licence Apache 2.0)
- Date de récupération : 2026-10-15
- Conditions d'utilisation vérifiées : oui pour OFBiz (Apache 2.0)
- Jetons et identifiants retirés de la collection : sans objet

`progessi.json` (extraits de la collection Postman interne) reste hors dépôt (`.gitignore`), conformément à `DATA_POLICY.md`.

## Ce qui vient d'OFBiz (vérifié)

| Ressource | Entités OFBiz | Champs |
|---|---|---|
| `timesheets` | `Timesheet`, `TimeEntry` | `timesheetId`, `partyId`, `fromDate`, `thruDate`, `statusId` (`TIMESHEET_IN_PROCESS`, `TIMESHEET_COMPLETED`, `TIMESHEET_APPROVED`) ; lignes `timeEntryId`, `workEffortId`, `fromDate`, `thruDate`, `hours` |
| `projects` | `WorkEffort`, `WorkEffortPartyAssignment` | `workEffortId`, `workEffortTypeId`, `workEffortParentId` (sous-projet), `workEffortName`, `currentStatusId` ; affectations `partyId`, `roleTypeId`, `fromDate`, `thruDate` |
| `profiles` | `Person`, `PartyIdentification`, `ContactMech` | `partyId`, `firstName`, `lastName`, `partyIdentifications` (`partyIdentificationTypeId`, `idValue`) |

## Ce qui vient du fonctionnement de Progessi (décrit par Youcef)

- Une feuille par mois et par collaborateur, des lignes par projet ou sous-projet, 1 jour pointé = 7 h.
- On ne peut pointer que sur un projet auquel le BM nous a affecté.
- Base `/api/control/rest`, `GET /{ressource}` filtrable par chemin pointé (`profile.partyId`), `POST /{ressource}` de recherche avec `filterModel` / `sortModel` (format AG Grid) et `pageNumber` / `pageSize`, réponses en tableau JSON.

## Ce qui est reconstitué

- Noms exacts `partyAssignments`, `timeEntries`, `reference`, type d'identifiant `PAYROLL_ID`, statut `PRJ_ACTIVE`, rôle `PROJECT_TEAM`.
- `pageNumber` commence à 0 (convention `viewIndex` d'OFBiz), taille de page par défaut 100.
- Pas encore reproduit : congés (`emplLeaves`, compteur de CP), notes de frais, paiements, authentification.
