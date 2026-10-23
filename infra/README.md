# infra

Docker Compose (postes locaux et VPS Hetzner), Terraform, workflows GitHub Actions. Choix d'hébergement : voir `docs/decisions/`.


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

