"""HTTP surface: request/response models, routes and error mapping."""

import logging
import sqlite3
import time
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from siddhi.application.goals import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    GoalConflict,
    GoalNotFound,
    GoalPage,
    NewGoal,
    RevisionPage,
    archive_goal,
    create_goal,
    get_goal,
    list_goals,
    list_revisions,
    revise_goal,
)
from siddhi.domain.goal import InvalidGoal
from siddhi.observability.health import health_report
from siddhi.observability.logging import log_event

logger = logging.getLogger("siddhi")

router = APIRouter()


class CreateGoalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    outcome_type: str
    description: str | None = None
    rationale: str | None = None
    priority: str | None = None
    target_date: date | None = None
    success_criteria: str | None = None
    constraints: str | None = None
    assumptions: str | None = None
    risks: str | None = None


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    outcome_type: str
    status: str
    description: str | None
    rationale: str | None
    priority: str | None
    target_date: str | None
    success_criteria: str | None
    constraints: str | None
    assumptions: str | None
    risks: str | None
    unknown_fields: list[str]
    revision: int
    created_at: str
    updated_at: str
    archived_at: str | None


class GoalPageResponse(BaseModel):
    items: list[GoalResponse]
    next_cursor: str | None
    has_more: bool


class PatchGoalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    outcome_type: str | None = None
    description: str | None = None
    rationale: str | None = None
    priority: str | None = None
    target_date: date | None = None
    success_criteria: str | None = None
    constraints: str | None = None
    assumptions: str | None = None
    risks: str | None = None
    revision_reason: str | None = Field(None, max_length=500)
    expected_revision: int | None = None


class RevisionResponse(BaseModel):
    revision_number: int
    changed_at: str
    actor: str
    reason: str | None
    changed_fields: list[str]
    prior_state: dict[str, object]


class RevisionPageResponse(BaseModel):
    items: list[RevisionResponse]
    next_cursor: str | None
    has_more: bool


@router.get("/health")
def get_health(request: Request) -> JSONResponse:
    payload, status_code = health_report(request.app.state.db_path)
    return JSONResponse(status_code=status_code, content=payload)


@router.post("/goals", status_code=201, response_model=GoalResponse)
def post_goal(body: CreateGoalRequest, request: Request) -> GoalResponse:
    goal = create_goal(request.app.state.goals, NewGoal(**body.model_dump()))
    return GoalResponse.model_validate(goal)


@router.get("/goals", response_model=GoalPageResponse)
def get_goals(
    request: Request,
    status: str = "active",
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    cursor: str | None = None,
) -> GoalPageResponse:
    page = list_goals(request.app.state.goals, status, limit, cursor)
    return _page_response(page)


@router.get("/goals/{goal_id}", response_model=GoalResponse)
def get_one_goal(goal_id: str, request: Request) -> GoalResponse:
    return GoalResponse.model_validate(get_goal(request.app.state.goals, goal_id))


@router.patch("/goals/{goal_id}", response_model=GoalResponse)
def patch_goal(goal_id: str, body: PatchGoalRequest, request: Request) -> GoalResponse:
    supplied = body.model_dump(exclude_unset=True)
    reason = supplied.pop("revision_reason", None)
    expected_revision = supplied.pop("expected_revision", None)
    if supplied.get("target_date") is not None:
        supplied["target_date"] = supplied["target_date"].isoformat()
    revised = revise_goal(
        request.app.state.goals, goal_id, supplied, reason, expected_revision
    )
    return GoalResponse.model_validate(revised)


@router.post("/goals/{goal_id}/archive", response_model=GoalResponse)
def post_archive(goal_id: str, request: Request) -> GoalResponse:
    return GoalResponse.model_validate(archive_goal(request.app.state.goals, goal_id))


@router.get("/goals/{goal_id}/revisions", response_model=RevisionPageResponse)
def get_revisions(
    goal_id: str,
    request: Request,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    cursor: str | None = None,
) -> RevisionPageResponse:
    page = list_revisions(request.app.state.goals, goal_id, limit, cursor)
    return _revision_page_response(page)


def _page_response(page: GoalPage) -> GoalPageResponse:
    return GoalPageResponse(
        items=[GoalResponse.model_validate(goal) for goal in page.items],
        next_cursor=page.next_cursor,
        has_more=page.has_more,
    )


def _revision_page_response(page: RevisionPage) -> RevisionPageResponse:
    return RevisionPageResponse(
        items=[
            RevisionResponse(
                revision_number=revision.revision_number,
                changed_at=revision.changed_at,
                actor=revision.actor,
                reason=revision.reason,
                changed_fields=revision.changed_fields,
                prior_state=revision.prior_state,
            )
            for revision in page.items
        ],
        next_cursor=page.next_cursor,
        has_more=page.has_more,
    )


def add_correlation_id(app: FastAPI) -> None:
    @app.middleware("http")
    async def correlation_id(request: Request, call_next):
        request.state.correlation_id = uuid4().hex
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Correlation-Id"] = request.state.correlation_id
        log_event(
            logger,
            "http.request",
            correlation_id=request.state.correlation_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round((time.perf_counter() - started) * 1000, 1),
        )
        return response


def error_body(
    request: Request,
    category: str,
    code: str,
    message: str,
    field: str | None = None,
    details: list[dict[str, object]] | None = None,
) -> dict:
    """Error envelope from api-contract 4; never includes a submitted value."""
    return {
        "error": {
            "category": category,
            "code": code,
            "message": message,
            "field": field,
            "correlation_id": request.state.correlation_id,
            "details": details or [],
        }
    }


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidGoal)
    async def invalid_goal(request: Request, exc: InvalidGoal) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_body(request, "validation", "invalid_field", exc.message, exc.field),
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0]
        field = str(first["loc"][-1]) if first["loc"] else None
        return JSONResponse(
            status_code=422,
            content=error_body(request, "validation", "invalid_field", first["msg"], field),
        )

    @app.exception_handler(GoalNotFound)
    async def goal_not_found(request: Request, exc: GoalNotFound) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content=error_body(
                request, "not_found", "goal_not_found", "no goal uses that identifier"
            ),
        )

    @app.exception_handler(GoalConflict)
    async def goal_conflict(request: Request, exc: GoalConflict) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content=error_body(
                request,
                "conflict",
                "revision_conflict",
                "expected_revision does not match the current revision",
                details=[{"current_revision": exc.current_revision}],
            ),
        )

    @app.exception_handler(sqlite3.Error)
    async def database_unavailable(request: Request, exc: sqlite3.Error) -> JSONResponse:
        # sqlite3 messages carry the database path, so only the exception type is logged.
        log_event(
            logger,
            "database.unavailable",
            correlation_id=request.state.correlation_id,
            error=type(exc).__name__,
        )
        return JSONResponse(
            status_code=503,
            content=error_body(
                request,
                "unavailable",
                "database_unavailable",
                "the local database is unavailable",
            ),
        )
