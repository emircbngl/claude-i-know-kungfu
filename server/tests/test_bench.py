from kungfu import bench, verify


def test_list_and_load_real_suite():
    assert bench.list_tasks("gleam", "train") == ["list_reverse", "sum_list"]
    assert bench.list_tasks("gleam", "test") == ["double_list", "list_length", "list_max", "list_product"]
    t = bench.load_task("gleam", "train", "list_reverse")
    assert t["scaffold"] == {}  # the sandbox owns the project config (gleam.toml)
    assert "src/list_reverse.gleam" in t["ref"]
    assert "test/list_reverse_test.gleam" in t["hidden"]


def test_merge_keeps_candidate_and_appends_hidden_tests():
    t = bench.load_task("gleam", "train", "list_reverse")
    m = bench.merge_files(t, {"src/list_reverse.gleam": "CANDIDATE"})
    assert m["src/list_reverse.gleam"] == "CANDIDATE"
    assert "test/list_reverse_test.gleam" in m


def test_metrics_math():
    res = [{"ok": True, "available": True, "unknown_symbols": [], "iters": 1},
           {"ok": False, "available": True, "unknown_symbols": ["x"], "iters": 3}]
    m = bench.metrics(res)
    assert m["pass_rate"] == 0.5 and m["hallucinated_symbol_rate"] == 0.5
    assert m["mean_self_correction_iters"] == 2.0 and m["measurable"] is True


def test_metrics_unmeasurable_when_unavailable():
    m = bench.metrics([{"ok": False, "available": False, "unknown_symbols": [], "iters": 1}])
    assert m["measurable"] is False


def test_render_report_shows_delta():
    cold = {"metrics": {"n": 2, "pass_rate": 0.0, "hallucinated_symbol_rate": 0.5,
                        "mean_self_correction_iters": 3, "measurable": True}}
    warm = {"metrics": {"n": 2, "pass_rate": 1.0, "hallucinated_symbol_rate": 0.0,
                        "mean_self_correction_iters": 1, "measurable": True}}
    rep = bench.render_report("gleam", cold, warm)
    assert "learning curve" in rep and "+1.0" in rep and "pass@1" in rep


def test_render_report_flags_unmeasurable():
    un = {"metrics": {"n": 1, "measurable": False, "available": 0}}
    rep = bench.render_report("gleam", un, None)
    assert "not measurable" in rep.lower()


def test_save_load_run(tmp_path):
    bench.save_run("gleam", "cold", {"metrics": {"n": 1, "pass_rate": 1.0}, "results": []},
                   bench_dir=tmp_path)
    got = bench.load_run("gleam", "cold", bench_dir=tmp_path)
    assert got["label"] == "cold" and got["metrics"]["pass_rate"] == 1.0


def test_score_not_measurable_without_docker(monkeypatch):
    monkeypatch.setattr(verify, "docker_available", lambda: False)
    sols = {"list_reverse": {"src/list_reverse.gleam": "pub fn reverse(x) { x }"},
            "sum_list": {"src/sum_list.gleam": "pub fn sum(x) { 0 }"}}
    out = bench.score("gleam", "train", sols)
    assert out["metrics"]["measurable"] is False
    assert all(r["available"] is False for r in out["results"])
