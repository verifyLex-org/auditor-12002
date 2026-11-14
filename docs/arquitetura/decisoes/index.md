# Decisões Arquiteturais (ADRs)

Este índice centraliza os **Architectural Decision Records (ADRs)** do projeto **Auditor 12.002**, documentando decisões estruturais, alternativas descartadas, *trade-offs* e critérios de verificação.

## Processo para Novas ADRs

1. Copie o arquivo modelo `docs/_templates/adr.md` (excluído do site público, mantido no repositório).
2. Nomeie o arquivo seguindo o padrão sequencial `adr-NNN-titulo-curto.md` em `docs/arquitetura/decisoes/`.
3. Preencha todas as seções obrigatórias (Contexto, Opções Consideradas, Decisão, Consequências e Verificação) e atualize a tabela abaixo e o `nav` em `mkdocs.yml`.
4. Submeta via Pull Request garantindo que `uv run --frozen mkdocs build --strict` passe sem alertas.

## Registro de Decisões

| Identificador | Título | Status | Data |
| --- | --- | --- | --- |
| [ADR-001](adr-001-maquina-estados-e-abstencao.md) | Máquina explícita de 4 estados e motor de aplicabilidade antes da detecção | Proposto (Design inicial) | 2026-11-13 |
| [ADR-002](adr-002-dupla-fonte-concordante.md) | Dupla fonte concordante (HTML + PDF do DOU) para achados tipográficos | Proposto (Design inicial) | 2026-11-13 |
| [ADR-003](adr-003-banco-unico-postgres-e-ollama-offline.md) | Banco único PostgreSQL 17 e inferência local offline via Ollama | Proposto (Design inicial) | 2026-11-13 |

> **Nota de status:** As ADRs iniciais refletem o desenho arquitetural consolidado no `README.md` na etapa de setup de documentação e entram em vigência operacional à medida que os módulos correspondentes forem implementados.
