"""Application assembly: migrate the store, then wire the HTTP surface."""

from pathlib import Path

from fastapi import FastAPI

from siddhi.adapters.sqlite.goal_repository import SqliteGoalRepository
from siddhi.adapters.sqlite.runner import apply_migrations
from siddhi.api.http import add_correlation_id, install_error_handlers, router


def create_app(db_path: Path) -> FastAPI:
    """Serve on a migrated local database. Configuration loading arrives in slice 6."""
    apply_migrations(db_path)
    app = FastAPI(title="Siddhi", openapi_url=None, docs_url=None, redoc_url=None)
    app.state.goals = SqliteGoalRepository(db_path)
    add_correlation_id(app)
    install_error_handlers(app)
    app.include_router(router)
    return app
