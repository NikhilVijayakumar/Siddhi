"""Shared test fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Path to a database file that does not exist yet and dies with the test."""
    return tmp_path / "siddhi.db"
