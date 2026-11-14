# ADR-003 — Banco Único PostgreSQL 17 e Inferência Local Offline via Ollama

| Campo | Valor |
| --- | --- |
| **Status** | Proposto (Design inicial) |
| **Data** | 2026-11-13 |
| **Autores** | Equipe verifyLex-org |
| **Regra / Invariante afetada** | Arquitetura de persistência, Offline, Determinismo, Segurança (`llm/`) |

## 1. Contexto

Sistemas de auditoria baseados em LLM frequentemente combinam bancos vetoriais separados, arquivos JSON em disco, caches ad-hoc e chamadas a APIs externas em nuvem. Essa dispersão introduz três problemas incompatíveis com o Auditor 12.002:

1. **Risco de exfiltração e dependência externa:** chamadas a APIs externas impedem garantia de execução offline e ampliam a superfície de risco em cenários de *prompt injection* indireto.
2. **Divergência numérica:** métricas calculadas em scripts Python desconectados do armazenamento transacional tendem a divergir entre execuções e relatórios.
3. **Não determinismo e custo variável:** re-executar inferências sem ledger indexado torna caro e instável reproduzir tabelas experimentais.

## 2. Opções Consideradas

### Opção 1: Stack distribuída (API externa + banco vetorial separado + arquivos JSON locais)

- Usar API proprietária para `R5`/`R6`, vector store dedicado para busca e arquivos JSON para resultados.
- **Vantagens:** menor necessidade de GPU local.
- **Desvantagens:** quebra o requisito de execução 100% offline, incorre em custo variável por token, depende de terceiros para reprodutibilidade futura e fragmenta o estado entre múltiplos armazenamentos.

### Opção 2: Banco único PostgreSQL 17 + `bm25s` em memória/processo + Ollama offline (`qwen3:8b`) (Escolhida)

- Consolidar estado, resultados, views analíticas e `llm_cache` exclusivamente no **PostgreSQL 17**, utilizar recuperação lexical exata com `bm25s` (sem vector store separado) e rodar `qwen3:8b` localmente via Ollama em rede Docker `internal: true`.
- **Vantagens:** operação 100% offline após o pull inicial dos pesos; isolamento total de rede para o LLM; fechamento matemático garantido por views SQL; reprodutibilidade determinística via `llm_cache`.
- **Desvantagens:** exige hardware local compatível (recomendado >= 12 GB de VRAM para execução fluida de `qwen3:8b`) e disciplina na geração da chave de cache (`modelo`, `digest`, `prompt`, `parâmetros`, `manifesto`, `commit Git`).

## 3. Decisão Adotada

Adota-se:

1. **PostgreSQL 17 como banco único** para dados operacionais, resultados das condições `D/A/B/C`, ledger idempotente `llm_cache` e views analíticas de fechamento numérico.
2. **Ollama local com `qwen3:8b`** executando em rede Docker marcada com `internal: true` (sem saída para a internet), sem ferramentas habilitadas, com JSON Schema estrito, `temperature = 0` e `seed = 42`.
3. **`bm25s` (variante Lucene, `k1=1.2, b=0.75`)** para recuperação lexical leve e reprodutível, dispensando banco vetorial adicional.

## 4. Consequências e Trade-offs

- **Positivas:** zero custo variável em nuvem, arquitetura enxuta de 3 serviços no `compose.yml` (PostgreSQL 17, Ollama e Streamlit), reprodução exata via `make reproduce` e eliminação de divergência entre views SQL e relatórios.
- **Negativas e riscos:** suítes completas sem cache exigem GPU local recomendada ou tempo maior em CPU; testes automatizados em CI não podem depender de GPU.
- **Mitigação:** o CI executará suítes unitárias, de casos difíceis, segurança (*prompt injection*) e E2E sem GPU (com dublês determinísticos / ledger), enquanto o `llm_cache` elimina re-chamadas redundantes na reprodução experimental.

## 5. Verificação e Auditoria

- A configuração de rede `internal: true` no serviço Ollama será auditável diretamente no `compose.yml` quando implementado.
- A suíte `tests/security` testará 12 cenários de *prompt injection* indireto contra o pipeline em quarentena.
- As views SQL em `sql/` serão a única fonte de contagem consumida pelo `Verificador FINAL` e pelo dashboard Streamlit.
