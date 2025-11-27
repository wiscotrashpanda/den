#!/bin/bash
set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed. Please install it first."
    echo "Visit https://github.com/astral-sh/uv for installation instructions."
    exit 1
fi

echo "Installing den as a global tool..."

# Install the tool from the current directory
# --force allows overwriting if it's already installed
# --reinstall ensures we get the latest version from the current code
uv tool install . --force --reinstall

echo ""
echo "✅ Installation complete!"
echo "You can now run 'den' from any terminal window."
