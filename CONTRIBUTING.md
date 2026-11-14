# Como contribuir — Auditor 12.002

Guia essencial de colaboração no repositório `verifyLex-org/auditor-12002`. A versão navegável também está publicada na seção de operação do portal de documentação.

## Regras inegociáveis

1. **Fronteira legal (Art. 76 do Decreto nº 12.002/2024):** nunca redija regras, mensagens de interface ou textos de documentação afirmando que um ato é "ilegal", "nulo", "inválido" ou "inconstitucional". O sistema emite estritamente **achados de técnica legislativa** e **sugestões de adequação** (art. 70, III).
2. **Imutabilidade após congelamento:** após o congelamento de `data/manifesto.csv`, `data/MANIFEST.sha256` e `data/gold/gold-v1.csv`, nenhum Pull Request deve alterar o corpus de teste ou o gabarito para "melhorar" métricas.
3. **Execução offline e quarentena:** textos de atos normativos são dados não confiáveis (sujeitos a *prompt injection* indireto). Não remova `spotlighting/datamarking`, não habilite acesso à internet no serviço Ollama (`internal: true`) e não adicione ferramentas ao LLM.
4. **Honestidade empírica:** nunca invente números, resultados de benchmarks, métricas de precisão/*recall* ou dispositivos legais inexistentes. Enquanto uma etapa não for implementada ou executada, marque seu status explicitamente.
5. **Segredos nunca entram no Git:** use variáveis de ambiente fora do controle de versão (`.env` está no `.gitignore`).

## Branches, Commits e Pull Requests

- **Padrão de branches:** `<tipo>/<issue>-<tema>` usando um dos prefixos `feat`, `fix`, `docs`, `sec`, `ci`, `chore`, `refactor`, `test` ou `hotfix` (ex.: `feat/12-regra-r1`, `sec/18-injection-guard`).
- **Commits e título de PR:** adote **Conventional Commits** em português com descrição curta no imperativo (`tipo(escopo): descrição curta`):
  - **Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`, `sec`.
  - **Escopos sugeridos:** `docs`, `domain`, `parser`, `rules`, `retrieval`, `llm`, `pipeline`, `verify`, `eval`, `sql`, `app`, `infra`, `data`, `deps`.

Exemplos:

```text
docs(regras): detalha exceções legais de R4 e R6
docs(adr): registra ADR-002 sobre dupla fonte concordante
ci(docs): configura build estrito do MkDocs no GitHub Actions
```

- **Revisão e propriedade:** o arquivo `.github/CODEOWNERS` define revisores obrigatórios por área sensível (`PREREGISTRO.md`, `data/`, `verify/`, `rules/`, `llm/`, `sql/`, `.github/`). O envio de código para `main` deve ocorrer via Pull Request usando `.github/PULL_REQUEST_TEMPLATE.md` e templates estruturados em `.github/ISSUE_TEMPLATE/`.
- **Segurança:** vulnerabilidades não devem ser abertas como issue pública; siga as instruções de divulgação coordenada em `SECURITY.md`.

## Fluxo de Pull Requests e Qualidade

Antes de abrir um PR, execute a bateria completa verificada pelo CI (`.github/workflows/ci.yml` e `.github/workflows/docs.yml`):

```bash
uv sync --locked
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy .
uv run --frozen pytest -m "not llm"
uv run --frozen python -m scripts.check_governance
uv run --frozen mkdocs build --strict
```

Ou via `pre-commit` (inclui `gitleaks`, `check-yaml`, `check-toml`, `detect-private-key` e `ruff`):

```bash
uv run --frozen pre-commit run --all-files
```

## Convenções de Documentação

- Redação em **português do Brasil**, objetiva e sem jargão implícito.
- Cada página Markdown em `docs/` deve ter **exatamente um título `<h1>`** (`# Título`), verificado automaticamente por `docs_hooks/check_site.py`.
- Nunca adicione `<script src="http...">` externos nem links `javascript:` nas páginas; todas as fontes e ativos devem ser empacotados em build pelo plugin `privacy`.
- Ao exemplificar os 4 estados do sistema, utilize as *admonitions* dedicadas: `conforme`, `achado`, `nao-aplicavel` e `nao-avaliavel`.
- Novas decisões arquiteturais devem copiar o modelo em `docs/_templates/adr.md` e ser indexadas em `docs/arquitetura/decisoes/index.md`.
