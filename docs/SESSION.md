# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-14
**Phase :** Sprint 0 (14/10 → 25/11/2026), Ydays 1 passé. Prochaine échéance : Ydays 2 le 25/11.

## Où on en est
- Docs optimisées (VS Code, Docker, Jira), règles Cursor retirées. Aucun code applicatif.
- Jira projet DataLift (clé `DL`) : 13 épopées, 67 stories, 27 tâches, DL Sprint 0 à 7. Après l'import, Jira fait foi (le CSV de `jira/` n'est plus tenu à jour).
- Décidé : ontologie (objets, liens, actions) en M1 avant les connecteurs, exploitation en M2, questions transverses à la démo de Ydays 9. ROADMAP, ARCHITECTURE, CONTEXT, GLOSSARY à jour.
- ADR-005 adoptée : ontologie (liens, actions, `datalift_id` + `silver_identity_map`).
- Oral Ydays 3 prêt : `docs/oral/` (pptx + script de génération). Spec Yooz en place.

## Prochaine étape
- Rédiger l'ADR modèle IA (API, local ou Hugging Face), puis mettre Jira à jour (liste ci-dessous).
- Sprint 0 : squelette Python + Makefile, puis specs des 7 autres plateformes (nécessaires aux champs de jointure de l'ontologie).

## Jira à mettre à jour
- Découper « Définir le modèle commun v1 dans contracts/ » : objets, puis liens + actions + `datalift_id`.
- « Convertir Yooz et Lucca vers le modèle commun » : ajouter le remplissage de `silver_identity_map`.
- Nouvelle story Sprint 6 : vues gold qui suivent les liens + question transverse en langage naturel.
- Créer et clôturer la tâche ADR-005. Clôturer « Remplacer GitHub Projects par Jira dans la documentation ».

## Points ouverts
- Décisions en attente : orchestration, interface, modèle IA (ticket Sprint 2), offre du VPS Hetzner.
- Hugging Face : licence Academia Hub via l'organisation Ynov (ZeroGPU 40 min/jour, dépôts privés). Avec Colab et Kaggle, à intégrer dans l'ADR modèle IA.
- Flux M1 validés : Yooz, Lucca, Progessi vers IFS (voir docs/CONTEXT.md).
- Yooz : compléter lien officiel, date et CGU dans `mocks/specs/yooz/SOURCE.md`.
- MCP Atlassian à authentifier sur le PC de bureau (`/mcp`).

## Fichiers touchés récemment
- `docs/decisions/ADR-005-ontologie-liens-actions.md` (nouveau)
- `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/CONTEXT.md`, `docs/GLOSSARY.md`, `docs/vulgarisation.md`, `AGENTS.md`
