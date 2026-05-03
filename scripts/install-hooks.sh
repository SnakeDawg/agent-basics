#!/usr/bin/env bash
# One-time setup: point git at the in-repo hooks directory.
#
# Usage: scripts/install-hooks.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

git config core.hooksPath .githooks
chmod +x .githooks/*

echo "✓ Git hooks enabled (core.hooksPath = .githooks)"
echo "  Active hooks:"
ls -1 .githooks | sed 's/^/    - /'
