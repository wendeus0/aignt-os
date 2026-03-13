---
id: F36-worker-owner-skip-observability
type: feature
summary: Tornar auditavel quando o worker autenticado pula runs pendentes de outro principal por ownership.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - features/F35-worker-runtime-ownership-filter/SPEC.md
  - src/aignt_os/runtime/worker.py
  - src/aignt_os/persistence.py
  - src/aignt_os/cli/rendering.py
  - tests/unit/test_worker_runtime.py
  - tests/integration/test_worker_runtime_flow.py
  - tests/integration/test_runs_cli.py
outputs:
  - worker_owner_skip_event
  - owner_skip_observability_red_tests
constraints:
  - "manter o AIgnt-Synapse-Flow como a engine propria de pipeline do AIgnt OS"
  - "restringir a frente a observabilidade do skip no worker; sem mudar CLI publica, schema SQLite, socket, IPC ou transporte remoto"
  - "preservar a politica atual de skip e seguir para runs incompatíveis"
  - "nao exigir DOCKER_PREFLIGHT porque a frente nao depende de Docker, build, boot em container ou integracao externa"
acceptance_criteria:
  - "Quando um runtime autenticado pular uma run pendente de outro principal, a propria run incompatível recebe evento `runtime_owner_skip` em `REQUEST` com mensagem objetiva contendo `runtime_started_by` e `run_initiated_by`."
  - "A run incompatível continua `pending` e `locked=false`, e o worker segue para a próxima run compatível sem falhar a fila."
  - "Polls consecutivos sem mudança no motivo do skip nao duplicam o mesmo evento `runtime_owner_skip` na mesma run."
  - "Runs legadas compativeis (`unknown`, `system`, `local_cli`) nao recebem evento de skip."
  - "Existe cobertura unitaria e de integracao para registro do evento, deduplicacao e exibicao em `aignt runs show <run_id>`."
non_goals:
  - "alterar o contrato de `runs submit` ou `runtime start|run|stop|status`"
  - "criar novo comando publico, painel novo ou migration de persistencia"
  - "falhar, requeue especial ou quarantine de runs incompatíveis"
  - "abrir observabilidade remota, multi-host ou transporte autenticado"
dependencies:
  - F35-worker-runtime-ownership-filter
---

# Contexto

A `F35` fechou o ownership local no consumo da fila: o worker autenticado so processa
runs pendentes compativeis com `started_by`, pulando runs de outro principal e seguindo
para a proxima compativel. O AIgnt-Synapse-Flow continua sendo a engine propria de
pipeline do AIgnt OS.

O residual local mais imediato agora e observabilidade. Hoje o skip acontece de forma
segura, mas a run incompatível continua pendente sem explicar por que nao foi
consumida. O repositório ja possui persistencia de `run_events` e `runs show` exibe
`Latest Signal`, o que permite resolver esse gap sem criar superficie nova.

# Objetivo

Registrar de forma auditavel quando o worker autenticado pula uma run pendente de outro
principal, reutilizando os eventos persistidos e a observabilidade local ja existente.

# Escopo

## Incluido

- evento persistido `runtime_owner_skip` na run incompatível
- mensagem objetiva com `runtime_started_by` e `run_initiated_by`
- deduplicacao do mesmo skip em polls consecutivos
- cobertura unitaria e de integracao para o worker e para `runs show`

## Fora de escopo

- qualquer comando publico novo
- qualquer mudanca em schema SQLite
- falha automatica, quarantine ou limpeza da fila
- qualquer coordenacao entre multiplos hosts ou transporte novo

# Casos de erro

- a run incompatível recebe skip repetido em polls consecutivos sem mudanca de contexto
- a run incompatível deixa de mostrar o motivo em `runs show`
- run legada compativel recebe skip indevido
- worker para de consumir a run compativel seguinte apos registrar o skip

# Cenarios verificaveis

## Cenario 1: skip fica auditavel

- Dado um runtime residente iniciado por `operator-a`
- E uma run pendente incompatível de `operator-b`
- Quando o worker fizer polling
- Entao a run incompatível recebe evento `runtime_owner_skip` em `REQUEST`
- E a mensagem registra `runtime_started_by=operator-a` e `run_initiated_by=operator-b`

## Cenario 2: deduplicacao do mesmo skip

- Dado uma run pendente incompatível que ja recebeu `runtime_owner_skip`
- Quando um novo polling ocorrer sem mudanca no motivo do skip
- Entao o mesmo evento nao e duplicado

## Cenario 3: observabilidade aparece em runs show

- Dado uma run pendente incompatível com `runtime_owner_skip`
- Quando `aignt runs show <run_id>` for executado
- Entao `Latest Signal` exibe `runtime_owner_skip @ REQUEST`
- E a mensagem do evento aparece na secao de eventos

# Observacoes

Esta frente continua estritamente local. Ela torna o skip explicavel, mas nao muda a
politica da fila nem fecha o bucket remoto de `G-11`.
