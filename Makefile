# ==============================================================================
# Auditor 12.002 - Automação Inicial de Documentação e Qualidade
# ==============================================================================

UV := $(shell command -v uv 2> /dev/null)
MKDOCS := $(if $(UV),uv run --frozen mkdocs,mkdocs)
RUFF := $(if $(UV),uv run --frozen ruff,ruff)
PRE_COMMIT := $(if $(UV),uv run --frozen pre-commit,pre-commit)

.PHONY: help setup hooks lint docs docs-build clean

help:
	@echo "Comandos disponiveis no setup inicial (Auditor 12.002):"
	@echo "  make setup       - Sincroniza ambiente virtual e lockfile via uv"
	@echo "  make hooks       - Instala os hooks pre-commit no clone local"
	@echo "  make lint        - Executa ruff check e ruff format --check em docs_hooks/"
	@echo "  make docs        - Inicia servidor local MkDocs em http://127.0.0.1:8001"
	@echo "  make docs-build  - Compila o site estatico em modo estrito (--strict)"
	@echo "  make clean       - Remove artefatos temporarios de build (site/ e .cache/)"

setup:
	uv sync --locked

hooks:
	$(PRE_COMMIT) install --install-hooks

lint:
	$(RUFF) check docs_hooks/
	$(RUFF) format --check docs_hooks/

docs:
	$(MKDOCS) serve -a 127.0.0.1:8001

docs-build:
	$(MKDOCS) build --strict

clean:
	rm -rf site .cache .ruff_cache
