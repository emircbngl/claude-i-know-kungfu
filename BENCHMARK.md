# Benchmark — an honest evaluation

This project is about not faking things, so this file reports what the evaluation
**actually** found — including a null result — rather than a flattering curve.

## Methodology

A **blind‑agent grounding ablation**, scored by the real compiler:

- For each held‑out task, two fresh, independent coder agents wrote a solution:
  - **cold** — only the task prompt; no knowledge base, no lookup, no tools.
  - **warm** — the task prompt plus a concise, doc‑grounded reference card for the
    language (the kind of grounding `kungfu_lookup` would provide). General
    reference only — never the task's solution.
- Neither condition was coached: the author of this repo did not write or hint the
  solutions. Every solution was compiled/tested in the Docker sandbox
  (`--network none`) against hidden tests.
- A "teacher" agent produced each reference card from the official docs (with
  citations), so even the grounding was agent‑derived, not hand‑authored.

## Results

| evaluation | cold pass@1 | warm pass@1 | delta |
| --- | --- | --- | --- |
| Gleam — basic list tasks (map, length, fold product/max), n=4 | 1.00 | 1.00 | 0 |
| Julia — basic tasks (concat, index, max, length), n=4 | 1.00 | 1.00 | 0 |
| Oberon — basic tasks (DIV, LEN, mul, add), n=4 | 1.00 | 1.00 | 0 |
| Gleam **hard** — a 2024 *removed* API (`result.then` → `result.try`), 5 cold samples | 1.00 (5/5) | 1.00 | 0 |

`selfcheck`: across all three languages the reference solutions compile and pass
their hidden tests 4/4 offline — the sandboxes and harness are sound.

## The finding (honest)

**A current, strong model already writes correct code in all three languages —
Gleam, Julia, and even niche Oberon‑07 — and it knows their *current* APIs**
(every one of 5 cold agents used `result.try`, not the removed `result.then`).
On the tasks tried there is **no pass@1 gap between cold and warm**, so this repo
reports none.

An earlier version showed a `0.50 → 1.00` curve. That was **staged** — the
"cold" solutions were hand‑picked to fail (2 of 4 wrong, then fixed). The
compiler verdicts in it were real, but the *delta* was an artifact of
construction. It has been removed; staging a number is precisely what this
project exists to prevent.

## What this means for the plugin's value

The value is **not** capability uplift on tasks the model can already do (it can).
It is:

1. **Verification, not trust** — the sandbox converts *"probably right"* into
   *"verified right."* On these tasks the model was right; you only *know* that
   because it was compiled and tested.
2. **Honesty** — nothing ungrounded or unrun is presented as done.
3. **Catching the real misses** — fabrication still happens on genuinely
   out‑of‑distribution surface (post‑cutoff library versions, proprietary or very
   obscure APIs). That is the regime the plugin is for.

## What would demonstrate an uplift (future work, not claimed)

Tasks whose correct answer is genuinely outside the model's training: a library
released after the model's cutoff, a proprietary/internal API, or a brand‑new
language version with breaking changes. Verifying those generally needs network
access for dependencies (`docker.network: "bridge"`), so they fall outside this
offline, self‑contained suite. Until such an eval is run, no capability‑uplift
number is claimed.

## Reproduce

```text
docker build -t kungfu-gleam:latest server/sandbox/gleam
/kungfu-bench gleam selfcheck     # reference solutions: expect 4/4
```

The blind‑agent ablation is an agent protocol (fresh coder agents, cold vs warm,
scored via `kungfu_verify`); the scoring harness lives in `server/kungfu/bench.py`.
