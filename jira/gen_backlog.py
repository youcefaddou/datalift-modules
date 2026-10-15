"""Génère backlog_DL.csv pour l'import Jira (espace DataLift, clé DL)."""
import csv
from pathlib import Path

PRIO = {"M": "High", "S": "Medium", "C": "Low", "W": "Lowest"}
SP = {i: f"DL Sprint {i}" for i in range(8)}

# id, nom, début, fin
EPICS = [
    (1, "Socle et environnements", "2026-10-14", "2026-12-16"),
    (2, "Catalogue et API simulées", "2026-10-14", "2027-05-05"),
    (3, "Données synthétiques", "2026-11-26", "2027-01-20"),
    (4, "Connecteurs", "2026-12-17", "2027-05-05"),
    (5, "Modèle commun", "2026-11-26", "2027-01-21"),
    (6, "Qualité des données", "2026-12-17", "2027-04-14"),
    (7, "Agent IA", "2026-12-17", "2027-03-24"),
    (8, "Interface de validation", "2027-01-22", "2027-03-24"),
    (9, "Exécution et réconciliation", "2027-03-04", "2027-05-05"),
    (10, "Supervision et tableau de bord", "2027-03-25", "2027-05-05"),
    (11, "Sécurité", "2026-11-26", "2027-05-05"),
    (12, "Documentation, recette et pilotage", "2026-10-14", "2027-05-27"),
    (13, "Communication (optionnel)", "2026-11-25", "2027-05-27"),
]

U = "utilisateur métier"
I = "intégrateur"
D = "développeur de l'équipe"
C = "chef de projet"

# epic, sprint (None = backlog), type, titre, en tant que, je veux, afin de, [EF], moscow, points, profil, [critères], [labels+]
S = [
    # ---------- Sprint 0 : 14/10 -> 25/11 (Ydays 2) ----------
    (1, 0, "Task", "Préparer le squelette Python et le Makefile (setup, test, lint)", C, "un squelette (pyproject, ruff, pytest, Makefile) qui s'installe en une commande", "que chaque équipier soit opérationnel en moins d'une heure le 25/11", ["ENF-05", "ENF-06"], "M", 3, "youcef",
     ["`make setup`, `make test`, `make lint` fonctionnent sur un poste Linux vierge", "Un test d'exemple passe", "README à jour"], []),
    (12, 0, "Task", "Configurer Jira : espace DL, sprints, import du backlog", C, "un Jira prêt avec backlog et sprints calés sur les journées Ydays", "piloter le projet et le présenter au jury", ["ENF-06"], "M", 2, "youcef",
     ["Espace DataLift clé DL, sprints 0 à 7 créés avec objectifs", "Backlog importé, épopées datées dans la Chronologie", "5 équipiers invités"], ["pilotage"]),
    (12, 0, "Task", "Relier Jira et GitHub (GitHub for Jira)", C, "voir branches, commits et PR dans chaque ticket", "suivre l'avancement sans double saisie", ["ENF-06"], "S", 1, "youcef",
     ["Application installée sur le dépôt datalift-modules", "Une branche feat/DL-xx apparaît dans le ticket DL-xx", "Règle de nommage ajoutée dans docs/CONVENTIONS.md"], ["pilotage"]),
    (12, 0, "Task", "Remplacer GitHub Projects par Jira dans la documentation", C, "des docs qui citent Jira comme outil de suivi", "que l'équipe utilise un seul outil", ["ENF-06"], "S", 1, "youcef",
     ["README, CONTRIBUTING et ONBOARDING mentionnent Jira", "Plus aucune mention de GitHub Projects"], ["pilotage"]),
    (12, 0, "Task", "Préparer et animer l'onboarding du 25/11", C, "un support d'onboarding (projet, règles, outils, rôles)", "que l'équipe démarre sur les mêmes bases", ["ENF-06"], "M", 2, "youcef",
     ["Support présenté le 25/11", "Rôles attribués et notés dans Jira", "Chacun a lu AGENTS.md et ONBOARDING.md"], ["pilotage"]),
    (1, 0, "Task", "Installer son environnement et lancer make setup", D, "un poste prêt (Python 3.12, Docker, Git, accès au dépôt et à Jira)", "contribuer dès le premier jour", ["ENF-05"], "M", 2, "ia-data",
     ["`make setup` et `make test` passent sur chaque poste", "Chaque équipier a poussé une branche de test liée à un ticket DL"], ["ydays2-autonome"]),
    (1, 0, "Story", "Mettre en place la CI GitHub Actions (lint et tests)", D, "que chaque PR lance ruff et pytest automatiquement", "ne jamais fusionner du code cassé", ["ENF-06"], "M", 3, "infra",
     ["Workflow déclenché sur chaque PR", "Une PR qui casse un test est bloquée", "Badge de statut dans le README"], ["ydays2-autonome"]),
    (1, 0, "Story", "Écrire le docker-compose de base (PostgreSQL)", D, "une base PostgreSQL locale lancée en une commande", "stocker les couches bronze, silver et gold", ["ENF-05"], "M", 3, "infra",
     ["`docker compose up` lance PostgreSQL", "Identifiants lus depuis .env (jamais dans le code)", "Documenté dans infra/README.md"], ["ydays2-autonome"]),
] + [
    (2, 0, "Story", f"Récupérer la spécification d'API {p} et remplir SOURCE.md", I, f"la spécification officielle de l'API {p} dans mocks/specs/{p.lower()}/", "que l'IA et les API simulées s'appuient sur des sources vérifiées", ["EF-10"], "M" if p in ("Yooz", "IFS", "Lucca", "Progessi") else "S", 2, "ia-data",
     [f"Spec (OpenAPI, JSON ou collection Postman) déposée dans mocks/specs/{p.lower()}/", "SOURCE.md rempli : URL, date, version, licence, qualité de la spec", "Aucune donnée réelle dans les exemples"], ["ydays2-autonome"])
    for p in ("Yooz", "IFS", "Lucca", "Progessi", "TeamTailor", "eTemptation", "Odoo", "Sage")
] + [
    # ---------- Sprint 1 : 26/11 -> 16/12 (Ydays 3, oral) ----------
    (5, 1, "Story", "Définir le modèle commun v1 dans contracts/", I, "un schéma unique pour fournisseurs, commandes, factures, collaborateurs, projets et temps", "que tous les connecteurs parlent la même langue", ["EF-12"], "M", 5, "youcef",
     ["Modèles Pydantic v2 versionnés dans contracts/", "Chaque champ provient d'une spec (aucun champ inventé)", "Schéma documenté"], []),
    (5, 1, "Story", "Ajouter le lignage à chaque donnée silver", I, "source_system, source_id et extracted_at sur chaque enregistrement", "retrouver toute donnée jusqu'à sa source", ["EF-13"], "M", 2, "youcef",
     ["Champs de lignage obligatoires dans le modèle commun", "Test qui refuse un enregistrement sans lignage"], []),
    (4, 1, "Story", "Définir l'interface connecteur dans contracts/", I, "un modèle de connecteur (lecture, écriture, pagination, erreurs)", "ajouter un connecteur sans modifier le cœur", ["EF-07", "ENF-07"], "S", 3, "youcef",
     ["Classe abstraite documentée dans contracts/", "Un connecteur factice l'implémente et passe les tests de contrat"], []),
    (3, 1, "Story", "Générer les données synthétiques v1 des 3 flux", I, "des fournisseurs, commandes, factures, collaborateurs, projets et temps synthétiques", "présenter un jeu de données crédible à l'oral de validation", ["ENF-03"], "M", 5, "youcef",
     ["Générateur reproductible (graine fixe)", "Volumes documentés", "Aucune donnée réelle"], []),
    (3, 1, "Story", "Injecter et documenter les défauts v1", I, "des défauts connus (doublons, montants incohérents, facture sans commande, fournisseur inconnu, collaborateur absent, heures hors limites, champs manquants)", "mesurer ce que DataLift détecte", ["EF-50"], "M", 3, "youcef",
     ["Chaque défaut injecté est listé avec son identifiant dans synthetic_data/", "Fichier de vérité terrain exploitable par les tests"], []),
    (1, 1, "Task", "ADR : accès Microsoft Fabric ou repli DuckDB", C, "une décision écrite sur le stockage analytique", "ne pas bloquer le sprint 2", ["ENF-05"], "M", 2, "youcef",
     ["2 options comparées (coût, accès équipe, effort)", "ADR validé dans docs/decisions/"], ["decision"]),
    (11, 1, "Task", "ADR : encadrer l'usage de jeux JSON anonymisés", C, "une procédure écrite pour utiliser des exemples JSON anonymisés", "rester conforme (RGPD, aucune donnée identifiable)", ["EF-82", "ENF-03"], "M", 2, "youcef",
     ["Procédure d'anonymisation vérifiable", "Aucune trace d'origine dans le dépôt ni dans Jira", "DATA_POLICY.md et AGENTS.md mis à jour"], ["decision"]),
    (12, 1, "Task", "Préparer le support de l'oral de validation", C, "une présentation du cadrage, de l'architecture et des données v1", "faire valider le projet le 16/12", [], "M", 3, "youcef",
     ["Support prêt le 15/12", "Démo des données v1 incluse", "Gantt présenté"], ["pilotage"]),
    (12, 1, "Task", "Répéter l'oral de validation en équipe", D, "répéter l'oral et répartir les prises de parole", "présenter un projet maîtrisé par toute l'équipe", [], "M", 2, "ia-data",
     ["Chaque équipier présente sa partie", "Durée respectée"], []),
    # ---------- Sprint 2 : 17/12 -> 21/01 (Ydays 4 + 5) ----------
    (6, 2, "Task", "Définir les règles de qualité et leurs seuils", C, "des règles écrites pour doublons, orphelins et incohérences", "que l'équipe les code sans ambiguïté le 21/01", ["EF-50", "EF-51"], "M", 3, "youcef",
     ["Une fiche par règle : définition, champs, seuil, exemple", "Règles reliées aux défauts injectés"], []),
    (11, 2, "Story", "Stocker les secrets hors du code", I, "que les clés d'API soient lues depuis l'environnement ou un coffre", "qu'aucun secret ne soit dans le dépôt", ["EF-81"], "M", 3, "youcef",
     ["Aucun secret dans le dépôt (scan en CI)", ".env.example à jour", "Connecteurs lisant leurs clés depuis la configuration"], []),
    (7, 2, "Task", "ADR : modèle IA (API ou local) et budget", C, "une décision écrite sur le modèle IA et son coût", "démarrer l'agent IA au sprint 3", ["ENF-08"], "M", 2, "youcef",
     ["2 options comparées (qualité, coût, confidentialité)", "Budget plafond fixé", "ADR validé"], ["decision"]),
    (2, 2, "Story", "Générer l'API simulée Yooz", D, "une API Yooz simulée à partir de sa spec", "développer sans accès à la vraie API", ["EF-11"], "M", 3, "ia-data",
     ["Endpoints factures et commandes servis depuis la spec", "Lancée par docker compose", "Test de contrat qui passe"], []),
    (2, 2, "Story", "Générer l'API simulée Lucca", D, "une API Lucca simulée à partir de sa spec", "développer sans accès à la vraie API", ["EF-11"], "M", 3, "ia-data",
     ["Endpoints collaborateurs servis depuis la spec", "Lancée par docker compose", "Test de contrat qui passe"], []),
    (2, 2, "Story", "Générer l'API simulée IFS (lecture et écriture)", D, "une API IFS simulée qui accepte les écritures", "tester les envois sans ERP réel", ["EF-11"], "M", 5, "infra",
     ["Endpoints fournisseurs, commandes, factures, collaborateurs, temps", "Une écriture est relisible", "Lancée par docker compose"], []),
    (3, 2, "Story", "Finaliser les données synthétiques et les charger dans les API simulées", D, "les API simulées alimentées avec les données synthétiques", "que les connecteurs lisent des données réalistes", ["EF-01", "EF-02"], "M", 3, "ia-data",
     ["Données v2 chargées dans Yooz, Lucca et IFS simulés", "Défauts injectés présents et documentés"], []),
    (4, 2, "Story", "Connecteur Yooz : lire les factures validées et leur commande", I, "récupérer les factures validées avec leur référence de commande", "alimenter le flux 1", ["EF-01", "EF-05"], "M", 5, "ia-data",
     ["Toutes les factures du jeu de test récupérées avec leur commande", "Pagination et authentification gérées", "Implémente l'interface connecteur"], []),
    (4, 2, "Story", "Connecteur Lucca : lire les collaborateurs", I, "récupérer les créations, modifications et départs", "alimenter le flux 2", ["EF-02", "EF-05"], "M", 5, "ia-data",
     ["Tous les collaborateurs du jeu de test récupérés", "Pagination et authentification gérées", "Implémente l'interface connecteur"], []),
    (4, 2, "Story", "Stocker les réponses brutes en bronze", I, "une copie brute et horodatée de chaque lecture", "pouvoir rejouer et auditer", ["EF-13"], "M", 3, "infra",
     ["Tables bronze_ créées", "Données identiques à la source, horodatées", "Relecture possible"], []),
    (6, 2, "Story", "Profiler les tables bronze", U, "le volume, les types, les valeurs nulles et distinctes de chaque table", "connaître l'état des données avant de les utiliser", ["EF-50"], "M", 3, "ia-data",
     ["Profil généré pour toutes les tables bronze", "Exportable (HTML ou CSV)"], []),
    (5, 2, "Story", "Convertir Yooz et Lucca vers le modèle commun (silver)", I, "les données bronze converties dans le modèle commun", "préparer l'envoi vers IFS", ["EF-12", "EF-13"], "M", 5, "ia-data",
     ["Tables silver_ remplies", "Lignage présent sur chaque ligne", "Tests de conversion"], []),
    (6, 2, "Story", "Détecter les doublons", U, "que les doublons (factures, collaborateurs) soient signalés", "ne pas envoyer deux fois la même donnée", ["EF-50", "EF-71"], "M", 3, "ia-data",
     ["Au moins [90 %] des doublons injectés détectés", "Test sur la vérité terrain"], []),
    (6, 2, "Story", "Détecter les références orphelines", U, "que les factures sans commande, fournisseurs inconnus et collaborateurs absents soient signalés", "les mettre de côté avant envoi", ["EF-50"], "M", 3, "ia-data",
     ["Toutes les références orphelines injectées détectées", "Test sur la vérité terrain"], []),
    (6, 2, "Story", "Détecter les incohérences (montants, champs manquants, heures)", U, "que les valeurs incohérentes soient signalées", "corriger avant envoi", ["EF-50", "EF-71"], "M", 3, "ia-data",
     ["Au moins [90 %] des incohérences injectées détectées", "Test sur la vérité terrain"], []),
    (6, 2, "Story", "Rapprocher chaque facture de sa commande d'achat", U, "que chaque facture soit comparée à sa commande", "bloquer les factures sans commande ou en écart", ["EF-51"], "M", 5, "ia-data",
     ["Factures sans commande signalées", "Écarts de montant ou de quantité signalés avec leur valeur"], []),
    (6, 2, "Story", "Générer le rapport de qualité v1", U, "un rapport lisible par un non-technicien", "comprendre la qualité de mes données", ["EF-50"], "M", 3, "ia-data",
     ["Synthèse et détail par table", "Taux de détection des défauts injectés affiché", "Exportable"], []),
    (1, 2, "Story", "Écrire les tests de contrat des connecteurs", D, "des tests qui vérifient chaque connecteur contre son API simulée", "détecter une rupture de contrat", ["ENF-06"], "M", 3, "infra",
     ["Tests dans tests/contract lancés en CI", "Un champ manquant fait échouer le test"], []),
    # ---------- Sprint 3 : 22/01 -> 03/03 (Ydays 6) ----------
    (7, 3, "Task", "Préparer le socle de l'agent IA (client modèle, coût)", C, "un client IA configuré, avec clé hors du code et mesure du coût", "que l'équipe se concentre sur le mapping le 03/03", ["ENF-08", "EF-81"], "M", 3, "youcef",
     ["Appel au modèle fonctionnel", "Coût et jetons journalisés par appel"], []),
    (8, 3, "Task", "ADR : technologie de l'interface (Next.js ou Streamlit)", C, "une décision écrite sur l'interface", "démarrer l'interface au sprint 4", ["EF-30"], "M", 2, "youcef",
     ["2 options comparées (effort, compétences équipe, rendu)", "ADR validé", "Squelette d'interface prêt avant le 24/03"], ["decision"]),
    (2, 3, "Story", "Charger les schémas des 8 plateformes dans le catalogue", I, "consulter le schéma de chaque plateforme", "que l'IA travaille sur toutes les paires", ["EF-10"], "M", 3, "ia-data",
     ["Schémas des 8 plateformes consultables", "Plateformes à spec incomplète signalées"], []),
    (7, 3, "Story", "Comprendre une demande en langage naturel", U, "écrire ma demande en français", "créer un flux sans compétence technique", ["EF-20"], "M", 5, "ia-data",
     ["Source, cible, objet et filtre extraits", "Demandes de référence des 3 flux comprises"], []),
    (7, 3, "Story", "Proposer la correspondance des champs avec score de confiance", I, "une proposition champ à champ avec un score", "valider vite les cas sûrs et me concentrer sur les autres", ["EF-21"], "M", 5, "ia-data",
     ["Proposition pour les 3 flux", "Score de confiance par champ", "Aucun champ inventé hors spec"], []),
    (7, 3, "Story", "Constituer le jeu de référence et mesurer la précision", I, "un jeu de correspondances attendues et un calcul de précision", "prouver la qualité du mapping", ["EF-21"], "M", 3, "ia-data",
     ["Jeu de référence pour les 3 flux", "Précision mesurée automatiquement", "Au moins [80 %] de correspondances correctes"], []),
    (7, 3, "Story", "Expliquer chaque proposition de correspondance", U, "une explication courte pour chaque champ proposé", "comprendre et faire confiance", ["EF-23"], "S", 3, "ia-data",
     ["Explication affichée pour chaque champ"], []),
    (7, 3, "Story", "Proposer des correspondances pour toute paire du catalogue", I, "une proposition entre deux plateformes quelconques", "préparer les flux du M2", ["EF-22"], "M", 5, "ia-data",
     ["Proposition générée pour toute paire des 8 plateformes", "Résultat consultable"], []),
    (4, 3, "Story", "Connecteur IFS : écrire et relire les collaborateurs", I, "créer et mettre à jour les collaborateurs dans IFS", "alimenter le flux 2", ["EF-04", "EF-05"], "M", 5, "infra",
     ["Enregistrement créé puis relu à l'identique", "Mise à jour et départ gérés"], []),
    # ---------- Sprint 4 : 04/03 -> 24/03 (Ydays 7) ----------
    (9, 4, "Task", "ADR : outil d'orchestration (Airflow, Dagster ou Fabric)", C, "une décision écrite sur l'orchestration", "exécuter les flux au sprint 5", ["EF-40"], "M", 2, "youcef",
     ["Options comparées (effort, coût, intégration)", "ADR validé"], ["decision"]),
    (11, 4, "Story", "Authentifier les utilisateurs et gérer les rôles", I, "des rôles lecture et validation", "qu'un rôle lecture ne puisse pas valider un flux", ["EF-80"], "M", 5, "youcef",
     ["Connexion obligatoire", "Un rôle lecture ne peut pas valider un flux (test)"], []),
    (8, 4, "Story", "Afficher le flux proposé et ses correspondances", U, "voir le flux et ses correspondances dans une interface", "les vérifier sans formation technique", ["EF-30"], "M", 5, "ia-data",
     ["Source, cible, champs, score et explication affichés", "Utilisable sans formation technique"], []),
    (8, 4, "Story", "Valider, corriger ou rejeter chaque correspondance", I, "valider, corriger ou rejeter chaque proposition", "garder la main sur ce qui est exécuté", ["EF-31"], "M", 5, "ia-data",
     ["Chaque proposition modifiable", "Décision enregistrée avec auteur et date"], []),
    (8, 4, "Story", "Bloquer l'exécution d'un flux non validé", I, "qu'aucun flux ne s'exécute sans validation enregistrée", "respecter le principe l'IA propose, l'humain valide", ["EF-25"], "M", 3, "ia-data",
     ["Test : un flux non validé ne s'exécute pas", "Message clair à l'utilisateur"], []),
    (8, 4, "Story", "Historiser les versions d'un flux", I, "consulter les versions précédentes d'un flux", "savoir ce qui a changé et qui l'a validé", ["EF-32"], "S", 3, "ia-data",
     ["Version précédente consultable", "Auteur et date de chaque version"], []),
    (7, 4, "Story", "Proposer et tester les transformations (formats, dates, codes)", I, "les transformations nécessaires proposées par l'IA", "envoyer des données au bon format", ["EF-24"], "S", 5, "ia-data",
     ["Transformations testées sur les cas documentés", "Validables dans l'interface"], []),
    (4, 4, "Story", "Connecteur IFS : écrire et relire les factures fournisseurs", I, "créer les factures fournisseurs dans IFS", "alimenter le flux 1", ["EF-04"], "M", 5, "infra",
     ["Enregistrement créé puis relu à l'identique", "Lien avec la commande d'achat conservé"], []),
    (8, 4, "Story", "Tester l'interface avec un utilisateur non technique", U, "valider un flux sans aide", "prouver l'ergonomie", ["EF-30"], "M", 2, "ia-data",
     ["Un testeur non technique valide un flux seul", "Remarques notées en tickets"], []),
    # ---------- Sprint 5 : 25/03 -> 14/04 (Ydays 8) ----------
    (9, 5, "Story", "Déployer l'orchestrateur (à la demande et planifié)", I, "lancer un flux à la demande ou selon un planning", "automatiser les échanges", ["EF-40"], "M", 5, "youcef",
     ["Exécution déclenchée et tracée", "Planning configurable"], []),
    (10, 5, "Story", "Journaliser chaque exécution", I, "la durée, les volumes, le statut et les erreurs de chaque exécution", "superviser les flux", ["EF-60", "ENF-04"], "M", 3, "youcef",
     ["Journal consultable par flux et par exécution"], []),
    (10, 5, "Story", "Alerter en cas d'échec ou d'anomalie", I, "une alerte en cas d'échec ou d'anomalie", "réagir vite", ["EF-61"], "M", 3, "youcef",
     ["Alerte reçue en moins de [5] minutes", "Test avec un échec provoqué"], []),
    (11, 5, "Story", "Pseudonymiser les données des collaborateurs hors démo", I, "que les données personnelles soient pseudonymisées hors démo", "protéger les collaborateurs", ["EF-82"], "M", 3, "youcef",
     ["Accès restreint", "Pseudonymisation cohérente entre tables", "Test : aucune donnée identifiable dans le jeu pseudonymisé"], []),
    (9, 5, "Story", "Exécuter le flux 2 : Lucca vers IFS", U, "synchroniser les collaborateurs de Lucca dans IFS", "que IFS reflète toujours Lucca", ["EF-44"], "M", 5, "ia-data",
     ["Créations, modifications et départs répercutés dans IFS", "Une modification dans IFS ne remonte pas dans Lucca"], ["flux-2"]),
    (9, 5, "Story", "Exécuter le flux 1 : Yooz vers IFS", U, "envoyer les factures validées de Yooz vers IFS", "ne plus les ressaisir", ["EF-40", "EF-51"], "M", 5, "ia-data",
     ["Factures rapprochées envoyées", "Factures sans commande ou en écart mises de côté"], ["flux-1"]),
    (9, 5, "Story", "Garantir l'idempotence des flux", I, "que rejouer un flux ne crée aucun doublon", "relancer sans risque", ["EF-43", "ENF-02"], "M", 5, "ia-data",
     ["Test : deux exécutions donnent le même résultat dans IFS"], []),
    (9, 5, "Story", "Mettre de côté les enregistrements en erreur", I, "la liste des enregistrements rejetés avec leur motif", "les retraiter", ["EF-45"], "M", 3, "ia-data",
     ["Rejets listés avec motif", "Retraitement possible"], []),
    (9, 5, "Story", "Produire le rapport de réconciliation", U, "comparer la source et la cible après exécution", "prouver que rien n'est perdu", ["EF-52"], "M", 5, "ia-data",
     ["Rapport par flux", "Aucun écart non expliqué (rejet, filtre, doublon)"], []),
    (4, 5, "Story", "Rejouer les erreurs temporaires sans doublon", I, "que les erreurs temporaires soient rejouées automatiquement", "ne pas perdre de données", ["EF-06", "ENF-02"], "M", 3, "infra",
     ["Erreur temporaire simulée puis rejouée sans doublon"], []),
    (6, 5, "Story", "Appliquer les règles de nettoyage validées avant envoi", I, "les données nettoyées selon les règles validées", "envoyer des données propres", ["EF-50"], "M", 3, "ia-data",
     ["Données nettoyées conformes aux règles", "Traçabilité des corrections"], []),
    # ---------- Sprint 6 : 15/04 -> 05/05 (Ydays 9) ----------
    (11, 6, "Story", "Tenir un journal d'audit des actions sensibles", I, "tracer validations, modifications et suppressions", "savoir qui a fait quoi", ["EF-83"], "S", 3, "youcef",
     ["Validation, modification et suppression tracées avec auteur et date"], []),
    (10, 6, "Task", "Mesurer le coût et la consommation des appels IA", C, "le coût et le nombre d'appels IA par flux", "maîtriser le budget", ["ENF-08"], "S", 2, "youcef",
     ["Coût par flux visible dans le tableau de bord"], []),
    (9, 6, "Task", "Tester la performance (1 000 enregistrements)", C, "vérifier le temps de traitement", "respecter l'exigence de performance", ["ENF-01"], "S", 2, "youcef",
     ["[1 000] enregistrements par flux traités en moins de [5] minutes"], []),
    (2, 6, "Story", "Générer l'API simulée Progessi", D, "une API Progessi simulée", "développer le flux 3", ["EF-11"], "S", 3, "ia-data",
     ["Feuilles de temps servies depuis la spec", "Lancée par docker compose"], ["flux-3"]),
    (4, 6, "Story", "Connecteur Progessi : lire les feuilles de temps validées", I, "récupérer les feuilles de temps validées", "alimenter le flux 3", ["EF-03"], "S", 3, "ia-data",
     ["Toutes les feuilles validées récupérées"], ["flux-3"]),
    (4, 6, "Story", "Connecteur IFS : écrire les temps", I, "créer les temps dans IFS", "alimenter le flux 3", ["EF-04"], "S", 3, "infra",
     ["Enregistrement créé puis relu à l'identique"], ["flux-3"]),
    (9, 6, "Story", "Exécuter le flux 3 en respectant l'ordre collaborateurs puis temps", U, "envoyer les feuilles de temps validées vers IFS", "ne plus les ressaisir", ["EF-41"], "M", 5, "ia-data",
     ["Aucun temps envoyé pour un collaborateur absent d'IFS", "Temps orphelins mis de côté"], ["flux-3"]),
    (10, 6, "Story", "Tableau de bord : volumes, délais et taux d'erreur par flux", "décideur", "suivre les flux d'un coup d'œil", "piloter l'activité", ["EF-70"], "M", 5, "ia-data",
     ["Indicateurs par flux à jour", "Accessible depuis l'interface"], []),
    (10, 6, "Story", "Signaler les anomalies dans le tableau de bord", "décideur", "voir les anomalies (montants, doublons, heures hors limites)", "agir avant qu'elles coûtent", ["EF-71"], "S", 3, "ia-data",
     ["Anomalies injectées signalées"], []),
    (12, 6, "Story", "Écrire les tests de bout en bout des flux 1 et 2", D, "des tests e2e qui rejouent les flux", "sécuriser la démo", ["ENF-06"], "M", 3, "infra",
     ["Tests dans tests/e2e lancés en CI", "Flux 1 et 2 couverts"], []),
    (12, 6, "Story", "Rédiger la documentation utilisateur et technique", D, "une documentation à jour", "qu'un nouvel arrivant comprenne et utilise DataLift", ["ENF-06"], "M", 3, "ia-data",
     ["Guide utilisateur", "Guide d'installation", "Architecture à jour"], []),
    # ---------- Sprint 7 : 06/05 -> 27/05 (Ydays 10 + 11) ----------
    (12, 7, "Task", "Rédiger le cahier de recette", C, "un test de recette par exigence M", "prouver que le cahier des charges est respecté", [], "M", 3, "youcef",
     ["Une ligne par exigence M avec résultat attendu"], ["pilotage"]),
    (12, 7, "Task", "Exécuter le cahier de recette", D, "dérouler chaque test de recette", "valider le produit", [], "M", 5, "ia-data",
     ["Chaque test exécuté et noté", "Anomalies créées en tickets"], []),
    (12, 7, "Task", "Corriger les anomalies de recette", D, "corriger les anomalies bloquantes", "livrer un produit stable", [], "M", 5, "ia-data",
     ["Aucune anomalie bloquante ouverte"], []),
    (12, 7, "Task", "Préparer le support et la démo de l'oral final", C, "une présentation et une démo rodées", "réussir l'oral final", [], "M", 3, "youcef",
     ["Support prêt", "Démo enregistrée en secours"], ["pilotage"]),
    (12, 7, "Task", "Répéter l'oral final en équipe", D, "répéter l'oral", "présenter un projet maîtrisé", [], "M", 2, "ia-data",
     ["Chaque équipier présente sa partie", "Durée respectée"], []),
    # ---------- Backlog sans sprint ----------
    (9, None, "Story", "Déclencher un flux sur événement (webhook)", I, "qu'un événement source déclenche l'envoi", "réduire le délai", ["EF-42"], "C", 5, "ia-data",
     ["Un événement source déclenche l'envoi"], []),
] + [
    (13, None, "Task", t, "membre de l'équipe", w, a, [], "C", pts, "marketing", acs, ["optionnel"])
    for t, w, a, pts, acs in [
        ("Étude de marché et concurrence", "une analyse de l'existant (n8n, Make, Workato, Boomi...)", "positionner DataLift", 3, ["Tableau comparatif", "Sources citées"]),
        ("Positionnement et proposition de valeur", "une proposition de valeur claire", "convaincre le jury", 2, ["Une phrase, trois arguments, une cible"]),
        ("Pitch de l'oral final", "un pitch de 2 minutes", "ouvrir l'oral avec impact", 3, ["Pitch répété et chronométré"]),
        ("Identité visuelle à partir du logo", "une charte simple (couleurs, typographie)", "avoir des supports cohérents", 3, ["Charte appliquée aux supports"]),
        ("Présence sur les réseaux", "une page projet et quelques publications", "valoriser le projet", 2, ["Page créée", "Publications planifiées"]),
    ]
]


def describe(asa, want, sothat, efs, moscow, prof, acs):
    que = "qu'" if asa[0] in "aeiouéèh" else "que "
    afin = "afin " if sothat.startswith(("que ", "qu'")) else ("afin d'" if sothat[0] in "aeiouéèh" else "afin de ")
    lines = [f"En tant {que}{asa}, je veux {want}, {afin}{sothat}.", ""]
    lines.append("Exigences : " + (", ".join(efs) if efs else "aucune (pilotage)") + f" | MoSCoW : {moscow} | Profil : {prof}")
    lines += ["", "Critères d'acceptation :"] + [f"- {a}" for a in acs]
    lines += ["", "Définition de terminé : code relu en PR, tests verts en CI, ticket DL cité dans la branche et les commits."]
    return "\n".join(lines)


NL = 4  # colonnes Labels
header = ["Issue ID", "Issue Type", "Summary", "Parent", "Description", "Priority", "Story Points", "Sprint", "Start date", "Due date"] + ["Labels"] * NL
rows = []
for eid, name, start, due in EPICS:
    rows.append([eid, "Epic", name, "", f"Épopée DataLift M1 : {name}.", "", "", "", start, due] + [""] * NL)
for n, (ep, sp, typ, title, asa, want, sothat, efs, mo, pts, prof, acs, extra) in enumerate(S, start=100):
    labels = ([prof] + efs + extra)[:NL]
    rows.append([n, typ, title, ep, describe(asa, want, sothat, efs, mo, prof, acs), PRIO[mo], pts,
                 SP[sp] if sp is not None else "", "", ""] + labels + [""] * (NL - len(labels)))

out = Path(__file__).with_name("backlog_DL.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([header] + rows)

# Résumé
from collections import defaultdict
tot = defaultdict(lambda: defaultdict(int))
for ep, sp, typ, title, asa, want, sothat, efs, mo, pts, prof, acs, extra in S:
    who = "youcef" if prof == "youcef" else ("optionnel" if prof == "marketing" else "equipe")
    tot["Backlog" if sp is None else SP[sp]][who] += pts
print(f"{out} : {len(EPICS)} épopées, {len(S)} tickets")
for k in sorted(tot):
    print(f"  {k:14} équipe {tot[k]['equipe']:3}  youcef {tot[k]['youcef']:3}  optionnel {tot[k]['optionnel']:3}")
covered = sorted({e for s in S for e in s[7]})
print("Exigences couvertes :", ", ".join(covered))
