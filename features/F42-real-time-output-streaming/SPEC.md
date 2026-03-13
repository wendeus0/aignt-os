---
id: F42-real-time-output-streaming
type: feature
summary: "Suporte a streaming de logs em tempo real na CLI e TUI"
inputs:
  - "Comando `runs follow <run_id>`"
  - "Visualização de dashboard em execução"
outputs:
  - "Fluxo contínuo de logs de stdout/stderr na CLI"
  - "Atualização automática de logs na TUI sem refresh manual"
acceptance_criteria:
  - "Deve permitir acompanhar logs de uma run em execução via `runs follow`"
  - "Deve encerrar o stream quando a run terminar"
  - "Deve suportar interrupção via Ctrl+C sem cancelar a run"
  - "Deve atualizar logs na TUI automaticamente quando novos dados forem escritos"
non_goals:
  - "Streaming via WebSocket para clientes remotos (MVP foca em local)"
  - "Streaming de artefatos binários"
---

# Contexto

Atualmente, para ver o progresso de uma run, o usuário precisa rodar `runs show` ou `runs logs` repetidamente, ou usar o dashboard que tem um refresh interval fixo. Não há uma maneira nativa de fazer "tail -f" nos logs da run via CLI.

# Objetivo

Implementar o comando `runs follow` na CLI que se comporta como um `tail -f` para os logs da run, e melhorar a TUI para atualizar logs em tempo real (ou próximo disso) de forma eficiente.
