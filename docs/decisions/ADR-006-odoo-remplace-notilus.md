# ADR-006 — Odoo Notes de frais remplace Notilus

- **Statut :** adoptée
- **Date :** 2026-10-15
- **Auteur :** Youcef Addou

## Contexte

Le catalogue M1 prévoit Notilus (Cegid) pour les notes de frais, avec un flux M2 vers IFS. Notilus n'a aucune documentation d'API publique : Cegid la réserve à ses clients, et aucun dépôt ni aucune spec n'existe en ligne (recherche du 2026-10-15). Le seul fichier obtenu (`cegid_notilus_openapi.json`) décrivait en réalité le service d'archivage électronique de Cegid.

## Options étudiées

1. **Garder Notilus avec une spec reconstituée** à partir du modèle Odoo `hr_expense` et des guides utilisateurs Notilus. Avantage : le logiciel prévu reste au catalogue. Inconvénient : l'API entière est inventée, donc invérifiable.
2. **Remplacer par un SaaS équivalent** (SAP Concur, Yokoy). Avantage : métier identique. Inconvénient : specs trouvées seulement dans des catalogues tiers, et pas d'environnement de test gratuit.
3. **Remplacer par Odoo Notes de frais** (Community, LGPL-3). Avantages : API externe officielle et documentée (JSON-2), logiciel gratuit qu'on peut auto-héberger en Docker, avec ses vraies règles métier ; nouveau style d'API (RPC) qui diversifie les connecteurs. Inconvénient : moins riche que Notilus sur les ordres de mission et les déplacements.

## Décision

Option 3 : Odoo Notes de frais remplace Notilus dans le catalogue, et le flux M2 devient « Odoo vers IFS (notes de frais) ». Au lieu d'un mock construit depuis une spec, on fait tourner un vrai Odoo Community avec des données fictives. C'est une variante d'ADR-002.

## Conséquences

- Spec et source dans `mocks/specs/odoo/` ; catalogue mis à jour dans `docs/CONTEXT.md`, `docs/ROADMAP.md`, `docs/GLOSSARY.md` et le README.
- À faire : service Odoo dans le `docker compose` des mocks, puis le script qui charge les données fictives.
- À faire valider par FORTIL si Notilus venait d'un besoin client.
- À surveiller : la version d'Odoo (JSON-2 à partir de 19 ; XML-RPC et JSON-RPC retirés en Odoo 22).
- La numérotation ADR-005 est réservée à l'ADR « ontologie » (DL-112).
