"""The learn loop: turn a mistake into a recallable lesson.

A lesson is a **misconception -> correct-model** pair, classified by an error
taxonomy and keyed by the *flawed reasoning* (``trigger``) so it surfaces the
next time that reasoning recurs — not just when the exact bad string reappears.

Storage: ``lessons.jsonl`` is the source of truth (one JSON lesson per line,
robust to append/dedupe/rollup). ``lessons.md`` is a human-readable view that is
re-rendered on every change. Recurring high-confidence lessons are rolled up into
``skeleton.md`` so the agent grasps structure, not just a flat list of fixes.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Optional

from . import _io
from . import store

# Error taxonomy (see references/error-taxonomy.md).
ERROR_TYPES = [
    "SYNTAX",        # malformed grammar
    "API-SHAPE",     # wrong signature / arity / argument order
    "SEMANTIC",      # wrong mental model of how the language behaves
    "NONEXISTENT",   # hallucinated a symbol / feature that does not exist
    "DEPENDENCY",    # wrong import / missing module / package mismatch
    "VERSION-DRIFT", # was right once, changed across versions
    "IDIOM",         # works, but not the idiomatic / safe way
]

# Order matters: more specific / less ambiguous categories are checked first.
# (e.g. SYNTAX before API-SHAPE so "unexpected token" is not caught by "expected".)
_CLASSIFY_RULES = [
    ("NONEXISTENT", ("unknown", "undefined", "not found", "no such", "does not exist",
                     "cannot find", "unresolved", "has no")),
    ("SYNTAX", ("syntax error", "unexpected token", "unexpected", "parse error",
                "parse", "indent", "expected `")),
    ("API-SHAPE", ("argument", "arity", "signature", "too many",
                   "too few", "takes", "positional")),
    ("DEPENDENCY", ("import", "module not found", "no module", "dependency",
                    "package", "cannot import")),
    ("VERSION-DRIFT", ("deprecated", "removed in", "renamed", "since version",
                       "no longer")),
    ("IDIOM", ("idiom", "idiomatic", "prefer", "should use", "anti-pattern")),
]


def lessons_path(home: Path, language: str) -> Path:
    return store.lang_dir(home, language) / "lessons.jsonl"


def lessons_md_path(home: Path, language: str) -> Path:
    return store.lang_dir(home, language) / "lessons.md"


def load_lessons(home: Path, language: str) -> list[dict]:
    p = lessons_path(home, language)
    if not p.exists():
        return []
    out: list[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _normalize(s: str) -> str:
    s = (s or "").lower().replace("`", " ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _slug(s: str, max_words: int = 6) -> str:
    words = _normalize(s).split()[:max_words]
    return "-".join(words) or "lesson"


def lesson_id(lesson: dict) -> str:
    if lesson.get("id"):
        return store._safe(str(lesson["id"]))
    basis = lesson.get("trigger") or lesson.get("misconception") or lesson.get("wrong") or "lesson"
    # Readable slug + a short hash of the FULL normalized basis, so two distinct
    # triggers that share their first few words get different ids (and are not
    # silently merged). Identical triggers still map to the same id.
    digest = hashlib.sha1(_normalize(basis).encode("utf-8")).hexdigest()[:6]
    return f"{_slug(basis)}-{digest}"


def classify(lesson: dict) -> str:
    """Return an error type, trusting an explicit valid one, else heuristics."""
    explicit = (lesson.get("error_type") or "").strip().upper()
    if explicit in ERROR_TYPES:
        return explicit
    text = " ".join(str(lesson.get(k, "")) for k in
                    ("error_text", "wrong", "misconception", "trigger")).lower()
    for etype, needles in _CLASSIFY_RULES:
        if any(n in text for n in needles):
            return etype
    return "SEMANTIC"


def _save(home: Path, language: str, lessons: list[dict]) -> None:
    _io.write_text_atomic(
        lessons_path(home, language),
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lessons),
    )
    _io.write_text_atomic(lessons_md_path(home, language),
                          render_lessons_md(language, lessons))
    store.update_manifest(home, language)


def add_lesson(home: Path, language: str, lesson: dict,
               today: Optional[str] = None,
               rollup_threshold: int = 3) -> dict:
    """Add or reinforce a lesson. Dedupe by id / normalized trigger.

    Returns a result dict: ``{id, error_type, added, reinforced, seen, rolled_up}``.
    """
    lesson = dict(lesson)
    lesson["error_type"] = classify(lesson)
    lid = lesson_id(lesson)
    lesson["id"] = lid
    norm_trigger = _normalize(lesson.get("trigger", ""))

    lessons = load_lessons(home, language)
    existing = None
    for x in lessons:
        if x.get("id") == lid or (norm_trigger and _normalize(x.get("trigger", "")) == norm_trigger):
            existing = x
            break

    rolled_up = False
    if existing is not None:
        existing["seen"] = int(existing.get("seen", 1)) + 1
        for k in ("misconception", "trigger", "wrong", "right", "model",
                  "source", "verified", "verified_against", "error_type"):
            v = lesson.get(k)
            if v not in (None, "", False):
                existing[k] = v  # apply corrections, not only fill blanks
                                 # (verified=False is skipped, so it never downgrades a True)
        seen = existing["seen"]
        reinforced, added = True, False
    else:
        lesson.setdefault("added", today or date.today().isoformat())
        lesson["seen"] = 1
        lessons.append(lesson)
        seen = 1
        reinforced, added = False, True

    _save(home, language, lessons)

    target = existing if existing is not None else lesson
    if seen >= rollup_threshold or bool(target.get("verified")):
        rolled_up = _rollup_one(home, language, target)

    return {
        "id": lid,
        "error_type": target.get("error_type"),
        "added": added,
        "reinforced": reinforced,
        "seen": seen,
        "rolled_up": rolled_up,
    }


def match_lessons(home: Path, language: str, query: Optional[str]) -> list[dict]:
    lessons = load_lessons(home, language)
    if not query:
        return lessons
    tokens = [t for t in _normalize(query).split() if len(t) > 2]
    if not tokens:
        return lessons

    def score(x: dict) -> int:
        hay = _normalize(" ".join(str(x.get(k, "")) for k in
                        ("trigger", "misconception", "wrong", "right", "model", "error_type")))
        return sum(hay.count(t) for t in tokens)

    scored = [(score(x), x) for x in lessons]
    scored = [(s, x) for s, x in scored if s > 0]
    scored.sort(key=lambda p: (p[0], int(p[1].get("seen", 1))), reverse=True)
    return [x for _, x in scored]


# ---- skeleton rollup ---------------------------------------------------------

_LEARNED_HEADER = "## Learned rules (from lessons)"


def _skeleton_scaffold(language: str) -> str:
    return (
        f"# {language} — skeleton\n\n"
        "## Core structural rules\n\n"
        "## Does NOT exist (negative knowledge)\n\n"
        f"{_LEARNED_HEADER}\n"
    )


def _rollup_one(home: Path, language: str, lesson: dict) -> bool:
    """Fold one lesson's correct model into skeleton.md. Idempotent by (id)."""
    rule = (lesson.get("model") or lesson.get("right") or "").strip().replace("\n", " ")
    if not rule:
        return False
    lid = lesson.get("id", "")
    marker = f"- ({lid})"
    text = store.get_skeleton(home, language) or _skeleton_scaffold(language)
    if marker in text:
        return False
    if _LEARNED_HEADER not in text:
        text = text.rstrip("\n") + "\n\n" + _LEARNED_HEADER + "\n"
    lines = text.rstrip("\n").splitlines()
    idx = lines.index(_LEARNED_HEADER)
    insert_at = len(lines)
    for j in range(idx + 1, len(lines)):
        if lines[j].startswith("## "):
            insert_at = j
            break
    lines.insert(insert_at, f"{marker} {rule}")
    store.set_skeleton(home, language, "\n".join(lines))
    return True


def rollup_skeleton(home: Path, language: str, threshold: int = 3) -> int:
    """Re-fold all qualifying lessons (recurring or verified). Returns count folded."""
    n = 0
    for x in load_lessons(home, language):
        if int(x.get("seen", 1)) >= threshold or bool(x.get("verified")):
            if _rollup_one(home, language, x):
                n += 1
    return n


# ---- rendering ---------------------------------------------------------------

def render_lessons_md(language: str, lessons: list[dict]) -> str:
    lines = [f"# {language} — lessons", "",
             "_Wrong -> right pairs, keyed by the flawed reasoning. "
             "Auto-rendered from lessons.jsonl; do not edit by hand._", ""]
    if not lessons:
        lines.append("_No lessons yet._")
        return "\n".join(lines) + "\n"
    by_type: dict[str, list[dict]] = {}
    for x in lessons:
        by_type.setdefault(x.get("error_type", "SEMANTIC"), []).append(x)
    for etype in ERROR_TYPES:
        group = by_type.get(etype)
        if not group:
            continue
        lines.append(f"## {etype}")
        lines.append("")
        for x in group:
            seen = int(x.get("seen", 1))
            badge = "VERIFIED" if x.get("verified") else "unverified"
            lines.append(f"### {x.get('id', '?')}  ·  seen×{seen}  ·  {badge}")
            if x.get("misconception"):
                lines.append(f"- **Misconception:** {x['misconception']}")
            if x.get("trigger"):
                lines.append(f"- **Triggers when:** {x['trigger']}")
            if x.get("wrong"):
                lines.append(f"- **Wrong:** `{str(x['wrong']).strip()}`")
            if x.get("right"):
                lines.append(f"- **Right:** `{str(x['right']).strip()}`")
            if x.get("model"):
                lines.append(f"- **Correct model:** {x['model']}")
            prov = x.get("source", "?")
            if x.get("verified_against"):
                prov += f" · {x['verified_against']}"
            lines.append(f"- **Provenance:** {prov}")
            lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"
