---
id: F40-run-cancellation
type: feature
summary: "Comando stop e cancelamento gracioso de runs em execução"
inputs:
  - "Comando CLI: aignt runs stop <run_id>"
outputs:
  - "Mensagem de sucesso na CLI"
  - "Transição de estado da run para 'cancelled'"
  - "Interrupção do step em execução (se houver)"
acceptance_criteria:
  - "Comando stop deve falhar se run não existir"
  - "Comando stop deve falhar se run já estiver terminal (completed/failed/cancelled)"
  - "Runtime deve interceptar sinal de cancelamento e abortar step atual"
  - "Run deve persistir estado final como 'cancelled'"
  - "Logs devem registrar quem solicitou o cancelamento"
non_goals:
  - "Cancelamento de steps atômicos remotos sem suporte a sinal (ex: API calls travadas)"
  - "Rollback de efeitos colaterais (undo)"
  - "Interface TUI para cancelamento (nesta feature é apenas CLI)"
---

## Contexto

Atualmente, uma run iniciada no AIgnt OS só termina quando completa todos os passos ou falha. Não existe mecanismo oficial para interromper uma execução em andamento (exceto matar o processo do runtime via SO, o que pode corromper estado).

A falta de um comando `stop` impede o controle de loops infinitos em agentes, processos travados ou desistência do usuário.

## Objetivo

Implementar o comando `aignt runs stop <run_id>` e a lógica correspondente no `RuntimeService` para:
1. Receber a solicitação de parada.
2. Sinalizar ao `StepExecutor` que deve abortar.
3. Transicionar a run para o estado `cancelled` de forma segura.
