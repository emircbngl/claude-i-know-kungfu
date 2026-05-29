# Adding / cold-starting a language

## Cold-start (from zero) — the `/kungfu-teach` flow

1. `kungfu_status(language)` — confirm it is managed and whether Docker is up.
2. **Fetch the real reference.** WebFetch the official tour/getting-started and the
   stdlib index; Context7 for any libraries. Prefer primary sources.
3. **Distil a skeleton.** Write `kungfu_save_card(language, kind="skeleton", body=…,
   source=…)` containing:
   - `## Core structural rules` — the handful of rules that define the language
     (e.g. expression-oriented, immutable by default, typed, error handling via
     `Result`).
   - `## Does NOT exist (negative knowledge)` — features it lacks that neighbours
     have (no `null`, no exceptions, no `class`). This is the anti-hallucination core.
4. **Verify seeds.** Write a few tiny snippets covering the core rules and
   `kungfu_verify` them. Save the ones that compile as cards with `verified=true`.
5. Cite every source. If you cannot fetch something, leave it out — never invent.

## Add a verification sandbox (so the language can be verified)

Create `server/sandbox/<lang>/` with a `Dockerfile` + `verify.sh` honoring the
contract (see `server/sandbox/README.md`):

- source mounted read-only at `/src`; copy to a writable workdir; build/type-check/
  test; exit non-zero on failure; run as non-root.
- Warm the dependency cache at build time so verification works with `--network none`.

Then add the language and its file extensions to `managed_languages` in
`~/.kungfu/config.json`. `kungfu_verify` builds the image lazily on first use.

## Add a benchmark suite (so learning can be measured)

Add tasks under `server/bench/<lang>/{train,test}/<id>/` with `prompt.md`, scaffold
files, `ref/` (reference solution), and `hidden/` (tests). Keep train and test
disjoint. `kungfu_bench` action `selfcheck` confirms the suite + sandbox are healthy.
