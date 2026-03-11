"""Shared fixtures for unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture()
def valid_spec_path(tmp_path: Path) -> Path:
    """Write a minimal valid SPEC to a temporary file and return its path."""
    spec = tmp_path / "SPEC.md"
    spec.write_text(
        """\
---
id: F-test-fixture
type: feature
summary: Minimal valid fixture spec.
inputs:
  - raw_request
outputs:
  - validated_spec
acceptance_criteria:
  - The validator must accept this SPEC.
non_goals:
  - Everything else.
---

# Contexto

Fixture para testes unitarios.

# Objetivo

Confirmar que uma SPEC minima valida passa na validacao.
""",
        encoding="utf-8",
    )
    return spec


@pytest.fixture()
def invalid_spec_path(tmp_path: Path) -> Path:
    """Write an invalid SPEC (no front matter) to a temporary file and return its path."""
    spec = tmp_path / "SPEC.md"
    spec.write_text("# Contexto\n\nSem front matter YAML.\n", encoding="utf-8")
    return spec


@pytest.fixture()
def spec_fixtures_dir() -> Path:
    """Return the path to the specs fixtures directory."""
    return FIXTURES_DIR / "specs"


@pytest.fixture()
def cli_fixtures_dir() -> Path:
    """Return the path to the cli_outputs fixtures directory."""
    return FIXTURES_DIR / "cli_outputs"
