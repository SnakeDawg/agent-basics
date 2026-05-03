#!/usr/bin/env bash
# Export the catalogue as a Claude Code plugin under dist/plugin/.
#
# Inside a plugin, agents/, skills/, and commands/ live as siblings of
# .claude-plugin/ (no .claude/ prefix). This script copies the .claude/
# contents into that layout and writes a minimal plugin.json.
#
# Usage: scripts/export-plugin.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$REPO/dist/plugin"

rm -rf "$DIST"
mkdir -p "$DIST/.claude-plugin"

for sub in agents skills commands; do
  if [ -d "$REPO/.claude/$sub" ]; then
    mkdir -p "$DIST/$sub"
    cp -R "$REPO/.claude/$sub/." "$DIST/$sub/"
  fi
done

cat > "$DIST/.claude-plugin/plugin.json" <<'JSON'
{
  "name": "agents-catalogue",
  "version": "0.1.0",
  "description": "Foundational catalogue of Claude Code subagents and skills."
}
JSON

echo "Plugin written to $DIST"
