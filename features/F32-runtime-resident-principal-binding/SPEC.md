---
id: F32-runtime-resident-principal-binding
type: feature
summary: Vincular o runtime residente ao principal autenticado que o iniciou, sem abrir socket nem transporte remoto.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - features/F29-auth-rbac-foundation/SPEC.md
  - features/F31-g11-remote-auth-decomposition/SPEC.md
  - src/synapse_os/cli/app.py
  - src/synapse_os/runtime/state.py
  - src/synapse_os/runtime/service.py
outputs:
  - runtime_started_by_binding
  - runtime_auth_red_tests
constraints:
  - "manter o Synapse-Flow como a engine propria de pipeline do SynapseOS"
  - "trabalhar apenas o menor recorte implementavel do bucket `resident_transport_auth`"
  - "nao introduzir socket, IPC, transporte em rede, RBAC novo ou coordenacao entre hosts"
  - "preservar compatibilidade com estado legado do runtime sem `started_by`"
  - "nao exigir DOCKER_PREFLIGHT porque a frente nao depende de boot em container, build de imagem ou integracao externa"
acceptance_criteria:
  - "Quando `auth_enabled=false`, `runtime start|run|stop|status` preservam o comportamento atual."
  - "Quando `auth_enabled=true`, `runtime start` e `runtime run` persistem `started_by` com o `principal_id` autenticado no estado do runtime."
  - "`runtime status` exibe `started_by` quando auth estiver habilitada; se o estado for legado e nao tiver `started_by`, a saida marca o binding como indisponivel sem quebrar o comando."
  - "Quando `auth_enabled=true` e o estado atual tiver `started_by`, `runtime stop` falha com `Authorization error:` se o principal autenticado for diferente do principal que iniciou o runtime."
  - "Quando `auth_enabled=true` e o estado atual for legado sem `started_by`, `runtime stop` preserva o fallback compativel atual para `operator`."
  - "Existe cobertura unitaria e de integracao para persistencia de `started_by`, rendering de status e enforcement de stop por principal."
non_goals:
  - "autenticar worker polling ou `runs submit`"
  - "persistir `token_id` ou binding por token no estado do runtime"
  - "introduzir novos papeis alem de `viewer` e `operator`"
  - "abrir qualquer forma de auth remota ou multi-host"
dependencies:
  - F29-auth-rbac-foundation
  - F31-g11-remote-auth-decomposition
---

# Contexto

Depois da `F31`, o residual de `G-11` foi decomposto e o bucket pequeno restante ficou
identificado como `resident_transport_auth`. No baseline atual, porem, o runtime
residente ainda nao expoe socket, IPC ou transporte proprio: a interacao pratica fica
restrita ao lifecycle local via `runtime start|run|stop`, com estado persistido em
arquivo e auth apenas na borda da CLI.

O menor recorte implementavel agora e vincular esse runtime residente ao principal
autenticado que o iniciou. Isso endurece o lifecycle local sem inventar transporte novo
e preserva o Synapse-Flow como a engine propria de pipeline do SynapseOS.

# Objetivo

Persistir o principal autenticado que iniciou o runtime residente e usar essa
provenance para endurecer `runtime stop`, mantendo compatibilidade com estado legado.

# Escopo

## Incluido

- campo `started_by` no estado do runtime
- persistencia de `started_by` em `runtime start` e `runtime run` quando auth estiver habilitada
- exibicao de `started_by` em `runtime status` quando auth estiver habilitada
- enforcement de `runtime stop` pelo mesmo principal quando o binding existir
- fallback compativel para estado legado sem `started_by`
- testes unitarios e de integracao do lifecycle autenticado

## Fora de escopo

- socket, IPC e qualquer transporte novo
- binding por `token_id`
- alteracoes em `runs submit`
- mudancas no auth registry local

# Casos de erro

- `runtime stop` com principal diferente do `started_by`
- estado legado sem `started_by` quando auth estiver habilitada
- runtime inconsistente por PID/process identity, mantendo o fail-safe atual

# Cenarios verificaveis

## Cenario 1: auth desabilitada preserva baseline

- Dado `auth_enabled=false`
- Quando `runtime start`, `runtime status` e `runtime stop` forem executados
- Entao o comportamento atual permanece inalterado

## Cenario 2: runtime registra principal autenticado

- Dado `auth_enabled=true` e um principal `operator-user`
- Quando `runtime start` for executado com token valido
- Entao o estado persistido inclui `started_by=operator-user`
- E `runtime status` exibe esse principal

## Cenario 3: stop rejeita principal diferente quando o binding existe

- Dado `auth_enabled=true` e um runtime iniciado por `operator-a`
- Quando `runtime stop` for executado por `operator-b`
- Entao a CLI retorna `Authorization error:`

## Cenario 4: estado legado permanece operavel

- Dado `auth_enabled=true` e um estado legado valido sem `started_by`
- Quando `runtime status` for executado
- Entao a saida sinaliza que o binding esta indisponivel
- E `runtime stop` continua aceitando o comportamento compativel atual para `operator`

# Observacoes

Esta frente nao autentica transporte entre processos. Ela apenas amarra o lifecycle do
runtime residente ao principal autenticado que o iniciou, como primeiro slice concreto
do bucket `resident_transport_auth`.
