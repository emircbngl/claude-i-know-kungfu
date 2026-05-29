---
description: Show what the kungfu knowledge base knows and whether the verifier is available.
argument-hint: [language]
---

Read the `i-know-kungfu` skill. Call the `kungfu_status` MCP tool (pass `language` = $ARGUMENTS if provided).

Report concisely: whether Docker (the verifier) is available, which languages are known, and — for the given language — its skeleton/lessons/card counts and last benchmark (cold vs warm). If Docker is unavailable, state plainly that code cannot be verified right now.
