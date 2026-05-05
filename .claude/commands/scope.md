---
description: Set or inspect the active context scope for activity slash commands. Writes a small state file under .claude/state/ that subsequent commands (e.g., /competitive-analysis, /market-research) read at start.
argument-hint: <scope-path> | clear
---

# /scope — set the active scope

Manage the active context scope for this session. Activity slash commands (`/competitive-analysis`, `/market-research`, `/prd`, etc.) read this scope to know which personas, archetypes, competitors, and per-activity filters to apply.

## Usage

| Invocation | Effect |
| --- | --- |
| `/scope <path>` | Set active scope. `<path>` is relative to `.claude/shared/`, e.g. `products/pro-workstation-pc/lines/mobile`. |
| `/scope <path-to-sku>.md` | Set active scope to a SKU leaf node (path includes the `.md`). |
| `/scope` (no args) | Print the current scope and the chain it resolves through. |
| `/scope clear` | Empty the state file. |

## Behavior

### When given a scope path (directory or SKU file)

1. Verify the path resolves under `.claude/shared/`:
   - For a directory path: `.claude/shared/<path>/scope.yaml` must exist.
   - For a SKU path (ends with `.md`): the file must exist and have YAML frontmatter with at least `id` and `line`.
2. If the path is invalid, report what's missing and stop. Don't write the state file.
3. If valid, write the path (without `.claude/shared/` prefix) to `.claude/state/active-scope`. Create `.claude/state/` if it doesn't exist.
4. Confirm to the user with the resolved chain (parent → company root).

### When given no argument

1. Read `.claude/state/active-scope`. If missing or empty, report "no active scope set."
2. If set, print:
   - The current scope.
   - The resolved chain (every level walked from the scope up to the company root).
   - A summary of what's loaded at each level (counts of personas, archetypes, competitors).

### When given `clear`

1. Empty `.claude/state/active-scope`.
2. Confirm to the user.

## Scope chain walking

For a scope path, walk up by reading each `scope.yaml`'s `parent:` field. The chain ends at the company level (no `parent:`). For SKU-level paths, the chain starts at the line containing the SKU file.

Example chain for `products/pro-workstation-pc/lines/mobile/skus/pwm-5000.md`:

```
pwm-5000.md (SKU frontmatter)
  → products/pro-workstation-pc/lines/mobile/scope.yaml
    → products/pro-workstation-pc/scope.yaml
      → portfolios/pro-workstations/scope.yaml
        → organizations/commercial-devices/scope.yaml
          → company/acme-computing/scope.yaml  (no parent — root)
```

## State file location

`.claude/state/active-scope` — single line, the scope path. Gitignored. Per-clone, per-PM.

## Why this exists

Without scope, every activity command has to be told manually what context to use. With scope, the PM declares it once at session start; every subsequent command picks it up automatically. Multi-PM repos: each PM has their own active scope locally, no conflicts because the state file isn't committed.
