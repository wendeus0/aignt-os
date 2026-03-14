# SPEC Format — SynapseOS

## Decisão
O formato oficial da SPEC no MVP é **Markdown estruturado com front matter YAML obrigatório**.

O template oficial está em [`docs/architecture/SPEC_TEMPLATE_v2.md`](./SPEC_TEMPLATE_v2.md).

## Por que não apenas JSON/YAML?
### Vantagens de schema formal puro
- validação forte,
- menos ambiguidade,
- contratos claros.

### Desvantagens
- pior legibilidade humana,
- menos contexto narrativo,
- maior rigidez para tarefas exploratórias.

## Por que não apenas Markdown livre?
### Vantagens
- ótima leitura humana,
- boa interpretação por IA.

### Desvantagens
- ambiguidade alta,
- parsing menos previsível,
- validação mais fraca.

## Modelo adotado
- YAML obrigatório para campos estruturais.
- Markdown obrigatório para contexto e nuances.
- Validação com Pydantic e JSON Schema.

## Campos mínimos obrigatórios no YAML

| Campo | Regra |
|---|---|
| `id` | String única no formato `F<NN>-<slug>` (ex: `F03-state-machine-mvp`) |
| `type` | Um dos valores: `feature`, `fix`, `refactor`, `chore` |
| `summary` | String não-vazia, descrição em uma linha |
| `inputs` | Lista não-vazia de entradas |
| `outputs` | Lista não-vazia de saídas esperadas |
| `acceptance_criteria` | Lista não-vazia — cada item deve ser verificável por teste |
| `non_goals` | Lista obrigatória — aceita vazia (`[]`), mas deve existir |

> **Assimetria intencional**: `acceptance_criteria` exige ao menos um item (sem ela não há como validar a feature). `non_goals` aceita lista vazia, mas o campo deve estar presente para confirmar que o escopo foi considerado explicitamente.

## Seções obrigatórias no corpo da SPEC

As seções `Contexto` e `Objetivo` são obrigatórias e devem ser escritas como **headings H1**:

```markdown
# Contexto

# Objetivo
```

> **Regra crítica**: o parser reconhece apenas `# ` (H1). Headings `## ` (H2) são ignorados pelo validator. Uma SPEC com `## Contexto` ou `## Objetivo` falhará em `SPEC_VALIDATION` como se as seções não existissem.

## Regras de validação
- Sem YAML válido, a SPEC não passa de `SPEC_VALIDATION`.
- `acceptance_criteria` deve conter pelo menos um item.
- `non_goals` deve existir como campo, podendo ser lista vazia.
- O corpo deve ter seções `# Contexto` e `# Objetivo` como headings H1.
- O campo `type` deve ser um dos valores válidos: `feature`, `fix`, `refactor`, `chore`.

## Testes de integração nos acceptance_criteria

Features que envolvem I/O real, persistência, lifecycle de runtime ou comportamento de CLI pública devem incluir pelo menos um critério de aceite verificável **somente via teste de integração** — não apenas via teste unitário.

Exemplos de features que exigem critério de integração:
- persistência em SQLite ou filesystem
- lifecycle do runtime (start, stop, status via CLI)
- comportamento de adapter com subprocesso real
- interação entre módulos via entrypoint público

## Ciclo de vida da SPEC

O ciclo de vida da SPEC **não é rastreado via campo no front matter no MVP**. O estado da feature é inferido pelo estágio do fluxo oficial (`SPEC → TEST_RED → CODE_GREEN → REFACTOR → SECURITY_REVIEW → REPORT → COMMIT`). Rastreamento de lifecycle (ex: `draft`, `approved`, `implemented`) é responsabilidade do processo de feature, não da SPEC em si.

## Relação com a esteira
- `SPEC_DISCOVERY` cria rascunho.
- `SPEC_NORMALIZATION` ajusta para formato oficial.
- `SPEC_VALIDATION` valida schema e seções obrigatórias.
- `PLAN` consome somente SPEC validada.
