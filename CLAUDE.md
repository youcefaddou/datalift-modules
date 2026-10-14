# CLAUDE.md — DataLift (dépôt modules)

@AGENTS.md
@docs/SESSION.md

## Démarrage de session

1. Résume `docs/SESSION.md` en 3 lignes : où on en est, prochaine étape, points bloquants.
2. Si aucun objectif n'est donné, demande-le. N'ouvre aucun autre fichier avant.

## Pendant la session

- Tâche sur plus d'un fichier : plan court d'abord (mode plan avec Shift+Tab).
- Specs d'API : `/spec` ou sous-agent `spec-explorer`, jamais de lecture intégrale.
- Fichiers de `docs/` : à la demande, selon la table de AGENTS.md.
- Tests ciblés plutôt que toute la suite.
- Commit et push uniquement sur demande.

## Fin de tâche

1. `/handoff` : met à jour `docs/SESSION.md` et propose un message de commit.
2. `SESSION.md` part dans le même commit que le travail : c'est lui qui transmet l'état d'un poste à l'autre.
3. Ensuite `/clear`. `/compact` seulement pour continuer la même tâche avec un contexte chargé.

## Compaction

Conserver : objectif de la session, fichiers modifiés, décisions prises, commandes de test, problèmes non résolus.

## Commandes

- Projet (à confirmer à Ydays 2) : `make setup`, `make test`, `make lint`, `make mocks`.
- `/handoff` : passation avant `/clear`.
- `/adr <sujet>` : rédige une décision d'architecture.
- `/spec <logiciel> <question>` : interroge une spec d'API via le sous-agent.
