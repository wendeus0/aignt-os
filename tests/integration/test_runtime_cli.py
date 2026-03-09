from __future__ import annotations

from importlib import import_module
from pathlib import Path
import json
import subprocess
import sys

from typer.testing import CliRunner


runner = CliRunner()


def invoke_runtime_command(tmp_path: Path, *args: str):
    cli_module = import_module("aignt_os.cli.app")
    env = {
        "AIGNT_OS_ENVIRONMENT": "test",
        "AIGNT_OS_RUNTIME_STATE_DIR": str(tmp_path),
    }
    return runner.invoke(cli_module.app, ["runtime", *args], env=env)


def test_runtime_start_initializes_single_resident_process_and_persists_state(
    tmp_path: Path,
) -> None:
    result = invoke_runtime_command(tmp_path, "start")

    assert result.exit_code == 0
    assert "running" in result.stdout.lower()

    state_files = list(tmp_path.glob("*.json"))
    assert state_files

    persisted_state = json.loads(state_files[0].read_text(encoding="utf-8"))
    assert persisted_state["status"] == "running"
    assert isinstance(persisted_state["pid"], int)
    assert persisted_state["pid"] > 0


def test_runtime_status_reports_running_for_active_runtime(tmp_path: Path) -> None:
    start_result = invoke_runtime_command(tmp_path, "start")
    assert start_result.exit_code == 0

    status_result = invoke_runtime_command(tmp_path, "status")

    assert status_result.exit_code == 0
    assert "running" in status_result.stdout.lower()


def test_runtime_start_rejects_second_active_process(tmp_path: Path) -> None:
    first_start = invoke_runtime_command(tmp_path, "start")
    assert first_start.exit_code == 0

    second_start = invoke_runtime_command(tmp_path, "start")

    assert second_start.exit_code != 0
    assert "already" in second_start.stdout.lower() or "already" in second_start.stderr.lower()


def test_runtime_stop_terminates_active_runtime_and_updates_status(tmp_path: Path) -> None:
    start_result = invoke_runtime_command(tmp_path, "start")
    assert start_result.exit_code == 0

    stop_result = invoke_runtime_command(tmp_path, "stop")

    assert stop_result.exit_code == 0
    assert "stopped" in stop_result.stdout.lower()

    status_result = invoke_runtime_command(tmp_path, "status")
    assert status_result.exit_code == 0
    assert "stopped" in status_result.stdout.lower()


def test_runtime_stop_reports_predictable_error_when_runtime_is_not_running(
    tmp_path: Path,
) -> None:
    result = invoke_runtime_command(tmp_path, "stop")

    assert result.exit_code != 0
    assert "not running" in result.stdout.lower() or "not running" in result.stderr.lower()


def test_runtime_status_reports_inconsistent_for_invalid_persisted_pid(
    tmp_path: Path,
) -> None:
    state_file = tmp_path / "runtime-state.json"
    state_file.write_text(
        json.dumps({"status": "running", "pid": 999_999_999}),
        encoding="utf-8",
    )

    result = invoke_runtime_command(tmp_path, "status")

    assert result.exit_code != 0
    assert "inconsistent" in result.stdout.lower() or "inconsistent" in result.stderr.lower()


def test_runtime_stop_refuses_to_signal_process_when_persisted_identity_mismatches(
    tmp_path: Path,
) -> None:
    arbitrary_process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        state_file = tmp_path / "runtime-state.json"
        state_file.write_text(
            json.dumps(
                {
                    "status": "running",
                    "pid": arbitrary_process.pid,
                    "started_at": "2026-03-09T00:00:00+00:00",
                    "process_identity": "unexpected-process",
                }
            ),
            encoding="utf-8",
        )

        result = invoke_runtime_command(tmp_path, "stop")

        assert result.exit_code != 0
        assert "inconsistent" in result.stdout.lower() or "inconsistent" in result.stderr.lower()
        assert arbitrary_process.poll() is None
    finally:
        arbitrary_process.terminate()
        arbitrary_process.wait(timeout=5)


def test_runtime_start_rejects_untrusted_state_directory(tmp_path: Path) -> None:
    cli_module = import_module("aignt_os.cli.app")
    env = {
        "AIGNT_OS_ENVIRONMENT": "test",
        "AIGNT_OS_RUNTIME_STATE_DIR": "../outside-runtime-state",
    }

    result = runner.invoke(cli_module.app, ["runtime", "start"], env=env)

    assert result.exit_code != 0
    assert "state" in result.stdout.lower() or "state" in result.stderr.lower()
