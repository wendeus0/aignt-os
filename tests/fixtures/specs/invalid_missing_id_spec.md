---
type: feature
summary: SPEC sem campo id.
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

Esta SPEC nao tem o campo id no front matter, o que deve causar falha.

# Objetivo

Confirmar que id ausente falha na validacao.
