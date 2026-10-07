# Bienvenue sur DataLift

## Jour 1

1. Signer l'accord de contribution.
2. Obtenir l'accès au dépôt GitHub et au tableau de suivi.
3. Lire dans l'ordre : `README.md`, `docs/CONTEXT.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/DATA_POLICY.md`.
4. Installer : Git, Python 3.12, Docker, VS Code ou Cursor.
5. Cloner le dépôt, copier `.env.example` en `.env`, lancer `make setup` puis `make test`.
6. Prendre un premier ticket marqué "good first issue".

## Travailler avec un assistant IA

Le dépôt est prêt pour les assistants IA :

| Outil | Fichier lu automatiquement |
|---|---|
| Claude Code (terminal, VS Code, JetBrains) | `CLAUDE.md` (qui importe `AGENTS.md`) |
| Cursor | `.cursor/rules/datalift.mdc` et `AGENTS.md` |
| Gemini CLI / Gemini Code Assist | `GEMINI.md` (qui importe `AGENTS.md`) |
| Autre outil ou chat web | Donner `AGENTS.md` en début de conversation |

Bonnes pratiques :
- Demande toujours un plan avant le code.
- Relis tout ce que l'IA produit : tu restes responsable du code.
- Ne colle jamais de secret ni de donnée réelle dans un assistant IA.

## Rituels Ydays

- Début de journée : point de 15 minutes (objectif du jour, blocages).
- Fin de journée : démo de ce qui fonctionne, mise à jour du tableau.

## Contacts

Chef de projet : Youcef Addou — youcef.addou@ynov.com
