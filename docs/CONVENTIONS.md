# Conventions — DataLift

## Langues

- Code, identifiants, commits, noms de branches : anglais.
- Documentation, tickets, pull requests : français.

## Python

- Python 3.12, typage obligatoire sur les fonctions publiques.
- Modèles de données avec Pydantic v2.
- Appels HTTP avec httpx, timeouts explicites, nouvelles tentatives sur erreurs temporaires.
- Lint et format : `ruff check` et `ruff format`.
- Pas de `print` : utiliser le module `logging` (format structuré).
- Pas de secret en dur : lire la configuration depuis l'environnement.

## Tests

- pytest. Arborescence : `tests/unit/`, `tests/contract/`, `tests/e2e/`.
- Chaque connecteur a des tests de contrat contre sa spécification.
- Un bug corrigé = un test qui le reproduit.

## Git

- Branches : `feat/...`, `fix/...`, `docs/...`, `chore/...`, `test/...`.
- Commits : Conventional Commits, par exemple `fix(connector-ifs): handle 429 rate limit`.
- Pull request obligatoire, au moins une relecture, CI verte.

## Données

- Tables : `bronze_<source>_<objet>`, `silver_<objet>`, `gold_<vue>`, en snake_case.
- Colonnes d'origine obligatoires en silver : `source_system`, `source_id`, `extracted_at`.
- Dates en UTC, format ISO 8601. Montants en décimal, jamais en flottant.

## Documentation

- Chaque dossier de module a un README.md.
- Toute décision technique structurante a une ADR dans `docs/decisions/`.
