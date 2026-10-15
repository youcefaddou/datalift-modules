# Source de la spécification

- Éditeur : Cegid (Cegid Notilus, notes de frais et déplacements)
- Format : **reconstitué**. Cegid confirme l'existence d'API, mais leur documentation est réservée aux clients ; aucun dépôt public ni spec trouvés (recherche du 2026-10-15).
- Lien vers la documentation officielle : aucune doc d'API publique ; modèle open source de référence : [Odoo `hr_expense`](https://github.com/odoo/odoo/tree/master/addons/hr_expense) (licence LGPL-3)
- Date de récupération : 2026-10-15
- Conditions d'utilisation vérifiées : oui pour Odoo (LGPL-3) ; guides utilisateurs Notilus publics, seul le vocabulaire est repris
- Jetons et identifiants retirés de la collection : sans objet

## Bases de la reconstitution

| Concept Notilus (guides utilisateurs) | Modèle Odoo `hr.expense` | Champs retenus |
|---|---|---|
| Note de frais : `N° de pièce`, `Type de Note`, `Mt Note`, `Mt à payer`, `Solde` | regroupement des dépenses d'un employé | numéro, type, employé, montant total, montant à payer, solde, statut |
| Frais : date, nature, devise, `Montant Réel` (TTC), `N°Justificatif`, remarque | `date`, `product_id` (catégorie), `quantity`, `price_unit`, `total_amount`, `tax_amount`, `untaxed_amount`, `currency_id`, `attachment_ids`, `description` | date, nature, quantité, TTC, HT, TVA, devise, justificatif, remarque |
| Frais kilométriques (sans justificatif) + véhicule (immatriculation, carburant) | `quantity` × barème | kilomètres, véhicule |
| Avance ponctuelle imputée à la remise | `payment_mode` (`own_account` / `company_account`) | avance imputée |
| Circuit : remise au contrôle (irréversible), validation multi-niveaux, refus d'un frais ou de la note avec motif, puis compta et paiement | `state` : `draft` → `submitted` → `approved` → `posted` → `paid`, ou `refused` | statut, niveau de validation, valideur, motif de refus |

Sources fonctionnelles : [guide CFDT Services, gestion des notes de frais](https://docs.cfdt-services.fr/docs/docs/Notilus%20-%20Gestion%20des%20notes%20de%20frais.html), [Cegid Notilus](https://www.cegid.com/fr/produits/cegid-notilus/logiciel-notes-de-frais/).

## Ce qui est reconstitué

Tout le format technique de l'API : URL, noms de champs, codes de statut, pagination, authentification. Le mock suivra le vocabulaire Notilus ci-dessus. Les ordres de mission ne sont pas couverts (absents du guide utilisé).

`cegid_notilus_openapi.json` n'est **pas** l'API Notilus : c'est le service d'archivage électronique Cegid (archives, smartfolders, conteneurs). Il est à supprimer.
