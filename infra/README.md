# infra

Docker Compose (postes locaux et VPS Hetzner CPX12), Terraform, workflows GitHub Actions. Budget mémoire par service : ADR-009.

## PostgreSQL local

Depuis la racine du dépôt, créer le fichier `.env` à partir de [.env.example](../.env.example), puis lancer PostgreSQL en une commande :

```bash
cp .env.example .env
docker compose up -d
```

Les identifiants et le port sont lus depuis `.env` : `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`.

Le service PostgreSQL est exposé localement sur `localhost:${POSTGRES_PORT}` et conserve ses données dans un volume Docker nommé `postgres_data`.

Pour arrêter le conteneur sans supprimer les données :

```bash
docker compose down
```

Pour supprimer aussi le volume de stockage local :

```bash
docker compose down -v
```

## Stack complète (VPS)

Dans `infra/`, avec `POSTGRES_PASSWORD` et `ODOO_DB_PASSWORD` définis dans `infra/.env` (jamais commité) :

```bash
docker compose up -d --build postgres mock-ifs mock-progessi
docker compose run --rm odoo odoo -d odoo -i hr_expense --stop-after-init   # première fois seulement
docker compose up -d odoo
docker stats --no-stream   # vérifier la mémoire de chaque service
```

Ports (liés à `127.0.0.1`) : PostgreSQL 5432, mock IFS 8001, mock Progessi 8002, Odoo 8069. Sur le VPS : `ssh -L 8069:127.0.0.1:8069 root@<IP>`.
