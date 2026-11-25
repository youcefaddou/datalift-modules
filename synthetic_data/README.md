# synthetic_data

Générateurs de données synthétiques. Chaque défaut injecté est documenté (type, proportion) pour mesurer la détection.

## Jeu v1 (DL-37)

Données propres des 3 flux du M1, au format silver (`contracts/v1`). Le jeu v1 ne contient aucun défaut injecté.

```bash
make synth            # graine 42, sortie dans synthetic_data/output/v1/
make synth SEED=7     # autre graine
```

La sortie n'est pas commitée : avec la même graine, le générateur produit exactement les mêmes fichiers.

### Volumes par défaut

| Fichier | Objet | Source simulée | Volume |
| --- | --- | --- | --- |
| `suppliers.json` | Fournisseurs | IFS | 20 |
| `purchase_orders.json` | Commandes d'achat | IFS | 60 |
| `supplier_invoices.json` | Factures fournisseurs (1 à 3 lignes) | Yooz | 50 |
| `employees.json` | Collaborateurs | Lucca | 40 |
| `projects.json` | Projets (4 projets client avec 1 sous-projet chacun) | Progessi | 8 |
| `time_entries.json` | Saisies de temps (1 par collaborateur et jour ouvré, 4 semaines) | Progessi | 800 |

Les volumes se règlent dans la classe `Volumes` de `generator.py`.

### Règles de génération

- Chaque facture correspond à une seule commande ; 10 commandes ne sont pas facturées. La facture porte le fournisseur de sa commande.
- Montant HT de la facture = somme des lignes, TVA à 20 %, montant TTC = HT + TVA.
- Les commandes sont passées entre le 01/08 et le 30/09/2026. Une facture est émise 5 à 30 jours après sa commande, avec une échéance à 30 jours.
- Les temps sont saisis du 05/10 au 30/10/2026, sur les jours ouvrés, entre 7 h et 8 h par jour. Ils portent sur 1 ou 2 sous-projets par collaborateur.
- Date d'extraction fixe (`extracted_at` = 2026-11-02T06:00Z). Aucune date du jeu n'est postérieure à l'extraction.
- `datalift_id` est un UUID v5 calculé à partir du type d'objet, de `source_system` et de `source_id`. Il est donc stable d'une exécution à l'autre.
- Les noms sont manifestement fictifs (« Fictif », « Exemple »…) et les emails utilisent le domaine réservé `exemple.invalid`.

Tests : `uv run pytest -q tests/unit/synthetic_data`

## Défauts injectés (DL-38)

Le même jeu v1, avec des défauts connus et leur vérité terrain (`ground_truth.json`) :

```bash
make synth-defects            # graine 42, sortie dans synthetic_data/output/v1_defects/
```

Catalogue des défauts, champs visés et format de la vérité terrain : [DEFECTS.md](DEFECTS.md).
