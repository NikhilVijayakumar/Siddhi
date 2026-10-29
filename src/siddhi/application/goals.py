"""Goal operations. Ports are declared here; adapters implement them."""

import base64
import json
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime
from typing import Protocol
from uuid import uuid4

from siddhi.domain.goal import Goal, GoalRevision, InvalidGoal, validate_new_goal

# Every field the owner can supply at creation, in contract order.
SUPPLIABLE_FIELDS = (
    "title",
    "outcome_type",
    "description",
    "rationale",
    "priority",
    "target_date",
    "success_criteria",
    "constraints",
    "assumptions",
    "risks",
)

LIST_STATUSES = ("active", "archived", "all")
DEFAULT_LIMIT = 25
MAX_LIMIT = 100


class GoalRepository(Protocol):
    def create(self, goal: Goal, changed_fields: list[str]) -> None: ...

    def get(self, goal_id: str) -> Goal | None: ...

    def list_page(
        self, status: str, limit: int, after: tuple[str, str] | None
    ) -> list[Goal]: ...

    def revise(
        self,
        goal: Goal,
        changed_fields: list[str],
        prior_state: dict[str, object],
        reason: str | None,
    ) -> bool:
        """Store the revision and the new row atomically; False if the row moved on."""
        ...

    def revisions(
        self, goal_id: str, limit: int, after_number: int | None
    ) -> list[GoalRevision]: ...


class GoalNotFound(Exception):
    """No goal uses the requested identifier."""


class GoalConflict(Exception):
    """The goal changed since the caller last read it."""

    def __init__(self, current_revision: int) -> None:
        super().__init__(
            f"expected_revision does not match the current revision {current_revision}"
        )
        self.current_revision = current_revision


@dataclass(frozen=True)
class GoalPage:
    items: list[Goal]
    next_cursor: str | None

    @property
    def has_more(self) -> bool:
        return self.next_cursor is not None


@dataclass(frozen=True)
class RevisionPage:
    items: list[GoalRevision]
    next_cursor: str | None

    @property
    def has_more(self) -> bool:
        return self.next_cursor is not None


@dataclass(frozen=True)
class NewGoal:
    """A validated-by-nobody-yet create request; `create_goal` does the checking."""

    title: str
    outcome_type: str
    description: str | None = None
    rationale: str | None = None
    priority: str | None = None
    target_date: date | None = None
    success_criteria: str | None = None
    constraints: str | None = None
    assumptions: str | None = None
    risks: str | None = None


def create_goal(repository: GoalRepository, request: NewGoal) -> Goal:
    """Validate, then store the goal and its creation revision in one transaction."""
    validate_new_goal(request.title, request.outcome_type, request.priority)
    now = utc_now()
    goal = Goal(
        id=str(uuid4()),
        title=request.title,
        outcome_type=request.outcome_type,
        status="active",
        description=request.description,
        rationale=request.rationale,
        priority=request.priority,
        target_date=request.target_date.isoformat() if request.target_date else None,
        success_criteria=request.success_criteria,
        constraints=request.constraints,
        assumptions=request.assumptions,
        risks=request.risks,
        revision=0,
        created_at=now,
        updated_at=now,
        archived_at=None,
    )
    supplied = [name for name in SUPPLIABLE_FIELDS if getattr(goal, name) is not None]
    repository.create(goal, supplied)
    return goal


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_goal(repository: GoalRepository, goal_id: str) -> Goal:
    goal = repository.get(goal_id)
    if goal is None:
        raise GoalNotFound(goal_id)
    return goal


def list_goals(
    repository: GoalRepository,
    status: str = "active",
    limit: int = DEFAULT_LIMIT,
    cursor: str | None = None,
) -> GoalPage:
    """One bounded page, ordered created_at DESC then id ASC."""
    if status not in LIST_STATUSES:
        raise InvalidGoal("status", f"status must be one of {', '.join(LIST_STATUSES)}")
    if not 1 <= limit <= MAX_LIMIT:
        raise InvalidGoal("limit", f"limit must be between 1 and {MAX_LIMIT}")
    after = decode_cursor(cursor) if cursor is not None else None
    rows = repository.list_page(status, limit + 1, after)
    items = rows[:limit]
    return GoalPage(
        items=items, next_cursor=encode_cursor(items[-1]) if len(rows) > limit else None
    )


def encode_cursor(goal: Goal) -> str:
    """The last row's sort key, opaque to clients (api-contract 3.2)."""
    return _encode({"created_at": goal.created_at, "id": goal.id})


def decode_cursor(cursor: str) -> tuple[str, str]:
    key = _decode(cursor)
    try:
        return str(key["created_at"]), str(key["id"])
    except KeyError:
        raise InvalidGoal("cursor", "cursor is not valid") from None


def encode_revision_cursor(revision_number: int) -> str:
    return _encode({"revision_number": revision_number})


def decode_revision_cursor(cursor: str) -> int:
    key = _decode(cursor)
    try:
        return int(key["revision_number"])
    except (KeyError, TypeError, ValueError):
        raise InvalidGoal("cursor", "cursor is not valid") from None


def revise_goal(
    repository: GoalRepository,
    goal_id: str,
    changes: dict[str, object],
    reason: str | None = None,
    expected_revision: int | None = None,
) -> Goal:
    """Apply the supplied fields, appending a revision only for values that changed."""
    goal = get_goal(repository, goal_id)
    if expected_revision is not None and expected_revision != goal.revision:
        raise GoalConflict(goal.revision)
    supplied = {name: value for name, value in changes.items() if name in SUPPLIABLE_FIELDS}
    validate_new_goal(
        supplied.get("title", goal.title),  # type: ignore[arg-type]
        supplied.get("outcome_type", goal.outcome_type),  # type: ignore[arg-type]
        supplied.get("priority", goal.priority),  # type: ignore[arg-type]
    )
    changed = [
        name
        for name in SUPPLIABLE_FIELDS
        if name in supplied and supplied[name] != getattr(goal, name)
    ]
    if not changed:
        return goal
    prior_state = {name: getattr(goal, name) for name in changed}
    revised = replace(
        goal,
        revision=goal.revision + 1,
        updated_at=utc_now(),
        **{name: supplied[name] for name in changed},
    )
    if not repository.revise(revised, changed, prior_state, reason):
        raise GoalConflict(get_goal(repository, goal_id).revision)
    return revised


def list_revisions(
    repository: GoalRepository,
    goal_id: str,
    limit: int = DEFAULT_LIMIT,
    cursor: str | None = None,
) -> RevisionPage:
    """One bounded page of history, newest revision first."""
    if not 1 <= limit <= MAX_LIMIT:
        raise InvalidGoal("limit", f"limit must be between 1 and {MAX_LIMIT}")
    get_goal(repository, goal_id)
    after = decode_revision_cursor(cursor) if cursor is not None else None
    rows = repository.revisions(goal_id, limit + 1, after)
    items = rows[:limit]
    return RevisionPage(
        items=items,
        next_cursor=(
            encode_revision_cursor(items[-1].revision_number) if len(rows) > limit else None
        ),
    )


def _encode(payload: dict[str, object]) -> str:
    return base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode()
    ).decode().rstrip("=")


def _decode(cursor: str) -> dict[str, object]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
    except ValueError:
        raise InvalidGoal("cursor", "cursor is not valid") from None
    if not isinstance(payload, dict):
        raise InvalidGoal("cursor", "cursor is not valid")
    return payload
