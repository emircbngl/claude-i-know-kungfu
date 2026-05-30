"""Configuration and the user-level knowledge home (``~/.kungfu``).

The knowledge base is personal and lives outside the repo. It is created on
first use (bootstrap). ``KUNGFU_HOME`` overrides the location (used by tests and
by the bench cold/warm snapshots).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from . import _io

CONFIG_VERSION = 1


def kungfu_home() -> Path:
    """Return the knowledge-base root, honoring ``KUNGFU_HOME``."""
    env = os.environ.get("KUNGFU_HOME")
    return Path(env).expanduser() if env else Path.home() / ".kungfu"


def default_config() -> dict[str, Any]:
    """The seed config written on first run.

    ``managed: true`` means a language is treated as unknown/high-risk —
    verification is mandatory and the honesty gate is strict. Known languages
    (e.g. Python) are unmanaged: the learn loop still runs, retrieval is optional.
    """
    return {
        "version": CONFIG_VERSION,
        "managed_languages": {
            "gleam": {"extensions": [".gleam"], "managed": True},
            "julia": {"extensions": [".jl"], "managed": True},
            "oberon": {"extensions": [".obn"], "managed": True},
            "python": {"extensions": [".py"], "managed": False},
        },
        "docker": {
            "enabled": True,
            "cpus": "1.0",
            "memory": "512m",
            "pids_limit": 256,
            "timeout_seconds": 60,
            "network": "none",
        },
        "fetch": {"prefer": ["context7", "webfetch"]},
        "learn": {"rollup_threshold": 3},
    }


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively fill missing keys in ``override`` from ``base``."""
    out = dict(override)
    for k, v in base.items():
        if k not in out:
            out[k] = v
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(v, out[k])
    return out


def ensure_home(home: Optional[Path] = None) -> Path:
    """Create ``~/.kungfu`` and its subdirectories if absent. Idempotent."""
    home = home or kungfu_home()
    (home / "knowledge").mkdir(parents=True, exist_ok=True)
    (home / "cache").mkdir(parents=True, exist_ok=True)
    return home


def config_path(home: Optional[Path] = None) -> Path:
    return (home or kungfu_home()) / "config.json"


def load_config(home: Optional[Path] = None) -> dict[str, Any]:
    """Load config, bootstrapping defaults on first run and back-filling new keys."""
    home = ensure_home(home)
    p = config_path(home)
    if not p.exists():
        cfg = default_config()
        _io.write_json_atomic(p, cfg)
        return cfg
    cfg = _io.read_json(p, default={})
    return _deep_merge(default_config(), cfg if isinstance(cfg, dict) else {})


def save_config(cfg: dict[str, Any], home: Optional[Path] = None) -> Path:
    home = ensure_home(home)
    return _io.write_json_atomic(config_path(home), cfg)


def language_for_path(path: str, cfg: dict[str, Any]) -> Optional[str]:
    """Map a file path to a configured language by extension, else None."""
    suffix = Path(path).suffix.lower()
    for lang, spec in cfg.get("managed_languages", {}).items():
        if suffix in [e.lower() for e in spec.get("extensions", [])]:
            return lang
    return None


def is_managed(language: str, cfg: dict[str, Any]) -> bool:
    spec = cfg.get("managed_languages", {}).get(language)
    return bool(spec and spec.get("managed"))
