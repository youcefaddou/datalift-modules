# CLAUDE.md — DataLift (dépôt modules)

@AGENTS.md
@docs/SESSION.md

## Démarrage de session

`docs/SESSION.md` est chargé ci-dessus. En premier message :
1. Résume en 3 lignes : où on en est, prochaine étape, points bloquants.
2. Si je n'ai pas donné d'objectif, demande-le. N'ouvre aucun autre fichier avant.

## Pendant la session

- Tâche qui touche plus d'un fichier : propose un plan (je peux passer en mode plan avec Shift+Tab).
- Specs d'API : utilise le sous-agent `spec-explorer`, ne lis jamais une spec entière dans la conversation.
- Lis les fichiers de `docs/` à la demande, selon la table de AGENTS.md.
- Lance les tests ciblés plutôt que toute la suite quand c'est possible.

## Fin de tâche ou changement de sujet

1. Je lance `/handoff` : tu mets à jour `docs/SESSION.md` et proposes un message de commit.
2. Je fais le commit, puis `/clear` pour repartir sur une session neuve.
3. `/compact` seulement si on continue la même tâche et que le contexte est chargé.

## Compact Instructions

Lors d'une compaction, conserve toujours : l'objectif de la session, la liste des fichiers modifiés, les décisions prises, les commandes de test, les problèmes non résolus.

## Commandes du projet

À confirmer à l'initialisation (Ydays 2) : `make setup`, `make test`, `make lint`, `make mocks`.

## Commandes personnalisées

- `/handoff` : met à jour SESSION.md avant un /clear.
- `/adr <sujet>` : rédige une décision d'architecture.
- `/spec <logiciel> <question>` : interroge une spec d'API via le sous-agent.
