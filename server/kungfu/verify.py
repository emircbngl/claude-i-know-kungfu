"""The verify loop: the one truth oracle that cannot be faked.

Generated code is compiled / type-checked / tested inside a locked Docker
container. The compiler's verdict is ground truth. If Docker is unavailable we
return an explicit *cannot verify* result — we never fake a pass. Running
model-generated code in a sandbox is also the responsible-AI posture.

Each language image follows one contract: source is mounted read-only at
``/src``; the image copies it to a writable workdir, builds/tests it, prints
diagnostics, and exits non-zero on failure. All language-specific logic lives in
``sandbox/<lang>/`` — adding a language never touches this file.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Optional

from ._log import get_logger

log = get_logger()

SANDBOX_DIR = Path(__file__).resolve().parent.parent / "sandbox"

_UNKNOWN_PATTERNS = [
    # Gleam: "The module `gleam/list` does not have a `fold_left` value."
    r"does not have (?:a |an )?[`\"']([A-Za-z_][\w./]*)[`\"']",
    # OBNC / Oberon and similar: "undeclared identifier: LENGTH"
    r"undeclared identifier[:\s]+[`\"']?([A-Za-z_][\w.]*)",
    # "`name` is not in scope/defined/imported"
    r"[`\"']([A-Za-z_][\w./]*)[`\"'] is not (?:in scope|defined|imported)",
    # "Unknown variable/type/... `name`" (backtick-delimited so the error's own
    # category word, e.g. "Unknown module value", is never captured as a symbol)
    r"[Uu]nknown (?:variable|type|record field|constructor|module field|value|function|import)[^`\n]*?[`\"']([A-Za-z_][\w./]*)[`\"']",
    # Python NameError
    r"[Nn]ame [`\"']?([A-Za-z_]\w*)[`\"']? is not defined",
    r"[Cc]annot find (?:module|name|value) [`\"']?([A-Za-z_][\w./]*)",
    # Python AttributeError / ModuleNotFoundError
    r"has no attribute [`\"']?([A-Za-z_]\w*)",
    r"No module named [`\"']?([A-Za-z_][\w.]*)",
]


def extract_unknown_symbols(text: str) -> list[str]:
    """Heuristically pull 'this symbol does not exist' names from compiler output.

    Approximate by design — its job is a *consistent* signal for the fabrication
    rate (cold vs. warm), not a perfect parser.
    """
    found: list[str] = []
    for pat in _UNKNOWN_PATTERNS:
        for m in re.finditer(pat, text or ""):
            name = m.group(1)
            if name and name not in found:
                found.append(name)
    return found


def _run(cmd: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        log.warning("command failed: %s (%s)", " ".join(cmd[:2]), exc)
        return None


def docker_available() -> bool:
    if shutil.which("docker") is None:
        return False
    res = _run(["docker", "info"], timeout=15)
    return bool(res and res.returncode == 0)


def image_tag(language: str) -> str:
    return f"kungfu-{language.strip().lower()}:latest"


def image_exists(tag: str) -> bool:
    res = _run(["docker", "image", "inspect", tag], timeout=20)
    return bool(res and res.returncode == 0)


def ensure_image(language: str, sandbox_dir: Optional[Path] = None,
                 build: bool = True) -> tuple[bool, str]:
    """Make sure the language image exists, building it lazily if needed."""
    tag = image_tag(language)
    if image_exists(tag):
        return True, "image present"
    ctx = (sandbox_dir or SANDBOX_DIR) / language.strip().lower()
    if not (ctx / "Dockerfile").exists():
        return False, f"no sandbox/Dockerfile for '{language}' at {ctx}"
    if not build:
        return False, "image missing and build disabled"
    log.info("building sandbox image %s (first use)...", tag)
    res = _run(["docker", "build", "-t", tag, str(ctx)], timeout=900)
    if not res or res.returncode != 0:
        return False, f"image build failed: {(res.stderr if res else 'no output')[-800:]}"
    return True, "image built"


def _unavailable(language: str, reason: str) -> dict:
    return {
        "language": language,
        "available": False,
        "ok": False,
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "diagnostics": "",
        "unknown_symbols": [],
        "image": image_tag(language),
        "reason": reason,
        "duration_s": 0.0,
    }


def run_in_sandbox(language: str, src_dir: Path, cfg: Optional[dict] = None,
                   sandbox_dir: Optional[Path] = None) -> dict:
    """Run the language image against a prepared source directory."""
    cfg = cfg or {}
    dcfg = cfg.get("docker", {}) if isinstance(cfg, dict) else {}
    if not dcfg.get("enabled", True):
        return _unavailable(language, "verification disabled in config (docker.enabled=false)")
    if not docker_available():
        return _unavailable(
            language,
            "Docker is not running; cannot verify. Treat this code as UNVERIFIED — "
            "do not claim it works. Start Docker and re-run kungfu_verify.",
        )
    ok, msg = ensure_image(language, sandbox_dir)
    if not ok:
        return _unavailable(language, f"cannot verify: {msg}")

    tag = image_tag(language)
    timeout = float(dcfg.get("timeout_seconds", 60))
    # A unique --name lets us actually kill the container on timeout. Killing the
    # `docker run` client alone leaves the container running on the daemon (--rm
    # only reaps it once it exits), so the configured timeout would not bound
    # runaway sandboxed code without this.
    name = f"kungfu-{uuid.uuid4().hex[:12]}"
    cmd = [
        "docker", "run", "--rm", "--name", name,
        "--network", str(dcfg.get("network", "none")),
        "--cpus", str(dcfg.get("cpus", "1.0")),
        "--memory", str(dcfg.get("memory", "512m")),
        "--pids-limit", str(dcfg.get("pids_limit", 256)),
        "--security-opt", "no-new-privileges",
        "-v", f"{src_dir}:/src:ro",
        tag,
    ]
    start = time.time()
    res = _run(cmd, timeout=timeout + 10)
    dur = round(time.time() - start, 2)
    if res is None:
        _run(["docker", "rm", "-f", name], timeout=20)  # reap the orphaned container
        return {**_unavailable(language, f"verification process timed out after ~{timeout}s"),
                "duration_s": dur}

    stdout, stderr = res.stdout or "", res.stderr or ""
    diagnostics = (stdout + "\n" + stderr).strip()
    return {
        "language": language,
        "available": True,
        "ok": res.returncode == 0,
        "exit_code": res.returncode,
        "stdout": stdout[-4000:],
        "stderr": stderr[-4000:],
        "diagnostics": diagnostics[-4000:],
        "unknown_symbols": extract_unknown_symbols(diagnostics),
        "image": tag,
        "reason": "" if res.returncode == 0 else "verification failed (see diagnostics)",
        "duration_s": dur,
    }


def verify(language: str, files: dict[str, str], cfg: Optional[dict] = None,
           sandbox_dir: Optional[Path] = None) -> dict:
    """Verify a set of {relative_path: content} files for a language.

    ``files`` should constitute whatever the language image expects (e.g. a
    minimal Gleam project: ``gleam.toml`` + ``src/*.gleam``).
    """
    if not files:
        return _unavailable(language, "no files provided to verify")
    tmp = Path(tempfile.mkdtemp(prefix="kungfu-verify-"))
    try:
        root = tmp.resolve()
        for rel, content in files.items():
            if not isinstance(content, str):
                return _unavailable(language, f"file content must be a string: {rel}")
            dest = tmp / rel
            try:
                dest.resolve().relative_to(root)  # reject any path that escapes tmp
            except ValueError:
                return _unavailable(language, f"unsafe path in files: {rel}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
        return run_in_sandbox(language, tmp, cfg, sandbox_dir)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
