# Architecture Decision Records

This directory holds short markdown records of architectural and design decisions made for this repo. The format is intentionally lightweight: each ADR captures *why* something was decided so future contributors don't have to re-derive the reasoning.

## Workflow

1. Copy [`_template.md`](_template.md) to a new file named `NNNN-short-slug.md` (next available number, kebab-case slug).
2. Fill in status, date, context, decision, consequences, and alternatives.
3. Commit. The file appears in the docs site automatically — no `mkdocs.yml` edits required.
4. If a later decision supersedes this one, update the original's status to `superseded by ADR-XXXX` instead of deleting it.

## When to write an ADR

Write one when you make a decision that:

- Is hard to reverse (changing it later costs significant work).
- Constrains future contributors (others have to live with the choice).
- Has plausible alternatives that someone might later question.

Skip the ADR for routine work: bug fixes, content edits, doc tweaks, anything tactical.

## Conventions

- File names: `NNNN-short-slug.md` (e.g. `0007-archetype-naming-convention.md`).
- Numbers are sequential and never reused. Superseded ADRs keep their number.
- Status values: `proposed`, `accepted`, `superseded by ADR-NNNN`, `deprecated`.
- Keep each ADR to one decision. Multiple decisions = multiple ADRs.
