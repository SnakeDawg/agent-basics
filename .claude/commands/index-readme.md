---
description: Regenerate the agent and skill catalogue tables in README.md
allowed-tools: Bash, Read
---

Run the indexer:

```bash
python3 scripts/index-readme.py
```

Then:

- If the script reports "README.md regenerated," show a short diff (e.g. `git diff --no-color README.md | head -60`) so the user can sanity-check.
- If it reports "already up to date," just confirm and stop.
- If it errors about missing markers, instruct the user to add `<!-- agents:start -->` / `<!-- agents:end -->` and `<!-- skills:start -->` / `<!-- skills:end -->` pairs to `README.md` where each table should live.
