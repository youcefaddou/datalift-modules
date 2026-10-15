# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-15
**Phase :** Sprint 0 (14/10 → 25/11/2026). Branche de travail : `develop` (tirée de `main`, fusion vers `main` par PR).

## Où on en est

- ADR adoptées : 005 ontologie (`datalift_id`, `silver_identity_map`), 006 modèle IA (Qwen sur Hugging Face, 0 €), 007 Odoo remplace Notilus.
- Specs avec `SOURCE.md` : Yooz, Lucca, Teamtailor, Personio (remplace eTemptation), Sage Embedded Accounting, Odoo ; IFS et Progessi reconstituées (sources citées).
- Mocks FastAPI : `mocks/ifs/` (OData, OAuth2, format et erreurs IFS) et `mocks/progessi/` (modèle OFBiz). 23 tests verts.
- `Makefile` + CI GitHub Actions (push sur `main` et `develop`, PR).
- Jira fait foi (le CSV de `jira/` n'est plus tenu). DL-26 à DL-33 terminés ; DL-18, DL-24, DL-48, DL-93 en cours.

## Prochaine étape

- Vérifier la CI verte sur `develop`, puis protéger `main` (check `checks` obligatoire) et clore DL-18 / DL-24.
- Mock Yooz (DL-46), puis Odoo Community dans un `docker compose` des mocks.

## Points ouverts

- Flux 3 : nom de la projection IFS de saisie des temps par le manager (`TimeCardManagerHandling` ?), via *Debug > Page Info*.
- Faire valider par FORTIL : Odoo à la place de Notilus, Personio à la place d'eTemptation. Flux M2 vers Sage à redéfinir (pas de paie).
- Yooz, Lucca, Teamtailor, Sage : lien officiel, date et CGU à compléter dans les `SOURCE.md`.
- `.env.example` : variables de l'ADR-006 (jeton Hugging Face, Space, serveur local).
- Décisions en attente : orchestration (DL-70), interface (DL-62), offre du VPS Hetzner.
- `sudo apt install make` sur le poste de Youcef.

## Fichiers touchés récemment

- `Makefile`, `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, `.gitignore`, `README.md`
- `mocks/ifs/`, `mocks/progessi/`, `tests/unit/mocks/`
- `mocks/specs/*/SOURCE.md` et specs ; `etemptation/` → `personio/`, `notilus/` → `odoo/`
- `docs/decisions/ADR-007-odoo-remplace-notilus.md`, `CONTEXT.md`, `ROADMAP.md`, `GLOSSARY.md`, `CONVENTIONS.md`, `CONTRIBUTING.md`, `AGENTS.md`

Tests : `make test` (ou `uv run pytest -q`)
