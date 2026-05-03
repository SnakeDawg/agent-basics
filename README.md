# Agent + skill catalogue

A foundational catalogue of reusable Claude Code **subagents** and **skills**, distributed as plain markdown so the catalogue can grow incrementally.

## Layout

```
.
├── CLAUDE.md                  # repo memory for Claude sessions working here
├── README.md                  # this file (catalogue tables auto-generated)
├── CONTRIBUTING.md            # naming + frontmatter spec, add-an-entry guide
├── docs/
│   └── anthropic-spec.md      # canonical spec, last-verified date
├── scripts/
│   ├── validate.py            # frontmatter + naming linter (stdlib-only)
│   ├── index-readme.py        # regenerates the catalogue tables below
│   ├── install-hooks.sh       # one-time: enable .githooks/ for this repo
│   └── export-plugin.sh       # produces dist/plugin/ for /plugin install
├── .githooks/
│   └── pre-commit             # runs validator + index check before commit
├── .github/workflows/
│   └── validate.yml           # same checks on PRs and pushes
└── .claude/
    ├── agents/                # one .md per subagent
    ├── skills/                # one directory per skill
    └── commands/              # slash commands powering the workflows
```

The repo is pre-wrapped under `.claude/` so the same tree Claude Code expects at runtime is the same tree you check in.

## Install

- **User-level (all your projects):**
  ```sh
  ln -s "$PWD/.claude/agents"/*   ~/.claude/agents/
  ln -s "$PWD/.claude/skills"/*   ~/.claude/skills/
  ln -s "$PWD/.claude/commands"/* ~/.claude/commands/
  ```
- **Project-level:** symlink (or copy) `.claude/` into a target project root.
  ```sh
  ln -s "$PWD/.claude" /path/to/project/.claude
  ```
- **Cherry-pick:** copy a single `agents/<name>.md` file or `skills/<name>/` directory into the target project's `.claude/`.
- **Plugin install:** run `scripts/export-plugin.sh` to produce `dist/plugin/`, then `/plugin install` from that path.

After install, run `/agents` inside Claude Code to confirm the subagents are discovered. Skills and slash commands are picked up automatically.

## Workflows

| Command | Purpose |
| --- | --- |
| `/new-agent [name]` | Interview-driven scaffolding for a new subagent. |
| `/new-skill [name]` | Interview-driven scaffolding for a new skill. |
| `/migrate-prompt` | Import an existing prompt blob as an agent or skill. |
| `/validate-catalogue [path]` | Lint frontmatter and naming. |
| `/index-readme` | Regenerate the catalogue tables in this README. |

Run `/validate-catalogue` and `/index-readme` before committing changes that add or rename entries — or enable the pre-commit hook to enforce both automatically:

```sh
scripts/install-hooks.sh   # one-time per clone; sets core.hooksPath to .githooks/
```

The same checks run on every PR and branch push via `.github/workflows/validate.yml`.

## Catalogue

### Agents

<!-- agents:start -->
| Name | Description |
| --- | --- |
| [`example-explainer`](.claude/agents/example-explainer.md) | Explains a code snippet in plain English. Use when the user asks "what does this code do?" or wants a walkthrough of unfamiliar code. |
<!-- agents:end -->

### Skills

<!-- skills:start -->
| Name | Description |
| --- | --- |
| [`example-greeting`](.claude/skills/example-greeting/SKILL.md) | Trivial greeting skill used to verify skill discovery. Trigger when the user asks Claude to introduce itself or says "run the example greeting skill". |
<!-- skills:end -->

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for naming rules, frontmatter spec, and the steps to add a new entry. The full spec lives in [`docs/anthropic-spec.md`](docs/anthropic-spec.md).
