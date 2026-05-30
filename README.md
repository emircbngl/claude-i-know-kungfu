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

The honest part. I ran a **blind‑agent evaluation**: fresh agents solved held‑out tasks with no help (**cold**) vs. with a doc‑grounded reference card (**warm**); every solution was scored by the real compiler in the sandbox. I did not hand‑write or coach the solutions.

| eval | cold pass@1 | warm pass@1 | delta |
| --- | --- | --- | --- |
| Gleam · Julia · Oberon (basic list/string tasks) | 1.00 | 1.00 | **0** |
| Gleam **hard** — a 2024 *removed* API (`result.then` → `result.try`) | 1.00 (5/5) | 1.00 | **0** |

**The honest finding: a current, strong model already writes correct code in all three languages — even using the up‑to‑date API that replaced a removed one.** There is no pass@1 gap to show, so this repo shows none. (An earlier version of this README displayed a `0.50 → 1.00` "learning curve"; that was a *staged* demonstration with hand‑picked failures, so it was removed — staging a number is exactly what this project exists to prevent.)

So the plugin's value is **not** "the model can't, and we make it" — it demonstrably can. The value is the **guarantee**: it converts *"probably right"* into *"verified right,"* refuses to present anything it did not ground or run, and catches the cases — genuinely out‑of‑distribution APIs, post‑cutoff versions — where the model *is* wrong. Demonstrating a capability gap would require tasks truly outside the model's training; that is future work, and **not claimed here**.

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

Builds on established ideas — retrieval‑augmented generation (RAG), self‑repair / self‑debugging loops, reflexion‑style memory, and Context7 documentation retrieval. What's distinctive is the *integration into one epistemically‑honest agent*: lessons grounded in **verified execution** and keyed by the **misconception** (not a string), an explicit **epistemic‑state gate** that blocks ungrounded output, **negative knowledge** as a first‑class anti‑hallucination tool, and a benchmark that **reports null results instead of staging wins**. "Self‑training" means a growing external knowledge base — **not** changes to model weights.

## Status & limitations

- **Verification works end‑to‑end on a Docker host.** Sandboxes for **Gleam, Julia, and Oberon** (the last builds the OBNC compiler from source) build and self‑check 4/4 offline (`--network none`).
- Pure logic (knowledge store, learn engine, verifier control flow, benchmark harness) is covered by a unit‑test suite: `uv run --extra dev pytest` → **38 passing**. The codebase also passed a max‑effort multi‑agent self‑review (14 findings fixed).
- **Honesty holds in the failure path:** with Docker stopped, `kungfu_verify` returns a structured "cannot verify" and the bench marks runs not measurable — it never fakes a pass or invents numbers.
- **No capability‑uplift claim.** A real blind‑agent eval found no pass@1 gap for a current model on the tasks tried (see above) — the plugin's value is verification & honesty, not making the model able to do what it already can. Showing an uplift would require genuinely out‑of‑distribution APIs; that is future work.

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
