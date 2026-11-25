# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-11-25
**Phase :** Sprint 0 (14/10 → 25/11/2026). Branche de travail : `develop` (tirée de `main`, fusion vers `main` par PR).

## Où on en est

- ADR adoptées : 005 ontologie (`datalift_id`, `silver_identity_map`), 007 Odoo remplace Notilus, 008 OpenRouter remplace Hugging Face (crédit unique d'environ 10 $). Proposée : 009 VPS CPX12 2 Go (à valider).
- Specs avec `SOURCE.md` : Yooz, Lucca, Teamtailor, Personio (remplace eTemptation), Sage Embedded Accounting, Odoo ; IFS et Progessi reconstituées (sources citées).
- Mocks FastAPI : `mocks/ifs/` (OData, OAuth2, format et erreurs IFS) et `mocks/progessi/` (modèle OFBiz). 23 tests verts.
- `Makefile` + CI GitHub Actions verte (push sur `main` et `develop`, PR). `main` protégée (PR + check `checks` obligatoires), branche par défaut : `develop`.
- `infra/docker-compose.yml` : PostgreSQL, mocks IFS et Progessi, Odoo 19 (`hr_expense` seul), `mem_limit` par service. Testé en local : Odoo environ 110 Mo, chaque mock environ 37 Mo.
- Jira fait foi (le CSV de `jira/` n'est plus tenu). Terminés : DL-18, DL-24, DL-26 à DL-33. En cours : DL-48 (IFS, manque la projection des temps), DL-93 (Progessi, manque les congés).

## Prochaine étape

- DL-23 : installer son environnement et lancer `make setup` (décidé par Youcef pour la prochaine session).
- VPS CPX12 : créer le serveur (clé SSH ed25519), installer Docker, 2 Go de swap, déployer `infra/`.
- Ensuite : mock Yooz (DL-46) depuis `mocks/specs/yooz/`, et le script de données fictives Odoo.

## Points ouverts

- Flux 3 : nom de la projection IFS de saisie des temps par le manager (`TimeCardManagerHandling` ?), via *Debug > Page Info*.
- Faire valider par FORTIL : Odoo à la place de Notilus, Personio à la place d'eTemptation. Flux M2 vers Sage à redéfinir (pas de paie).
- Yooz, Lucca, Teamtailor, Sage : lien officiel, date et CGU à compléter dans les `SOURCE.md`.
- `.env.example` (non modifiable par Claude) : retirer Hugging Face, ajouter `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `OPENROUTER_MODEL`, `POSTGRES_PASSWORD`, `ODOO_DB_PASSWORD`.
- OpenRouter : compte, crédit, clé avec limite de dépense ; vérifier les quotas réels. Jira : retirer la story du Space Hugging Face.
- M2 : ADR à prévoir pour le fine-tuning (OpenRouter ne sert pas nos modèles).
- Décisions en attente : orchestration (DL-70), interface (DL-62).
- `sudo apt install make` sur le poste de Youcef.

## Fichiers touchés récemment

- ADR-006, 008, 009 ; `infra/` (compose, Dockerfile.mocks, odoo.conf, init PostgreSQL) ; `.dockerignore`
- `AGENTS.md`, `ARCHITECTURE.md`, `ONBOARDING.md`, `vulgarisation.md`, `GLOSSARY.md`
- Un seul compose (`infra/docker-compose.yml`), `compose.yaml` supprimé ; `make up`, `make odoo`, `make down`

Tests : `make test` (ou `uv run pytest -q`)
