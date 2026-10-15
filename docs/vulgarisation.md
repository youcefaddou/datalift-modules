# DataLift en bref

> Une vue d'ensemble du projet, pour qu'on parte tous de la même compréhension.

## Le problème

Une entreprise de 50 à 200 personnes utilise une dizaine de logiciels métier : factures fournisseurs (Yooz), RH (Lucca), feuilles de temps (Progessi), ERP (IFS), comptabilité, recrutement, notes de frais.

Ces logiciels échangent mal leurs données. En pratique, on ressaisit à la main, on passe par des exports Excel ou par des scripts fragiles. C'est lent et source d'erreurs.

## Ce que fait DataLift

DataLift est une plateforme web d'intégration de données assistée par IA, inspirée de Palantir Foundry. Elle fait six choses :

1. **Connecter** les logiciels via leurs API, avec un connecteur par logiciel.
2. **Unifier** les données dans un modèle commun : une définition unique de Facture, Fournisseur, Collaborateur, Feuille de temps, indépendante du logiciel source. C'est l'équivalent de l'ontologie chez Palantir. Le modèle décrit aussi les liens entre objets (une facture est liée à sa commande et à son fournisseur) et les actions possibles (envoyer une facture vers IFS, avec ses règles).
3. **Recevoir une demande en langage naturel**, par exemple : « envoie les factures validées de Yooz vers IFS ».
4. **Proposer puis faire valider** : l'IA propose le flux, les correspondances de champs et les transformations, avec un score de confiance. Un humain relit et valide. Aucun flux ne s'exécute sans validation enregistrée.
5. **Exécuter et superviser** : transfert des données, contrôles, réconciliation, alertes.
6. **Interroger** les données de plusieurs logiciels à la fois, par exemple : « quels collaborateurs ont des temps dans Progessi mais n'existent pas encore dans IFS ? ». Aucun logiciel ne sait répondre seul à ce type de question.

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
- **Silver** : données nettoyées, contrôlées et converties dans le modèle commun. Chaque ligne porte son lignage : `source_system`, `source_id`, `extracted_at`. Un même fournisseur ou collaborateur présent dans plusieurs logiciels n'a qu'un seul identifiant DataLift (`datalift_id`).
- **Gold** : vues qui suivent les liens entre objets, rapprochements, tableau de bord. C'est sur ces vues que portent les questions transverses.

Deux garanties sur tous les flux :

- **Idempotence** : rejouer un flux ne crée jamais de doublon.
- **Traçabilité** : on sait d'où vient chaque donnée et qui a validé chaque flux.

## L'IA du projet

- **Modèles open source** de la famille Qwen, servis par un Space Hugging Face privé de l'organisation Ynov. Coût : 0 €.
- **Accès** : chaque membre rejoint l'organisation Ynov sur Hugging Face et dispose de 40 minutes de GPU par jour (ZeroGPU).
- **En développement**, un modèle plus petit de la même famille peut tourner en local sur un PC avec un GPU de 8 Go.
- **Un cadre fixé** : l'IA choisit parmi les objets, les liens et les actions de l'ontologie, ses réponses sont vérifiées automatiquement, et un humain valide.
- **Veille** : les modèles open source évoluent en quelques semaines. À chaque sprint, on teste les nouveaux sur notre jeu de référence et on garde le meilleur.
- **En M2**, un modèle de correspondance spécialisé sera entraîné sur les GPU dédiés de Ynov.
- **Données** : aucune donnée réelle n'est envoyée aux modèles, et tout reste privé sur Hugging Face.

Détails : [ADR-005](decisions/ADR-005-ontologie-liens-actions.md) (ontologie) et [ADR-006](decisions/ADR-006-modele-ia.md) (modèle IA).

## Le périmètre M1

8 logiciels sont au catalogue. Pour les 8, l'IA doit savoir proposer des correspondances. Pour 3 d'entre eux, on va jusqu'à l'exécution réelle vers IFS :

| Flux               | Données                                            | Règle métier                                                               |
| ------------------ | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1. Yooz → IFS     | Factures fournisseurs                               | Une facture sans commande, ou en écart avec sa commande, est mise de côté |
| 2. Lucca → IFS    | Collaborateurs (arrivées, modifications, départs) | Lucca fait foi                                                               |
| 3. Progessi → IFS | Feuilles de temps validées                         | Le collaborateur doit exister dans IFS : le flux 2 passe avant               |

La démo de Ydays 9 montrera aussi des questions transverses posées en langage naturel.

Aucune donnée réelle : on génère des données synthétiques, avec des défauts injectés volontairement pour tester les contrôles. Les logiciels sont remplacés par des API simulées, générées à partir de leurs spécifications officielles.

## En une phrase

DataLift connecte les logiciels d'une entreprise : une IA open source propose les flux et le mapping, un humain valide, et la plateforme exécute avec contrôle, réconciliation et traçabilité.

Pour aller plus loin : [CONTEXT.md](CONTEXT.md), [ARCHITECTURE.md](ARCHITECTURE.md), [GLOSSARY.md](GLOSSARY.md), [décisions d&#39;architecture](decisions/).
