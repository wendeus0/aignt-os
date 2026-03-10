---
name: memory-curator
description: Use esta skill quando a tarefa for consolidar a memória durável do projeto em `memory.md`, registrar o estado atual da frente e gerar handoff de sessão. Não use esta skill para corrigir código, decidir backlog, criar ADR ou substituir o log operacional detalhado.
---

# Objetivo

Manter `memory.md` como memória durável, curta e reaproveitável do projeto.

O foco é consolidar:
- estado global do projeto
- snapshot local apenas quando ele afeta a próxima sessão
- frentes ativas
- decisões estáveis
- pendências abertas
- próximos passos recomendados
- último handoff

# Escopo

Esta skill:
- lê `AGENTS.md`, `CONTEXT.md`, `memory.md`, `PENDING_LOG.md` e `ERROR_LOG.md`
- usa `git status` e `git diff --stat` para captar apenas o snapshot local relevante
- atualiza `memory.md` sem virar log de conversa
- consolida decisões já aceitas e pendências ainda abertas
- gera handoff de encerramento quando explicitamente acionada

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
- for necessário atualizar o estado atual de uma frente em `memory.md`
- for necessário registrar decisões estáveis e trade-offs já aceitos
- for necessário preparar handoff confiável para a próxima sessão

# Convenção operacional de encerramento

Use explicitamente uma destas chamadas:
- `$memory-curator encerrar conversa`
- `$memory-curator close session`

Importante:
- isso é uma convenção operacional de uso da skill
- isso não é um alias técnico nativo da plataforma

Ao ser chamada nesse modo, esta skill deve obrigatoriamente:
1. atualizar `memory.md`
2. consolidar o snapshot local apenas se ele alterar a próxima sessão
3. gerar um prompt de handoff semelhante ao prompt de abertura em pair programming

# Regras obrigatórias

- `memory.md` deve funcionar como memória durável do projeto, não como log de conversa.
- Detalhe operacional da sessão fica em `PENDING_LOG.md` e `ERROR_LOG.md`.
- Separe explicitamente estado global do projeto e snapshot local, quando houver snapshot relevante.
- Registre em `Stable decisions` apenas decisões já adotadas pelo projeto.
- Não promova detalhe frágil de ambiente a decisão estável sem adoção formal.
- `Active fronts` deve listar apenas frentes em andamento ou recém-concluídas que ainda moldam o próximo passo.
- `Open decisions` deve listar dúvidas reais ainda abertas, não backlog genérico.
- `Next recommended steps` deve ser curto, finito e acionável.
- `Last handoff summary` deve ser curto, reutilizável e orientado à próxima sessão.
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

Dentro de `Current project state`, separe:
- estado global do projeto
- snapshot local relevante, quando existir

# Processo

1. Leia o contexto estável e a memória existente.
2. Classifique cada informação como:
   - memória durável
   - snapshot local relevante
   - detalhe operacional que deve ficar fora de `memory.md`
3. Atualize `memory.md` sem duplicação desnecessária.
4. Se a chamada for de encerramento, gere também o handoff.
5. Deixe explícito o que continua pendente.

# Formato do handoff de encerramento

O handoff deve manter o espírito de um prompt de pair programming para retomada.

Use este formato curto:
- `Read before acting`
- `Current state`
- `Open points`
- `Recommended next front`

Regras do handoff:
- mandar a próxima sessão reler o contexto persistente
- resumir o estado atual em poucas linhas
- apontar pendências que realmente afetam a retomada
- recomendar uma única frente principal para começar
- não copiar a conversa
- não virar checklist infinito

# Saída final esperada

Entregue apenas:
1. arquivos atualizados
2. resumo curto do que entrou em `memory.md`
3. estado atual da frente
4. pendências abertas relevantes
5. prompt de handoff, se a skill tiver sido chamada para encerramento
