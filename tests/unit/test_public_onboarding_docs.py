from __future__ import annotations

from pathlib import Path

README_PATH = Path(__file__).resolve().parents[2] / "README.md"


def _readme_text() -> str:
    return README_PATH.read_text(encoding="utf-8")


def test_readme_includes_public_first_run_quickstart_and_boundary() -> None:
    readme = _readme_text()

    assert "## Primeira Run Publica" in readme
    assert "`aignt doctor`" in readme
    assert "`aignt runs submit <spec_path> --mode sync --stop-at SPEC_VALIDATION`" in readme
    assert "`aignt runs show <run_id>`" in readme
    assert "`repo-preflight`" in readme
    assert "nao substitui" in readme.lower()


def test_readme_troubleshooting_covers_doctor_checks_and_invalid_spec() -> None:
    readme = _readme_text()

    assert "`runtime_state`" in readme
    assert "`runs_db`" in readme
    assert "`artifacts_dir`" in readme
    assert "`warn`" in readme
    assert "SPEC invalida" in readme
    assert "sync-first" in readme
