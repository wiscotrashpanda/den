"""Authentication commands for external services.

This module provides the auth command group for managing credentials
for external services like Anthropic.
"""

from dataclasses import dataclass

import typer

from den.auth_storage import save_credential


@dataclass
class Provider:
    """Configuration for an authentication provider.

    Attributes:
        name: Display name for the provider.
        key_name: Key used in auth.json storage.
        prompt_text: Text shown when prompting for credentials.
    """

    name: str
    key_name: str
    prompt_text: str


PROVIDERS: dict[str, Provider] = {
    "Anthropic": Provider(
        name="Anthropic",
        key_name="anthropic_api_key",
        prompt_text="Enter your Anthropic API key",
    ),
    "GitHub": Provider(
        name="GitHub",
        key_name="github_token",
        prompt_text="Enter your GitHub personal access token",
    ),
}


def validate_api_key(api_key: str) -> bool:
    """Validate that an API key is non-empty.

    Args:
        api_key: The API key string to validate.

    Returns:
        True if the API key is valid (non-empty), False otherwise.
    """
    return len(api_key.strip()) > 0


auth_app = typer.Typer(help="Authentication commands for external services.")


@auth_app.command()
def login() -> None:
    """Log in to an external service by providing credentials."""
    # Display provider selection prompt
    provider_names = list(PROVIDERS.keys())

    typer.echo("Select an authentication provider:")
    for i, name in enumerate(provider_names, 1):
        typer.echo(f"  {i}. {name}")

    try:
        choice = typer.prompt(
            "Enter provider number",
            type=int,
            default=1,
        )
    except typer.Abort:
        raise typer.Exit(0)

    # Validate choice
    if choice < 1 or choice > len(provider_names):
        typer.echo(f"Invalid choice. Please select 1-{len(provider_names)}.")
        raise typer.Exit(1)

    provider_name = provider_names[choice - 1]
    provider = PROVIDERS[provider_name]

    # Prompt for API key with masked input
    while True:
        try:
            api_key = typer.prompt(
                provider.prompt_text,
                hide_input=True,
            )
        except typer.Abort:
            raise typer.Exit(0)

        if validate_api_key(api_key):
            break
        else:
            typer.echo("Error: API key cannot be empty. Please try again.")

    # Save the credential
    try:
        save_credential(provider.key_name, api_key)
        typer.echo(f"Successfully saved {provider.name} credentials")
    except OSError as e:
        typer.echo(f"Error: Failed to save credentials - {e}")
        raise typer.Exit(1)
