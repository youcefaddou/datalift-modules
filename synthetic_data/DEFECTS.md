# Défauts injectés (v1)

Les données synthétiques contiennent des défauts volontaires. Ils servent à mesurer ce que DataLift détecte : chaque défaut injecté est enregistré dans un fichier de vérité terrain, que les tests comparent aux anomalies trouvées par le pipeline.

Code : `synthetic_data/defects.py` (injecteur) et `synthetic_data/build_defects.py` (jeu v1 avec défauts). Tests : `tests/unit/synthetic_data/test_defects.py` et `test_build_defects.py`.

## Catalogue

| Code | Flux | Objet visé | Défaut injecté | Détection attendue |
| --- | --- | --- | --- | --- |
| `DUPLICATE` | 1, 2, 3 | tout objet | Copie d'un enregistrement, même contenu, identifiant technique suffixé `-DUP` | Doublon détecté |
| `AMOUNT_MISMATCH` | 1 | facture | Un montant (par exemple le TTC) décalé de ± 10,00 : il ne correspond plus aux autres montants ni à la commande | Incohérence de montant, facture mise de côté |
| `INVOICE_WITHOUT_PO` | 1 | facture | Référence de commande d'achat vidée (`None`) | Facture mise de côté |
| `UNKNOWN_SUPPLIER` | 1 | facture | Fournisseur remplacé par `UNKNOWN-SUPPLIER-nnnn`, absent de la liste des fournisseurs | Référence orpheline |
| `UNKNOWN_EMPLOYEE` | 3 | temps | Collaborateur remplacé par `UNKNOWN-EMPLOYEE-nnnn`, absent de la liste des collaborateurs | Temps mis de côté |
| `HOURS_OUT_OF_RANGE` | 3 | temps | Heures fixées à -1,5 ou 25,5 (hors de 0 à 24) | Incohérence d'heures |
| `MISSING_FIELD` | 1, 2, 3 | tout objet | Champ obligatoire vidé (`None`) | Champ manquant |

## Règles d'injection

- **Reproductible** : une même graine (`DefectInjector(seed)`) donne les mêmes données et la même vérité terrain.
- **Proportion** : 5 % des enregistrements par défaut et par appel (`DEFAULT_RATE`), au moins 1 enregistrement si la proportion est positive. Chaque appel accepte un `rate` différent.
- **Un défaut par enregistrement** : un enregistrement déjà modifié n'est plus choisi, pour que la vérité terrain reste sans ambiguïté.
- **Indépendant du format** : les enregistrements sont des dictionnaires et les noms de champs sont passés en paramètre.
- Les données d'entrée ne sont jamais modifiées : chaque méthode renvoie une nouvelle liste.

## Vérité terrain

`DefectInjector.write_ground_truth(path)` écrit un fichier JSON :

```json
{
  "seed": 42,
  "defects": [
    {
      "defect_id": "DEF-0001",
      "defect_type": "DUPLICATE",
      "flow": 1,
      "object": "invoice",
      "record_id": "INV-017-DUP",
      "field": "id",
      "original_value": "INV-017",
      "injected_value": "INV-017-DUP"
    }
  ]
}
```

| Champ | Sens |
| --- | --- |
| `defect_id` | Identifiant unique du défaut (`DEF-nnnn`) |
| `defect_type` | Code du catalogue |
| `flow` | Flux concerné (1 : Yooz → IFS, 2 : Lucca → IFS, 3 : Progessi → IFS) |
| `object` | Objet visé (nom choisi par le générateur) |
| `record_id` | Identifiant de l'enregistrement modifié (pour `DUPLICATE` : celui de la copie) |
| `field` | Champ modifié |
| `original_value` | Valeur avant injection (pour `DUPLICATE` : identifiant de l'original) |
| `injected_value` | Valeur après injection |

Les montants et les heures sont écrits sous forme de chaînes (`"130.00"`), pour ne jamais passer par des flottants.

## Jeu v1 avec défauts

`synthetic_data/build_defects.py` branche l'injecteur sur le générateur du jeu v1 : il produit le jeu propre, le convertit en dictionnaires, injecte les défauts avec la même graine, puis écrit les données et la vérité terrain. Le code du générateur n'est pas modifié.

```bash
make synth-defects            # graine 42, sortie dans synthetic_data/output/v1_defects/
make synth-defects SEED=7     # autre graine
```

La sortie contient les 6 fichiers du jeu v1 et `ground_truth.json`. Elle n'est pas commitée : avec la même graine, le script produit exactement les mêmes fichiers.

Les défauts sont injectés dans les données au format silver (`contracts/v1`). L'identifiant de chaque enregistrement est `datalift_id`.

| Fichier | Flux | Défaut | Champ |
| --- | --- | --- | --- |
| `supplier_invoices.json` | 1 | `DUPLICATE` | `datalift_id` (copie suffixée `-DUP`, même `invoice_no`) |
| `supplier_invoices.json` | 1 | `AMOUNT_MISMATCH` | `gross_curr_amount` (le TTC ne vaut plus HT + TVA) |
| `supplier_invoices.json` | 1 | `INVOICE_WITHOUT_PO` | `purchase_order_datalift_id` |
| `supplier_invoices.json` | 1 | `UNKNOWN_SUPPLIER` | `supplier_datalift_id` |
| `supplier_invoices.json` | 1 | `MISSING_FIELD` | `invoice_no` |
| `employees.json` | 2 | `DUPLICATE` | `datalift_id` |
| `employees.json` | 2 | `MISSING_FIELD` | `family_name` |
| `time_entries.json` | 3 | `DUPLICATE` | `datalift_id` |
| `time_entries.json` | 3 | `UNKNOWN_EMPLOYEE` | `employee_datalift_id` |
| `time_entries.json` | 3 | `HOURS_OUT_OF_RANGE` | `hours` |
| `time_entries.json` | 3 | `MISSING_FIELD` | `work_effort_id` |

`suppliers.json`, `purchase_orders.json` et `projects.json` restent identiques au jeu propre.

Avec la graine 42 : 162 défauts (2 de chaque type sur les 50 factures et les 40 collaborateurs, 34 à 40 de chaque type sur les 800 saisies de temps).

Certains défauts rendent un enregistrement invalide au sens des contrats : heures négatives (`hours` doit être positif ou nul) et champs obligatoires vides (`invoice_no`, `work_effort_id`). Le chargement en objets silver les rejette : ce rejet fait partie de la détection attendue.

Tests : `tests/unit/synthetic_data/test_build_defects.py`.
