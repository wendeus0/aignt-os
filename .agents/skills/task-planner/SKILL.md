---
name: task-planner
description: Use esta skill quando a feature tiver 3 ou mais passos independentes e for necessário decompor os critérios de aceite em tasks atômicas rastreáveis via TaskCreate/TaskUpdate/TaskList. Não use para hotfixes simples nem para substituir `session-primer`.
---

# Objetivo

Decompor os critérios de aceite de uma SPEC em tasks atômicas, criar essas tasks com `TaskCreate`, e manter o status de cada uma atualizado (`pending → in_progress → completed`) durante a execução.

# Quando esta skill deve ser usada

Use esta skill quando:

- a feature tiver 3 ou mais passos independentes ou sequencialmente dependentes
- a sessão for longa e a perda de contexto entre mensagens for um risco real
- o usuário pedir explicitamente um plano de execução rastreável
- `test-red` ou `green-refactor` precisarem coordenar múltiplos arquivos em ordem

# Quando esta skill NÃO deve ser usada

Não use esta skill para:

- hotfixes ou mudanças diretas de 1–2 arquivos (custo de overhead supera o benefício)
- substituir `session-primer` como orientação inicial da sessão
- substituir `technical-triage` como priorização de backlog
- rastrear tasks de outras features simultaneamente (trabalhe uma feature por vez)

# Restrições obrigatórias

- Crie tasks apenas para a feature ativa no momento.
- Nunca misture tasks de features diferentes na mesma sessão.
- Cada task deve ser atômica: um único critério de aceite ou um único arquivo-alvo.
- Mantenha o status sempre atualizado — uma task nunca deve ficar em `in_progress` por mais de uma mensagem sem atualização.
- Ao final da feature, marque todas as tasks como `completed` ou registre as que ficaram abertas em `PENDING_LOG.md`.

# Processo

## 1. Ler a SPEC

Leia `features/<feature>/SPEC.md` e extraia:
- lista de critérios de aceite (`acceptance_criteria`)
- dependências entre critérios (se A deve preceder B)
- fora de escopo (`non_goals`) — nunca crie task para itens fora de escopo

## 2. Decompor em tasks atômicas

Para cada critério de aceite, crie uma task descrevendo:
- o que deve ser feito (ação concreta)
- o arquivo ou módulo alvo, se identificável
- o critério de aceite que a task satisfaz

Agrupe critérios trivialmente relacionados em uma única task se fizerem sentido juntos (ex.: criar arquivo + adicionar import).

## 3. Criar tasks com TaskCreate

Use a ferramenta `TaskCreate` para cada task. Campos obrigatórios:
- `name`: descrição curta e acionável (ex.: "Escrever teste RED para CancellationToken")
- `description`: critério de aceite da SPEC que esta task satisfaz
- Status inicial: `pending`

## 4. Apresentar o plano ao usuário

Liste as tasks criadas com IDs e status. Aguarde confirmação antes de iniciar execução.

## 5. Executar e manter status

Durante a execução da feature (em conjunto com `test-red`, `green-refactor` etc.):

- Antes de iniciar uma task: `TaskUpdate` → `in_progress`
- Ao concluir uma task: `TaskUpdate` → `completed`
- Se uma task for bloqueada: registre o bloqueio na descrição e marque como `pending` novamente com nota

## 6. Encerrar o plano

Ao final:
1. Liste todas as tasks com status final via `TaskList`.
2. Tasks `completed`: confirmadas.
3. Tasks `pending` ou `in_progress` remanescentes: registre em `PENDING_LOG.md`.

# Saída final esperada

Entregue:

1. Lista de tasks criadas (ID, nome, status)
2. Sequência de execução recomendada
3. Dependências explícitas entre tasks, se houver
4. Próxima skill a invocar para iniciar execução (geralmente `test-red`)
