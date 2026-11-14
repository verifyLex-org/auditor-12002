# Roteiro de Demonstração (`DEMO`)

!!! warning "Roteiro-alvo (em roadmap)"
    Planejado com base na arquitetura do `README.md`. O dashboard Streamlit (`app/`), o `compose.yml` e a CLI `pipeline/` ainda não foram implementados; os comandos abaixo documentam o fluxo esperado após a entrega do sistema funcional.

## Objetivo da Demonstração

Demonstrar ponta a ponta, em ambiente **100% offline**, como o **Auditor 12.002** classifica atos normativos federais frente às seis regras do Decreto nº 12.002/2024 com rastreabilidade completa, respeito a exceções legais e abstenção determinística.

## Fluxo Alvo de Execução Offline

1. **Verificação de integridade do corpus:**
   - Executar `make verify-manifest` para confirmar que os arquivos em `data/raw/` correspondem exatamente ao `data/manifesto.csv` e ao `data/MANIFEST.sha256`.
2. **Inicialização da stack local isolada:**
   - Subir os serviços com `docker compose up -d`: **PostgreSQL 17**, **Ollama** (rede `internal: true`, sem acesso externo) e **Streamlit** (`http://localhost:8501`).
   - Confirmar que os pesos do modelo `qwen3:8b` já foram baixados previamente (`docker compose exec ollama ollama pull qwen3:8b`), permitindo desconectar a máquina da rede.
3. **Inspeção na interface analítica (`http://localhost:8501`):** percorrer os quatro casos abaixo.

<div class="vlx-card-grid">
  <article class="vlx-card"><header><span class="vlx-badge vlx-badge--achado">ACHADO</span></header><h3>Caso 1 — ACHADO ancorado</h3><p>Ato com ocorrência verificada (ex.: <code>R2</code> ou <code>R1</code>): trecho literal, offset exato, SHA-256 e ressalva do art. 76.</p></article>
  <article class="vlx-card"><header><span class="vlx-badge vlx-badge--nao-aplicavel">NAO_APLICAVEL</span></header><h3>Caso 2 — Exceção legal</h3><p>Decreto de promulgação em <code>R4</code> (ou ato meramente alterador em <code>R6</code>): a justificativa normativa evita o falso positivo.</p></article>
  <article class="vlx-card"><header><span class="vlx-badge vlx-badge--nao-avaliavel">NAO_AVALIAVEL</span></header><h3>Caso 3 — Abstenção</h3><p>Divergência entre HTML e PDF oficial (ou falha do verificador): comportamento <em>fail-closed</em>.</p></article>
  <article class="vlx-card"><header><span class="vlx-badge">AUDITORIA</span></header><h3>Caso 4 — Auditoria matemática</h3><p>Tabela recomputada por views SQL no PostgreSQL 17, validada pelo <code>Verificador FINAL</code>, com registro no <code>llm_cache</code>.</p></article>
</div>

## O que já está demonstrável agora (Fase 1 — Documentação)

Enquanto os módulos de código são implementados, o portal de documentação pode ser servido localmente de forma integralmente estática:

```bash
uv sync --locked
uv run --frozen mkdocs serve -a 127.0.0.1:8001
```
