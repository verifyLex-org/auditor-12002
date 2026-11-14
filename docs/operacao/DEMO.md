# Roteiro de Demonstração (`DEMO`)

> **Estágio:** Roteiro-alvo de demonstração planejado com base na arquitetura do `README.md`. O dashboard Streamlit (`app/`), o `docker-compose.yml` e a CLI `pipeline/` ainda não foram implementados; os comandos abaixo documentam o fluxo esperado após a entrega do sistema funcional.

## Objetivo da Demonstração

Demonstrar ponta a ponta, em ambiente **100% offline**, como o **Auditor 12.002** classifica atos normativos federais frente às seis regras do Decreto nº 12.002/2024 com rastreabilidade completa, respeito a exceções legais e abstenção determinística.

## Fluxo Alvo de Execução Offline

1. **Verificação de integridade do corpus:**
   - Executar `make verify-manifest` para confirmar que os arquivos em `data/raw/` correspondem exatamente ao `data/manifesto.csv` e ao `data/MANIFEST.sha256`.
2. **Inicialização da stack local isolada:**
   - Subir os serviços com `docker compose up -d`: **PostgreSQL 17**, **Ollama** (rede `internal: true`, sem acesso externo) e **Streamlit** (`http://localhost:8501`).
   - Confirmar que os pesos do modelo `qwen3:8b` já foram baixados previamente (`docker compose exec ollama ollama pull qwen3:8b`), permitindo desconectar a máquina da rede.
3. **Inspeção na interface analítica (`http://localhost:8501`):**
   - **Caso 1 — `ACHADO` ancorado:** exibir um ato com ocorrência verificada (por exemplo, cláusula genérica `"revogam-se as disposições em contrário"` em `R2` ou ausência de forma prevista de vigência em `R1`), mostrando o trecho literal, o offset exato, o hash SHA-256 e a ressalva do art. 76.
   - **Caso 2 — `NAO_APLICAVEL` por exceção legal:** exibir um decreto de promulgação de ato internacional avaliado em `R4` (ou ato meramente alterador em `R6`), destacando a justificativa normativa automática que evita falso positivo.
   - **Caso 3 — `NAO_AVALIAVEL` por abstenção:** exibir um caso de divergência entre HTML e PDF oficial (ou falha controlada no verificador), evidenciando o comportamento *fail-closed*.
   - **Caso 4 — Auditoria matemática e cache:** exibir a tabela consolidada de resultados recomputada por views SQL no PostgreSQL 17 e validada pelo `Verificador FINAL`, além do registro no `llm_cache`.

## O que já está demonstrável agora (Fase 1 — Documentação)

Enquanto os módulos de código são implementados, o portal de documentação pode ser servido localmente de forma integralmente estática:

```bash
uv sync --locked
uv run --frozen mkdocs serve -a 127.0.0.1:8001
```
