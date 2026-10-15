# Contribuer à DataLift

1. Lis [docs/ONBOARDING.md](docs/ONBOARDING.md) puis [docs/CONVENTIONS.md](docs/CONVENTIONS.md).
2. Prends un ticket dans Jira (projet DataLift, clé `DL`), assigne-le toi et passe-le « En cours ».
3. Travaille sur la branche `develop` (`git switch develop && git pull`).
4. Code avec des tests. Lance `make lint` et `make test`.
5. Commite en Conventional Commits avec la clé du ticket : `feat(connector-yooz): read validated invoices (DL-123)`.
6. Pousse sur `develop` et vérifie que la CI est verte. `main` est mis à jour par une PR depuis `develop`.
7. Passe le ticket « Terminé » quand le travail est sur `develop` avec la CI verte.

**Rappels :** aucune donnée réelle, aucun secret, ne modifie pas `contracts/` sans décision d'architecture.
