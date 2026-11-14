## Resumo

<!-- Descreva objetivamente o que muda, por que muda e como a alteração foi validada. -->

- **Issue relacionada:** Closes #

## Tipo de Mudança

- [ ] `feat` — Nova funcionalidade
- [ ] `fix` — Correção de defeito
- [ ] `docs` — Documentação / ADR / cartões
- [ ] `sec` — Segurança / quarentena / hard cases adversários
- [ ] `refactor` — Refatoração sem alteração de comportamento externo
- [ ] `test` — Adição ou ajuste de testes
- [ ] `ci` / `chore` — Esteira, governança, dependências ou automação

## Checklist de Governança e Invariantes (Auditor 12.002)

- [ ] Título do PR em **Conventional Commits** (`tipo(escopo): descrição curta`) e branch no padrão (`feat|fix|docs|sec|ci|chore|refactor|test/<issue>-<tema>`).
- [ ] **Fronteira jurídica (Art. 76):** nenhum código, prompt, interface ou documentação afirma ilegalidade, nulidade, invalidade ou inconstitucionalidade de ato normativo.
- [ ] **Imutabilidade experimental:** não altera `PREREGISTRO.md`, `data/manifesto.csv`, `data/MANIFEST.sha256` ou `data/gold/gold-v1.csv` após congelamento (ou inclui justificativa formal e registro de versão).
- [ ] **Isolamento offline e segurança:** preserva *spotlighting/datamarking*, rede `internal: true` sem ferramentas no Ollama, ausência de `<script src>` externos e zero segredos/PII no diff.
- [ ] **Honestidade empírica:** nenhuma métrica, cobertura ou evidência foi estimada ou inventada; os comandos abaixo foram executados após a última edição.
- [ ] **ADR / Documentação:** decisão arquitetural relevante registrada em `docs/arquitetura/decisoes/` (a partir de `docs/_templates/adr.md`) e documentação sincronizada.

## Validação Local Executada

```bash
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy .
uv run --frozen pytest -m "not llm"
uv run --frozen python -m scripts.check_governance
uv run --frozen mkdocs build --strict  # quando houver alteração em docs/ ou mkdocs.yml
```

- **Resultados observados:** <!-- informe PASS/FAIL/N/A para cada comando executado -->

## Riscos e Rollback

- **Impacto esperado:**
- **Como reverter com segurança:** `git revert <sha>` (sem alterações destrutivas em schema/dados congelados).
