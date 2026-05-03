---
description: Convert an existing prompt blob into a properly formatted agent or skill
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob
---

You are importing an existing prompt into the catalogue. The user has prose they've been using as an ad-hoc instruction and wants it converted into a properly formatted subagent or skill entry.

## Steps

1. **Type** (`AskUserQuestion`, single-select): `Subagent`, `Skill`. Use the difference of intent:
   - Subagent = a delegated assistant the parent invokes for a chunk of work.
   - Skill = a triggered procedure the model executes when keywords match.
2. **Source** (`AskUserQuestion`, single-select): `Paste it inline`, `Read from a file path`. If file path, ask for the path and `Read` it.
3. Read the prompt text and propose:
   - A **name** (kebab-case) inferred from the content.
   - A **description** (one sentence) inferred from the content.
   - The **body**, restructured into the conventional sections for the chosen type.
4. Show the proposed file to the user and ask for confirmation or edits.
5. Once confirmed, hand off to the appropriate workflow:
   - For a subagent, write to `.claude/agents/<name>.md` matching the structure in `.claude/agents/_template.md`.
   - For a skill, create `.claude/skills/<name>/` and write `SKILL.md` matching `.claude/skills/_template/SKILL.md`.
6. Run validation:
   ```bash
   python3 scripts/validate.py <new-path>
   ```
7. Regenerate the README index:
   ```bash
   python3 scripts/index-readme.py
   ```
8. Report the path and remind the user to commit.

## Reference

- Spec: `docs/anthropic-spec.md`
- Conventions: `CONTRIBUTING.md`
