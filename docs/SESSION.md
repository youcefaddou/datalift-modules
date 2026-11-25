# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-11-25 (fin de séance)
**Phase :** Sprint 1 (fin le 15/12). Branche de travail : `develop` (fusion vers `main` par PR). Commanditaire : FORTIL Infogérance.

## Où on en est

- Sprint 1 terminé côté code : contrats v1 (DL-34), lignage (DL-35), interface connecteur (DL-36), données synthétiques v1 (DL-37, `make synth`), défauts avec vérité terrain (DL-38), ontologie : liens, actions, `silver_identity_map`, `FlowDefinition` (DL-113). 106 tests verts, CI verte.
- ADR adoptées : 005, 007, 008 (OpenRouter), 010 (PostgreSQL seul), 011 (extraits anonymisés FORTIL). Proposée : 009 (VPS CPX12 2 Go).
- Mocks : IFS (sans saisie des temps) et Progessi (congés `emplLeaves`, `sickLeaves`).
- VPS Hetzner (2.29.165.60) : comptes `youcef` et `yasser` par clé, root interdit en SSH, Docker, 2 Go de swap, `ssh.socket` actif, deploy key GitHub en lecture seule (compte `yasser`). Stack pas encore déployée.
- Oral : `docs/oral/DataLift_oral_validation_16-12-2026.pptx` fait foi (modifié à la main) ; ne plus lancer `build_oral_ydays3.py`. Notes de présentateur réécrites.
- Historique Git nettoyé (aucune attribution IA) ; règle dans `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`.

## Prochaine étape

- Yasser : cloner le dépôt sur le VPS (dossier de déploiement), créer le `.env`, lancer `make up`, mesurer avec `docker stats`.
- Sprint 2 : DL-46 (mock Yooz, Yannis), DL-47 (mock Lucca, Aida), DL-51 (connecteur Lucca, Aida), connecteurs au-dessus de `contracts/connector.py`.
- DL-48 : saisie des temps IFS (`TimeCardManagerHandling` via *Debug > Page Info*, quand Youcef aura accès à IFS).

## Points ouverts

- Jira : passer DL-37 à « Terminé » ; fermer DL-114 (Space Hugging Face) ; assigner les tickets selon l'oral.
- Slide 9 de l'oral : la stack affiche encore « Microsoft Fabric (repli DuckDB) » (contredit l'ADR-010).
- `.env.example` (non modifiable par Claude) : variables OpenRouter, `POSTGRES_PASSWORD`, `ODOO_DB_PASSWORD` ; retirer Hugging Face.
- Équipe : chacun resynchronise `develop` et `main` après la réécriture de l'historique ; Yannis configure `git config user.name/email` (commit signé « Ubuntu »).
- Branches distantes `feat/DL-34`, `feat/dl-34`, `feat/DL-48-mocks-ifs-progessi` : à supprimer si plus utilisées.
- `contracts/v1/schema.json` à régénérer (Pydantic 2.14).
- OpenRouter : compte, crédit, clé avec limite. FORTIL : valider Odoo et Personio.
- Décisions en attente : orchestration (DL-70), interface (DL-62), fine-tuning (M2).
- Poste WSL de Yannis : voir son message pour `uv sync` derrière le proxy (dépôt sous `/mnt/c`).

## Fichiers touchés récemment

- `contracts/connector.py`, `contracts/connector_contract.py`, `contracts/v1/ontology.py`, tests `tests/contract/`
- `mocks/progessi/` (congés), ADR-008 à 011, `infra/`, `docs/oral/` (deck, notes), `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`

Tests : `make test` (ou `uv run pytest -q`)
