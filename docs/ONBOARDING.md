# Arrivée sur DataLift

## Jour 1

1. Obtenir l'accès au dépôt GitHub et au projet Jira DataLift (clé `DL`).
2. Lire dans l'ordre : `README.md`, `docs/CONTEXT.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/DATA_POLICY.md`.
3. Installer : Git, Python 3.12, Docker Desktop, VS Code.
4. Extensions VS Code conseillées : Python, Ruff, Docker, Claude Code ou Gemini Code Assist.
5. Récupérer auprès du chef de projet la clé OpenRouter de l'équipe, à mettre dans son `.env` uniquement (ADR-008).
6. Cloner le dépôt, copier `.env.example` en `.env`, lancer `make setup` puis `make test`.
7. Prendre un premier ticket Jira avec le libellé `good-first-issue`.

## Travailler avec un assistant IA

| Outil                             | Fichier lu automatiquement                                      |
| --------------------------------- | --------------------------------------------------------------- |
| Claude Code (VS Code ou terminal) | `CLAUDE.md`, qui importe `AGENTS.md` et `docs/SESSION.md` |
| Gemini Code Assist / Gemini CLI   | `GEMINI.md`, qui importe les mêmes fichiers                  |
| Autre outil ou chat web           | Donner `AGENTS.md` en début de conversation                  |

Bonnes pratiques :

- Demande un plan avant le code.
- Relis tout ce que l'IA produit : tu restes responsable du code.
- Ne colle jamais de secret ni de donnée réelle dans un assistant IA.

## Rituels Ydays

- Début de journée : point de 15 minutes (objectif du jour, blocages).
- Fin de journée : démo de ce qui fonctionne, mise à jour des tickets Jira.

## Contact

Chef de projet : Youcef Addou — youcef.addou@ynov.com
