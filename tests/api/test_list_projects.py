"""Project reads: bounded pages, source context, and no source access."""

import base64
import json

import pytest

from tests.fakes import FakeSource, inventory, project

REFRESH = "/ingestion/vyasa/refresh"
PROJECT_ID = "e620f8eda2274e9397a3f7430f22c012"
NON_STRING_CURSOR = (
    base64.urlsafe_b64encode(json.dumps({"display_name": 1, "project_id": None}).encode())
    .decode()
    .rstrip("=")
)


def test_a_project_payload_carries_observation_context(make_client):
    source = FakeSource(inventory(project(project_id=PROJECT_ID), freshness="stale"))

    with make_client(source) as client:
        report = client.post(REFRESH).json()
        response = client.get(f"/projects/{PROJECT_ID}")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "project_id": PROJECT_ID,
        "display_name": "Siddhi",
        "state": "active",
        "identity_status": "resolved",
        "providers": ["github"],
        "languages": ["Python"],
        "first_observed_at": report["started_at"],
        "last_observed_at": report["started_at"],
        "freshness": "stale",
    }
    assert source.calls == 1


def test_projects_are_listed_by_name_and_paged_without_duplicates(make_client):
    source = FakeSource(
        inventory(
            project(project_id="c", display_name="Gamma"),
            project(project_id="a", display_name="Alpha"),
            project(project_id="b", display_name="Beta"),
        )
    )

    with make_client(source) as client:
        client.post(REFRESH)
        first = client.get("/projects", params={"limit": 2}).json()
        second = client.get("/projects", params={"limit": 2, "cursor": first["next_cursor"]}).json()

    assert [item["display_name"] for item in first["items"]] == ["Alpha", "Beta"]
    assert first["has_more"] is True
    assert first["next_cursor"] is not None
    assert [item["display_name"] for item in second["items"]] == ["Gamma"]
    assert second["has_more"] is False
    assert second["next_cursor"] is None
    assert len({item["project_id"] for item in first["items"] + second["items"]}) == 3


def test_projects_with_the_same_name_are_paged_by_identifier(make_client):
    source = FakeSource(
        inventory(
            project(project_id="b", display_name="Same"),
            project(project_id="a", display_name="Same"),
        )
    )

    with make_client(source) as client:
        client.post(REFRESH)
        first = client.get("/projects", params={"limit": 1}).json()
        second = client.get(
            "/projects", params={"limit": 1, "cursor": first["next_cursor"]}
        ).json()

    assert [item["project_id"] for item in first["items"]] == ["a"]
    assert [item["project_id"] for item in second["items"]] == ["b"]
    assert second["has_more"] is False


def test_listing_filters_by_source_state(make_client):
    source = FakeSource(
        inventory(
            project(project_id="a", display_name="Alpha"),
            project(project_id="b", display_name="Beta", state="missing"),
            project(project_id="c", display_name="Gamma", state="inaccessible"),
        )
    )

    with make_client(source) as client:
        client.post(REFRESH)
        missing = client.get("/projects", params={"state": "missing"}).json()
        everything = client.get("/projects").json()

    assert [item["state"] for item in missing["items"]] == ["missing"]
    assert len(everything["items"]) == 3


def test_a_missing_project_is_a_state_not_a_deletion(make_client):
    source = FakeSource(inventory(project(project_id="a", display_name="Alpha", state="missing")))

    with make_client(source) as client:
        client.post(REFRESH)
        response = client.get("/projects/a")

    assert response.status_code == 200
    assert response.json()["state"] == "missing"


def test_an_empty_current_view_is_an_empty_page_not_an_error(make_client):
    source = FakeSource(inventory())

    with make_client(source) as client:
        client.post(REFRESH)
        response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == {"items": [], "next_cursor": None, "has_more": False}


def test_an_unobserved_project_is_not_found(make_client):
    with make_client(FakeSource(inventory())) as client:
        response = client.get("/projects/does-not-exist")

    assert response.status_code == 404
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("not_found", "project_not_found")


def test_a_project_absent_from_a_completed_read_is_no_longer_served(make_client):
    source = FakeSource(
        inventory(project(project_id="a", display_name="Alpha"), project(project_id="b", display_name="Beta")),
        inventory(project(project_id="a", display_name="Alpha")),
    )

    with make_client(source) as client:
        client.post(REFRESH)
        report = client.post(REFRESH).json()
        removed = client.get("/projects/b")
        listed = client.get("/projects").json()

    assert report["counts"]["removed"] == 1
    assert removed.status_code == 404
    assert [item["project_id"] for item in listed["items"]] == ["a"]


@pytest.mark.parametrize(
    "params, field",
    [
        ({"state": "archived"}, "state"),
        ({"cursor": "not-a-cursor"}, "cursor"),
        ({"cursor": NON_STRING_CURSOR}, "cursor"),
        ({"limit": 0}, "limit"),
    ],
)
def test_an_unusable_query_is_rejected_before_reading(make_client, params, field):
    with make_client(FakeSource(inventory(project(project_id="a", display_name="Alpha")))) as client:
        client.post(REFRESH)
        response = client.get("/projects", params=params)

    assert response.status_code == 422, response.text
    error = response.json()["error"]
    assert (error["category"], error["code"]) == ("validation", "invalid_field")
    assert error["field"] == field
