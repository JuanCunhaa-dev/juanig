#!/usr/bin/env bash
set -euo pipefail
REPO="Juancunhaa-dev/juanig"
DEST="${HOME}/.local/bin"
mkdir -p "$DEST"

if command -v pipx >/dev/null 2>&1; then
  pipx install "git+https://github.com/${REPO}.git"
elif command -v pip3 >/dev/null 2>&1; then
  pip3 install --user "git+https://github.com/${REPO}.git"
else
  echo "Install Python 3 and pip first." >&2
  exit 1
fi

export PATH="${DEST}:${PATH}"
if command -v juanig >/dev/null 2>&1; then
  juanig --install-skills
  echo "juanig is ready. Open a new terminal and run: juanig --help"
else
  echo "juanig installed but is not on PATH yet. Add ${DEST} to PATH."
fi
