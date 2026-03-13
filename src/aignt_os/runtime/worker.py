from __future__ import annotations

import time
from collections.abc import Callable

from aignt_os.config import AppSettings
from aignt_os.persistence import (
    ArtifactStore,
    PersistedPipelineRunner,
    RunRecord,
    RunRepository,
)
from aignt_os.runtime.state import RuntimeState, RuntimeStateStore

LEGACY_INITIATED_BY_VALUES = frozenset({"unknown", "system", "local_cli"})


class RuntimeWorker:
    def __init__(
        self,
        *,
        repository: RunRepository,
        runner: PersistedPipelineRunner,
        poll_interval_seconds: float = 0.5,
        runtime_state_provider: Callable[[], RuntimeState] | None = None,
    ) -> None:
        self.repository = repository
        self.runner = runner
        self.poll_interval_seconds = poll_interval_seconds
        self.runtime_state_provider = runtime_state_provider

    def poll_once(self) -> str | None:
        while True:
            run_record = self._next_pending_run()
            if run_record is None:
                return None
            if not self.repository.acquire_lock(run_record.run_id):
                continue
            try:
                self.runner.run_existing(run_record.run_id, assume_locked=True)
            except Exception:
                # Failed runs are already persisted by the runner observer.
                pass
            return run_record.run_id

    def sleep_when_idle(self) -> None:
        time.sleep(self.poll_interval_seconds)

    def _next_pending_run(self) -> RunRecord | None:
        compatible_initiators = self._compatible_initiators()
        if compatible_initiators is None:
            return self.repository.find_next_pending_run()
        return self.repository.find_next_pending_run_for_initiators(compatible_initiators)

    def _compatible_initiators(self) -> set[str] | None:
        if self.runtime_state_provider is None:
            return None

        runtime_state = self.runtime_state_provider()
        if runtime_state.status != "running" or runtime_state.started_by is None:
            return None

        return set(LEGACY_INITIATED_BY_VALUES | {runtime_state.started_by})


def build_runtime_worker(settings: AppSettings) -> RuntimeWorker:
    repository = RunRepository(settings.runs_db_path)
    artifact_store = ArtifactStore(settings.artifacts_dir)
    runtime_state_store = RuntimeStateStore(settings.runtime_state_file)
    runner = PersistedPipelineRunner(
        repository=repository,
        artifact_store=artifact_store,
    )
    return RuntimeWorker(
        repository=repository,
        runner=runner,
        poll_interval_seconds=settings.runtime_poll_interval_seconds,
        runtime_state_provider=runtime_state_store.read if settings.auth_enabled else None,
    )
