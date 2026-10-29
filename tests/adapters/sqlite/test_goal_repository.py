"""The repository's own lost-update guard, without an HTTP client in the way."""

from dataclasses import replace

from siddhi.adapters.sqlite.goal_repository import SqliteGoalRepository
from siddhi.adapters.sqlite.runner import apply_migrations
from siddhi.domain.goal import Goal


def goal(revision: int = 0, title: str = "Original") -> Goal:
    return Goal(
        id="6f1c0a1e-3d5e-4a2b-9d4f-0c1b2a3d4e5f",
        title=title,
        outcome_type="software",
        status="active",
        revision=revision,
        created_at="2026-10-29T12:00:00Z",
        updated_at="2026-10-29T12:00:00Z",
    )


def test_second_write_from_the_same_snapshot_is_refused(db_path):
    apply_migrations(db_path)
    repository = SqliteGoalRepository(db_path)
    repository.create(goal(), ["title", "outcome_type"])

    first = replace(goal(), revision=1, title="Winner")
    assert repository.revise(first, ["title"], {"title": "Original"}, None) is True

    stale = replace(goal(), revision=1, title="Loser")
    assert repository.revise(stale, ["title"], {"title": "Original"}, None) is False

    assert repository.get(goal().id).title == "Winner"
    assert [r.revision_number for r in repository.revisions(goal().id, 10, None)] == [1, 0]
