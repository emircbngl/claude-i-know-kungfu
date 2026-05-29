# Retrieval discipline

## Manifest-first

Always `kungfu_lookup` before writing. It returns the cheap manifest, the skeleton
(incl. negative knowledge), the matched lessons, and only the matched cards — never
the whole language. Read the `note` field: a "no grounded knowledge" note means
**stop and fetch** before asserting anything.

## When to fetch

Fetch the moment you are unsure whether a function/type/syntax exists or what its
shape is. Being unsure is not a problem; *guessing instead of fetching* is.

- **Libraries:** Context7 — `resolve-library-id` then `get-library-docs`. This gives
  version-accurate docs and is preferred for the library long tail.
- **Syntax / language core / stdlib:** `WebFetch` the official tour/reference;
  `WebSearch` to find it. Prefer primary sources (official docs, the language's own
  repo) over blog posts.

Do **not** pre-index "all libraries" — it is infeasible and itself a fabrication
risk. Fetch lazily, on demand.

## Distil, then persist with provenance

You (Claude) distil raw docs into a small card; the server stores it. Persist with:

```
kungfu_save_card(language, kind="syntax|stdlib|library", slug, body,
                 source="<the URL you read>", verified=false)
```

- A card **with** a `source` is GROUNDED. A card **without** one is a HYPOTHESIS —
  do not save guesses as if they were facts.
- Set `verified=true` only after the snippet actually compiled in the sandbox.
- Pin library cards to a version in the slug (e.g. `gleam_json@1.0`).

## Negative knowledge

Record what does **not** exist as deliberately as what does. When you confirm (from
docs or a compiler error) that a feature is absent, add it to the skeleton's
"Does NOT exist" section via `kungfu_save_card(kind="skeleton", …)`. Negative facts
are the cheapest, highest-leverage defense against hallucination.
