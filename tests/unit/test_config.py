from importlib import import_module

import pytest
from pydantic import ValidationError


def test_settings_exposes_default_values() -> None:
    config_module = import_module("aignt_os.config")

    settings = config_module.AppSettings()

    assert settings.model_dump()["app_name"]
    assert settings.model_dump()["environment"]


def test_settings_accepts_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    config_module = import_module("aignt_os.config")
    monkeypatch.setenv("AIGNT_OS_APP_NAME", "AIgnt OS Test")

    settings = config_module.AppSettings()

    assert settings.app_name == "AIgnt OS Test"


def test_settings_exposes_runtime_state_file(monkeypatch: pytest.MonkeyPatch) -> None:
    config_module = import_module("aignt_os.config")
    monkeypatch.setenv("AIGNT_OS_RUNTIME_STATE_DIR", ".runtime-state")

    settings = config_module.AppSettings()

    assert settings.runtime_state_dir.name == ".runtime-state"
    assert settings.runtime_state_file.name == "runtime-state.json"


def test_settings_exposes_run_persistence_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    config_module = import_module("aignt_os.config")
    monkeypatch.setenv("AIGNT_OS_RUNS_DB_PATH", ".runtime/runs.sqlite3")
    monkeypatch.setenv("AIGNT_OS_ARTIFACTS_DIR", ".runtime/artifacts")

    settings = config_module.AppSettings()

    assert settings.runs_db_path.name == "runs.sqlite3"
    assert settings.artifacts_dir.name == "artifacts"


def test_settings_rejects_invalid_environment_value() -> None:
    config_module = import_module("aignt_os.config")

    with pytest.raises(ValidationError):
        config_module.AppSettings(environment="invalid")
