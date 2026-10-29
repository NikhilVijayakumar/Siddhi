"""Health composition: cheap checks that reveal nothing about this machine."""

import sqlite3
from contextlib import closing
from pathlib import Path

from siddhi.adapters.sqlite.runner import connect, read_schema_version

INTEGRATIONS = {"status": "not_configured", "detail": "no source adapters in this change"}


def health_report(db_path: Path) -> tuple[dict, int]:
    """The payload and its status code; only reachability and version are read."""
    try:
        with closing(connect(db_path)) as connection:
            version = read_schema_version(connection)
    except sqlite3.Error:
        return (
            {
                "status": "unavailable",
                "schema_version": None,
                "checks": {
                    "service": {"status": "ok"},
                    "database": {"status": "unavailable"},
                    "integrations": dict(INTEGRATIONS),
                },
            },
            503,
        )
    return (
        {
            "status": "ok",
            "schema_version": version,
            "checks": {
                "service": {"status": "ok"},
                "database": {"status": "ok", "schema_version": version},
                "integrations": dict(INTEGRATIONS),
            },
        },
        200,
    )
