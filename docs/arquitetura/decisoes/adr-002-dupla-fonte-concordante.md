# ADR-002 — Dupla Fonte Concordante para Achados Tipográficos

| Campo | Valor |
| --- | --- |
| **Status** | Proposto (Design inicial) |
| **Data** | 2026-11-13 |
| **Autores** | Equipe verifyLex-org |
| **Regra / Invariante afetada** | `R3@1.0`, `R5@1.0`, Detector de avaliabilidade (`parser/`) |

## 1. Contexto

Publicações oficiais de atos normativos em portais HTML ocasionalmente apresentam discrepâncias de codificação tipográfica frente ao texto diagramado no Diário Oficial da União (PDF), especialmente em marcadores ordinais (`º` vs. `.` ou `o`), pontuação após `Art. 10.` e abertura/fechamento de aspas em blocos de alteração (`R3` e `R5`). Emitir um `ACHADO` com base em um artefato HTML degradado produziria falsos positivos imputáveis à conversão do portal e não à técnica legislativa do ato.

## 2. Opções Consideradas

### Opção 1: Fonte única (apenas HTML ou apenas PDF)

- Extrair somente a versão HTML (mais limpa para parsing) ou somente o PDF do DOU.
- **Vantagens:** pipeline de extração mais simples e menor volume de armazenamento em `data/raw/`.
- **Desvantagens:** erros de formatação do portal HTML ou ruídos de quebra de linha/coluna no PDF convertem-se diretamente em falsos positivos de técnica legislativa.

### Opção 2: Dupla fonte concordante (HTML + PDF oficial do DOU) (Escolhida)

- Armazenar fonte primária (`HTML`) e conferência oficial (`PDF` do DOU) por ato em `data/raw/{ato_id}/` e exigir confirmação simultânea nas duas fontes para regras sensíveis a tipografia/aspas.
- **Vantagens:** elimina falsos positivos originados por artefato de publicação ou extração; força abstenção auditável (`NAO_AVALIAVEL`) quando as fontes divergem.
- **Desvantagens:** aumenta a complexidade do `parser/` (alinhamento entre duas representações) e exige coleta conjunta de HTML e PDF no corpus.

## 3. Decisão Adotada

Regras sensíveis à tipografia e delimitação de aspas (notadamente `R3@1.0` e `R5@1.0`) só podem emitir `ACHADO` quando a ocorrência for **confirmada simultaneamente** na fonte primária (HTML) e na conferência oficial (PDF do DOU). Havendo divergência relevante entre as duas fontes na unidade auditada, o detector de avaliabilidade deve encerrar o par como `NAO_AVALIAVEL`.

## 4. Consequências e Trade-offs

- **Positivas:** alta precisão nas ocorrências reportadas como `ACHADO` e evidência auditável ancorada por hash de ambos os arquivos originais no `manifesto.csv`.
- **Negativas e riscos:** redução intencional de cobertura automática em atos cuja extração PDF apresente desalinhamento estrutural.
- **Mitigação:** acompanhamento explícito da métrica de **cobertura** ao lado de **precisão** e **risco seletivo** no protocolo experimental.

## 5. Verificação e Auditoria

- O inventário `data/manifesto.csv` registrará os arquivos e respectivos hashes SHA-256 de HTML, PDF e XML (quando disponível) por `ato_id`.
- A suíte planejada de testes (`tests/`) incluirá casos sintéticos de divergência HTML vs. PDF validando a transição obrigatória para `NAO_AVALIAVEL`.
