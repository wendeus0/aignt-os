---
id: F35-worker-runtime-ownership-filter
type: feature
summary: Filtrar no worker as runs pendentes compativeis com o owner do runtime residente autenticado.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - features/F32-runtime-resident-principal-binding/SPEC.md
  - features/F34-async-submit-runtime-ownership/SPEC.md
  - src/synapse_os/runtime/worker.py
  - src/synapse_os/persistence.py
  - tests/unit/test_worker_runtime.py
  - tests/integration/test_worker_runtime_flow.py
outputs:
  - worker_runtime_owner_filter
  - worker_owner_filter_red_tests
constraints:
  - "manter o Synapse-Flow como a engine propria de pipeline do SynapseOS"
  - "restringir a frente ao consumo da fila pelo worker; sem alterar CLI publica, socket, IPC, transporte remoto ou auth registry"
  - "preservar compatibilidade com runs legadas sem owner autenticado explicito"
  - "nao exigir DOCKER_PREFLIGHT porque a frente nao depende de Docker, build, boot em container ou integracao externa"
acceptance_criteria:
  - "Quando nao houver ownership ativo no runtime residente, o worker preserva o comportamento atual de consumir a run pendente mais antiga."
  - "Quando o runtime residente estiver autenticado com `started_by`, o worker consome apenas runs pendentes cuja `initiated_by` seja o mesmo principal ou um valor legado compativel."
  - "Quando a run pendente mais antiga pertencer a outro principal autenticado, o worker a ignora sem lockar nem falhar e continua procurando a proxima run compativel."
  - "Runs legadas com `initiated_by` em `unknown`, `system` ou `local_cli` continuam compativeis com runtime autenticado para preservar backlog anterior."
  - "Existe cobertura unitaria e de integracao para skip de owner incompatível, consumo da proxima run compatível e compatibilidade legada."
non_goals:
  - "alterar `runs submit`, `runtime start|run|stop|status` ou qualquer mensagem de erro publica"
  - "marcar automaticamente como failed as runs incompatíveis"
  - "introduzir binding por `token_id`, novas roles ou enforcement remoto/multi-host"
  - "mudar a ordem global da fila fora do subconjunto compativel"
dependencies:
  - F32-runtime-resident-principal-binding
  - F34-async-submit-runtime-ownership
---

# Contexto

A `F32` vinculou o runtime residente local ao principal autenticado que o iniciou por
meio de `started_by`. A `F34` fechou o gap no submit autenticado, impedindo enqueue
assinado para `async` quando o runtime residente nao esta pronto ou pertence a outro
principal. O Synapse-Flow continua sendo a engine propria de pipeline do SynapseOS.

Mesmo assim, o worker residente ainda consome a fila apenas por FIFO simples. Isso
significa que um runtime autenticado pode executar runs pendentes de outro principal
ja persistidas na fila, ou ficar preso numa ordem que nao respeita ownership local do
runtime.

# Objetivo

Filtrar o consumo do worker para que um runtime residente autenticado processe apenas
runs pendentes compativeis com o principal que o iniciou, sem falhar runs
incompativeis e sem abrir transporte novo.

# Escopo

## Incluido

- leitura opcional do estado atual do runtime no worker
- selecao da proxima run pendente compativel com `started_by`
- skip de runs incompatíveis sem lock nem falha
- compatibilidade explicita para runs legadas (`unknown`, `system`, `local_cli`)
- testes unitarios e de integracao do fluxo do worker

## Fora de escopo

- qualquer mudanca em CLI publica
- qualquer alteracao de schema SQLite
- qualquer mecanismo de requeue, quarantine ou falha automatica para runs incompatíveis
- socket, IPC, RPC ou operacao remota/multi-host

# Casos de erro

- runtime autenticado encontra apenas runs pendentes de outro principal
- run incompatível ocupa a primeira posicao da fila e deve ser pulada
- runtime autenticado encontra mix de runs legadas e runs autenticadas de outro owner
- worker sem ownership ativo deve manter o comportamento atual

# Cenarios verificaveis

## Cenario 1: worker sem ownership ativo preserva baseline

- Dado um worker sem ownership ativo no runtime
- Quando existir uma fila com runs pendentes
- Entao a run pendente mais antiga continua sendo consumida

## Cenario 2: worker autenticado pula run de outro principal

- Dado um runtime residente iniciado por `operator-a`
- E uma fila cuja run mais antiga pertence a `operator-b`
- E exista depois uma run pendente de `operator-a`
- Quando o worker fizer polling
- Entao a run de `operator-b` permanece pendente e desbloqueada
- E a run de `operator-a` e processada

## Cenario 3: worker autenticado aceita backlog legado

- Dado um runtime residente iniciado por `operator-a`
- E uma run legada pendente com `initiated_by=local_cli`, `system` ou `unknown`
- Quando o worker fizer polling
- Entao a run legada continua elegivel para processamento

# Observacoes

Esta frente fecha apenas o ownership local no consumo da fila pelo worker. Ela nao
introduz erro publico novo, nao altera a persistencia e nao tenta resolver
coordenacao entre runtimes ou ownership remoto.
