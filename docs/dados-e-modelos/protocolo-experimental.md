# Protocolo Experimental (`D / A / B / C`)

> **Estágio:** Protocolo pré-registrado antes da coleta final de gabarito e da execução experimental. O documento normativo fonte na raiz do repositório é [PREREGISTRO.md](https://github.com/verifyLex-org/auditor-12002/blob/main/PREREGISTRO.md).

Os blocos abaixo são incluídos diretamente do `PREREGISTRO.md` para evitar divergência entre o documento congelado na raiz e o portal de documentação:

--8<-- "PREREGISTRO.md:protocolo"

---

## Resultados Experimentais (`gold-v1`)

> **Status de execução:** **Pendente de execução.** A tabela abaixo permanece reservada até o congelamento de `data/manifesto.csv`, `data/MANIFEST.sha256`, `data/gold/gold-v1.csv` e a execução determinística reproduzida via `make reproduce`.

| Condição | Precisão `ACHADO` (IC 95%) | *Recall* Mutações (120) | Acurácia `NAO_APLICAVEL` | Cobertura | Risco Seletivo |
| --- | --- | --- | --- | --- | --- |
| **D** (Determinístico) | *Pendente* | *Pendente* | *Pendente* | *Pendente* | *Pendente* |
| **A** (LLM *zero-shot*) | *Pendente* | *Pendente* | *Pendente* | *Pendente* | *Pendente* |
| **B** (LLM + BM25) | *Pendente* | *Pendente* | *Pendente* | *Pendente* | *Pendente* |
| **C** (Pipeline completo) | *Pendente* | *Pendente* | *Pendente* | *Pendente* | *Pendente* |
