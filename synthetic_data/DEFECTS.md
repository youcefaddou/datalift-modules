# Défauts injectés (v1)

Les données synthétiques contiennent des défauts volontaires. Ils servent à mesurer ce que DataLift détecte : chaque défaut injecté est enregistré dans un fichier de vérité terrain, que les tests comparent aux anomalies trouvées par le pipeline.

Code : `synthetic_data/defects.py`. Tests : `tests/unit/synthetic_data/test_defects.py`.

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

## Branchement avec le générateur

À faire quand le générateur existe : un point d'entrée appelle le générateur puis l'injecteur, avec la même graine.

```python
from synthetic_data.defects import DefectInjector

injector = DefectInjector(seed=42)
invoices = injector.duplicates(invoices, flow=1, obj="invoice", id_field="id")
invoices = injector.invoices_without_po(invoices, obj="invoice", id_field="id", po_field="po")
injector.write_ground_truth(output_dir / "ground_truth.json")
```

Les noms d'objets et de champs sont à aligner avec le générateur des données synthétiques v1.
