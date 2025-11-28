"""Plist scanner module for finding existing LaunchAgent files.

This module provides functionality to scan the LaunchAgents directory
for plist files matching a configured domain prefix.
"""

from pathlib import Path

LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"


def get_launch_agents_dir() -> Path:
    """Return the path to the LaunchAgents directory.

    Returns:
        Path to ~/Library/LaunchAgents/
    """
    return LAUNCH_AGENTS_DIR


def build_plist_path(domain: str, task_name: str) -> Path:
    """Construct full path for a plist file from domain and task name.

    Args:
        domain: The domain prefix (e.g., 'com.example').
        task_name: The task name.

    Returns:
        Full path to the plist file in ~/Library/LaunchAgents/.

    _Requirements: 2.4, 2.5_
    """
    filename = f"{domain}.{task_name}.plist"
    return get_launch_agents_dir() / filename


def build_plist_filename(domain: str, task_name: str) -> str:
    """Construct plist filename from domain and task name.

    Args:
        domain: The domain prefix (e.g., 'com.example').
        task_name: The task name.

    Returns:
        Filename in format {domain}.{task}.plist

    _Requirements: 2.4_
    """
    return f"{domain}.{task_name}.plist"


def extract_task_name(plist_path: Path, domain: str) -> str:
    """Extract the task name from a plist filename.

    Given a plist file path and the domain prefix, extracts the task name
    portion from the filename. Assumes filename format: {domain}.{task}.plist

    Args:
        plist_path: Path to the plist file.
        domain: The domain prefix.

    Returns:
        The task name portion of the filename.

    _Requirements: 4.1_
    """
    filename = plist_path.name
    # Remove the domain prefix and leading dot
    prefix = f"{domain}."
    suffix = ".plist"

    if filename.startswith(prefix) and filename.endswith(suffix):
        # Extract the middle portion (task name)
        return filename[len(prefix) : -len(suffix)]
    return ""


def scan_domain_agents(domain: str, agents_dir: Path | None = None) -> list[Path]:
    """Find all plist files matching the given domain prefix.

    Scans the LaunchAgents directory for plist files that start with
    the specified domain prefix and end with .plist.

    Args:
        domain: The domain prefix to match.
        agents_dir: Optional directory to scan (defaults to ~/Library/LaunchAgents/).

    Returns:
        List of paths to matching plist files.

    _Requirements: 4.1_
    """
    if agents_dir is None:
        agents_dir = get_launch_agents_dir()

    if not agents_dir.exists():
        return []

    prefix = f"{domain}."
    matching_files: list[Path] = []

    try:
        for path in agents_dir.iterdir():
            if (
                path.is_file()
                and path.name.startswith(prefix)
                and path.name.endswith(".plist")
            ):
                matching_files.append(path)
    except OSError:
        return []

    return sorted(matching_files)
