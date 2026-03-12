from __future__ import annotations

from aignt_os.cli.errors import (
    CLIExitCode,
    format_cli_error,
)


def test_format_cli_error_prefixes_messages_by_category() -> None:
    assert format_cli_error(CLIExitCode.USAGE, "bad option") == "Usage error: bad option"
    assert format_cli_error(CLIExitCode.NOT_FOUND, "missing run") == "Not found: missing run"
    assert (
        format_cli_error(CLIExitCode.VALIDATION, "invalid spec") == "Validation error: invalid spec"
    )
    assert (
        format_cli_error(CLIExitCode.ENVIRONMENT, "runtime not ready")
        == "Environment error: runtime not ready"
    )
    assert (
        format_cli_error(CLIExitCode.EXECUTION, "dispatch exploded")
        == "Execution error: dispatch exploded"
    )
