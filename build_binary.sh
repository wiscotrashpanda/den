#!/bin/bash
set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed. Please install it first."
    exit 1
fi

echo "Building standalone executable with PyInstaller..."

# Clean previous builds
rm -rf build dist den.spec

# Run PyInstaller using uv (ephemeral installation)
# --onefile: Create a single executable file
# --name den: Name the executable 'den'
# --clean: Clean PyInstaller cache
uv run --with pyinstaller pyinstaller --onefile --name den --clean src/den/main.py

echo ""
echo "✅ Build complete!"
echo "Executable is located at: $(pwd)/dist/den"
echo ""
echo "To install this binary to /usr/local/bin (so it's available in your PATH),"
echo "run the following command:"
echo ""
echo "  sudo ln -sf \"$(pwd)/dist/den\" /usr/local/bin/den"
echo ""
echo "Or to copy it (if you plan to unplug the drive):"
echo ""
echo "  sudo cp \"$(pwd)/dist/den\" /usr/local/bin/den"
