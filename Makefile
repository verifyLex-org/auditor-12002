.PHONY: setup lint test test-sec verify-manifest up reproduce

setup:
	uv python install 3.12
	uv sync --locked --dev
	uv run --no-sync pre-commit install

lint:
	uv run --no-sync ruff check .
	uv run --no-sync ruff format --check .

test:
	uv run --no-sync pytest -m "not llm"

test-sec:
	uv run --no-sync pytest tests/security -m "not llm"

verify-manifest:
	uv run --no-sync python -m verify.manifest

up:
	docker compose up -d --pull never --no-build

reproduce: verify-manifest
	docker compose run --rm --pull never app python -m app.cli reproduce --gold-tag gold-v1