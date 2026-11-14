# Pré-registro Experimental — Auditor 12.002

> **Status:** Rascunho de pré-registro para congelamento prévio à montagem do gabarito `gold-v1.csv` e à execução do experimento `D / A / B / C`. Nenhum resultado experimental foi gerado até o momento.

## 1. Identificação e Compromisso de Congelamento

- **Projeto:** Auditor 12.002 (`verifyLex-org/auditor-12002`)
- **Marco normativo auditado:** Decreto nº 12.002, de 22 de abril de 2024 (vigência a partir de 1º/06/2024, art. 78), regras `R1@1.0` a `R6@1.0`.
- **Regra de integridade:** este pré-registro, os arquivos de manifesto (`data/manifesto.csv`, `data/MANIFEST.sha256`) e o gabarito `data/gold/gold-v1.csv` serão congelados antes da execução comparativa sobre o conjunto de teste (60 atos). Após o congelamento, alterações nessas referências devem ser bloqueadas em CI.

<!-- --8<-- [start:protocolo] -->
## 2. Questão de Pesquisa e Hipóteses (`D / A / B / C`)

O experimento avalia se a combinação de **motor explícito de aplicabilidade em 4 estados**, **dupla fonte concordante** e **verificadores determinísticos pós-geração** reduz falsos positivos e melhora a calibração frente a baselines baseados em LLM isolado ou RAG lexical simples, operando 100% offline com `qwen3:8b`.

### Condições experimentais comparadas

| Condição | Descrição | LLM | Recuperação | Aplicabilidade (4 estados) | Verificadores |
| --- | --- | --- | --- | --- | --- |
| **D** | Baseline determinístico (regras + SQL; abstenção/heurística em R5/R6) | Não | — | Sim | Integridade |
| **A** | LLM *zero-shot* (`qwen3:8b`, texto do ato + artigo da regra) | Sim | Nenhuma | Não | Apenas schema |
| **B** | LLM + recuperação lexical BM25 (`bm25s`, variante Lucene, `k1=1.2, b=0.75`) | Sim | BM25 (top-5) | Não | Apenas schema |
| **C** | **Pipeline completo** (aplicabilidade + checkers + LLM delimitado + verificadores) | Sim (R5/R6) | BM25 (top-5) | Sim | Integridade + predicado + final |

### Hipóteses pré-especificadas

- **H1 (Precisão sobre LLM isolado):** a condição **C** obtém maior precisão de `ACHADO` do que **A** e **B** nas 360 decisões reais, reduzindo falsos positivos em casos de exceção legal e bloqueios de extração.
- **H2 (Separação de escopo e exceção):** as condições com motor de aplicabilidade (**D** e **C**) superam **A** e **B** na acurácia de classificação de `NAO_APLICAVEL` (incluindo blocos citados de outro ato e decretos de promulgação de atos internacionais em `R4`).
- **H3 (*Recall* controlado sem inflar prevalência):** em **120 mutações sintéticas controladas** (20 por regra), a condição **C** mantém *recall* superior ao baseline determinístico **D** nas regras híbridas/semânticas (`R5`, `R6`) sem degradar a precisão nas regras determinísticas (`R1`–`R4`).
- **H4 (Segurança contra *prompt injection*):** sob a bateria de 12 ataques de *prompt injection* indireto em textos normativos simulados, a condição **C** não permite emissão de `ACHADO` sem âncora byte a byte válida nem execução de ações fora do JSON Schema.

## 3. Corpus de Avaliação e Mutações Sintéticas

- **Conjunto real fechado (70 atos):** atos normativos federais publicados após `01/06/2024` (art. 78) no âmbito da administração pública federal direta, autárquica e fundacional (art. 2º):
  - **Desenvolvimento (`dev`):** 10 atos (60 decisões `ato × regra`), usados para calibração de parser, regras e prompts antes do congelamento.
  - **Teste (`test`):** 60 atos (360 decisões `ato × regra`), mantidos fechados até a rodada oficial:
    - 12 decretos numerados;
    - 3 decretos de promulgação de atos internacionais;
    - 18 portarias ministeriais;
    - 20 portarias/instruções normativas de autarquias e fundações;
    - 7 resoluções de colegiados.
- **Conjunto sintético de mutações:** **120 mutações sintéticas controladas** (20 por regra, `R1` a `R6`) injetadas sobre atos base para estimar *recall* de defeitos raros sem inferir prevalência real a partir da taxa sintética.

## 4. Desfechos, Métricas e Rigor Estatístico

- **Desfecho primário:** precisão de `ACHADO` no conjunto de teste real (360 decisões `ato × regra`).
- **Desfechos secundários:**
  - *Recall* em mutações sintéticas controladas (120 mutações);
  - Acurácia específica em casos de exceção e fora de escopo (`NAO_APLICAVEL`);
  - Cobertura (`1 - taxa de NAO_AVALIAVEL`) e risco seletivo (*selective risk* sobre decisões emitidas como `CONFORME`/`ACHADO`);
  - Taxa de aprovação dos invariantes de verificação (integridade byte a byte, suporte de predicado e verificador FINAL).
- **Concordância inter-anotadores:** cálculo do **κ de Cohen por regra antes da adjudicação** entre anotadores cegos sobre o gabarito.
- **Incerteza e testes de hipótese:**
  - Intervalos de confiança de **Wilson (95%)** para proporções;
  - ***Bootstrap* agrupado por ato** (*cluster bootstrap* preservando correlação entre as 6 regras do mesmo ato);
  - **Teste exato de McNemar** para comparações pareadas entre condições (`C vs. A`, `C vs. B`, `C vs. D`) no mesmo conjunto de decisões.
<!-- --8<-- [end:protocolo] -->

## 5. Critérios de Corte, Regras de Parada e Relato Negativo

- **Parâmetros congelados de inferência e recuperação:**
  - Modelo local: `qwen3:8b` via Ollama, rede `internal: true`, sem ferramentas, `temperature = 0`, `seed = 42`, saída restrita a JSON Schema.
  - Recuperação lexical (condições **B** e **C**): `bm25s`, variante Lucene (`k1 = 1.2`, `b = 0.75`), `top-5`.
- **Regras de parada e transparência:**
  - É proibido ajustar prompts, limiares ou regras após visualizar métricas do conjunto de teste (60 atos) mantendo o mesmo rótulo `gold-v1`.
  - Resultados nulos ou negativos (por exemplo, ausência de ganho estatisticamente significativo de **C** sobre **D** ou **B** em alguma regra) serão reportados integralmente nas tabelas de resultados e na avaliação final.
  - Toda métrica final deverá ser reproduzível via `make reproduce` a partir do ledger `llm_cache` no PostgreSQL 17 e recalculada por views SQL.
