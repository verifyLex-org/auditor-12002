# Como Contribuir

As regras de colaboração deste repositório protegem três pilares do **Auditor 12.002**: a **fronteira jurídica do Art. 76**, a **imutabilidade do conjunto de teste congelado** e a **reprodutibilidade offline**.

## Regras Inegociáveis

1. **Fronteira legal (Art. 76):** nunca redija código, prompts, mensagens ou documentação atribuindo invalidade, ilegalidade ou inconstitucionalidade a um ato normativo. Emite-se exclusivamente achado de técnica legislativa e sugestão de adequação (art. 70, III). Veja [Fronteira Jurídica](../dominio/fronteira-art76.md).
2. **Congelamento do corpus e do gabarito:** após o congelamento de `data/manifesto.csv`, `data/MANIFEST.sha256` e `data/gold/gold-v1.csv`, alterações nesses arquivos para melhorar métricas são proibidas e devem ser bloqueadas pelo CI.
3. **Preservação da quarentena:** mantenha os textos normativos como dados não confiáveis (somente leitura), preserve o *spotlighting/datamarking*, mantenha o Ollama em rede `internal: true` e não conceda ferramentas ao LLM.
4. **Honestidade técnica:** nunca invente números de avaliação, métricas ou resultados não executados. Utilize sempre o estado explícito quando algo estiver pendente de implementação ou rodada.

## Padrão de Commits e Pull Requests

- Utilize **Conventional Commits** em português (`tipo(escopo): descrição curta no imperativo`):
  - Exemplos: `docs(adr): adiciona ADR-003 sobre banco único`, `feat(rules): implementa checker R1@1.0`.
- Antes de abrir um Pull Request, valide localmente os checks ativos no repositório (ver [Como Rodar](como-rodar.md)):
  - `uv run --frozen ruff check docs_hooks/`
  - `uv run --frozen ruff format --check docs_hooks/`
  - `uv run --frozen mkdocs build --strict`

## Padrões de Escrita na Documentação

- Mantenha exatamente um `<h1>` por página em `docs/` (validado automaticamente por `docs_hooks/check_site.py`).
- Não introduza `<script src>` externos nem links `javascript:`.
- Utilize as *admonitions* `conforme`, `achado`, `nao-aplicavel` e `nao-avaliavel` ao exemplificar os estados da máquina de decisão.
- Para registrar novas decisões arquiteturais, siga o processo descrito em [Decisões Arquiteturais (ADRs)](../arquitetura/decisoes/index.md) usando `docs/_templates/adr.md`.
