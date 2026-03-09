from __future__ import annotations

from importlib import import_module
from pathlib import Path

import pytest


def test_runtime_service_treats_identity_mismatch_as_inconsistent(tmp_path: Path) -> None:
    service_module = import_module("aignt_os.runtime.service")
    state_module = import_module("aignt_os.runtime.state")

    service = service_module.RuntimeService(tmp_path / "runtime-state.json")
    service.state_store._write(  # noqa: SLF001
        state_module.RuntimeState(
            status="running",
            pid=1,
            started_at="2026-03-09T00:00:00+00:00",
        )
    )

    state = service.current_state()

    assert state.status == "inconsistent"


def test_runtime_service_stop_does_not_signal_when_identity_validation_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    service_module = import_module("aignt_os.runtime.service")
    state_module = import_module("aignt_os.runtime.state")

    service = service_module.RuntimeService(tmp_path / "runtime-state.json")
    service.state_store._write(  # noqa: SLF001
        state_module.RuntimeState(
            status="running",
            pid=4242,
            started_at="2026-03-09T00:00:00+00:00",
        )
    )

    signal_attempted = False

    def fail_if_stop_called(pid: int) -> None:
        nonlocal signal_attempted
        signal_attempted = True

    monkeypatch.setattr(service, "_stop_process", fail_if_stop_called)

    with pytest.raises(service_module.RuntimeLifecycleError):
        service.stop()

    assert signal_attempted is False
