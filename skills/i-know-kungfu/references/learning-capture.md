# Learning capture

A lesson captures the *reasoning* error, not just a bad string — so it generalizes
and is recalled the next time that reasoning recurs.

## Fields (call `kungfu_learn`)

- `misconception` — the wrong belief, in plain words. ("Gleam has early-return like JS.")
- `trigger` — when this wrong thought occurs; the recall key. ("reaching for `return`
  to yield a value")
- `wrong` — the incorrect code/assumption.
- `right` — the correction.
- `model` — the structural reason it is wrong. ("Gleam is expression-oriented; the
  last expression is the value; there is no `return`.")
- `source` — `verify-failure` (best), `user-correction`, or `test-failure`.
- `verified` — `true` if the `right` actually compiled.
- `error_type` — optional; otherwise auto-classified (see `error-taxonomy.md`).

## When to capture

- **Right after a `kungfu_verify` failure you fixed** — the failed code and the fix
  are a ready-made wrong→right pair; use `source="verify-failure"`, `verified=true`.
- **When the user corrects you** — `source="user-correction"`.

Capture in known languages too (e.g. Python): the learn loop is language-agnostic.

## Recall, dedupe, rollup

- `kungfu_lookup` surfaces lessons whose `trigger` matches your task, *before* you
  write — that is how you "already know" the right answer next time.
- Re-recording the same trigger does not duplicate it; it increments `seen`.
- Recurring or verified lessons are folded into `skeleton.md` ("Learned rules"), so
  the language's structure accretes instead of a flat list of fixes.

## Write the model, not just the fix

A lesson that only says "use `list.fold`" is weak. A lesson whose `model` explains
"the language has no early return; everything is an expression" prevents a whole
family of mistakes. Always fill `model`.
