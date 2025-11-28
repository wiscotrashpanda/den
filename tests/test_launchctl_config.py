"""Unit tests for the launchctl config module.

Tests for config reading functions including path resolution,
domain loading with various file states.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from den.launchctl_config import (
    DEFAULT_DOMAIN,
    get_config_file_path,
    get_domain,
)


def test_get_config_file_path_returns_correct_path():
    """Test that get_config_file_path returns ~/.config/den/config.json.

    _Requirements: 2.1_
    """
    result = get_config_file_path()
    expected = Path.home() / ".config" / "den" / "config.json"
    assert result == expected


def test_get_domain_returns_default_for_missing_file():
    """Test that get_domain returns default when config file doesn't exist.

    _Requirements: 2.3_
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        nonexistent_file = Path(tmpdir) / "nonexistent" / "config.json"

        with patch(
            "den.launchctl_config.get_config_file_path", return_value=nonexistent_file
        ):
            result = get_domain()
            assert result == DEFAULT_DOMAIN


def test_get_domain_returns_default_for_empty_file():
    """Test that get_domain returns default when config file is empty.

    _Requirements: 2.3_
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        config_file.write_text("")

        with patch(
            "den.launchctl_config.get_config_file_path", return_value=config_file
        ):
            result = get_domain()
            assert result == DEFAULT_DOMAIN


def test_get_domain_returns_configured_value():
    """Test that get_domain returns domain from valid config file.

    _Requirements: 2.1, 2.2_
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        config_file.write_text(json.dumps({"domain": "com.mycompany"}))

        with patch(
            "den.launchctl_config.get_config_file_path", return_value=config_file
        ):
            result = get_domain()
            assert result == "com.mycompany"


def test_get_domain_returns_default_for_invalid_json():
    """Test that get_domain returns default when config file has invalid JSON.

    _Requirements: 2.3_
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        config_file.write_text("{ invalid json }")

        with patch(
            "den.launchctl_config.get_config_file_path", return_value=config_file
        ):
            result = get_domain()
            assert result == DEFAULT_DOMAIN


def test_get_domain_returns_default_when_domain_key_missing():
    """Test that get_domain returns default when domain key is absent.

    _Requirements: 2.3_
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        config_file.write_text(json.dumps({"other_key": "value"}))

        with patch(
            "den.launchctl_config.get_config_file_path", return_value=config_file
        ):
            result = get_domain()
            assert result == DEFAULT_DOMAIN
