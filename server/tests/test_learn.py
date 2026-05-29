from kungfu import learn, store


def test_classify_taxonomy():
    assert learn.classify({"error_text": "Unknown variable `foo`"}) == "NONEXISTENT"
    assert learn.classify({"error_text": "expected 1 argument, got 2"}) == "API-SHAPE"
    assert learn.classify({"error_text": "syntax error: unexpected token"}) == "SYNTAX"
    assert learn.classify({"error_text": "No module named x"}) == "DEPENDENCY"
    assert learn.classify({"misconception": "it has early return"}) == "SEMANTIC"
    assert learn.classify({"error_type": "IDIOM"}) == "IDIOM"   # explicit trusted


def test_add_dedupe_reinforce(tmp_path):
    base = {"misconception": "has return", "trigger": "reaching for return",
            "wrong": "return 42", "right": "42", "model": "expression oriented"}
    r1 = learn.add_lesson(tmp_path, "gleam", dict(base))
    assert r1["added"] and r1["seen"] == 1
    r2 = learn.add_lesson(tmp_path, "gleam", {"trigger": "Reaching for `return`"})
    assert r2["reinforced"] and r2["seen"] == 2          # normalized trigger dedupes
    assert len(learn.load_lessons(tmp_path, "gleam")) == 1


def test_verified_lesson_rolls_into_skeleton(tmp_path):
    learn.add_lesson(tmp_path, "gleam",
                     {"trigger": "x", "model": "no return; expression oriented",
                      "verified": True})
    sk = store.get_skeleton(tmp_path, "gleam")
    assert "Learned rules" in sk and "expression oriented" in sk


def test_recurrence_threshold_rolls_up(tmp_path):
    for _ in range(3):
        learn.add_lesson(tmp_path, "gleam",
                         {"trigger": "recurring thing", "model": "the structural rule"},
                         rollup_threshold=3)
    assert "the structural rule" in store.get_skeleton(tmp_path, "gleam")


def test_match_lessons(tmp_path):
    learn.add_lesson(tmp_path, "gleam", {"trigger": "reaching for return", "model": "no return"})
    assert learn.match_lessons(tmp_path, "gleam", "return")
    assert learn.match_lessons(tmp_path, "gleam", "completely unrelated zzz") == []


def test_render_md_view(tmp_path):
    learn.add_lesson(tmp_path, "gleam",
                     {"misconception": "m", "trigger": "t", "wrong": "w", "right": "r", "model": "mod"})
    md = learn.render_lessons_md("gleam", learn.load_lessons(tmp_path, "gleam"))
    assert "lessons" in md and "Wrong" in md and "Right" in md
