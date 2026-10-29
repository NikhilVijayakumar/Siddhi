"""Source inventory vocabulary. Siddhi stores what was observed; it does not judge it."""

from dataclasses import dataclass

STATES = ("active", "missing", "inaccessible")


class SourceError(Exception):
    """A source could not supply a usable observation.

    Only `category` may leave the adapter: source messages can carry local paths,
    so they are never stored, logged or served.
    """

    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category


@dataclass(frozen=True)
class ProjectRecord:
    """One project exactly as the source described it."""

    project_id: str
    display_name: str
    state: str
    identity_status: str
    providers: tuple[str, ...]
    languages: tuple[str, ...]


@dataclass(frozen=True)
class Inventory:
    """One complete inventory read, with the source's own context."""

    projects: list[ProjectRecord]
    index_version: str | None = None
    freshness: str | None = None


@dataclass(frozen=True)
class StoredProject:
    """A project in the current view, with the run that last observed it."""

    project_id: str
    display_name: str
    state: str
    identity_status: str
    providers: tuple[str, ...]
    languages: tuple[str, ...]
    first_observed_at: str
    last_observed_at: str
    freshness: str | None


def validate_inventory(inventory: Inventory) -> None:
    """Reject the whole observation when any project is unusable; never coerce."""
    seen: set[str] = set()
    for record in inventory.projects:
        if not isinstance(record.project_id, str) or not record.project_id.strip():
            raise SourceError("unsupported_contract", "a project has no identifier")
        if not isinstance(record.display_name, str) or not record.display_name.strip():
            raise SourceError("unsupported_contract", "a project has no display name")
        if record.state not in STATES:
            raise SourceError("unsupported_contract", "a project has an unsupported state")
        if not isinstance(record.identity_status, str) or not record.identity_status.strip():
            raise SourceError("unsupported_contract", "a project has no identity status")
        if not all(
            isinstance(value, str) for value in (*record.providers, *record.languages)
        ):
            raise SourceError("unsupported_contract", "a project has a non-text label")
        if record.project_id in seen:
            raise SourceError("unsupported_contract", "a project identifier was repeated")
        seen.add(record.project_id)
