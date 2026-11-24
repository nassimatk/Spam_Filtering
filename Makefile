.DEFAULT_GOAL := help
COMPOSE ?= docker compose
.PHONY: help init build up down clean logs ps lint up-lake lake-test lake-demo

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

# ---- E2 : Lakehouse -------------------------------------------------
SPARK_SUBMIT_E2 = /opt/spark/bin/spark-submit --master spark://spark-master:7077 \
  --conf spark.driver.host=spark-client --conf spark.driver.bindAddress=0.0.0.0 \
  --conf spark.cores.max=1 --conf spark.executor.memory=512m --conf spark.driver.memory=512m

up-lake: init ## E2 : MinIO + buckets (console : http://localhost:9001)
	@$(COMPOSE) up -d minio minio-init

lake-test: ## E2 : test Spark <-> MinIO <-> Hudi (nécessite le service spark-client d'E3)
	@$(COMPOSE) exec spark-client $(SPARK_SUBMIT_E2) /opt/app/lakehouse/test_hudi_minio.py

lake-demo: ## E2 : démonstration Hudi (upsert, time travel, incrémental)
	@$(COMPOSE) exec spark-client $(SPARK_SUBMIT_E2) /opt/app/lakehouse/demo_hudi.py

# TODO : E1, E3 et E4 ajoutent leurs raccourcis ci-dessous
