"""Inventory operations. Ports are declared here; adapters implement them."""

import base64
import json
from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from siddhi.application.goals import utc_now
from siddhi.domain.project import (
    Inventory,
    SourceError,
    StoredProject,
    validate_inventory,
)

DEFAULT_LIMIT = 25
MAX_LIMIT = 100
LIST_STATES = ("active", "missing", "inaccessible", "all")


class ProjectSource(Protocol):
    def fetch_inventory(self) -> Inventory: ...


class ProjectRepository(Protocol):
    def publish(
        self, run_id: str, started_at: str, finished_at: str, inventory: Inventory
    ) -> dict[str, int]:
        """Store the run and the observed projects in one transaction."""
        ...

    def record_failed_run(
        self, run_id: str, started_at: str, finished_at: str, failure: str
    ) -> None: ...

    def list_page(
        self, state: str, limit: int, after: tuple[str, str] | None
    ) -> list[StoredProject]: ...

    def get(self, project_id: str) -> StoredProject | None: ...

    def latest_run(self) -> "RunSummary | None": ...


class InvalidProject(Exception):
    """A listing or retrieval request the contract does not allow."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(message)
        self.field = field
        self.message = message


class ProjectNotFound(Exception):
    """No stored project uses the requested identifier."""


class SourceNotConfigured(Exception):
    """No inventory source is configured, so nothing was attempted."""


class SourceUnavailable(Exception):
    """The source could not supply a usable observation; the run records why."""

    def __init__(self, category: str, run_id: str) -> None:
        super().__init__(f"the source failed with category {category}")
        self.category = category
        self.run_id = run_id


@dataclass(frozen=True)
class RunSummary:
    run_id: str
    outcome: str
    finished_at: str
    freshness: str | None


@dataclass(frozen=True)
class RunReport:
    run_id: str
    started_at: str
    finished_at: str
    outcome: str
    index_version: str | None
    freshness: str | None
    projects_total: int
    counts: dict[str, int]


@dataclass(frozen=True)
class ProjectPage:
    items: list[StoredProject]
    next_cursor: str | None

    @property
    def has_more(self) -> bool:
        return self.next_cursor is not None


def refresh_inventory(
    repository: ProjectRepository, source: ProjectSource | None
) -> RunReport:
    """Read one complete inventory or record why nothing could be published."""
    if source is None:
        raise SourceNotConfigured()
    run_id = str(uuid4())
    started_at = utc_now()
    try:
        inventory = source.fetch_inventory()
        validate_inventory(inventory)
    except SourceError as exc:
        repository.record_failed_run(run_id, started_at, utc_now(), exc.category)
        raise SourceUnavailable(exc.category, run_id) from None
    finished_at = utc_now()
    counts = repository.publish(run_id, started_at, finished_at, inventory)
    return RunReport(
        run_id=run_id,
        started_at=started_at,
        finished_at=finished_at,
        outcome="completed",
        index_version=inventory.index_version,
        freshness=inventory.freshness,
        projects_total=len(inventory.projects),
        counts=counts,
    )


def list_projects(
    repository: ProjectRepository,
    state: str = "all",
    limit: int = DEFAULT_LIMIT,
    cursor: str | None = None,
) -> ProjectPage:
    """One bounded page, ordered display_name ASC then project_id ASC."""
    if state not in LIST_STATES:
        raise InvalidProject("state", f"state must be one of {', '.join(LIST_STATES)}")
    if not 1 <= limit <= MAX_LIMIT:
        raise InvalidProject("limit", f"limit must be between 1 and {MAX_LIMIT}")
    after = decode_cursor(cursor) if cursor is not None else None
    rows = repository.list_page(state, limit + 1, after)
    items = rows[:limit]
    return ProjectPage(
        items=items,
        next_cursor=encode_cursor(items[-1]) if len(rows) > limit else None,
    )


def get_project(repository: ProjectRepository, project_id: str) -> StoredProject:
    project = repository.get(project_id)
    if project is None:
        raise ProjectNotFound(project_id)
    return project


def encode_cursor(project: StoredProject) -> str:
    """The last row's sort key, opaque to clients (api-contract 3.2)."""
    return _encode({"display_name": project.display_name, "project_id": project.project_id})


def decode_cursor(cursor: str) -> tuple[str, str]:
    key = _decode(cursor)
    display_name = key.get("display_name")
    project_id = key.get("project_id")
    if not isinstance(display_name, str) or not isinstance(project_id, str):
        raise InvalidProject("cursor", "cursor is not valid")
    return display_name, project_id


def _encode(payload: dict[str, object]) -> str:
    return (
        base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode())
        .decode()
        .rstrip("=")
    )


def _decode(cursor: str) -> dict[str, object]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
    except ValueError:
        raise InvalidProject("cursor", "cursor is not valid") from None
    if not isinstance(payload, dict):
        raise InvalidProject("cursor", "cursor is not valid")
    return payload
