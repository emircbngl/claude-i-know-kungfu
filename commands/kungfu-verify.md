---
description: Compile/test the current target-language code in the Docker sandbox.
argument-hint: [language] [path-or-files]
---

Read the `i-know-kungfu` skill and `references/verification-loop.md`.

Determine the language and the files to verify from: $ARGUMENTS (and the current working context). Assemble the `{relative_path: content}` map the language image expects (e.g. Gleam: `gleam.toml` + `src/*.gleam`, plus `test/*` to run tests) and call `kungfu_verify(language, files)`.

Then act on the result honestly:
- `available=false` → tell the user the code is UNVERIFIED and why; do not claim it works.
- `ok=false` → read `diagnostics`/`unknown_symbols`, fix, re-verify, and capture the wrong→right via `kungfu_learn`.
- `ok=true` → report it as VERIFIED.
