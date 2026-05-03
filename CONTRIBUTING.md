# Contributing

How to add a new agent or skill to the catalogue.

The fast path is the interview-driven slash commands — they enforce the conventions in this document automatically:

| Command | Purpose |
| --- | --- |
| `/new-agent [name]` | Scaffold a new subagent. |
| `/new-skill [name]` | Scaffold a new skill. |
| `/migrate-prompt` | Import an existing prompt blob. |
| `/validate-catalogue [path]` | Lint frontmatter and naming. |
| `/index-readme` | Regenerate the README catalogue tables. |

The rest of this document is the manual reference. The canonical Anthropic spec lives in [`docs/anthropic-spec.md`](docs/anthropic-spec.md).

## Naming

- `kebab-case`, lowercase, no spaces.
- The filename stem (for agents) or directory name (for skills) **must match** the `name:` field in YAML frontmatter.

## Agents

Path: `.claude/agents/<name>.md`

```markdown
---
name: <name>
description: One sentence describing when Claude should delegate to this agent.
tools: Read, Grep, Glob, Bash         # optional; omit to inherit all tools
model: sonnet                          # optional: opus | sonnet | haiku | inherit
---

System prompt body. Cover:

- **Role** — what this agent is.
- **When to use** — triggers and scope.
- **Constraints** — what it must not do.
```

Frontmatter fields:

| Field | Required | Notes |
| --- | --- | --- |
| `name` | yes | Must match the filename stem. |
| `description` | yes | Single sentence; this is the trigger Claude reads when deciding to delegate. |
| `tools` | no | Comma-separated list. Omit to inherit the parent's full toolset. |
| `model` | no | One of `opus`, `sonnet`, `haiku`, or `inherit`. |

## Skills

Path: `.claude/skills/<skill-name>/SKILL.md`

Each skill lives in its own directory. Supporting files (scripts, references, examples) sit alongside `SKILL.md` and can be referenced from the body.

```markdown
---
name: <skill-name>
description: When Claude should invoke this skill. Be specific about triggers.
---

# <Skill name>

Body of skill instructions:

- **When this triggers** — keywords or situations.
- **Steps** — what the skill does.
- **Output format** — how results should look.
```

Frontmatter fields:

| Field | Required | Notes |
| --- | --- | --- |
| `name` | yes | Must match the directory name. |
| `description` | yes | The trigger Claude reads when deciding to invoke. |

## Add an entry (manual)

Prefer the slash commands above. If you want to do it by hand:

1. Copy the matching template:
   - Agent: `.claude/agents/_template.md` → `.claude/agents/<name>.md`
   - Skill: `.claude/skills/_template/` → `.claude/skills/<name>/`
2. Edit the frontmatter (`name`, `description`, optional fields).
3. Replace the body with the actual instructions.
4. Run `python3 scripts/validate.py` to lint.
5. Run `python3 scripts/index-readme.py` to regenerate the README tables.

## Validation

- Frontmatter must be valid YAML between `---` fences.
- The first non-frontmatter line is the body — a blank line after the closing `---` is conventional but not required.
- Run `python3 scripts/validate.py [path]` (or `/validate-catalogue [path]` from inside Claude Code) to check naming, required fields, and frontmatter parsing. Exits non-zero on failure, suitable for hooks or CI.

## Architecture decisions

Significant design choices are recorded as ADRs (Architecture Decision Records) under [`docs/adr/`](docs/adr/README.md). To add one:

1. Copy [`docs/adr/_template.md`](docs/adr/_template.md) to `docs/adr/NNNN-short-slug.md` (next available number).
2. Fill in status, date, context, decision, consequences, and alternatives.
3. Commit. The new ADR appears in the published docs site automatically.

Write an ADR when a decision is hard to reverse, constrains future contributors, or has plausible alternatives that someone might later question. Skip it for routine work. See [`docs/adr/README.md`](docs/adr/README.md) for the full convention.

## Docs site

This repo publishes as a static site via GitHub Pages, built by [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The site auto-rebuilds on every push to `main`.

- **Adding content:** drop a new markdown file anywhere under the repo (e.g. `.claude/agents/<name>.md`, `.claude/shared/portfolios/<name>/...`, `docs/<anything>.md`). It appears in the site automatically — no `mkdocs.yml` edits required.
- **Renaming or reordering sidebar entries:** drop a `.pages` file in the relevant directory using the [awesome-pages](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) syntax.
- **Local preview:**
  ```
  pip install mkdocs-material mkdocs-awesome-pages-plugin
  bash scripts/build-docs.sh   # assembles docs/ from .claude/ + root files
  mkdocs serve                  # http://localhost:8000
  ```
  Re-run `scripts/build-docs.sh` after editing source files outside `docs/` to refresh the preview.

The framework is subject-agnostic: forking this repo and replacing the content under `.claude/shared/` with a different subject works without `mkdocs.yml` edits.
