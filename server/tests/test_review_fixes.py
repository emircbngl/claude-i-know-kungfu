"""Regression tests for the bugs found in the max-effort code review."""

from kungfu import _io, cards, learn, store


def test_string_field_named_false_not_coerced_to_bool():
    # Only `verified` is boolean; a string field equal to "false" must survive.
    c = cards.new_card("g", "library", "x", "b", title="false", source="u")
    c2 = cards.loads(cards.dumps(c))
    assert c2.title == "false" and c2.verified is False


def test_retrieval_note_no_false_negative_when_cards_exist(tmp_path):
    store.save_card(tmp_path, cards.new_card("python", "syntax", "decorators", "use @", source="u"))
    note = store.lookup(tmp_path, "python", "zzznomatch")["note"].lower()
    assert "no grounded knowledge" not in note  # a query miss is not "we know nothing"


def test_distinct_triggers_sharing_words_do_not_merge(tmp_path):
    learn.add_lesson(tmp_path, "gleam", {"trigger": "map over a list returns a new list ALPHA", "right": "a"})
    learn.add_lesson(tmp_path, "gleam", {"trigger": "map over a list returns a new list BETA", "right": "b"})
    assert len(learn.load_lessons(tmp_path, "gleam")) == 2


def test_reinforcement_applies_correction(tmp_path):
    learn.add_lesson(tmp_path, "gleam", {"trigger": "X", "right": "old", "model": "m"})
    learn.add_lesson(tmp_path, "gleam", {"trigger": "X", "right": "new-correct"})
    lessons = learn.load_lessons(tmp_path, "gleam")
    assert len(lessons) == 1
    assert lessons[0]["right"] == "new-correct" and lessons[0]["seen"] == 2


def test_atomic_write_and_json_helpers(tmp_path):
    p = tmp_path / "sub" / "f.txt"
    _io.write_text_atomic(p, "hello")
    assert p.read_text() == "hello"
    jp = tmp_path / "x.json"
    _io.write_json_atomic(jp, {"k": [1, 2]})
    assert _io.read_json(jp) == {"k": [1, 2]}
    assert _io.read_json(tmp_path / "missing.json", default={"d": 1}) == {"d": 1}


def test_distinct_slugs_colliding_on_safe_do_not_overwrite(tmp_path):
    # "list comprehension" and "list-comprehension" both _safe -> list-comprehension.
    store.save_card(tmp_path, cards.new_card("g", "syntax", "list comprehension", "A", source="u"))
    store.save_card(tmp_path, cards.new_card("g", "syntax", "list-comprehension", "B", source="u"))
    cs = store.read_cards(tmp_path, "g", "syntax")
    assert sorted(c.slug for c in cs) == ["list comprehension", "list-comprehension"]
    assert sorted(c.body for c in cs) == ["A", "B"]  # both preserved, no silent overwrite


def test_same_slug_still_dedupes(tmp_path):
    store.save_card(tmp_path, cards.new_card("g", "syntax", "case", "v1", source="u"))
    store.save_card(tmp_path, cards.new_card("g", "syntax", "case", "v2", source="u"))
    cs = store.read_cards(tmp_path, "g", "syntax")
    assert len(cs) == 1 and cs[0].body == "v2"  # identical slug overwrites (dedupe intact)
