# Auditor 12.002

> **Aviso de independência:** Este é um projeto independente de código aberto, desenvolvido exclusivamente sobre dados públicos oficiais (Diário Oficial da União, Câmara dos Deputados e Portal da Legislação). Não possui vínculo institucional, patrocínio ou endosso da Casa Civil, da Secretaria Especial para Assuntos Jurídicos (SAJ) ou da Universidade de Brasília (UnB).

Assistente auditável de revisão de técnica legislativa sob o **Decreto nº 12.002/2024**, projetado para identificar achados verificáveis em atos normativos federais, explicitar exceções legais e abster-se automaticamente quando não dispõe de evidência íntegra suficiente.

---

## O que é (e o que não é)

* **O que faz:** avalia atos normativos publicados frente a 6 regras objetivas do Decreto nº 12.002/2024, classificando cada par `(ato, regra)` em uma máquina de estados explícita:
  * `CONFORME`: regra aplicável e atendida na evidência extraída;
  * `ACHADO`: ocorrência verificada de técnica legislativa com trecho literal ancorado por offset e hash;
  * `NAO_APLICAVEL`: regra fora do escopo do ato ou coberta por exceção legal explícita;
  * `NAO_AVALIAVEL`: abstenção obrigatória por limitação de extração, divergência entre fontes ou ausência de suporte verificável.
* **O que não faz (Art. 76):** não emite juízo de legalidade, validade ou constitucionalidade. Nos termos do art. 76 do Decreto nº 12.002/2024, a inobservância às regras de técnica legislativa **não resulta em invalidade do ato** — as saídas constituem estritamente *achados de técnica legislativa* e *sugestões de adequação* (art. 70, III). Também não avalia mérito político ou "conformidade total".

---

## Arquitetura e Defesas Estruturais

O sistema adota uma arquitetura enxuta de banco único (**PostgreSQL 17**) e execução **100% offline** após o download inicial dos pesos do modelo local:

```mermaid
flowchart LR
  subgraph NAO_CONFIAVEL["Dados não confiáveis (somente leitura)"]
    RAW[data/raw/*: HTML + PDF + XML<br/>SHA-256 no manifesto]
  end
  subgraph DET["Núcleo determinístico"]
    P[Parser hierárquico<br/>art/§/inciso/alínea/blocos citados]
    AV[Detector de avaliabilidade<br/>dupla fonte concordante]
    AP[Motor de aplicabilidade<br/>escopo · pré-condição · exceções]
    CK[Checkers R1–R5]
  end
  subgraph LLM["LLM em quarentena (sem ferramentas, sem rede)"]
    SP[Spotlighting / datamarking]
    MK[Maker R5/R6<br/>JSON Schema · temp 0 · seed 42]
  end
  subgraph VER["Verificação"]
    EV[Integridade byte a byte<br/>+ suporte do predicado]
    RD[Redator<br/>template + explicação]
    VF[Verificador FINAL<br/>sobre o artefato renderizado]
  end
  DB[(PostgreSQL 17<br/>tabelas + views + llm_cache)]
  UI[Streamlit offline]

  RAW --> P --> AV --> AP
  AP -->|aplicável e avaliável| CK
  AP -->|R5 ambíguo / R6| SP --> MK --> EV
  CK --> EV --> DB
  AP -->|NAO_APLICAVEL / NAO_AVALIAVEL| DB
  DB --> RD --> VF
  VF -->|aprovado| UI
  VF -->|reprovado| DB
