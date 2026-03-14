"""Pipeline full-flow integration tests (F49).

Tests exercise the Synapse-Flow pipeline — the engine própria de pipeline
do SynapseOS — through the complete execution path: SPEC_VALIDATION →
PLAN → TEST_RED → CODE_GREEN → QUALITY_GATE → REVIEW → SECURITY → DOCUMENT.

These tests close the coverage gap documented in test_review_rework.py
(which exercised only the state machine directly) and extend test_happy_path.py
to cover the final execution states (QUALITY_GATE, REVIEW, SECURITY, DOCUMENT).

No real subprocesses or external tools are invoked.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_VALID_SPEC_CONTENT = """\
---
id: F49-full-flow-fixture
type: feature
summary: Full-flow fixture spec for F49 pipeline integration tests.
inputs:
  - raw_request
outputs:
  - plan_md
  - tests_md
  - code_md
  - run_report_md
acceptance_criteria:
  - Pipeline must execute all states from SPEC_VALIDATION to DOCUMENT.
  - Pipeline must support stop_at=DOCUMENT.
non_goals:
  - Real subprocess execution.
  - Worker or scheduler integration.
---

# Contexto

Fixture para testes de integração do fluxo completo do Synapse-Flow (F49).

# Objetivo

Exercitar a pipeline do SynapseOS do início ao fim usando executores fake
e verificar hand-offs entre os estados finais do fluxo linear.
"""


def _make_spec(tmp_path: Path, content: str = _VALID_SPEC_CONTENT) -> Path:
    spec = tmp_path / "SPEC.md"
    spec.write_text(content, encoding="utf-8")
    return spec


def _pipeline_module():
    from importlib import import_module

    return import_module("synapse_os.pipeline")


class _FakeExecutor:
    """Records every call and returns a fixed artifact set."""

    def __init__(self, **artifacts: str) -> None:
        self._artifacts = artifacts
        self.calls: list[str] = []

    def execute(self, step, context):  # type: ignore[no-untyped-def]
        self.calls.append(step.state)
        pipeline = _pipeline_module()
        return pipeline.StepExecutionResult(artifacts=dict(self._artifacts))


class _ReworkOnceReviewExecutor:
    """Raises ReviewRejectedError on the first call; succeeds on subsequent calls."""

    def __init__(self) -> None:
        self.call_count = 0

    def execute(self, step, context):  # type: ignore[no-untyped-def]
        from synapse_os.supervisor import ReviewRejectedError

        self.call_count += 1
        if self.call_count == 1:
            raise ReviewRejectedError("Rework requested by reviewer.")
        pipeline = _pipeline_module()
        return pipeline.StepExecutionResult(artifacts={"review_md": "# Approved"})


def _full_executors(**document_artifacts: str) -> dict:
    """Return a dict with fake executors for all seven execution states."""
    return {
        "PLAN": _FakeExecutor(plan_md="# Plan"),
        "TEST_RED": _FakeExecutor(tests_md="# Tests"),
        "CODE_GREEN": _FakeExecutor(code_md="# Code"),
        "QUALITY_GATE": _FakeExecutor(),
        "REVIEW": _FakeExecutor(review_md="# Review"),
        "SECURITY": _FakeExecutor(security_md="# Security"),
        "DOCUMENT": _FakeExecutor(**document_artifacts),
    }


# ---------------------------------------------------------------------------
# Criterion 1 — full flow: step_history contains all execution states in order
# ---------------------------------------------------------------------------


def test_pipeline_full_flow_step_history_contains_code_green_through_document(
    tmp_path: Path,
) -> None:
    """Criterion 1: step_history records all execution states in order."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    context = pipeline.PipelineEngine(executors=_full_executors()).run(
        spec_path, stop_at="DOCUMENT"
    )

    expected_tail = [
        "CODE_GREEN",
        "QUALITY_GATE",
        "REVIEW",
        "SECURITY",
        "DOCUMENT",
    ]
    history = context.step_history
    for state in expected_tail:
        assert state in history, f"Expected '{state}' in step_history, got: {history}"

    # Verify linear order within the tail
    for i, state in enumerate(expected_tail[:-1]):
        assert history.index(state) < history.index(
            expected_tail[i + 1]
        ), f"Expected '{state}' before '{expected_tail[i + 1]}' in step_history"


def test_pipeline_full_flow_step_history_starts_with_spec_validation_and_plan(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    context = pipeline.PipelineEngine(executors=_full_executors()).run(
        spec_path, stop_at="DOCUMENT"
    )

    assert context.step_history[0] == "SPEC_VALIDATION"
    assert context.step_history[1] == "PLAN"


# ---------------------------------------------------------------------------
# Criterion 2 — stop_at="DOCUMENT" halts at DOCUMENT without reaching COMPLETE
# ---------------------------------------------------------------------------


def test_pipeline_stop_at_document_returns_document_as_current_state(
    tmp_path: Path,
) -> None:
    """Criterion 2: stop_at='DOCUMENT' terminates the run at DOCUMENT state."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    context = pipeline.PipelineEngine(executors=_full_executors()).run(
        spec_path, stop_at="DOCUMENT"
    )

    assert context.current_state == "DOCUMENT"


def test_pipeline_stop_at_document_is_accepted_as_valid_stop_at_value(
    tmp_path: Path,
) -> None:
    """Criterion 2: 'DOCUMENT' is a valid stop_at value (no ValueError raised)."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    # Must not raise ValueError("Unsupported stop_at state")
    context = pipeline.PipelineEngine(executors=_full_executors()).run(
        spec_path, stop_at="DOCUMENT"
    )

    assert "DOCUMENT" in context.step_history


def test_pipeline_stop_at_document_does_not_invoke_any_executor_after_document(
    tmp_path: Path,
) -> None:
    """Criterion 2: no executor runs after DOCUMENT when stop_at='DOCUMENT'."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)
    executors = _full_executors()
    document_exec = executors["DOCUMENT"]
    assert isinstance(document_exec, _FakeExecutor)

    pipeline.PipelineEngine(executors=executors).run(spec_path, stop_at="DOCUMENT")

    # DOCUMENT executor was called exactly once
    assert document_exec.calls == ["DOCUMENT"]


# ---------------------------------------------------------------------------
# Criterion 3 — DOCUMENT executor artifact is present in context.artifacts
# ---------------------------------------------------------------------------


def test_pipeline_document_executor_artifact_run_report_md_is_in_context(
    tmp_path: Path,
) -> None:
    """Criterion 3: artifact produced by DOCUMENT executor is in context.artifacts."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    context = pipeline.PipelineEngine(
        executors=_full_executors(run_report_md="# Run Report\n\nAll steps completed.")
    ).run(spec_path, stop_at="DOCUMENT")

    assert "run_report_md" in context.artifacts
    assert context.artifacts["run_report_md"] == "# Run Report\n\nAll steps completed."


def test_pipeline_document_executor_artifacts_are_merged_with_prior_step_artifacts(
    tmp_path: Path,
) -> None:
    """Criterion 3: artifacts from all steps are accessible after DOCUMENT."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    context = pipeline.PipelineEngine(
        executors=_full_executors(run_report_md="# Report")
    ).run(spec_path, stop_at="DOCUMENT")

    # Artifacts from earlier steps must still be present
    assert "plan_md" in context.artifacts
    assert "tests_md" in context.artifacts
    assert "code_md" in context.artifacts
    assert "run_report_md" in context.artifacts


# ---------------------------------------------------------------------------
# Criterion 4 — rework: REVIEW → CODE_GREEN via PipelineEngine
# ---------------------------------------------------------------------------


def test_pipeline_review_rework_records_review_in_step_history_before_second_code_green(
    tmp_path: Path,
) -> None:
    """Criterion 4 (migrated from test_review_rework): rework transition is recorded."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    review_exec = _ReworkOnceReviewExecutor()
    executors = {
        "PLAN": _FakeExecutor(plan_md="# Plan"),
        "TEST_RED": _FakeExecutor(tests_md="# Tests"),
        "CODE_GREEN": _FakeExecutor(code_md="# Code"),
        "QUALITY_GATE": _FakeExecutor(),
        "REVIEW": review_exec,
        "SECURITY": _FakeExecutor(security_md="# Security"),
        "DOCUMENT": _FakeExecutor(run_report_md="# Report"),
    }

    context = pipeline.PipelineEngine(executors=executors).run(
        spec_path, stop_at="DOCUMENT"
    )

    history = context.step_history
    # REVIEW must appear at least once (the rework trigger)
    assert "REVIEW" in history

    # CODE_GREEN must appear at least twice: original + rework re-run
    code_green_indices = [i for i, s in enumerate(history) if s == "CODE_GREEN"]
    assert len(code_green_indices) >= 2, (
        f"Expected CODE_GREEN at least twice in step_history (rework loop), got: {history}"
    )

    # The first REVIEW must precede the second CODE_GREEN
    first_review_idx = history.index("REVIEW")
    second_code_green_idx = code_green_indices[1]
    assert first_review_idx < second_code_green_idx, (
        f"Expected first REVIEW before second CODE_GREEN in step_history, got: {history}"
    )


def test_pipeline_review_rework_review_executor_is_called_twice_after_one_rework(
    tmp_path: Path,
) -> None:
    """Criterion 4: REVIEW executor is invoked again after rework returns to CODE_GREEN."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    review_exec = _ReworkOnceReviewExecutor()
    executors = {
        "PLAN": _FakeExecutor(plan_md="# Plan"),
        "TEST_RED": _FakeExecutor(tests_md="# Tests"),
        "CODE_GREEN": _FakeExecutor(code_md="# Code"),
        "QUALITY_GATE": _FakeExecutor(),
        "REVIEW": review_exec,
        "SECURITY": _FakeExecutor(security_md="# Security"),
        "DOCUMENT": _FakeExecutor(run_report_md="# Report"),
    }

    pipeline.PipelineEngine(executors=executors).run(spec_path, stop_at="DOCUMENT")

    # Review executor was called twice: once for the rework, once for the success
    assert review_exec.call_count == 2


def test_pipeline_review_rework_completes_successfully_after_single_rework_cycle(
    tmp_path: Path,
) -> None:
    """Criterion 4: pipeline reaches DOCUMENT without error after rework cycle."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    executors = {
        "PLAN": _FakeExecutor(plan_md="# Plan"),
        "TEST_RED": _FakeExecutor(tests_md="# Tests"),
        "CODE_GREEN": _FakeExecutor(code_md="# Code"),
        "QUALITY_GATE": _FakeExecutor(),
        "REVIEW": _ReworkOnceReviewExecutor(),
        "SECURITY": _FakeExecutor(security_md="# Security"),
        "DOCUMENT": _FakeExecutor(run_report_md="# Report"),
    }

    context = pipeline.PipelineEngine(executors=executors).run(
        spec_path, stop_at="DOCUMENT"
    )

    assert context.current_state == "DOCUMENT"
    assert "DOCUMENT" in context.step_history


# ---------------------------------------------------------------------------
# Criterion 5 — full path from TEST_RED to DOCUMENT without rework
# ---------------------------------------------------------------------------


def test_pipeline_full_path_without_rework_runs_all_states_without_error(
    tmp_path: Path,
) -> None:
    """Criterion 5: pipeline runs TEST_RED through DOCUMENT without error or rework."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)

    # Should not raise any exception
    context = pipeline.PipelineEngine(executors=_full_executors()).run(
        spec_path, stop_at="DOCUMENT"
    )

    assert "TEST_RED" in context.step_history
    assert "CODE_GREEN" in context.step_history
    assert "QUALITY_GATE" in context.step_history
    assert "REVIEW" in context.step_history
    assert "SECURITY" in context.step_history
    assert "DOCUMENT" in context.step_history


def test_pipeline_full_path_without_rework_each_executor_called_exactly_once(
    tmp_path: Path,
) -> None:
    """Criterion 5: without rework, each executor is invoked exactly once."""
    pipeline = _pipeline_module()
    spec_path = _make_spec(tmp_path)
    executors = _full_executors()

    pipeline.PipelineEngine(executors=executors).run(spec_path, stop_at="DOCUMENT")

    for state, exec_ in executors.items():
        assert isinstance(exec_, _FakeExecutor)
        assert exec_.calls == [state], (
            f"Executor for '{state}' expected exactly 1 call, got: {exec_.calls}"
        )
