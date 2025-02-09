APP_CONTAINER_NAME = app
DB_CONTAINER_NAME = db
RUN_APP = docker-compose exec $(APP_CONTAINER_NAME)
RUN_POETRY =  $(RUN_APP) poetry run

prepare:
	docker-compose up -d --build

up:
	docker-compose up -d

build:
	docker-compose build

down:
	docker-compose down

update:
	$(RUN_APP) poetry update

format:
	$(RUN_POETRY) ruff format

test:
	$(RUN_POETRY) pytest

app:
	docker exec -it $(APP_CONTAINER_NAME) bash

db:
	docker exec -it $(DB_CONTAINER_NAME) bash

makemigrations:
	$(RUN_POETRY) alembic revision --autogenerate 

migrate:
	$(RUN_POETRY) alembic upgrade head
