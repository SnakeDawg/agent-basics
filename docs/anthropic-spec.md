# Anthropic spec reference

**Last verified:** 2026-05-02

This document is the in-repo source of truth for the Claude Code subagent and skill formats. Builders (`/new-agent`, `/new-skill`) reference this file for offline use. The live canonical docs live at https://docs.claude.com/en/docs/claude-code and can be fetched on demand via WebFetch when the user explicitly asks for "latest."

## Subagents

- **File location:** `.claude/agents/<name>.md` (project-level) or `~/.claude/agents/<name>.md` (user-level).
- **Discovery:** Claude Code auto-discovers files matching this pattern; they appear in `/agents`.
- **Filename rule:** the filename stem MUST match the `name` frontmatter field.

### Frontmatter

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `name` | yes | string (kebab-case) | Must match the filename stem. |
| `description` | yes | string (one sentence) | Trigger Claude reads when deciding to delegate. |
| `tools` | no | comma-separated string | Subset of available tools. Omit to inherit all. |
| `model` | no | enum | `opus`, `sonnet`, `haiku`, or `inherit`. |

### Body

Free-form markdown; conventional sections:
- **Role** — what the agent is.
- **When to use** — explicit triggers and scope.
- **Constraints** — what the agent must not do; output format.

### Reference docs
- https://docs.claude.com/en/docs/claude-code/sub-agents

## Skills

- **File location:** `.claude/skills/<skill-name>/SKILL.md`.
- **Discovery:** Claude Code auto-discovers `SKILL.md` files in this layout; the model invokes via the Skill tool when descriptions match.
- **Directory rule:** the directory name MUST match the `name` frontmatter field.
- **Supporting files:** scripts, references, and examples live alongside `SKILL.md` in the same directory and can be referenced from the body.

### Frontmatter

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `name` | yes | string (kebab-case) | Must match the directory name. |
| `description` | yes | string (one sentence) | Trigger Claude reads when deciding to invoke. |

### Body

Free-form markdown; conventional sections:
- **When this triggers** — keywords or situations.
- **Steps** — what the skill does.
- **Output format** — how results should look.

### Reference docs
- https://docs.claude.com/en/docs/claude-code/skills

## Slash commands (related infrastructure)

Not catalogued as agents or skills, but the `/new-agent`, `/new-skill`, etc. workflows in this repo are built as slash commands.

- **File location:** `.claude/commands/<name>.md`.
- **Frontmatter fields:** `description`, `argument-hint`, `allowed-tools`, `model`.
- **Body:** the prompt template Claude executes when the command is invoked. `$ARGUMENTS` interpolates everything after the command; `$1`, `$2`, ... interpolate positional args.
- **Reference:** https://docs.claude.com/en/docs/claude-code/slash-commands

## Conventions specific to this repo

- Names are kebab-case, lowercase, no spaces. The only exception is the `_template` prefix used for non-functional scaffolding entries.
- Each new entry must update the catalogue tables in `README.md`. The `/index-readme` command regenerates these tables automatically.
- Validation rules (filename matches `name`, required fields present, kebab-case) are enforced by `scripts/validate.py` and exposed via `/validate-catalogue`.

## Drift policy

When this file's "last verified" date is older than 30 days, the builders should suggest running WebFetch against the reference doc URLs above and offer to update this file with any spec changes.
