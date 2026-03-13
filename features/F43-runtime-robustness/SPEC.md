---
id: F43-runtime-robustness
type: feature
summary: "Timeouts granulares por step e políticas de retry para falhas transientes"
inputs:
  - "Configuração global `execution_timeout_seconds`"
  - "Configuração global `max_retries`"
  - "SPEC metadata para override por step (future)"
outputs:
  - "Interrupção forçada de steps que excedem o timeout"
  - "Retry automático para falhas não-terminais (ex: rede, lock)"
  - "Status `timed_out` explícito em `RunStepRecord`"
acceptance_criteria:
  - "Deve interromper um step se ele exceder o tempo limite configurado"
  - "Deve registrar o status `timed_out` no banco de dados"
  - "Deve tentar re-executar steps que falhem com erros recuperáveis até `max_retries` vezes"
  - "Não deve fazer retry em erros de validação de SPEC ou erros fatais conhecidos"
non_goals:
  - "Timeouts dinâmicos baseados em histórico"
  - "Retries complexos com backoff exponencial configurável por step (MVP é global)"
---

# Contexto

Atualmente, se um step travar (ex: loop infinito, dead lock em sub-processo), a run fica presa para sempre como `running`. Além disso, falhas transientes (ex: erro de I/O momentâneo) causam falha imediata da run.

# Objetivo

Implementar um mecanismo de timeout para `StepExecutor` e uma lógica básica de retry no `PipelineEngine` para aumentar a robustez da execução.
