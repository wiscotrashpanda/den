"""LaunchCtl configuration module for reading domain settings.

This module handles reading the domain configuration from the config.json file
at ~/.config/den/config.json for use in LaunchAgent plist file naming.
"""

import json
from pathlib import Path

DEFAULT_DOMAIN = "com.example"


def get_config_file_path() -> Path:
    """Return the path to the config.json file.

    Returns:
        Path to ~/.config/den/config.json
    """
    return Path.home() / ".config" / "den" / "config.json"


def get_domain() -> str:
    """Read domain from ~/.config/den/config.json or return default.

    Reads the 'domain' key from the configuration file. If the file
    does not exist, contains invalid JSON, or lacks a domain key,
    returns the default domain 'com.example'.

    Returns:
        The configured domain string, or 'com.example' if not configured.
    """
    config_file = get_config_file_path()

    if not config_file.exists():
        return DEFAULT_DOMAIN

    try:
        with config_file.open("r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return DEFAULT_DOMAIN
            config = json.loads(content)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DOMAIN

    return config.get("domain", DEFAULT_DOMAIN)
