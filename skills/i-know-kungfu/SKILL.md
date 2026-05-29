---
name: i-know-kungfu
description: >
  Write correct code in languages you do NOT know well — without faking it. Use this
  whenever you are about to write, review, or debug code in a niche / new / unfamiliar
  language, DSL, or a post-cutoff library version, or whenever the user worries about
  hallucinated APIs ("don't make up functions", "are you sure that exists", "verify it",
  "you don't know this language"). Also use to learn from a correction so the same mistake
  is not repeated. Triggers on: Gleam, Roc, Unison, Mojo, Nim, Zig, V, niche DSLs, "write
  this in <language I doubt you know>", "stop hallucinating APIs", "verify this compiles",
  "remember this fix", plus the /kungfu-status, /kungfu-lookup, /kungfu-teach, /kungfu-verify,
  /kungfu-learn and /kungfu-bench commands. Backed by the `kungfu` MCP server (knowledge
  store + Docker verifier + benchmark) and a per-language knowledge base at ~/.kungfu.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, mcp__kungfu__kungfu_status, mcp__kungfu__kungfu_lookup, mcp__kungfu__kungfu_save_card, mcp__kungfu__kungfu_verify, mcp__kungfu__kungfu_learn, mcp__kungfu__kungfu_bench
---

# I Know KungFu

You can acquire a new language fast — but only by *actually* acquiring it
(retrieve real docs, then prove it compiles), never by pretending. Pattern-matching
syntax from a language you know into one you don't is the failure this skill exists
to stop.

Track an **epistemic state** for everything you write (see
`references/epistemic-states.md`):

- **VERIFIED** — it compiled/ran in the sandbox. Highest trust.
- **GROUNDED** — backed by a real source you fetched and cited. Trusted, not-yet-run.
- **HYPOTHESIS** — a guess. Allowed while thinking, never allowed at "done".

## Prime directives (never violate)

1. **No HYPOTHESIS survives to completion.** Before you call code finished, every
   non-trivial symbol must be GROUNDED or VERIFIED. Anything still a guess must be
   promoted (fetch/verify) or explicitly disclosed to the user as unverified.
2. **The compiler is truth.** Use `kungfu_verify`. If it is unavailable (no Docker),
   you may NOT claim the code works — say it is UNVERIFIED and why.
3. **Cite or verify every API.** If a function/type/syntax is not in the knowledge
   base and you did not just fetch it from a real source, it is a guess — treat it
   as one.
4. **Negative knowledge counts.** Knowing a feature does *not* exist (no `class`, no
   `null`, no exceptions) prevents most hallucinations. Check the skeleton's
   "Does NOT exist" section.
5. **Capture every fixed mistake** as a lesson with `kungfu_learn` so it is recalled
   next time the same reasoning recurs.

## The loop (managed languages)

```
kungfu_status  →  kungfu_lookup  →  [fetch + kungfu_save_card if gaps]
               →  write code     →  kungfu_verify
               →  if fail: fix + kungfu_learn (wrong→right)  →  repeat
               →  done (state every symbol's epistemic state honestly)
```

1. **Orient** — `kungfu_status(language)`. Is the language managed? Is Docker up?
   What is already known?
2. **Ground** — `kungfu_lookup(language, topic)`. Read the skeleton, the matched
   lessons (wrong→right), and the matched cards *before* writing. If the note says
   there is no grounded knowledge, do not assert from memory.
3. **Fill gaps honestly** — for anything you are unsure of, fetch the real docs
   (Context7 `resolve-library-id`/`get-library-docs` for libraries; `WebFetch`/
   `WebSearch` for syntax), distil a card, and persist it with
   `kungfu_save_card(..., source=<url>)`. See `references/retrieval-discipline.md`.
4. **Write** — small, then verify. Do not write a large unverified blob.
5. **Verify** — `kungfu_verify(language, files)` with the files the image expects
   (e.g. Gleam: `gleam.toml` + `src/*.gleam`). See `references/verification-loop.md`.
6. **Learn** — on any failure you fix, call `kungfu_learn` with the misconception,
   the trigger (the wrong thought), wrong→right, and the structural model. Prefer
   `source='verify-failure'`, `verified=true`. See `references/learning-capture.md`.

For an **unfamiliar language from zero**, run the cold-start flow
(`/kungfu-teach`, `references/adding-a-language.md`) first.

## Honesty when you cannot verify

If Docker is down or no sandbox exists for the language, say so plainly:
"I could not verify this; treat it as unverified." Never dress a guess as a fact.
This is the whole point of the plugin.

## Measuring that it learns

`/kungfu-bench` runs the held-out suite cold (empty KB) vs. warm (after learning
from the train split) and renders a learning curve. It never reports faked numbers:
if code could not be verified, the run is marked not measurable.

## Reference index

- `references/epistemic-states.md` — the four states and the gate rule.
- `references/retrieval-discipline.md` — manifest-first lookup; when and how to fetch.
- `references/verification-loop.md` — building the files dict; reading diagnostics.
- `references/error-taxonomy.md` — the seven error types used to classify lessons.
- `references/learning-capture.md` — how to write a lesson that generalizes.
- `references/adding-a-language.md` — cold-start a language; add a sandbox image.
