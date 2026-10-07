# ADR-004 — Contrats communs pour connecteurs et modèle de données

- **Statut :** adoptée
- **Date :** 2026-10-07
- **Auteur :** Youcef Addou

## Contexte

La plateforme doit pouvoir ajouter des logiciels sans modifier son cœur.

## Décision

Tous les connecteurs implémentent la même interface (`read`, `write`, `describe_schema`, `health_check`) et produisent ou consomment le modèle commun défini dans `contracts/`.

## Conséquences

Ajout de connecteurs simplifié. Les contrats deviennent critiques : modification uniquement par ADR.
