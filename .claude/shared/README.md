# Shared context

Reference markdown that agents and skills can read when they need organizational, strategic, or persona context. Not catalogue entries — these files have no YAML frontmatter and are skipped by `scripts/validate.py` and `scripts/index-readme.py`.

## Scope (today)

This tree is currently scoped to **Acme Computing → Commercial Devices Group (Commercial) → Pro Workstation portfolio → Pro Workstation PC**. As the catalogue grows we can add sibling branches for other organizations, portfolios, or products.

## Layout

```
shared/
├── company/                              # parent corporate level
│   └── acme-computing/
│       ├── identity.md                   # who we are: mission, vision, values
│       ├── strategy.md                   # how we win: where we play, priorities
│       └── charter.md                    # scope, decision rights, stakeholders
├── organizations/                        # business unit level
│   └── commercial-devices/
│       ├── identity.md
│       ├── strategy.md
│       └── charter.md
├── portfolios/                           # product family level
│   └── pro-workstations/
│       ├── identity.md
│       ├── strategy.md
│       └── charter.md
├── products/                             # individual product line level
│   └── pro-workstation-pc/
│       ├── identity.md
│       ├── strategy.md
│       └── charter.md
├── personas/
│   ├── internal/                         # users of the agents/skills
│   │   ├── strategist.md
│   │   ├── product-manager-software.md
│   │   └── product-manager-hardware.md
│   └── external/                         # customers being analyzed
│       ├── engineering-manager.md
│       ├── cad-design-engineer.md
│       ├── it-procurement-lead.md
│       └── creative-director.md
└── archetypes/                           # behavioral patterns; cross-cut personas
    ├── pragmatist.md
    ├── innovator.md
    ├── performance-maximizer.md
    ├── compliance-driven.md
    └── cost-conscious.md
```

## How agents reference these files

In an agent or skill body, link by relative path from the repo root:

```markdown
Before answering, read:
- .claude/shared/products/pro-workstation-pc/strategy.md
- .claude/shared/personas/external/engineering-manager.md
- .claude/shared/archetypes/performance-maximizer.md
```

Agents that should read multiple files in this tree should list them explicitly rather than relying on directory globbing — Claude is better at honoring a short, named list than a "read everything in X" instruction.

## Authoring conventions

- **Filename:** kebab-case, lowercase, `.md` extension.
- **Title:** first line is `# <Entity> — <Document type>` (e.g. `# Acme Computing — Identity`). Helps agents quote source clearly.
- **`[TBD: ...]` markers:** wherever proprietary or internal-only specifics belong, use a `[TBD: confirm with <source>]` placeholder. Agents are instructed to cite these as gaps rather than fabricate around them.
- **No YAML frontmatter.** These aren't discoverable agents/skills — they're reference documents the model reads on demand.
- **Last reviewed:** when content gets revised against an authoritative source, drop a `_Last reviewed: YYYY-MM-DD against <source>._` line at the bottom so freshness is visible.

## Adding a new branch

When you expand beyond Pro Workstation PC:
- New organization: create `organizations/<name>/` with the three docs.
- New portfolio under the same org: create `portfolios/<name>/` with the three docs.
- New product under a portfolio: create `products/<name>/` with the three docs.
- New persona: drop into `personas/internal/` or `personas/external/` based on whether the persona uses the agent or is being analyzed by it.
- New archetype: only when a behavioral pattern recurs across enough personas to warrant a reusable name.
