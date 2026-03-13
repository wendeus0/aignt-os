# F36 Report

## Resumo executivo

- A `F36-worker-owner-skip-observability` torna auditavel quando o worker autenticado do runtime residente pula uma run pendente de outro principal por mismatch de ownership.
- O evento `runtime_owner_skip` passa a ser persistido na propria run incompatível, preservando o AIgnt-Synapse-Flow como a engine propria de pipeline do AIgnt OS.
- O recorte permaneceu local-only: sem mudanca de CLI publica, sem schema novo e sem transporte remoto.

## Escopo alterado

- `RunRepository` passa a listar runs pendentes desbloqueadas em ordem FIFO e a consultar o ultimo evento de uma run
- `RuntimeWorker` passa a registrar `runtime_owner_skip` em `REQUEST` antes de seguir para a proxima run compativel
- o worker evita duplicar o mesmo skip em polls consecutivos quando o ultimo evento relevante ja corresponde ao mesmo motivo
- runs legadas com `initiated_by` em `unknown`, `system` ou `local_cli` continuam elegiveis e nao recebem skip
- `runs show <run_id>` passa a refletir o novo evento sem precisarmos alterar a superficie publica
- `SPEC.md`, `NOTES.md`, `CHECKLIST.md` e este `REPORT.md` adicionados para a `F36`

## Validacoes executadas

- `validate_spec_file(Path('features/F36-worker-owner-skip-observability/SPEC.md'))`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/aignt-os/.cache/uv uv run --no-sync python -m pytest tests/unit/test_worker_runtime.py tests/integration/test_worker_runtime_flow.py -q`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/aignt-os/.cache/uv uv run --no-sync ruff check src/aignt_os/runtime/worker.py src/aignt_os/persistence.py tests/unit/test_worker_runtime.py tests/integration/test_worker_runtime_flow.py`
- `env UV_CACHE_DIR=/home/g0dsssp33d/work/projects/aignt-os/.cache/uv uv run --no-sync python -m mypy src/aignt_os/runtime/worker.py src/aignt_os/persistence.py`
- `./scripts/commit-check.sh --no-sync --skip-branch-validation --skip-docker --skip-security`
- `./scripts/security-gate.sh`

## Review de seguranca

- Parecer final: aprovado.
- Riscos revisados:
  - worker autenticado deixar runs incompatíveis invisiveis para investigacao
  - spam de eventos repetidos a cada poll sem mudanca de contexto
  - regressao do filtro legado para runs sem ownership explicito
- Mitigacoes aplicadas:
  - o evento e gravado na run incompatível com contexto objetivo de `runtime_started_by` e `run_initiated_by`
  - a deduplicacao consulta o ultimo evento da run antes de persistir um novo `runtime_owner_skip`
  - runs legadas compativeis permanecem sem skip e cobertas por teste

## Riscos residuais

- Runs incompatíveis continuam pendentes ate que um runtime compativel as consuma; esta frente melhora explicabilidade, nao politica de fila.
- A observabilidade adicional fica restrita a `run_events` e `runs show`; nao ha alerta ativo nem metrica agregada para o skip.

## Proximos passos

- Se `resident_transport_auth` continuar como bucket local, o proximo slice natural e decidir se `docs/IDEAS.md` ja pode marcar a parte residente como encerrada ou se ainda vale um ajuste pequeno de observabilidade agregada.
- Se o trabalho migrar para auth remota ou multi-host, a frente deve ser reavaliada em triagem separada antes de abrir ADR ou transporte novo.

## Status final da frente

- `READY_FOR_COMMIT`
