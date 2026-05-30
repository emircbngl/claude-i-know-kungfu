# Benchmark — an honest evaluation

This project is about not faking things, so this file reports what the evaluation
**actually** found: a current model is broadly capable even in niche languages, the
gap is a small *structural* one concentrated in a single language's idiosyncratic
rules, and execution feedback — not trust — closes it.

## Methodology

A **controlled, blind‑agent evaluation**, scored by the real compiler.

- **10 identical tasks × 3 languages × 3 samples = 90 one‑shot solutions.** Every
  task is the *same problem with the same examples* in Gleam, Julia, and
  Oberon‑07 — only the function signature changes. This isolates the one variable
  that matters: the language.
- **Cold:** each solution was written by a fresh, independent agent from its **own
  knowledge only** — no knowledge base, no lookup, no web, no tools.
- **Verify‑fix:** for each cold failure, the **exact compiler diagnostic** was fed
  back to a fresh agent that revised; re‑scored in Docker; repeated up to two
  rounds. **No knowledge base — pure execution feedback.**
- Every solution (cold and revised) was scored against **hidden tests** inside the
  offline Docker sandbox (`--network none`; Gleam v1.15, Julia 1.11, OBNC 0.17.2).
  Solutions were not written or hinted by the author. Full data — all 90 cold
  solutions and every diagnostic — is committed at
  [`server/bench/suite10_eval.json`](server/bench/suite10_eval.json).

The 10 tasks: `total`, `largest`, `count_even`, `gcd_of`, `fib`, `reverse_digits`,
`is_prime`, `digit_sum`, `collatz`, and `eval_expr` — a precedence‑and‑parens
integer expression evaluator (the hard one).

## Result — cold pass rate (passed / 3 samples)

| task | Gleam | Julia | Oberon‑07 |
| --- | --- | --- | --- |
| total | 3/3 | 3/3 | 3/3 |
| largest | 3/3 | 3/3 | 3/3 |
| count_even | 3/3 | 3/3 | 3/3 |
| gcd_of | 3/3 | 3/3 | 3/3 |
| fib | 2/3 | 3/3 | 3/3 |
| reverse_digits | 3/3 | 3/3 | 3/3 |
| is_prime | 3/3 | 3/3 | 2/3 |
| digit_sum | 3/3 | 3/3 | 3/3 |
| collatz | 3/3 | 3/3 | 3/3 |
| **eval_expr** | **3/3** | **3/3** | **0/3** |
| **TOTAL** | **29/30** | **30/30** | **26/30** |

**Cold overall: 85/90 (94%). After the verify‑fix loop: 90/90.**

## Finding 1 — where the model is already good, the plugin adds nothing

85 of 90 one‑shot solutions compiled and passed hidden tests with **no help at
all** — in three languages a current model barely saw in training. Nine of the ten
tasks are essentially solved cold in every language. Where there is no gap, this
repo reports none.

> An earlier version of this file showed a staged `0.50 → 1.00` "learning curve"
> built from hand‑picked failures. It was deleted. Staging a number is exactly what
> this project exists to prevent.

## Finding 2 — the gap is a *language trap*, and it's structural

The five cold failures are not spread out — they concentrate. Four of five are in
Oberon‑07, and **three are the same task: `eval_expr`, which is 3/3 in Gleam, 3/3
in Julia, and 0/3 in Oberon.**

It isn't difficulty — an expression parser needs the same mutual recursion
(`expr → term → factor → expr`) in all three. It's that Oberon‑07 enforces rules a
model pattern‑matching from C/Pascal/Rust doesn't anticipate. Every cold failure
maps to a specific, nameable rule:

| failure | the trap (real compiler diagnostic) | error type | iters to fix |
| --- | --- | --- | --- |
| gleam / fib | used `order.Lt` without `import gleam/order` | IMPORT | 1 |
| oberon / is_prime | `IF p THEN RETURN 1 ELSE RETURN 0 END` — `RETURN` must be the **last** statement of a body | SYNTAX | 1 |
| oberon / eval_expr | a nested procedure can't see the enclosing proc's local `pos` | SEMANTIC | 1 |
| oberon / eval_expr | a nested procedure can't call its **sibling** nested procedure | SEMANTIC | 2 |
| oberon / eval_expr | used Oberon‑2 `PROCEDURE^` forward decl — **removed in Oberon‑07** | NONEXISTENT | 2 |

The fix the agents converge on for the Oberon parser is the genuine Oberon‑07
idiom: **lift state to module level and use a procedure‑typed variable** to break
the recursion cycle (since there are no forward declarations). Feed the real
compiler error back and **every** failure recovers within two rounds — one in the
first round, two more in the second: **85/90 → 90/90**, on execution feedback
alone, with no knowledge base.

> Corroborates an earlier focused run: the *same* parser task, 6 fresh samples
> each — Gleam 6/6, Julia (BigInt factorial) 6/6, Oberon 1/6 cold → 5/6 with the
> verify loop. Same phenomenon, same direction, larger N here.

## These five failures are exactly what the Learn loop captures

Each failure is a textbook **misconception → correct‑model** lesson — e.g.
*"reaching for an early/conditional `RETURN` in Oberon"* → *"`RETURN` is the final
statement of a procedure body; compute into a `VAR` and return once."* Captured
once (keyed by the flawed reasoning), surfaced proactively by `kungfu_lookup`
before the next Oberon task, the trap stops reaching the compiler at all. The
verify‑fix loop pays the cost once; the lesson makes it free thereafter. That is
the entire point of the plugin, measured on real failures.

## Reproduce

```text
server/bench/{gleam,julia,oberon}/suite10/<task>/   # 30 task cells, identical across langs
server/bench/suite10_eval.json                      # full data: matrix, 90 cold solutions, every diagnostic + fix
```

```text
docker build -t kungfu-oberon:latest server/sandbox/oberon   # (gleam / julia similarly)
/kungfu-bench oberon selfcheck                               # reference solutions pass 10/10
```

Re‑scoring any stored solution = `bench.merge_files` the candidate into its task
and call `verify.verify` (see `server/kungfu/bench.py`).

## Caveats

One model, three samples per cell, up to two verify‑fix rounds — directional, not a
leaderboard. Nine of ten tasks are classic algorithms a strong model knows in any
language, so the cold rate is high by design; the **discriminating** task is
`eval_expr` and the discriminating language is Oberon‑07. Every number is from the
real compiler on hidden tests, with all 90 cold solutions committed for inspection.
