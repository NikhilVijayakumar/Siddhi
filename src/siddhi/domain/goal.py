"""Goal fields, allowed values and rules. No HTTP types, no storage."""

from dataclasses import dataclass

OUTCOME_TYPES = ("software", "publication", "research", "internal_investment", "other")
PRIORITIES = ("low", "normal", "high", "critical")
STATUSES = ("active", "archived")
MAX_TITLE_LENGTH = 200

# Null in any of these means "not recorded"; reported as unknown_fields (api-contract 3.1).
UNKNOWN_TRACKED = (
    "description",
    "rationale",
    "priority",
    "target_date",
    "success_criteria",
    "constraints",
    "assumptions",
    "risks",
)


class InvalidGoal(ValueError):
    """A supplied value breaks a domain rule; names the offending field."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(message)
        self.field = field
        self.message = message


@dataclass(frozen=True)
class Goal:
    """A portfolio goal. Optional fields are None when not recorded, never defaulted."""

    id: str
    title: str
    outcome_type: str
    status: str
    description: str | None = None
    rationale: str | None = None
    priority: str | None = None
    target_date: str | None = None
    success_criteria: str | None = None
    constraints: str | None = None
    assumptions: str | None = None
    risks: str | None = None
    revision: int = 0
    created_at: str = ""
    updated_at: str = ""
    archived_at: str | None = None

    @property
    def unknown_fields(self) -> list[str]:
        """Every tracked field currently null; derived so it cannot disagree."""
        return [name for name in UNKNOWN_TRACKED if getattr(self, name) is None]


@dataclass(frozen=True)
class GoalRevision:
    """One append-only record of a change; prior_state holds only the changed fields."""

    goal_id: str
    revision_number: int
    changed_at: str
    actor: str
    changed_fields: list[str]
    prior_state: dict[str, object]
    reason: str | None = None


def validate_new_goal(title: str, outcome_type: str, priority: str | None) -> None:
    """Raise InvalidGoal for the first value that breaks a rule."""
    if not 1 <= len(title.strip()) <= MAX_TITLE_LENGTH:
        raise InvalidGoal(
            "title", f"title must be 1-{MAX_TITLE_LENGTH} characters and not blank"
        )
    if outcome_type not in OUTCOME_TYPES:
        raise InvalidGoal(
            "outcome_type", f"outcome_type must be one of {', '.join(OUTCOME_TYPES)}"
        )
    if priority is not None and priority not in PRIORITIES:
        raise InvalidGoal("priority", f"priority must be one of {', '.join(PRIORITIES)} or null")
