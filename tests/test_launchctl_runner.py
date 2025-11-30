"""Unit tests for the launchctl runner module.

These tests verify launchctl command execution with mocked subprocess calls.
"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from den.launchctl_runner import (
  load_agent,
  unload_agent,
  LaunchctlError,
)


class TestLoadAgent:
  """Tests for load_agent function."""

  def test_successful_load(self) -> None:
    """Test successful launchctl load execution."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch(
      "den.launchctl_runner.subprocess.run", return_value=mock_result
    ) as mock_run:
      load_agent(plist_path)

      mock_run.assert_called_once_with(
        ["launchctl", "load", str(plist_path)],
        capture_output=True,
        text=True,
        check=False,
      )

  def test_load_failure_raises_error(self) -> None:
    """Test that failed launchctl load raises LaunchctlError."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Could not find specified service"
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch("den.launchctl_runner.subprocess.run", return_value=mock_result):
      with pytest.raises(LaunchctlError) as exc_info:
        load_agent(plist_path)

      assert "launchctl load" in exc_info.value.command
      assert exc_info.value.returncode == 1
      assert "Could not find specified service" in exc_info.value.stderr

  def test_launchctl_not_found_raises_error(self) -> None:
    """Test that missing launchctl command raises LaunchctlError."""
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch(
      "den.launchctl_runner.subprocess.run",
      side_effect=FileNotFoundError("launchctl not found"),
    ):
      with pytest.raises(LaunchctlError) as exc_info:
        load_agent(plist_path)

      assert "launchctl load" in exc_info.value.command
      assert exc_info.value.returncode == -1
      assert "launchctl command not found" in exc_info.value.stderr


class TestUnloadAgent:
  """Tests for unload_agent function."""

  def test_successful_unload(self) -> None:
    """Test successful launchctl unload execution."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch(
      "den.launchctl_runner.subprocess.run", return_value=mock_result
    ) as mock_run:
      unload_agent(plist_path)

      mock_run.assert_called_once_with(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
        text=True,
        check=False,
      )

  def test_unload_failure_raises_error(self) -> None:
    """Test that failed launchctl unload raises LaunchctlError."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Could not find specified service"
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch("den.launchctl_runner.subprocess.run", return_value=mock_result):
      with pytest.raises(LaunchctlError) as exc_info:
        unload_agent(plist_path)

      assert "launchctl unload" in exc_info.value.command
      assert exc_info.value.returncode == 1
      assert "Could not find specified service" in exc_info.value.stderr

  def test_launchctl_not_found_raises_error(self) -> None:
    """Test that missing launchctl command raises LaunchctlError."""
    plist_path = Path("/Users/test/Library/LaunchAgents/com.example.task.plist")

    with patch(
      "den.launchctl_runner.subprocess.run",
      side_effect=FileNotFoundError("launchctl not found"),
    ):
      with pytest.raises(LaunchctlError) as exc_info:
        unload_agent(plist_path)

      assert "launchctl unload" in exc_info.value.command
      assert exc_info.value.returncode == -1
      assert "launchctl command not found" in exc_info.value.stderr
