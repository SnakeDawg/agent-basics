---
description: Interview the user and scaffold a new skill at .claude/skills/<name>/SKILL.md
argument-hint: "[skill-name]"
allowed-tools: AskUserQuestion, Read, Write, WebFetch, Bash, Glob
---

You are scaffolding a new Claude Code **skill** for this catalogue. Drive an interview, then write the file.

## Reference material — read first

1. `docs/anthropic-spec.md` — embedded source of truth for the skill format. Check the "Last verified" date.
2. `CONTRIBUTING.md` — repo-specific naming and frontmatter conventions.
3. `.claude/skills/_template/SKILL.md` — starting skeleton.
4. `.claude/skills/example-greeting/SKILL.md` — concrete reference example.

If the user explicitly asks for "latest docs," "fresh from Anthropic," or the spec doc's last-verified date is older than 30 days, WebFetch:
- https://docs.claude.com/en/docs/claude-code/skills

Compare against `docs/anthropic-spec.md` and surface any changes before continuing. Offer to update the spec doc.

## Interview

If `$ARGUMENTS` is non-empty, use it as the proposed skill name and skip step 1's question (still validate).

Use `AskUserQuestion` for fixed-choice fields. Use plain prompts for free-text. Don't batch unrelated questions.

1. **Name** (free-text) — kebab-case, lowercase. Reject and re-ask if:
   - Not kebab-case (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`).
   - Directory `.claude/skills/<name>/` already exists (use Glob).
2. **Description** (free-text) — one sentence specifying when Claude should invoke. Be explicit about trigger phrases or situations; this is what the model reads when deciding.
3. **When this triggers** (free-text) — bullet list of trigger phrases or scenarios.
4. **Steps** (free-text) — numbered list of what the skill does end-to-end.
5. **Output format** (free-text) — what the user should see when the skill produces a result.
6. **Supporting files?** (`AskUserQuestion`, single-select): `None`, `Yes — I'll add them later`. If the latter, mention that they go alongside `SKILL.md` in the same directory and can be referenced from the body.

## Write the file

Create the directory `.claude/skills/<name>/` and write `SKILL.md`:

```markdown
---
name: <name>
description: <one-sentence trigger>
---

# <Skill name (Title Case)>

<one-paragraph summary>

## When this triggers

<bullets from interview step 3>

## Steps

<numbered list from interview step 4>

## Output format

<from interview step 5>
```

## Post-write steps

1. Run validation:
   ```bash
   python3 scripts/validate.py .claude/skills/<name>/SKILL.md
   ```
   If it fails, show the errors and offer to fix and re-write.
2. Regenerate the README index:
   ```bash
   python3 scripts/index-readme.py
   ```
3. Report the path of the new file and remind the user to commit.
