---
description: Interview the user and scaffold a new subagent at .claude/agents/<name>.md
argument-hint: "[agent-name]"
allowed-tools: AskUserQuestion, Read, Write, WebFetch, Bash, Glob
---

You are scaffolding a new Claude Code **subagent** for this catalogue. Drive an interview, then write the file.

## Reference material — read first

1. `docs/anthropic-spec.md` — embedded source of truth for the subagent format. Check the "Last verified" date.
2. `CONTRIBUTING.md` — repo-specific naming and frontmatter conventions.
3. `.claude/agents/_template.md` — starting skeleton.
4. `.claude/agents/example-explainer.md` — concrete reference example.

If the user explicitly asks for "latest docs," "fresh from Anthropic," or the spec doc's last-verified date is older than 30 days, WebFetch:
- https://docs.claude.com/en/docs/claude-code/sub-agents

Compare against `docs/anthropic-spec.md` and surface any changes to the user before continuing. Offer to update the spec doc.

## Interview

If `$ARGUMENTS` is non-empty, use it as the proposed agent name and skip step 1's question (still validate the name).

Use `AskUserQuestion` for fixed-choice fields. Use plain prompts (write a question, wait for the user's reply) for free-text fields. Don't ask multiple questions at once unless they're related.

1. **Name** (free-text) — kebab-case, lowercase. Reject and re-ask if:
   - Not kebab-case (validate against `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`).
   - File `.claude/agents/<name>.md` already exists (use Glob to check).
2. **Description** (free-text) — one sentence describing when Claude should delegate to this agent. This is the trigger.
3. **Role / system prompt body** (free-text, can span multiple paragraphs) — what the agent is, how it behaves.
4. **Tools** (`AskUserQuestion`, single-select):
   - Inherit all tools (omit `tools` field) — Recommended for general agents.
   - Read-only: `Read, Grep, Glob`
   - Read + Bash: `Read, Grep, Glob, Bash`
   - Custom — follow up with a free-text prompt for a comma-separated list.
5. **Model** (`AskUserQuestion`, single-select): `inherit` (Recommended), `opus`, `sonnet`, `haiku`.
6. **Constraints** (free-text, optional) — what the agent must NOT do, output format expectations. Skip if user has nothing.

## Write the file

Output path: `.claude/agents/<name>.md`

Format:

```markdown
---
name: <name>
description: <one-sentence trigger>
# tools: <if specified>
# model: <if not 'inherit'>
---

# <Agent name>

<role paragraph>

## When to use

<bullets derived from the description and any clarifying answers>

## Constraints

<bullets, or omit the section if the user had no constraints>
```

Only emit the `tools:` and `model:` lines if the user chose non-default values. The `#` placeholder lines above are for reference — do not include commented frontmatter in the final file.

## Post-write steps

1. Run validation:
   ```bash
   python3 scripts/validate.py .claude/agents/<name>.md
   ```
   If it fails, show the errors and offer to fix and re-write.
2. Regenerate the README index:
   ```bash
   python3 scripts/index-readme.py
   ```
3. Report the path of the new file and remind the user to commit.
