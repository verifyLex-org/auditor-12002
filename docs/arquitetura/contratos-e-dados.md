# Contratos de Dados e Banco Único

> **Estágio:** Especificação arquitetural pré-implementação. O schema SQL exato (`sql/`) e os modelos Pydantic v2 (`domain/`) ainda serão criados e versionados nos próximos marcos.

## Separação de Camadas

A arquitetura planejada separa estritamente três níveis de responsabilidade:

1. **Domínio puro (`domain/`):** contratos Pydantic v2 e invariantes da máquina de estados (`CONFORME`, `ACHADO`, `NAO_APLICAVEL`, `NAO_AVALIAVEL`), sem acesso a disco, rede ou banco de dados.
2. **Aplicação e Pipeline (`parser/`, `rules/`, `retrieval/`, `llm/`, `verify/`, `pipeline/`):** orquestram extração hierárquica, dupla fonte, aplicabilidade, quarentena de LLM e verificação pós-geração.
3. **Persistência e Apresentação (`sql/`, `app/`):** banco único em **PostgreSQL 17** (tabelas, `llm_cache` e views analíticas) e interface local em **Streamlit**.

## Invariantes Planejadas dos Contratos (`domain/`)

Embora os schemas exatos ainda não tenham sido codificados, o design do `README.md` estabelece invariantes obrigatórias para os contratos Pydantic v2:

- **Identificação do par avaliado:** todo resultado pertence a um par `(ato_id, regra_id_versao)` e a uma condição experimental (`D`, `A`, `B` ou `C`).
- **Ancoragem literal obrigatória em `ACHADO`:** um registro no estado `ACHADO` deve carregar trecho literal, offsets verificáveis no texto canônico extraído e digest criptográfico (`SHA-256`), reprovável automaticamente caso a substring não exista byte a byte no documento.
- **Justificativa explícita em abstenção e exceção:**
  - `NAO_APLICAVEL` deve apontar a regra de exceção ou pré-condição ausente;
  - `NAO_AVALIAVEL` deve registrar o código estruturado da limitação (divergência HTML/PDF, falha de parsing, reprovação no verificador ou violação de JSON Schema).
- **Proibição de linguagem conclusiva ilegal (Art. 76):** textos renderizados não podem afirmar invalidade ou ilegalidade do ato auditado.

## Banco Único PostgreSQL 17 (`sql/` e `llm_cache`)

Para evitar proliferação de bancos auxiliares ou arquivos intermediários inconsistentes, o sistema consolida persistência e auditoria no **PostgreSQL 17**:

- **Tabelas operacionais:** inventário de atos e hashes de manifesto, unidades hierárquicas extraídas (`art`, `§`, `inciso`, `alínea`, blocos citados), resultados por `(ato, regra, condição)` e trilha de verificação (`Integridade`, `Predicado`, `Verificador FINAL`).
- **Ledger idempotente `llm_cache`:** armazena requisições e respostas estruturadas do LLM indexadas por chave composta determinística contendo:
  1. Hash/identificador do modelo local (`qwen3:8b`) e digest;
  2. Prompt e template versionados;
  3. Parâmetros congelados (`temperature = 0`, `seed = 42`, JSON Schema);
  4. Manifesto do corpus (`MANIFEST.sha256`);
  5. Commit Git da execução.
- **Views analíticas de fechamento:** todo totalizador, contagem por estado e métrica agregada exibida na UI Streamlit ou nos relatórios experimentais será recomputada diretamente por views SQL, sendo rejeitada pelo `Verificador FINAL` em caso de discrepância após a renderização.
