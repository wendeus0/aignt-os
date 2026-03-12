---
id: chore-quality-gate-state
type: chore
summary: Adicionar estado QUALITY_GATE à state machine entre CODE_GREEN e REVIEW
inputs:
  - ADR-013 aceito
  - AGENTS.md atualizado com quality-gate como passo formal
  - Fluxo oficial atualizado em CONTEXT.md, SDD.md e TDD.md
outputs:
  - LINEAR_STATE_FLOW com QUALITY_GATE entre CODE_GREEN e REVIEW
  - Transições de state machine atualizadas
  - Testes cobrindo transição CODE_GREEN → QUALITY_GATE → REVIEW
  - Testes cobrindo impossibilidade de pular QUALITY_GATE direto para REVIEW/SECURITY
acceptance_criteria:
  - LINEAR_STATE_FLOW inclui QUALITY_GATE entre CODE_GREEN e REVIEW
  - A state machine aceita a transição CODE_GREEN → QUALITY_GATE
  - A state machine aceita a transição QUALITY_GATE → REVIEW
  - A state machine rejeita a transição CODE_GREEN → REVIEW (deve passar por QUALITY_GATE)
  - A state machine rejeita a transição CODE_GREEN → SECURITY (deve passar por QUALITY_GATE e REVIEW)
  - test_state_machine_follows_minimal_happy_path_to_complete() continua passando com a nova sequência
  - Todos os testes existentes de state machine seguem verdes
  - A chore não altera comportamento de outros módulos além de state_machine.py e seus testes
non_goals:
  - Implementar a lógica do executor de QUALITY_GATE (somente estado e transições)
  - Alterar pipeline.py, supervisor.py ou adapters
  - Criar novos fixtures além dos de state machine
  - Abrir feature de produto adicional
---

# Contexto

O `AGENTS.md` foi atualizado para incluir `QUALITY_GATE` como passo formal entre `REFACTOR` e `SECURITY_REVIEW`. O ADR-013 formalizou a decisão. Os documentos centrais (CONTEXT.md, SDD.md, TDD.md) foram atualizados.

O único artefato de código ainda não atualizado é a `LINEAR_STATE_FLOW` em `src/aignt_os/state_machine.py`, que atualmente define:

```python
LINEAR_STATE_FLOW: tuple[str, ...] = (
    "REQUEST", "SPEC_DISCOVERY", "SPEC_NORMALIZATION", "SPEC_VALIDATION",
    "PLAN", "TEST_RED", "CODE_GREEN", "REVIEW", "SECURITY", "DOCUMENT", "COMPLETE",
)
```

# Objetivo

Adicionar `"QUALITY_GATE"` à `LINEAR_STATE_FLOW` entre `"CODE_GREEN"` e `"REVIEW"`, atualizar os testes de state machine para cobrir as novas transições e garantir que nenhum teste existente quebre.

# Escopo

## Incluído
- Edição de `src/aignt_os/state_machine.py`: inserir `"QUALITY_GATE"` em `LINEAR_STATE_FLOW`
- Edição de `tests/unit/test_state_machine.py`: adicionar testes de transição para `QUALITY_GATE`

## Fora de escopo
- Implementação do executor de QUALITY_GATE no pipeline
- Mudanças em supervisor.py, pipeline.py, persistence.py ou adapters
- Novos ADRs além do ADR-013 já criado
- Documentação além das já atualizadas nesta chore
