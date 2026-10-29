"""HTTP surface: request/response models, routes and error mapping."""

from datetime import date
from uuid import uuid4

from fastapi import APIRouter, FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from siddhi.application.goals import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    GoalNotFound,
    GoalPage,
    NewGoal,
    create_goal,
    get_goal,
    list_goals,
)
from siddhi.domain.goal import InvalidGoal

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


def _page_response(page: GoalPage) -> GoalPageResponse:
    return GoalPageResponse(
        items=[GoalResponse.model_validate(goal) for goal in page.items],
        next_cursor=page.next_cursor,
        has_more=page.has_more,
    )


def add_correlation_id(app: FastAPI) -> None:
    @app.middleware("http")
    async def correlation_id(request: Request, call_next):
        request.state.correlation_id = uuid4().hex
        response = await call_next(request)
        response.headers["X-Correlation-Id"] = request.state.correlation_id
        return response


def error_body(
    request: Request,
    category: str,
    code: str,
    message: str,
    field: str | None = None,
) -> dict:
    """Error envelope from api-contract 4; never includes a submitted value."""
    return {
        "error": {
            "category": category,
            "code": code,
            "message": message,
            "field": field,
            "correlation_id": request.state.correlation_id,
            "details": [],
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
