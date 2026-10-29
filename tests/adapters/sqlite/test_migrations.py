"""Migration runner: fresh baseline, ordered upgrade, fail-closed behaviour."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from siddhi.adapters.sqlite.runner import (
    MIGRATIONS_DIR,
    MigrationFailed,
    SchemaTooNew,
    apply_migrations,
    connect,
    read_schema_version,
)

BASELINE = (MIGRATIONS_DIR / "001_initial_schema.sql").read_text(encoding="utf-8")
GOAL_ROW = """INSERT INTO goals (id, title, outcome_type, status, created_at, updated_at)
              VALUES ('g1', 'Kept', 'software', 'active', '2026-10-29T00:00:00Z',
                      '2026-10-29T00:00:00Z')"""


def write_migrations(directory: Path, migrations: dict[str, str]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for name, sql in migrations.items():
        (directory / name).write_text(sql, encoding="utf-8")
    return directory


def tables(path: Path) -> set[str]:
    with closing(connect(path)) as connection:
        return {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }


def test_fresh_database_is_created_at_the_latest_version(db_path):
    assert not db_path.exists()

    assert apply_migrations(db_path) == 2

    assert {"schema_version", "goals", "goal_revisions", "ingestion_runs", "projects"} <= tables(
        db_path
    )
    with closing(sqlite3.connect(db_path)) as connection:
        ledger = connection.execute(
            "SELECT version, applied_at FROM schema_version ORDER BY version"
        ).fetchall()
    assert [version for version, _ in ledger] == [1, 2]
    assert all(applied_at.endswith("Z") for _, applied_at in ledger)


def test_no_backup_is_taken_when_there_is_nothing_to_lose(db_path):
    apply_migrations(db_path)

    assert list(db_path.parent.glob("*.bak")) == []


def test_newer_database_is_refused_naming_both_versions(db_path):
    apply_migrations(db_path)
    with closing(connect(db_path)) as connection, connection:
        connection.execute(
            "INSERT INTO schema_version (version, applied_at) VALUES (99, '2099-01-01T00:00:00Z')"
        )

    with pytest.raises(SchemaTooNew) as refused:
        apply_migrations(db_path)

    assert "99" in str(refused.value)
    assert "2" in str(refused.value)
    with closing(sqlite3.connect(db_path)) as connection:
        assert connection.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] == 99
        assert connection.execute("SELECT COUNT(*) FROM goals").fetchone()[0] == 0


def test_failed_migration_leaves_prior_version_and_rows_readable(db_path, tmp_path):
    migrations = tmp_path / "migrations"
    write_migrations(migrations, {"001_initial_schema.sql": BASELINE})
    assert apply_migrations(db_path, migrations) == 1
    with closing(connect(db_path)) as connection, connection:
        connection.execute(GOAL_ROW)

    write_migrations(
        migrations,
        {
            "002_broken.sql": "CREATE TABLE half (x INTEGER);\nTHIS IS NOT SQL;",
            "003_later.sql": "CREATE TABLE never (x INTEGER);",
        },
    )
    with pytest.raises(MigrationFailed) as failed:
        apply_migrations(db_path, migrations)

    assert "002_broken.sql" in str(failed.value)
    with closing(connect(db_path)) as connection:
        assert read_schema_version(connection) == 1
    assert "half" not in tables(db_path)
    assert "never" not in tables(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        assert connection.execute("SELECT title FROM goals").fetchone()[0] == "Kept"


def test_duplicate_migration_versions_are_rejected(db_path, tmp_path):
    migrations = write_migrations(
        tmp_path / "migrations",
        {
            "001_first.sql": "CREATE TABLE first (x INTEGER);",
            "001_second.sql": "CREATE TABLE second (x INTEGER);",
        },
    )

    with pytest.raises(ValueError):
        apply_migrations(db_path, migrations)


def test_backup_is_kept_before_upgrading(db_path, tmp_path):
    migrations = tmp_path / "migrations"
    write_migrations(migrations, {"001_initial_schema.sql": BASELINE})
    assert apply_migrations(db_path, migrations) == 1

    write_migrations(migrations, {"002_extra.sql": "CREATE TABLE extra (x INTEGER);"})
    assert apply_migrations(db_path, migrations) == 2

    backups = sorted(db_path.parent.glob(f"{db_path.name}.v1.*.bak"))
    assert len(backups) == 1, backups
    with closing(sqlite3.connect(backups[0])) as connection:
        assert connection.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] == 1


def test_connect_enables_foreign_keys_and_leaves_wal_off(db_path):
    with closing(connect(db_path)) as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert connection.execute("PRAGMA journal_mode").fetchone()[0].lower() != "wal"
