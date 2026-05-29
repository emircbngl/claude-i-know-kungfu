from kungfu import cards


def test_roundtrip_and_verified_state():
    c = cards.new_card("gleam", "syntax", "case", "body text",
                       source="http://x", verified=True, verified_against="1.x")
    assert cards.epistemic_state(c) == cards.VERIFIED
    c2 = cards.loads(cards.dumps(c))
    assert c2.slug == "case" and c2.verified is True
    assert c2.source == "http://x" and c2.body == "body text"
    assert c2.verified_against == "1.x"


def test_grounded_and_hypothesis_states():
    assert cards.epistemic_state(cards.new_card("g", "syntax", "a", "b", source="u")) == cards.GROUNDED
    assert cards.epistemic_state(cards.new_card("g", "syntax", "a", "b")) == cards.HYPOTHESIS


def test_is_stale_only_for_verified_version_drift():
    c = cards.new_card("g", "syntax", "a", "b", verified=True, verified_against="1.x")
    assert cards.is_stale(c, "2.x") is True
    assert cards.is_stale(c, "1.x") is False
    assert cards.is_stale(cards.new_card("g", "syntax", "a", "b"), "1.x") is False


def test_confidence_inferred_from_state():
    assert cards.new_card("g", "syntax", "a", "b", verified=True).confidence == "high"
    assert cards.new_card("g", "syntax", "a", "b", source="u").confidence == "medium"
    assert cards.new_card("g", "syntax", "a", "b").confidence == "low"
