# F32 Report

## Resumo executivo

- A `F32-runtime-resident-principal-binding` implementou o primeiro slice concreto do bucket `resident_transport_auth` sem abrir socket ou transporte remoto.
- O runtime residente agora persiste `started_by` quando auth local esta habilitada, exibe esse binding em `runtime status` e endurece `runtime stop` contra outro operador quando o binding existe.
- O Synapse-Flow continua sendo a engine propria de pipeline do SynapseOS; a frente permaneceu restrita ao lifecycle local do runtime.

## Escopo entregue

- `RuntimeState` e `RuntimeStateStore` estendidos com `started_by`
- `RuntimeService.start()` e `RuntimeService.run_foreground()` passam a persistir o principal autenticado que iniciou o runtime
- `runtime status` renderiza `Started by` quando auth esta habilitada e sinaliza `unavailable` para estado legado sem binding
- `runtime stop` rejeita operador diferente quando o estado atual tem `started_by`
- estado legado sem `started_by` permanece operavel com o fallback compativel atual
- `SPEC.md`, `NOTES.md`, `CHECKLIST.md` e este `REPORT.md` adicionados para a `F32`

## Validacoes executadas

- `validate_spec_file(Path('features/F32-runtime-resident-principal-binding/SPEC.md'))`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_runtime_state.py tests/unit/test_cli_rich_output.py tests/integration/test_cli_auth_rbac.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff check src/synapse_os/cli/app.py src/synapse_os/cli/rendering.py src/synapse_os/runtime/service.py src/synapse_os/runtime/state.py tests/unit/test_runtime_state.py tests/unit/test_cli_rich_output.py tests/integration/test_cli_auth_rbac.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m mypy src/synapse_os/cli/app.py src/synapse_os/cli/rendering.py src/synapse_os/runtime/service.py src/synapse_os/runtime/state.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_runtime_state.py tests/unit/test_runtime_service_security.py tests/unit/test_cli_rich_output.py tests/integration/test_runtime_cli.py tests/integration/test_cli_auth_rbac.py -q`
- `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security`
- `./scripts/security-gate.sh`

## Review de seguranca

- Parecer final: aprovado.
- Riscos revisados:
  - regressao no hardening previo de `process_identity`
  - bloqueio indevido de `runtime stop` para estado legado
  - ampliacao acidental do recorte para transporte novo
- Mitigacoes aplicadas:
  - `started_by` foi adicionado sem remover o fail-safe atual de estado inconsistente
  - `runtime stop` so faz enforcement por principal quando o binding existe
  - a frente permaneceu sem socket, sem IPC e sem alteracoes no auth registry

## Riscos residuais

- O binding e por `principal_id`, nao por `token_id`; dois tokens do mesmo principal continuam equivalentes para `runtime stop`.
- O bucket maior de `resident_transport_auth` continua incompleto; a `F32` cobre apenas lifecycle local do runtime.

## Proximos passos

- Rodar `branch-sync-guard` antes de commit/push/PR.
- Triar se o proximo slice de `resident_transport_auth` ainda cabe sem socket ou se o tema precisa de ADR/adiamento.

## Status final da frente

- `READY_FOR_COMMIT`
