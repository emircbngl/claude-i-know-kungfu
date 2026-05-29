---
description: Retrieve grounded knowledge + lessons for a language before writing code.
argument-hint: [language] [topic]
---

Read the `i-know-kungfu` skill and `references/retrieval-discipline.md`.

Parse a language and optional topic from: $ARGUMENTS. Call `kungfu_lookup(language, query=topic)`. Summarize the skeleton (including its "Does NOT exist" negative knowledge), the matched lessons (wrong→right), and the matched cards with their epistemic state.

If the `note` says there is no grounded knowledge for this language, do NOT assert APIs from memory — fetch real docs first (Context7 for libraries, WebFetch for syntax), or run `/kungfu-teach`.
