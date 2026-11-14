# Dados, Modelos e Pesquisa

> **Estágio:** Documentação de desenho. Nenhum resultado experimental foi produzido; as tabelas de resultados permanecem pendentes até o congelamento do gabarito.

Esta seção responde a três perguntas de pesquisa reproduzível: **sobre quais dados** o sistema foi avaliado, **com qual modelo** e **sob qual protocolo** as condições foram comparadas.

## Mapa da seção

| Documento | Pergunta que responde | Status |
| --- | --- | --- |
| [Data Card](DATA_CARD.md) | Qual é o corpus, como foi estratificado e como sua integridade é verificada? | Especificado |
| [Model Card](MODEL_CARD.md) | Qual modelo local é usado, com quais parâmetros e limites? | Especificado |
| [Protocolo D/A/B/C](protocolo-experimental.md) | Como as condições são comparadas e quais métricas contam? | Pré-registrado; execução pendente |

## Princípios de rigor

!!! abstract "Regras do protocolo"
    - **Pré-registro antes da coleta:** o protocolo está no `PREREGISTRO.md`, que é tratado como congelado.
    - **Corpus fechado:** o conjunto de atos e o gabarito `gold-v1` são fixados por manifesto SHA-256 antes da execução.
    - **Métricas com incerteza:** precisão e acurácia vêm com intervalos de confiança; comparações usam McNemar com agrupamento por ato.
    - **Cobertura junto com precisão:** o sistema pode abster-se. Sem a métrica de cobertura, uma precisão alta não significa nada.

!!! warning "Sem resultados ainda"
    As métricas ainda não foram calculadas. Não cite números deste portal como resultados até que o `make reproduce` gere a tabela correspondente.
