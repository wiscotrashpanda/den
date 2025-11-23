import typer
from rich import print
from typing import Optional
from denctl import __version__
from denctl.commands.hello import hello
from denctl.commands import homebrew
from denctl.commands import auth

app = typer.Typer(
    name="denctl",
    help="denctl - 🦝 automation CLI",
    no_args_is_help=True,
)

# Register commands
app.command(name="hello")(hello)
app.add_typer(homebrew.app, name="homebrew")
app.add_typer(auth.app, name="auth")


def version_callback(value: bool):
    if value:
        print(f"denctl version: [bold blue]{__version__}[/bold blue]")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Show version and exit.",
    ),
):
    pass


def main() -> None:
    app()


if __name__ == "__main__":
    main()
