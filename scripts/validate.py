#!/usr/bin/env python3
"""Validate frontmatter and naming for catalogue entries.

Usage:
    python3 scripts/validate.py [path]

If path is omitted, validates every entry under .claude/agents/ and
.claude/skills/. Exits non-zero on any failure.

Pure stdlib; no PyYAML dependency. Handles only the flat key:value YAML
shape the catalogue uses.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / ".claude" / "agents"
SKILLS_DIR = REPO / ".claude" / "skills"

KEBAB = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
TEMPLATE = re.compile(r"^_[a-z0-9]+(-[a-z0-9]+)*$")
VALID_MODELS = {"opus", "sonnet", "haiku", "inherit"}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Extract flat key:value pairs from a YAML frontmatter block."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def check(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_name(name: str, errors: list[str]) -> None:
    if not (KEBAB.match(name) or TEMPLATE.match(name)):
        errors.append(f"name '{name}' is not kebab-case")


def validate_agent(path: Path) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(path.read_text())
    if fm is None:
        return ["frontmatter missing or unparseable"]
    check("name" in fm, errors, "missing required field: name")
    check("description" in fm, errors, "missing required field: description")
    name = fm.get("name", "")
    if name:
        validate_name(name, errors)
        check(name == path.stem, errors, f"name '{name}' does not match filename stem '{path.stem}'")
    if "description" in fm:
        check(bool(fm["description"]), errors, "description is empty")
    if "model" in fm:
        check(fm["model"] in VALID_MODELS, errors, f"model '{fm['model']}' not in {sorted(VALID_MODELS)}")
    return errors


def validate_skill(skill_md: Path) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(skill_md.read_text())
    if fm is None:
        return ["frontmatter missing or unparseable"]
    check("name" in fm, errors, "missing required field: name")
    check("description" in fm, errors, "missing required field: description")
    name = fm.get("name", "")
    dir_name = skill_md.parent.name
    if name:
        validate_name(name, errors)
        check(name == dir_name, errors, f"name '{name}' does not match directory '{dir_name}'")
    if "description" in fm:
        check(bool(fm["description"]), errors, "description is empty")
    return errors


def discover(target: Path | None) -> list[tuple[str, Path]]:
    """Return list of (kind, path) tuples to validate."""
    items: list[tuple[str, Path]] = []
    if target is None:
        for p in sorted(AGENTS_DIR.glob("*.md")):
            items.append(("agent", p))
        for p in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            items.append(("skill", p))
        return items

    p = target.resolve()
    try:
        rel = p.relative_to(REPO)
    except ValueError:
        rel = p
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == ".claude" and parts[1] == "agents" and p.suffix == ".md":
        items.append(("agent", p))
    elif len(parts) >= 4 and parts[0] == ".claude" and parts[1] == "skills" and p.name == "SKILL.md":
        items.append(("skill", p))
    elif len(parts) >= 3 and parts[0] == ".claude" and parts[1] == "skills" and p.is_dir():
        skill_md = p / "SKILL.md"
        if skill_md.exists():
            items.append(("skill", skill_md))
    else:
        print(f"error: {target} is not a recognised catalogue entry", file=sys.stderr)
        sys.exit(2)
    return items


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else None
    items = discover(target)
    if not items:
        print("no entries found")
        return 0

    failures = 0
    for kind, path in items:
        rel = path.relative_to(REPO)
        errors = validate_agent(path) if kind == "agent" else validate_skill(path)
        if errors:
            failures += 1
            print(f"FAIL {rel}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK   {rel}")

    print()
    print(f"{len(items)} entr{'y' if len(items) == 1 else 'ies'} checked, {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
