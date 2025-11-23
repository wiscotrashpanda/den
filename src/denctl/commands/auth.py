import typer
import json
from pathlib import Path
from typing import Dict, Any
from rich.console import Console

app = typer.Typer(name="auth", help="Manage authentication credentials.")
console = Console()

CONFIG_DIR = Path.home() / ".config" / "denctl"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_general_config() -> Dict[str, Any]:
    """Load general configuration from JSON file."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def save_general_config(config: Dict[str, Any]) -> None:
    """Save general configuration to JSON file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    # Ensure privacy
    CONFIG_FILE.chmod(0o600)


@app.command()
def anthropic():
    """
    Prompt for and save the Anthropic API key.
    """
    key = typer.prompt("Enter your Anthropic API Key", hide_input=True)
    if not key.startswith("sk-"):
        console.print("[yellow]Warning: Key does not start with 'sk-'.[/yellow]")

    config = get_general_config()
    config["anthropic_api_key"] = key
    save_general_config(config)
    console.print(f"[green]API Key saved to {CONFIG_FILE}[/green]")
