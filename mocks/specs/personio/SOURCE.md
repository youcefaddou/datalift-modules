# Source de la spécification

- Éditeur : Personio (remplace eTemptation, dont aucune doc d'API publique n'est disponible)
- Format : OpenAPI 3 (`personio-personnel-data-api-oa3.yaml` « Personnel Data » v1.0, `personio-auth-api.yaml` « Authentication » v1.0)
- Lien vers la documentation officielle : https://github.com/personio/api-docs (commit fb5b7f9f6c56 du 2026-08-21), https://developer.personio.de
- Date de récupération : 2026-10-15
- Conditions d'utilisation vérifiées : dépôt public sans licence, utilisé comme référence pour construire le mock
- Jetons et identifiants retirés de la collection : oui, un JWT d'exemple remplacé par `<example-jwt-removed>`

## Périmètre utile

Temps et absences : `/company/attendances`, `/company/time-offs`, `/company/absence-periods`, `/company/attendances/projects`, et `/company/employees` pour rattacher les collaborateurs.
