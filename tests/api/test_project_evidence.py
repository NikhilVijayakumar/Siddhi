"""Project evidence reads: checkout-level retrieval over the source."""

from siddhi.domain.project import SourceError

from tests.fakes import FakeSource, inventory, project

REFRESH = "/ingestion/vyasa/refresh"
PROJECT_ID = "e620f8eda2274e9397a3f7430f22c012"


def detail(project_id: str = PROJECT_ID) -> dict:
    return {
        "project_id": project_id,
        "checkouts": [
            {
                "remote": "https://github.com/owner/repo",
                "status": "clean",
                "observed_at": "2026-10-29T12:00:00Z",
            }
        ],
        "languages": ["Python"],
        "markers": ["implementation:complete"],
        "frameworks": ["fastapi"],
    }


def test_a_stored_project_returns_checkout_evidence(make_client):
    source = FakeSource(
        inventory(project()),
        details=(detail(),),
    )

    with make_client(source) as client:
        client.post(REFRESH)
        response = client.get(f"/projects/{PROJECT_ID}/evidence")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "project_id": PROJECT_ID,
        "freshness": "current",
        "checkouts": [
            {
                "remote": "https://github.com/owner/repo",
                "status": "clean",
                "observed_at": "2026-10-29T12:00:00Z",
            }
        ],
        "languages": ["Python"],
        "markers": ["implementation:complete"],
        "frameworks": ["fastapi"],
    }


def test_a_failed_evidence_read_maps_a_source_failure_and_keeps_stored_data(make_client, db_path):
    source = FakeSource(
        inventory(project()),
        details=(SourceError("tool_error", "no index"),),
    )

    with make_client(source) as client:
        client.post(REFRESH)
        before_runs = client.get("/health").json()["checks"]["integrations"]["last_run"]

        response = client.get(f"/projects/{PROJECT_ID}/evidence")

    assert response.status_code == 503, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("unavailable", "source_unavailable")
    assert error["details"] == [{"run_id": None, "failure": "tool_error"}]
    assert client.get(f"/projects/{PROJECT_ID}").status_code == 200
    assert client.get("/health").json()["checks"]["integrations"]["last_run"] == before_runs


def test_an_evidence_read_without_a_configured_source_reports_it(make_client):
    source = FakeSource(inventory(project()))

    with make_client(source) as configured:
        configured.post(REFRESH)

    with make_client(None) as client:
        response = client.get(f"/projects/{PROJECT_ID}/evidence")

    assert response.status_code == 503, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("unavailable", "source_not_configured")
    assert error["details"] == []
    assert client.get(f"/projects/{PROJECT_ID}").status_code == 200


def test_an_unknown_stored_project_is_not_found(make_client):
    source = FakeSource(inventory(project()))

    with make_client(source) as client:
        response = client.get("/projects/unknown-project-id/evidence")

    assert response.status_code == 404, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("not_found", "project_not_found")
