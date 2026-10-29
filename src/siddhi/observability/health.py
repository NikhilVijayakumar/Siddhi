"""Health composition: cheap checks that reveal nothing about this machine."""

import sqlite3
from contextlib import closing
from pathlib import Path

from siddhi.adapters.sqlite.project_repository import SqliteProjectRepository
from siddhi.adapters.sqlite.runner import connect, read_schema_version


def health_report(db_path: Path, source_configured: bool = False) -> tuple[dict, int]:
    """The payload and its status code; only reachability, version and the last run are read."""
    try:
        with closing(connect(db_path)) as connection:
            version = read_schema_version(connection)
        integrations = _integrations(db_path, source_configured)
    except sqlite3.Error:
        return (
            {
                "status": "unavailable",
                "schema_version": None,
                "checks": {
                    "service": {"status": "ok"},
                    "database": {"status": "unavailable"},
                    "integrations": {
                        "status": "unavailable",
                        "source": "vyasa",
                        "last_run": None,
                    },
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
                "integrations": integrations,
            },
        },
        200,
    )


def _integrations(db_path: Path, source_configured: bool) -> dict:
    if not source_configured:
        return {"status": "not_configured", "source": "vyasa", "last_run": None}
    run = SqliteProjectRepository(db_path).latest_run()
    return {
        "status": "configured",
        "source": "vyasa",
        "last_run": None
        if run is None
        else {
            "run_id": run.run_id,
            "outcome": run.outcome,
            "finished_at": run.finished_at,
            "freshness": run.freshness,
        },
    }
