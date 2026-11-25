# infra

Un seul Docker Compose, `infra/docker-compose.yml`, pour les postes et le VPS Hetzner CPX12. Limite de mémoire par service : ADR-009.

## Lancer

Depuis la racine du dépôt, avec un `.env` copié depuis [.env.example](../.env.example) (`POSTGRES_PASSWORD` et `ODOO_DB_PASSWORD` obligatoires ; `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PORT` facultatifs) :

```bash
cp .env.example .env
make up      # PostgreSQL + mocks IFS et Progessi
make odoo    # Odoo Notes de frais (installe ou met à jour le module, puis démarre)
make down    # arrête sans supprimer les données
```

Pour supprimer aussi les données : `docker compose -f infra/docker-compose.yml --env-file .env down -v`.

Ports, liés à `127.0.0.1` : PostgreSQL `${POSTGRES_PORT:-5432}`, mock IFS 8001, mock Progessi 8002, Odoo 8069. Sur le VPS, par tunnel SSH : `ssh -L 8069:127.0.0.1:8069 <utilisateur>@<IP>`.

Mémoire par service : `docker stats --no-stream`.
