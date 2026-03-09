---
name: memory-curator
description: Use esta skill quando a tarefa for consolidar a memória durável do projeto em `memory.md`, registrar o estado atual da frente e gerar handoff de sessão. Não use esta skill para corrigir código, decidir backlog, criar ADR ou substituir o log operacional detalhado.
---

# Objetivo

Manter `memory.md` como memória durável, curta e reaproveitável do projeto, consolidando decisões estáveis, trade-offs, estado atual da frente e próximos passos.

# Escopo

Esta skill:
- lê `AGENTS.md`, `CONTEXT.md`, `memory.md`, `PENDING_LOG.md` e `ERROR_LOG.md`
- atualiza `memory.md` com decisões incorporadas, trade-offs, mudanças estruturais relevantes e estado atual da frente
- consolida pendências abertas sem reabrir debates já encerrados
- gera handoff de sessão quando explicitamente acionada para encerramento

Esta skill não:
- decide backlog sozinha
- substitui `technical-triage`
- substitui `session-logger` no log operacional detalhado
- cria ADR
- abre PR
- corrige código

# Leia antes de agir

Leia nesta ordem:
1. `AGENTS.md`
2. `CONTEXT.md`
3. `memory.md`, se existir
4. `PENDING_LOG.md`, se existir
5. `ERROR_LOG.md`, se existir
6. `git status`
7. `git diff --stat`
8. instrução atual do usuário

# Quando esta skill deve ser usada

Use esta skill quando:
- for necessário consolidar memória durável do projeto
- for necessário atualizar o estado atual de uma frente, branch ou PR em `memory.md`
- for necessário registrar decisões estáveis e trade-offs já aceitos
- for necessário preparar handoff confiável para a próxima sessão

# Convenção operacional de encerramento

Quando o usuário disser exatamente `Vamos encerrar a conversa`, recomenda-se invocar esta skill com texto adicional para acionar o fluxo de fechamento.

Use uma destas chamadas:
- `$memory-curator encerrar conversa`
- `$memory-curator close session`

Importante:
- isso é uma convenção operacional de uso da skill
- isso não é um alias técnico nativo da plataforma

Ao ser chamada nesse modo, esta skill deve:
1. organizar um resumo confiável da sessão
2. atualizar `memory.md`
3. gerar um prompt de handoff para a próxima sessão

# Regras obrigatórias

- Mantenha `memory.md` estável e reaproveitável.
- Não transforme `memory.md` em transcrição de conversa.
- Prefira consolidar em vez de duplicar.
- Registre apenas decisões já tomadas ou estado realmente observado.
- Se houver dúvida de priorização, encaminhe para `technical-triage`.
- Se algo pertencer ao log detalhado da sessão, deixe com `session-logger`.

# Estrutura mínima de `memory.md`

Mantenha estas seções:
- `Current project state`
- `Stable decisions`
- `Active fronts`
- `Open decisions`
- `Recurrent pitfalls`
- `Next recommended steps`
- `Last handoff summary`

# Processo

1. Leia o contexto estável e a memória existente.
2. Identifique o que mudou de forma durável.
3. Atualize `memory.md` sem duplicação desnecessária.
4. Se a chamada for de encerramento, produza também o handoff.
5. Deixe explícito o que continua pendente.

# Saída final esperada

Entregue apenas:
1. arquivos atualizados
2. resumo curto do que entrou em `memory.md`
3. estado atual da frente
4. pendências abertas relevantes
5. prompt de handoff, se a skill tiver sido chamada para encerramento
