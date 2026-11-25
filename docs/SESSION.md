# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-11-25
**Phase :** Sprint 1. Branche de travail : `develop` (fusion vers `main` par PR). Commanditaire : FORTIL Infogérance.

## Où on en est

- ADR adoptées : 005 ontologie, 007 Odoo, 008 OpenRouter, 010 PostgreSQL seul (sans Fabric ni DuckDB). Proposées, à valider : 009 VPS CPX12 2 Go, 011 extraits anonymisés FORTIL (DL-40).
- Contrats v1 dans `contracts/` (DL-34, Ilyes) : lignage et `datalift_id` sur chaque objet. `schema.json` légèrement décalé de Pydantic 2.14 (à régénérer).
- Mocks : IFS (sans la saisie des temps) et Progessi (avec `emplLeaves` et `sickLeaves`, DL-93 fait). 38 tests verts, CI verte.
- VPS Hetzner CPX12 créé, accès SSH de Youcef et de Yasser ; Yasser installe le serveur.
- `infra/docker-compose.yml` seul compose : `make up`, `make odoo`, `make down`.
- Oral : 16 slides, 9 min 50, avec équipe en 2 pôles, partie commanditaire FORTIL, limites, risques hiérarchisés.
- Veille OpenRouter faite (DL-117) : aucun Qwen gratuit ; `google/gemma-4-31b-it:free` par défaut, `qwen/qwen3.7-flash` en secours.

## Prochaine étape

- DL-36 : interface connecteur (`read`, `write`, `describe_schema`, `health_check`) au-dessus des contrats d'Ilyes.
- DL-48 : saisie des temps IFS (entity set et champs de `TimeCardManagerHandling` via *Debug > Page Info*, quand Youcef aura accès à IFS).
- Valider ADR-009 et ADR-011, puis compléter `DATA_POLICY.md` et la règle 1 d'`AGENTS.md`.

## Points ouverts

- `.env.example` (non modifiable par Claude) : `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `OPENROUTER_MODEL`, `POSTGRES_PASSWORD`, `ODOO_DB_PASSWORD` ; retirer Hugging Face.
- OpenRouter : compte, crédit, clé avec limite de dépense. Jira : fermer DL-114 (Space Hugging Face).
- Jira : assigner les tickets selon la répartition de l'oral (data 18-19 chacun, infra 14, pilotage 18).
- FORTIL : valider Odoo et Personio ; flux M2 vers Sage à redéfinir.
- Yooz, Lucca, Teamtailor, Sage : lien officiel, date et CGU dans les `SOURCE.md`.
- M2 : ADR pour le fine-tuning. Décisions en attente : orchestration (DL-70), interface (DL-62).

## Fichiers touchés récemment

- ADR-010, ADR-011 ; `AGENTS.md` ; `docs/oral/` (deck et script)
- `mocks/progessi/` (congés), `tests/unit/mocks/test_progessi_mock.py`
- `contracts/v1/*.py` (lint), suppression des doublons `unit/` et `contracts/contracts/`

Tests : `make test` (ou `uv run pytest -q`)
