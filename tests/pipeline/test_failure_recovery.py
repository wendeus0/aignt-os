"""Pipeline failure recovery tests.

Tests cover failure handling in the Synapse-Flow pipeline engine:
- observer notification on failure
- exception propagation with context preservation
- SPEC validation errors vs execution errors
- partial step_history before failure
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

_VALID_SPEC_CONTENT = """\
---
id: F-failure-recovery-fixture
type: feature
summary: Fixture spec for failure recovery tests.
inputs:
  - raw_request
outputs:
  - plan_md
acceptance_criteria:
  - Pipeline must propagate executor failures cleanly.
non_goals:
  - Real subprocess execution.
---

# Contexto

Fixture para testes de recuperação de falha.

# Objetivo

Verificar que a pipeline propaga erros corretamente ao observer.
"""

_INVALID_SPEC_CONTENT = "# Sem front matter YAML\n"


def _make_spec(tmp_path: Path, content: str) -> Path:
    spec = tmp_path / "SPEC.md"
    spec.write_text(content, encoding="utf-8")
    return spec


def _pipeline_module():
    from importlib import import_module

    return import_module("synapse_os.pipeline")


class _FakeExecutor:
    def __init__(self, **artifacts: str) -> None:
        self._artifacts = artifacts
        self.calls: list[str] = []

    def execute(self, step, context):  # type: ignore[no-untyped-def]
        self.calls.append(step.state)
        pipeline = _pipeline_module()
        return pipeline.StepExecutionResult(artifacts=dict(self._artifacts))


class _FailingExecutor:
    def __init__(self, message: str = "Fake failure") -> None:
        self._message = message

    def execute(self, step, context):  # type: ignore[no-untyped-def]
        pipeline = _pipeline_module()
        raise pipeline.PipelineExecutionError(self._message)


class _RecordingObserver:
    """Records all observer calls for assertion."""

    def __init__(self) -> None:
        self.started: list[Any] = []
        self.completed_steps: list[Any] = []
        self.run_completed: list[Any] = []
        self.failed: list[tuple[Any, Any, Any]] = []

    def on_run_started(self, context) -> None:  # type: ignore[no-untyped-def]
        self.started.append(context)

    def on_step_completed(self, step, context, result) -> None:  # type: ignore[no-untyped-def]
        self.completed_steps.append((step.state, context.current_state))

    def on_run_completed(self, context) -> None:  # type: ignore[no-untyped-def]
        self.run_completed.append(context)

    def on_run_failed(self, context, step, exc) -> None:  # type: ignore[no-untyped-def]
        self.failed.append((context, step, exc))


def test_failure_recovery_observer_receives_on_run_failed_when_plan_executor_raises(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor("plan failed"), "TEST_RED": _FakeExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    assert len(observer.failed) == 1
    _context, _step, exc = observer.failed[0]
    assert "plan failed" in str(exc)


def test_failure_recovery_observer_receives_failing_step_info(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor(), "TEST_RED": _FakeExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    _context, step, _exc = observer.failed[0]
    assert step is not None
    assert step.state == "PLAN"


def test_failure_recovery_observer_on_run_started_called_before_failure(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    assert len(observer.started) == 1
    assert len(observer.run_completed) == 0


def test_failure_recovery_spec_validation_completes_before_plan_failure(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    completed_states = [s for s, _ in observer.completed_steps]
    assert "SPEC_VALIDATION" in completed_states


def test_failure_recovery_observer_receives_spec_validation_error_type(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _INVALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FakeExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.SpecValidationError):
        engine.run(spec)

    assert len(observer.failed) == 1
    _context, _step, exc = observer.failed[0]
    assert isinstance(exc, pipeline.SpecValidationError)


def test_failure_recovery_step_history_preserved_after_partial_execution(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    context, _step, _exc = observer.failed[0]
    assert "SPEC_VALIDATION" in context.step_history


def test_failure_recovery_missing_executor_raises_pipeline_execution_error(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    engine = pipeline.PipelineEngine(executors={})

    with pytest.raises(pipeline.PipelineExecutionError, match="Missing executor"):
        engine.run(spec)


def test_failure_recovery_run_completed_not_called_when_failure_occurs(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": _FailingExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec)

    assert len(observer.run_completed) == 0
    assert len(observer.failed) == 1


def test_failure_recovery_failing_test_red_executor_still_called_plan_observer(
    tmp_path: Path,
) -> None:
    pipeline = _pipeline_module()
    spec = _make_spec(tmp_path, _VALID_SPEC_CONTENT)
    plan_executor = _FakeExecutor(plan_md="plan content")
    observer = _RecordingObserver()
    engine = pipeline.PipelineEngine(
        executors={"PLAN": plan_executor, "TEST_RED": _FailingExecutor()},
        observer=observer,
    )

    with pytest.raises(pipeline.PipelineExecutionError):
        engine.run(spec, stop_at="TEST_RED")

    assert len(plan_executor.calls) == 1
    completed_states = [s for s, _ in observer.completed_steps]
    assert "PLAN" in completed_states
    assert len(observer.failed) == 1
