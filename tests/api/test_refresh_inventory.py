"""Refresh contract: a completed read publishes, a failed one changes nothing."""

import sqlite3

from siddhi.domain.project import SourceError

from tests.fakes import FakeSource, inventory, project

REFRESH = "/ingestion/vyasa/refresh"


def rows(db_path, sql, parameters=()):
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(sql, parameters)]


def test_a_completed_refresh_stores_every_project_and_reports_the_run(make_client, db_path):
    source = FakeSource(
        inventory(
            project(project_id="a", display_name="Alpha"),
            project(project_id="b", display_name="Beta", state="missing"),
        )
    )

    with make_client(source) as client:
        response = client.post(REFRESH)

    assert response.status_code == 200, response.text
    report = response.json()
    assert report["source"] == "vyasa"
    assert report["outcome"] == "completed"
    assert report["projects_total"] == 2
    assert report["counts"] == {"added": 2, "updated": 0, "removed": 0, "unchanged": 0}
    assert (report["index_version"], report["freshness"]) == ("11", "current")
    assert report["started_at"].endswith("Z")
    assert report["finished_at"].endswith("Z")

    stored = rows(
        db_path,
        "SELECT project_id, display_name, state, first_observed_at FROM projects"
        " ORDER BY project_id",
    )
    assert [(row["project_id"], row["state"]) for row in stored] == [
        ("a", "active"),
        ("b", "missing"),
    ]
    assert stored[0]["first_observed_at"] == report["started_at"]
    assert rows(db_path, "SELECT outcome, failure, projects_total FROM ingestion_runs") == [
        {"outcome": "completed", "failure": None, "projects_total": 2}
    ]


def test_a_repeat_unchanged_refresh_keeps_the_first_observation_time(make_client, db_path):
    source = FakeSource(
        inventory(project(project_id="a", display_name="Alpha")),
        inventory(project(project_id="a", display_name="Alpha")),
    )

    with make_client(source) as client:
        first = client.post(REFRESH).json()
        second = client.post(REFRESH).json()

    assert second["counts"] == {"added": 0, "updated": 0, "removed": 0, "unchanged": 1}
    stored = rows(db_path, "SELECT first_observed_at, last_observed_at FROM projects")
    assert len(stored) == 1
    assert stored[0]["first_observed_at"] == first["started_at"]
    assert stored[0]["last_observed_at"] == second["started_at"]


def test_changed_added_and_absent_projects_are_counted(make_client, db_path):
    source = FakeSource(
        inventory(project(project_id="a", display_name="Alpha"), project(project_id="b", display_name="Beta")),
        inventory(project(project_id="a", display_name="Alpha renamed"), project(project_id="c", display_name="Gamma")),
    )

    with make_client(source) as client:
        client.post(REFRESH)
        second = client.post(REFRESH).json()

    assert second["counts"] == {"added": 1, "updated": 1, "removed": 1, "unchanged": 0}
    stored = rows(db_path, "SELECT project_id, display_name FROM projects ORDER BY project_id")
    assert stored == [
        {"project_id": "a", "display_name": "Alpha renamed"},
        {"project_id": "c", "display_name": "Gamma"},
    ]


def test_a_failed_refresh_keeps_inventory_and_goals_and_records_the_failure(make_client, db_path):
    source = FakeSource(
        inventory(project(project_id="a", display_name="Alpha")),
        SourceError("connection_failed", r"E:\secret\vyasa-mcp.exe could not start"),
    )

    with make_client(source) as client:
        client.post(REFRESH)
        goal = client.post(
            "/goals", json={"title": "Ship inventory", "outcome_type": "software"}
        ).json()
        failed = client.post(REFRESH)

        assert failed.status_code == 503, failed.text
        error = failed.json()["error"]
        assert (error["category"], error["code"]) == ("unavailable", "source_unavailable")
        failed_run = rows(db_path, "SELECT id FROM ingestion_runs WHERE outcome = 'failed'")
        assert error["details"] == [
            {"run_id": failed_run[0]["id"], "failure": "connection_failed"}
        ]
        assert "secret" not in failed.text
        assert [item["id"] for item in client.get("/goals").json()["items"]] == [goal["id"]]

    assert [row["project_id"] for row in rows(db_path, "SELECT project_id FROM projects")] == ["a"]
    runs = rows(
        db_path,
        "SELECT outcome, failure, added, updated, removed, unchanged"
        " FROM ingestion_runs ORDER BY rowid",
    )
    assert [row["outcome"] for row in runs] == ["completed", "failed"]
    assert runs[1] == {
        "outcome": "failed",
        "failure": "connection_failed",
        "added": 0,
        "updated": 0,
        "removed": 0,
        "unchanged": 0,
    }


def test_a_cross_site_refresh_is_refused_before_the_source_runs(make_client, db_path):
    source = FakeSource(inventory(project()))

    with make_client(source) as client:
        response = client.post(REFRESH, headers={"Origin": "https://example.test"})

    assert response.status_code == 403, response.text
    assert response.json()["error"]["code"] == "cross_site_request"
    assert source.calls == 0
    assert rows(db_path, "SELECT id FROM ingestion_runs") == []


def test_a_loopback_origin_is_this_machine(make_client):
    with make_client(FakeSource(inventory(project()))) as client:
        response = client.post(REFRESH, headers={"Origin": "http://127.0.0.1:8000"})

    assert response.status_code == 200, response.text


def test_a_refresh_body_is_refused_instead_of_ignored(make_client):
    with make_client(FakeSource(inventory())) as client:
        response = client.post(REFRESH, json={"unexpected": 1})

    assert response.status_code == 422, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("validation", "invalid_field")
    assert error["field"] == "unexpected"


def test_refresh_without_a_configured_source_reports_it_and_writes_no_run(make_client, db_path):
    with make_client(None) as client:
        response = client.post(REFRESH)

    assert response.status_code == 503, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("unavailable", "source_not_configured")
    assert error["details"] == []
    assert rows(db_path, "SELECT id FROM ingestion_runs") == []


def test_an_unsupported_source_state_publishes_nothing(make_client, db_path):
    source = FakeSource(inventory(project(project_id="a", display_name="Alpha", state="archived")))

    with make_client(source) as client:
        response = client.post(REFRESH)

    assert response.status_code == 503, response.text
    assert response.json()["error"]["details"][0]["failure"] == "unsupported_contract"
    assert rows(db_path, "SELECT project_id FROM projects") == []
    assert [row["outcome"] for row in rows(db_path, "SELECT outcome FROM ingestion_runs")] == [
        "failed"
    ]


def test_a_repeated_source_identifier_publishes_nothing(make_client, db_path):
    source = FakeSource(
        inventory(project(project_id="a", display_name="Alpha"), project(project_id="a", display_name="Again"))
    )

    with make_client(source) as client:
        response = client.post(REFRESH)

    assert response.status_code == 503, response.text
    assert response.json()["error"]["details"][0]["failure"] == "unsupported_contract"
    assert rows(db_path, "SELECT project_id FROM projects") == []
