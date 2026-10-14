# ADR-005 — Ontologie : liens et actions dans le modèle commun

- **Statut :** adoptée
- **Date :** 2026-10-14
- **Auteur :** Youcef Addou

## Contexte

Le modèle commun (`contracts/`, ADR-004) prévoit des objets : Supplier, PurchaseOrder, SupplierInvoice, InvoiceLine, Employee, Project, TimeEntry. Les relations entre ces objets restent implicites : rapprochement facture/commande, dépendance temps/collaborateur. Les règles métier des écritures vers IFS (facture sans commande mise de côté, collaborateur absent d'IFS) sont décrites dans `docs/CONTEXT.md`, pas dans le contrat.

Conséquences de cette situation :

- chaque pipeline recode ses propres jointures ;
- impossible de poser des questions qui croisent plusieurs logiciels (questions transverses) ;
- l'agent IA ne dispose d'aucune structure pour raisonner sur les données.

Décision de cadrage : la structure de l'ontologie (objets, liens, actions) est construite en M1. Le M2 construit au-dessus (agents, questions libres, applications). Cette structure doit exister avant l'écriture des connecteurs (Sprint 2), sinon ils devront être repris.

## Options étudiées

1. **Objets seuls, jointures dans les pipelines** (situation actuelle)
   - Avantages : aucun travail supplémentaire.
   - Inconvénients : logique de jointure dupliquée, pas de questions transverses, contrats à refaire en M2 alors que les connecteurs seront écrits.
2. **Liens et actions déclarés dans `contracts/` (Pydantic), stockés en tables relationnelles PostgreSQL**
   - Avantages : même stack que le reste du projet, rien de nouveau à apprendre pour l'équipe. Testable avec pytest. Suffisant pour les questions transverses en SQL. Le travail de conception revient au chef de projet entre les journées Ydays et ne consomme pas les 6 journées de production.
   - Inconvénients : conception à faire tôt, et elle dépend des specs récupérées. Les requêtes de graphe profondes (chemins longs entre objets) sont peu pratiques en SQL.
3. **Base orientée graphe (Neo4j ou équivalent) pour l'ontologie**
   - Avantages : requêtes de chemins natives, outillage plus proche de celui de Palantir.
   - Inconvénients : nouvelle technologie et nouveau langage de requête à apprendre sur 6 journées de production, un service de plus à héberger sur le VPS, deux bases à synchroniser. Aucune question du M1 ne l'exige.

## Décision

Option 2.

**Identité des objets.** Chaque objet silver porte, en plus du lignage, un identifiant DataLift stable : `datalift_id`. La table `silver_identity_map` (type d'objet, `datalift_id`, `source_system`, `source_id`) relie cet identifiant aux identifiants de chaque logiciel. Un collaborateur présent dans Lucca, Progessi et IFS correspond à un seul `datalift_id`. La clé de rapprochement entre logiciels est choisie à partir des specs, par exemple un matricule ou un email s'ils existent.

**Liens.** Chaque lien est déclaré dans le contrat : nom, objet source, objet cible, cardinalité, caractère obligatoire. En silver, un lien se traduit par une colonne de clé étrangère vers le `datalift_id` de l'objet lié. Liste M1, à confirmer avec les specs :

| Lien | De | Vers | Cardinalité |
| --- | --- | --- | --- |
| `supplier` | SupplierInvoice | Supplier | N:1 |
| `purchase_order` | SupplierInvoice | PurchaseOrder | N:1, facultatif (absent : facture mise de côté) |
| `lines` | SupplierInvoice | InvoiceLine | 1:N |
| `supplier` | PurchaseOrder | Supplier | N:1 |
| `employee` | TimeEntry | Employee | N:1 |
| `project` | TimeEntry | Project | N:1 |

**Actions.** Chaque écriture vers un logiciel est déclarée comme une action sur un objet : nom, objet, logiciel cible, préconditions, effet. Un objet qui ne respecte pas une précondition est mis de côté avec son motif. Chaque exécution est journalisée avec la validation qui l'autorise (ADR-003). Actions M1 :

| Action | Objet | Cible | Préconditions |
| --- | --- | --- | --- |
| `send_invoice_to_ifs` | SupplierInvoice | IFS | Facture validée dans Yooz, liée à une commande, sans écart avec elle |
| `sync_employee_to_ifs` | Employee | IFS | Données issues de Lucca (outil maître). Couvre création, modification, départ |
| `send_time_entry_to_ifs` | TimeEntry | IFS | Feuille validée, collaborateur lié déjà présent dans IFS |

**Définition de flux.** Un flux référence une action au lieu d'une cible libre : source, filtre, correspondances, action, planning, statut de validation.

**Questions transverses.** La couche gold expose des vues qui suivent les liens. Une question en langage naturel est traduite en SQL par le LLM et exécutée avec un rôle en lecture seule, limité aux vues gold. La requête est affichée avec la réponse.

## Conséquences

Positives :

- Les jointures sont définies une seule fois, dans le contrat.
- Les questions transverses deviennent possibles en SQL simple.
- L'agent IA travaille sur une structure connue (objets, liens, actions) : ses sorties sont plus faciles à valider, et un modèle plus petit (éventuellement local) devient envisageable.
- Les règles métier deviennent testables : chaque précondition a ses tests unitaires.
- L'idempotence est facilitée : avant d'écrire, une action vérifie dans `silver_identity_map` si l'objet existe déjà dans la cible.

Négatives :

- La story « Définir le modèle commun v1 dans `contracts/` » grossit et doit être découpée.
- La conception dépend des specs : les récupérer reste la priorité du Sprint 0.
- PostgreSQL convient pour 7 objets. À réévaluer en M2 si l'ontologie grossit.

À surveiller :

- La qualité des clés de rapprochement entre logiciels. Les données synthétiques doivent inclure des cas difficiles : homonymes, clé manquante, doublons.
- Toute modification des liens ou des actions passe par une nouvelle ADR (règle d'ADR-004).
