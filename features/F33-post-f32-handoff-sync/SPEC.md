---
id: F33-post-f32-handoff-sync
type: chore
summary: Alinhar o handoff pos-F32 ao estado real do baseline antes da proxima triagem de produto.
inputs:
  - CONTEXT.md
  - docs/architecture/SDD.md
  - docs/architecture/TDD.md
  - docs/architecture/SPEC_FORMAT.md
  - docs/IDEAS.md
  - PENDING_LOG.md
  - ERROR_LOG.md
  - memory.md
  - features/F31-g11-remote-auth-decomposition/SPEC.md
  - features/F32-runtime-resident-principal-binding/SPEC.md
outputs:
  - post_f32_handoff_alignment
  - updated_g11_resident_auth_baseline_docs
constraints:
  - "manter o Synapse-Flow como a engine propria de pipeline do SynapseOS"
  - "restringir a frente a handoff e backlog docs; sem alteracao funcional de CLI, runtime ou auth"
  - "nao introduzir nova feature de produto, socket, IPC, transporte remoto ou ADR"
  - "nao exigir DOCKER_PREFLIGHT, porque a frente nao depende de Docker, build, boot ou integracao pratica"
acceptance_criteria:
  - "Existe `features/F33-post-f32-handoff-sync/SPEC.md` valida, descrevendo a frente como chore doc-only de alinhamento pos-`F32`."
  - "`PENDING_LOG.md` registra que a `F32-runtime-resident-principal-binding` foi mergeada pela PR `#68` e que o primeiro slice de `resident_transport_auth` ja foi entregue."
  - "`ERROR_LOG.md` deixa de tratar a falha de `repo-checks` da PR `#65` como bloqueio aberto e a registra como incidente resolvido pela estabilizacao da PR `#66`."
  - "`memory.md` deixa de apontar `F31` como frente ativa e passa a refletir que `main` incorpora `F32`, mantendo `resident_transport_auth` apenas como bucket parcialmente absorvido."
  - "`docs/IDEAS.md` passa a refletir que `G-11` ja absorveu `F32` como primeiro slice do bucket residente, sem sugerir que auth remota ja exista."
  - "A cobertura em `tests/unit/test_auth_registry_docs.py` trava explicitamente o novo estado pos-`F32` em `docs/IDEAS.md`."
non_goals:
  - "implementar novo comportamento de runtime, auth registry ou CLI publica"
  - "abrir outro slice de `resident_transport_auth`"
  - "iniciar `remote_multi_host_auth` ou qualquer transporte entre hosts"
dependencies:
  - F31-g11-remote-auth-decomposition
  - F32-runtime-resident-principal-binding
---

# Contexto

A `F31-g11-remote-auth-decomposition` removeu a ambiguidade de `G-11` e a `F32-runtime-resident-principal-binding`
entregou o primeiro slice concreto do bucket `resident_transport_auth` no baseline atual.
O Synapse-Flow continua sendo a engine propria de pipeline do SynapseOS, e o runtime
segue local-only, sem socket, IPC autenticado ou operacao entre hosts.

Apesar disso, o handoff operacional ainda parou antes da `F32`: `PENDING_LOG.md`,
`ERROR_LOG.md` e `memory.md` continuam registrando `F31` como frente ativa ou mantendo o
incidente da PR `#65` como bloqueio aberto, embora a baseline ja tenha sido estabilizada
na `#66` e a `F32` tenha sido mergeada na `#68`.

# Objetivo

Realinhar o handoff pos-`F32` ao estado real do repositorio, mantendo backlog, memoria
duravel e log operacional coerentes com o baseline atual antes da proxima triagem de produto.

# Escopo

## Incluido

- criar a SPEC e os artefatos minimos da `F33`
- atualizar `PENDING_LOG.md`, `ERROR_LOG.md` e `memory.md` para o estado pos-`F32`
- atualizar `docs/IDEAS.md` para refletir a absorcao de `F32` dentro do bucket `G-11`
- ajustar o teste documental que trava o estado de `docs/IDEAS.md`

## Fora de escopo

- qualquer implementacao nova em `src/`
- nova SPEC de produto alem desta chore
- alteracao de workflow, CI ou gatilhos remotos
- qualquer transporte autenticado entre processos ou hosts

# Requisitos nao funcionais

- a frente deve permanecer doc-only
- o delta deve ser pequeno, auditavel e sem comportamento de produto novo
- a documentacao resultante nao pode sugerir que auth remota ou socket ja existem
- a memoria duravel deve registrar somente estado estavel, nao recontar a sessao toda

# Casos de erro

- `PENDING_LOG.md` continuar parando na `F31`
- `ERROR_LOG.md` continuar marcando a PR `#65` como bloqueio operacional ainda aberto
- `memory.md` continuar apontando `F31` como frente ativa
- `docs/IDEAS.md` sugerir que `resident_transport_auth` ainda nao absorveu nenhum slice ou insinuar que auth remota ja esta implementada

# Cenarios verificaveis

## Cenario 1: handoff pos-F32 fica coerente

- Dado o baseline atual em `main`
- Quando `PENDING_LOG.md`, `ERROR_LOG.md` e `memory.md` forem lidos
- Entao todos refletem a merge da `F32` e o fechamento operacional da estabilizacao da baseline

## Cenario 2: backlog de G-11 incorpora o primeiro slice residente

- Dado `docs/IDEAS.md` atualizado
- Quando o item `G-11` for lido
- Entao ele registra `F29` e `F30` como fundacao local absorvida
- E registra `F32` como primeiro slice absorvido do bucket `resident_transport_auth`
- E continua deixando `remote_multi_host_auth` explicitamente adiado

# Observacoes

Esta frente prepara a proxima triagem, mas nao decide ainda qual sera a `F34`. Depois do
handoff alinhado, a proxima decisao deve escolher explicitamente entre outro slice local-only
de `resident_transport_auth` ou um hardening menor fora desse bucket.
