# Como Rodar

Esta página separa claramente o que **já está ativo no repositório hoje** (portal de documentação e verificação estrita) dos comandos da **stack completa de auditoria** descritos no `README.md` para os próximos marcos de código.

## 1. Ambiente de Documentação (Ativo Agora)

### Pré-requisitos

- Python `3.12+`
- [Astral `uv`](https://docs.astral.sh/uv/)
- Git

### Comandos disponíveis

=== "Setup e Servidor Local"

    ```bash
    uv sync --locked
    uv run --frozen mkdocs serve -a 127.0.0.1:8001
    ```

    Acesse `http://127.0.0.1:8001` no navegador. No primeiro build com o plugin `privacy` ativo, é necessário acesso à internet para baixar e embutir as fontes localmente em `site/`.

=== "Qualidade, Tipagem, Governança e Build"

    ```bash
    uv run --frozen ruff check .
    uv run --frozen ruff format --check .
    uv run --frozen mypy .
    uv run --frozen pytest -m "not llm"
    uv run --frozen python -m scripts.check_governance
    uv run --frozen mkdocs build --strict
    ```

=== "Pre-commit"

    ```bash
    uv run --frozen pre-commit install --install-hooks
    uv run --frozen pre-commit run --all-files
    ```

=== "Atalhos via Makefile"

    ```bash
    make setup       # uv python install 3.12 + uv sync --locked + hooks
    make lint        # ruff check . e ruff format --check .
    make typecheck   # mypy .
    make governance  # scripts.check_governance
    make test        # pytest -m "not llm"
    make check       # executa toda a esteira local
    make docs        # mkdocs serve em 127.0.0.1:8001
    make docs-build  # mkdocs build --strict
    make clean       # remove site/, .cache/ e .ruff_cache/
    ```

---

## 2. Stack Completa de Auditoria (Planejada no `README.md`)

> **Estágio:** Os comandos abaixo são a arquitetura-alvo e **ainda não funcionam de ponta a ponta**. O arquivo `compose.yml` e o `Dockerfile` existem, mas estão **vazios**; `data/` contém apenas placeholders vazios; os módulos Python são stubs.

### Pré-requisitos previstos

- Docker e Docker Compose
- Python 3.12+ e `uv`
- GPU com `>= 12 GB` de VRAM recomendada para inferência local via Ollama (`qwen3:8b`)

### Fluxo offline previsto

```bash
git clone https://github.com/verifyLex-org/auditor-12002.git
cd auditor-12002

# Passos previstos após implementação da stack:
make verify-manifest
docker compose up -d
docker compose exec ollama ollama pull qwen3:8b
```
