"""Ordered, transactional schema migrations. Forward only: no down migrations."""

from __future__ import annotations

import re
import shutil
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

# shortcut: migrations are read next to this module; switch to importlib.resources if
# Siddhi is ever shipped as a zip/zipapp.
MIGRATIONS_DIR = Path(__file__).parent / "migrations"
MIGRATION_FILE = re.compile(r"^(\d{3})_[a-z0-9_]+\.sql$")
BUSY_TIMEOUT_SECONDS = 5.0


class SchemaTooNew(Exception):
    """The database records a version this application cannot serve."""


class MigrationFailed(Exception):
    """A migration raised; the database stays at the last committed version."""


def connect(path: Path) -> sqlite3.Connection:
    """Open the store with the pragmas it relies on. WAL stays off in this slice."""
    connection = sqlite3.connect(
        path, timeout=BUSY_TIMEOUT_SECONDS, isolation_level=None
    )
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def read_schema_version(connection: sqlite3.Connection) -> int:
    """Recorded version, or 0 when the ledger has not been created yet."""
    exists = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_version'"
    ).fetchone()
    if not exists:
        return 0
    return connection.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] or 0


def discover_migrations(directory: Path = MIGRATIONS_DIR) -> list[tuple[int, Path]]:
    """Migration files as (version, path), ascending. Duplicate versions are an error."""
    found: dict[int, Path] = {}
    for path in sorted(Path(directory).glob("*.sql")):
        match = MIGRATION_FILE.match(path.name)
        if match is None:
            raise ValueError(f"migration file name not recognised: {path.name}")
        version = int(match.group(1))
        if version in found:
            raise ValueError(
                f"duplicate migration version {version}: "
                f"{found[version].name}, {path.name}"
            )
        found[version] = path
    return sorted(found.items())


def apply_migrations(db_path: Path, migrations_dir: Path = MIGRATIONS_DIR) -> int:
    """Apply pending migrations in order and return the resulting version."""
    plan = discover_migrations(migrations_dir)
    supported = plan[-1][0] if plan else 0
    db_path = Path(db_path)
    with closing(connect(db_path)) as connection:
        at = read_schema_version(connection)
        if at > supported:
            raise SchemaTooNew(
                f"database schema version {at} is newer than the supported "
                f"version {supported}; the database was not modified"
            )
        pending = [(version, path) for version, path in plan if version > at]
        if pending and at > 0:
            _copy_before_migration(connection, db_path, at)
        for version, path in pending:
            _apply_one(connection, version, path, at)
            at = version
        return read_schema_version(connection)


def _copy_before_migration(
    connection: sqlite3.Connection, db_path: Path, version: int
) -> None:
    """Keep a recovery copy of the last good version beside the store."""
    journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
    if journal_mode.lower() == "wal":
        raise MigrationFailed(
            "refusing to migrate: a WAL database cannot be copied safely; "
            "checkpoint or back up the store first"
        )
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    # shortcut: copies are never pruned; retention is an open owner decision.
    shutil.copy2(db_path, db_path.with_name(f"{db_path.name}.v{version}.{stamp}.bak"))


def _apply_one(
    connection: sqlite3.Connection, version: int, path: Path, from_version: int
) -> None:
    """Run one migration and record it in the same transaction."""
    statements = _statements(path.read_text(encoding="utf-8"))
    connection.execute("BEGIN IMMEDIATE")
    try:
        for statement in statements:
            connection.execute(statement)
        connection.execute(
            "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
            (version, _utc_now()),
        )
    except BaseException as exc:
        connection.rollback()
        raise MigrationFailed(
            f"migration {path.name} failed; the database remains at "
            f"version {from_version}"
        ) from exc
    else:
        connection.commit()


def _statements(sql: str) -> list[str]:
    """Split a script into complete statements; a ';' inside a string or trigger is safe."""
    statements: list[str] = []
    buffer = ""
    for line in sql.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statements.append(buffer)
            buffer = ""
    if any(
        line.strip() and not line.strip().startswith("--")
        for line in buffer.splitlines()
    ):
        raise ValueError(f"migration script ends mid-statement: {buffer.strip()[:60]}")
    return statements


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
