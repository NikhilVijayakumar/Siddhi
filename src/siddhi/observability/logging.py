"""Structured single-line JSON events on stdout; request bodies are never logged."""

import json
import logging
import sys
from datetime import UTC, datetime


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)


def log_event(logger: logging.Logger, event: str, **fields: object) -> None:
    logger.info(
        json.dumps(
            {"at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "event": event} | fields,
            separators=(",", ":"),
            default=str,
        )
    )
