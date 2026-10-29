"""POST /goals/{id}/archive: retired from the default listing, never deleted."""

import sqlite3


def create(client, **fields):
    response = client.post("/goals", json={"title": "A goal", "outcome_type": "software"} | fields)
    assert response.status_code == 201, response.text
    return response.json()


def archive(client, goal_id):
    return client.post(f"/goals/{goal_id}/archive")


def count(db_path, table):
    with sqlite3.connect(db_path) as connection:
        return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_archiving_sets_status_time_and_one_revision(client, db_path):
    goal = create(client, title="Retire me")

    response = archive(client, goal["id"])

    assert response.status_code == 200
    archived = response.json()
    assert archived["status"] == "archived"
    assert archived["archived_at"].endswith("Z")
    assert archived["revision"] == 1
    with sqlite3.connect(db_path) as connection:
        assert connection.execute(
            "SELECT revision_number, changed_fields, prior_state FROM goal_revisions "
            "WHERE goal_id = ? ORDER BY revision_number DESC",
            (goal["id"],),
        ).fetchall()[0] == (1, '["status"]', '{"status": "active"}')


def test_archived_goal_leaves_the_default_listing_but_stays_readable(client):
    goal = create(client, title="Hide me")

    archive(client, goal["id"])

    assert [item["id"] for item in client.get("/goals").json()["items"]] == []
    assert [item["id"] for item in client.get("/goals", params={"status": "archived"}).json()["items"]] == [
        goal["id"]
    ]
    assert client.get(f"/goals/{goal['id']}").json()["status"] == "archived"
    assert [item["revision_number"] for item in client.get(f"/goals/{goal['id']}/revisions").json()["items"]] == [
        1,
        0,
    ]


def test_archiving_twice_is_idempotent(client, db_path):
    goal = create(client)
    first = archive(client, goal["id"]).json()

    second = archive(client, goal["id"])

    assert second.status_code == 200
    assert second.json()["revision"] == first["revision"]
    assert second.json()["archived_at"] == first["archived_at"]
    assert count(db_path, "goal_revisions") == 2


def test_archiving_deletes_no_rows(client, db_path):
    goal = create(client)
    client.patch(f"/goals/{goal['id']}", json={"title": "Revised first"})

    archive(client, goal["id"])

    assert count(db_path, "goals") == 1
    assert count(db_path, "goal_revisions") == 3


def test_archiving_an_unknown_goal_is_not_found(client):
    response = archive(client, "00000000-0000-4000-8000-000000000000")

    assert response.status_code == 404
    assert response.json()["error"]["category"] == "not_found"
