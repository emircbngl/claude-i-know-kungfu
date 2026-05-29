from kungfu import cards, store


def test_save_read_and_dedupe_overwrites(tmp_path):
    store.save_card(tmp_path, cards.new_card("gleam", "syntax", "case", "v1", source="u"))
    store.save_card(tmp_path, cards.new_card("gleam", "syntax", "case", "v2", source="u"))
    got = store.read_cards(tmp_path, "gleam", "syntax")
    assert len(got) == 1 and got[0].body == "v2"   # same (kind, slug) overwrote


def test_manifest_counts(tmp_path):
    store.save_card(tmp_path, cards.new_card("gleam", "syntax", "a", "x", source="u"))
    store.save_card(tmp_path, cards.new_card("gleam", "library", "lib@1", "x", source="u"))
    m = store.manifest(tmp_path, "gleam")
    assert m["counts"]["syntax"] == 1 and m["counts"]["library"] == 1


def test_lookup_empty_warns_hypothesis(tmp_path):
    lk = store.lookup(tmp_path, "rust", "anything")
    assert "no grounded knowledge" in lk["note"].lower()


def test_lookup_matches_query(tmp_path):
    store.save_card(tmp_path, cards.new_card(
        "gleam", "syntax", "case-expr", "pattern matching with case", source="u"))
    lk = store.lookup(tmp_path, "gleam", "pattern")
    assert any(c["slug"] == "case-expr" for c in lk["cards"])
    assert lk["cards"][0]["state"] == cards.GROUNDED


def test_skeleton_via_save_card(tmp_path):
    store.save_card(tmp_path, cards.Card(language="gleam", kind="skeleton", slug="-",
                                         body="# gleam\n## Core\n- expression oriented"))
    assert "expression oriented" in store.get_skeleton(tmp_path, "gleam")
    assert store.manifest(tmp_path, "gleam")["has_skeleton"] is True
