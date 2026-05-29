from kungfu import verify


def test_extract_unknown_symbols():
    text = ("Unknown variable `foo`\nNo module named `bar`\n"
            "name `baz` is not defined\nhas no attribute `qux`")
    syms = verify.extract_unknown_symbols(text)
    for name in ("foo", "bar", "baz", "qux"):
        assert name in syms


def test_degrades_honestly_without_docker(monkeypatch):
    monkeypatch.setattr(verify, "docker_available", lambda: False)
    r = verify.verify("gleam", {"gleam.toml": "name = \"app\"", "src/a.gleam": "pub fn a() { 1 }"})
    assert r["available"] is False and r["ok"] is False
    assert "docker" in r["reason"].lower()        # never fakes a pass


def test_no_files():
    r = verify.verify("gleam", {})
    assert r["available"] is False and "no files" in r["reason"]


def test_unsafe_path_rejected(monkeypatch):
    monkeypatch.setattr(verify, "docker_available", lambda: True)
    r = verify.verify("gleam", {"../evil.gleam": "x"})
    assert r["available"] is False and "unsafe" in r["reason"].lower()
