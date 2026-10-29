"""Shared test fixtures."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from siddhi.bootstrap.app import create_app


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Path to a database file that does not exist yet and dies with the test."""
    return tmp_path / "siddhi.db"


@pytest.fixture
def client(db_path: Path):
    """HTTP client over a freshly migrated database."""
    with TestClient(create_app(db_path)) as test_client:
        yield test_client


@pytest.fixture
def make_client(db_path: Path):
    """Build clients over the same database, each with its own inventory source."""

    def build(project_source=None):
        return TestClient(create_app(db_path, project_source=project_source))

    return build
