# Epistemic states

Every symbol/claim you use while writing target-language code has exactly one state.
Behavior is gated by state — this is the spine of the whole plugin, not a label.

| State | Means | May ship as "done"? |
| --- | --- | --- |
| **VERIFIED** | Compiled/ran in the Docker sandbox | Yes — highest trust |
| **GROUNDED** | Backed by a cited source you fetched | Yes, but mark not-yet-run |
| **HYPOTHESIS** | A guess (pattern-matched from another language) | **No** — promote or disclose |
| **KNOWN-WRONG** | Matches a stored lesson's misconception | **No** — apply the correction |

## The single rule

**No HYPOTHESIS survives to completion.** Promote it:

- HYPOTHESIS → GROUNDED: fetch a real source, save it with `kungfu_save_card(source=…)`.
- HYPOTHESIS → VERIFIED: compile/test it with `kungfu_verify`.
- If you cannot do either, tell the user it is unverified and why. Do not present it
  as working.

## KNOWN-WRONG

`kungfu_lookup` surfaces lessons whose `trigger` matches what you are about to do.
If your intended approach matches a lesson's misconception, you are about to repeat a
KNOWN-WRONG move — use the lesson's `right`/`model` instead.

## How to talk about it

When you finish, be explicit, e.g.: "`list.reverse` and `list.map` are VERIFIED
(compiled in the sandbox); the `gleam/json` usage is GROUNDED (from the official
docs, not run); I have no basis for anything else." That sentence is the product.
