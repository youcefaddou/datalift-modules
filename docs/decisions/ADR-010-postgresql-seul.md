# ADR-010 — Couche gold et tableau de bord : PostgreSQL seul, sans Fabric ni DuckDB

- **Statut :** adoptée
- **Date :** 2026-11-25
- **Auteur :** Youcef Addou

## Contexte

La stack prévoyait « PostgreSQL, Microsoft Fabric (repli DuckDB) » : Fabric pour stocker la couche gold (vues, réconciliation) et alimenter le tableau de bord, DuckDB en repli si l'accès à Fabric manquait. Le ticket DL-39 devait trancher.

Contraintes :

- VPS Hetzner de 2 Go (ADR-009) : chaque composant ajouté réduit la marge.
- Budget limité : Fabric demande une licence ou une capacité.
- Volumes du M1 faibles : données synthétiques de 3 flux.
- Peu de journées de production.

## Options étudiées

1. **PostgreSQL seul** : la couche gold est faite de vues SQL (et de vues matérialisées si besoin) dans la même base que bronze et silver.
   - Avantages : rien de plus à héberger ni à apprendre, aucun coût, un seul langage (SQL) et une seule sauvegarde. Largement suffisant pour les volumes du M1.
   - Inconvénients : pas d'outil d'analyse dédié. Si les volumes explosent au M2, il faudra réévaluer.
2. **Microsoft Fabric pour la couche gold et le tableau de bord Power BI**
   - Avantages : outil reconnu en entreprise, valorisant sur un CV, tableau de bord Power BI prêt à l'emploi.
   - Inconvénients : licence ou accès Ynov à obtenir, un composant de plus, des données copiées hors du VPS, plus de temps de mise en place.

## Décision

Option 1 : **PostgreSQL seul**. La couche gold est faite de vues SQL nommées `gold_` (CONVENTIONS.md). DuckDB n'est plus utile.

## Conséquences

Positives :

- Un composant en moins, et rien à ajouter au budget mémoire de l'ADR-009.
- Bronze, silver et gold dans une seule base : la réconciliation et le lignage se requêtent ensemble.
- L'agent IA interroge gold en SQL en lecture seule (ADR-005), sur la même base.

Négatives :

- Le tableau de bord doit lire PostgreSQL : l'outil reste à choisir avec l'interface (DL-62).
- Si les volumes du M2 l'exigent, une nouvelle ADR sera nécessaire (entrepôt analytique dédié).

À mettre en place : retirer Fabric et DuckDB de `AGENTS.md` et du support de l'oral. Ticket DL-39 clos par cette ADR.
