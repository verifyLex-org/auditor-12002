# ADR-001 — Máquina Explícita de 4 Estados e Motor de Aplicabilidade

| Campo | Valor |
| --- | --- |
| **Status** | Proposto (Design inicial) |
| **Data** | 2026-11-13 |
| **Autores** | Equipe verifyLex-org |
| **Regra / Invariante afetada** | Todas (`R1@1.0` a `R6@1.0`), Art. 76, Abstenção determinística |

## 1. Contexto

Sistemas ingênuos de verificação normativa costumam operar em classificação binária (`Conforme` vs. `Não conforme`). Na revisão de técnica legislativa sob o Decreto nº 12.002/2024, essa modelagem gera duas classes graves de erro:

1. **Falsos positivos em exceções legais e pré-condições ausentes:** por exemplo, apontar violação de `"considerando"` (`R4`) em decretos de promulgação de atos internacionais (exceção expressa) ou cobrar cláusula de objeto (`R6`) em atos meramente alteradores (art. 6º, parágrafo único).
2. **Falsos negativos ou alucinações silenciosas em falhas de extração:** quando o parser falha ou há ruído na fonte, um modelo binário tende a classificar como `Conforme` ou inventar um achado sem suporte.

## 2. Opções Consideradas

### Opção 1: Classificação binária (`CONFORME` / `ACHADO`) direta nos checkers/LLM

- Passar todo ato diretamente para os checkers e para o LLM decidir também se a regra se aplica.
- **Vantagens:** menor número de estados no contrato de saída.
- **Desvantagens:** mistura falha de extração com conformidade real, delega interpretação de exceções legais claras ao LLM e impede medição isolada de cobertura e risco seletivo.

### Opção 2: Máquina explícita de 4 estados com motor de avaliabilidade e aplicabilidade prévios (Escolhida)

- Exigir que todo par `(ato, regra)` percorra primeiro o **detector de avaliabilidade** (`NAO_AVALIAVEL`) e o **motor de aplicabilidade** (`NAO_APLICAVEL`) antes de acionar checkers ou LLM.
- **Vantagens:** separa falhas de extração e exceções legais de mérito sintático/semântico; permite medir acurácia de exceção e risco seletivo no protocolo `D/A/B/C`; garante *fail-closed* para `NAO_AVALIAVEL`.
- **Desvantagens:** exige modelagem explícita das pré-condições de cada regra e maior cobertura de testes para transições de estado.

## 3. Decisão Adotada

Adota-se uma **máquina de estados explícita em 4 valores** (`CONFORME`, `ACHADO`, `NAO_APLICAVEL`, `NAO_AVALIAVEL`) com separação arquitetural obrigatória:

1. **Avaliabilidade primeiro:** integridade e concordância de extração bloqueiam a análise em `NAO_AVALIAVEL` antes de qualquer regra de conteúdo.
2. **Aplicabilidade antes da detecção:** escopo e exceções legais explícitas encerram o par como `NAO_APLICAVEL` sem enviar o texto ao LLM.
3. **Verificação pós-detecção:** falhas de schema, de âncora literal byte a byte ou de predicado rebaixam saídas para `NAO_AVALIAVEL`.

## 4. Consequências e Trade-offs

- **Positivas:** redução estrutural de falsos positivos, menor exposição do LLM a atos que não exigem inferência e rastreabilidade estatística clara entre cobertura e precisão.
- **Negativas e riscos:** se o motor de aplicabilidade classificar erroneamente um ato como `NAO_APLICAVEL`, o erro silencia a detecção subsequente.
- **Mitigação:** inclusão de casos difíceis (`tests/hard_cases`), métricas dedicadas de acurácia em `NAO_APLICAVEL` e testes comparativos no experimento `D/A/B/C`.

## 5. Verificação e Auditoria

- Contratos Pydantic v2 em `domain/` restringirão o domínio de saída aos quatro valores enumerados, exigindo justificativa estruturada para `NAO_APLICAVEL` e `NAO_AVALIAVEL`.
- O experimento pré-registrado em `PREREGISTRO.md` testa diretamente essa decisão por meio da hipótese **H2** (`D` e `C` vs. `A` e `B`).
