# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for building the den CLI executable.

This configuration creates a single-file executable that bundles
all Python dependencies including typer, anthropic, and httpx.

Usage:
    pyinstaller den.spec

Output:
    dist/den - Standalone executable
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path('.').resolve() / 'src'
sys.path.insert(0, str(src_path))

a = Analysis(
    ['src/den/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'typer',
        'typer.core',
        'typer.main',
        'click',
        'click.core',
        'anthropic',
        'httpx',
        'httpx._transports',
        'httpx._transports.default',
        'den',
        'den.main',
        'den.commands',
        'den.commands.auth',
        'den.commands.brew',
        'den.commands.hello',
        'den.auth_storage',
        'den.brew_logger',
        'den.brew_runner',
        'den.brewfile_formatter',
        'den.gist_client',
        'den.hash_utils',
        'den.state_storage',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='den',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
