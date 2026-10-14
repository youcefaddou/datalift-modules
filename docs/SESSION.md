# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-14
**Phase :** Sprint 0 (14/10 → 25/11/2026), Ydays 1 passé. Prochaine échéance : Ydays 2 le 25/11.

## Où on en est

- Docs optimisées (VS Code, Docker, Jira), vue d'ensemble dans `docs/vulgarisation.md`. Aucun code applicatif.
- ADR-005 adoptée : ontologie (objets, liens, actions, `datalift_id` + `silver_identity_map`) en M1, avant les connecteurs.
- ADR-006 adoptée : IA à 0 €, Qwen open source sur un Space Hugging Face de l'organisation Ynov (Qwen3.6-35B-A3B par défaut, Qwen3.8-27B à comparer), Qwen3.5-9B en local, entraînement sur les GPU Ynov, veille modèles à chaque sprint.
- Jira à jour. Jira fait foi : le CSV de `jira/` n'est plus tenu à jour.
  - Clôturés : DL-21, DL-45, DL-112 (ADR-005).
  - Créés : DL-113 liens/actions/identités (Sprint 1), DL-114 Space Hugging Face (Sprint 3), DL-115 vues gold et DL-116 question transverse (Sprint 6), DL-117 à DL-123 veille modèles (Sprints 1 à 7).
  - Mis à jour : DL-34, DL-54, DL-61, DL-91.
- Oral Ydays 3 prêt : `docs/oral/` (pptx + script de génération). Spec Yooz en place.

## Prochaine étape

- Sprint 0 : DL-18 (squelette Python + Makefile), puis specs des 7 autres plateformes, nécessaires aux champs de jointure de l'ontologie.

## Points ouverts

- Décisions en attente : orchestration (DL-70), interface (DL-62), offre du VPS Hetzner.
- Yooz : compléter lien officiel, date et CGU dans `mocks/specs/yooz/SOURCE.md`.
- `.env.example` : ajouter les variables de l'ADR-006 (jeton Hugging Face, Space, serveur local). La règle `Read(./.env.*)` de `.claude/settings.json` bloque aussi ce fichier pour l'IA : à ajuster si besoin.
- Support de l'oral du 16/12 : ajouter l'ontologie et les questions transverses ? (à décider)
- Flux M1 validés : Yooz, Lucca, Progessi vers IFS (voir `docs/CONTEXT.md`).

## Fichiers touchés récemment

- `docs/decisions/ADR-005-ontologie-liens-actions.md`, `docs/decisions/ADR-006-modele-ia.md` (nouveaux)
- `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/CONTEXT.md`, `docs/GLOSSARY.md`, `docs/ONBOARDING.md`, `docs/ROADMAP.md`, `docs/vulgarisation.md`
