#!/usr/bin/env python3
"""Regenerate the agent and skill catalogue tables in README.md.

Tables are written between marker comments:
    <!-- agents:start --> ... <!-- agents:end -->
    <!-- skills:start --> ... <!-- skills:end -->

Templates (entries whose name starts with `_`) are skipped.
Pure stdlib; reuses the frontmatter parser convention from validate.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
AGENTS_DIR = REPO / ".claude" / "agents"
SKILLS_DIR = REPO / ".claude" / "skills"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def collect_agents() -> list[tuple[str, str, Path]]:
    rows: list[tuple[str, str, Path]] = []
    for path in sorted(AGENTS_DIR.glob("*.md")):
        fm = parse_frontmatter(path.read_text())
        name = fm.get("name", path.stem)
        if name.startswith("_"):
            continue
        rows.append((name, fm.get("description", ""), path))
    return rows


def collect_skills() -> list[tuple[str, str, Path]]:
    rows: list[tuple[str, str, Path]] = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_md.read_text())
        name = fm.get("name", skill_md.parent.name)
        if name.startswith("_"):
            continue
        rows.append((name, fm.get("description", ""), skill_md))
    return rows


def render_table(rows: list[tuple[str, str, Path]], label: str) -> str:
    if not rows:
        return f"_No {label} yet._\n"
    lines = ["| Name | Description |", "| --- | --- |"]
    for name, desc, path in rows:
        rel = path.relative_to(REPO).as_posix()
        lines.append(f"| [`{name}`]({rel}) | {desc} |")
    return "\n".join(lines) + "\n"


def replace_block(text: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}:start -->"
    end = f"<!-- {marker}:end -->"
    s = text.find(start)
    e = text.find(end)
    if s == -1 or e == -1 or e < s:
        raise SystemExit(
            f"error: README.md is missing markers '{start}' / '{end}'. "
            "Add the marker pair where the table should live."
        )
    return text[: s + len(start)] + "\n" + body + text[e:]


def main(argv: list[str]) -> int:
    check_only = "--check" in argv[1:]

    if not README.exists():
        print("error: README.md not found", file=sys.stderr)
        return 2

    original = README.read_text()
    text = original
    text = replace_block(text, "agents", render_table(collect_agents(), "agents"))
    text = replace_block(text, "skills", render_table(collect_skills(), "skills"))

    if text == original:
        print("README.md already up to date")
        return 0

    if check_only:
        print("error: README.md is out of date. Run `python3 scripts/index-readme.py` to regenerate.", file=sys.stderr)
        return 1

    README.write_text(text)
    print("README.md regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
