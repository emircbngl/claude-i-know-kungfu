"""The measure loop: quantify competence and prove learning.

The server cannot generate solutions (it never calls an LLM), so the benchmark
splits cleanly:

* **Server side (here):** given candidate solutions, merge each with its hidden
  tests, run them through the verifier, and compute metrics. Also ``selfcheck``
  the reference solutions to confirm the suite + sandbox are healthy.
* **Agent protocol (driven by the skill/command):** Claude writes solutions for
  the ``test`` split twice — ``cold`` (empty KB) and ``warm`` (after learning
  from the ``train`` split) — and this module scores both into a learning curve.

Train/test are separate dirs so the agent never learns from what it is graded on.

Task layout (``bench/<lang>/<split>/<id>/``)::

    prompt.md              # the instruction given to the agent
    <scaffold files>       # optional project files at the task root; for Gleam the
                           # sandbox supplies gleam.toml, so tasks ship none
    ref/src/<id>.gleam     # reference solution (used by selfcheck)
    hidden/test/<id>_test.gleam   # hidden tests, always merged in

A candidate solution is a ``{relative_path: content}`` mapping (e.g.
``{"src/list_reverse.gleam": "..."}``); it is merged as
``{**scaffold, **candidate, **hidden}`` and verified.
"""

from __future__ import annotations

import statistics
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import _io
from . import config as config_mod
from . import verify as verify_mod

BENCH_DIR = Path(__file__).resolve().parent.parent / "bench"


def bench_root(language: str, bench_dir: Optional[Path] = None) -> Path:
    return (bench_dir or BENCH_DIR) / language.strip().lower()


def _read_tree(base: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not base.exists():
        return out
    for f in sorted(base.rglob("*")):
        if f.is_file():
            out[str(f.relative_to(base))] = f.read_text(encoding="utf-8")
    return out


def list_tasks(language: str, split: str, bench_dir: Optional[Path] = None) -> list[str]:
    d = bench_root(language, bench_dir) / split
    if not d.exists():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir())


def load_task(language: str, split: str, task_id: str,
              bench_dir: Optional[Path] = None) -> dict:
    d = bench_root(language, bench_dir) / split / task_id
    prompt = (d / "prompt.md").read_text(encoding="utf-8") if (d / "prompt.md").exists() else ""
    scaffold = {
        f.name: f.read_text(encoding="utf-8")
        for f in d.iterdir()
        if f.is_file() and f.name not in ("prompt.md", "task.json")
    }
    return {
        "id": task_id,
        "language": language,
        "split": split,
        "prompt": prompt,
        "scaffold": scaffold,
        "ref": _read_tree(d / "ref"),
        "hidden": _read_tree(d / "hidden"),
    }


def merge_files(task: dict, candidate: dict[str, str]) -> dict[str, str]:
    """Hidden tests win last so a candidate can never overwrite its own grader."""
    return {**task["scaffold"], **candidate, **task["hidden"]}


def _candidate(sol) -> tuple[dict, int]:
    if isinstance(sol, dict) and isinstance(sol.get("files"), dict):
        return sol["files"], int(sol.get("iters", 1))
    return (sol or {}), 1


def metrics(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {"n": 0, "available": 0, "measurable": False}
    available = sum(1 for r in results if r.get("available", True))
    passed = sum(1 for r in results if r.get("ok"))
    hallu_tasks = sum(1 for r in results if r.get("unknown_symbols"))
    total_unknown = sum(len(r.get("unknown_symbols", [])) for r in results)
    iters = [int(r.get("iters", 1)) for r in results]
    return {
        "n": n,
        "available": available,
        "measurable": available == n,
        "passed": passed,
        "pass_rate": round(passed / n, 3),
        "hallucinated_symbol_rate": round(hallu_tasks / n, 3),
        "total_unknown_symbols": total_unknown,
        "mean_self_correction_iters": round(statistics.mean(iters), 2),
    }


def score(language: str, split: str, solutions: dict, cfg: Optional[dict] = None,
          bench_dir: Optional[Path] = None, sandbox_dir: Optional[Path] = None) -> dict:
    """Verify each candidate against its hidden tests and compute metrics."""
    results: list[dict] = []
    for tid in list_tasks(language, split, bench_dir):
        task = load_task(language, split, tid, bench_dir)
        if tid not in (solutions or {}):
            results.append({"task": tid, "ok": False, "available": True,
                            "unknown_symbols": [], "reason": "no candidate provided",
                            "iters": 1})
            continue
        files, iters = _candidate(solutions[tid])
        v = verify_mod.verify(language, merge_files(task, files), cfg, sandbox_dir)
        results.append({
            "task": tid, "ok": v["ok"], "available": v["available"],
            "unknown_symbols": v["unknown_symbols"],
            "reason": v["reason"], "iters": iters,
        })
    return {"language": language, "split": split,
            "results": results, "metrics": metrics(results)}


def selfcheck(language: str, split: str = "test", cfg: Optional[dict] = None,
              bench_dir: Optional[Path] = None, sandbox_dir: Optional[Path] = None) -> dict:
    """Run the reference solutions: a healthy suite + sandbox passes them all."""
    solutions = {tid: load_task(language, split, tid, bench_dir)["ref"]
                 for tid in list_tasks(language, split, bench_dir)}
    out = score(language, split, solutions, cfg, bench_dir, sandbox_dir)
    out["selfcheck_ok"] = bool(out["metrics"].get("measurable")) and \
        out["metrics"].get("pass_rate") == 1.0
    return out


# ---- run persistence + report ------------------------------------------------

def runs_dir(language: str, bench_dir: Optional[Path] = None) -> Path:
    # Runs are per-user state, not package data — default under ~/.kungfu so the
    # installed plugin dir is never mutated and projects don't clobber each other.
    base = Path(bench_dir) if bench_dir is not None else (config_mod.kungfu_home() / "bench")
    d = base / language.strip().lower() / "_runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_run(language: str, label: str, scored: dict,
             bench_dir: Optional[Path] = None, at: Optional[str] = None) -> Path:
    p = runs_dir(language, bench_dir) / f"{label}.json"
    payload = {"label": label, "language": language,
               "at": at or datetime.now().isoformat(timespec="seconds"),
               "metrics": scored.get("metrics", {}), "results": scored.get("results", [])}
    return _io.write_json_atomic(p, payload)


def load_run(language: str, label: str, bench_dir: Optional[Path] = None) -> Optional[dict]:
    return _io.read_json(runs_dir(language, bench_dir) / f"{label}.json", default=None)


def _delta(cold, warm, lower_is_better=False) -> str:
    if cold is None or warm is None:
        return "—"
    d = round(warm - cold, 3)
    arrow = ""
    if d != 0:
        good = (d < 0) if lower_is_better else (d > 0)
        arrow = " ✅" if good else " ⚠️"
    return f"{d:+}{arrow}"


def render_report(language: str, cold: Optional[dict], warm: Optional[dict]) -> str:
    """Render the cold-vs-warm learning curve as a Markdown section."""
    cm = (cold or {}).get("metrics", {})
    wm = (warm or {}).get("metrics", {})
    lines = [f"## {language} — learning curve (held-out test split)", ""]

    if not cold and not warm:
        lines.append("_No runs recorded yet._")
        return "\n".join(lines) + "\n"
    if (cold and not cm.get("measurable")) or (warm and not wm.get("measurable")):
        lines.append("> ⚠️ A run was **not measurable** (Docker unavailable, so code "
                     "could not be verified). No numbers are reported rather than faking "
                     "a result. Start Docker and re-run to populate this table.")
        lines.append("")

    rows = [
        ("tasks (n)", cm.get("n"), wm.get("n"), None),
        ("pass@1", cm.get("pass_rate"), wm.get("pass_rate"), False),
        ("hallucinated-symbol rate", cm.get("hallucinated_symbol_rate"),
         wm.get("hallucinated_symbol_rate"), True),
        ("mean self-correction iters", cm.get("mean_self_correction_iters"),
         wm.get("mean_self_correction_iters"), True),
    ]
    lines += ["| metric | cold (no KB) | warm (after learning) | delta |",
              "| --- | --- | --- | --- |"]
    for name, c, w, lib in rows:
        delta = "—" if lib is None else _delta(c, w, lower_is_better=lib)
        lines.append(f"| {name} | {c if c is not None else '—'} | "
                     f"{w if w is not None else '—'} | {delta} |")
    lines.append("")
    lines.append("_pass@1 higher is better; hallucination rate and iters lower is "
                 "better. Cold = empty KB; warm = after learning from the train split._")
    return "\n".join(lines) + "\n"


def report(language: str, bench_dir: Optional[Path] = None) -> str:
    return render_report(language,
                         load_run(language, "cold", bench_dir),
                         load_run(language, "warm", bench_dir))
