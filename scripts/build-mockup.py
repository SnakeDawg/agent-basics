#!/usr/bin/env python3
"""Render the data-driven mockup pages from per-skill YAML and frontmatter.

Outputs:
  docs/mockup/skill-anatomy.html  — first skill with mockup.yaml (placeholder for per-skill pages)
  docs/mockup/catalog.html        — index of every skill + agent

Run: python3 scripts/build-mockup.py
"""
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
AGENTS_DIR = ROOT / ".claude" / "agents"
TEMPLATES_DIR = ROOT / "scripts" / "templates"
OUT_DIR = ROOT / "docs" / "mockup"


def parse_frontmatter(md_path: Path):
    """Return (frontmatter dict, body line count) from a markdown file."""
    text = md_path.read_text()
    if not text.startswith("---"):
        return {}, len(text.splitlines())
    end = text.find("\n---", 3)
    if end == -1:
        return {}, len(text.splitlines())
    fm = yaml.safe_load(text[3:end]) or {}
    body = text[end + 4 :]
    return fm, len(body.splitlines())


def discover_skills():
    """Yield {name, description, line_count, has_mockup} for each skill."""
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm, lc = parse_frontmatter(skill_md)
        yield {
            "name": fm.get("name", skill_dir.name),
            "description": fm.get("description", ""),
            "line_count": lc,
            "has_mockup": (skill_dir / "mockup.yaml").exists(),
            "mockup_path": (skill_dir / "mockup.yaml") if (skill_dir / "mockup.yaml").exists() else None,
        }


def discover_agents():
    """Yield {name, description, line_count} for each agent."""
    for agent_md in sorted(AGENTS_DIR.glob("*.md")):
        if agent_md.stem.startswith("_"):
            continue
        fm, lc = parse_frontmatter(agent_md)
        yield {
            "name": fm.get("name", agent_md.stem),
            "description": fm.get("description", ""),
            "line_count": lc,
        }


def render_anatomy(env, skill):
    """Render skill-anatomy.html for one skill that has a mockup.yaml."""
    data = yaml.safe_load(skill["mockup_path"].read_text())
    diagram_path = skill["mockup_path"].parent / "mockup-diagram.svg"
    diagram_svg = diagram_path.read_text() if diagram_path.exists() else ""

    template = env.get_template("skill-anatomy.html.j2")
    return template.render(
        skill_name=skill["name"],
        page=data["page"],
        kpi_tiles=data["kpi_tiles"],
        capability_groups=data["capability_groups"],
        diagram_svg=diagram_svg,
    )


def render_catalog(env, skills, agents):
    """Render catalog.html — index of skills + agents."""
    skill_entries = [
        {
            "name": s["name"],
            "description": s["description"],
            "line_count": s["line_count"],
            # For now every detail link points at the single skill-anatomy.html page;
            # only skills with mockup.yaml claim a working detail view.
            "detail_href": "skill-anatomy.html" if s["has_mockup"] else None,
        }
        for s in skills
    ]
    template = env.get_template("catalog.html.j2")
    return template.render(skills=skill_entries, agents=list(agents))


def main():
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    skills = list(discover_skills())
    agents = list(discover_agents())

    catalog_html = render_catalog(env, skills, agents)
    catalog_out = OUT_DIR / "catalog.html"
    catalog_out.write_text(catalog_html)
    print(f"wrote {catalog_out.relative_to(ROOT)} ({len(skills)} skills, {len(agents)} agents)")

    mocked_skills = [s for s in skills if s["has_mockup"]]
    if not mocked_skills:
        print("no skills have mockup.yaml — skipping anatomy page")
        return

    s = mocked_skills[0]
    if len(mocked_skills) > 1:
        print(f"note: {len(mocked_skills)} skills have mockup.yaml; rendering '{s['name']}' only for now")

    anatomy_html = render_anatomy(env, s)
    anatomy_out = OUT_DIR / "skill-anatomy.html"
    anatomy_out.write_text(anatomy_html)
    print(f"wrote {anatomy_out.relative_to(ROOT)} from {s['mockup_path'].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
