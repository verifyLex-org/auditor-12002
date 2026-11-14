---
title: Início
hide:
  - navigation
  - toc
---

<div class="vlx-landing-wrap">

<div class="vlx-hero">
  <span class="vlx-eyebrow">Decreto nº 12.002/2024 · verifyLex-org</span>
  <h1 class="vlx-title">Auditor 12.002</h1>
  <p class="vlx-headline">Assistente auditável de revisão de técnica legislativa com abstenção determinística</p>
  <p class="vlx-subheadline">
    Avaliação reproduzível de atos normativos federais publicados frente a seis regras objetivas do Decreto nº 12.002/2024, com banco único PostgreSQL 17, dupla fonte concordante e execução 100% offline.
  </p>
  <div class="vlx-cta-group">
    <a href="dominio/" class="vlx-btn-primary">Explorar Domínio e Regras</a>
    <a href="arquitetura/" class="vlx-btn-secondary">Ver Arquitetura Alvo</a>
  </div>
</div>

<div class="vlx-stat-strip">
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">4</div>
    <div class="vlx-stat-label">Estados explícitos de decisão (<code>CONFORME</code>, <code>ACHADO</code>, <code>NAO_APLICAVEL</code>, <code>NAO_AVALIAVEL</code>)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">6</div>
    <div class="vlx-stat-label">Regras auditáveis versionadas (<code>R1@1.0</code> a <code>R6@1.0</code>)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">70</div>
    <div class="vlx-stat-label">Atos previstos no corpus fechado (60 teste + 10 dev)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">Offline</div>
    <div class="vlx-stat-label">Inferência local via Ollama (<code>qwen3:8b</code>) em rede isolada</div>
  </div>
</div>

</div>

!!! info "Estado do repositório — Fase de documentação inicial"
    Este portal consolida a especificação técnica, a fronteira jurídica (art. 76), os registros de decisão arquitetural (ADRs) e o pré-registro experimental do **Auditor 12.002**. Os módulos de código (`domain/`, `parser/`, `rules/`, `llm/`, `verify/`, `sql/`, `app/`), o corpus fechado em `data/` e a execução das condições `D/A/B/C` ainda serão implementados nos próximos marcos.

## Máquina de Estados Explícita

Cada par `(ato, regra)` é classificado em exatamente um de quatro estados mutuamente exclusivos:

!!! conforme "CONFORME — Regra aplicável e atendida na evidência extraída"
    A regra aplica-se ao escopo do ato, a evidência íntegra está disponível e os critérios objetivos ou verificados foram satisfeitos.

!!! achado "ACHADO — Ocorrência verificada de técnica legislativa (Art. 70, III)"
    Desvio objetivo de técnica legislativa ancorado por trecho literal, offset e hash SHA-256. Em regras sensíveis à tipografia, exige confirmação simultânea na fonte primária (HTML) e no PDF oficial do DOU. Nunca equivale a juízo de invalidade ou ilegalidade (art. 76).

!!! nao-aplicavel "NAO_APLICAVEL — Fora de escopo ou sob exceção legal explícita"
    O ato não se enquadra na pré-condição da regra (por exemplo, `R5` em ato não alterador) ou incide em exceção prevista no decreto (por exemplo, decretos de promulgação de atos internacionais em `R4` ou atos meramente alteradores/revogadores em `R6`).

!!! nao-avaliavel "NAO_AVALIAVEL — Abstenção obrigatória por insuficiência de evidência"
    Acionado deterministicamente quando há falha de extração, divergência entre HTML e PDF ou ausência de suporte verificável byte a byte na saída do modelo local.

## Navegação do Portal

<div class="grid cards" markdown>

-   :material-book-open-variant-outline: **[Domínio e Regras R1–R6](dominio/index.md)**

    ---

    Escopo legal do Decreto nº 12.002/2024, catálogo `R1@1.0` a `R6@1.0` e fronteira do Art. 76.

-   :material-sitemap-outline: **[Arquitetura e ADRs](arquitetura/index.md)**

    ---

    Pipeline em etapas, quarentena do LLM, banco único PostgreSQL 17 e decisões arquiteturais.

-   :material-database-check-outline: **[Dados, Modelos e Protocolo D/A/B/C](dados-e-modelos/DATA_CARD.md)**

    ---

    Data Card do corpus fechado, Model Card do `qwen3:8b` e desenho experimental pré-registrado.

-   :material-shield-lock-outline: **[Segurança, FinOps e Operação](seguranca/threat-model.md)**

    ---

    Defesas contra *prompt injection* indireto, custos offline (`FINOPS.md`), roteiro de demo e guia de uso.

</div>

!!! note "Aviso de independência institucional"
    Projeto independente de código aberto (`verifyLex-org`), desenvolvido sobre atos públicos oficiais (Diário Oficial da União, Câmara dos Deputados e Portal da Legislação). Não possui vínculo, patrocínio ou endosso da Casa Civil, da SAJ ou da Universidade de Brasília (UnB).
