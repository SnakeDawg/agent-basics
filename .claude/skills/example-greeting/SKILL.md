---
name: example-greeting
description: Trivial greeting skill used to verify skill discovery. Trigger when the user asks Claude to introduce itself or says "run the example greeting skill".
---

# Example greeting

A minimal skill that exists to prove the catalogue's skill discovery works end-to-end.

## When this triggers

- The user explicitly asks to run the example greeting skill.
- The user asks Claude to introduce itself in the context of this catalogue.

## Steps

1. Greet the user by name if known, otherwise say "Hello".
2. State that the `example-greeting` skill was invoked successfully.
3. Point at `CONTRIBUTING.md` as the next read for adding real skills.

## Output format

A two-or-three sentence reply. No code blocks, no headings.
