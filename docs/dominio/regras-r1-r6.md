# Catálogo das 6 Regras Auditáveis (`R1@1.0` a `R6@1.0`)

!!! info "Estágio neste repositório"
    Especificação normativa de regras. Os módulos correspondentes em `rules/` ainda não foram implementados.

Todas as regras referem-se ao **Decreto nº 12.002, de 22 de abril de 2024** (com vigência a partir de 1º de junho de 2024, nos termos do art. 78). Cada regra possui identificador e versão imutáveis por ciclo experimental.

## Visão Geral do Catálogo

<div class="vlx-strip vlx-reveal" role="img" aria-label="Execução por regra: R1 a R4 determinísticas, R5 híbrida, R6 com LLM delimitado">
  <span class="vlx-strip-seg vlx-strip-seg--det"><code>R1@1.0</code></span>
  <span class="vlx-strip-seg vlx-strip-seg--det"><code>R2@1.0</code></span>
  <span class="vlx-strip-seg vlx-strip-seg--det"><code>R3@1.0</code></span>
  <span class="vlx-strip-seg vlx-strip-seg--det"><code>R4@1.0</code></span>
  <span class="vlx-strip-seg vlx-strip-seg--hyb"><code>R5@1.0</code></span>
  <span class="vlx-strip-seg vlx-strip-seg--llm"><code>R6@1.0</code></span>
</div>
<p class="vlx-strip-legend"><span class="vlx-chip vlx-chip--det">Determinística</span> <span class="vlx-chip vlx-chip--hyb">Híbrida</span> <span class="vlx-chip vlx-chip--llm">LLM em quarentena</span> Quatro das seis regras nunca acionam o modelo.</p>

<div class="vlx-card-grid">
  <article class="vlx-card">
    <header><code class="vlx-rule">R1@1.0</code><span class="vlx-chip vlx-chip--det">Determinística</span></header>
    <h3>Cláusula de vigência expressa e em forma prevista</h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 16, <em>caput</em>; art. 18, I–IV e parágrafo único</p>
    <p class="vlx-card-note"><span>Escopo</span>Aplica-se a todo ato do corpus.</p>
  </article>
  <article class="vlx-card">
    <header><code class="vlx-rule">R2@1.0</code><span class="vlx-chip vlx-chip--det">Determinística</span></header>
    <h3>Vedação da revogação genérica (<q>revogam-se as disposições em contrário</q>)</h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 15, § 1º</p>
    <p class="vlx-card-note"><span>Ressalva</span>Ocorrências dentro de blocos citados de outro ato não contam.</p>
  </article>
  <article class="vlx-card">
    <header><code class="vlx-rule">R3@1.0</code><span class="vlx-chip vlx-chip--det">Determinística · dupla fonte</span></header>
    <h3>Numeração ordinal até o 9º e cardinal com ponto a partir do 10º (<code>Art. 10.</code>)</h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 12, I, “a”/“b”, V e VI, “a”/“b”</p>
    <p class="vlx-card-note"><span>Ressalva</span>Ignora dispositivos em blocos de alteração; valida sufixo <code>-A</code> (art. 14, parágrafo único).</p>
  </article>
  <article class="vlx-card vlx-card--ex">
    <header><code class="vlx-rule">R4@1.0</code><span class="vlx-chip vlx-chip--det">Determinística</span></header>
    <h3>Vedação de enunciados iniciados por <q>considerando</q></h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 4º, § 3º</p>
    <p class="vlx-card-note"><span>Exceção legal</span>Decretos de promulgação de atos internacionais (<code>NAO_APLICAVEL</code>).</p>
  </article>
  <article class="vlx-card">
    <header><code class="vlx-rule">R5@1.0</code><span class="vlx-chip vlx-chip--hyb">Determinística + LLM delimitado</span></header>
    <h3>Técnica de alteração: fórmula padrão, aspas e <code>(NR)</code></h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 14, I e VII</p>
    <p class="vlx-card-note"><span>Escopo</span>Somente atos que alteram outros atos.</p>
  </article>
  <article class="vlx-card vlx-card--ex">
    <header><code class="vlx-rule">R6@1.0</code><span class="vlx-chip vlx-chip--llm">LLM delimitado + verificador</span></header>
    <h3>Indicação de objeto e âmbito de aplicação nos primeiros dispositivos</h3>
    <p class="vlx-card-fund"><span>Fundamento</span>Art. 6º, <em>caput</em></p>
    <p class="vlx-card-note"><span>Exceção legal</span>Atos meramente alteradores ou revogadores (art. 6º, parágrafo único).</p>
  </article>
</div>

??? note "Ver o catálogo em formato de tabela"

    | ID / Versão | Regra | Fundamento no Decreto nº 12.002/2024 | Escopo e Exceção Legal | Estratégia de Execução |
    | --- | --- | --- | --- | --- |
    | `R1@1.0` | Cláusula de vigência expressa e em forma prevista | Art. 16, *caput*; art. 18, I–IV e parágrafo único | Aplica-se a todo ato do corpus | Determinística |
    | `R2@1.0` | Vedação da revogação genérica (`"revogam-se as disposições em contrário"`) | Art. 15, § 1º | Ocorrências dentro de blocos citados de outro ato não contam | Determinística |
    | `R3@1.0` | Numeração ordinal até o 9º e cardinal com ponto a partir do 10º (`Art. 10.`) | Art. 12, I, `"a"`/`"b"`, V e VI, `"a"`/`"b"` | Ignora dispositivos em blocos de alteração; valida sufixo `-A` (art. 14, parágrafo único) | Determinística (dupla fonte) |
    | `R4@1.0` | Vedação de enunciados iniciados por `"considerando"` | Art. 4º, § 3º | **Exceção explícita:** decretos de promulgação de atos internacionais | Determinística |
    | `R5@1.0` | Técnica de alteração: fórmula padrão, aspas e `"(NR)"` | Art. 14, I e VII | Somente atos que alteram outros atos | Determinística + LLM delimitado |
    | `R6@1.0` | Indicação de objeto e âmbito de aplicação nos primeiros dispositivos | Art. 6º, *caput* | **Exceção explícita:** atos meramente alteradores ou revogadores (art. 6º, parágrafo único) | LLM delimitado + verificador |

---

## Detalhamento por Regra

### `R1@1.0` — Cláusula de vigência expressa

- **Fundamento:** Art. 16, *caput*; art. 18, incisos I a IV e parágrafo único.
- **Pré-condição:** aplicável a 100% dos atos do corpus.
- **Foco de verificação:** verificar presença de cláusula explícita de entrada em vigor e conformidade com as formas previstas de contagem e marco de vigência.
- **Execução:** puramente determinística sobre a árvore hierárquica de dispositivos finais do ato.

### `R2@1.0` — Vedação da cláusula de revogação genérica

- **Fundamento:** Art. 15, § 1º.
- **Pré-condição:** aplicável aos dispositivos próprios do ato auditado.
- **Foco de verificação:** identificar formulações genéricas equivalentes a `"revogam-se as disposições em contrário"`.
- **Proteção contra falso positivo:** o parser hierárquico delimita **blocos citados/de alteração** (transcrições de outros atos entre aspas), de modo que expressões genéricas eventualmente presentes em texto reproduzido de norma anterior não gerem `ACHADO`.

### `R3@1.0` — Numeração de artigos e dispositivos com sufixo `-A`

- **Fundamento:** Art. 12, I, `"a"`/`"b"`, V e VI, `"a"`/`"b"`; art. 14, parágrafo único.
- **Pré-condição:** dispositivos próprios do ato (blocos de alteração ignorados para numeração sequencial do ato alterador, com validação de sufixo `-A` onde aplicável).
- **Foco de verificação:** emprego de numeração ordinal (`Art. 1º` a `Art. 9º`) até o nono dispositivo e cardinal seguida de ponto a partir do décimo (`Art. 10.`).
- **Exigência de dupla fonte:** como pontuações e marcadores ordinais (`º` vs. `.`) podem sofrer degradação em HTML ou OCR/PDF, `R3@1.0` só emite `ACHADO` quando a ocorrência coincide na fonte primária (HTML) e na conferência (PDF oficial do DOU); em divergência, abstém-se como `NAO_AVALIAVEL`.

### `R4@1.0` — Vedação de enunciados iniciados por `"considerando"`

- **Fundamento:** Art. 4º, § 3º.
- **Exceção explícita (`NAO_APLICAVEL`):** decretos de promulgação de atos internacionais (tratados, acordos e convenções promulgados).
- **Foco de verificação:** detecção determinística de preâmbulos ou dispositivos iniciados por `"considerando"` fora da exceção.
- **Por que é crítica no experimento:** serve de teste direto para o motor de aplicabilidade (`H2`), pois um LLM *zero-shot* sem separação de exceção tende a sinalizar falso positivo em decretos de promulgação (3 atos reservados na estratificação de teste).

### `R5@1.0` — Técnica de alteração legislativa

- **Fundamento:** Art. 14, I e VII.
- **Pré-condição (`NAO_APLICAVEL` quando ausente):** aplica-se somente a atos que promovam alteração em outro ato normativo.
- **Foco de verificação:** emprego da fórmula introdutória de alteração, abertura/fechamento de aspas e aposição de `"(NR)"` ao final dos dispositivos alterados.
- **Execução híbrida:** checagens tipográficas/estruturais determinísticas combinadas com chamada delimitada ao LLM (`qwen3:8b`) apenas para casos ambíguos de fronteira de bloco alterado, sempre sujeita a dupla fonte e verificadores pós-geração.

### `R6@1.0` — Indicação de objeto e âmbito de aplicação

- **Fundamento:** Art. 6º, *caput*.
- **Exceção explícita (`NAO_APLICAVEL`):** atos meramente alteradores ou revogadores (art. 6º, parágrafo único).
- **Foco de verificação:** confirmar se o primeiro artigo (ou primeiros dispositivos) explicita o objeto do ato e o respectivo âmbito de aplicação.
- **Execução:** executada pelo componente LLM em quarentena (`qwen3:8b`, JSON Schema, `temp = 0`, `seed = 42`) com recuperação lexical `bm25s` quando aplicável, obrigatoriamente validada pelos verificadores de integridade byte a byte, suporte do predicado e verificador FINAL.
