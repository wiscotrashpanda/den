# Claude Code Guidelines for denctl

This document provides guidance for working with the denctl project using Claude Code.

## Project Overview

**denctl** is a Python CLI automation tool for macOS built with Typer. It can be invoked using either `denctl` or `den` for convenience. The tool currently provides:

- Homebrew backup management with AI formatting
- Authentication management for API keys
- Scheduled automated backups via launchd

## Commands

- **Install:** `uv sync` (installs dependencies & project in editable mode)
- **Test:** `uv run pytest` or `uv run pytest tests/`
- **Single Test:** `uv run pytest tests/test_hello.py::test_hello_default_name`
- **Format:** `uv run ruff format .`
- **Lint:** `uv run ruff check .` or `uv run ruff check . --fix` (auto-fix)
- **Type Check:** `uv run mypy .`
- **Run CLI:** `uv run denctl [command]` or `uv run den [command]`

## Code Style & Conventions

- **Language:** Python 3.12+ (pyproject.toml requires >=3.12)
- **Formatting:** Use `ruff` (line-length=88, target py312)
- **Linting:** Ruff with E, F, I, B rules (Pyflakes, pycodestyle, isort, flake8-bugbear)
- **Type Hints:** Mandatory for all function signatures (args & returns). Use `typing` imports.
- **Imports:** Standard library first, then third-party, then local `denctl` imports (ruff auto-sorts)
- **Architecture:** `src` layout (`src/denctl/`). Keep `__init__.py` minimal (version only).
- **CLI Framework:** Use `typer` with `typer.Typer()` apps. Commands via `@app.command()`.
- **Output:** Use `rich.console.Console()` for styled terminal output, not raw `print()`.
- **Testing:** Write `pytest` tests in `tests/`. Use `typer.testing.CliRunner` for CLI tests.
- **Docstrings:** Google-style docstrings for all modules, commands, and complex functions.
- **Error Handling:** Raise `typer.Exit(code=N)` on errors, use rich console for messages.
- **Config Files:** Store in `~/.config/denctl/`, use JSON, set 600 permissions for secrets.
- **Subprocess:** Use `subprocess.run()` with `capture_output=True`, `text=True`, `check=True` where appropriate.
- **Constants:** Use UPPER_CASE for module-level constants (CONFIG_DIR, PLIST_PATH, etc.).

## Project Structure

```
denctl/
├── src/
│   └── denctl/
│       ├── __init__.py          # Package initialization (version only)
│       ├── main.py              # Main CLI entry point
│       └── commands/
│           ├── __init__.py
│           ├── auth.py          # Authentication management
│           ├── hello.py         # Example hello command
│           └── homebrew.py      # Homebrew backup functionality
├── tests/
│   ├── __init__.py
│   └── test_hello.py            # Test suite
├── pyproject.toml               # Project configuration
├── uv.lock                      # Dependency lock file
├── CLAUDE.MD                    # This file
└── README.md                    # Project documentation
```

## Development Workflow

1. Make changes to source files in `src/denctl/`
2. Run tests: `uv run pytest tests/`
3. Format code: `uv run ruff format .`
4. Lint code: `uv run ruff check . --fix`
5. Type check: `uv run mypy .`
6. Test CLI commands: `uv run den [command]`

## Key Implementation Patterns

### Command Structure

Commands are organized as Typer applications:
- Simple commands are registered directly via `@app.command()`
- Command groups use `typer.Typer()` instances added via `app.add_typer()`

### Configuration Management

- General config: `~/.config/denctl/config.json` (API keys, shared settings)
- Module-specific config: `~/.config/denctl/<module>.json` (e.g., homebrew.json)
- Always set 600 permissions on config files containing secrets

### Rich Console Output

Use Rich Console for all user-facing output:
- Success: `console.print("[green]✓[/green] Message")`
- Warnings: `console.print("[yellow]Warning:[/yellow] Message")`
- Errors: `console.print("[bold red]Error:[/bold red] Message")`

### Error Handling

- Use `typer.Exit(code=N)` to exit with status codes
- Catch subprocess errors and provide helpful messages
- Validate dependencies before running commands

## Testing

- Use `pytest` for all tests
- Use `typer.testing.CliRunner` for CLI command tests
- Test both success and failure scenarios
- Mock external dependencies (subprocess, API calls) when appropriate
