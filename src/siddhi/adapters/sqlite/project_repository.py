"""SQLite project projection: one transaction publishes a run and its projects."""

import json
from contextlib import closing
from pathlib import Path

from siddhi.adapters.sqlite.runner import connect
from siddhi.application.inventory import RunSummary
from siddhi.domain.project import Inventory, ProjectRecord, StoredProject

READ_COLUMNS = (
    "p.project_id, p.display_name, p.state, p.identity_status, p.providers,"
    " p.languages, p.first_observed_at, p.last_observed_at, r.freshness"
)
FROM_PROJECTS = "FROM projects p JOIN ingestion_runs r ON r.id = p.last_run_id"


class SqliteProjectRepository:
    """shortcut: connects per operation; pool only if contention becomes real."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def publish(
        self, run_id: str, started_at: str, finished_at: str, inventory: Inventory
    ) -> dict[str, int]:
        """Compare against the current view, then write rows and the run atomically."""
        desired = {record.project_id: record for record in inventory.projects}
        connection = connect(self._db_path)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO ingestion_runs (id, source, started_at, finished_at,"
                " outcome, failure, index_version, freshness, projects_total)"
                " VALUES (?, 'vyasa', ?, ?, 'completed', NULL, ?, ?, ?)",
                (
                    run_id,
                    started_at,
                    finished_at,
                    inventory.index_version,
                    inventory.freshness,
                    len(inventory.projects),
                ),
            )
            current = {
                row[0]: row
                for row in connection.execute(
                    "SELECT project_id, display_name, state, identity_status,"
                    " providers, languages FROM projects"
                )
            }
            counts = {"added": 0, "updated": 0, "removed": 0, "unchanged": 0}
            for project_id, record in desired.items():
                existing = current.get(project_id)
                if existing is None:
                    connection.execute(
                        "INSERT INTO projects (project_id, display_name, state,"
                        " identity_status, providers, languages, first_observed_at,"
                        " last_observed_at, last_run_id)"
                        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            project_id,
                            record.display_name,
                            record.state,
                            record.identity_status,
                            _labels(record.providers),
                            _labels(record.languages),
                            started_at,
                            started_at,
                            run_id,
                        ),
                    )
                    counts["added"] += 1
                elif _changed(existing, record):
                    connection.execute(
                        "UPDATE projects SET display_name = ?, state = ?,"
                        " identity_status = ?, providers = ?, languages = ?,"
                        " last_observed_at = ?, last_run_id = ? WHERE project_id = ?",
                        (
                            record.display_name,
                            record.state,
                            record.identity_status,
                            _labels(record.providers),
                            _labels(record.languages),
                            started_at,
                            run_id,
                            project_id,
                        ),
                    )
                    counts["updated"] += 1
                else:
                    connection.execute(
                        "UPDATE projects SET last_observed_at = ?, last_run_id = ?"
                        " WHERE project_id = ?",
                        (started_at, run_id, project_id),
                    )
                    counts["unchanged"] += 1
            for project_id in set(current) - set(desired):
                connection.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
                counts["removed"] += 1
            connection.execute(
                "UPDATE ingestion_runs SET added = ?, updated = ?, removed = ?,"
                " unchanged = ? WHERE id = ?",
                (
                    counts["added"],
                    counts["updated"],
                    counts["removed"],
                    counts["unchanged"],
                    run_id,
                ),
            )
            connection.commit()
            return counts
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def record_failed_run(
        self, run_id: str, started_at: str, finished_at: str, failure: str
    ) -> None:
        """One run row and nothing else: a partial read never changes the view."""
        connection = connect(self._db_path)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO ingestion_runs (id, source, started_at, finished_at,"
                " outcome, failure) VALUES (?, 'vyasa', ?, ?, 'failed', ?)",
                (run_id, started_at, finished_at, failure),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def list_page(
        self, state: str, limit: int, after: tuple[str, str] | None
    ) -> list[StoredProject]:
        """One page of the (display_name ASC, project_id ASC) keyset."""
        sql = f"SELECT {READ_COLUMNS} {FROM_PROJECTS}"
        clauses: list[str] = []
        parameters: list[object] = []
        if state != "all":
            clauses.append("p.state = ?")
            parameters.append(state)
        if after is not None:
            clauses.append(
                "(p.display_name > ? OR (p.display_name = ? AND p.project_id > ?))"
            )
            parameters.extend([after[0], after[0], after[1]])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY p.display_name ASC, p.project_id ASC LIMIT ?"
        parameters.append(limit)
        with closing(connect(self._db_path)) as connection:
            return [_to_project(row) for row in connection.execute(sql, parameters)]

    def get(self, project_id: str) -> StoredProject | None:
        with closing(connect(self._db_path)) as connection:
            row = connection.execute(
                f"SELECT {READ_COLUMNS} {FROM_PROJECTS} WHERE p.project_id = ?",
                (project_id,),
            ).fetchone()
        return None if row is None else _to_project(row)

    def latest_run(self) -> RunSummary | None:
        with closing(connect(self._db_path)) as connection:
            row = connection.execute(
                "SELECT id, outcome, finished_at, freshness FROM ingestion_runs"
                " ORDER BY started_at DESC, id DESC LIMIT 1"
            ).fetchone()
        if row is None:
            return None
        return RunSummary(run_id=row[0], outcome=row[1], finished_at=row[2], freshness=row[3])


def _labels(values: tuple[str, ...]) -> str:
    return json.dumps(list(values), separators=(",", ":"))


def _changed(existing: tuple, record: ProjectRecord) -> bool:
    _, display_name, state, identity_status, providers, languages = existing
    return (display_name, state, identity_status, providers, languages) != (
        record.display_name,
        record.state,
        record.identity_status,
        _labels(record.providers),
        _labels(record.languages),
    )


def _to_project(row: tuple) -> StoredProject:
    project_id, display_name, state, identity_status, providers, languages = row[:6]
    return StoredProject(
        project_id=project_id,
        display_name=display_name,
        state=state,
        identity_status=identity_status,
        providers=tuple(json.loads(providers)),
        languages=tuple(json.loads(languages)),
        first_observed_at=row[6],
        last_observed_at=row[7],
        freshness=row[8],
    )
