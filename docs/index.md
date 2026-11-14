---
title: Início
hide:
  - navigation
  - toc
---

<div class="vlx-landing-wrap">

<div class="vlx-hero">
  <div class="vlx-badges">
    <span class="vlx-badge">Decreto nº 12.002/2024</span>
    <span class="vlx-badge">100% offline</span>
    <span class="vlx-badge">Python 3.12</span>
    <span class="vlx-badge">Licença MIT</span>
  </div>
  <h1 class="vlx-title">Auditor 12.002</h1>
  <p class="vlx-headline">Revisão auditável de técnica legislativa, com abstenção determinística quando a evidência não basta.</p>
  <p class="vlx-subheadline">
    Avalia atos normativos federais publicados contra seis regras objetivas do Decreto nº 12.002/2024. Cada veredito aponta sua evidência literal ou declara por que não pôde ser emitido.
  </p>
  <div class="vlx-cta-group">
    <a href="operacao/como-rodar/" class="vlx-btn-primary">Começar pelo quickstart</a>
    <a href="dominio/" class="vlx-btn-secondary">Entender o domínio e as regras</a>
  </div>
</div>

<div class="vlx-stat-strip">
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">4</div>
    <div class="vlx-stat-label">Estados mutuamente exclusivos por par (ato, regra)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">6</div>
    <div class="vlx-stat-label">Regras versionadas, de <code class="vlx-rule">R1@1.0</code> a <code class="vlx-rule">R6@1.0</code></div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">70</div>
    <div class="vlx-stat-label">Atos no corpus fechado previsto (60 de teste e 10 de desenvolvimento)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">Offline</div>
    <div class="vlx-stat-label">Inferência local com Ollama (<code>qwen3:8b</code>) em rede isolada</div>
  </div>
</div>

</div>

!!! info "Estado atual do repositório"

    | Pronto para uso | Em roadmap |
    | --- | --- |
    | Especificação de domínio e fronteira do Art. 76 | Pipeline de execução (`parser/`, `rules/`, `llm/`, `verify/`) |
    | ADRs 001 a 003 e contratos de dados | Banco PostgreSQL 17 e views (`sql/`) |
    | Pré-registro experimental (`PREREGISTRO.md`) | Execução das condições D, A, B e C (`pipeline/`, `eval/`) |
    | CI, governança, pre-commit e portal de documentação | Corpus `data/` e painel Streamlit (`app/`) |

## Como funciona a decisão

Cada par `(ato, regra)` cai em exatamente um de quatro estados. A abstenção é um resultado válido, não uma falha silenciosa.

<div class="vlx-state-grid">
  <div class="vlx-state-card vlx-state-card--conforme">
    <span class="vlx-badge vlx-badge--conforme">CONFORME</span>
    <p>Regra aplicável, evidência íntegra e critério atendido.</p>
  </div>
  <div class="vlx-state-card vlx-state-card--achado">
    <span class="vlx-badge vlx-badge--achado">ACHADO</span>
    <p>Ocorrência ancorada por trecho, offset e SHA-256. Não é juízo de invalidade (art. 76).</p>
  </div>
  <div class="vlx-state-card vlx-state-card--nao-aplicavel">
    <span class="vlx-badge vlx-badge--nao-aplicavel">NAO_APLICAVEL</span>
    <p>Fora do escopo da regra ou sob exceção legal explícita.</p>
  </div>
  <div class="vlx-state-card vlx-state-card--nao-avaliavel">
    <span class="vlx-badge vlx-badge--nao-avaliavel">NAO_AVALIAVEL</span>
    <p>Abstenção obrigatória: falha de extração, divergência entre HTML e PDF ou suporte não verificado.</p>
  </div>
</div>

## Escolha seu caminho

<div class="grid cards" markdown>

-   :material-scale-balance: **[Jurídico e domínio](dominio/index.md)**

    ---

    - Escopo do Decreto nº 12.002/2024
    - Catálogo `R1@1.0` a `R6@1.0`
    - Fronteira do Art. 76

-   :material-sitemap-outline: **[Engenharia e arquitetura](arquitetura/index.md)**

    ---

    - Pipeline determinístico e quarentena do LLM
    - Dupla fonte concordante (HTML + PDF do DOU)
    - Contratos Pydantic v2 e banco único

-   :material-flask-outline: **[Pesquisa e avaliação](dados-e-modelos/index.md)**

    ---

    - Data Card do corpus fechado
    - Model Card do `qwen3:8b`
    - Protocolo D/A/B/C pré-registrado

-   :material-console: **[Operação](operacao/como-rodar.md)**

    ---

    - Quickstart offline reproduzível
    - Roteiro de demonstração
    - Custos e requisitos de hardware

</div>

!!! note "Independência institucional"
    Projeto independente de código aberto (`verifyLex-org`), desenvolvido sobre atos públicos oficiais (Diário Oficial da União, Câmara dos Deputados e Portal da Legislação). Não possui vínculo, patrocínio ou endosso da Casa Civil, da SAJ ou da Universidade de Brasília (UnB).
