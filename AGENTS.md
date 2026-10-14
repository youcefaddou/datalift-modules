# AGENTS.md — DataLift (dépôt modules)

Contexte de référence pour tout assistant IA. Court par design : les détails sont dans `docs/`, à lire seulement quand la tâche le demande.

## Projet

DataLift : plateforme d'intégration de données assistée par IA, inspirée de Palantir Foundry. Elle connecte des logiciels métier via leurs API et réunit leurs données dans un modèle commun. L'utilisateur décrit le flux en langage naturel, l'IA propose le flux et les correspondances de champs, un humain valide, DataLift exécute, contrôle et supervise.

Projet étudiant Ydays (Ynov), M1 puis M2. Chef de projet et architecte : Youcef Addou. Vue d'ensemble : `docs/vulgarisation.md`. Flux du M1 et catalogue des plateformes : `docs/CONTEXT.md`.

## Ce dépôt

| Dossier | Contenu |
| --- | --- |
| `contracts/` | Modèle commun + interface connecteur. **Lecture seule sauf ADR.** |
| `mocks/specs/` | Specs officielles des API, avec un `SOURCE.md` par logiciel (lourdes : voir règles de contexte) |
| `mocks/` | API simulées générées depuis les specs |
| `synthetic_data/` | Données synthétiques, défauts injectés documentés |
| `connectors/<logiciel>/` | Un connecteur par logiciel, implémente `contracts/` |
| `pipelines/` | Bronze (brut), silver (modèle commun), gold (vues, réconciliation) |
| `ui/` | Interface de validation |
| `tests/` | unit, contract, e2e |
| `infra/` | Docker, Terraform, CI |
| `jira/` | Import initial du backlog (CSV) et scripts. Après l'import, Jira fait foi |

## Stack et outils

- Python 3.12, Pydantic v2, httpx, FastAPI, pytest, ruff.
- PostgreSQL, Microsoft Fabric (repli DuckDB).
- IA : modèles open source (Qwen) sur un Space Hugging Face de l'organisation Ynov, en local pour le développement, budget 0 € (ADR-006).
- Docker, Terraform, GitHub Actions. Hébergement : VPS Hetzner (offre à choisir).
- Poste de travail : VS Code, Docker Desktop. Suivi : Jira, projet DataLift (clé `DL`). Code : GitHub.

Choix encore ouverts : voir `docs/decisions/`. Ne tranche pas seul un choix ouvert : propose 2 options.

## Règles non négociables

1. Aucune donnée réelle : synthétiques et API simulées uniquement.
2. Aucun secret dans le code ni dans la conversation.
3. `contracts/` fait foi.
4. L'IA propose, l'humain valide : aucun flux exécutable sans validation enregistrée.
5. Idempotence : rejouer un flux ne crée jamais de doublon.
6. Lignage : `source_system`, `source_id`, `extracted_at` sur chaque donnée silver.
7. Pas de code sans test.
8. Une tâche = un ticket Jira = une branche = une PR.

## Conventions (résumé)

Code et commits en anglais (Conventional Commits), documentation en français, rédigée simplement et sans métaphore. Tables `bronze_`, `silver_`, `gold_`. Détails : `docs/CONVENTIONS.md`.

## Règles de contexte (économie de tokens)

- Ne lis un fichier de `docs/` que si la tâche le demande (table ci-dessous).
- Ne charge jamais une spec d'API entière : cherche la section utile (grep) ou délègue à un sous-agent qui renvoie un résumé.
- Réponses courtes : plan en quelques lignes, puis code, puis comment tester.
- Ne réécris pas un fichier entier pour une petite modification.

| Fichier | Quand le lire |
| --- | --- |
| `docs/SESSION.md` | Toujours (état courant, très court) |
| `docs/vulgarisation.md` | Expliquer le projet simplement |
| `docs/CONTEXT.md` | Produit, flux, catalogue des plateformes |
| `docs/ARCHITECTURE.md` | Tâche technique structurante |
| `docs/CONVENTIONS.md` | Écriture de code, Git |
| `docs/DATA_POLICY.md` | Manipulation de données ou de specs |
| `docs/ROADMAP.md` | Planification d'un sprint ou d'une journée Ydays |
| `docs/GLOSSARY.md` | Terme métier inconnu |
| `docs/ONBOARDING.md` | Arrivée d'un membre, installation du poste |
| `docs/decisions/` | Avant de remettre en cause un choix |

## Façon de travailler

1. Reformule la tâche, propose un plan court.
2. Pose une question si c'est ambigu, ne suppose pas.
3. Code + tests.
4. Indique les fichiers modifiés et comment tester.
5. En fin de tâche : mets à jour `docs/SESSION.md` (état, prochaine étape), dans le même commit que le travail.
