"""HTTP surface: request/response models, routes and error mapping."""

from datetime import date
from uuid import uuid4

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from siddhi.application.goals import NewGoal, create_goal
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


@router.post("/goals", status_code=201, response_model=GoalResponse)
def post_goal(body: CreateGoalRequest, request: Request) -> GoalResponse:
    goal = create_goal(request.app.state.goals, NewGoal(**body.model_dump()))
    return GoalResponse.model_validate(goal)


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
