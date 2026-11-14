# Segurança e Governança

!!! info "Estágio neste repositório"
    Modelo de ameaças e governança documentados. A bateria de testes de segurança (`tests/security`) e os controles em `llm/` e `verify/{evidence,terminology}.py` ainda não foram implementados.

O Auditor 12.002 trata o texto legislativo como **dado não confiável**, mesmo quando vem de fonte oficial. Esta seção descreve as ameaças, os controles e as regras de contribuição.

## Mapa da seção

| Documento | Conteúdo |
| --- | --- |
| [Threat Model](threat-model.md) | Ativos, fronteiras de confiança e matriz `TM-01` a `TM-07`. |
| [FinOps e hardware](FINOPS.md) | Custos operacionais offline e requisitos de hardware. |
| [Contribuir](../operacao/contribuir.md) | Regras inegociáveis, branches, commits e revisão. |
| [Política de segurança](https://github.com/verifyLex-org/auditor-12002/blob/main/SECURITY.md) | Como reportar vulnerabilidades (`SECURITY.md` na raiz). |

## Controles centrais

!!! abstract "Quatro defesas"
    1. **Motor de aplicabilidade antes da detecção:** exceções legais não chegam ao checker nem ao modelo.
    2. **Dupla fonte concordante:** `ACHADO` tipográfico exige HTML e PDF do DOU de acordo.
    3. **LLM em quarentena:** modelo sem ferramentas, em rede Docker `internal: true`, com texto marcado por *spotlighting/datamarking*.
    4. **Verificação matemática:** toda citação é checada byte a byte e todo número é recomputado por views SQL.

!!! warning "Freio de congelamento"
    O CI bloqueia alterações no corpus e no gabarito somente depois que `data/MANIFEST.sha256` for preenchido. Antes disso, a guarda apenas emite aviso. `PREREGISTRO.md` também gera aviso, não bloqueio.
