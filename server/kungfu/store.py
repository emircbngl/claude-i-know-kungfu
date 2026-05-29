"""The librarian: sharded read/write of the per-language knowledge base.

Layout under ``~/.kungfu/knowledge/<lang>/``::

    _index.md            # human-readable manifest (a VIEW, recomputed from files)
    skeleton.md          # structural model + negative knowledge + learned rules
    syntax/<topic>.md    # one concept per file
    stdlib/<module>.md
    libraries/<lib>.md
    lessons.jsonl        # data: wrong -> right lessons (managed by learn.py)
    lessons.md           # VIEW of lessons.jsonl (managed by learn.py)

Design rule: **files are the source of truth; every ``.md`` index is a view**
recomputed from them. ``lookup`` is manifest-first — it returns the cheap index,
the skeleton, and only the matched shards, never the whole language.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

from . import _io
from . import cards as cards_mod
from .cards import Card

# kind -> subdirectory for file-backed cards
KINDS_DIR = {"syntax": "syntax", "stdlib": "stdlib", "library": "libraries"}


def _safe(s: str) -> str:
    return s.strip().lower().replace("/", "_").replace(" ", "-")


def lang_dir(home: Path, language: str) -> Path:
    """Return (and create) the directory for a language's knowledge."""
    d = home / "knowledge" / _safe(language)
    for sub in KINDS_DIR.values():
        (d / sub).mkdir(parents=True, exist_ok=True)
    return d


def card_path(home: Path, card: Card) -> Path:
    d = lang_dir(home, card.language)
    if card.kind == "skeleton":
        return d / "skeleton.md"
    sub = KINDS_DIR.get(card.kind)
    fname = _safe(card.slug) + ".md"
    return (d / sub / fname) if sub else (d / fname)


def save_card(home: Path, card: Card) -> Path:
    """Persist a card. Same (kind, slug) overwrites — that is the dedupe.

    ``kind == "skeleton"`` is special: it writes the free-form skeleton.md
    (structural model + negative knowledge), not a frontmatter card.
    """
    if card.kind == "skeleton":
        return set_skeleton(home, card.language, card.body)
    p = card_path(home, card)
    # Collision guard: _safe is lossy (slashes/spaces collapse), so two DISTINCT
    # slugs can map to one filename. If the target already holds a different slug,
    # disambiguate with a short hash rather than silently overwriting it.
    if p.exists():
        try:
            existing = cards_mod.loads(p.read_text(encoding="utf-8"))
            if existing.slug != card.slug:
                h = hashlib.sha1(card.slug.strip().lower().encode("utf-8")).hexdigest()[:6]
                p = p.with_name(f"{p.stem}-{h}{p.suffix}")
        except OSError:
            pass
    _io.write_text_atomic(p, cards_mod.dumps(card))
    update_manifest(home, card.language)
    return p


def read_cards(home: Path, language: str, kind: Optional[str] = None) -> list[Card]:
    d = lang_dir(home, language)
    subs = [KINDS_DIR[kind]] if kind else list(KINDS_DIR.values())
    out: list[Card] = []
    for sub in subs:
        for f in sorted((d / sub).glob("*.md")):
            try:
                out.append(cards_mod.loads(f.read_text(encoding="utf-8")))
            except OSError:
                continue
    return out


def skeleton_path(home: Path, language: str) -> Path:
    return lang_dir(home, language) / "skeleton.md"


def get_skeleton(home: Path, language: str) -> str:
    p = skeleton_path(home, language)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def set_skeleton(home: Path, language: str, text: str) -> Path:
    p = skeleton_path(home, language)
    _io.write_text_atomic(p, text.rstrip("\n") + "\n")
    update_manifest(home, language)
    return p


def manifest(home: Path, language: str) -> dict:
    """Compute a manifest dict directly from files (never parsed from _index.md)."""
    counts: dict[str, int] = {}
    topics: list[dict] = []
    for kind in KINDS_DIR:
        cs = read_cards(home, language, kind)
        counts[kind] = len(cs)
        for c in cs:
            topics.append({
                "kind": kind,
                "slug": c.slug,
                "title": c.title,
                "state": cards_mod.epistemic_state(c),
                "source": c.source,
                "verified_against": c.verified_against,
            })
    from . import learn as learn_mod  # lazy: avoid import cycle
    lessons = learn_mod.load_lessons(home, language)
    return {
        "language": language,
        "counts": counts,
        "lessons": len(lessons),
        "has_skeleton": bool(get_skeleton(home, language).strip()),
        "topics": topics,
    }


def update_manifest(home: Path, language: str) -> Path:
    """Render _index.md from the computed manifest (a view)."""
    m = manifest(home, language)
    lines = [
        f"# {language} — knowledge manifest",
        "",
        f"- syntax: {m['counts'].get('syntax', 0)}",
        f"- stdlib: {m['counts'].get('stdlib', 0)}",
        f"- libraries: {m['counts'].get('library', 0)}",
        f"- lessons: {m['lessons']}",
        f"- skeleton: {'yes' if m['has_skeleton'] else 'no'}",
        "",
        "| kind | topic | state | source |",
        "| --- | --- | --- | --- |",
    ]
    for t in sorted(m["topics"], key=lambda x: (x["kind"], x["slug"])):
        src = t["source"] or "—"
        lines.append(f"| {t['kind']} | {t['slug']} | {t['state']} | {src} |")
    p = lang_dir(home, language) / "_index.md"
    _io.write_text_atomic(p, "\n".join(lines) + "\n")
    return p


def _card_view(c: Card) -> dict:
    return {
        "kind": c.kind,
        "slug": c.slug,
        "title": c.title,
        "state": cards_mod.epistemic_state(c),
        "source": c.source,
        "verified_against": c.verified_against,
        "body": c.body,
    }


def _score(card: Card, query: str) -> int:
    q = query.lower().strip()
    hay = " ".join([card.slug, card.title, card.body]).lower()
    score = hay.count(q) * 3
    score += sum(1 for tok in q.split() if tok and tok in hay)
    return score


def _retrieval_note(language: str, m: dict, skeleton: str, cards: list, lessons: list) -> str:
    # Base the "we know nothing" warning on TOTAL stored knowledge, not on the
    # query-filtered `cards` — otherwise a query that simply matches nothing would
    # falsely tell the agent to distrust a KB that does have grounded cards.
    total_cards = sum(m["counts"].values())
    if not skeleton.strip() and total_cards == 0 and m["lessons"] == 0:
        return (
            f"No grounded knowledge for '{language}' yet. Treat everything you write as "
            f"HYPOTHESIS: do NOT assert APIs from memory. Run /kungfu-teach {language} or "
            f"fetch real docs and save them before claiming anything works."
        )
    bits = []
    if lessons:
        bits.append(f"{len(lessons)} relevant lesson(s) loaded — check them before writing")
    if skeleton.strip():
        bits.append("skeleton loaded (incl. negative knowledge)")
    bits.append("anything not GROUNDED or VERIFIED must be flagged HYPOTHESIS and verified")
    return "; ".join(bits) + "."


def lookup(home: Path, language: str, query: Optional[str] = None,
           kind: Optional[str] = None, limit: int = 6) -> dict:
    """Manifest-first retrieval: skeleton + matched cards + matched lessons only."""
    skeleton = get_skeleton(home, language)
    m = manifest(home, language)
    cards = read_cards(home, language, kind)
    if query:
        scored = [(s, c) for c in cards if (s := _score(c, query)) > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        cards = [c for _, c in scored][:limit]
    else:
        cards = cards[:limit]

    from . import learn as learn_mod  # lazy
    if query:
        lessons = learn_mod.match_lessons(home, language, query)
    else:
        lessons = learn_mod.load_lessons(home, language)
    lessons = lessons[:limit]

    return {
        "language": language,
        "skeleton": skeleton,
        "manifest": {
            "counts": m["counts"],
            "lessons": m["lessons"],
            "has_skeleton": m["has_skeleton"],
        },
        "cards": [_card_view(c) for c in cards],
        "lessons": lessons,
        "note": _retrieval_note(language, m, skeleton, cards, lessons),
    }
