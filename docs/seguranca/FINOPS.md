# FinOps e Eficiência Operacional Offline

> **Estágio:** Especificação de custos e dimensionamento operacional baseada na arquitetura definida no `README.md` e na `ADR-003`. Medições reais de latência e consumo de VRAM serão registradas após a implementação do pipeline.

## 1. Modelo Econômico: Zero Custo Variável de API

Por decisão arquitetural ([ADR-003](../arquitetura/decisoes/adr-003-banco-unico-postgres-e-ollama-offline.md)), o **Auditor 12.002** não utiliza provedores comerciais de LLM em nuvem nem bancos vetoriais gerenciados:

| Componente | Modelo de custo | Observação operacional |
| --- | --- | --- |
| **Inferência LLM (`qwen3:8b` via Ollama)** | **R$ 0,00 / token** (execução local) | Custo fixo limitado à infraestrutura local (GPU/energia) já disponível; download único dos pesos antes do modo offline. |
| **Recuperação lexical (`bm25s`)** | **R$ 0,00** (processamento local em CPU/RAM) | Dispensa serviços dedicados de embeddings e bancos vetoriais separados. |
| **Persistência e auditoria (PostgreSQL 17)** | **R$ 0,00** (container local único) | Banco único consolida tabelas, `llm_cache` e views analíticas. |
| **Interface analítica (Streamlit offline)** | **R$ 0,00** (container local) | Operação local na porta `8501`. |

## 2. Economia de Computação pelo Design em Camadas

O maior ganho de eficiência computacional do Auditor 12.002 não vem de otimizações isoladas de GPU, mas de **não acionar o LLM quando não é necessário**:

1. **Filtragem determinística prévia (`R1`–`R4`):** quatro das seis regras são integralmente determinísticas e não consomem inferência LLM.
2. **Motor de aplicabilidade antes da detecção:** atos fora de escopo ou sob exceção (`NAO_APLICAVEL`) e atos com fonte divergente/ilegível (`NAO_AVALIAVEL`) encerram o fluxo antes de invocar o Ollama.
3. **Uso seletivo em `R5`:** o modelo local só entra em casos ambíguos de `R5` que não foram resolvidos pelas checagens determinísticas, além de `R6` nos atos aplicáveis.
4. **Ledger idempotente `llm_cache`:** cada chamada bem-sucedida fica registrada no PostgreSQL 17 pela chave composta (`modelo`, `digest`, `prompt`, `parâmetros`, `manifesto`, `commit Git`), permitindo que `make reproduce` regenere métricas e tabelas sem re-executar inferência repetida.

## 3. Requisitos de Hardware e Limites Operacionais

- **Ambiente recomendado para inferência completa (`D/A/B/C`):** GPU com **`>= 12 GB` de VRAM** para rodar `qwen3:8b` via Ollama com latência adequada, além de Docker e Docker Compose.
- **Execução no CI e máquinas sem GPU:** as suítes de testes unitários, casos difíceis, segurança e E2E (`make test` e `make test-sec`) são projetadas para rodar **sem GPU**, mantendo o custo de CI limitado a runners CPU padrão.
- **Métricas pendentes de aferição após implementação:** tempo médio por ato nas condições `D`, `A`, `B` e `C`, taxa de acerto em cache (`llm_cache` hit rate) e pico de memória por container.
