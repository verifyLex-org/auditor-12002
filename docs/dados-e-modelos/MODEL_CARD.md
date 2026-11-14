# Model Card — Componente LLM Delimitado (`qwen3:8b`)

!!! info "Estágio neste repositório"
    Especificação do uso delimitado de LLM conforme `README.md` e `ADR-003`. O módulo `llm/` e os registros no `llm_cache` aguardam implementação.

## 1. Identificação e Papel no Sistema

- **Modelo local planejado:** `qwen3:8b` executado localmente via **Ollama**.
- **Papel estrito na arquitetura:** o LLM **não** decide legalidade, **não** avalia as regras determinísticas `R1`–`R4` e **não** tem acesso à rede ou ferramentas. Atua exclusivamente como módulo *Maker* delimitado para:
  - Casos ambíguos de fronteira em **`R5@1.0`** (técnica de alteração legislativa);
  - Avaliação semântica de indicação de objeto e âmbito de aplicação em **`R6@1.0`** (após triagem do motor de aplicabilidade que descarta atos meramente alteradores/revogadores).
- **Parâmetros congelados:**
  - `temperature = 0`
  - `seed = 42`
  - Saída restrita a **JSON Schema** estrito
- **Recuperação lexical associada (condições B e C):** `bm25s`, variante Lucene (`k1 = 1.2`, `b = 0.75`), `top-5`.

## 2. Isolamento, Quarentena e Verificação Obrigatória

| Controle | Mecanismo especificado |
| --- | --- |
| **Isolamento de rede** | Container Ollama em rede Docker `internal: true` (100% sem saída para a internet). |
| **Ausência de agência** | Nenhuma ferramenta (*function calling*, shell, HTTP ou SQL) exposta ao modelo. |
| **Defesa de entrada** | Texto normativo marcado com *spotlighting/datamarking*, preservando a linguagem imperativa original para auditoria sem confundi-la com instruções do sistema. |
| **Verificação pós-saída** | Toda citação ou achado proposto passa por verificação de **integridade byte a byte** no documento e **suporte do predicado** antes de persistir no PostgreSQL 17; falhas convertem a saída em `NAO_AVALIAVEL`. |
| **Idempotência** | Chamadas indexadas no `llm_cache` por hash do modelo, digest, prompt, parâmetros, manifesto do corpus e commit Git. |

## 3. Usos Previstos vs. Fora de Escopo

- **Uso previsto:** apoio delimitado à detecção de `R5` (casos ambíguos) e `R6` dentro do pipeline offline do Auditor 12.002, sempre submetido aos verificadores determinísticos e à fronteira do Art. 76.
- **Fora de escopo:** uso como consultor jurídico autônomo; execução sem verificador de âncora literal; uso em ambiente com dados sigilosos sem revisão do modelo de ameaças; emissão de juízo sobre constitucionalidade ou validade jurídica.

## 4. Avaliação e Limitações Conhecidas

- **Desempenho comparativo:** será mensurado no experimento `D / A / B / C` comparando LLM *zero-shot* (`A`), LLM + BM25 (`B`) e pipeline completo (`C`) contra o baseline determinístico (`D`). *(Resultados pendentes de execução.)*
- **Requisito computacional:** recomenda-se GPU com `>= 12 GB` de VRAM para inferência local fluida do `qwen3:8b`; execuções repetidas utilizam o `llm_cache`.
- **Fallback *fail-closed*:** qualquer violação de JSON Schema, ausência de citação literal no texto extraído ou falha no `Verificador FINAL` impede a emissão de `CONFORME`/`ACHADO`, resultando em `NAO_AVALIAVEL`.
