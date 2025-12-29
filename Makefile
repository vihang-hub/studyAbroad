.PHONY: help install dev build test clean docker-up docker-down

help:
	@echo "Study Abroad Development Commands"
	@echo "=================================="
	@echo "make install       - Install all dependencies (frontend + backend)"
	@echo "make dev           - Start development servers (frontend + backend)"
	@echo "make build         - Build production bundles"
	@echo "make test          - Run all tests"
	@echo "make test-coverage - Run tests with coverage"
	@echo "make test-mutation - Run mutation testing"
	@echo "make lint          - Run linters"
	@echo "make docker-up     - Start all services with Docker Compose"
	@echo "make docker-down   - Stop all Docker services"
	@echo "make clean         - Clean build artifacts and caches"

install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing backend dependencies..."
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

dev:
	@echo "Starting development servers..."
	@echo "Frontend will run on http://localhost:3000"
	@echo "Backend will run on http://localhost:8000"
	@make -j2 dev-frontend dev-backend

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

build:
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "Backend doesn't require build step (Python)"

test:
	@echo "Running frontend tests..."
	cd frontend && npm run test
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest

test-coverage:
	@echo "Running frontend tests with coverage..."
	cd frontend && npm run test:coverage
	@echo "Running backend tests with coverage..."
	cd backend && . venv/bin/activate && pytest --cov=app --cov-report=html --cov-report=term

test-mutation:
	@echo "Running mutation testing (frontend only)..."
	cd frontend && npm run test:mutation

lint:
	@echo "Linting frontend..."
	cd frontend && npm run lint
	@echo "Linting backend..."
	cd backend && . venv/bin/activate && ruff check . && black --check .

docker-up:
	docker-compose up -d
	@echo "Services started:"
	@echo "  - PostgreSQL: localhost:54322"
	@echo "  - Supabase Studio: http://localhost:54323"
	@echo "  - Backend API: http://localhost:8000"

docker-down:
	docker-compose down

clean:
	@echo "Cleaning frontend..."
	cd frontend && rm -rf .next node_modules coverage .vitest
	@echo "Cleaning backend..."
	cd backend && rm -rf venv __pycache__ .pytest_cache htmlcov .coverage
	@echo "Cleaning Docker volumes..."
	docker-compose down -v
