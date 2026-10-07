# ADR-001 — Architecture en couches bronze, silver, gold

- **Statut :** adoptée
- **Date :** 2026-10-07
- **Auteur :** Youcef Addou

## Contexte

Les données viennent d'API hétérogènes et doivent être traçables jusqu'à leur source.

## Décision

Trois couches : bronze (brut, jamais modifié), silver (modèle commun, contrôlé), gold (vues et réconciliation).

## Conséquences

Traçabilité complète, reprise possible à chaque étape. Coût de stockage supplémentaire, accepté.
