---
description: Bootstrap a language from zero — fetch real docs, distil a skeleton, verify seeds.
argument-hint: [language]
---

Read the `i-know-kungfu` skill and `references/adding-a-language.md`, then run the cold-start flow for the language in: $ARGUMENTS.

1. `kungfu_status(language)` — is it managed? is Docker up?
2. Fetch the official tour/reference and stdlib index (WebFetch/WebSearch; Context7 for libraries). Prefer primary sources.
3. Distil and save the skeleton with `kungfu_save_card(language, kind="skeleton", body=…, source=…)`: a `## Core structural rules` section AND a `## Does NOT exist (negative knowledge)` section (features it lacks that neighbouring languages have).
4. Write a few tiny seed snippets and `kungfu_verify` them; save the ones that compile as cards with `verified=true`.

Cite every source. Never invent syntax — if you cannot fetch it, leave it out and say so.
