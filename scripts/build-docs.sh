#!/usr/bin/env bash
#
# Assemble docs/ tree from sources before running `mkdocs build`.
#
# Why: MkDocs requires `docs_dir` to be a child directory of the config file's
# parent. Source content (README, CONTRIBUTING, CLAUDE.md, and .claude/ catalogue +
# shared content) lives outside docs/ for good reasons (drop-in install for .claude/,
# convention for root files). This script copies those into docs/ as a build step.
#
# The copied paths are gitignored so the source of truth stays in its native location.
# Re-running this script is idempotent — it removes the copied subtrees first.

set -euo pipefail

cd "$(dirname "$0")/.."

# Root-level docs become top-level pages in the site
cp README.md docs/index.md
cp CONTRIBUTING.md docs/contributing.md
cp CLAUDE.md docs/claude.md

# Catalogue + shared content from .claude/ becomes a top-level section each
rm -rf docs/agents docs/skills docs/shared
cp -r .claude/agents docs/agents
cp -r .claude/skills docs/skills
cp -r .claude/shared docs/shared

# Rewrite repo-relative paths in the copied root docs so links resolve in the site.
# Source files keep their original repo-relative links; only the copies are rewritten.
rewrite() {
    local f="$1"
    sed -i \
        -e 's|](\.claude/agents/|](agents/|g' \
        -e 's|](\.claude/skills/|](skills/|g' \
        -e 's|](\.claude/shared/|](shared/|g' \
        -e 's|](CONTRIBUTING\.md|](contributing.md|g' \
        -e 's|](CLAUDE\.md|](claude.md|g' \
        -e 's|](docs/anthropic-spec\.md|](anthropic-spec.md|g' \
        -e 's|](docs/adr/|](adr/|g' \
        -e 's|](docs/intake/|](intake/|g' \
        "$f"
}
rewrite docs/index.md
rewrite docs/contributing.md
rewrite docs/claude.md

echo "docs/ tree assembled. Run 'mkdocs serve' for local preview or 'mkdocs build' to generate site/."
