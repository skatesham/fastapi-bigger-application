APP_PYTHON ?= python3
COMPOSE ?= docker compose

.DEFAULT_GOAL := help

.PHONY: help install run test format lint typecheck check db-up db-down db-logs db-shell migration-new migration-up migration-down migration-current migration-history seed docker-up docker-down docker-reset docker-logs docker-ps docker-shell docker-rebuild

help: ## Lista os comandos disponíveis
	@awk 'BEGIN { FS = ":.*## "; printf "Uso: make <comando>\n\nComandos:\n" } /^[a-zA-Z0-9_-]+:.*## / { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Instala as dependências locais, incluindo ferramentas de desenvolvimento
	$(APP_PYTHON) -m pip install -e ".[dev]"

run: migration-up seed ## Aplica banco e inicia a API local com recarregamento
	@echo ""
	@echo "API iniciando em http://localhost:8000"
	@echo "Documentação interativa: http://localhost:8000/docs"
	@echo ""
	$(APP_PYTHON) -m uvicorn app.main:app --reload

test: ## Executa os testes
	$(APP_PYTHON) -m pytest

format: ## Formata o código com Black e isort
	$(APP_PYTHON) -m black app tests db
	$(APP_PYTHON) -m isort app tests db

lint: ## Executa o linter
	$(APP_PYTHON) -m flake8 app tests db

typecheck: ## Executa a verificação estática de tipos
	$(APP_PYTHON) -m mypy app db

check: lint typecheck test ## Executa análises e testes

db-up: ## Inicia somente o PostgreSQL
	$(COMPOSE) up -d --wait db

db-down: ## Para somente o PostgreSQL
	$(COMPOSE) stop db

db-logs: ## Exibe os logs do PostgreSQL
	$(COMPOSE) logs -f db

db-shell: ## Abre um psql no container PostgreSQL
	$(COMPOSE) exec db psql -U skatesham -d skatesham

migration-new: ## Cria migration; use MESSAGE="descricao"
	@test -n "$(MESSAGE)" || (echo 'Use: make migration-new MESSAGE="descricao"' >&2; exit 1)
	$(APP_PYTHON) -m alembic revision --autogenerate -m "$(MESSAGE)"

migration-up: ## Aplica todas as migrations pendentes
	$(APP_PYTHON) -m alembic upgrade head

migration-down: ## Reverte a última migration
	$(APP_PYTHON) -m alembic downgrade -1

migration-current: ## Exibe a revisão atual do banco
	$(APP_PYTHON) -m alembic current

migration-history: ## Exibe o histórico de migrations
	$(APP_PYTHON) -m alembic history

seed: ## Aplica os seeds pendentes uma única vez
	$(APP_PYTHON) -m db.seed

docker-up: ## Constrói e inicia todos os containers
	$(COMPOSE) up --build -d

docker-down: ## Para e remove os containers
	$(COMPOSE) down

docker-reset: ## Para containers e remove o volume do banco
	$(COMPOSE) down -v

docker-logs: ## Exibe os logs da API
	$(COMPOSE) logs -f api

docker-ps: ## Exibe o estado dos containers
	$(COMPOSE) ps

docker-shell: ## Abre um shell no container da API
	$(COMPOSE) exec api /bin/sh

docker-rebuild: ## Reconstrói e reinicia a API
	$(COMPOSE) up --build -d api
