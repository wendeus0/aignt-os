---
id: F02-h2-sections
type: feature
summary: SPEC com secoes em H2 em vez de H1.
inputs:
  - raw_request
outputs:
  - validated_spec
acceptance_criteria:
  - must validate
non_goals:
  - nothing
---

## Contexto

Esta SPEC usa H2 (##) para as secoes em vez de H1 (#).
O parser so reconhece H1, entao Contexto e Objetivo nao serao detectados.

## Objetivo

Esta secao tambem usa H2 e nao sera detectada.
