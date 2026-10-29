"""Application assembly: migrate the store, then wire the HTTP surface."""

from collections.abc import Callable
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from siddhi.adapters.sqlite.goal_repository import SqliteGoalRepository
from siddhi.adapters.sqlite.project_repository import SqliteProjectRepository
from siddhi.adapters.sqlite.runner import apply_migrations
from siddhi.api.http import add_correlation_id, install_error_handlers, router
from siddhi.application.inventory import ProjectSource
from siddhi.bootstrap.config import Settings
from siddhi.observability.logging import configure_logging


def create_app(db_path: Path, project_source: ProjectSource | None = None) -> FastAPI:
    """Serve on a migrated local database, with an optional inventory source."""
    apply_migrations(db_path)
    app = FastAPI(title="Siddhi", openapi_url=None, docs_url=None, redoc_url=None)
    app.state.db_path = db_path
    app.state.goals = SqliteGoalRepository(db_path)
    app.state.projects = SqliteProjectRepository(db_path)
    app.state.project_source = project_source
    add_correlation_id(app)
    install_error_handlers(app)
    app.include_router(router)
    return app


def serve(settings: Settings, run: Callable[..., None] = uvicorn.run) -> None:
    """Start the service on the validated address; `run` is injectable for tests."""
    configure_logging(settings.log_level)
    run(create_app(settings.database_path), host=settings.bind_host, port=settings.bind_port)
