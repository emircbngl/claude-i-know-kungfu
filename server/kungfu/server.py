"""FastMCP server: the kungfu toolset.

Thin wrappers over the pure modules. The server is the librarian + verifier +
bench — it never calls an LLM. Tool docstrings are written for Claude: they state
the honesty contract each tool enforces.
"""

from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from . import bench as bench_mod
from . import cards as cards_mod
from . import config as config_mod
from . import learn as learn_mod
from . import store as store_mod
from . import verify as verify_mod
from ._log import get_logger

log = get_logger()
mcp = FastMCP("kungfu")


def _home():
    return config_mod.ensure_home()


@mcp.tool
def kungfu_status(language: Optional[str] = None) -> dict:
    """Orientation. Call this FIRST when about to work in a language.

    Reports what the knowledge base knows, whether the Docker verifier is
    available, lesson counts, and the last benchmark. If ``docker_available`` is
    false, you cannot prove code works — say so honestly instead of claiming it.
    """
    home = _home()
    cfg = config_mod.load_config()
    kdir = home / "knowledge"
    known = sorted(p.name for p in kdir.iterdir() if p.is_dir()) if kdir.exists() else []
    out = {
        "home": str(home),
        "docker_available": verify_mod.docker_available(),
        "languages_known": known,
        "managed_languages": cfg.get("managed_languages", {}),
    }
    if language:
        m = store_mod.manifest(home, language)
        cold = bench_mod.load_run(language, "cold")
        warm = bench_mod.load_run(language, "warm")
        out["language"] = {
            "name": language,
            "managed": config_mod.is_managed(language, cfg),
            "counts": m["counts"],
            "lessons": m["lessons"],
            "has_skeleton": m["has_skeleton"],
            "last_bench": {
                "cold": (cold or {}).get("metrics"),
                "warm": (warm or {}).get("metrics"),
            },
        }
    return out


@mcp.tool
def kungfu_lookup(language: str, query: Optional[str] = None,
                  kind: Optional[str] = None, limit: int = 6) -> dict:
    """Manifest-first retrieval. Call BEFORE writing any code in a managed language.

    Returns the language skeleton (incl. negative knowledge), the lessons whose
    flawed reasoning matches your query, and only the matched cards — never the
    whole language. Read ``note``: if it says there is no grounded knowledge,
    everything you write is a HYPOTHESIS until you fetch real docs or verify it.
    """
    return store_mod.lookup(_home(), language, query=query, kind=kind, limit=limit)


@mcp.tool
def kungfu_save_card(language: str, kind: str, slug: str, body: str,
                     title: str = "", source: str = "", verified: bool = False,
                     verified_against: str = "", confidence: str = "") -> dict:
    """Persist distilled knowledge with provenance. YOU distil; the server stores.

    ``kind`` is one of ``syntax`` / ``stdlib`` / ``library``. Provide a real
    ``source`` (the URL you fetched) so the card is GROUNDED rather than a
    HYPOTHESIS. Set ``verified=True`` only if it actually compiled in the sandbox.
    """
    home = _home()
    card = cards_mod.new_card(
        language, kind, slug, body, title=title, source=source,
        verified=verified, verified_against=verified_against, confidence=confidence,
    )
    path = store_mod.save_card(home, card)
    state = cards_mod.epistemic_state(card)
    note = {
        "VERIFIED": "Verified by execution — highest trust.",
        "GROUNDED": "Backed by a cited source; mark not-yet-run until verified.",
        "HYPOTHESIS": "No source and not verified — this is a GUESS. Fetch a real "
                      "source or verify it before relying on it.",
    }[state]
    return {"saved": str(path), "slug": card.slug, "kind": card.kind,
            "epistemic_state": state, "note": note}


@mcp.tool
def kungfu_verify(language: str, files: dict) -> dict:
    """Compile/type-check/test code in the Docker sandbox. The truth oracle.

    ``files`` maps relative paths to contents and must form whatever the language
    image expects (e.g. a minimal Gleam project: ``gleam.toml`` + ``src/*.gleam``).
    Honesty rule: if ``available`` is false you may NOT claim the code works; tell
    the user it is unverified. If ``ok`` is false, fix it, then record the
    wrong->right with ``kungfu_learn``.
    """
    cfg = config_mod.load_config()
    res = verify_mod.verify(language, files, cfg)
    if not res["available"]:
        res["guidance"] = ("Could not verify. Do NOT claim this code works. Tell the "
                           "user it is UNVERIFIED and why (" + res["reason"] + ").")
    elif not res["ok"]:
        res["guidance"] = ("Verification FAILED. Fix using the diagnostics, then capture "
                           "the wrong->right as a lesson via kungfu_learn.")
    else:
        res["guidance"] = ("VERIFIED — safe to present as working. Consider saving a "
                           "verified snippet via kungfu_save_card(verified=True).")
    return res


@mcp.tool
def kungfu_learn(language: str, misconception: str = "", trigger: str = "",
                 wrong: str = "", right: str = "", model: str = "",
                 source: str = "user-correction", verified: bool = False,
                 verified_against: str = "", error_type: str = "",
                 error_text: str = "") -> dict:
    """Record a mistake as a misconception -> correct-model lesson.

    Capture the *reasoning* error in ``misconception``/``trigger`` (when this
    wrong thought occurs), the bad code in ``wrong``, the fix in ``right``, and
    the structural reason in ``model``. The lesson is keyed by ``trigger`` so it
    surfaces next time that reasoning recurs. Prefer ``source='verify-failure'``
    with ``verified=True`` when the fix actually compiled — that is the strongest
    kind of lesson.
    """
    home = _home()
    cfg = config_mod.load_config()
    thr = int(cfg.get("learn", {}).get("rollup_threshold", 3))
    lesson = {
        "misconception": misconception, "trigger": trigger, "wrong": wrong,
        "right": right, "model": model, "source": source, "verified": verified,
        "verified_against": verified_against, "error_type": error_type,
        "error_text": error_text,
    }
    result = learn_mod.add_lesson(home, language, lesson, rollup_threshold=thr)
    result["note"] = ("Lesson stored; kungfu_lookup will surface it the next time this "
                      "reasoning recurs. Folded into the skeleton if recurring/verified.")
    return result


@mcp.tool
def kungfu_bench(language: str, action: str = "report", split: str = "test",
                 solutions: Optional[dict] = None, label: str = "") -> dict:
    """Measure competence on the held-out suite. Proves the agent actually learns.

    Actions:
    - ``list``: show train/test task ids and their prompts.
    - ``selfcheck``: run the reference solutions (a healthy suite + sandbox passes all).
    - ``score``: verify your ``solutions`` ({task_id: {relative_path: content}}, or
      {task_id: {"files": {...}, "iters": n}}) against hidden tests; pass ``label``
      ('cold' or 'warm') to persist the run.
    - ``report``: render the cold-vs-warm learning curve from saved runs.

    Never fakes numbers: if Docker is down, runs are marked not measurable.
    """
    home = _home()  # ensure home exists for run persistence
    cfg = config_mod.load_config()
    action = (action or "report").lower()

    if action == "list":
        out = {}
        for sp in ("train", "test"):
            out[sp] = [
                {"id": tid, "prompt": bench_mod.load_task(language, sp, tid)["prompt"]}
                for tid in bench_mod.list_tasks(language, sp)
            ]
        return out

    if action == "selfcheck":
        return bench_mod.selfcheck(language, split, cfg)

    if action == "score":
        scored = bench_mod.score(language, split, solutions or {}, cfg)
        if label:
            path = bench_mod.save_run(language, label, scored)
            scored["saved_run"] = str(path)
        return scored

    if action == "report":
        return {
            "markdown": bench_mod.report(language),
            "cold": (bench_mod.load_run(language, "cold") or {}).get("metrics"),
            "warm": (bench_mod.load_run(language, "warm") or {}).get("metrics"),
        }

    return {"error": f"unknown action '{action}'",
            "valid": ["list", "selfcheck", "score", "report"]}


def main() -> None:
    """Entry point used by the plugin's .mcp.json (stdio transport)."""
    log.info("starting kungfu MCP server (home=%s)", config_mod.kungfu_home())
    mcp.run()


if __name__ == "__main__":
    main()
