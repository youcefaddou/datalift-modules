# Glossaire — DataLift

## Concepts

| Terme | Définition |
| --- | --- |
| ADR | Architecture Decision Record : fiche qui trace une décision technique et sa raison |
| API | Interface qui permet à un logiciel d'échanger des données avec un autre |
| API simulée (mock) | API qui reproduit le comportement d'une vraie à partir de sa spécification |
| Bronze, silver, gold | Couches de données : brut, modèle commun contrôlé, vues prêtes à l'emploi |
| Catalogue | Plateformes dont DataLift connaît les schémas |
| Connecteur | Module qui lit ou écrit dans un logiciel via son API |
| Contrat | Règle partagée entre modules : modèle commun, interface connecteur, définition de flux |
| Correspondance (mapping) | Lien entre un champ source et un champ cible |
| Données synthétiques | Données générées, sans lien avec des personnes ou entreprises réelles, avec des défauts injectés et documentés |
| Flux | Échange de données défini entre une source et une cible |
| Idempotence | Rejouer une opération donne le même résultat, sans doublon |
| Lakehouse | Plateforme qui stocke et analyse de grands volumes de données |
| Lignage | Origine d'une donnée : `source_system`, `source_id`, `extracted_at` |
| Modèle commun (ontologie) | Représentation unique des objets métier, indépendante des logiciels |
| Outil maître | Logiciel qui fait référence pour un type de données (Lucca pour les collaborateurs) |
| Rapprochement | Vérification qu'une facture correspond à sa commande d'achat |
| Réconciliation | Vérification que la cible contient exactement ce qui a été envoyé |
| Score de confiance | Probabilité estimée par l'IA qu'une correspondance proposée soit correcte |
| Story points | Estimation de l'effort d'un ticket Jira (repère : 1 point ≈ 1 h effective, 5 maximum) |
| Webhook | Notification envoyée par un logiciel quand un événement se produit |

## Logiciels du catalogue

| Logiciel | Domaine |
| --- | --- |
| eTemptation | Gestion des temps et des activités |
| IFS | ERP (progiciel de gestion intégré), cible des flux M1 |
| Lucca | Suite de logiciels RH, outil maître des collaborateurs |
| Notilus | Notes de frais |
| Progessi | Gestion d'affaires (projets, temps, facturation) |
| Sage | Comptabilité et paie |
| TeamTailor | Recrutement |
| Yooz | Dématérialisation et validation des factures fournisseurs |
