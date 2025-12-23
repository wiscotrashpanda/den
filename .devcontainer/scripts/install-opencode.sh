#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Checking for existing OpenCode CLI (opencode)..."
if command -v opencode >/dev/null 2>&1; then
  echo "OpenCode CLI already installed at: $(command -v opencode)"
  exit 0
fi

# Try common install methods in order
# 1) npm (common for JS-based CLIs)
if command -v npm >/dev/null 2>&1; then
  echo "Attempting to install OpenCode CLI with npm..."
  npm install -g opencode || true
  if command -v opencode >/dev/null 2>&1; then
    echo "Installed OpenCode CLI via npm: $(command -v opencode)"
    exit 0
  fi
fi

# 2) pip (some CLIs provide a Python package)
if command -v pip3 >/dev/null 2>&1; then
  echo "Attempting to install OpenCode CLI with pip..."
  pip3 install --user opencode-cli || true
  if command -v opencode >/dev/null 2>&1; then
    echo "Installed OpenCode CLI via pip: $(command -v opencode)"
    exit 0
  fi
fi

# 3) Try a GitHub releases install script pattern (best-effort)
# NOTE: Replace the URL below with the official install script if you have one.
GH_INSTALL_URL="https://raw.githubusercontent.com/opencode-org/cli/main/install.sh"
if command -v curl >/dev/null 2>&1; then
  echo "Attempting to fetch install script from GitHub: ${GH_INSTALL_URL}"
  set +e
  curl -fsSL "${GH_INSTALL_URL}" -o /tmp/opencode-install.sh
  curl_exit=$?
  set -e
  if [ $curl_exit -eq 0 ] && [ -s /tmp/opencode-install.sh ]; then
    chmod +x /tmp/opencode-install.sh
    /tmp/opencode-install.sh || true
    if command -v opencode >/dev/null 2>&1; then
      echo "Installed OpenCode CLI via GitHub script: $(command -v opencode)"
      exit 0
    fi
  else
    echo "Could not fetch the GitHub install script. Skipping this method."
  fi
fi

# If we reach here, installation didn't succeed automatically
cat <<'INFO'

⚠️ OpenCode CLI was not installed automatically.

I attempted to install via npm, pip, and a GitHub install script but none succeeded.

Next steps you can try:
  - Provide the official install URL for the OpenCode CLI and I'll wire it into the script.
  - Run one of these manually in the Codespace terminal:
      npm install -g opencode
      pip3 install --user opencode-cli
      curl -fsSL <official install script URL> | bash

INFO

exit 0
