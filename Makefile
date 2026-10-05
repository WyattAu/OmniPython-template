# Thin wrapper over scripts/ — the same verbs in every Omni template.
.PHONY: build test lint fmt fmt-check typecheck docs contract ci clean

build:
	uv build --package omni-core

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

fmt:
	./scripts/fmt.sh

fmt-check:
	uv run ruff format --check .
	uv run ruff check .

typecheck:
	./scripts/typecheck.sh

docs:
	./scripts/docs.sh

contract:
	./scripts/check-contract.sh

## What CI gates before merge (mirror of .github/workflows/ci.yml):
ci: contract fmt-check lint typecheck test

clean:
	rm -rf dist .venv .pytest_cache .ruff_cache .coverage
