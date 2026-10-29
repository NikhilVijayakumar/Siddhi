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
