# ADR-0003: Assemble docs/ at build time from sources spread across the repo

- **Status:** accepted
- **Date:** 2026-05-03
- **Deciders:** repo owner

## Context

Default MkDocs convention puts all documentation under a single `docs/` folder. This repo's content is deliberately spread across several top-level locations:

- `README.md`, `CONTRIBUTING.md`, `CLAUDE.md` at the repo root.
- `.claude/agents/` and `.claude/skills/` — the catalogue, kept under `.claude/` so the repo can be dropped into a Claude Code installation as-is.
- `.claude/shared/` — subject content (strategy, personas, archetypes, etc.).
- `docs/` — specs, intake forms, ADRs.

Surfacing all of it in one site requires getting all the markdown into a single tree that MkDocs can read.

The first attempt set `docs_dir: .` (the repo root) so MkDocs would walk every directory. **MkDocs explicitly forbids this** — `docs_dir` cannot be the parent of the config file. Build fails with a configuration error.

A second design constraint: the framework must be **subject-agnostic**. Hardcoding paths like `.claude/shared/portfolios/pro-workstations/...` into `mkdocs.yml` would couple the generator config to a specific subject. Adding a new portfolio (e.g. rugged) shouldn't require config edits.

## Decision

Use the conventional `docs_dir: docs` and assemble the docs tree at build time with a small shell script (`scripts/build-docs.sh`). The script:

1. Copies `README.md`, `CONTRIBUTING.md`, `CLAUDE.md` to `docs/index.md`, `docs/contributing.md`, `docs/claude.md`.
2. Copies `.claude/agents/`, `.claude/skills/`, `.claude/shared/` into `docs/agents/`, `docs/skills/`, `docs/shared/`.
3. Rewrites repo-relative links in the copied root docs so they resolve under `docs/`.

The Pages workflow runs the script before `mkdocs build`. Local preview works the same way: run `scripts/build-docs.sh && mkdocs serve`.

The copied paths under `docs/` are gitignored — source of truth stays in its native location.

## Consequences

- **Positive:** every `.md` in the repo (root files, catalogue, `.claude/shared/`, `docs/`) becomes part of the site. No duplication in version control.
- **Positive:** new content under `.claude/agents/`, `.claude/skills/`, or `.claude/shared/` appears in the site automatically — the script picks up whatever's there. No `mkdocs.yml` edits required to add a portfolio, agent, skill, or ADR. Framework is fully pluggable.
- **Positive:** sticking with the conventional `docs_dir: docs` means MkDocs and its ecosystem (plugins, tooling, examples) work as documented.
- **Negative:** local preview now requires running the build script first. Documented in `CONTRIBUTING.md`.
- **Negative:** the link-rewrite step in the script is a string-replace; if a contributor adds a link pattern not covered by the rewrites, the link will be broken in the site (but fine in the source). Rewrite rules are easy to extend.

## Alternatives considered

- **`docs_dir: .` (the repo root):** rejected — MkDocs forbids it.
- **`docs_dir: docs/` + symlinks from `docs/` to `.claude/`:** rejected — symlinks behave inconsistently across platforms (Windows contributors, some CI runners).
- **Move all content into `docs/`:** rejected — `.claude/` is a Claude Code convention; moving it breaks the drop-in install pattern and the slash commands that reference those paths.
- **[`monorepo` plugin](https://github.com/backstage/mkdocs-monorepo-plugin):** rejected — designed for combining separate sub-projects with their own `mkdocs.yml`. Overkill for this single-repo case and adds a dependency.

## References

- `mkdocs.yml` (repo root) — resulting configuration.
- `scripts/build-docs.sh` — the assembly script.
- [awesome-pages plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) — auto-discovered nav once content is in `docs/`.
