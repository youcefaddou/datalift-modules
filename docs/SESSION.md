# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-15
**Phase :** Sprint 0 (14/10 – 25/11/2026), branche `feat/DL-48-mocks-ifs-progessi` (4 commits, pas encore poussée)

## Où on en est
- Specs dans `mocks/specs/` avec `SOURCE.md` : Yooz, Lucca, Teamtailor (collection publique), Personio (remplace eTemptation), Sage Embedded Accounting ; IFS, Progessi et Notilus reconstituées, sources citées.
- Mocks FastAPI : `mocks/ifs/` (OData, OAuth2, format et erreurs IFS, 8 collections) et `mocks/progessi/` (modèle OFBiz : profils, projets, feuilles de temps). 23 tests verts.
- `Makefile` (setup, test, lint, format, mocks) et CI GitHub Actions (`.github/workflows/ci.yml`) commités.
- Jira : DL-26 à DL-33 terminés ; DL-18, DL-24, DL-48, DL-93 en cours.

## Prochaine étape
- Push refusé : le jeton GitHub n'a pas le scope `workflow`. L'ajouter, puis `git push -u origin feat/DL-48-mocks-ifs-progessi`, ouvrir la PR, vérifier la CI verte, protéger `main`.
- `sudo apt install make`.
- Mock Yooz (DL-46) à partir de `mocks/specs/yooz/`.

## Points ouverts
- Flux 3 : nom de la projection IFS de saisie des temps par le manager (`TimeCardManagerHandling` ?), à lire dans *Debug > Page Info*.
- Notilus (DL-32) : pas d'API publique ; spec reconstituée depuis Odoo `hr_expense` (LGPL-3) + guides Notilus (`mocks/specs/notilus/SOURCE.md`). Supprimer `cegid_notilus_openapi.json` (archivage Cegid, hors sujet).
- Flux M2 vers Sage à redéfinir (Embedded Accounting ne couvre pas la paie).
- ADR à rédiger : résolution d'identité entre systèmes (contracts/), JSON anonymisé.
- docker compose des mocks, conditions d'utilisation des specs Lucca / Teamtailor / Sage.
- Décisions en attente : orchestration, techno de l'interface, modèle IA.

## Fichiers touchés récemment
- `Makefile`, `.github/workflows/ci.yml`, `README.md`, `pyproject.toml`, `uv.lock`, `.gitignore` (exclut `mocks/specs/progessi/progessi.json`)
- `mocks/ifs/` (app.py, seed.json, README.md), `mocks/progessi/` (idem)
- `tests/unit/mocks/test_ifs_mock.py`, `test_progessi_mock.py`
- `mocks/specs/{yooz,ifs,progessi,lucca,teamtailor,personio,sage}/` (specs + `SOURCE.md`) ; `etemptation/` renommé en `personio/` ; collection Yooz déplacée depuis `docs/assets/`
- `docs/CONTEXT.md` (catalogue : Personio, Sage)

Tests : `uv run pytest tests/unit/mocks -q`
