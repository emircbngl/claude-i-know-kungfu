# Demo — Oberon

Oberon (Niklaus Wirth's Oberon-07) is genuinely niche: it has no official Docker
image, so the sandbox **builds the OBNC compiler from source** (Karl Landström's
Oberon-07 compiler, https://miasap.se/obnc/, v0.17.2). OBNC compiles Oberon to C;
the test oracle is Oberon's built-in `ASSERT`, which traps (non-zero exit) on
failure. Run `--network none`.

## Learning curve (held-out test split, n = 4, Docker-verified)

| metric | cold (no KB) | warm (after learning) | delta |
| --- | --- | --- | --- |
| pass@1 | 0.50 | 1.00 | **+0.50** |
| hallucinated-symbol rate | 0.25 | 0.00 | **−0.25** |

`selfcheck`: 4/4 reference solutions compile and their `ASSERT`s hold offline.

## The mistakes the compiler caught (real output)

| natural cross-language guess | OBNC verdict | correct |
| --- | --- | --- |
| `RETURN n / 2` *(C/Python integer `/`)* | `error: incompatible types in operation "/": INTEGER, INTEGER` | `n DIV 2` |
| `RETURN LENGTH(a)` *(a `length()` builtin)* | `error: undeclared identifier: LENGTH` | `LEN(a)` |

In Oberon-07, `/` is **real** division; integer division is `DIV` (with `MOD`),
and array length is the builtin `LEN` — there is no `LENGTH`.

## Learn loop

Both are captured as one `SEMANTIC` wrong→right lesson (trigger: *"integer
division or array length in Oberon"*) and rolled into the Oberon skeleton.

## Reproduce

```text
docker build -t kungfu-oberon:latest server/sandbox/oberon   # builds OBNC from source
/kungfu-bench oberon selfcheck     # expect 4/4
/kungfu-bench oberon cold
/kungfu-bench oberon warm
/kungfu-bench oberon report
```
