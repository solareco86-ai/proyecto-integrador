#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Setting up development environment in .venv..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate and install dev requirements
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
else
  echo "requirements-dev.txt not found; skipping pip install -r requirements-dev.txt"
fi

echo "Dev environment ready. Activate with: source .venv/bin/activate"