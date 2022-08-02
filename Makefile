SHELL := /bin/bash
.ONESHELL:


PYTHON = `command -v python3.8 || command -v python3.9`
basename := $(shell basename ${PYTHON})

.PHONY: install
install:
	if ! [ -x "${PYTHON}" ]; then echo "You need Python3.8 or Python3.9 installed"; exit 1; fi
	test -d venv || ${PYTHON} -m venv venv
	source venv/bin/activate
	pip install --upgrade pip setuptools wheel build
	pip install -e .[dev]

.PHONY: test
test:
	source venv/bin/activate
	pytest

.PHONY: lint
test:
	source venv/bin/activate
	flake8 src/
	isort src/
	black src/

.PHONY: mypy
mypy:	
	source venv/bin/activate
	mypy src/

.PHONY: clean
clean: ## Resets the development workspace
	@echo 'cleaning workspace'
	rm -rf .coverage
	rm -rf .eggs/
	rm -rf airflow/logs/*
	rm -rf venv/ .tox/ .mypy_cache/ .pytest_cache/ build/ dist/ target/
	find . -depth -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -depth -type d -name '__pycache__' -delete
	echo 'done'


# Docker commands

.PHONY: compose-prep compose-up docker-reset compose-down

compose-prep:
	mkdir -p ./docker/postgres/postgres-db-volume ./docker/postgres/postgres-dw-volume

compose-up:
	docker-compose --env-file ./airflow/.env -f docker-compose.yml up -d --build --force-recreate

docker-reset:
	docker kill $(docker ps -aq)
	docker system prune --all --volumes -f

compose-down:
	docker-compose --env-file ./airflow/.env -f docker-compose.yml down --remove-orphans
	sudo rm -rf docker/postgres/postgres-db-volume
	sudo rm -rf docker/postgres/postgres-dw-volume



