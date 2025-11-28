"""LaunchCtl input validation module.

This module provides validation functions for user input when creating
LaunchAgent configurations, including task names, commands, and schedule values.
"""

import re


def validate_task_name(name: str) -> tuple[bool, str]:
    """Validate task name contains only allowed characters.

    Task names must be non-empty and contain only alphanumeric characters,
    hyphens, and underscores. Spaces, slashes, and other special characters
    are not allowed.

    Args:
        name: The task name to validate.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.

    _Requirements: 6.1, 6.2_
    """
    if not name:
        return False, "Task name cannot be empty"

    # Allow only alphanumeric, hyphens, and underscores
    pattern = r"^[a-zA-Z0-9_-]+$"
    if not re.match(pattern, name):
        return False, (
            "Task name can only contain alphanumeric characters, "
            "hyphens, and underscores"
        )

    return True, ""


def validate_command(command: str) -> tuple[bool, str]:
    """Validate command is non-empty.

    Args:
        command: The command string to validate.

    Returns:
        Tuple of (is_valid, error_message).

    _Requirements: 6.3_
    """
    if not command or not command.strip():
        return False, "Command cannot be empty"

    return True, ""


def validate_interval(seconds: int) -> tuple[bool, str]:
    """Validate interval is positive.

    Args:
        seconds: The interval in seconds.

    Returns:
        Tuple of (is_valid, error_message).

    _Requirements: 6.4_
    """
    if seconds <= 0:
        return False, "Interval must be a positive integer"

    return True, ""


def validate_hour(hour: int) -> tuple[bool, str]:
    """Validate hour is in range 0-23.

    Args:
        hour: The hour value.

    Returns:
        Tuple of (is_valid, error_message).

    _Requirements: 6.5_
    """
    if hour < 0 or hour > 23:
        return False, "Hour must be between 0 and 23"

    return True, ""


def validate_minute(minute: int) -> tuple[bool, str]:
    """Validate minute is in range 0-59.

    Args:
        minute: The minute value.

    Returns:
        Tuple of (is_valid, error_message).

    _Requirements: 6.6_
    """
    if minute < 0 or minute > 59:
        return False, "Minute must be between 0 and 59"

    return True, ""
