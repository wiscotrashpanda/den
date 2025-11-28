"""Entry point for running den as a module or via PyInstaller.

This module allows the package to be executed with `python -m den`
and serves as the entry point for PyInstaller bundling.
"""

from den.main import app

if __name__ == "__main__":
    app()
