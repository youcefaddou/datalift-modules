# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-11-25
**Phase :** Sprint 1 (fin le 15/12). Branche de travail : `develop` (fusion vers `main` par PR). Commanditaire : FORTIL Infogérance.

## Où on en est

- ADR adoptées : 005 ontologie, 007 Odoo, 008 OpenRouter, 010 PostgreSQL seul. Proposées, à valider : 009 VPS CPX12 2 Go, 011 extraits anonymisés FORTIL (DL-40).
- Contrats v1 dans `contracts/` (DL-34) ; DL-35 fait (lignage obligatoire testé). `schema.json` à régénérer (Pydantic 2.14).
- Mocks : IFS (sans la saisie des temps) et Progessi (congés inclus).
- DL-37 fait : `make synth` génère le jeu synthétique v1 des 3 flux au format silver (graine 42, sans défaut injecté) dans `synthetic_data/output/v1/` (non commité). Volumes et règles : `synthetic_data/README.md`. 88 tests verts.
- VPS Hetzner CPX12 créé ; Yasser installe le serveur. `infra/docker-compose.yml` : `make up`, `make odoo`, `make down`.
- Veille OpenRouter (DL-117) : `google/gemma-4-31b-it:free` par défaut, `qwen/qwen3.7-flash` en secours.

## Prochaine étape

- DL-36 : interface connecteur (`read`, `write`, `describe_schema`, `health_check`) au-dessus des contrats v1.
- DL-48 : saisie des temps IFS (`TimeCardManagerHandling` via *Debug > Page Info*, quand Youcef aura accès à IFS).
- Sprint 2 : DL-46 (mock Yooz, assigné à Yannis) ; défauts injectés documentés dans le jeu synthétique (ticket à créer).

## Points ouverts

- Poste WSL : dépôt sous `/mnt/c`, l'Explorer VS Code ne se rafraîchit pas seul. `uv sync` derrière le proxy : préfixer `SSL_CERT_FILE=/mnt/c/Users/T0334283/.claude/thales-ca.pem`.
- DL-37 : la définition de terminé demande une PR relue, mais le commit est poussé directement sur `develop` (choix de Yannis).
- `.env.example` (non modifiable par Claude) : variables OpenRouter, Postgres et Odoo ; retirer Hugging Face.
- OpenRouter : compte, crédit, clé avec limite. Jira : fermer DL-114 ; assigner les tickets selon l'oral.
- FORTIL : valider Odoo et Personio ; flux M2 vers Sage à redéfinir.
- Yooz, Lucca, Teamtailor, Sage : lien officiel, date et CGU dans les `SOURCE.md`.
- Décisions en attente : orchestration (DL-70), interface (DL-62), fine-tuning (M2).

## Fichiers touchés récemment

- `synthetic_data/` (`generator.py`, `__init__.py`, `README.md`), `tests/unit/synthetic_data/test_generator.py`
- `Makefile` (cible `synth`), `.gitignore` (`synthetic_data/output/`)

Tests : `make test` (ou `uv run pytest -q`) ; jeu synthétique : `uv run pytest -q tests/unit/synthetic_data`
