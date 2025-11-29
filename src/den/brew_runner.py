"""Brew runner module for executing Homebrew commands.

This module handles execution of Homebrew commands including brew upgrade
and brew bundle dump for generating Brewfiles.
"""

import os
import shutil
import subprocess


class BrewCommandError(Exception):
    """Exception raised when a Homebrew command fails."""

    def __init__(self, command: str, returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(f"Command '{command}' failed with code {returncode}: {stderr}")


def _get_brew_context() -> tuple[str, dict[str, str]]:
    """Resolve brew executable path and environment.

    Ensures brew is found even when running in restricted environments (like launchd)
    by checking common Homebrew installation paths.

    Returns:
        Tuple of (brew_executable_path, environment_dict)
    """
    env = os.environ.copy()
    current_path = env.get("PATH", "")

    # Common Homebrew paths to check
    brew_prefixes = ["/opt/homebrew/bin", "/usr/local/bin"]
    valid_prefixes = [p for p in brew_prefixes if os.path.isdir(p)]

    # Update PATH in env to include Homebrew paths
    full_path = current_path
    if valid_prefixes:
        # Prepend to ensure they are found first
        full_path = f"{os.pathsep.join(valid_prefixes)}{os.pathsep}{current_path}"
    env["PATH"] = full_path

    # Resolve executable using the augmented path
    brew_exec = shutil.which("brew", path=full_path) or "brew"

    return brew_exec, env


def run_brew_upgrade() -> None:
    """Execute brew upgrade command to update all installed packages.

    Raises:
        BrewCommandError: If brew upgrade fails.
    """
    brew_cmd, env = _get_brew_context()
    try:
        result = subprocess.run(
            [brew_cmd, "upgrade"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        if result.returncode != 0:
            raise BrewCommandError("brew upgrade", result.returncode, result.stderr)
    except FileNotFoundError as e:
        raise BrewCommandError("brew upgrade", -1, "brew command not found") from e


def generate_brewfile() -> str:
    """Execute brew bundle dump and return Brewfile content.

    Returns:
        The Brewfile content as a string.

    Raises:
        BrewCommandError: If brew bundle dump fails.
    """
    brew_cmd, env = _get_brew_context()
    try:
        result = subprocess.run(
            [brew_cmd, "bundle", "dump", "--force", "--file=-"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        if result.returncode != 0:
            raise BrewCommandError(
                "brew bundle dump --force --file=-", result.returncode, result.stderr
            )
        return result.stdout
    except FileNotFoundError as e:
        raise BrewCommandError(
            "brew bundle dump --force --file=-", -1, "brew command not found"
        ) from e
