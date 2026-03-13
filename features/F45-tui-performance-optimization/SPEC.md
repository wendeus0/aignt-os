---
id: F45-tui-performance-optimization
type: feature
summary: "Otimização de renderização da TUI para logs massivos e listas longas"
inputs:
  - Limite de buffer de logs em `AppSettings`
outputs:
  - Renderização paginada ou truncada de logs
  - TUI responsiva mesmo com milhares de linhas de log
acceptance_criteria:
  - "Configuração `tui_log_buffer_lines` (default: 1000)"
  - "`runs follow` e `watch` devem truncar logs antigos para manter performance"
  - "Mensagem indicando truncamento ('... N lines truncated ...')"
  - "Testes unitários validando a lógica de truncamento"
non_goals:
  - Implementar scroll infinito virtualizado complexo
  - Alterar backend de persistência de logs
---

# Contexto

A interface de terminal (TUI/CLI) utiliza a biblioteca `rich` para renderização. Em execuções longas (long-running tasks) ou com output verboso, o buffer de logs pode crescer indefinidamente, causando lentidão na renderização, flicker e alto consumo de memória no cliente CLI.

# Objetivo

Implementar limites configuráveis para a exibição de logs na CLI (`runs follow` e `watch`), garantindo que apenas as linhas mais recentes (buffer circular ou truncamento) sejam renderizadas, preservando a responsividade da ferramenta.
