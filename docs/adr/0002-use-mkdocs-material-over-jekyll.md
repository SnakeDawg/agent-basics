# ADR-0002: Use MkDocs Material as the static-site generator

- **Status:** accepted
- **Date:** 2026-05-03
- **Deciders:** repo owner

## Context

[ADR-0001](0001-use-repo-as-docs-platform.md) committed to publishing the repo as a GitHub Pages site. Two realistic generator choices:

1. **Jekyll** — built into GitHub Pages with zero configuration. Default behavior: every `.md` in the configured docs folder becomes a page. No build step required.
2. **MkDocs Material** — Python-based generator with a polished theme. Requires a small config file and a CI workflow to build and deploy. Provides search, sidebar navigation with sections, code-copy buttons, dark mode, and a Confluence-style UX out of the box.

The goal of this site is to replace external wikis (see ADR-0001). That puts a high bar on navigation and search — without those, the site is functionally inferior to the wiki it's replacing.

## Decision

Use MkDocs Material. The Confluence-style UX (sidebar nav + working full-text search + clean typography) is the whole point; Jekyll's default look does not clear the bar.

## Consequences

- **Positive:** real navigation and search. Site looks professional. Theme is well-maintained and widely adopted (used by many open-source projects' docs).
- **Positive:** plugins exist for common needs (auto-discovered nav, version dropdowns, redirects) — extensible without rewriting the framework.
- **Negative:** adds a build step. The Pages site depends on a GitHub Actions workflow succeeding; a broken workflow = stale site.
- **Negative:** Python build dependency. Contributors who want to preview locally need `pip install mkdocs-material mkdocs-awesome-pages-plugin`.

## Alternatives considered

- **Jekyll (default Pages):** rejected — no built-in search, plain default theme, customizing it well takes more effort than just adopting MkDocs Material.
- **Docusaurus / VitePress / other JS-based generators:** rejected — Node toolchain is heavier than Python for a markdown-only repo, and the team has Python in the stack already (`scripts/validate.py`, `scripts/index-readme.py`).
- **Hugo:** capable but theme ecosystem skews toward blogs rather than docs; Material theme on MkDocs is purpose-built for the use case here.

## References

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- `mkdocs.yml` (repo root) — the resulting configuration.
- `.github/workflows/pages.yml` — the deploy workflow.
