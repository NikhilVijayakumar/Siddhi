"""SQLite goal repository: one connection and one transaction per write."""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

from siddhi.adapters.sqlite.runner import connect
from siddhi.domain.goal import Goal

COLUMNS = (
    "id",
    "title",
    "outcome_type",
    "status",
    "description",
    "rationale",
    "priority",
    "target_date",
    "success_criteria",
    "constraints",
    "assumptions",
    "risks",
    "revision",
    "created_at",
    "updated_at",
    "archived_at",
)


class SqliteGoalRepository:
    """shortcut: connects per operation; pool only if contention becomes real."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def create(self, goal: Goal, changed_fields: list[str]) -> None:
        """Insert the goal and its creation revision together or not at all."""
        connection = connect(self._db_path)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                f"INSERT INTO goals ({', '.join(COLUMNS)}) "
                f"VALUES ({', '.join('?' * len(COLUMNS))})",
                tuple(getattr(goal, column) for column in COLUMNS),
            )
            connection.execute(
                "INSERT INTO goal_revisions "
                "(goal_id, revision_number, changed_at, actor, reason, "
                " changed_fields, prior_state) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (goal.id, 0, goal.created_at, "owner", None, json.dumps(changed_fields), "{}"),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def get(self, goal_id: str) -> Goal | None:
        with closing(connect(self._db_path)) as connection:
            row = connection.execute(
                f"SELECT {', '.join(COLUMNS)} FROM goals WHERE id = ?", (goal_id,)
            ).fetchone()
        return None if row is None else _to_goal(row)

    def list_page(
        self, status: str, limit: int, after: tuple[str, str] | None
    ) -> list[Goal]:
        """One page of the (created_at DESC, id ASC) keyset; `after` is the last row's key."""
        sql = f"SELECT {', '.join(COLUMNS)} FROM goals"
        clauses: list[str] = []
        parameters: list[object] = []
        if status != "all":
            clauses.append("status = ?")
            parameters.append(status)
        if after is not None:
            clauses.append("(created_at < ? OR (created_at = ? AND id > ?))")
            parameters.extend([after[0], after[0], after[1]])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC, id ASC LIMIT ?"
        parameters.append(limit)
        with closing(connect(self._db_path)) as connection:
            return [_to_goal(row) for row in connection.execute(sql, parameters)]


def _to_goal(row: sqlite3.Row | tuple) -> Goal:
    return Goal(**dict(zip(COLUMNS, row)))
