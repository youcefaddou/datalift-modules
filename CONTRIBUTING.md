# Contribuer à DataLift

1. Lis [docs/ONBOARDING.md](docs/ONBOARDING.md) puis [docs/CONVENTIONS.md](docs/CONVENTIONS.md).
2. Prends un ticket dans Jira (projet DataLift, clé `DL`), assigne-le toi et passe-le « En cours ».
3. Crée une branche depuis `main` avec la clé du ticket : `feat/DL-123-sujet-court`, `fix/DL-123-...`, `docs/DL-123-...`.
4. Code avec des tests. Lance `make lint` et `make test`.
5. Commite en Conventional Commits avec la clé du ticket : `feat(connector-yooz): read validated invoices (DL-123)`.
6. Ouvre une pull request en remplissant le modèle. Au moins une relecture et une CI verte sont obligatoires.
7. Après fusion : supprime la branche et passe le ticket « Terminé ».

**Rappels :** aucune donnée réelle, aucun secret, ne modifie pas `contracts/` sans décision d'architecture.
