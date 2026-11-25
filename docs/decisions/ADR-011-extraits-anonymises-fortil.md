# ADR-011 — Extraits anonymisés de FORTIL Infogérance : cadre et pilote

- **Statut :** adoptée
- **Date :** 2026-11-25
- **Auteur :** Youcef Addou

## Contexte

FORTIL Infogérance est le commanditaire de DataLift. Elle accepte de fournir des extraits de ses données, anonymisés, pour un pilote à la fin du M1.

La règle 1 (AGENTS.md) et `DATA_POLICY.md` interdisent toute donnée réelle dans le dépôt et dans les environnements de l'équipe. Un extrait correctement anonymisé n'est plus une donnée personnelle, mais il reste une donnée d'entreprise confidentielle (fournisseurs, montants, projets). Il faut donc un cadre écrit avant d'en recevoir un seul.

Cette ADR traite le ticket DL-40.

## Options étudiées

1. **Rester sur des données 100 % synthétiques**
   - Avantages : aucun risque, aucune procédure.
   - Inconvénients : pas de validation sur des cas réels. Les défauts réels (formats, doublons, cas limites) restent inconnus jusqu'au M2.
2. **Accepter des extraits anonymisés par FORTIL, sous une procédure stricte**
   - Avantages : un vrai pilote pour le commanditaire, et des défauts réalistes pour mesurer la qualité et le mapping.
   - Inconvénients : une procédure à suivre à chaque extrait. Un risque résiduel si l'anonymisation est mal faite.

## Décision

Option 2, avec les règles suivantes.

**Avant réception**

- **L'anonymisation est faite chez FORTIL, avant tout envoi.** Fait par Addou Youcef grace a son Anon_ToolKit. Il marche sur un systeme de clé/valeur, par exemple: Nom = PERSONNE_001ecfz
- Anonymisation irréversible : noms, prénoms, emails, téléphones, adresses, IBAN et numéros de sécurité sociale sont remplacés par des valeurs fictives. Les identifiants sont renumérotés de façon cohérente d'une table à l'autre, et aucune table de correspondance ne quitte FORTIL. Les noms de fournisseurs et de clients sont remplacés.

**À la réception**

- Contrôle automatique avant tout chargement : recherche d'emails, de téléphones, d'IBAN et de numéros de sécurité sociale. Une seule détection bloque l'extrait, qui est renvoyé à FORTIL.
- Relecture humaine par le chef de projet sur un échantillon.

**Pendant le pilote**

- Les extraits ne sont **jamais commités**, ni dans ce dépôt ni dans `datalift-core`. Ils ne sont jamais copiés dans Jira, ni dans un ticket, ni dans une conversation avec un assistant IA.
- Stockage : un volume Docker dédié sur le VPS, accessible au seul chef de projet et au sysadmin.
- **Aucun contenu d'extrait n'est envoyé à un LLM.** L'IA reçoit les noms et les types des champs, avec des exemples synthétiques. C'est suffisant pour proposer les correspondances.
- Les résultats présentés (oral, rapport) sont agrégés : taux de correspondance, défauts détectés, jamais de lignes.

**Après le pilote**

- Suppression des extraits et du volume à la fin du pilote, consignée dans le ticket Jira du pilote (date et confirmation, sans aucun contenu).

**Au M2**

- Un test sur les données réelles de FORTIL demande une nouvelle ADR et une convention de traitement des données avec FORTIL Infogérance.

## Conséquences

Positives :

- Un pilote réel pour le commanditaire, sans donnée personnelle dans l'équipe.
- Des défauts réalistes pour mesurer la qualité et le mapping.

Négatives :

- Une procédure à respecter à chaque extrait.
- La qualité de l'anonymisation dépend de FORTIL : le contrôle automatique limite ce risque sans l'annuler.

À mettre en place, une fois l'ADR adoptée :

- Compléter `DATA_POLICY.md` et la règle 1 d'`AGENTS.md` par un renvoi à cette ADR.
- Le script de contrôle à la réception, avec ses tests (ticket à créer).
- Un ticket « Pilote FORTIL sur extraits anonymisés » pour la fin du M1.
