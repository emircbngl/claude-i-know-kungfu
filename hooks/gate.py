#!/usr/bin/env python3
"""I Know KungFu honesty gate (Pre/PostToolUse hook).

Reads the hook event JSON from stdin, finds the file being written, and — if its
extension belongs to a *managed* language — injects a reminder so Claude grounds
and verifies instead of guessing. Hooks can enforce; a skill can only advise.

Dependency-free and defensive by design: any error exits 0 silently so a hook
never breaks a tool call. Honors KUNGFU_HOME (defaults to ~/.kungfu).
"""

import json
import os
import sys
from pathlib import Path

# Fallback if config.json does not exist yet (mirrors config.default_config()).
_DEFAULT_MANAGED = {
    ".gleam": ("gleam", True),
    ".jl": ("julia", True),
    ".obn": ("oberon", True),
    ".py": ("python", False),
}


def kungfu_home() -> Path:
    return Path(os.environ.get("KUNGFU_HOME") or (Path.home() / ".kungfu"))


def managed_map() -> dict:
    """extension -> (language, managed_bool)."""
    cfg_path = kungfu_home() / "config.json"
    if not cfg_path.exists():
        return dict(_DEFAULT_MANAGED)
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT_MANAGED)
    out = {}
    for lang, spec in (cfg.get("managed_languages") or {}).items():
        for ext in spec.get("extensions", []):
            out[str(ext).lower()] = (lang, bool(spec.get("managed")))
    return out or dict(_DEFAULT_MANAGED)


def file_from_payload(payload: dict) -> str:
    ti = payload.get("tool_input") or payload.get("toolInput") or {}
    if isinstance(ti, dict):
        return ti.get("file_path") or ti.get("path") or ""
    return ""


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    fp = file_from_payload(payload)
    if not fp:
        return 0
    ext = Path(fp).suffix.lower()
    entry = managed_map().get(ext)
    if not entry:
        return 0
    language, managed = entry
    if not managed:
        return 0

    if mode == "pre":
        print(
            f"[kungfu] About to write {language} (a managed language). Before asserting "
            f"any API: call kungfu_status('{language}') and kungfu_lookup('{language}', "
            f"<topic>). Every symbol must be GROUNDED (cited) or VERIFIED (compiled); "
            f"anything else is a HYPOTHESIS and must be flagged. You will be verified."
        )
    elif mode == "post":
        print(
            f"[kungfu] {language} file written. Now verify it: call "
            f"kungfu_verify('{language}', files) to compile/test in the sandbox. If Docker "
            f"is unavailable, tell the user the code is UNVERIFIED. If it fails, fix it and "
            f"record the wrong->right via kungfu_learn."
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
