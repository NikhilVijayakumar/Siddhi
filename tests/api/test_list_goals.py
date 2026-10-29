"""GET /goals and GET /goals/{id}: bounded keyset pagination over stored goals."""

import sqlite3

import pytest


def create(client, **fields):
    goal = {"title": "A goal", "outcome_type": "software"} | fields
    response = client.post("/goals", json=goal)
    assert response.status_code == 201, response.text
    return response.json()


def run(db_path, sql, parameters=()):
    with sqlite3.connect(db_path) as connection:
        connection.execute(sql, parameters)
        connection.commit()


def list_goals(client, **parameters):
    response = client.get("/goals", params=parameters)
    assert response.status_code == 200, response.text
    return response.json()


def test_retrieving_a_goal_returns_it_as_created(client):
    created = create(client, title="Read me back", priority="high", target_date="2027-01-31")

    response = client.get(f"/goals/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_unknown_identifier_is_a_not_found_error(client):
    response = client.get("/goals/00000000-0000-4000-8000-000000000000")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["category"] == "not_found"
    assert error["correlation_id"] == response.headers["X-Correlation-Id"]


def test_archived_goals_remain_retrievable(client, db_path):
    goal = create(client)
    run(
        db_path,
        "UPDATE goals SET status = 'archived', archived_at = '2026-10-29T00:00:00Z' WHERE id = ?",
        (goal["id"],),
    )

    response = client.get(f"/goals/{goal['id']}")

    assert response.status_code == 200
    assert response.json()["status"] == "archived"
    assert response.json()["archived_at"] == "2026-10-29T00:00:00Z"


def test_page_is_bounded_and_reports_more(client):
    for n in range(3):
        create(client, title=f"Goal {n}")

    page = list_goals(client, limit=2)

    assert len(page["items"]) == 2
    assert page["has_more"] is True
    assert page["next_cursor"]


def test_following_the_cursor_returns_every_goal_once(client):
    created = [create(client, title=f"Goal {n}") for n in range(5)]
    seen, cursor, pages = [], None, 0

    while True:
        page = list_goals(client, limit=2, **({"cursor": cursor} if cursor else {}))
        pages += 1
        seen.extend(item["id"] for item in page["items"])
        cursor = page["next_cursor"]
        if not page["has_more"]:
            break

    assert pages == 3
    assert len(seen) == len(set(seen)) == 5
    assert set(seen) == {goal["id"] for goal in created}
    assert cursor is None and page["next_cursor"] is None


def test_listing_defaults_to_active_and_filters_on_status(client, db_path):
    active = create(client, title="Active")
    archived = create(client, title="Archived")
    run(
        db_path,
        "UPDATE goals SET status = 'archived', archived_at = '2026-10-29T00:00:00Z' WHERE id = ?",
        (archived["id"],),
    )

    assert [item["id"] for item in list_goals(client)["items"]] == [active["id"]]
    assert [item["id"] for item in list_goals(client, status="archived")["items"]] == [
        archived["id"]
    ]
    assert {item["id"] for item in list_goals(client, status="all")["items"]} == {
        active["id"],
        archived["id"],
    }


def test_ordering_falls_back_to_identifier_when_timestamps_match(client, db_path):
    goals = [create(client, title=f"Tie {n}") for n in range(3)]
    run(db_path, "UPDATE goals SET created_at = '2026-10-29T12:00:00Z'")

    listed = [item["id"] for item in list_goals(client)["items"]]

    assert listed == sorted(goal["id"] for goal in goals)


@pytest.mark.parametrize("cursor", ["not-a-cursor", "eyJvIjoyNX0"])
def test_invalid_cursor_is_a_validation_error(client, cursor):
    response = client.get("/goals", params={"cursor": cursor})

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["category"] == "validation"
    assert error["field"] == "cursor"


@pytest.mark.parametrize(
    "parameters",
    [{"limit": 0}, {"limit": 101}, {"status": "deleted"}],
    ids=["limit-low", "limit-high", "bad-status"],
)
def test_out_of_range_parameters_are_rejected(client, parameters):
    response = client.get("/goals", params=parameters)

    assert response.status_code == 422
    assert response.json()["error"]["category"] == "validation"
