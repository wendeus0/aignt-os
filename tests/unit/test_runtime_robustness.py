import time
from unittest.mock import MagicMock, patch

import pytest

from synapse_os.config import AppSettings
from synapse_os.pipeline import (
    PipelineContext,
    PipelineEngine,
    PipelineStep,
    StepExecutionResult,
)
from synapse_os.supervisor import RetryableStepError


@pytest.fixture
def mock_settings():
    return AppSettings(
        execution_timeout_seconds=0.1,  # Fast timeout for testing
        max_retries=2,
    )


def test_pipeline_respects_execution_timeout(mock_settings):
    """Test that pipeline stops step execution when timeout is exceeded."""
    # Setup a slow executor that sleeps longer than timeout
    mock_executor = MagicMock()

    def slow_execute(*args, **kwargs):
        time.sleep(0.3)
        return StepExecutionResult(clean_output="finished")

    mock_executor.execute = MagicMock(side_effect=slow_execute)

    # Register executor for PLAN step
    executors = {"PLAN": mock_executor}

    engine = PipelineEngine(settings=mock_settings, executors=executors)

    mock_step = MagicMock(spec=PipelineStep)
    mock_step.state = "PLAN"
    mock_context = MagicMock(spec=PipelineContext)

    # We verify that RetryableStepError is raised (which wraps TimeoutError)
    with pytest.raises(RetryableStepError, match="exceeded timeout"):
        engine._execute_runtime_step(mock_step, mock_context)


def test_pipeline_retries_on_transient_failure(mock_settings):
    """Test that pipeline retries a step that fails with a recoverable error."""
    # Create engine with default supervisor (using max_retries=2 from settings)
    engine = PipelineEngine(settings=mock_settings)

    mock_step = MagicMock(spec=PipelineStep)
    mock_step.state = "PLAN"
    mock_context = MagicMock(spec=PipelineContext)
    mock_context.supervisor_decisions = []

    # Mock _execute_runtime_step to fail twice then succeed
    with patch.object(engine, "_execute_runtime_step") as mock_exec:
        success_result = StepExecutionResult(clean_output="success")

        mock_exec.side_effect = [
            RetryableStepError("fail 1"),
            RetryableStepError("fail 2"),
            success_result,
        ]

        result = engine._run_runtime_step(mock_step, mock_context)

        assert result == success_result
        assert mock_exec.call_count == 3
        # Check supervisor decisions recorded in context
        assert len(mock_context.supervisor_decisions) == 2
        assert "retry:PLAN" in mock_context.supervisor_decisions[0]
        assert "retry:PLAN" in mock_context.supervisor_decisions[1]


def test_pipeline_fails_after_max_retries_exceeded(mock_settings):
    """Test that pipeline fails after max retries are exhausted."""
    engine = PipelineEngine(settings=mock_settings)

    mock_step = MagicMock(spec=PipelineStep)
    mock_step.state = "PLAN"
    mock_context = MagicMock(spec=PipelineContext)
    mock_context.supervisor_decisions = []

    with patch.object(engine, "_execute_runtime_step") as mock_exec:
        mock_exec.side_effect = RetryableStepError("always fail")

        # max_retries=2, so:
        # 1. Initial attempt -> fail
        # 2. Retry 1 -> fail
        # 3. Retry 2 -> fail
        # 4. Fail (raise)

        with pytest.raises(RetryableStepError, match="always fail"):
            engine._run_runtime_step(mock_step, mock_context)

        assert mock_exec.call_count == 3
