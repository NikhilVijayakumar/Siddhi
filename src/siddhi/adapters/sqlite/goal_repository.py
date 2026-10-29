"""SQLite goal repository: one connection and one transaction per write."""

import json
import sqlite3
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
