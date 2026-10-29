"""POST /goals: create a goal with its initial revision."""

import sqlite3
import uuid

import pytest
from fastapi.testclient import TestClient

from siddhi.bootstrap.app import create_app

UNKNOWN_BY_DEFAULT = [
    "description",
    "rationale",
    "priority",
    "target_date",
    "success_criteria",
    "constraints",
    "assumptions",
    "risks",
]


@pytest.fixture
def client(db_path):
    with TestClient(create_app(db_path)) as test_client:
        yield test_client


def rows(db_path, sql, parameters=()):
    with sqlite3.connect(db_path) as connection:
        return connection.execute(sql, parameters).fetchall()


def goal_count(db_path):
    return rows(db_path, "SELECT COUNT(*) FROM goals")[0][0]


def test_minimal_create_stores_an_active_goal_with_its_identifier(client, db_path):
    response = client.post(
        "/goals", json={"title": "Publish the architecture note", "outcome_type": "publication"}
    )

    assert response.status_code == 201
    goal = response.json()
    assert uuid.UUID(goal["id"])
    assert goal["title"] == "Publish the architecture note"
    assert goal["outcome_type"] == "publication"
    assert goal["status"] == "active"
    assert goal["revision"] == 0
    assert goal["archived_at"] is None
    assert goal["created_at"].endswith("Z")
    assert goal["updated_at"] == goal["created_at"]
    assert goal["unknown_fields"] == UNKNOWN_BY_DEFAULT
    assert goal_count(db_path) == 1


def test_absent_fields_stay_null_rather_than_defaulted(client):
    goal = client.post(
        "/goals", json={"title": "Ship nothing invented", "outcome_type": "other"}
    ).json()

    for field in UNKNOWN_BY_DEFAULT:
        assert goal[field] is None


def test_non_software_outcome_needs_no_extra_field(client):
    response = client.post(
        "/goals",
        json={"title": "Internal tooling investment", "outcome_type": "internal_investment"},
    )

    assert response.status_code == 201
    assert response.json()["outcome_type"] == "internal_investment"


def test_blank_title_is_rejected_without_creating_a_row(client, db_path):
    response = client.post("/goals", json={"title": "   ", "outcome_type": "software"})

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["category"] == "validation"
    assert error["field"] == "title"
    assert error["message"] == "title must be 1-200 characters and not blank"
    assert error["correlation_id"] == response.headers["X-Correlation-Id"]
    assert goal_count(db_path) == 0


@pytest.mark.parametrize(
    "body",
    [
        {"title": "Ship it", "outcome_type": "shipwreck"},
        {"title": "Ship it", "outcome_type": "software", "priority": "urgent"},
        {"title": "Ship it", "outcome_type": "software", "stage": "discovery"},
    ],
    ids=["unknown-outcome", "unknown-priority", "unknown-field"],
)
def test_invalid_input_is_rejected_without_creating_a_row(client, db_path, body):
    response = client.post("/goals", json=body)

    assert response.status_code == 422
    assert response.json()["error"]["category"] == "validation"
    assert goal_count(db_path) == 0


def test_create_appends_an_initial_revision(client, db_path):
    goal = client.post(
        "/goals", json={"title": "Record the start", "outcome_type": "research"}
    ).json()

    revisions = rows(
        db_path,
        "SELECT revision_number, actor, reason, changed_fields, prior_state "
        "FROM goal_revisions WHERE goal_id = ?",
        (goal["id"],),
    )

    assert revisions == [
        (0, "owner", None, '["title", "outcome_type"]', "{}")
    ]


def test_every_response_carries_a_correlation_id(client):
    response = client.post("/goals", json={"title": "Trace me", "outcome_type": "software"})

    correlation_id = response.headers["X-Correlation-Id"]
    assert len(correlation_id) == 32
    assert int(correlation_id, 16) >= 0
