# Fronteira Jurídica (Art. 76 e Art. 70, III)

> **Estágio:** Diretriz normativa e contratual permanente do projeto, aplicável desde a concepção da documentação e da interface.

O **Auditor 12.002** opera sob limites legais explícitos extraídos do próprio **Decreto nº 12.002/2024**. A clareza terminológica não é cosmética: ela impede que um sistema automatizado de técnica legislativa extrapole sua competência para emitir juízos jurídicos inválidos ou enganosos.

## O limite expresso no Art. 76

Nos termos do **art. 76 do Decreto nº 12.002/2024**, a inobservância às regras de técnica legislativa **não resulta em invalidade do ato normativo**.

Consequentemente, as saídas do Auditor 12.002 constituem estritamente:

- **Achados de técnica legislativa** (com evidência literal ancorada no texto oficial);
- **Sugestões de adequação redacional**, alinhadas ao papel de revisão previsto no **art. 70, III** do decreto.

## O que o sistema pode e não pode afirmar

| Aspecto | Permitido no Auditor 12.002 | Proibido em saídas, prompts e docs |
| --- | --- | --- |
| **Natureza do apontamento** | *"Achado de técnica legislativa relativo ao art. X do Decreto nº 12.002/2024."* | *"Ato ilegal"*, *"norma inválida"*, *"ato nulo"*, *"inconstitucional"*. |
| **Escopo da avaliação** | *"Avaliação restrita às 6 regras do catálogo (`R1@1.0`–`R6@1.0`) sobre a evidência extraída."* | *"Ato 100% conforme"*, *"validado juridicamente"*, *"sem vícios legais"*. |
| **Mérito regulatório** | Não avaliado. | Recomendações sobre conveniência, oportunidade ou mérito político da norma. |
| **Incerteza ou conflito de fonte** | Abstenção explícita como `NAO_AVALIAVEL` com causa declarada. | Inferir `CONFORME` por ausência de detecção ou emitir `ACHADO` sem âncora exata. |

## Exemplo de enquadramento das saídas

!!! achado "Linguagem permitida em um ACHADO"
    Enunciado próprio do ato iniciado por `"Considerando"` no preâmbulo (trecho literal ancorado entre offsets `X` e `Y`, SHA-256 `...`), em desacordo com o art. 4º, § 3º do Decreto nº 12.002/2024 (`R4@1.0`). Trata-se de achado formal de técnica legislativa; nos termos do art. 76 do mesmo decreto, não implica invalidade do ato.

!!! nao-avaliavel "Linguagem permitida em uma abstenção (`NAO_AVALIAVEL`)"
    O trecho correspondente ao dispositivo de alteração apresenta divergência entre a fonte primária (HTML) e o PDF oficial do DOU. O sistema abstém-se de emitir classificação conclusiva para `R3@1.0` por insuficiência de evidência concordante.

## Independência institucional

Este projeto é uma iniciativa independente de código aberto (`verifyLex-org`), construída exclusivamente sobre dados públicos oficiais (Diário Oficial da União, Câmara dos Deputados e Portal da Legislação), nos termos do art. 8º, IV, da Lei nº 9.610/1998. Não possui vínculo institucional, patrocínio ou endosso da Casa Civil da Presidência da República, da Secretaria Especial para Assuntos Jurídicos (SAJ) ou da Universidade de Brasília (UnB).
