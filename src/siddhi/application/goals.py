"""Goal operations. Ports are declared here; adapters implement them."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Protocol
from uuid import uuid4

from siddhi.domain.goal import Goal, validate_new_goal

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


class GoalRepository(Protocol):
    def create(self, goal: Goal, changed_fields: list[str]) -> None: ...


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
