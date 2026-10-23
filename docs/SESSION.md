# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-23
**Phase :** Sprint 0 (14/10 → 25/11/2026). Branche de travail : `develop` (tirée de `main`, fusion vers `main` par PR).

## Où on en est

- ADR adoptées : 005 ontologie (`datalift_id`, `silver_identity_map`), 006 modèle IA (Qwen sur Hugging Face, 0 €), 007 Odoo remplace Notilus.
- Specs avec `SOURCE.md` : Yooz, Lucca, Teamtailor, Personio (remplace eTemptation), Sage Embedded Accounting, Odoo ; IFS et Progessi reconstituées (sources citées).
- Mocks FastAPI : `mocks/ifs/` (OData, OAuth2, format et erreurs IFS) et `mocks/progessi/` (modèle OFBiz). 23 tests verts.
- `Makefile` + CI GitHub Actions verte (push sur `main` et `develop`, PR). `main` protégée (PR + check `checks` obligatoires), branche par défaut : `develop`.
- Jira fait foi (le CSV de `jira/` n'est plus tenu). Terminés : DL-18, DL-24, DL-26 à DL-33. En cours : DL-48 (IFS, manque la projection des temps), DL-93 (Progessi, manque les congés).

## Prochaine étape

- DL-23 : installer son environnement et lancer `make setup` (décidé par Youcef pour la prochaine session).
- Ensuite : mock Yooz (DL-46) depuis `mocks/specs/yooz/`, puis Odoo Community dans un `docker compose` des mocks.

## Points ouverts

- Flux 3 : nom de la projection IFS de saisie des temps par le manager (`TimeCardManagerHandling` ?), via *Debug > Page Info*.
- Faire valider par FORTIL : Odoo à la place de Notilus, Personio à la place d'eTemptation. Flux M2 vers Sage à redéfinir (pas de paie).
- Yooz, Lucca, Teamtailor, Sage : lien officiel, date et CGU à compléter dans les `SOURCE.md`.
- `.env.example` : variables de l'ADR-006 (jeton Hugging Face, Space, serveur local).
- Décisions en attente : orchestration (DL-70), interface (DL-62), offre du VPS Hetzner.
- `sudo apt install make` sur le poste de Youcef.

## Fichiers touchés récemment

- `docs/SESSION.md` (cette session : clôture de DL-24 dans Jira, sans changement de code)
- `compose.yaml` et `infra/README.md` : PostgreSQL local démarré en une commande depuis `.env`
Tests : `make test` (ou `uv run pytest -q`)


