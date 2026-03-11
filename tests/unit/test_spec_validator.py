from importlib import import_module
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "specs"


def _validator_module():
    return import_module("aignt_os.specs.validator")


def test_valid_spec_file_returns_structured_document() -> None:
    validator = _validator_module()

    document = validator.validate_spec_file(FIXTURES_DIR / "valid_feature_spec.md")

    assert document.metadata.id == "F02-spec-engine-mvp"
    assert document.metadata.type == "feature"
    assert document.metadata.acceptance_criteria == ["YAML front matter is required."]
    assert "Contexto" in document.sections
    assert "Objetivo" in document.sections


def test_valid_spec_exposes_body_stripped() -> None:
    validator = _validator_module()

    document = validator.validate_spec_file(FIXTURES_DIR / "valid_feature_spec.md")

    assert document.body
    assert not document.body.startswith("\n")
    assert not document.body.endswith("\n")


def test_spec_without_yaml_front_matter_is_rejected() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="front matter"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_missing_yaml_spec.md")


def test_spec_requires_non_empty_acceptance_criteria() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="acceptance_criteria"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_acceptance_criteria_spec.md")


def test_spec_requires_context_section() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="Contexto"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_missing_context_spec.md")


def test_spec_requires_objetivo_section() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="Objetivo"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_missing_objetivo_spec.md")


def test_spec_rejects_empty_inputs_list() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="inputs"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_empty_inputs_spec.md")


def test_spec_rejects_missing_id_field() -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="id"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_missing_id_spec.md")


def test_spec_rejects_h2_sections_as_not_recognized() -> None:
    """The parser only recognises H1 headings; H2 sections must not satisfy the requirement."""
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match="Contexto"):
        validator.validate_spec_file(FIXTURES_DIR / "invalid_h2_sections_spec.md")


@pytest.mark.parametrize(
    "fixture_name, expected_match",
    [
        ("invalid_missing_yaml_spec.md", "front matter"),
        ("invalid_acceptance_criteria_spec.md", "acceptance_criteria"),
        ("invalid_missing_context_spec.md", "Contexto"),
        ("invalid_missing_objetivo_spec.md", "Objetivo"),
        ("invalid_empty_inputs_spec.md", "inputs"),
        ("invalid_missing_id_spec.md", "id"),
        ("invalid_h2_sections_spec.md", "Contexto"),
    ],
)
def test_all_invalid_fixture_specs_raise_spec_validation_error(
    fixture_name: str, expected_match: str
) -> None:
    validator = _validator_module()

    with pytest.raises(validator.SpecValidationError, match=expected_match):
        validator.validate_spec_file(FIXTURES_DIR / fixture_name)


def test_spec_accepts_empty_non_goals(tmp_path: Path) -> None:
    """non_goals is allowed to be an empty list per the validator contract."""
    validator = _validator_module()
    spec = tmp_path / "SPEC.md"
    spec.write_text(
        """\
---
id: F-empty-non-goals
type: feature
summary: SPEC com non_goals vazio.
inputs:
  - input_a
outputs:
  - output_a
acceptance_criteria:
  - must pass
non_goals: []
---

# Contexto

Teste de non_goals vazio.

# Objetivo

Confirmar que non_goals vazio e aceito.
""",
        encoding="utf-8",
    )

    document = validator.validate_spec_file(spec)

    assert document.metadata.non_goals == []


def test_spec_accepts_unicode_in_summary_and_criteria(tmp_path: Path) -> None:
    validator = _validator_module()
    spec = tmp_path / "SPEC.md"
    spec.write_text(
        """\
---
id: F-unicode
type: feature
summary: "Resumo com acentuação: São Paulo → UTF-8 ✓"
inputs:
  - entrada_α
outputs:
  - saída_β
acceptance_criteria:
  - "Critério com ç e ñ deve ser aceito"
non_goals:
  - nada além do escopo
---

# Contexto

Conteúdo com caracteres especiais: ã, é, ü, ñ, 中文.

# Objetivo

Validar que Unicode em todos os campos é suportado.
""",
        encoding="utf-8",
    )

    document = validator.validate_spec_file(spec)

    assert "UTF-8" in document.metadata.summary
    assert "ç" in document.metadata.acceptance_criteria[0]
