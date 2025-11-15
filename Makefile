.PHONY: help install dev-up dev-down migrate upgrade run-worker run-beat test

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev-up       - Start development services (PostgreSQL, Redis)"
	@echo "  make dev-down     - Stop development services"
	@echo "  make migrate      - Create new database migration"
	@echo "  make upgrade      - Apply database migrations"
	@echo "  make run-server   - Run FastAPI development server"
	@echo "  make run-worker   - Run Celery worker"
	@echo "  make run-beat     - Run Celery beat scheduler"
	@echo "  make test         - Run tests"

install:
	pip install -r requirements.txt

dev-up:
	docker-compose up -d

dev-down:
	docker-compose down

migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

run-server:
	uvicorn app.main:app --reload --port 8000

run-worker:
	celery -A app.core.celery_app worker --loglevel=info

run-beat:
	celery -A app.core.celery_app beat --loglevel=info

test:
	pytest tests/ -v --cov=app
