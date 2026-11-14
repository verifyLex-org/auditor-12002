---
title: Início
hide:
  - navigation
  - toc
---

<div class="vlx-landing-wrap">

<div class="vlx-hero">
  <div class="vlx-pills vlx-rv">
    <span class="vlx-pill">Auditor 12.002</span>
    <span class="vlx-pill">Decreto nº 12.002/2024</span>
    <span class="vlx-pill">100% offline</span>
    <span class="vlx-pill">Python 3.12</span>
    <span class="vlx-pill">MIT</span>
  </div>
  <h1 class="vlx-title vlx-rv" style="animation-delay: 0.08s">Revisão legislativa<br><em>que mostra a prova.</em></h1>
  <p class="vlx-lead vlx-rv" style="animation-delay: 0.16s">
    Avalia atos normativos federais publicados contra seis regras objetivas do Decreto nº 12.002/2024. Cada veredito aponta sua evidência literal ou declara por que não pôde ser emitido.
  </p>
  <div class="vlx-cta-group vlx-rv" style="animation-delay: 0.24s">
    <a href="operacao/como-rodar/" class="vlx-btn-primary">Começar pelo quickstart <span class="vlx-arrow" aria-hidden="true">→</span></a>
    <a href="dominio/" class="vlx-btn-secondary">Entender o domínio e as regras</a>
  </div>
  <div class="vlx-verdict vlx-rv" style="animation-delay: 0.34s" aria-label="Exemplo ilustrativo do formato de um veredito">
    <div class="vlx-verdict-bar"><span class="vlx-dot" aria-hidden="true"></span><span class="vlx-dot" aria-hidden="true"></span><span class="vlx-dot" aria-hidden="true"></span><span>veredito · formato ilustrativo</span></div>
    <div class="vlx-verdict-body">
      <div><span class="vlx-k">par</span><span class="vlx-v">(ato, R3@1.0)</span></div>
      <div><span class="vlx-k">estado</span><span class="vlx-v"><span class="vlx-badge vlx-badge--achado">ACHADO</span></span></div>
      <div><span class="vlx-k">trecho</span><span class="vlx-v">[trecho literal ancorado]</span></div>
      <div><span class="vlx-k">offset</span><span class="vlx-v">[posição no documento]</span></div>
      <div><span class="vlx-k">sha256</span><span class="vlx-v">[hash do trecho]<span class="vlx-caret" aria-hidden="true"></span></span></div>
    </div>
  </div>
</div>

<div class="vlx-stat-strip vlx-reveal vlx-rv">
  <div class="vlx-stat-item">
    <div class="vlx-stat-number vlx-count-4" aria-label="4"></div>
    <div class="vlx-stat-label">Estados mutuamente exclusivos por par (ato, regra)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number vlx-count-6" aria-label="6"></div>
    <div class="vlx-stat-label">Regras versionadas, de <code class="vlx-rule">R1@1.0</code> a <code class="vlx-rule">R6@1.0</code></div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number vlx-count-70" aria-label="70"></div>
    <div class="vlx-stat-label">Atos no corpus fechado previsto (60 de teste e 10 de desenvolvimento)</div>
  </div>
  <div class="vlx-stat-item">
    <div class="vlx-stat-number">Offline</div>
    <div class="vlx-stat-label">Inferência local com Ollama (<code>qwen3:8b</code>) em rede isolada</div>
  </div>
</div>

</div>

## Quatro estados, nenhuma falha silenciosa

A abstenção é um resultado válido. Nenhum caminho de erro produz `CONFORME` ou `ACHADO` por acidente.

<div class="vlx-state-grid vlx-reveal vlx-rv">
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

## O modelo nunca decide sozinho

Dados não confiáveis entram por um núcleo determinístico. O LLM roda em quarentena e toda saída é verificada byte a byte.

<div class="vlx-zones vlx-reveal vlx-rv">
  <div class="vlx-zone">
    <p class="vlx-zone-title">ZONA NÃO CONFIÁVEL</p>
    <div class="vlx-node"><b>data/raw/*</b>HTML + PDF + XML, SHA-256 no manifesto</div>
  </div>
  <div class="vlx-zone vlx-zone--det">
    <p class="vlx-zone-title">NÚCLEO DETERMINÍSTICO</p>
    <div class="vlx-node"><b>Parser hierárquico</b>art / § / inciso / alínea</div>
    <div class="vlx-node"><b>Avaliabilidade e aplicabilidade</b>dupla fonte · escopo · exceções</div>
    <div class="vlx-node"><b>Checkers R1–R5</b>regras objetivas</div>
  </div>
  <div class="vlx-zone vlx-zone--llm">
    <p class="vlx-zone-title">LLM EM QUARENTENA</p>
    <div class="vlx-node"><b>Spotlighting / datamarking</b>sem ferramentas, sem rede</div>
    <div class="vlx-node"><b>Maker R5/R6</b>JSON Schema · temp 0 · seed 42</div>
  </div>
  <div class="vlx-zone vlx-zone--verify">
    <p class="vlx-zone-title">VERIFICAÇÃO</p>
    <div class="vlx-node"><b>Integridade byte a byte</b>e suporte do predicado</div>
    <div class="vlx-node"><b>Verificador FINAL</b>sobre o artefato renderizado</div>
  </div>
  <span class="vlx-link vlx-link--1" aria-hidden="true"></span><span class="vlx-link vlx-link--2" aria-hidden="true"></span><span class="vlx-link vlx-link--3" aria-hidden="true"></span>
</div>

## Escolha seu caminho

<div class="grid cards vlx-reveal vlx-rv" markdown>

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

## Estado atual do repositório

<p class="vlx-section-lead">Especificação normativa, contratos de dados e governança automatizada estão prontos e auditados. Os módulos de execução e ingestão encontram-se estruturados como stubs em construção.</p>

<div class="vlx-status-board vlx-reveal vlx-rv">
  <section class="vlx-status-panel vlx-status-panel--ready" aria-labelledby="vlx-status-ready-title">
    <div class="vlx-status-head">
      <h3 class="vlx-status-title" id="vlx-status-ready-title">Artefatos disponíveis</h3>
      <span class="vlx-status-pill vlx-status-pill--ready"><span class="vlx-status-dot" aria-hidden="true"></span>Pronto para uso</span>
    </div>
    <ul class="vlx-status-list">
      <li><strong>Domínio e fronteira do Art. 76:</strong> escopo jurídico e catálogo <code>R1@1.0</code> a <code>R6@1.0</code> especificados.</li>
      <li><strong>Decisões e contratos:</strong> ADRs 001 a 003, Data Card, Model Card e pré-registro em <code>PREREGISTRO.md</code>.</li>
      <li><strong>Integridade de manifesto:</strong> gerador e verificador determinístico em <code>verify/manifest.py</code> com testes.</li>
      <li><strong>Governança e documentação:</strong> CI, <code>scripts.check_governance</code>, hooks de pre-commit e portal MkDocs.</li>
    </ul>
  </section>
  <section class="vlx-status-panel vlx-status-panel--roadmap" aria-labelledby="vlx-status-roadmap-title">
    <div class="vlx-status-head">
      <h3 class="vlx-status-title" id="vlx-status-roadmap-title">Entregas planejadas</h3>
      <span class="vlx-status-pill vlx-status-pill--roadmap"><span class="vlx-status-dot" aria-hidden="true"></span>Em roadmap</span>
    </div>
    <ul class="vlx-status-list">
      <li><strong>Pipeline e verificadores semânticos:</strong> módulos <code>parser/</code>, <code>rules/</code>, <code>llm/</code>, <code>retrieval/</code> e <code>verify/{evidence,terminology}.py</code>.</li>
      <li><strong>Persistência e containerização:</strong> banco PostgreSQL 17, views em <code>sql/</code>, <code>compose.yml</code> e <code>Dockerfile</code>.</li>
      <li><strong>Execução experimental D/A/B/C:</strong> orquestrador e métricas comparativas em <code>pipeline/</code> e <code>eval/</code>.</li>
      <li><strong>Corpus e visualização:</strong> atos do conjunto fechado em <code>data/</code> e painel Streamlit em <code>app/</code>.</li>
    </ul>
  </section>
</div>

!!! note "Independência institucional"
    Projeto independente de código aberto (`verifyLex-org`), desenvolvido sobre atos públicos oficiais (Diário Oficial da União, Câmara dos Deputados e Portal da Legislação). Não possui vínculo, patrocínio ou endosso da Casa Civil, da SAJ ou da Universidade de Brasília (UnB).
