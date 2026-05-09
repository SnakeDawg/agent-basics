#!/usr/bin/env python3
"""Render the data-driven mockup pages from per-skill YAML.

Reads .claude/skills/<skill>/mockup.yaml + mockup-diagram.svg and writes
docs/mockup/skill-anatomy.html (currently one skill — first one with a
mockup.yaml wins; multi-skill output is the next step).

Run:    python3 scripts/build-mockup.py
"""
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
TEMPLATES_DIR = ROOT / "scripts" / "templates"
OUT_DIR = ROOT / "docs" / "mockup"


def discover_skills():
    """Yield (skill_name, mockup_yaml_path) for every skill that opted in."""
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        mockup_yaml = skill_dir / "mockup.yaml"
        if mockup_yaml.exists():
            yield skill_dir.name, mockup_yaml


def render_anatomy(env, skill_name, mockup_yaml):
    data = yaml.safe_load(mockup_yaml.read_text())
    diagram_path = mockup_yaml.parent / "mockup-diagram.svg"
    diagram_svg = diagram_path.read_text() if diagram_path.exists() else ""

    template = env.get_template("skill-anatomy.html.j2")
    return template.render(
        skill_name=skill_name,
        page=data["page"],
        kpi_tiles=data["kpi_tiles"],
        capability_groups=data["capability_groups"],
        diagram_svg=diagram_svg,
    )


def main():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    skills = list(discover_skills())
    if not skills:
        raise SystemExit("No skills with mockup.yaml found.")

    skill_name, mockup_yaml = skills[0]
    if len(skills) > 1:
        print(f"note: {len(skills)} skills have mockup.yaml; rendering '{skill_name}' only for now")

    html = render_anatomy(env, skill_name, mockup_yaml)
    out = OUT_DIR / "skill-anatomy.html"
    out.write_text(html)
    print(f"wrote {out.relative_to(ROOT)} from {mockup_yaml.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
