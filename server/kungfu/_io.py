"""Atomic file I/O helpers.

The knowledge base is the product's memory, so writes must not corrupt it on a
crash or interleave under concurrent tool calls. Every write goes to a temp file
in the same directory and is then atomically ``os.replace``d into place.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def write_text_atomic(path: Path | str, text: str, encoding: str = "utf-8") -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
        os.replace(tmp, path)  # atomic on POSIX
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass
    return path


def write_json_atomic(path: Path | str, obj: Any) -> Path:
    return write_text_atomic(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path | str, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default
