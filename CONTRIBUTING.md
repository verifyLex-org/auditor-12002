# Como contribuir — Auditor 12.002

Guia essencial de colaboração no repositório `verifyLex-org/auditor-12002`. A versão navegável também está publicada na seção de operação do portal de documentação.

## Regras inegociáveis

1. **Fronteira legal (Art. 76 do Decreto nº 12.002/2024):** nunca redija regras, mensagens de interface ou textos de documentação afirmando que um ato é "ilegal", "nulo", "inválido" ou "inconstitucional". O sistema emite estritamente **achados de técnica legislativa** e **sugestões de adequação** (art. 70, III).
2. **Imutabilidade após congelamento:** após o congelamento de `data/manifesto.csv`, `data/MANIFEST.sha256` e `data/gold/gold-v1.csv`, nenhum Pull Request deve alterar o corpus de teste ou o gabarito para "melhorar" métricas.
3. **Execução offline e quarentena:** textos de atos normativos são dados não confiáveis (sujeitos a *prompt injection* indireto). Não remova `spotlighting/datamarking`, não habilite acesso à internet no serviço Ollama (`internal: true`) e não adicione ferramentas ao LLM.
4. **Honestidade empírica:** nunca invente números, resultados de benchmarks, métricas de precisão/*recall* ou dispositivos legais inexistentes. Enquanto uma etapa não for implementada ou executada, marque seu status explicitamente.
5. **Segredos nunca entram no Git:** use variáveis de ambiente fora do controle de versão (`.env` está no `.gitignore`).

## Commits

Adote **Conventional Commits** em português com descrição curta no imperativo:

```text
tipo(escopo): descrição curta no imperativo
```

- **Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`.
- **Escopos sugeridos:** `docs`, `domain`, `parser`, `rules`, `retrieval`, `llm`, `pipeline`, `verify`, `eval`, `sql`, `app`, `infra`, `data`.

Exemplos:

```text
docs(regras): detalha exceções legais de R4 e R6
docs(adr): registra ADR-002 sobre dupla fonte concordante
ci(docs): configura build estrito do MkDocs no GitHub Actions
```

## Fluxo de Pull Requests e Qualidade

Antes de abrir um PR alterando documentação ou scripts de apoio:

```bash
uv sync --locked
uv run --frozen ruff check docs_hooks/
uv run --frozen ruff format --check docs_hooks/
uv run --frozen mkdocs build --strict
```

Se tiver o `pre-commit` instalado localmente:

```bash
uv run --frozen pre-commit run --all-files
```

## Convenções de Documentação

- Redação em **português do Brasil**, objetiva e sem jargão implícito.
- Cada página Markdown em `docs/` deve ter **exatamente um título `<h1>`** (`# Título`), verificado automaticamente por `docs_hooks/check_site.py`.
- Nunca adicione `<script src="http...">` externos nem links `javascript:` nas páginas; todas as fontes e ativos devem ser empacotados em build pelo plugin `privacy`.
- Ao exemplificar os 4 estados do sistema, utilize as *admonitions* dedicadas: `conforme`, `achado`, `nao-aplicavel` e `nao-avaliavel`.
- Novas decisões arquiteturais devem copiar o modelo em `docs/_templates/adr.md` e ser indexadas em `docs/arquitetura/decisoes/index.md`.
