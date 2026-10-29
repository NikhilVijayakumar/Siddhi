"""/health and request logging: truthful, cheap and free of local detail."""

import logging

import pytest

from tests.fakes import FakeSource, inventory, project

from siddhi.domain.project import SourceError


def test_health_reports_service_database_and_integrations(client):
    response = client.get("/health")

    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "ok"
    assert health["schema_version"] == 2
    assert health["checks"]["service"] == {"status": "ok"}
    assert health["checks"]["database"] == {"status": "ok", "schema_version": 2}
    assert health["checks"]["integrations"] == {
        "status": "not_configured",
        "source": "vyasa",
        "last_run": None,
    }


def test_health_reports_a_configured_source_before_any_run(make_client):
    with make_client(FakeSource(inventory())) as client:
        integrations = client.get("/health").json()["checks"]["integrations"]

    assert integrations == {"status": "configured", "source": "vyasa", "last_run": None}


def test_health_reports_the_last_completed_run(make_client):
    with make_client(FakeSource(inventory(project()))) as client:
        report = client.post("/ingestion/vyasa/refresh").json()
        integrations = client.get("/health").json()["checks"]["integrations"]

    assert integrations == {
        "status": "configured",
        "source": "vyasa",
        "last_run": {
            "run_id": report["run_id"],
            "outcome": "completed",
            "finished_at": report["finished_at"],
            "freshness": "current",
        },
    }


def test_health_reports_a_failed_last_run_and_stays_usable(make_client):
    with make_client(FakeSource(SourceError("tool_error", "no index"))) as client:
        client.post("/ingestion/vyasa/refresh")
        response = client.get("/health")

    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "ok"
    assert health["checks"]["database"]["status"] == "ok"
    assert health["checks"]["integrations"]["last_run"]["outcome"] == "failed"
    assert health["checks"]["integrations"]["last_run"]["freshness"] is None


def test_health_reveals_neither_the_executable_nor_the_source_message(make_client, tmp_path):
    executable = str(tmp_path / "secret" / "vyasa-mcp.exe")

    with make_client(
        FakeSource(SourceError("connection_failed", f"{executable} refused to start"))
    ) as client:
        client.post("/ingestion/vyasa/refresh")
        body = client.get("/health").text

    assert executable not in body
    assert "refused to start" not in body
    assert "secret" not in body.lower()


def test_unusable_database_is_unavailable_not_a_crash(client, db_path):
    db_path.unlink()
    db_path.mkdir()

    response = client.get("/health")

    assert response.status_code == 503
    health = response.json()
    assert health["status"] == "unavailable"
    assert health["checks"]["database"] == {"status": "unavailable"}
    assert health["checks"]["service"] == {"status": "ok"}


def test_health_and_errors_reveal_neither_path_nor_credentials(client, db_path):
    created = client.post("/goals", json={"title": "Hidden", "outcome_type": "software"})
    bodies = [client.get("/health").text, created.text, client.get("/goals/nope").text]

    for body in bodies:
        assert str(db_path) not in body
        assert str(db_path.parent) not in body
        for word in ("password", "secret", "token", "credential"):
            assert word not in body.lower()


def test_a_request_is_logged_with_its_correlation_id_and_no_body(client, caplog):
    with caplog.at_level(logging.INFO, logger="siddhi"):
        response = client.post(
            "/goals", json={"title": "Never log this title", "outcome_type": "software"}
        )

    assert caplog.records, "no request log was emitted"
    logged = " ".join(record.getMessage() for record in caplog.records)
    assert response.headers["X-Correlation-Id"] in logged
    assert "Never log this title" not in logged
