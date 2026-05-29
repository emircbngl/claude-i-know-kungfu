"""Logging helper.

CRITICAL: this server speaks JSON-RPC over stdio. Anything written to stdout
corrupts the protocol stream. All diagnostics must go to stderr — never use
bare print() anywhere in the package.
"""

from __future__ import annotations

import logging
import sys

_CONFIGURED = False


def get_logger(name: str = "kungfu") -> logging.Logger:
    global _CONFIGURED
    logger = logging.getLogger(name)
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("[kungfu] %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        _CONFIGURED = True
    return logger
