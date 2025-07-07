# Security: Use .PHONY to prevent conflicts with files
.PHONY: install test lint format check-types security-check docker-build docker-run

install:
	@echo "Installing dependencies..."
	poetry install --with dev --sync

test:
	@echo "Running tests..."
	poetry run pytest -v --cov=src --cov-fail-under=90

lint:
	@echo "Linting code..."
	poetry run ruff check .

format:
	@echo "Formatting code..."
	poetry run black .
	poetry run ruff --fix .

check-types:
	@echo "Type checking..."
	poetry run mypy src

security-check:
	@echo "Security scanning..."
	poetry run bandit -r src --severity-level high --confidence-level high
	poetry run safety check --full-report

docker-build:
	@echo "Building Docker image..."
	docker build --pull --no-cache -t package_name:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -it --rm -p 8000:8000 --name package_name package_name:latest

ci: install lint check-types test security-check
