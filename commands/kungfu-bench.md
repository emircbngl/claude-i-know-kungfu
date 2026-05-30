---
description: Measure cold (no KB) vs warm (with grounding) pass rates on held-out tasks — reports honest numbers, including null results.
argument-hint: [language] [list|selfcheck|cold|warm|report]
---

Read the `i-know-kungfu` skill. Parse the language and action from: $ARGUMENTS.

- `list` → `kungfu_bench(language, action="list")` and show the train/test tasks.
- `selfcheck` → `kungfu_bench(language, action="selfcheck")`; the reference solutions should all pass (validates suite + sandbox).
- `cold` → for each **test** task, write a solution using ONLY your own knowledge (do NOT call kungfu_lookup), then `kungfu_bench(language, action="score", split="test", solutions=…, label="cold")`.
- `warm` → first learn from the **train** split (solve each, `kungfu_verify`, capture lessons), then solve the **test** split using `kungfu_lookup`, and `kungfu_bench(…, label="warm")`.
- `report` → `kungfu_bench(language, action="report")` and write the returned markdown into `BENCHMARK.md`.

Never invent numbers: if a run is marked not measurable (Docker down), report that instead of a result.
