# État de la session — DataLift modules

> Fichier court (40 lignes max), réécrit à chaque `/handoff`. Ne pas y mettre d'historique.

**Mis à jour :** 2026-10-14
**Phase :** Sprint 0 (14/10 → 25/11/2026), Ydays 1 passé. Prochaine échéance : Ydays 2 le 25/11.

## Où on en est
- Kit de démarrage en place (AGENTS.md, docs, squelette des dossiers). Aucun code applicatif.
- Jira projet DataLift (clé `DL`) créé, branché en MCP sur le PC portable (pas sur le PC de bureau).
- Backlog importé : 13 épopées, 67 stories, 27 tâches, réparties en DL Sprint 0 à 7 (19 hors sprint). Source : `jira/backlog_DL.csv`, généré par `jira/gen_backlog.py`.
- `docs/ROADMAP.md` aligné sur les sprints (1 sprint = période jusqu'à une journée Ydays, story ≤ 5 points).
- Gantt M1 : `docs/assets/gantt_datalift_m1.png` (`jira/gen_gantt.py`).
- Oral de validation Ydays 3 (16/12) préparé : `docs/oral/DataLift_oral_validation_16-12-2026.pptx`, régénérable via `uv run --with python-pptx python docs/oral/build_oral_ydays3.py`.

## Prochaine étape
- Sprint 0 : squelette Python + Makefile (`make setup/test/lint`), puis récupérer les specs des 8 plateformes dans `mocks/specs/` et remplir les `SOURCE.md`.

## Points ouverts
- Décisions en attente : orchestration, technologie de l'interface, modèle IA.
- Flux M1 validés : Yooz, Lucca, Progessi vers IFS (voir docs/CONTEXT.md).
- Collection Postman Yooz rangée dans `docs/assets/` : à déplacer vers `mocks/specs/yooz/`.
- Fichier verrou LibreOffice commité par erreur (`docs/oral/.~lock.*#`) : à supprimer et ignorer.
- MCP Jira à reconfigurer sur le PC de bureau si besoin.

## Fichiers touchés récemment
- `docs/ROADMAP.md`, `jira/*`, `docs/oral/*`, `docs/assets/*`
