.DEFAULT_GOAL := help
COMPOSE ?= docker compose
.PHONY: help init build up down clean logs ps lint

help: ## Affiche cette aide
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Crée .env à partir de .env.example
	@test -f .env || cp .env.example .env

build: init ## Construit les images
	@$(COMPOSE) build

up: init ## Lance toute la plateforme
	@$(COMPOSE) up -d --build

down: ## Arrête la plateforme
	@$(COMPOSE) down

clean: ## Arrête et supprime les volumes
	@$(COMPOSE) down -v

logs: ## Journaux : make logs SERVICE=kafka
	@$(COMPOSE) logs -f --tail=100 $(SERVICE)

ps: ## État des services
	@$(COMPOSE) ps

lint: ## Vérifie le style Python
	@ruff check .
# TODO : chaque propriétaire ajoute ses raccourcis (ex. up-ingestion, spark-job, trigger-dag)
