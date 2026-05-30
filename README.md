<p align="center">
  <img src="assets/banner.svg" alt="I Know KungFu — a Claude Code plugin that grounds and verifies code instead of trusting the model's memory" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-00ff41.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/MCP-FastMCP-1f6feb.svg" alt="Model Context Protocol server">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2.svg" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/tests-38%20passing-2ea043.svg" alt="38 tests passing">
  <img src="https://img.shields.io/badge/verified-Docker%20sandbox-2496ED.svg?logo=docker&logoColor=white" alt="Verified in a Docker sandbox">
</p>

> *"I know kung fu."* — *"Show me."*

**I Know KungFu** is a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin that makes Claude **prove its code instead of trusting its memory** — and **never pretend** to know. When Claude writes a language or API it is unsure of, the plugin grounds every symbol in real documentation, compiles/tests it in a Docker sandbox, and turns each genuine mistake into a lesson it recalls next time. It is an **anti‑hallucination / verification layer** for LLM code generation.

It ships an **MCP server**, a self‑improving per‑language **knowledge base**, an **honesty gate** (hooks), and a **benchmark harness** with an honestly‑reported evaluation (see [below](#what-a-real-evaluation-actually-showed) and [BENCHMARK.md](BENCHMARK.md)).

---

## What if I told you…

…that when you ask an LLM for code in territory it never really learned — a niche language, a post‑training‑cutoff API, an obscure library — its failure mode is **confident fabrication**: plausible‑but‑nonexistent syntax invented from languages it *does* know. Telling a model "don't make things up" barely helps. Only two things reliably stop fabrication:

- **Grounding** — back every claim with a real, cited source.
- **Execution** — run the compiler; it is the one oracle that cannot be faked.

This plugin is built entirely around those two forces.

## The idea: epistemic honesty

> *"There is no spoon."* — and there is no faking it.

Every symbol Claude writes carries an **epistemic state**, and behavior is gated by it:

| State | Means | May ship as "done"? |
| --- | --- | --- |
| **VERIFIED** | Compiled / ran in the sandbox | ✅ highest trust |
| **GROUNDED** | Backed by a cited source it fetched | ✅ but marked not‑yet‑run |
| **HYPOTHESIS** | A guess pattern‑matched from another language | ❌ promote or disclose |

**The one rule: no HYPOTHESIS survives to completion.** It is promoted to GROUNDED (fetch real docs) or VERIFIED (compile it), or the user is told plainly that it is unverified and why. That sentence — *"these symbols are verified, these are grounded, I have no basis for anything else"* — is the product.

## How it works — four loops

```mermaid
flowchart LR
    A[Task in an<br/>unfamiliar language] --> S["kungfu_status"]
    S --> L["kungfu_lookup<br/>skeleton + lessons"]
    L --> W[Write code]
    W --> V["kungfu_verify<br/>Docker truth oracle"]
    V -- fail --> F["fix + kungfu_learn<br/>misconception → correct model"]
    F --> V
    V -- pass --> D["Done — every symbol<br/>VERIFIED or GROUNDED"]
    L -. gap .-> FE["Context7 / WebFetch"] -. distil .-> SC["kungfu_save_card<br/>(with provenance)"] -.-> L
```

| Loop | What it does |
| --- | --- |
| **Retrieve** | Fetch real syntax/library docs (Context7 + WebFetch), shard per language under `~/.kungfu`, load only what's needed. Records **negative knowledge** — what does *not* exist. |
| **Verify** | Compile / type‑check / test generated code in a locked Docker sandbox. If Docker is down, it says so — it never fakes a pass. |
| **Learn** | Turn each mistake into a **misconception → correct‑model** lesson, keyed by the flawed reasoning so it is recalled the next time that reasoning recurs. Recurring lessons roll up into a structural **skeleton** of the language. |
| **Measure** | A blind‑agent benchmark harness that scores solutions in the sandbox and reports **honest numbers — including null results.** No staged curves. |

> *"I can only show you the door. You're the one that has to walk through it."*

The MCP server is the **librarian**, not the brain: it stores, retrieves, verifies, and benchmarks, and it **never calls an LLM**. All judgment — what to fetch, how to distil, what to write — stays with Claude.

## What a real evaluation actually showed

> *"Welcome to the real world."*

The honest part. I ran a **blind‑agent evaluation**: fresh agents solved held‑out tasks **cold** (one‑shot, no help) vs. **with the plugin** (grounding and, where the cold attempt failed, one round of its `kungfu_verify` compile‑and‑fix loop). Every solution was scored by the real compiler in the sandbox; I did not hand‑write or coach them.

| evaluation | cold (one‑shot, no help) | with the plugin's verify loop | delta |
| --- | --- | --- | --- |
| Gleam · Julia · Oberon — basic list/string tasks | 1.00 | 1.00 | **0** |
| Gleam — a 2024 *removed* API (`result.then` → `result.try`), 5 samples | 1.00 | 1.00 | **0** |
| Gleam — recursive‑descent expression parser (precedence + parens), 6 samples | **1.00** (6/6) | — | **0** |
| Julia — exact factorial (BigInt; `21!` overflows Int64), 6 samples | **1.00** (6/6) | — | **0** |
| **Oberon — the *same* parser task** (precedence + parens), 6 samples | **0.17** (1/6) | **0.83** (5/6) | **+0.66** ✅ |

**Two honest findings:**

1. **On tasks the model already knows, the plugin adds no pass@1 — and this repo says so** rather than staging a win. A current model writes correct Gleam/Julia/Oberon for basic tasks, uses the *current* API that replaced a removed one, and even nails the **hard** tasks one‑shot in two of three languages — a full expression parser in Gleam (6/6) and exact BigInt factorials in Julia (6/6). (An earlier README showed a `0.50 → 1.00` "learning curve"; it was *staged* with hand‑picked failures and was removed — faking a number is exactly what this project opposes.)

2. **The gap is a *language trap*, not difficulty — and the verify loop closes it.** The *same* hard task — a precedence‑and‑parens expression parser — is **6/6 cold in Gleam but 1/6 cold in Oberon.** Both need mutual recursion; Gleam allows it across top‑level functions, but **Oberon‑07 has no forward declarations** (and OBNC forbids calling a *sibling* nested procedure). One‑shot, 4 of 6 fresh agents failed to compile (reaching for `FORWARD` or flat mutual recursion); one honestly *refused to guess*; only one compiled. Feed each failure its **real compiler error once** — `kungfu_verify` — and all four diagnose the constraint and restructure correctly: **1/6 → 5/6**. Every number is from the real compiler, independently re‑scored; tasks are reproducible under `server/bench/*/hard` and `server/bench/oberon/test/ob_calc`.

That second row is the whole thesis in one line: **the plugin earns its keep exactly where the model struggles — and it's execution feedback, not trust, that fixes it.**

## Install

Prerequisites: **Python 3.11+**, [**uv**](https://docs.astral.sh/uv/), and **Docker** (for verification; the plugin degrades honestly without it).

```text
/plugin marketplace add emircbngl/claude-i-know-kungfu
/plugin install i-know-kungfu@i-know-kungfu-marketplace
```

The MCP server starts automatically via `.mcp.json` (`uv` resolves dependencies on first run). The knowledge base bootstraps itself at `~/.kungfu` on first use.

## Quickstart

```text
/kungfu-status gleam              # what's known? is the verifier up?
/kungfu-teach gleam               # cold-start: fetch docs, distil a skeleton, verify seeds
"write a Gleam function that …"   # the skill drives: lookup → write → verify → learn
/kungfu-verify gleam <files>      # compile/test it in the sandbox — the truth oracle
/kungfu-bench gleam selfcheck     # sanity-check the suite + sandbox
```

### MCP tools

`kungfu_status` · `kungfu_lookup` · `kungfu_save_card` · `kungfu_verify` · `kungfu_learn` · `kungfu_bench`

## Knowledge base layout (`~/.kungfu`, personal, never committed)

```text
knowledge/<lang>/
  _index.md            # manifest (a view, recomputed from files)
  skeleton.md          # structural model + negative knowledge + learned rules
  syntax/<topic>.md    stdlib/<module>.md    libraries/<lib>@<ver>.md
  lessons.jsonl        # data: misconception → correct-model lessons
  lessons.md           # human-readable view of the above
```

Files are the source of truth; every `.md` index is a regenerated view. Retrieval is manifest‑first — it never loads a whole language. All writes are atomic (temp + `os.replace`).

## Design notes (honest about prior art)

Builds on established ideas — retrieval‑augmented generation (RAG), self‑repair / self‑debugging loops, reflexion‑style memory, and Context7 documentation retrieval. What's distinctive is the *integration into one epistemically‑honest agent*: lessons grounded in **verified execution** and keyed by the **misconception** (not a string), an explicit **epistemic‑state gate** that blocks ungrounded output, **negative knowledge** as a first‑class anti‑hallucination tool, and a benchmark that **reports honest numbers — null where the model needs no help, a real delta where it does — instead of staging wins**. "Self‑training" means a growing external knowledge base — **not** changes to model weights.

## Status & limitations

- **Verification works end‑to‑end on a Docker host.** Sandboxes for **Gleam, Julia, and Oberon** (the last builds the OBNC compiler from source) build and self‑check offline (`--network none`).
- Pure logic (knowledge store, learn engine, verifier control flow, benchmark harness) is covered by a unit‑test suite: `uv run --extra dev pytest` → **38 passing**. The codebase also passed a max‑effort multi‑agent self‑review (14 findings fixed).
- **Honesty holds in the failure path:** with Docker stopped, `kungfu_verify` returns a structured "cannot verify" and the bench marks runs not measurable — it never fakes a pass or invents numbers.
- **Where the plugin helps — measured, not asserted.** On tasks the model already knows, no pass@1 uplift (and the repo says so). On a genuinely hard task — an Oberon‑07 recursive‑descent parser that hits the no‑forward‑declarations trap — the gap is real and the verify‑fix loop closes it: one‑shot **1/6 → 5/6** with the loop. The value is verification + honesty + closing that gap, not making the model able to do what it already can.

## Repository layout

```text
.claude-plugin/    plugin.json, marketplace.json
.mcp.json          wires the kungfu MCP server
hooks/             honesty-gate hooks + gate.py
skills/            i-know-kungfu/SKILL.md + references/
commands/          /kungfu-* commands
server/            FastMCP server (kungfu/), Docker sandboxes, bench suite, tests
assets/            banner
```

## Keywords

Claude Code plugin · MCP server · anti‑hallucination · LLM code generation · grounding · retrieval‑augmented generation · Docker sandbox verification · code verification · epistemic honesty · learn from mistakes · FastMCP · Anthropic Claude.

## Star history

<a href="https://star-history.com/#emircbngl/claude-i-know-kungfu&Date">
  <img src="https://api.star-history.com/svg?repos=emircbngl/claude-i-know-kungfu&type=Date" alt="Star history chart for emircbngl/claude-i-know-kungfu" width="640">
</a>

## License

MIT © 2026 [emircbngl](https://github.com/emircbngl)

> *"Free your mind."*
