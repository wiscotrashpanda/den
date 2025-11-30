# den Codebase Guide for Agents

## Build, Lint, & Test

- **Install:** `pip install -e ".[dev]"` to install with dev dependencies.
- **Test:** Run all tests with `pytest`.
- **Single Test:** `pytest tests/test_hello.py::test_hello_default_output`
- **Lint:** Follow standard Python PEP 8. Type hints are required (mypy compatible).
- **Run:** `python -m den` or install via `pip install -e .` and run `den`.

## Code Style & Conventions

- **Imports:** Use absolute imports (e.g., `from den.commands.auth import auth_app`). Group: stdlib, 3rd-party, local.
- **Formatting:** Standard PEP 8. 2 spaces indentation.
- **Types:** Fully type-hinted functions/methods (args and return types).
- **Naming:** `snake_case` for functions/vars, `PascalCase` for classes, `UPPER_CASE` for constants.
- **Docstrings:** Required for all public modules, functions, and classes. Use Google style (Summary, Args, Returns).
- **Structure:** Commands go in `src/den/commands/`. Main entry point is `src/den/main.py` using `typer`.
- **Error Handling:** Use custom exceptions where appropriate.
- **Testing:** Use `typer.testing.CliRunner` for CLI command tests.
