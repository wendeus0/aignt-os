---
id: F02-missing-objetivo
type: feature
summary: SPEC com Contexto mas sem Objetivo.
inputs:
  - raw_request
outputs:
  - validated_spec
acceptance_criteria:
  - must validate
non_goals:
  - nothing
---

# Contexto

Esta SPEC tem a secao Contexto preenchida mas nao tem a secao Objetivo.
A validacao deve falhar exigindo a secao Objetivo.
