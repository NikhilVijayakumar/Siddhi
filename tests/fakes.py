"""Test doubles for source adapters. The suite never starts Vyasa."""

from siddhi.domain.project import Inventory, ProjectRecord


class FakeSource:
    """Returns each supplied result once, then keeps returning the last one.

    An `Exception` result is raised instead of returned, which is how adapter
    failures reach the application.
    """

    def __init__(self, *results: Inventory | Exception) -> None:
        self._results = list(results)
        self.calls = 0

    def fetch_inventory(self) -> Inventory:
        index = min(self.calls, len(self._results) - 1)
        self.calls += 1
        result = self._results[index]
        if isinstance(result, Exception):
            raise result
        return result


def project(
    project_id: str = "e620f8eda2274e9397a3f7430f22c012",
    display_name: str = "Siddhi",
    state: str = "active",
    identity_status: str = "resolved",
    providers: tuple[str, ...] = ("github",),
    languages: tuple[str, ...] = ("Python",),
) -> ProjectRecord:
    return ProjectRecord(
        project_id=project_id,
        display_name=display_name,
        state=state,
        identity_status=identity_status,
        providers=providers,
        languages=languages,
    )


def inventory(
    *projects: ProjectRecord, freshness: str | None = "current", index_version: str | None = "11"
) -> Inventory:
    return Inventory(projects=list(projects), index_version=index_version, freshness=freshness)
