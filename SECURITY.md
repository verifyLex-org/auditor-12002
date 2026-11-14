# Política de Segurança — Auditor 12.002

## 1. Versões e Branches Suportadas

| Referência | Suporte de segurança |
| --- | --- |
| `main` | Suportada continuamente |
| Branches de desenvolvimento (`feat/*`, `fix/*`, `docs/*`, `sec/*`) | Correções aplicadas via Pull Request antes do merge na `main` |

## 2. Como Reportar uma Vulnerabilidade

**Não abra issues públicas para relatar falhas de segurança.**

Utilize o canal privado de **GitHub Security Advisories** do repositório:

- [Reportar vulnerabilidade de forma privada](https://github.com/verifyLex-org/auditor-12002/security/advisories/new)

Inclua no relato, sempre que possível:

1. Descrição técnica da falha e superfície afetada (ex.: `parser/`, `llm/`, `verify/`, `sql/`, `docs_hooks/`, workflows de CI).
2. Passos ou entrada mínima para reprodução (se envolver *prompt injection* indireto, inclua o trecho sanitizado e a regra `R1`–`R6` impactada).
3. Impacto observado em relação aos invariantes do sistema (ex.: emissão indevida de `CONFORME`/`ACHADO`, contorno de `NAO_AVALIAVEL`, acesso de rede externo ou exposição de dados).

## 3. Prazos de Resposta (Coordenação)

- **Confirmação de recebimento e triagem inicial:** até **3 dias úteis**.
- **Avaliação de severidade e plano de mitigação:** até **7 dias úteis**.
- **Publicação de correção:** priorizada em branch `sec/<issue>-<tema>` com teste de regressão em `tests/security/` antes da divulgação pública.

## 4. Escopo Prioritário do Projeto

- **Execução 100% offline e quarentena do LLM:** qualquer caminho que permita ao serviço Ollama (`qwen3:8b`) ou ao portal estático (`site/`) realizar requisições externas não previstas.
- **Contorno de *prompt injection* e verificação:** entradas textuais que induzam saída fora do JSON Schema, citação byte a byte inexistente sem rebaixamento para `NAO_AVALIAVEL` ou violação da fronteira do Art. 76 do Decreto nº 12.002/2024.
- **Integridade do corpus e gabarito:** bypass na verificação `MANIFEST.sha256` ou adulteração silenciosa de relatórios recalculados em SQL.
- **Segurança da cadeia de suprimentos (CI/CD):** permissões excessivas em workflows, actions não pinadas por SHA completo ou exposição de segredos.

## 5. Fora de Escopo

- Conteúdo público de atos normativos federais armazenados em `data/raw/` (atos oficiais nos termos do art. 8º, IV, da Lei nº 9.610/1998).
- Ataques que exijam acesso físico ou administrativo prévio à estação local já comprometida fora dos containers isolados.
