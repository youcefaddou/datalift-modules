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
| gold | Vues métier, indicateurs, réconciliation | Recalculables depuis silver |

## Plan de contrôle

| Composant | Rôle | Où |
| --- | --- | --- |
| Catalogue | Schémas des API et du modèle commun | modules (lecture des specs) |
| Agent IA | Demande en langage naturel, flux et correspondances proposés | équipe data, dans ce dépôt (dossier à définir) |
| Validation | Interface humaine | `ui/` |
| Orchestrateur | Exécution des flux validés, dans l'ordre des dépendances (collaborateurs avant temps) | `pipelines/` (outil à valider) |
| Supervision | Journaux, métriques, alertes | équipe data, dans `pipelines/` |

## Contrats (`contracts/`)

- **Modèle commun** : Supplier, PurchaseOrder, SupplierInvoice, InvoiceLine, Employee, Project, TimeEntry (puis Candidate, ExpenseReport...). Chaque objet porte son origine : `source_system`, `source_id`, `extracted_at`.
- **Interface connecteur** : `read`, `write`, `describe_schema`, `health_check`.
- **Définition de flux** : source, cible, objet, filtre, correspondances, planning, statut de validation.

## Déploiement

- Local : Docker Compose sur chaque poste (VS Code, Docker Desktop).
- Environnement d'équipe : VPS Hetzner avec Docker Compose. Offre et configuration à choisir (ADR à rédiger).
- CI : GitHub Actions. Infrastructure décrite avec Terraform.

## Décisions

Voir `docs/decisions/`. Décisions en attente : orchestration, interface, modèle IA, offre du VPS.
