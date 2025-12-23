# CLAUDE.md

This file provides guidance for Claude Code when working on this project.

## Project Overview

`den` is a Python CLI utility for local machine automations built with Typer. It provides commands for Homebrew management, macOS LaunchAgent management, and GitHub repository creation.

## Quick Reference

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run single test
uv run pytest tests/test_hello.py::test_hello_default_output

# Run the CLI
uv run den
```

## Project Structure

- `src/den/` - Main source code
  - `main.py` - CLI entry point using Typer
  - `commands/` - Command modules (auth, brew, hello, launchctl, repo)
  - Supporting modules for each feature (formatters, clients, validators, etc.)
- `tests/` - Test files using pytest
- `openspec/` - Specifications and change proposals

## Code Style

- **Python version:** 3.12+
- **Imports:** Absolute imports, grouped (stdlib, 3rd-party, local)
- **Type hints:** Required for all functions (args and return types)
- **Naming:** `snake_case` for functions/vars, `PascalCase` for classes
- **Docstrings:** Google style for public functions/classes
- **Testing:** Use `typer.testing.CliRunner` for CLI tests

## Key Dependencies

- `typer` - CLI framework
- `anthropic` - Claude API for Brewfile formatting
- `httpx` - HTTP client for GitHub API calls

## Important Files

- `AGENTS.md` - Detailed agent instructions and OpenSpec reference
- `openspec/AGENTS.md` - For proposals, specs, and architectural changes
- `pyproject.toml` - Project configuration and dependencies

## When Making Changes

1. Follow existing patterns in the codebase
2. Add tests for new functionality
3. Ensure type hints are complete
4. For architectural changes or new features, consult `openspec/AGENTS.md`
