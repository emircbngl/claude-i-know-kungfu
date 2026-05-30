# Benchmark — an honest evaluation

This project is about not faking things, so this file reports what the evaluation
**actually** found — null results where the model needs no help, and a real,
earned delta in the one place it does.

## Methodology

A **blind‑agent evaluation**, scored by the real compiler:

- For each held‑out task, fresh, independent coder agents wrote a solution
  **cold** — only the prompt, no knowledge base, no lookup, no tools.
- **With the verify loop** means `kungfu_verify`: the solution is compiled/tested
  in the Docker sandbox (`--network none`) and, on failure, the agent is given the
  **real compiler error** and revises (one round here).
- Solutions were not written or hinted by the repo author. Everything — cold and
  revised — was scored against hidden tests in the sandbox and **independently
  re‑scored** for this table.

## Results

| evaluation | cold (one‑shot) | with verify loop | delta |
| --- | --- | --- | --- |
| Gleam · Julia · Oberon — basic list/string tasks (n=4 each) | 1.00 | 1.00 | 0 |
| Gleam — a 2024 *removed* API (`result.then` → `result.try`), 5 samples | 1.00 | 1.00 | 0 |
| **Gleam — recursive‑descent expression parser** (precedence + parens), 6 samples | **1.00** (6/6) | — | 0 |
| **Julia — exact factorial** (BigInt; `21!` overflows Int64), 6 samples | **1.00** (6/6) | — | 0 |
| **Oberon — recursive‑descent expression parser** (precedence + parens), 6 samples | **0.17** (1/6) | **0.83** (5/6) | **+0.66** |

## Finding 1 — where the model is already good, the plugin adds nothing

A current, strong model writes correct Gleam, Julia, and Oberon for basic tasks,
uses the *current* API that replaced a removed one (5/5 cold used `result.try`),
and even nails the **hard** tasks one‑shot in two of three languages: a full
expression parser in Gleam (6/6) and exact BigInt factorials in Julia (6/6 — every
agent reached for `big(n)`; they all knew `21!` overflows). Where there is no gap,
this repo reports none.

> An earlier version showed a staged `0.50 → 1.00` "learning curve" (cold solutions
> hand‑picked to fail). It was removed; staging a number is exactly what this
> project exists to prevent.

## Finding 2 — the gap is a *language trap*, not task difficulty — and the verify loop closes it

The most informative result: the **same** hard task — a precedence‑and‑parens
expression parser — is **6/6 cold in Gleam but 1/6 cold in Oberon.**

It isn't about difficulty: both need mutual recursion
(`expr → term → factor → expr`). Gleam lets top‑level functions call each other in
any order, so it's routine. **Oberon‑07 has no forward declarations**, and OBNC
additionally forbids calling a *sibling* nested procedure — a sharp, non‑obvious
constraint. One‑shot, 6 fresh agents:

| approach taken (Oberon) | result | real OBNC verdict |
| --- | --- | --- |
| `FORWARD;` declaration | ❌ | `syntax error … expecting END` (no FORWARD in Oberon‑07) |
| repeat‑heading forward decl | ❌ | `undeclared identifier: Number` |
| flat mutually‑recursive procs | ❌ | `undeclared identifier: Factor` |
| nested proc using enclosing locals | ❌ | `undeclared identifier: pos` |
| **procedure variable** | ✅ | compiles, all asserts pass |
| (one agent) | ⊘ | **honestly refused to guess** without a compiler |

→ **cold pass@1 = 1/6.** Feed each compile failure its real OBNC error once (the
verify loop). All four diagnose the constraint and restructure correctly — a
nested chain, a module‑level procedure with a `VAR` parameter, a procedure
variable. → **with the loop, 5/6 (+0.66)**, driven entirely by execution feedback.

## What it means

- The plugin does **not** make a capable model able to do what it already can —
  it's strong even on hard tasks in niche languages.
- It earns its keep on **idiosyncratic language semantics the model doesn't
  anticipate one‑shot** (Oberon's missing forward declarations). There, the
  compiler‑in‑the‑loop turns a 17% success rate into 83%. That is the regime the
  plugin is for: *"probably right"* → *"verified right,"* and a real fix where the
  model is genuinely wrong.

## Reproduce

Each hard task is a reproducible bench task:

```text
server/bench/gleam/hard/expr_parser      server/bench/julia/hard/bigint_factorial
server/bench/oberon/test/ob_calc
```

```text
docker build -t kungfu-oberon:latest server/sandbox/oberon
/kungfu-bench oberon selfcheck      # reference solutions pass
```

The blind‑agent protocol (fresh agents, cold vs. verify‑fix, scored via
`kungfu_verify`) is driven by the skill; the scoring harness is
`server/kungfu/bench.py`.

## Caveats

Small samples (n = 4–6 per row), one model, one verify‑fix round. Directional,
not a leaderboard. Cold solutions are real blind attempts; verify‑loop revisions
are real agent fixes prompted only by the compiler error; all independently
re‑scored in the sandbox.
