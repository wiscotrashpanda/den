import typer
from rich.console import Console

console = Console()


def hello(name: str = typer.Argument("World", help="Name to greet")):
    """Say hello to someone."""
    console.print(f"[bold green]Hello {name}![/bold green]")
