---
description: Lint frontmatter and naming on a single entry or the whole catalogue
argument-hint: "[path]"
allowed-tools: Bash
---

Run the validator. If `$ARGUMENTS` is non-empty, validate only that path; otherwise validate every entry under `.claude/agents/` and `.claude/skills/`.

```bash
python3 scripts/validate.py $ARGUMENTS
```

If failures are reported, summarise them briefly and offer to fix the most common issues:
- `name does not match filename/directory` — rename the file, or update the `name:` field.
- `name is not kebab-case` — propose a kebab-case alternative.
- `missing required field` — fill it in.
- `frontmatter missing or unparseable` — show the malformed frontmatter and propose a fix.
