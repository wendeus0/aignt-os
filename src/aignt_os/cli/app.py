import typer

from aignt_os import __version__
from aignt_os.config import AppSettings
from aignt_os.runtime.service import RuntimeLifecycleError, RuntimeService


app = typer.Typer(help="AIgnt OS CLI")
runtime_app = typer.Typer(help="Manage the minimal persistent runtime.")
app.add_typer(runtime_app, name="runtime")


@app.callback()
def main() -> None:
    return None


@app.command()
def version() -> None:
    typer.echo(__version__)


def _runtime_service() -> RuntimeService:
    settings = AppSettings()
    try:
        return RuntimeService(settings.runtime_state_file)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


@runtime_app.command("start")
def runtime_start() -> None:
    service = _runtime_service()
    try:
        state = service.start()
    except RuntimeLifecycleError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Runtime status: {state.status} (pid={state.pid})")


@runtime_app.command("status")
def runtime_status() -> None:
    service = _runtime_service()
    state = service.status()

    if state.status == "inconsistent":
        typer.echo("Runtime status: inconsistent", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Runtime status: {state.status}")


@runtime_app.command("stop")
def runtime_stop() -> None:
    service = _runtime_service()
    try:
        state = service.stop()
    except RuntimeLifecycleError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Runtime status: {state.status}")
