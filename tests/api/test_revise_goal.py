"""PATCH /goals/{id} and GET /goals/{id}/revisions: revisions are append-only."""

import sqlite3

import pytest


def create(client, **fields):
    response = client.post("/goals", json={"title": "A goal", "outcome_type": "software"} | fields)
    assert response.status_code == 201, response.text
    return response.json()


def revisions(db_path, goal_id):
    with sqlite3.connect(db_path) as connection:
        return connection.execute(
            "SELECT revision_number, actor, reason, changed_fields, prior_state "
            "FROM goal_revisions WHERE goal_id = ? ORDER BY revision_number DESC",
            (goal_id,),
        ).fetchall()


def test_revising_a_field_appends_a_revision(client, db_path):
    goal = create(client, title="Revise me")

    response = client.patch(
        f"/goals/{goal['id']}", json={"priority": "high", "revision_reason": "Deadline agreed"}
    )

    assert response.status_code == 200
    revised = response.json()
    assert revised["priority"] == "high"
    assert revised["revision"] == 1
    assert revised["updated_at"].endswith("Z")
    assert "priority" not in revised["unknown_fields"]
    assert revisions(db_path, goal["id"])[0] == (
        1,
        "owner",
        "Deadline agreed",
        '["priority"]',
        '{"priority": null}',
    )


def test_explicit_null_clears_a_field_back_to_unknown(client, db_path):
    goal = create(client, title="Clear me", description="Draft text")

    revised = client.patch(f"/goals/{goal['id']}", json={"description": None}).json()

    assert revised["description"] is None
    assert "description" in revised["unknown_fields"]
    assert revisions(db_path, goal["id"])[0] == (
        1,
        "owner",
        None,
        '["description"]',
        '{"description": "Draft text"}',
    )


def test_absent_fields_are_untouched(client):
    goal = create(client, title="Keep me", rationale="Because", priority="low")

    revised = client.patch(f"/goals/{goal['id']}", json={"title": "Renamed"}).json()

    assert revised["title"] == "Renamed"
    assert revised["rationale"] == "Because"
    assert revised["priority"] == "low"


def test_stale_expected_revision_conflicts_without_changing_anything(client, db_path):
    goal = create(client)
    assert (
        client.patch(f"/goals/{goal['id']}", json={"title": "Second"}, params={})
        .json()["revision"]
        == 1
    )

    response = client.patch(
        f"/goals/{goal['id']}", json={"title": "Third", "expected_revision": 0}
    )

    assert response.status_code == 409
    error = response.json()["error"]
    assert error["category"] == "conflict"
    assert error["details"] == [{"current_revision": 1}]
    assert client.get(f"/goals/{goal['id']}").json()["title"] == "Second"
    assert len(revisions(db_path, goal["id"])) == 2


def test_matching_expected_revision_is_accepted(client):
    goal = create(client)

    response = client.patch(
        f"/goals/{goal['id']}", json={"title": "Second", "expected_revision": 0}
    )

    assert response.status_code == 200
    assert response.json()["revision"] == 1


def test_no_op_update_creates_no_revision(client, db_path):
    goal = create(client, title="Unchanged")

    response = client.patch(f"/goals/{goal['id']}", json={"title": "Unchanged"})

    assert response.status_code == 200
    assert response.json()["revision"] == 0
    assert len(revisions(db_path, goal["id"])) == 1


@pytest.mark.parametrize(
    "body",
    [
        {"status": "archived"},
        {"id": "00000000-0000-4000-8000-000000000000"},
        {"revision": 7},
        {"created_at": "2026-01-01T00:00:00Z"},
        {"archived_at": "2026-01-01T00:00:00Z"},
    ],
    ids=["status", "id", "revision", "created_at", "archived_at"],
)
def test_server_owned_fields_cannot_be_written(client, db_path, body):
    goal = create(client)

    response = client.patch(f"/goals/{goal['id']}", json=body)

    assert response.status_code == 422
    assert response.json()["error"]["category"] == "validation"
    assert len(revisions(db_path, goal["id"])) == 1


@pytest.mark.parametrize(
    "body",
    [
        {"title": "   "},
        {"outcome_type": "shipwreck"},
        {"priority": "urgent"},
        {"revision_reason": "x" * 501},
    ],
    ids=["blank-title", "bad-outcome", "bad-priority", "long-reason"],
)
def test_invalid_values_are_rejected_without_a_revision(client, db_path, body):
    goal = create(client)

    response = client.patch(f"/goals/{goal['id']}", json=body)

    assert response.status_code == 422
    assert len(revisions(db_path, goal["id"])) == 1
    assert client.get(f"/goals/{goal['id']}").json() == goal


def test_revising_an_unknown_goal_is_not_found(client):
    response = client.patch(
        "/goals/00000000-0000-4000-8000-000000000000", json={"title": "Nope"}
    )

    assert response.status_code == 404
    assert response.json()["error"]["category"] == "not_found"


def test_history_lists_every_revision_newest_first(client):
    goal = create(client, title="First title")
    client.patch(f"/goals/{goal['id']}", json={"title": "Second title"})
    client.patch(f"/goals/{goal['id']}", json={"priority": "critical"})

    page = client.get(f"/goals/{goal['id']}/revisions").json()

    assert [item["revision_number"] for item in page["items"]] == [2, 1, 0]
    assert page["items"][0]["changed_fields"] == ["priority"]
    assert page["items"][1]["prior_state"] == {"title": "First title"}
    assert page["items"][-1]["changed_fields"] == ["title", "outcome_type"]
    assert page["has_more"] is False
    assert page["next_cursor"] is None


def test_history_pages_follow_the_cursor_without_gaps(client):
    goal = create(client)
    for title in ("two", "three", "four"):
        client.patch(f"/goals/{goal['id']}", json={"title": title})

    first = client.get(f"/goals/{goal['id']}/revisions", params={"limit": 2}).json()
    second = client.get(
        f"/goals/{goal['id']}/revisions",
        params={"limit": 2, "cursor": first["next_cursor"]},
    ).json()

    assert [item["revision_number"] for item in first["items"]] == [3, 2]
    assert first["has_more"] is True
    assert [item["revision_number"] for item in second["items"]] == [1, 0]
    assert second["has_more"] is False


def test_history_of_an_unknown_goal_is_not_found(client):
    response = client.get("/goals/00000000-0000-4000-8000-000000000000/revisions")

    assert response.status_code == 404
    assert response.json()["error"]["category"] == "not_found"
