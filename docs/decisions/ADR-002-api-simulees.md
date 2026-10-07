# ADR-002 — API simulées construites depuis les spécifications officielles

- **Statut :** adoptée
- **Date :** 2026-10-07
- **Auteur :** Youcef Addou

## Contexte

L'équipe n'a pas accès à des environnements réels, et les données réelles sont interdites.

## Décision

Chaque logiciel est simulé à partir de sa documentation officielle (OpenAPI, JSON, collection Postman) stockée dans `mocks/specs/` avec sa source.

## Conséquences

Réalisme suffisant pour la démo. Risque d'écart avec l'API réelle, limité par des tests de contrat.
