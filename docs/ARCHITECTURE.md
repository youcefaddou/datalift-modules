# Architecture — DataLift

Version de travail. Le dossier d'architecture complet est tenu par le chef de projet.

## Deux plans

- **Plan de données** : la circulation des données de la source à la cible.
- **Plan de contrôle** : catalogue, agent IA, validation, orchestration, supervision.

## Plan de données

```
[API source] -> connecteur -> bronze (brut) -> silver (modèle commun, contrôlé) -> gold (vues, réconciliation)
                                                      |
                                                      v
                                            connecteur -> [API cible]
```

| Couche | Contenu | Règle |
| --- | --- | --- |
| bronze | Réponses d'API brutes, horodatées | Jamais modifiées |
| silver | Objets du modèle commun | Validés par les contrats et les contrôles qualité |
| gold | Vues métier qui suivent les liens de l'ontologie, indicateurs, réconciliation | Recalculables depuis silver |

## Plan de contrôle

| Composant | Rôle | Où |
| --- | --- | --- |
| Catalogue | Schémas des API et du modèle commun | modules (lecture des specs) |
| Agent IA | Demande en langage naturel, flux et correspondances proposés, questions transverses (SQL en lecture seule sur gold) | équipe data, dans ce dépôt (dossier à définir). Modèle : ADR-008 (OpenRouter) |
| Validation | Interface humaine | `ui/` |
| Orchestrateur | Exécution des flux validés, dans l'ordre des dépendances (collaborateurs avant temps) | `pipelines/` (outil à valider) |
| Supervision | Journaux, métriques, alertes | équipe data, dans `pipelines/` |

## Contrats (`contracts/`)

- **Modèle commun** : Supplier, PurchaseOrder, SupplierInvoice, InvoiceLine, Employee, Project, TimeEntry (puis Candidate, ExpenseReport...). Chaque objet porte son origine (`source_system`, `source_id`, `extracted_at`) et un identifiant DataLift stable (`datalift_id`).
- **Liens** : relations déclarées entre objets (facture → commande → fournisseur, temps → collaborateur → projet). Voir ADR-005.
- **Actions** : écritures vers un logiciel, déclarées sur un objet avec leurs préconditions (règles métier). Voir ADR-005.
- **Interface connecteur** : `read`, `write`, `describe_schema`, `health_check`.
- **Définition de flux** : source, cible, objet, filtre, correspondances, planning, statut de validation.

## Déploiement

- Local : Docker Compose sur chaque poste (VS Code, Docker Desktop).
- Environnement d'équipe : VPS Hetzner CPX12 (2 Go) avec Docker Compose (`infra/docker-compose.yml`), budget mémoire par service : ADR-009.
- CI : GitHub Actions. Infrastructure décrite avec Terraform.

## Décisions

Voir `docs/decisions/`. Décisions en attente : orchestration, interface.
