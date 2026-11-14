# Data Card — Corpus Fechado do Auditor 12.002

!!! info "Estágio neste repositório"
    Especificação do corpus fechado conforme `README.md` e `PREREGISTRO.md`. Os arquivos em `data/raw/`, `data/manifesto.csv`, `data/MANIFEST.sha256` e `data/gold/gold-v1.csv` ainda serão coletados, anotados e congelados.

## 1. Visão Geral do Conjunto de Dados

- **Nome planejado:** Corpus Fechado `Auditor 12.002` (`gold-v1`)
- **Escopo temporal:** atos normativos federais publicados após **01/06/2024** (início de vigência do Decreto nº 12.002/2024, art. 78).
- **Escopo institucional:** administração pública federal direta, autárquica e fundacional (art. 2º do Decreto nº 12.002/2024).
- **Tamanho total planejado:** **70 atos normativos federais** (`420` pares `ato × regra` no total):
  - **Desenvolvimento (`dev`):** 10 atos (60 decisões `ato × regra`);
  - **Teste (`test`):** 60 atos (360 decisões `ato × regra`).
- **Conjunto auxiliar sintético:** **120 mutações sintéticas controladas** (20 por regra, `R1` a `R6`) destinadas exclusivamente à medição de *recall* em defeitos de baixa prevalência natural.

## 2. Estratificação do Conjunto de Teste (60 atos)

| Categoria normativa | Quantidade prevista | Relevância experimental |
| --- | ---: | --- |
| Decretos numerados | 12 | Baseline de alta revisão formal; testa precisão e baixa taxa de falso positivo |
| Decretos de promulgação de atos internacionais | 3 | Caso crítico de exceção explícita em `R4` (vedação de `"considerando"`) |
| Portarias ministeriais | 18 | Variedade de atos originários e alteradores (`R5`, `R6`) |
| Portarias e instruções normativas de autarquias e fundações | 20 | Maior diversidade redacional e de estrutura de vigência/alteração |
| Resoluções de colegiados | 7 | Estruturas específicas de preâmbulo e deliberação |
| **Total do conjunto de teste** | **60** | **360 decisões `ato × regra`** |

## 3. Fontes, Proveniência e Licença

- **Fontes públicas oficiais:**
  - Diário Oficial da União (DOU — PDF oficial de conferência e HTML);
  - Câmara dos Deputados (legislação compilada / HTML / XML quando disponível);
  - Portal da Legislação (Presidência da República).
- **Estrutura prevista por ato (`data/raw/{ato_id}/`):**
  - Fonte primária (`HTML`);
  - Conferência oficial (`PDF` do DOU);
  - `XML` (quando disponível na origem);
  - Metadados de proveniência (URL, data de coleta, tipo de ato, órgão emissor).
- **Regime de direitos autorais:** os textos de atos oficiais públicos não são objeto de proteção de direito autoral nos termos do **art. 8º, IV, da Lei nº 9.610/1998**.

## 4. Integridade Criptográfica e Congelamento

- Cada arquivo em `data/raw/` terá seu hash `SHA-256` inventariado em `data/manifesto.csv`.
- O arquivo `data/MANIFEST.sha256` consolidará o hash mestre do corpus.
- O gabarito anotado em `data/gold/gold-v1.csv` será produzido por **anotação dupla-cega** seguindo o guia em `data/gold/`, com registro do **κ de Cohen por regra antes da adjudicação** e resolução posterior de divergências.
- Após o congelamento de `gold-v1.csv` e do manifesto, Pull Requests que alterem esses arquivos devem ser bloqueados automaticamente no CI.

## 5. Riscos, Vieses e Limitações Declaradas

1. **Proxy público pós-publicação:** a avaliação incide sobre atos já publicados (que já passaram por revisão editorial prévia), e não sobre minutas internas em fase de elaboração.
2. **Baixa prevalência natural em decretos:** decretos revisados tendem a apresentar poucos erros formais, gerando intervalos de confiança amplos em amostras de 60 atos; por isso o *recall* é avaliado separadamente nas 120 mutações sintéticas, **sem extrapolar prevalência real a partir das mutações**.
3. **Risco de *prompt injection* indireto:** embora sejam fontes públicas oficiais, os textos em `data/raw/` são tratados arquiteturalmente como dados não confiáveis (somente leitura) para validar as defesas do sistema.
