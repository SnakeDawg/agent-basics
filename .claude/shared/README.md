# Shared context

Structured organizational context that agents inject into skills via the scope system. Two file shapes: **structured YAML** for facts (always preferred), **prose markdown** only where structure can't carry the meaning.

## Scope (today)

This tree is currently scoped to **Acme Computing → Commercial Devices Group → Pro Workstation portfolio → Pro Workstation PC → mobile / fixed lines → SKUs**. As the catalogue grows we can add sibling branches for other organizations, portfolios, or products.

## Layout

```
shared/
├── company/<name>/                          # corporate level
│   ├── identity.yaml                        # mission, vision, values, brand
│   ├── charter.yaml                         # scope, decision rights, stakeholders
│   ├── strategy.yaml                        # priorities, initiatives, hypotheses
│   └── scope.yaml                           # operational scope manifest
├── organizations/<name>/                    # business unit level
│   ├── identity.yaml
│   ├── charter.yaml
│   ├── strategy.yaml
│   └── scope.yaml
├── portfolios/<name>/                       # product family level
│   ├── identity.yaml
│   ├── charter.yaml
│   ├── strategy.yaml
│   └── scope.yaml
├── products/<name>/                         # individual product level
│   ├── identity.yaml
│   ├── charter.yaml
│   ├── strategy.yaml
│   ├── scope.yaml
│   └── lines/<line>/
│       ├── scope.yaml                       # line-specific filters
│       └── skus/<sku-id>.md                 # SKU file: frontmatter-heavy + short narrative
├── personas/<id>.yaml                       # reusable persona profiles
├── archetypes/<id>.yaml                     # reusable behavioral patterns
└── competitors/<id>.md                      # competitor profiles with lineup roster
```

## File types and when to use which

| File | Format | Lifecycle | Purpose |
| --- | --- | --- | --- |
| `identity.yaml` | YAML | annual | Mission, vision, position, brand pillars, what-we-are-not |
| `charter.yaml` | YAML | rare (re-org) | Mandate, in/out scope, decision rights, stakeholders, success metrics |
| `strategy.yaml` | YAML | quarterly | Horizon, priorities, initiatives, hypotheses, time horizons, risks |
| `scope.yaml` | YAML | as needed | Operational manifest — personas, archetypes, competitors, per-activity filters |
| Persona / archetype | YAML | as needed | Atomic reusable profiles referenced by ID from `scope.yaml` |
| Competitor | Markdown + frontmatter | as needed | Competitor profile with `lineup:` roster of their SKUs |
| SKU | Markdown + frontmatter | per refresh | Concrete shippable model — specs, price, head-to-head competitor pairs, short positioning narrative |

## How agents reference these files

Agents do **not** browse `shared/` directly. The scope system handles loading:

1. PM runs `/scope <path>` once per session.
2. Activity slash command (e.g., `/competitive-analysis`) walks the scope chain, merges manifests, loads referenced atomic profiles, and hands the resolved context to the underlying skill.
3. Skill stays generic and never reads `shared/`.

See `docs/architecture.md` for the full pattern and `.claude/commands/scope.md` for the slash command.

## Authoring conventions

- **Filename:** kebab-case, lowercase. YAML files use `.yaml`; SKUs and competitor profiles use `.md` with YAML frontmatter.
- **`placeholders:` field** in any YAML file: list of "TBD" notes flagging where the content needs validation against authoritative internal sources. Agents cite these as gaps rather than fabricate around them.
- **`last_reviewed:` field** at the bottom of every YAML file: ISO date, refreshed when content is updated.
- **No prose-heavy `.md` files at the hierarchy levels.** If narrative is genuinely needed beyond what structured fields can carry, add an optional `narrative.md` at that level — only when the structure can't capture the meaning.

## Adding a new branch

- **New organization** → `organizations/<name>/` with `identity.yaml`, `charter.yaml`, `strategy.yaml`, `scope.yaml`.
- **New portfolio** → `portfolios/<name>/` with the same four files.
- **New product** → `products/<name>/` plus `lines/<line>/scope.yaml` and `skus/<sku-id>.md` files for each shipping SKU.
- **New persona / archetype / competitor** → drop a single file under `personas/`, `archetypes/`, or `competitors/` and reference it by ID from any `scope.yaml`.
