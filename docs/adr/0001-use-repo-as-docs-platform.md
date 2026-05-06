# ADR-0001: Use this repo as the docs platform instead of an external wiki

- **Status:** accepted
- **Date:** 2026-05-03
- **Deciders:** repo owner

## Context

Teams contributing to this catalogue (agents, skills, strategy, personas, archetypes, and supporting documentation) need a single browsable home for that content. The default options were:

1. **External wiki** (Confluence, Notion, etc.) — separate from the repo, requires accounts, has its own editor, drifts out of sync with the markdown source of truth.
2. **GitHub repo + Pages** — markdown stays in version control, edits go through PRs, the published site rebuilds automatically.

The repo already stores everything as plain markdown by design (see `CLAUDE.md` at the repo root). Maintaining a parallel wiki would mean copying content out of git and accepting two sources of truth.

## Decision

Use this repo as the single source of truth for all documentation — agent/skill catalogue, subject content under `.claude/shared/`, technical specs, intake forms, and architecture decisions. Publish the content as a GitHub Pages site so non-contributors can browse without cloning.

## Consequences

- **Positive:** one source of truth (git). All edits are reviewable as PRs. History is permanent. Forking the repo gives a downstream team a clean copy of the structure plus their own content.
- **Positive:** non-technical contributors can still participate via the strategy intake form (kept in the repo at `docs/intake/strategy-intake.md`, intentionally not published) — they fill out fields, someone else converts to markdown.
- **Negative:** no WYSIWYG editor. Direct contributors need to be comfortable with markdown (or use the intake form path).
- **Negative:** publishing requires a working build pipeline; if that breaks, the site goes stale until fixed.

## Alternatives considered

- **Confluence / Notion / similar wiki:** rejected because content would drift from the markdown source, requires per-team accounts, and adds an external dependency.
- **Plain README-only browsing on GitHub:** rejected because GitHub's markdown rendering doesn't provide search, sidebar navigation, or a coherent index across folders.

## References

- `CLAUDE.md` (repo root) — project conventions, markdown-first rationale.
- [ADR-0002](0002-use-mkdocs-material-over-jekyll.md) — choice of static-site generator.
- [ADR-0003](0003-mkdocs-docs-dir-equals-repo-root.md) — layout choice that lets MkDocs read content from anywhere in the repo.
