"""Integration tests: CLI adapter output → parsing engine → ParsedOutput.

Tests validate the full flow from raw adapter output through the parsing
engine, ensuring the integration produces structured, clean results.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from aignt_os import parsing

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "cli_outputs"


def _read_fixture(name: str, *, unicode_escape: bool = False) -> str:
    raw = (FIXTURES_DIR / name).read_text(encoding="utf-8")
    if unicode_escape:
        return raw.encode("utf-8").decode("unicode_escape")
    return raw


def test_adapter_parser_flow_produces_parsed_output_from_noisy_mixed_input() -> None:
    raw = _read_fixture("noisy_mixed_output.txt", unicode_escape=True)

    result = parsing.parse_cli_output(raw)

    assert result.stdout_raw == raw
    assert "[transport]" not in result.stdout_clean
    assert result.stdout_clean != raw


def test_adapter_parser_flow_extracts_python_artifact_from_mixed_output() -> None:
    raw = _read_fixture("noisy_mixed_output.txt", unicode_escape=True)

    result = parsing.parse_cli_output(raw)

    assert len(result.artifacts) == 1
    assert result.artifacts[0].language == "python"
    assert "greet" in result.artifacts[0].content


def test_adapter_parser_flow_strips_ansi_sequences_from_clean_output() -> None:
    raw = _read_fixture("noisy_mixed_output.txt", unicode_escape=True)

    result = parsing.parse_cli_output(raw)

    assert "\x1b[" not in result.stdout_clean
    assert "\x1b[" in result.stdout_raw


def test_adapter_parser_flow_preserves_raw_output_unchanged() -> None:
    raw = _read_fixture("noisy_mixed_output.txt", unicode_escape=True)

    result = parsing.parse_cli_output(raw)

    assert result.stdout_raw == raw
    assert "[transport]" in result.stdout_raw


def test_adapter_parser_flow_handles_gemini_plan_output() -> None:
    raw = _read_fixture("gemini_plan.txt")

    result = parsing.parse_cli_output(raw)

    assert result.stdout_clean
    assert len(result.artifacts) >= 1
    assert result.artifacts[0].language == "python"


def test_adapter_parser_flow_handles_codex_tests_output() -> None:
    raw = _read_fixture("codex_tests.txt")

    result = parsing.parse_cli_output(raw)

    assert result.stdout_clean
    assert len(result.artifacts) == 1
    assert result.artifacts[0].language == "python"
    assert "def test_" in result.artifacts[0].content


def test_adapter_parser_flow_handles_claude_review_output() -> None:
    raw = _read_fixture("claude_review.txt")

    result = parsing.parse_cli_output(raw)

    assert result.stdout_clean
    assert len(result.artifacts) == 1
    assert result.artifacts[0].language == "python"


def test_adapter_parser_flow_validates_python_artifact_syntax() -> None:
    raw = _read_fixture("gemini_plan.txt")
    result = parsing.parse_cli_output(raw)

    for artifact in result.artifacts:
        if artifact.language == "python":
            parsing.validate_python_artifact(artifact)


def test_adapter_parser_flow_raises_for_artifact_exceeding_size_limit() -> None:
    oversized_block = "```python\n" + "x = 1\n" * (128 * 1024 // 6 + 1) + "```"

    with pytest.raises(parsing.ParsingArtifactError, match="too large"):
        parsing.parse_cli_output(oversized_block)


def test_adapter_parser_flow_full_round_trip_noisy_to_structured() -> None:
    raw = _read_fixture("noisy_mixed_output.txt", unicode_escape=True)

    result = parsing.parse_cli_output(raw)

    assert result.stdout_raw
    assert result.stdout_clean
    assert result.stdout_clean != result.stdout_raw
    assert isinstance(result.artifacts, list)
    assert all(a.content for a in result.artifacts)
