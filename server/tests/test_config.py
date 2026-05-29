import json

from kungfu import config


def test_bootstrap_creates_config(tmp_path):
    cfg = config.load_config(tmp_path)
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "knowledge").is_dir()
    assert cfg["version"] == config.CONFIG_VERSION


def test_deep_merge_backfills_missing_keys(tmp_path):
    config.ensure_home(tmp_path)
    (tmp_path / "config.json").write_text(
        json.dumps({"managed_languages": {"foo": {"extensions": [".foo"], "managed": True}}}),
        encoding="utf-8",
    )
    cfg = config.load_config(tmp_path)
    assert "docker" in cfg and "learn" in cfg          # back-filled from defaults
    assert "foo" in cfg["managed_languages"]            # user value preserved


def test_language_for_path_and_managed(tmp_path):
    cfg = config.load_config(tmp_path)
    assert config.language_for_path("a/b.gleam", cfg) == "gleam"
    assert config.language_for_path("a/b.py", cfg) == "python"
    assert config.language_for_path("a/b.rs", cfg) is None
    assert config.is_managed("gleam", cfg) is True
    assert config.is_managed("python", cfg) is False
