#!/usr/bin/env python3
"""Build rendered markdown views from .claude/shared/ YAML for the mkdocs site.

Reads structured YAML (identity / charter / strategy / scope, personas,
archetypes) plus already-markdown files (competitors, SKUs) under
.claude/shared/, and emits a navigable docs/shared/ tree of rendered views,
indexes, and Mermaid diagrams.

Run via build-docs.sh; not committed output (docs/shared/ is gitignored).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SHARED = REPO / ".claude" / "shared"
OUT = REPO / "docs" / "shared"

REPO_BLOB = "https://github.com/SnakeDawg/agent-basics/blob/main"


# ---------- helpers ----------

def load(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def lvl(p: Path) -> str:
    """Return parent / level kind from a hierarchy directory path."""
    for kind in ("company", "organizations", "portfolios", "products"):
        if f"/{kind}/" in str(p) or str(p).endswith(f"/{kind}"):
            return kind
    return "unknown"


def slugify(s: str) -> str:
    return s.lower().replace(" ", "-").replace("/", "-")


# ---------- renderers ----------

def render_persona(data: dict, path: Path) -> str:
    pid = data.get("id", path.stem)
    name = data.get("display_name", pid)
    ptype = data.get("type", "")
    out = [f"# {name}", ""]
    out.append(f"_{ptype.title()} persona_" if ptype else "")
    out.append("")

    if titles := data.get("title_examples"):
        out.append("## Title examples")
        for t in titles:
            out.append(f"- {t}")
        out.append("")

    if industry := data.get("industry_context"):
        out.append("## Industry context")
        if isinstance(industry, list):
            for i in industry:
                out.append(f"- {i}")
        else:
            out.append(industry)
        out.append("")

    for label, key in [("Tools", "tools_used"), ("Goals", "goals"),
                       ("Frustrations", "frustrations"),
                       ("Day in life", "day_in_life"),
                       ("Decision style", "decision_style"),
                       ("What they want", "what_they_want"),
                       ("What they don't want", "what_they_dont_want"),
                       ("Common objections", "common_objections")]:
        if val := data.get(key):
            out.append(f"## {label}")
            for item in val:
                out.append(f"- {item}")
            out.append("")

    if bb := data.get("buying_behavior"):
        out.append("## Buying behavior")
        if role := bb.get("role"):
            out.append(f"**Role:** {role}")
            out.append("")
        if criteria := bb.get("decision_criteria_weighted"):
            out.append("**Decision criteria (weighted):**")
            for c in criteria:
                w = c.get("weight", "?")
                out.append(f"{w}. {c.get('criterion', '')}")
            out.append("")
        if behaviors := bb.get("evaluation_behaviors"):
            out.append("**Evaluation behaviors:**")
            for b in behaviors:
                out.append(f"- {b}")
            out.append("")

    if needs := data.get("needs_from_catalogue"):
        out.append("## Needs from this catalogue")
        for n in needs:
            if "skill" in n:
                out.append(f"- **`{n['skill']}`** — {n.get('purpose', '')}")
            elif "default_output_shape" in n:
                out.append(f"- _Default output shape:_ {n['default_output_shape']}")
        out.append("")

    if archs := data.get("maps_to_archetypes"):
        out.append("## Maps to archetypes")
        if primary := archs.get("primary"):
            out.append(f"**Primary:** " + ", ".join(f"[`{a}`](../archetypes/{a}.md)" for a in primary))
        if secondary := archs.get("secondary"):
            out.append(f"**Secondary:** " + ", ".join(f"[`{a}`](../archetypes/{a}.md)" for a in secondary))
        out.append("")

    if pl := data.get("placeholders"):
        out.append("## Validation TBD")
        for p in pl:
            out.append(f"- {p}")
        out.append("")

    if lr := data.get("last_reviewed"):
        out.append(f"_Last reviewed: {lr}_")

    return "\n".join(out).rstrip() + "\n"


def render_archetype(data: dict, path: Path) -> str:
    aid = data.get("id", path.stem)
    name = data.get("display_name", aid)
    out = [f"# {name}", "", "_Behavioral archetype_", ""]

    if co := data.get("core_orientation"):
        out.append("## Core orientation")
        out.append(co.strip())
        out.append("")

    for label, key in [("Buying signals", "buying_signals"),
                       ("Quotes", "quotes"),
                       ("How they evaluate", "how_they_evaluate"),
                       ("What we offer", "what_we_offer"),
                       ("Common objections", "common_objections")]:
        if val := data.get(key):
            out.append(f"## {label}")
            for item in val:
                if label == "Quotes":
                    out.append(f'> "{item}"')
                    out.append("")
                else:
                    out.append(f"- {item}")
            out.append("")

    if dw := data.get("decision_weights"):
        out.append("## Decision weights")
        out.append("| Dimension | Weight |")
        out.append("| --- | --- |")
        for k, v in dw.items():
            out.append(f"| {k.replace('_', ' ')} | {v} |")
        out.append("")

    related = []
    if opp := data.get("opposite_archetype"):
        related.append(f"**Opposite:** [`{opp}`]({opp}.md)")
    if rel := data.get("related_archetypes"):
        related.append(f"**Related:** " + ", ".join(f"[`{r}`]({r}.md)" for r in rel))
    if related:
        out.append("## Related archetypes")
        for r in related:
            out.append(r)
            out.append("")

    if mp := data.get("maps_to_personas"):
        out.append("## Maps to personas")
        if primary := mp.get("primary"):
            out.append(f"**Primary:** " + ", ".join(f"[`{p}`](../personas/{p}.md)" for p in primary))
        if secondary := mp.get("secondary"):
            out.append(f"**Secondary:** " + ", ".join(f"[`{p}`](../personas/{p}.md)" for p in secondary))
        out.append("")

    if rt := data.get("research_treatment"):
        out.append("## How research skills should treat this archetype")
        for skill, treatment in rt.items():
            out.append(f"- **`{skill}`** — {treatment}")
        out.append("")

    if lr := data.get("last_reviewed"):
        out.append(f"_Last reviewed: {lr}_")

    return "\n".join(out).rstrip() + "\n"


def render_hierarchy_unit(level: str, name: str, identity: dict,
                          charter: dict, strategy: dict, scope: dict) -> str:
    display = identity.get("display_name", name)
    out = [f"# {display}", "", f"_{level.title()} — {name}_", ""]

    if mission := identity.get("mission"):
        out.append("## Mission")
        out.append(mission.strip())
        out.append("")

    if vision := identity.get("vision"):
        out.append("## Vision")
        out.append(vision.strip())
        out.append("")

    if pos := identity.get("position"):
        out.append("## Position")
        for p in pos:
            out.append(f"- {p}")
        out.append("")

    if pillars := identity.get("brand_pillars"):
        out.append("## Brand pillars")
        for p in pillars:
            out.append(f"- **{p['name']}.** {p['description'].strip()}")
        out.append("")

    if not_ := identity.get("not"):
        out.append("## What we are not")
        for n in not_:
            out.append(f"- {n}")
        out.append("")

    if mandate := charter.get("mandate"):
        out.append("## Mandate")
        out.append(mandate.strip())
        out.append("")

    if charter_scope := charter.get("scope"):
        if in_scope := charter_scope.get("in_scope"):
            out.append("### In scope")
            for i in in_scope:
                out.append(f"- {i}")
            out.append("")
        if out_scope := charter_scope.get("out_of_scope"):
            out.append("### Out of scope")
            for i in out_scope:
                out.append(f"- {i}")
            out.append("")

    if dr := charter.get("decision_rights"):
        out.append("### Decision rights")
        out.append("| Decision | Owner |")
        out.append("| --- | --- |")
        for d in dr:
            out.append(f"| {d.get('decision', '')} | {d.get('owner', '')} |")
        out.append("")

    if sv := strategy.get("strategic_vision"):
        out.append("## Strategic vision")
        out.append(sv.strip())
        out.append("")

    if priorities := strategy.get("priorities"):
        out.append("## Strategic priorities")
        for p in priorities:
            status = p.get("status", "")
            badge = f" _({status})_" if status else ""
            out.append(f"### {p.get('title', p.get('id', ''))}{badge}")
            if rationale := p.get("rationale"):
                out.append(rationale.strip())
                out.append("")

    if hw := strategy.get("how_we_win"):
        out.append("## How we win")
        for h in hw:
            out.append(f"- **{h.get('title', '')}.** {h.get('description', '').strip()}")
        out.append("")

    if risks := strategy.get("key_risks"):
        out.append("## Key risks")
        for r in risks:
            out.append(f"- {r}")
        out.append("")

    if scope.get("personas") or scope.get("competitors"):
        out.append("## Scope manifest summary")
    if personas := scope.get("personas", {}).get("primary"):
        out.append(f"**Primary personas:** " + ", ".join(f"[`{p}`](../personas/{p}.md)" for p in personas))
        out.append("")
    if archs := scope.get("archetypes", {}).get("primary"):
        out.append(f"**Primary archetypes:** " + ", ".join(f"[`{a}`](../archetypes/{a}.md)" for a in archs))
        out.append("")
    if comps := scope.get("competitors", {}).get("primary"):
        out.append(f"**Primary competitors:** " + ", ".join(f"[`{c}`](../competitors/{c}.md)" for c in comps))
        out.append("")

    if lr := identity.get("last_reviewed"):
        out.append(f"_Last reviewed: {lr}_")

    return "\n".join(out).rstrip() + "\n"


def render_competitor(data: dict, body: str, path: Path) -> str:
    cid = data.get("id", path.stem)
    name = data.get("display_name", cid)
    out = [f"# {name}", "", f"_Competitor profile — parent: {data.get('parent_company', '?')}, category: {data.get('category', '?')}_", ""]

    if pos := data.get("positioning"):
        out.append(f"_{pos}_")
        out.append("")

    if lineup := data.get("lineup"):
        out.append("## Lineup")
        out.append("| SKU | Line | Positioning |")
        out.append("| --- | --- | --- |")
        for s in lineup:
            out.append(f"| `{s.get('id', '')}` | {s.get('line', '')} | {s.get('positioning', '')} |")
        out.append("")

    if posture := data.get("posture"):
        if strengths := posture.get("strengths"):
            out.append("## Strengths")
            for s in strengths:
                out.append(f"- {s}")
            out.append("")
        if weaknesses := posture.get("weaknesses"):
            out.append("## Weaknesses")
            for w in weaknesses:
                out.append(f"- {w}")
            out.append("")

    out.append("---")
    out.append("")
    out.append(body.strip())
    out.append("")
    return "\n".join(out)


def render_sku(data: dict, body: str, path: Path) -> str:
    sid = data.get("id", path.stem)
    name = data.get("display_name", sid)
    line = data.get("line", "?")
    status = data.get("status", "?")
    pos = data.get("positioning", "")

    out = [f"# {name}", "", f"_SKU — {line} line, status: {status}_", "", f"_{pos}_", ""]

    if specs := data.get("specs"):
        out.append("## Specs")
        out.append("| Spec | Value |")
        out.append("| --- | --- |")
        for k, v in specs.items():
            if isinstance(v, list):
                v = ", ".join(str(x) for x in v)
            out.append(f"| {k.replace('_', ' ')} | {v} |")
        out.append("")

    if price := data.get("price_range_usd"):
        out.append(f"**Price range (USD):** ${price[0]:,} – ${price[1]:,}")
        out.append("")

    if uses := data.get("target_use_cases"):
        out.append("## Target use cases")
        for u in uses:
            out.append(f"- {u}")
        out.append("")

    if cs := data.get("competitor_skus", {}).get("primary"):
        out.append("## Head-to-head competitor SKUs")
        out.append("| Competitor SKU | Our advantage | Their advantage |")
        out.append("| --- | --- | --- |")
        for c in cs:
            our = ", ".join(c.get("our_advantage", []))
            their = ", ".join(c.get("their_advantage", []))
            out.append(f"| `{c.get('id', '')}` | {our} | {their} |")
        out.append("")

    out.append("---")
    out.append("")
    out.append(body.strip())
    out.append("")
    return "\n".join(out)


# ---------- index builders ----------

def build_personas_index(personas: dict[str, dict]) -> str:
    out = ["# Personas", "",
           "Reusable persona profiles. Referenced by ID from `scope.yaml` files.", "", "## Index", "",
           "| ID | Display name | Type | Primary archetypes |",
           "| --- | --- | --- | --- |"]
    for pid in sorted(personas):
        p = personas[pid]
        archs = p.get("maps_to_archetypes", {}).get("primary", [])
        archs_str = ", ".join(f"`{a}`" for a in archs) if archs else "—"
        out.append(f"| [`{pid}`]({pid}.md) | {p.get('display_name', pid)} | {p.get('type', '')} | {archs_str} |")
    out.append("")
    return "\n".join(out)


def build_archetypes_index(archetypes: dict[str, dict]) -> str:
    out = ["# Archetypes", "",
           "Behavioral patterns that cross-cut personas. Referenced by ID from `scope.yaml` files.", "", "## Index", "",
           "| ID | Display name | Opposite | Related |",
           "| --- | --- | --- | --- |"]
    for aid in sorted(archetypes):
        a = archetypes[aid]
        opp = a.get("opposite_archetype", "")
        opp_str = f"`{opp}`" if opp else "—"
        rel = ", ".join(f"`{r}`" for r in a.get("related_archetypes", [])) or "—"
        out.append(f"| [`{aid}`]({aid}.md) | {a.get('display_name', aid)} | {opp_str} | {rel} |")
    out.append("")
    return "\n".join(out)


def build_competitors_index(competitors: dict[str, dict]) -> str:
    out = ["# Competitors", "",
           "Competitor profiles with SKU lineup rosters. Referenced by ID from `scope.yaml` files and SKU `competitor_skus` mappings.", "",
           "## Index", "",
           "| ID | Name | Parent company | Category | SKU count |",
           "| --- | --- | --- | --- | --- |"]
    for cid in sorted(competitors):
        c = competitors[cid]
        sku_count = len(c.get("lineup", []))
        out.append(f"| [`{cid}`]({cid}.md) | {c.get('display_name', cid)} | {c.get('parent_company', '?')} | {c.get('category', '?')} | {sku_count} |")
    out.append("")
    return "\n".join(out)


def build_skus_index(skus: dict[str, dict]) -> str:
    out = ["# SKUs", "",
           "Concrete shippable models — leaf nodes of the hierarchy.", "",
           "## Index", "",
           "| ID | Display name | Line | Status | Price range (USD) |",
           "| --- | --- | --- | --- | --- |"]
    for sid in sorted(skus):
        s = skus[sid]
        price = s.get("price_range_usd")
        price_str = f"${price[0]:,}–${price[1]:,}" if price else "—"
        out.append(f"| [`{sid}`]({sid}.md) | {s.get('display_name', sid)} | {s.get('line', '')} | {s.get('status', '')} | {price_str} |")
    out.append("")
    return "\n".join(out)


def build_competitor_crosswalk(skus: dict[str, dict]) -> str:
    out = ["# SKU competitor crosswalk", "",
           "Head-to-head competitor SKU mappings declared in our SKU files.", "",
           "| Our SKU | Line | Competitor SKU | Our advantage | Their advantage |",
           "| --- | --- | --- | --- | --- |"]
    for sid in sorted(skus):
        s = skus[sid]
        for c in s.get("competitor_skus", {}).get("primary", []):
            our = ", ".join(c.get("our_advantage", []))
            their = ", ".join(c.get("their_advantage", []))
            out.append(f"| `{sid}` | {s.get('line', '')} | `{c.get('id', '')}` | {our} | {their} |")
    out.append("")
    return "\n".join(out)


def build_hierarchy_index(units: list[tuple[str, str, dict, dict, dict, dict]]) -> str:
    """Render hierarchy index with a Mermaid diagram of loaded units."""
    out = ["# Hierarchy", "",
           "Six-level organizational hierarchy. Each level above SKU has identity / charter / strategy / scope manifests.", "",
           "## Map", "",
           "```mermaid",
           "graph TD"]

    # build node ids and edges
    by_kind: dict[str, list[str]] = {"company": [], "organizations": [],
                                     "portfolios": [], "products": []}
    for level, name, identity, _, _, _ in units:
        by_kind.setdefault(level, []).append((name, identity.get("display_name", name)))

    for level in ["company", "organizations", "portfolios", "products"]:
        for name, display in by_kind.get(level, []):
            node_id = slugify(f"{level}-{name}")
            out.append(f'    {node_id}["{display}<br/>({level})"]')

    # edges via parent: in scope.yaml — fall back to nesting order
    parents = {}
    for level, name, _, _, _, scope in units:
        if p := scope.get("parent"):
            # parent path like "portfolios/pro-workstations"
            kind, pname = p.split("/", 1)
            parents[(level, name)] = (kind, pname)

    for (level, name), (pkind, pname) in parents.items():
        node = slugify(f"{level}-{name}")
        parent = slugify(f"{pkind}-{pname}")
        out.append(f"    {parent} --> {node}")

    out.append("```")
    out.append("")

    # unit list
    out.append("## Units")
    out.append("")
    out.append("| Level | Name | Display | Identity | Strategy |")
    out.append("| --- | --- | --- | --- | --- |")
    for level, name, identity, _, _, _ in units:
        link = f"{level}/{name}.md"
        out.append(f"| {level} | `{name}` | [{identity.get('display_name', name)}]({link}) | {'✓' if identity else '—'} | {'✓' if identity else '—'} |")
    out.append("")

    return "\n".join(out)


def build_index() -> str:
    return """# Shared context

Generated views of the structured organizational context that agents inject
into skills via the scope system. All views are auto-generated from
`.claude/shared/` YAML by `scripts/build-shared-docs.py` at site-build time.

## Sections

- [**Hierarchy**](hierarchy.md) — six-level org map (company → organization → portfolio → product → line → SKU) with Mermaid diagram
- [**Personas**](personas/index.md) — reusable persona profiles
- [**Archetypes**](archetypes/index.md) — behavioral patterns that cross-cut personas
- [**Competitors**](competitors/index.md) — competitor profiles with SKU lineup rosters
- [**SKUs**](skus/index.md) — concrete shippable models, with competitor crosswalk

## How agents use this

Agents do **not** browse `shared/` directly. The scope system handles loading:

1. PM runs `/scope <path>` once per session.
2. Activity slash command (e.g., `/competitive-analysis`) walks the scope chain, merges manifests, loads referenced atomic profiles, and hands the resolved context to the underlying skill.
3. Skill stays generic and never reads `shared/`.

See [the architecture doc](../architecture.md) for the full pattern.
"""


# ---------- main ----------

def main():
    if not SHARED.exists():
        print(f"No {SHARED} — skipping shared docs build")
        return

    # Clean output
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # ---- Personas ----
    personas: dict[str, dict] = {}
    for p in sorted((SHARED / "personas").glob("*.yaml")):
        data = load(p)
        personas[data.get("id", p.stem)] = data
        write(OUT / "personas" / f"{p.stem}.md", render_persona(data, p))
    write(OUT / "personas" / "index.md", build_personas_index(personas))

    # ---- Archetypes ----
    archetypes: dict[str, dict] = {}
    for p in sorted((SHARED / "archetypes").glob("*.yaml")):
        data = load(p)
        archetypes[data.get("id", p.stem)] = data
        write(OUT / "archetypes" / f"{p.stem}.md", render_archetype(data, p))
    write(OUT / "archetypes" / "index.md", build_archetypes_index(archetypes))

    # ---- Competitors (markdown with frontmatter) ----
    competitors: dict[str, dict] = {}
    for p in sorted((SHARED / "competitors").glob("*.md")):
        text = p.read_text()
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm = yaml.safe_load(text[3:end])
                body = text[end + 4:].lstrip("\n")
                competitors[fm.get("id", p.stem)] = fm
                write(OUT / "competitors" / f"{p.stem}.md", render_competitor(fm, body, p))
    write(OUT / "competitors" / "index.md", build_competitors_index(competitors))

    # ---- SKUs (markdown with frontmatter) ----
    skus: dict[str, dict] = {}
    for p in sorted((SHARED / "products").rglob("skus/*.md")):
        text = p.read_text()
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm = yaml.safe_load(text[3:end])
                body = text[end + 4:].lstrip("\n")
                skus[fm.get("id", p.stem)] = fm
                write(OUT / "skus" / f"{p.stem}.md", render_sku(fm, body, p))
    write(OUT / "skus" / "index.md", build_skus_index(skus))
    write(OUT / "skus" / "competitor-crosswalk.md", build_competitor_crosswalk(skus))

    # ---- Hierarchy units ----
    units: list[tuple[str, str, dict, dict, dict, dict]] = []
    for kind in ("company", "organizations", "portfolios", "products"):
        kind_dir = SHARED / kind
        if not kind_dir.exists():
            continue
        for unit_dir in sorted(kind_dir.iterdir()):
            if not unit_dir.is_dir():
                continue
            identity = load(unit_dir / "identity.yaml") if (unit_dir / "identity.yaml").exists() else {}
            charter = load(unit_dir / "charter.yaml") if (unit_dir / "charter.yaml").exists() else {}
            strategy = load(unit_dir / "strategy.yaml") if (unit_dir / "strategy.yaml").exists() else {}
            scope = load(unit_dir / "scope.yaml") if (unit_dir / "scope.yaml").exists() else {}
            if identity or charter or strategy or scope:
                units.append((kind, unit_dir.name, identity, charter, strategy, scope))
                content = render_hierarchy_unit(kind, unit_dir.name, identity, charter, strategy, scope)
                write(OUT / kind / f"{unit_dir.name}.md", content)

    write(OUT / "hierarchy.md", build_hierarchy_index(units))

    # ---- Top-level index ----
    write(OUT / "index.md", build_index())

    print(f"Generated {len(personas)} personas, {len(archetypes)} archetypes, "
          f"{len(competitors)} competitors, {len(skus)} SKUs, {len(units)} hierarchy units → {OUT}")


if __name__ == "__main__":
    main()
