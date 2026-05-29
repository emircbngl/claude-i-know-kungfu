# Verification loop

The Docker sandbox is the one oracle that cannot be faked. Use it.

## Build the files dict

`kungfu_verify(language, files)` takes `{relative_path: content}` that forms whatever
the language image expects:

- **Gleam:** a minimal project — `gleam.toml` plus `src/<module>.gleam`. Add
  `test/<module>_test.gleam` (gleeunit) to run tests, not just build.
- **Python:** one or more `*.py`; add `test_*.py` to run pytest, otherwise it is a
  byte-compile check.

## Read the result honestly

```
available=false  → you CANNOT verify. Tell the user it is UNVERIFIED and why.
                   Do not claim it works. (e.g. Docker not running.)
ok=false         → it failed. Read `diagnostics` and `unknown_symbols`, fix, re-verify.
ok=true          → VERIFIED. Safe to present as working.
```

`unknown_symbols` lists identifiers the compiler did not recognize — these are
exactly your hallucinations. Each one is a lesson waiting to be captured.

## The fix→learn cycle

On a failure you fix, immediately call `kungfu_learn` (see
`references/learning-capture.md`) with `source="verify-failure"` and, once the fix
compiles, `verified=true`. A verified wrong→right pair is the strongest lesson.

## Verify small and often

Verify in small increments rather than writing a large blob and verifying once.
Smaller diffs give sharper diagnostics and cleaner lessons.
