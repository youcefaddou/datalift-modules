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
|---|---|---|
| bronze | Réponses d'API brutes, horodatées | Jamais modifiées |
| silver | Objets du modèle commun | Validés par les contrats et les contrôles qualité |
| gold | Vues métier, indicateurs, réconciliation | Recalculables depuis silver |

## Plan de contrôle

| Composant | Rôle | Où |
|---|---|---|
| Catalogue | Schémas des API et du modèle commun | modules (lecture des specs) |
| Agent IA | Demande en langage naturel, flux et correspondances proposés | développé à part par le chef de projet |
| Validation | Interface humaine | `ui/` |
| Orchestrateur | Exécution des flux validés, dans l'ordre des dépendances (collaborateurs avant temps) | `pipelines/` (outil à valider) |
| Supervision | Journaux, métriques, alertes | base dans `pipelines/`, avancé à part |

## Contrats (`contracts/`)

- **Modèle commun** : Supplier, PurchaseOrder, SupplierInvoice, InvoiceLine, Employee, Project, TimeEntry (puis Candidate, ExpenseReport...). Chaque objet porte son origine : `source_system`, `source_id`, `extracted_at`.
- **Interface connecteur** : `read`, `write`, `describe_schema`, `health_check`.
- **Définition de flux** : source, cible, objet, filtre, correspondances, planning, statut de validation.

## Décisions

Voir `docs/decisions/`. Les décisions en attente : orchestration, interface, modèle IA.
