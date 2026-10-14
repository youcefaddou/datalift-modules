# DataLift, expliqué simplement

> Ce document sert à ce qu'on parte tous de la même image du projet. Pas besoin d'être expert en données pour le lire.

## Le problème de départ

Prends une entreprise de 50 à 200 personnes. Elle utilise une dizaine de logiciels :
- un pour les factures fournisseurs (Yooz) ;
- un pour les RH (Lucca) ;
- un pour les feuilles de temps (Progessi) ;
- un gros logiciel central qui gère un peu tout (IFS, ce qu'on appelle un ERP) ;
- et quelques autres.

Ces logiciels ne se parlent pas bien entre eux. Résultat : des gens recopient les mêmes infos d'un outil à l'autre, font des exports Excel ou bricolent des scripts qui cassent au moindre changement. C'est lent, ça crée des erreurs, et personne n'aime faire ça.

## Ce que fait DataLift

DataLift sert de **traducteur et de gare de triage** entre ces logiciels. Concrètement, c'est une application web qui fait cinq choses :

1. **Se brancher** sur chaque logiciel. Chaque logiciel propose une « porte d'entrée » officielle pour lire ou écrire ses données : son API. Pour chaque logiciel, on écrit un petit module qui sait passer par cette porte : un **connecteur**.
2. **Ranger les données dans une langue commune.** Yooz appelle une facture d'une certaine façon, IFS d'une autre. On définit une seule façon de décrire une Facture, un Fournisseur, un Collaborateur, une Feuille de temps, peu importe le logiciel d'origine. C'est notre **modèle commun** (Palantir appelle ça une « ontologie »).
3. **Comprendre une demande en français.** L'utilisateur écrit par exemple : « envoie les factures validées de Yooz vers IFS ».
4. **Proposer, puis faire valider.** L'IA propose comment faire : quel champ de Yooz correspond à quel champ d'IFS, quelles transformations appliquer, avec un niveau de confiance. **Un humain relit et valide.** Rien ne part sans cette validation.
5. **Exécuter et surveiller.** DataLift fait le transfert, vérifie que tout est bien arrivé et prévient s'il y a un souci.

## Une image pour s'en souvenir

Imagine un bureau de traduction :
- les **connecteurs** sont les coursiers qui vont chercher et déposer les documents chez chaque client ;
- le **modèle commun** est la langue de travail interne du bureau ;
- l'**IA** est un traducteur qui prépare un premier jet ;
- l'**humain** est le relecteur qui signe avant l'envoi ;
- la **supervision** est le suivi des envois : tout est arrivé ? rien en double ? rien de perdu ?

## Le parcours type d'un utilisateur

1. Il crée un espace pour l'entreprise cliente.
2. Il branche les logiciels de l'entreprise, en piochant dans notre catalogue de connecteurs.
3. DataLift récupère les données et fait un premier bilan : doublons, infos manquantes, incohérences.
4. Il décrit ce qu'il veut en langage naturel.
5. L'IA propose le flux et les correspondances de champs.
6. Il vérifie, corrige si besoin, et valide.
7. DataLift exécute, contrôle et garde une trace de tout.

## Ce qu'on construit cette année (M1)

On travaille avec 8 logiciels. Pour les 8, l'IA doit savoir proposer des correspondances. Pour 3 d'entre eux, on va jusqu'au bout, c'est-à-dire un vrai transfert vers IFS :

| Flux | Ce qui circule | Règle importante |
|---|---|---|
| 1. Yooz → IFS | Les factures fournisseurs | Une facture qui ne correspond à aucune commande est mise de côté, pas envoyée |
| 2. Lucca → IFS | Les collaborateurs (arrivées, changements, départs) | C'est Lucca qui fait foi |
| 3. Progessi → IFS | Les feuilles de temps validées | Le collaborateur doit déjà exister dans IFS, donc le flux 2 passe avant |

On n'utilise **jamais de vraies données** : on fabrique des données fictives (dites synthétiques), avec des erreurs glissées exprès pour vérifier que DataLift les repère. Et on travaille avec des **versions simulées** des logiciels, construites à partir de leur documentation officielle.

## Les quelques mots qu'on va entendre souvent

- **API** : la porte d'entrée officielle d'un logiciel pour lire ou écrire ses données.
- **Connecteur** : notre module qui sait parler à l'API d'un logiciel.
- **Modèle commun** : notre façon unique de décrire les données, quel que soit le logiciel.
- **Bronze, silver, gold** : trois étages de rangement. Bronze, c'est la donnée brute telle qu'on l'a reçue. Silver, la donnée nettoyée et traduite dans le modèle commun. Gold, des vues prêtes à l'emploi (tableaux de bord, rapprochements).
- **Correspondance (mapping)** : « tel champ ici = tel champ là-bas ».
- **Réconciliation** : vérifier qu'on retrouve bien à l'arrivée ce qui est parti.
- **Lignage** : pour chaque donnée, on sait d'où elle vient et quand on l'a récupérée.
- **Idempotence** : relancer un flux deux fois ne crée jamais de doublon.

## En une phrase

DataLift relie les logiciels d'une entreprise : l'IA prépare le travail, un humain valide, et la plateforme exécute proprement en gardant une trace de tout.

Pour aller plus loin : [CONTEXT.md](CONTEXT.md) (le produit en détail), [ARCHITECTURE.md](ARCHITECTURE.md) (comment c'est construit), [GLOSSARY.md](GLOSSARY.md) (tous les termes).
