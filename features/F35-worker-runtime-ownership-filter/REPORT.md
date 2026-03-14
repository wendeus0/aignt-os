# F35 Report

## Resumo executivo

- A `F35-worker-runtime-ownership-filter` fecha o ownership local no consumo da fila pelo worker do runtime residente.
- O worker agora filtra runs pendentes compatíveis com `started_by` quando o runtime autenticado está ativo, mantendo o Synapse-Flow como a engine propria de pipeline do SynapseOS.
- O recorte permaneceu local-only: sem mudança de CLI pública, sem schema novo e sem transporte remoto.

## Escopo alterado

- `RuntimeWorker` passa a aceitar provider opcional do estado do runtime e a filtrar a fila apenas quando houver ownership ativo
- `RunRepository` passa a expor busca da próxima run pendente compatível por `initiated_by`
- runs incompatíveis de outro principal ficam pendentes e destravadas; o worker segue para a próxima compatível
- runs legadas com `initiated_by` em `unknown`, `system` ou `local_cli` continuam elegíveis sob runtime autenticado
- `SPEC.md`, `NOTES.md`, `CHECKLIST.md` e este `REPORT.md` adicionados para a `F35`

## Validacoes executadas

- `validate_spec_file(Path('features/F35-worker-runtime-ownership-filter/SPEC.md'))`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_worker_runtime.py tests/integration/test_worker_runtime_flow.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync ruff check src/synapse_os/runtime/worker.py src/synapse_os/persistence.py tests/unit/test_worker_runtime.py tests/integration/test_worker_runtime_flow.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/synapse-os/.cache/uv uv run --no-sync python -m mypy src/synapse_os/runtime/worker.py src/synapse_os/persistence.py`
- `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security`
- `./scripts/security-gate.sh`

## Review de seguranca

- Parecer final: aprovado.
- Riscos revisados:
  - runtime autenticado consumir run pendente de outro principal
  - starvation por run incompatível no topo da fila
  - regressao do comportamento atual quando não houver ownership ativo
- Mitigacoes aplicadas:
  - o filtro só entra quando há `started_by` ativo no runtime
  - a busca passa a selecionar a primeira run compatível, sem lockar ou falhar as incompatíveis
  - backlog legado permanece compatível por política explícita e coberta por teste

## Riscos residuais

- Runs incompatíveis continuam pendentes até que um runtime compatível as consuma.
- O recorte não adiciona observabilidade nova para explicar skips de ownership; isso permanece follow-up opcional, não requisito desta frente.

## Proximos passos

- Se o bucket `resident_transport_auth` continuar, o próximo slice deve decidir se vale adicionar observabilidade explícita dos skips do worker sem ampliar para transporte novo.
- Se esse tema crescer além do runtime local, parar e reavaliar com triagem antes de abrir ADR ou auth remota.

## Status final da frente

- `READY_FOR_COMMIT`
