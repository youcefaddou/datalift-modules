# Contexte produit — DataLift

## Le problème

Une PME de 50 à 200 personnes utilise une dizaine de logiciels métier (factures, ERP, RH, recrutement, temps, frais, comptabilité). Ils échangent mal : ressaisies, exports Excel, scripts fragiles.

## La vision

Plateforme d'intégration de données assistée par IA, inspirée de Palantir :

1. **Connecter** les logiciels via leurs API.
2. **Réunir** les données dans un modèle commun (ontologie : Fournisseur, Facture, Collaborateur, Temps..., indépendamment des logiciels).
3. **Demander** en langage naturel : "envoie les factures validées de Yooz vers IFS".
4. **Valider** : l'IA propose le flux et les correspondances, un humain valide.
5. **Exécuter et superviser** : exécution, contrôles, réconciliation, alertes.

La migration d'un logiciel à un autre est un cas particulier : un flux exécuté une seule fois.

## Les 3 niveaux du M1

| Niveau | Contenu | Plateformes |
|---|---|---|
| 1. Catalogue | Specs d'API chargées, l'IA propose des correspondances entre n'importe lesquelles | Les 8 |
| 2. API simulées | Générées depuis les specs | Les 8, selon la qualité des specs |
| 3. Flux exécutés | Lecture, modèle commun, validation, écriture, réconciliation, supervision | 3 flux, tous vers IFS |

## Catalogue des plateformes

| Plateforme | Domaine | Rôle en M1 |
|---|---|---|
| Yooz | Factures fournisseurs | Source du flux 1 |
| IFS | ERP | Cible des 3 flux |
| Lucca | SIRH | Source du flux 2, outil maître des collaborateurs |
| Progessi | Gestion d'affaires | Source du flux 3 (feuilles de temps) |
| TeamTailor | Recrutement | Catalogue (flux exécuté en M2) |
| Personio | Gestion des temps et absences (remplace eTemptation, sans doc publique) | Catalogue |
| Odoo (Notes de frais) | Notes de frais (remplace Notilus, sans API publique) | Catalogue |
| Sage | Comptabilité, banque (Embedded Accounting API) | Catalogue |

## Les 3 flux exécutés

| Flux | Objet | Priorité | Dépendance |
|---|---|---|---|
| Flux 1 : Yooz vers IFS | Factures fournisseurs rapprochées des commandes d'achat | Indispensable | Fournisseurs et commandes présents dans IFS |
| Flux 2 : Lucca vers IFS | Collaborateurs : créations, modifications, départs | Indispensable | Aucune |
| Flux 3 : Progessi vers IFS | Feuilles de temps validées | Important | Flux 2 : le collaborateur doit exister dans IFS |

**Étapes communes :** déclenchement (planning ou webhook), lecture par le connecteur source, stockage bronze, conversion silver (modèle commun) et contrôles, écriture par le connecteur IFS, réconciliation, journal et alertes.

**Points métier à retenir :**
- Flux 1 : une facture sans commande ou en écart avec sa commande est mise de côté, pas envoyée.
- Flux 2 : Lucca fait foi. Une modification dans IFS ne remonte pas dans Lucca.
- Flux 3 : une feuille de temps d'un collaborateur absent d'IFS est mise de côté.

Les champs exacts sont à établir à partir des specs de `mocks/specs/`. **Ne jamais inventer de champ** : s'appuyer uniquement sur les spécifications.

## Hors M1

Données réelles, exécution sans validation humaine, écriture vers une autre cible qu'IFS. Flux prévus en M2 : TeamTailor vers Lucca, Odoo vers IFS (notes de frais), un flux vers Sage (à redéfinir : Sage Embedded Accounting ne couvre pas la paie).

## Positionnement

L'existant est riche (n8n, Make, Workato, Boomi, outils des éditeurs, startups IA). DataLift vise les PME, les logiciels utilisés en France, une IA qui propose avec un humain qui valide, et une supervision intégrée. On réutilise les briques open source (Magneto pour la correspondance de schémas, outils de qualité de données) plutôt que de les recréer.
