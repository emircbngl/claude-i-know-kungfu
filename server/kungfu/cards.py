"""Knowledge cards: a unit of grounded knowledge with provenance.

A card is a Markdown file with a small frontmatter block. The frontmatter is the
honesty ledger: where the knowledge came from, whether it was verified by
execution, and against which language version. We parse a deliberately tiny
frontmatter dialect (scalar ``key: value`` lines) so there is no YAML dependency
and the format stays auditable by hand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

# Epistemic states (see references/epistemic-states.md).
VERIFIED = "VERIFIED"      # compiled/ran in the sandbox
GROUNDED = "GROUNDED"      # backed by a cited fetched source, not yet run
HYPOTHESIS = "HYPOTHESIS"  # a guess; must be promoted or disclosed

_KINDS = {"syntax", "stdlib", "library", "skeleton", "verified"}


@dataclass
class Card:
    language: str
    kind: str
    slug: str
    title: str = ""
    source: str = ""            # URL, or "verify" / "user"
    fetched: str = ""           # ISO date the knowledge was captured
    verified: bool = False      # the content was confirmed by execution
    verified_against: str = ""  # language/toolchain version it was verified on
    confidence: str = "low"     # high | medium | low
    body: str = ""

    def __post_init__(self) -> None:
        self.kind = (self.kind or "").strip().lower()
        if not self.title:
            self.title = self.slug


def epistemic_state(card: Card) -> str:
    """The single rule that drives honesty: proof beats citation beats guess."""
    if card.verified:
        return VERIFIED
    if card.source:
        return GROUNDED
    return HYPOTHESIS


def is_stale(card: Card, current_version: str) -> bool:
    """A verified card is stale when the toolchain version has drifted."""
    if not (card.verified and card.verified_against and current_version):
        return False
    return card.verified_against.strip() != current_version.strip()


def _fmt_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


_FIELDS = ["language", "kind", "slug", "title", "source", "fetched",
           "verified", "verified_against", "confidence"]


def dumps(card: Card) -> str:
    """Serialize a card to frontmatter + body Markdown."""
    lines = ["---"]
    for f in _FIELDS:
        lines.append(f"{f}: {_fmt_scalar(getattr(card, f))}")
    lines.append("---")
    text = "\n".join(lines) + "\n"
    if card.body:
        text += "\n" + card.body.rstrip("\n") + "\n"
    return text


def loads(text: str) -> Card:
    """Parse frontmatter + body Markdown back into a Card."""
    lines = text.splitlines()
    meta: dict[str, object] = {}
    body = text
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            for line in lines[1:end]:
                if ":" in line:
                    k, _, v = line.partition(":")
                    k = k.strip()
                    if k in _FIELDS:
                        meta[k] = v.strip()  # all fields are strings...
            body = "\n".join(lines[end + 1:]).strip("\n")
    # ...except `verified`, which is the one boolean (a bare bool(str) would be
    # True for both "true" and "false", so compare the text explicitly).
    verified = str(meta.get("verified", "")).strip().lower() == "true"
    return Card(
        language=str(meta.get("language", "")),
        kind=str(meta.get("kind", "")),
        slug=str(meta.get("slug", "")),
        title=str(meta.get("title", "")),
        source=str(meta.get("source", "")),
        fetched=str(meta.get("fetched", "")),
        verified=verified,
        verified_against=str(meta.get("verified_against", "")),
        confidence=str(meta.get("confidence", "low")),
        body=body,
    )


def new_card(
    language: str,
    kind: str,
    slug: str,
    body: str,
    title: str = "",
    source: str = "",
    verified: bool = False,
    verified_against: str = "",
    confidence: str = "",
    today: Optional[str] = None,
) -> Card:
    """Construct a card, inferring confidence from its epistemic state."""
    fetched = today or date.today().isoformat()
    if not confidence:
        confidence = "high" if verified else ("medium" if source else "low")
    return Card(
        language=language,
        kind=kind,
        slug=slug,
        title=title or slug,
        source=source,
        fetched=fetched,
        verified=verified,
        verified_against=verified_against,
        confidence=confidence,
        body=body,
    )
