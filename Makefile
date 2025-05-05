APP_CONTAINER_NAME = app
DB_CONTAINER_NAME = db
RUN_APP = docker-compose exec $(APP_CONTAINER_NAME)
RUN_UV =  $(RUN_APP) uv run

prepare:
	docker-compose up -d --build

up:
	docker-compose up -d

build:
	docker-compose build

down:
	docker-compose down

format:
	$(RUN_UV) ruff format

test:
	$(RUN_UV) pytest

app:
	docker exec -it $(APP_CONTAINER_NAME) bash

db:
	docker exec -it $(DB_CONTAINER_NAME) bash

makemigrations:
	$(RUN_UV) alembic revision --autogenerate

migrate:
	$(RUN_UV) alembic upgrade head
