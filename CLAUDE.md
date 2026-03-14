# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read first

Before making non-trivial changes, read these in order:

1. `CONTEXT.md`
2. `docs/architecture/SDD.md`
3. `docs/architecture/TDD.md`
4. `docs/architecture/SPEC_FORMAT.md`
5. `features/<current-feature>/SPEC.md` if the task is feature-specific

If they conflict: feature `SPEC.md` governs behavior, `SDD.md` governs architecture, `TDD.md` governs testing strategy, `SPEC_FORMAT.md` governs SPEC structure.

---

## Build, test, lint, and validation

### Standard local validation

```bash
./scripts/commit-check.sh --sync-dev   # full: syncs env + format + lint + typecheck + tests
./scripts/commit-check.sh --no-sync    # fast rerun after env is already synced
```

### Individual checks

```bash
uv run --no-sync ruff format --check .
uv run --no-sync ruff check .
uv run --no-sync python -m mypy
uv run --no-sync python -m pytest
```

Always use `python -m pytest` and `python -m mypy` (not bare `pytest`/`mypy`) — the repo hardened against broken virtualenv wrappers.

### Running a single test

```bash
uv run --no-sync python -m pytest tests/unit/test_state_machine.py
uv run --no-sync python -m pytest tests/unit/test_state_machine.py::test_state_machine_follows_minimal_happy_path_to_complete
```

### Docker and runtime validation

```bash
./scripts/docker-preflight.sh              # lightweight: compose config only (default)
./scripts/docker-preflight.sh --build      # validate application image
./scripts/docker-preflight.sh --full-runtime  # full runtime (boot, lifecycle, persistence, integration)
```

Use `--full-runtime` only when the change touches boot, lifecycle, persistence, or container runtime behavior.

### Validate a SPEC locally

```bash
uv run --no-sync python -c "
from pathlib import Path
from synapse_os.specs.validator import validate_spec_file
result = validate_spec_file(Path('features/<feature>/SPEC.md'))
print(result)
"
```

The public API is `validate_spec_file(path: Path) -> SpecDocument` — there is no `SpecValidator` class.

---

## Architecture overview

SynapseOS is a CLI-first meta-orchestrator for external AI tools (Gemini, Codex, Claude, etc.). Two flows exist and must not be confused:

1. **Official feature development workflow** (humans/agents working in the repo):
   ```
   DOCKER_PREFLIGHT → SPEC → TEST_RED → CODE_GREEN → REFACTOR → QUALITY_GATE → SECURITY_REVIEW → REPORT → COMMIT
   ```

2. **Internal runtime state flow** (Synapse-Flow, the repository's own pipeline engine):
   ```
   REQUEST → SPEC_DISCOVERY → SPEC_NORMALIZATION → SPEC_VALIDATION → PLAN → TEST_RED → CODE_GREEN → REVIEW → SECURITY → DOCUMENT → COMPLETE
   ```

### Key modules

| Module | Role |
|---|---|
| `src/synapse_os/cli/app.py` | Typer CLI entry point (`synapse` command) |
| `src/synapse_os/state_machine.py` | `SynapseStateMachine` — linear state machine for Synapse-Flow |
| `src/synapse_os/pipeline.py` | `PipelineEngine` — executes steps, coordinates `StepExecutor` impls |
| `src/synapse_os/persistence.py` | `RunRepository` (SQLAlchemy/SQLite) + `ArtifactStore` (filesystem) + `PersistedPipelineRunner` |
| `src/synapse_os/adapters.py` | `BaseCLIAdapter` — async subprocess execution with circuit breaker |
| `src/synapse_os/supervisor.py` | Deterministic failure handling (retry / reroute / fail) |
| `src/synapse_os/runtime/` | `RuntimeService`, `RuntimeWorker`, `RunDispatchService`, `RuntimeStateStore` |
| `src/synapse_os/specs/validator.py` | SPEC validation engine |
| `src/synapse_os/contracts.py` | Domain models via Pydantic v2 |
| `src/synapse_os/config.py` | `AppSettings` (pydantic-settings, `SYNAPSE_OS_` env prefix) |
| `src/synapse_os/reporting.py` | `RUN_REPORT.md` generation at `DOCUMENT` state |

### Runtime modes

The current runtime is a minimal dual-mode foundation:
- **Sync** (`--mode sync`): inline execution via `PersistedPipelineRunner`
- **Async** (`--mode async`): queues run to SQLite; `RuntimeWorker` polls and executes
- **Auto**: `RunDispatchService` detects based on runtime state

`RuntimeStateStore` treats missing state as `stopped` and corrupted/mismatched persisted state as `inconsistent`. Changes to runtime behavior must preserve these three-state safety checks.

### SPEC format

SPECs are Markdown with required YAML frontmatter. Required metadata fields: `id`, `type`, `summary`, `inputs`, `outputs`, `acceptance_criteria`, `non_goals`. Required body sections: `# Contexto` and `# Objetivo` as **H1 headings only** — `##` headings are ignored by the parser.

Feature directories: `features/F<NN>-<slug>/SPEC.md`

---

## Key conventions

### Terminology

- **Synapse-Flow** = the repository's own pipeline engine (always name it this way)
- `SPEC` = the formal feature specification
- `run` = one pipeline execution
- `worker` / `runtime` = the resident long-lived mode

### Configuration

All `AppSettings` fields use the `SYNAPSE_OS_` prefix. Never use `os.environ` directly — always go through `AppSettings`.

### Contracts

`CLIExecutionResult` keeps `stdout_raw` and `stdout_clean` separate. Do not collapse them into one field.

### Testing conventions

- Naming: `test_<what_it_does>_<scenario>` (e.g., `test_state_machine_blocks_plan_before_spec_validation`)
- Do not mock what can be tested with the real implementation (e.g., do not mock `validate_spec_file`)
- Do not use `time.sleep` in tests — use time mocks
- Key exceptions to test explicitly: `InvalidStateTransition`, `SpecValidationError`, `RuntimeInconsistentError`
- `tests/unit/` — isolated logic; `tests/integration/` — CLI bootstrap and runtime CLI; `tests/fixtures/specs/` — SPEC fixtures

### Branch sync

On non-`main` branches, check drift before substantial work and before commit/PR:

```bash
./scripts/branch-sync-check.sh
```

Use `./scripts/branch-sync-update.sh` only as the conservative helper described in `AGENTS.md` — not as an automatic fix.

### Development policy

- Work one feature at a time; never mix scopes across features
- Write tests before production code (TDD)
- Do not refactor before tests are green
- Do not start Docker-dependent execution without a validated DOCKER_PREFLIGHT
- Treat `observability/` as future-facing — verify concrete implementation before wiring against it

### Stop criteria

Stop and report explicitly when:
- The `SPEC.md` is ambiguous
- Tests contradict the SPEC
- The change requires wide refactoring outside the feature scope
- The change requires architectural decisions not covered by existing ADRs

---

## Nota sobre `.claude/skills/`

As entradas em `.claude/skills/` são **symlinks** apontando para `.agents/skills/`. A fonte canônica é `.agents/skills/`. No Windows, symlinks requerem developer mode ou WSL.
