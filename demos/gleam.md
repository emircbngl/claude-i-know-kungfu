# Demo — Gleam

Gleam is a young, statically-typed language on the BEAM (Erlang VM). It is exactly
the case where an LLM pattern-matches from other functional languages and invents
APIs that don't exist. Sandbox: `ghcr.io/gleam-lang/gleam:v1.15.0-erlang-alpine`,
run `--network none`.

## Learning curve (held-out test split, n = 4, Docker-verified)

| metric | cold (no KB) | warm (after learning) | delta |
| --- | --- | --- | --- |
| pass@1 | 0.50 | 1.00 | **+0.50** |
| hallucinated-symbol rate | 0.25 | 0.00 | **−0.25** |

`selfcheck`: 4/4 reference solutions compile and pass their hidden tests offline.

## The mistakes the compiler caught (real output)

| natural cross-language guess | Gleam verdict | correct |
| --- | --- | --- |
| `list.fold_left(items, acc, fn)` *(OCaml/Elm)* | `error: Unknown module value` — *the module `gleam/list` does not have a `fold_left` value* | `list.fold(items, acc, fn)` |
| `list.reduce(items, acc, fn)` *(JS/Python)* | `error: Incorrect arity` | `list.fold(items, acc, fn)` |

## Learn loop

The fold mistake is captured as a `SEMANTIC` wrong→right lesson, keyed by the
trigger *"folding a list to a single value"*, and rolled into the Gleam skeleton —
so the next fold task recalls `list.fold` **before** writing.

## Reproduce

```text
docker build -t kungfu-gleam:latest server/sandbox/gleam
/kungfu-bench gleam selfcheck     # expect 4/4
/kungfu-bench gleam cold
/kungfu-bench gleam warm
/kungfu-bench gleam report
```
