# Feuille de route — DataLift M1 (semaine C)

Les livrables suivent les objectifs officiels des sessions Ydays : c'est sur eux que porte l'évaluation. Un sprint couvre la période qui se termine par une journée Ydays. L'équipe travaille le jour Ydays (7 h) ; entre deux journées, seul le chef de projet avance.

| Journée | Date | Sprint | Livrable (objectif de session) | Contenu DataLift |
| --- | --- | --- | --- | --- |
| Ydays 1 | 14/10/2026 | – | Équipe pressentie | Présentation du projet, recrutement |
| Ydays 2 | 25/11/2026 | Sprint 0 (14/10 → 25/11) | Équipe constituée, environnements prêts | Rôles, onboarding, `make setup`, backlog Jira, specs des 8 plateformes récupérées, ontologie conçue (ADR-005) |
| Ydays 3 | 16/12/2026 | Sprint 1 (26/11 → 16/12) | Projet validé | Oral : cadrage, architecture, données synthétiques v1. Ontologie dans `contracts/` : objets, liens, actions |
| Ydays 4 | 20/01/2027 | Sprint 2 (17/12 → 21/01) | Données chargées et profilées | API simulées, données synthétiques finalisées, connecteurs Yooz et Lucca en lecture, bronze, profilage |
| Ydays 5 | 21/01/2027 | Sprint 2 | Rapport de qualité v1 | Doublons, références orphelines, incohérences sur les données des 3 flux |
| Ydays 6 | 03/03/2027 | Sprint 3 (22/01 → 03/03) | Propositions de mapping avec score de confiance | Agent IA de correspondance, jeu de référence, mesure de précision |
| Ydays 7 | 24/03/2027 | Sprint 4 (04/03 → 24/03) | Mapping validé via l'interface | Interface de validation, règles de transformation |
| Ydays 8 | 14/04/2027 | Sprint 5 (25/03 → 14/04) | Migration complète, rapport de réconciliation | Flux 1 et 2 exécutés vers IFS : nettoyage, anonymisation, idempotence, réconciliation |
| Ydays 9 | 05/05/2027 | Sprint 6 (15/04 → 05/05) | Démo complète | Bout en bout, tests, tableau de bord KPI, questions transverses en langage naturel, documentation, flux 3 |
| Ydays 10 | 26/05/2027 | Sprint 7 (06/05 → 27/05) | Finalisation, recette | Cahier de recette exécuté |
| Ydays 11 | 27/05/2027 | Sprint 7 | Oral final | Présentation et démo |

**Règle de priorité :** si le retard s'accumule, le flux 3 est démontré au niveau catalogue (correspondances proposées) au lieu d'être exécuté. Les flux 1 et 2 ne sont pas négociables. Pour tenir la journée 8, les connecteurs sont construits dès le sprint 2 : l'ingestion passe par eux.

**Ontologie :** sa structure (objets, liens, actions) est livrée en M1, avant les connecteurs. Le M2 construit au-dessus.

**Taille des stories :** une story confiée à l'équipe tient dans une journée Ydays (5 points maximum, repère 1 point ≈ 1 h effective).

## M2 (2027-2028)

- Exploitation de l'ontologie : questions libres, agents qui repèrent une anomalie et proposent une action validée par un humain, applications métier.
- Flux exécutés supplémentaires : TeamTailor vers Lucca, Odoo vers IFS (notes de frais), un flux vers Sage (à redéfinir).
- Modèle IA spécialisé pour la correspondance de champs.
- Socle analytique et tableau de bord avancé.
- Interface v2.
