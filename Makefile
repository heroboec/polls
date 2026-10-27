COMPOSE = docker compose
APP = web

.PHONY: up down build shell bash

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

down-v:
	$(COMPOSE) down -v

build:
	$(COMPOSE) build

shell:
	$(COMPOSE) exec $(APP) python manage.py shell

bash:
	$(COMPOSE) exec $(APP) bash
