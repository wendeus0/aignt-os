# ADR-013 — Adicionar QUALITY_GATE como passo formal no fluxo oficial

## Status
Aceito

## Contexto
O `AGENTS.md` foi atualizado para introduzir a skill `quality-gate` como passo obrigatório entre `REFACTOR` e `SECURITY_REVIEW` no fluxo oficial do projeto. Antes dessa atualização, o fluxo era:

```text
SPEC → TEST_RED → CODE_GREEN → REFACTOR → SECURITY_REVIEW → REPORT → COMMIT
```

O projeto já realizava validações automatizadas (testes, lint, typecheck) de forma informal durante o `REFACTOR` ou como parte da revisão de código. No entanto, esse passo não estava formalizado como estágio explícito da esteira, nem como estado rastreável na state machine.

## Decisão
Adicionar `QUALITY_GATE` como passo formal no fluxo oficial entre `REFACTOR` e `SECURITY_REVIEW`:

```text
SPEC → TEST_RED → CODE_GREEN → REFACTOR → QUALITY_GATE → SECURITY_REVIEW → REPORT → COMMIT
```

Regras derivadas:
- `QUALITY_GATE` é um gate **automatizado**: valida testes passando, lint sem erros, typecheck limpo e regressão funcional.
- `QUALITY_GATE` não substitui o `SECURITY_REVIEW`; ambos são gates obrigatórios e sequenciais.
- Na state machine interna, `QUALITY_GATE` é um estado rastreável entre `CODE_GREEN` e `REVIEW`.
- A skill `quality-gate` é responsável por este passo; é distinta da skill `security-review`.
- O passo `QUALITY_GATE` deve ser implementado como chore dedicada, seguindo o fluxo oficial com SPEC → TEST_RED → CODE_GREEN.

## Consequências

### Positivas
- Torna explícito e auditável o gate de qualidade técnica antes do gate de segurança.
- Reduz risco de aprovação de código com regressão funcional ou problemas de lint/typecheck.
- Alinha a documentação de arquitetura com o `AGENTS.md` atualizado.
- Permite observabilidade do estado `QUALITY_GATE` na state machine por run.

### Negativas
- Adiciona um novo estado à state machine, exigindo atualização da implementação em `state_machine.py`.
- Aumenta ligeiramente o número de steps na esteira, mas mantém a esteira linear.
- Exige chore dedicada para não introduzir mudança de código sem SPEC e testes.

## Alternativas consideradas
- Manter `QUALITY_GATE` como passo implícito dentro de `REFACTOR`: descartado porque invisibiliza o gate e impede rastreabilidade por run.
- Fundir `QUALITY_GATE` com `SECURITY_REVIEW` em um único passo: descartado porque as responsabilidades são distintas — qualidade técnica vs. riscos de segurança.
- Não implementar o estado na state machine no MVP: possível como estado pós-MVP, mas inconsistente com o fluxo oficial documentado.

## Relação com ADRs existentes
- ADR-003 (state-machine-pipeline-engine): este ADR estende o modelo de estados do MVP.
- ADR-008 (spec-driven-development): o `QUALITY_GATE` reforça o princípio de gates explícitos na esteira.
