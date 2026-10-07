# Politique des données — DataLift (dépôt modules)

## Règle principale

**Aucune donnée réelle dans ce dépôt ni dans les environnements de l'équipe.**

## Données autorisées

- Données synthétiques générées par `synthetic_data/`.
- Spécifications publiques des API (OpenAPI, JSON, collections Postman) dans `mocks/specs/`, avec leur source et leur date dans un `SOURCE.md`.

## Avant d'ajouter une spécification d'API

- Vérifier qu'elle provient de la documentation publique de l'éditeur ou d'une collection publique.
- Vérifier les conditions d'utilisation de la documentation.
- Ne jamais inclure de jeton, clé ou identifiant présent dans une collection Postman : les remplacer par des variables.

## Données personnelles

- Même synthétiques, les données de type personne (noms, emails, IBAN) sont générées avec des valeurs manifestement fictives.
- Les vraies données personnelles sont interdites, y compris "juste pour tester".

## Secrets

- Dans `.env` uniquement, jamais commité.
- Si un secret a été commité par erreur : le signaler immédiatement au chef de projet, le révoquer, puis nettoyer l'historique.

## Incident

Toute fuite ou suspicion de donnée réelle est signalée immédiatement au chef de projet.
