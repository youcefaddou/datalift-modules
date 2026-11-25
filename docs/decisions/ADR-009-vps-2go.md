# ADR-009 — VPS Hetzner CPX12 (2 Go) et budget mémoire par service

- **Statut :** proposée
- **Date :** 2026-11-25
- **Auteur :** Youcef Addou

## Contexte

L'environnement d'équipe tourne sur un VPS Hetzner avec Docker Compose (ARCHITECTURE.md). L'offre restait à choisir.

Contraintes :

- Coût mensuel le plus bas possible.
- Plus aucun modèle d'IA hébergé : les LLM sont appelés par HTTP via OpenRouter (ADR-008).
- Services à faire tourner : PostgreSQL (bronze, silver, gold), les mocks FastAPI (IFS, Progessi, puis Yooz), Odoo Community (ADR-007), puis l'API et l'interface de DataLift.
- Il faut pouvoir monter en puissance sans tout refaire.

## Options étudiées

1. **CPX12 : 1 vCPU AMD, 2 Go de RAM, 40 Go de disque (environ 11 €/mois)**
   - Avantages : le moins cher, et suffisant pour la charge du M1 (quelques utilisateurs, des volumes de données synthétiques faibles).
   - Inconvénients : la RAM est juste. Chaque service doit être réglé au plus bas et sa mémoire mesurée.
2. **Offre à 4 Go (environ 20 €/mois)**
   - Avantages : une marge confortable, sans réglage particulier.
   - Inconvénients : un coût presque doublé pour une charge qui n'en a pas besoin au M1.

## Décision

Option 1 : **CPX12**, avec un budget de mémoire par service imposé par `mem_limit` dans `infra/docker-compose.yml`.

| Service | Limite | Réglages |
| --- | --- | --- |
| PostgreSQL 17 (alpine) | 384 Mo | `shared_buffers=96MB`, `max_connections=30`, une seule instance partagée par DataLift et Odoo |
| Odoo 19 Community | 640 Mo | Module Notes de frais (`hr_expense`) uniquement, sans données de démo, `workers=0`, aucun cron |
| Chaque mock FastAPI | 128 Mo | Une seule image partagée par tous les mocks |
| API et interface DataLift (à venir) | 256 Mo | Réservé |
| **Total des limites** | **environ 1,5 Go** | Le reste (environ 500 Mo) va au système et à Docker |

Autres règles :

- **Swap de 2 Go** sur le VPS, en sécurité contre un pic de mémoire.
- **Aucun port public** : tous les ports sont liés à `127.0.0.1`. On y accède par un tunnel SSH, jusqu'à ce qu'un reverse proxy avec HTTPS soit décidé.
- **Données persistantes** dans des volumes Docker nommés (`pgdata`, `odoodata`) : elles survivent aux redéploiements et se sauvegardent avec `pg_dump`.
- **Aucune installation manuelle** sur le serveur en dehors de Docker. Le déploiement se fait par `git pull` puis `docker compose up -d`.

**Montée en puissance**, dans cet ordre :

1. Mesurer avec `docker stats`. Si un service atteint sa limite, ajuster les limites entre les services.
2. Agrandir le serveur avec *Rescale* dans Hetzner, en cochant **« CPU and RAM only »** : quelques minutes avec un redémarrage, sans perte de données, et le retour en arrière reste possible (le disque n'est pas agrandi).
3. Avec Terraform, le type de serveur est une variable (`server_type`). Le changer revient à modifier une ligne.
4. Si la charge le demande au M2, sortir PostgreSQL sur un serveur ou un volume dédié. Les services se connectent par variables d'environnement, donc rien ne change dans le code.

## Conséquences

Positives :

- Un coût d'environ 11 €/mois.
- La consommation de chaque service est connue et bornée : un service qui déborde est redémarré seul sans faire tomber les autres.
- Le passage à une offre supérieure est rapide et réversible.

Négatives :

- Une marge faible : chaque nouveau service doit déclarer sa limite et être mesuré.
- Un seul vCPU : les traitements lourds (gros volumes, nombreux flux en parallèle) seront lents.
- PostgreSQL et Odoo partagent une instance : une panne de PostgreSQL arrête les deux.

À surveiller : la mémoire réelle par service (`docker stats`), l'usage du swap, l'espace disque.

À mettre en place : le swap et Docker sur le VPS, les variables `POSTGRES_PASSWORD` et `ODOO_DB_PASSWORD` dans `.env`, et le code Terraform du serveur.
