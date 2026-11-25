.PHONY: setup test lint format mocks up down odoo

setup: ## Installe les dépendances (prérequis : uv)
	@command -v uv >/dev/null || { echo "uv manquant : curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	uv sync --locked

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

mocks: ## IFS sur :8001, Progessi sur :8002 (Ctrl+C pour tout arrêter)
	uv run uvicorn mocks.ifs.app:app --port 8001 & \
	uv run uvicorn mocks.progessi.app:app --port 8002 & \
	wait

COMPOSE := docker compose -f infra/docker-compose.yml --env-file .env

up: ## PostgreSQL + mocks dans Docker (variables lues dans .env)
	$(COMPOSE) up -d --build postgres mock-ifs mock-progessi

odoo: ## Odoo Notes de frais : installe le module au premier lancement, puis démarre
	$(COMPOSE) run --rm odoo odoo -d odoo -i hr_expense --stop-after-init
	$(COMPOSE) up -d odoo

down: ## Arrête la stack sans supprimer les données
	$(COMPOSE) down
