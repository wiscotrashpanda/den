"""Launchctl runner module for loading and unloading LaunchAgents.

This module handles execution of launchctl commands for managing
macOS LaunchAgent plist files.
"""

import subprocess
from pathlib import Path


class LaunchctlError(Exception):
    """Raised when a launchctl command fails."""

    def __init__(self, command: str, returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(f"Command '{command}' failed with code {returncode}: {stderr}")


def load_agent(plist_path: Path) -> None:
    """Load a LaunchAgent using launchctl.

    Args:
        plist_path: Path to the plist file.

    Raises:
        LaunchctlError: If the load command fails.
    """
    try:
        result = subprocess.run(
            ["launchctl", "load", str(plist_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise LaunchctlError(
                f"launchctl load {plist_path}",
                result.returncode,
                result.stderr.strip() or "Unknown error",
            )
    except FileNotFoundError as e:
        raise LaunchctlError(
            f"launchctl load {plist_path}",
            -1,
            "launchctl command not found",
        ) from e


def unload_agent(plist_path: Path) -> None:
    """Unload a LaunchAgent using launchctl.

    Args:
        plist_path: Path to the plist file.

    Raises:
        LaunchctlError: If the unload command fails.
    """
    try:
        result = subprocess.run(
            ["launchctl", "unload", str(plist_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise LaunchctlError(
                f"launchctl unload {plist_path}",
                result.returncode,
                result.stderr.strip() or "Unknown error",
            )
    except FileNotFoundError as e:
        raise LaunchctlError(
            f"launchctl unload {plist_path}",
            -1,
            "launchctl command not found",
        ) from e
