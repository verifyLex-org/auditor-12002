.PHONY: help setup hooks lint typecheck governance test test-e2e test-sec verify-manifest check up reproduce docs docs-build clean

help:
	@echo "Comandos disponiveis (Auditor 12.002):"
	@echo "  make setup            - Instala Python 3.12, sincroniza dependencias e hooks"
	@echo "  make hooks            - Instala os hooks pre-commit no clone local"
	@echo "  make lint             - Executa ruff check e ruff format --check"
	@echo "  make typecheck        - Executa verificacao estatica de tipos com mypy"
	@echo "  make governance       - Valida artefatos de governanca e workflows SHA-pinados"
	@echo "  make test             - Roda suite de testes sem LLM e sem E2E"
	@echo "  make test-e2e         - Compila o portal e roda os testes E2E (Playwright)"
	@echo "  make check            - Executa lint, typecheck, governance, test e docs-build"
	@echo "  make test-sec         - Roda bateria de seguranca (tests/security)"
	@echo "  make verify-manifest  - Valida manifesto do corpus"
	@echo "  make up               - Sobe containers com docker compose"
	@echo "  make reproduce        - Reproduz experimentos da tag gold-v1"
	@echo "  make docs             - Inicia servidor local MkDocs em http://127.0.0.1:8001"
	@echo "  make docs-build       - Compila o site estatico em modo estrito (--strict)"
	@echo "  make clean            - Remove artefatos temporarios de build (site/ e .cache/)"

setup:
	uv python install 3.12
	uv sync --locked --dev
	uv run --no-sync pre-commit install

hooks:
	uv run --no-sync pre-commit install --install-hooks

lint:
	uv run --no-sync ruff check .
	uv run --no-sync ruff format --check .

typecheck:
	uv run --no-sync mypy .

governance:
	uv run --no-sync python -m scripts.check_governance

test:
	uv run --no-sync pytest -m "not llm and not e2e"

test-e2e: docs-build
	uv run --no-sync playwright install --only-shell chromium
	uv run --no-sync pytest tests/e2e -m e2e

check: lint typecheck governance test docs-build

test-sec:
	uv run --no-sync pytest tests/security -m "not llm"

verify-manifest:
	uv run --no-sync python -m verify.manifest

up:
	docker compose up -d --pull never --no-build

reproduce: verify-manifest
	docker compose run --rm --pull never app python -m app.cli reproduce --gold-tag gold-v1

docs:
	uv run --frozen mkdocs serve -a 127.0.0.1:8001

docs-build:
	uv run --frozen mkdocs build --strict

clean:
	rm -rf site .cache .ruff_cache
