# Glossaire — DataLift

## Concepts

| Terme | Définition |
| --- | --- |
| Action | Écriture vers un logiciel, déclarée sur un objet du modèle commun avec ses préconditions (règles métier) |
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
| Identifiant DataLift (`datalift_id`) | Identifiant stable d'un objet, commun à tous les logiciels où il existe |
| Lakehouse | Plateforme qui stocke et analyse de grands volumes de données |
| Lien | Relation déclarée entre deux objets du modèle commun (une facture et sa commande) |
| Lignage | Origine d'une donnée : `source_system`, `source_id`, `extracted_at` |
| Modèle commun (ontologie) | Représentation unique des objets métier, de leurs liens et des actions possibles, indépendante des logiciels |
| Outil maître | Logiciel qui fait référence pour un type de données (Lucca pour les collaborateurs) |
| OpenRouter | Service qui donne accès à de nombreux LLM avec une seule clé et une API compatible OpenAI (ADR-008) |
| Question transverse | Question dont la réponse croise les données de plusieurs logiciels |
| Quantification | Compression d'un modèle (par exemple en 4 bits) pour qu'il tienne dans moins de mémoire GPU |
| Rapprochement | Vérification qu'une facture correspond à sa commande d'achat |
| Réconciliation | Vérification que la cible contient exactement ce qui a été envoyé |
| Score de confiance | Probabilité estimée par l'IA qu'une correspondance proposée soit correcte |
| Story points | Estimation de l'effort d'un ticket Jira (repère : 1 point ≈ 1 h effective, 5 maximum) |
| Veille modèles | Revue, à chaque sprint, des nouveaux modèles disponibles sur OpenRouter pour garder les meilleurs (ADR-008) |
| Webhook | Notification envoyée par un logiciel quand un événement se produit |

## Logiciels du catalogue

| Logiciel | Domaine |
| --- | --- |
| Personio | Gestion des temps et des absences (remplace eTemptation, sans API publique) |
| IFS | ERP (progiciel de gestion intégré), cible des flux M1 |
| Lucca | Suite de logiciels RH, outil maître des collaborateurs |
| Odoo (Notes de frais) | ERP open source, module `hr_expense` (remplace Notilus, sans API publique : ADR-007) |
| Progessi | Gestion d'affaires (projets, temps, facturation) |
| Sage | Comptabilité et banque (Embedded Accounting API) |
| TeamTailor | Recrutement |
| Yooz | Dématérialisation et validation des factures fournisseurs |
