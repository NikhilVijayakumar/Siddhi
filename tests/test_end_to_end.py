"""The whole lifecycle over HTTP, and what every failure leaves behind."""

import sqlite3

from fastapi.testclient import TestClient

from siddhi.bootstrap.app import create_app


def create(client, **fields):
    response = client.post(
        "/goals", json={"title": "Reach five customers", "outcome_type": "other"} | fields
    )
    assert response.status_code == 201, response.text
    return response.json()


def snapshot(db_path):
    with sqlite3.connect(db_path) as connection:
        goals = connection.execute("SELECT * FROM goals ORDER BY id").fetchall()
        revisions = connection.execute(
            "SELECT * FROM goal_revisions ORDER BY goal_id, revision_number"
        ).fetchall()
    return goals, revisions


def test_a_goal_runs_its_whole_lifecycle_on_one_database(db_path):
    with TestClient(create_app(db_path)) as client:
        created = create(client, success_criteria="five signed agreements")
        assert client.get(f"/goals/{created['id']}").json() == created

        revised = client.patch(
            f"/goals/{created['id']}",
            json={"priority": "high", "revision_reason": "Committed in planning"},
        ).json()
        assert revised["priority"] == "high"
        assert revised["revision"] == 1

        history = client.get(f"/goals/{created['id']}/revisions").json()["items"]
        assert [(item["revision_number"], item["changed_fields"]) for item in history] == [
            (1, ["priority"]),
            (0, ["title", "outcome_type", "success_criteria"]),
        ]

        archived = client.post(f"/goals/{created['id']}/archive").json()
        assert (archived["status"], archived["revision"]) == ("archived", 2)
        assert client.get("/goals").json()["items"] == []
        assert [
            goal["id"]
            for goal in client.get("/goals", params={"status": "archived"}).json()["items"]
        ] == [created["id"]]
        assert [
            item["revision_number"]
            for item in client.get(f"/goals/{created['id']}/revisions").json()["items"]
        ] == [2, 1, 0]

        assert client.get("/health").json()["status"] == "ok"


def test_rejected_requests_change_nothing(client, db_path):
    goal = create(client)
    before = snapshot(db_path)
    attempts = [
        ("create without title", lambda: client.post("/goals", json={"outcome_type": "other"})),
        ("blank title", lambda: client.post("/goals", json={"title": " ", "outcome_type": "other"})),
        ("bad priority", lambda: client.patch(f"/goals/{goal['id']}", json={"priority": "urgent"})),
        (
            "stale revision",
            lambda: client.patch(f"/goals/{goal['id']}", json={"title": "Nope", "expected_revision": 9}),
        ),
        ("unknown goal", lambda: client.get("/goals/unknown-identifier")),
        ("revise unknown goal", lambda: client.patch("/goals/unknown-identifier", json={"title": "Nope"})),
        ("archive unknown goal", lambda: client.post("/goals/unknown-identifier/archive")),
        ("unknown route", lambda: client.get("/agenda")),
    ]

    outcomes = []
    for label, attempt in attempts:
        response = attempt()
        outcomes.append((label, response.status_code))
        assert snapshot(db_path) == before, f"{label} changed stored state"

    assert outcomes == [
        ("create without title", 422),
        ("blank title", 422),
        ("bad priority", 422),
        ("stale revision", 409),
        ("unknown goal", 404),
        ("revise unknown goal", 404),
        ("archive unknown goal", 404),
        ("unknown route", 404),
    ]


def test_an_unusable_database_is_reported_and_not_repaired(client, db_path):
    create(client)
    db_path.unlink()
    db_path.mkdir()

    read = client.get(f"/goals")
    write = client.post("/goals", json={"title": "Doomed", "outcome_type": "other"})
    health = client.get("/health")

    assert (read.status_code, write.status_code, health.status_code) == (503, 503, 503)
    for response in (read, write):
        assert response.json()["error"]["category"] == "unavailable"
        assert str(db_path) not in response.text
    assert db_path.is_dir(), "the unusable path was replaced rather than reported"
