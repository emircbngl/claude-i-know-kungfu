# Demo — Julia

Julia looks superficially like Python but differs in ways that trip up an LLM:
strings concatenate with `*` (not `+`), and arrays are **1-based**. Sandbox:
`julia:1.11`, run `--network none` (the Julia stdlib, incl. `Test`, is bundled).

## Learning curve (held-out test split, n = 4, Docker-verified)

| metric | cold (no KB) | warm (after learning) | delta |
| --- | --- | --- | --- |
| pass@1 | 0.50 | 1.00 | **+0.50** |
| hallucinated-symbol rate | 0.00 | 0.00 | — |

`selfcheck`: 4/4 reference solutions compile and pass their hidden tests offline.

> Note: Julia's failures here are `MethodError` / wrong-result, not "unknown
> identifier", so the hallucinated-symbol heuristic stays 0.00 — honestly. The
> pass@1 jump is the signal.

## The mistakes the runtime caught (real output)

| natural cross-language guess | Julia verdict | correct |
| --- | --- | --- |
| `cat_str(a, b) = a + b` *(Python/JS string `+`)* | `MethodError: no method matching +(::String, ::String)` | `a * b` |
| `second(v) = v[1]` *(0-based thinking)* | returns the **first** element → hidden test fails | `v[2]` (1-based) |

## Learn loop

The string-`+` mistake is captured as a `SEMANTIC` wrong→right lesson (trigger:
*"joining two strings with +"*) and rolled into the Julia skeleton.

## Reproduce

```text
docker build -t kungfu-julia:latest server/sandbox/julia
/kungfu-bench julia selfcheck     # expect 4/4
/kungfu-bench julia cold
/kungfu-bench julia warm
/kungfu-bench julia report
```
