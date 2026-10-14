# DataLift en bref

> Une vue d'ensemble du projet, pour qu'on parte tous de la même compréhension.

## Le problème

Une entreprise de 50 à 200 personnes utilise une dizaine de logiciels métier : factures fournisseurs (Yooz), RH (Lucca), feuilles de temps (Progessi), ERP (IFS), comptabilité, recrutement, notes de frais.

Ces logiciels échangent mal leurs données. En pratique, on ressaisit à la main, on passe par des exports Excel ou par des scripts fragiles. C'est lent et source d'erreurs.

## Ce que fait DataLift

DataLift est une plateforme web d'intégration de données assistée par IA, inspirée de Palantir Foundry. Elle fait cinq choses :

1. **Connecter** les logiciels via leurs API, avec un connecteur par logiciel.
2. **Unifier** les données dans un modèle commun : une définition unique de Facture, Fournisseur, Collaborateur, Feuille de temps, indépendante du logiciel source. C'est l'équivalent de l'ontologie chez Palantir.
3. **Recevoir une demande en langage naturel**, par exemple : « envoie les factures validées de Yooz vers IFS ».
4. **Proposer puis faire valider** : l'IA propose le flux, les correspondances de champs et les transformations, avec un score de confiance. Un humain relit et valide. Aucun flux ne s'exécute sans validation enregistrée.
5. **Exécuter et superviser** : transfert des données, contrôles, réconciliation, alertes.

Une migration d'un logiciel vers un autre n'est qu'un cas particulier : un flux exécuté une seule fois.

## Le parcours utilisateur

1. Créer un espace pour l'entreprise cliente.
2. Brancher ses logiciels à partir du catalogue de connecteurs.
3. DataLift extrait les données et produit un premier diagnostic qualité : doublons, références orphelines, incohérences.
4. Décrire le flux voulu en langage naturel.
5. L'IA propose le flux et le mapping.
6. L'utilisateur corrige si besoin et valide.
7. DataLift exécute, contrôle et journalise.

## Le pipeline

- **Bronze** : données brutes, telles que renvoyées par l'API source.
- **Silver** : données nettoyées, contrôlées et converties dans le modèle commun. Chaque ligne porte son lignage : `source_system`, `source_id`, `extracted_at`.
- **Gold** : vues prêtes à l'emploi, rapprochements, tableau de bord.

Deux garanties sur tous les flux :

- **Idempotence** : rejouer un flux ne crée jamais de doublon.
- **Traçabilité** : on sait d'où vient chaque donnée et qui a validé chaque flux.

## Le périmètre M1

8 logiciels sont au catalogue. Pour les 8, l'IA doit savoir proposer des correspondances. Pour 3 d'entre eux, on va jusqu'à l'exécution réelle vers IFS :

| Flux | Données | Règle métier |
| --- | --- | --- |
| 1. Yooz → IFS | Factures fournisseurs | Une facture sans commande, ou en écart avec sa commande, est mise de côté |
| 2. Lucca → IFS | Collaborateurs (arrivées, modifications, départs) | Lucca fait foi |
| 3. Progessi → IFS | Feuilles de temps validées | Le collaborateur doit exister dans IFS : le flux 2 passe avant |

Aucune donnée réelle : on génère des données synthétiques, avec des défauts injectés volontairement pour tester les contrôles. Les logiciels sont remplacés par des API simulées, générées à partir de leurs spécifications officielles.

## En une phrase

DataLift connecte les logiciels d'une entreprise : l'IA propose les flux et le mapping, un humain valide, et la plateforme exécute avec contrôle, réconciliation et traçabilité.

Pour aller plus loin : [CONTEXT.md](CONTEXT.md), [ARCHITECTURE.md](ARCHITECTURE.md), [GLOSSARY.md](GLOSSARY.md).
