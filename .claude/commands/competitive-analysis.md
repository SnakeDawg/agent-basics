---
description: Run a competitive analysis in the active scope. Resolves the scope chain, applies the competitive-analysis activity filters, loads referenced competitor and persona profiles, and invokes the competitive-analysis skill with the focused brief.
argument-hint: [topic] | --scope <path> [topic]
---

# /competitive-analysis — scope-aware competitive analysis

Wraps the `competitive-analysis` skill with scope resolution. The PM sets the scope once via `/scope`; this command reads it and produces a competitive analysis tailored to that scope.

## Usage

| Invocation | Effect |
| --- | --- |
| `/competitive-analysis` | Use active scope from `.claude/state/active-scope`. Topic is inferred from the surrounding conversation, or the user is asked. |
| `/competitive-analysis [topic]` | As above, with explicit topic. |
| `/competitive-analysis --scope <path> [topic]` | One-off scope override. Doesn't change the persisted active scope. |

## Behavior

### Step 1 — resolve scope

1. If `--scope <path>` was passed: use it.
2. Else read `.claude/state/active-scope`.
3. If both are empty: pause and ask the user to run `/scope <path>` first or pass `--scope`. Do not run unscoped.

### Step 2 — walk the scope chain

Starting at the active scope, walk up parents (line → product → portfolio → org → company), reading each `scope.yaml` (or, for SKU-level scopes, the SKU file's frontmatter).

### Step 3 — merge manifests

- Lists at each level concatenate.
- A child's `excluded:` removes items inherited from parents.
- A child's `primary:` overrides a parent's `secondary:` for the same item (promotion).

### Step 4 — extract competitive-analysis filters

From the merged manifest, pull `activity_scope.competitive-analysis`:

- `primary_set` — the competitors to focus on.
- `secondary_set` — competitors to mention but not deep-dive.
- `dimensions` — the comparison dimensions to use.
- `exclude_dimensions` — dimensions to skip.

For SKU-level scopes, also pull the SKU's `competitor_skus` — these are 1:1 head-to-head pairs with declared `our_advantage` / `their_advantage` hypotheses.

### Step 5 — load referenced atomic profiles

For each competitor ID in `primary_set` / `secondary_set`: read `.claude/shared/competitors/<id>.md`. For each competitor SKU referenced in `competitor_skus`, look up the competitor SKU within the parent competitor file's `lineup` for context.

If `target_personas` is defined in the merged manifest, also load `.claude/shared/personas/<id>.md` for each.

### Step 6 — invoke the competitive-analysis skill

Hand the skill the resolved, filtered brief:

- Topic (from user prompt or inferred).
- Competitor set (resolved competitor profiles + SKU mappings if applicable).
- Target personas (resolved persona profiles, if any).
- Comparison dimensions (filtered list).
- Excluded dimensions.
- A note that scope was resolved from `<path>` and the chain that was walked.

The skill stays generic — it doesn't read `shared/` or `scope.yaml` itself. All scope work is done here.

### Step 7 — present the result

The skill produces its standard output. Prepend a one-line note about the resolved scope so the PM can verify the right context was used:

> Scope: `products/pro-workstation-pc/lines/mobile/skus/pwm-5000`
> Resolved chain: pwm-5000 → mobile → pro-workstation-pc → pro-workstations → commercial-devices → acme-computing

## What this enables

- **SKU-level head-to-head** when scoped to a SKU. Three 1:1 competitor SKU pairs, not a survey.
- **Line-level competitive landscape** when scoped to a line. The line's competitor set across all your line's SKUs.
- **Portfolio-level strategic competitive view** when scoped to a portfolio. Full competitor lines vs. your portfolio.

Same skill. Same agent. Different scope → different focus.

## Per-invocation override examples

```
/competitive-analysis --scope products/pro-workstation-pc/lines/rugged "vs Toughbook"
/competitive-analysis --scope portfolios/pro-workstations
/competitive-analysis --scope products/pro-workstation-pc/lines/mobile/skus/pwm-7000.md
```
