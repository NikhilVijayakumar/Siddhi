# API Design

**Document:** `api-design.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Public application API for the Siddhi backend

**Related documents:** `vision.md`, `scope-and-roadmap.md`, `functional-requirements.md`, `non-functional-requirements.md`, `system-architecture.md`, `architectural-decisions.md`, `domain-model.md`, `data-model.md`, `data-ownership.md`, `application-workflows.md`, `source-integration.md`, `ingestion-and-snapshots.md`, `deterministic-analysis.md`, `external-analysis.md`, `security-and-privacy.md`

---

## 1. Purpose

This document defines the HTTP API contract for Siddhi's backend.

The API provides a stable interface through which the future desktop application and other authorized clients can access portfolio data, configure source integrations, trigger ingestion, inspect evidence, run deterministic analysis, request external analysis, and record portfolio decisions.

The API must separate client interaction from internal implementation details. Clients interact with meaningful portfolio resources and application workflows rather than directly accessing database tables, source adapters, or internal Python objects.

The API is intended to support:

- A local-first desktop application.
- Future authorized clients.
- Automated tests and development tools.
- Controlled integration with other internal systems, if required later.

The initial implementation is proposed to use Python, FastAPI, Pydantic, and SQLite, with the API documented through OpenAPI. These technology choices remain subject to confirmation in `architectural-decisions.md`.

## 2. Design principles

### 2.1 API as the application boundary

All client access to Siddhi's persistent application data must pass through the backend API or the backend's internal application services.

The frontend must not access SQLite directly.

The API must not expose internal repository classes, SQL structures, ORM models, or adapter implementation details as its public contract.

### 2.2 Domain-oriented resources

API resources should reflect Siddhi's domain concepts, including:

- Goals.
- Initiatives.
- Portfolio priorities.
- Plans and plan revisions.
- Milestones.
- Dependencies.
- Decisions.
- Source configurations.
- Ingestion runs.
- Snapshots.
- Evidence records.
- Analysis runs.
- Findings and reports.
- External analysis requests.
- Recommendations.

The exact resource model should follow the finalized domain and data models rather than being determined solely by the existing database structure.

### 2.3 Explicit workflows

Operations that initiate work or change important state should use explicit application actions.

For example, refreshing a source, publishing an ingestion result, executing an analysis, and approving a recommendation are different operations. They must not be hidden inside an ordinary resource read or update.

### 2.4 Stable contracts

The API must have documented request and response schemas, predictable errors, explicit lifecycle transitions, and a versioning policy.

Internal implementation changes should not require a client rewrite unless the public contract intentionally changes.

### 2.5 Least privilege

The API must expose only the operations required by the client and the configured deployment model.

Local hosting does not eliminate security requirements. The backend must not assume that every process capable of connecting to localhost is authorized.

---

## 3. Architecture and responsibilities

```text id="j2n5vc"
Desktop Application / Authorized Client
                  |
                  v
             HTTP API
                  |
                  v
       Request and Response Models
                  |
                  v
       Application / Use-Case Layer
                  |
        +---------+----------+
        |                    |
        v                    v
    Domain Logic        Source Adapters
        |                    |
        +---------+----------+
                  |
                  v
       Repository / Persistence Layer
                  |
                  v
                SQLite
```

### 3.1 API layer

The API layer is responsible for:

- Routing and HTTP methods.
- Request validation.
- Response serialization.
- Authentication and authorization.
- Pagination and filtering.
- HTTP status codes.
- Error responses.
- Request correlation IDs.
- API documentation.

### 3.2 Application layer

The application layer executes use cases such as:

- Creating or updating a goal.
- Linking a project to an initiative.
- Starting a source ingestion run.
- Publishing an eligible snapshot.
- Running deterministic analysis.
- Requesting external analysis.
- Recording a portfolio decision.

Business rules and workflow transitions belong in this layer or the domain layer, not in the HTTP route handlers.

### 3.3 Domain layer

The domain layer owns portfolio rules, validation, state transitions, and invariants.

It must not depend on FastAPI request objects or HTTP-specific behavior.

### 3.4 Source adapters

Source adapters communicate with Vyasa, OpenSpec, OKF, Git, and supported verification systems. The API should invoke them through application services rather than exposing arbitrary adapter operations directly.

### 3.5 Persistence layer

The persistence layer owns database access, transactions, migrations, and repository implementations.

The API must not expose direct SQL execution or unrestricted database manipulation.

---

## 4. API conventions

### 4.1 Base path and versioning

The initial API should use a versioned base path:

`/api/v1`

Examples:

- `/api/v1/goals`
- `/api/v1/projects`
- `/api/v1/sources`
- `/api/v1/ingestion-runs`
- `/api/v1/analysis-runs`

The exact versioning strategy should be documented before the first stable release.

Backward-compatible additions should be preferred within a version. Breaking changes should require an explicit migration strategy and, when necessary, a new API version.

### 4.2 Data format

JSON should be the default request and response format for ordinary API operations.

The API must define explicit schemas for all public request and response bodies. Unrestricted dictionaries should not be used where a stable structured model is practical.

Timestamps should use a consistent ISO 8601 representation, including timezone information where applicable. Date-only values should be used for date-based planning fields when time-of-day is not meaningful.

### 4.3 Resource identifiers

Resources should use stable, opaque identifiers generated or managed by Siddhi.

Clients must not rely on database row IDs, file paths, or display names as identifiers unless a specific contract explicitly defines that behavior.

Source-native identifiers should be retained separately from Siddhi resource IDs.

### 4.4 Field naming

Use one consistent JSON naming convention across the API. `snake_case` is a reasonable initial choice for a Python-oriented backend, but this should be confirmed before client generation.

Once the API is published, naming changes must be treated as contract changes.

### 4.5 Filtering, sorting, and pagination

Collection endpoints should support appropriate filtering and pagination.

Common parameters may include:

- `limit`
- `cursor` or another documented pagination token
- `sort`
- `status`
- `source_id`
- `project_id`
- `goal_id`
- `from` and `to` for supported time ranges

Only filters that are meaningful for a given resource should be exposed.

Pagination must have a documented maximum page size. Large evidence collections and findings must not be returned as unbounded responses.

### 4.6 Concurrency

Where concurrent updates could overwrite important data, the API should support optimistic concurrency control, for example through a resource revision or ETag.

An update based on an obsolete revision should return a conflict response rather than silently overwriting newer data.

The exact mechanism should be chosen during implementation.

---

## 5. Resource groups and endpoint inventory

The following endpoint inventory is a proposed logical contract. It is not a claim that these routes already exist.

### 5.1 System and health

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/health` | Basic process health |
| `GET` | `/api/v1/ready` | Readiness for normal application operations |
| `GET` | `/api/v1/system/info` | API version and supported capabilities |

Health endpoints must not disclose secrets, local filesystem details, credentials, or internal diagnostics.

Readiness should reflect whether required dependencies are available for the intended operation. An optional external AI provider being unavailable should not make the entire API unready for deterministic portfolio work.

### 5.2 Portfolio goals

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/goals` | List goals |
| `POST` | `/api/v1/goals` | Create a goal |
| `GET` | `/api/v1/goals/{goal_id}` | Retrieve a goal |
| `PATCH` | `/api/v1/goals/{goal_id}` | Update permitted goal fields |
| `GET` | `/api/v1/goals/{goal_id}/evidence` | Retrieve mapped evidence |
| `GET` | `/api/v1/goals/{goal_id}/findings` | Retrieve relevant findings |
| `GET` | `/api/v1/goals/{goal_id}/history` | Retrieve supported history |

Goal lifecycle transitions must be validated by the application layer. A client must not be able to bypass approval or required evidence rules by directly changing a status field.

### 5.3 Initiatives and relationships

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/initiatives` | List initiatives |
| `POST` | `/api/v1/initiatives` | Create an initiative |
| `GET` | `/api/v1/initiatives/{initiative_id}` | Retrieve an initiative |
| `PATCH` | `/api/v1/initiatives/{initiative_id}` | Update permitted fields |
| `GET` | `/api/v1/initiatives/{initiative_id}/projects` | Retrieve associated projects |
| `GET` | `/api/v1/initiatives/{initiative_id}/milestones` | Retrieve milestones |
| `GET` | `/api/v1/initiatives/{initiative_id}/dependencies` | Retrieve dependencies |

Relationship creation and removal should use explicit operations or validated relationship fields, according to the finalized domain contract.

### 5.4 Projects and source inventory

Siddhi should expose project information derived from its approved project-inventory integration.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/projects` | List known projects |
| `GET` | `/api/v1/projects/{project_id}` | Retrieve a project reference |
| `GET` | `/api/v1/projects/{project_id}/sources` | Retrieve linked source references |
| `GET` | `/api/v1/projects/{project_id}/evidence` | Retrieve associated evidence |

Project metadata owned by Vyasa must not become independently editable through ordinary Siddhi project endpoints.

Any Siddhi-specific portfolio mapping should be stored separately from the source-owned project metadata.

### 5.5 Plans, milestones, and dependencies

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/plans` | List plans |
| `POST` | `/api/v1/plans` | Create a plan |
| `GET` | `/api/v1/plans/{plan_id}` | Retrieve a plan |
| `POST` | `/api/v1/plans/{plan_id}/revisions` | Create a plan revision |
| `GET` | `/api/v1/plans/{plan_id}/revisions` | List plan revisions |
| `GET` | `/api/v1/milestones` | List milestones |
| `POST` | `/api/v1/milestones` | Create a milestone |
| `PATCH` | `/api/v1/milestones/{milestone_id}` | Update permitted milestone fields |
| `GET` | `/api/v1/dependencies` | List dependencies |
| `POST` | `/api/v1/dependencies` | Create a dependency |
| `DELETE` | `/api/v1/dependencies/{dependency_id}` | Remove a dependency when permitted |

Plan revisions must preserve history. Updating a plan must not silently erase the version that supported an earlier review or decision.

### 5.6 Decisions and recommendations

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/decisions` | List decisions |
| `POST` | `/api/v1/decisions` | Record a decision |
| `GET` | `/api/v1/decisions/{decision_id}` | Retrieve a decision |
| `GET` | `/api/v1/recommendations` | List recommendations |
| `GET` | `/api/v1/recommendations/{recommendation_id}` | Retrieve a recommendation |
| `POST` | `/api/v1/recommendations/{recommendation_id}/review` | Record a review outcome |

Recommendation review operations must not bypass the decision workflow. Accepting a recommendation for further investigation is not the same as approving a portfolio change.

### 5.7 Source configurations

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/sources` | List configured sources |
| `POST` | `/api/v1/sources` | Register a source configuration |
| `GET` | `/api/v1/sources/{source_id}` | Retrieve source configuration metadata |
| `PATCH` | `/api/v1/sources/{source_id}` | Update permitted configuration fields |
| `POST` | `/api/v1/sources/{source_id}/test-connection` | Test source accessibility |
| `POST` | `/api/v1/sources/{source_id}/refresh` | Request an ingestion run |
| `GET` | `/api/v1/sources/{source_id}/snapshots` | List source snapshots |
| `GET` | `/api/v1/sources/{source_id}/status` | Retrieve current source status |

The API must not expose secret values when returning source configuration. Credential references or safe status indicators should be returned instead.

### 5.8 Ingestion and snapshots

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/ingestion-runs` | List ingestion runs |
| `GET` | `/api/v1/ingestion-runs/{run_id}` | Retrieve run status and metadata |
| `POST` | `/api/v1/ingestion-runs/{run_id}/cancel` | Request cancellation when supported |
| `GET` | `/api/v1/snapshots/{snapshot_id}` | Retrieve snapshot metadata |
| `GET` | `/api/v1/snapshots/{snapshot_id}/changes` | Retrieve recorded changes |
| `GET` | `/api/v1/snapshots/{snapshot_id}/coverage` | Retrieve collection coverage |

The API must not expose unrestricted raw snapshot content. Content retrieval must be bounded and authorized according to the source and data-access policies.

### 5.9 Evidence

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/evidence` | Search or list evidence records |
| `GET` | `/api/v1/evidence/{evidence_id}` | Retrieve evidence metadata |
| `GET` | `/api/v1/evidence/{evidence_id}/provenance` | Retrieve source provenance |
| `GET` | `/api/v1/evidence/{evidence_id}/history` | Retrieve available evidence history |

Evidence should expose its classification, source reference, snapshot, observation time, and known limitations where appropriate.

Source-derived evidence must not be editable through a general-purpose evidence update endpoint. Siddhi-owned assessments and mappings should use their own resources.

### 5.10 Deterministic analysis

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/analysis-runs` | Request a deterministic analysis |
| `GET` | `/api/v1/analysis-runs` | List analysis runs |
| `GET` | `/api/v1/analysis-runs/{run_id}` | Retrieve analysis status and metadata |
| `GET` | `/api/v1/analysis-runs/{run_id}/findings` | Retrieve findings |
| `GET` | `/api/v1/analysis-runs/{run_id}/report` | Retrieve a report |
| `POST` | `/api/v1/analysis-runs/{run_id}/cancel` | Request cancellation when supported |

The request must identify the analysis type, scope, and applicable input references or selection policy. The backend should record the exact inputs used.

### 5.11 External analysis

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/external-analysis-requests` | Create an external analysis request |
| `GET` | `/api/v1/external-analysis-requests` | List requests |
| `GET` | `/api/v1/external-analysis-requests/{request_id}` | Retrieve request status and metadata |
| `GET` | `/api/v1/external-analysis-requests/{request_id}/result` | Retrieve the validated result |
| `POST` | `/api/v1/external-analysis-requests/{request_id}/review` | Record a human review |

External analysis requests must pass disclosure-policy checks before provider submission. Provider credentials and unrestricted provider configuration must not be exposed through the API.

### 5.12 Reports

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/reports` | List available reports |
| `GET` | `/api/v1/reports/{report_id}` | Retrieve report metadata and content |
| `POST` | `/api/v1/reports` | Request report generation where supported |

Reports should preserve the snapshot and analysis references used to produce them.

The initial release should avoid duplicating the report-generation functionality already available through analysis-run resources unless a separate reusable report model is justified.

---

## 6. Request and response contracts

### 6.1 Request validation

Every write or action endpoint must validate its request using an explicit schema.

Validation should cover:

- Required fields.
- Field types and length limits.
- Allowed enum values.
- Identifier formats.
- Referential integrity.
- Lifecycle transitions.
- Scope and resource limits.
- Authorization and disclosure constraints.

FastAPI response models can validate serialized responses and publish their schemas through OpenAPI. This is useful for keeping the API contract machine-readable and supporting client generation. <Link url="https://fastapi.tiangolo.com/tutorial/response-model/" title="FastAPI response model documentation"/>.

### 6.2 Response envelope

Ordinary resource responses should use a consistent representation, but the API need not wrap every response in an artificial envelope if a direct resource representation is clearer.

A resource response should provide:

- Stable resource ID.
- Resource fields.
- Relevant lifecycle status.
- Revision or version information where applicable.
- Timestamps where meaningful.
- Related-resource references where useful.

Collection responses should include the items and pagination metadata required by the selected pagination method.

### 6.3 Example: create a goal

Illustrative request:

```http
POST /api/v1/goals
Content-Type: application/json
```

```json
{
  "title": "Establish a reusable engineering capability",
  "intended_outcome": "Enable multiple portfolio initiatives",
  "description": "A proposed example goal",
  "priority": "medium"
}
```

Illustrative response:

```http
HTTP/1.1 201 Created
Location: /api/v1/goals/goal_123
```

```json
{
  "id": "goal_123",
  "title": "Establish a reusable engineering capability",
  "intended_outcome": "Enable multiple portfolio initiatives",
  "description": "A proposed example goal",
  "priority": "medium",
  "status": "active",
  "revision": 1
}
```

The identifiers and values are examples, not prescribed production values. The final schema must follow the approved domain model.

### 6.4 Example: request ingestion

Illustrative request:

```http
POST /api/v1/sources/source_123/refresh
Content-Type: application/json
```

```json
{
  "mode": "incremental",
  "reason": "Portfolio review preparation"
}
```

Illustrative response for asynchronous execution:

```http
HTTP/1.1 202 Accepted
Location: /api/v1/ingestion-runs/run_456
```

```json
{
  "run_id": "run_456",
  "source_id": "source_123",
  "status": "queued",
  "status_url": "/api/v1/ingestion-runs/run_456"
}
```

The API must return `202 Accepted` only when the request has been accepted for processing but has not yet completed. If the operation is synchronous and complete, it should return the appropriate completed response instead.

### 6.5 Response models and internal models

API request and response models should be separate from database models and, where necessary, domain entities.

This prevents internal refactoring from accidentally changing the public contract and allows the API to omit sensitive or internal fields.

---

## 7. Error handling

The API must return consistent, documented error responses.

### 7.1 Error format

The initial contract should use a structured error representation containing:

- Stable error code.
- Human-readable summary.
- Optional field-level validation details.
- Request correlation ID.
- Safe remediation guidance where useful.

Illustrative example:

```json
{
  "error": {
    "code": "SOURCE_NOT_ACCESSIBLE",
    "message": "The configured source could not be accessed.",
    "details": [],
    "request_id": "req_789"
  }
}
```

The API must not expose stack traces, credentials, private source content, or internal implementation details in production error responses.

### 7.2 HTTP status codes

Use semantically appropriate HTTP status codes.

| Status | Intended use |
|---|---|
| `200 OK` | Successful read or completed operation |
| `201 Created` | A new resource was created |
| `202 Accepted` | An asynchronous operation was accepted |
| `204 No Content` | Successful operation with no response body |
| `400 Bad Request` | Malformed or invalid request |
| `401 Unauthorized` | Missing or invalid authentication |
| `403 Forbidden` | Operation is not permitted |
| `404 Not Found` | Resource does not exist or is not visible to the caller |
| `409 Conflict` | State conflict or invalid transition |
| `412 Precondition Failed` | A concurrency precondition failed |
| `413 Content Too Large` | Request exceeds configured size limits |
| `422 Unprocessable Content` | Valid request representation that fails semantic validation |
| `429 Too Many Requests` | Rate or usage limit exceeded |
| `500 Internal Server Error` | Unexpected server failure |
| `503 Service Unavailable` | Temporarily unavailable service or required dependency |

The exact mapping between validation errors and `400` or `422` should be consistent throughout the API. FastAPI's default validation behavior may be retained if documented.

### 7.3 Domain errors versus HTTP errors

Application services should produce typed domain or application errors. The API layer should map these to HTTP responses.

Domain logic must not depend on HTTP status codes.

### 7.4 Partial success

For operations that can process multiple records, the response must distinguish complete success from partial success.

For asynchronous ingestion and analysis, partial outcomes should generally be represented in the run resource rather than hidden inside a generic successful response.

---

## 8. Asynchronous operations and job management

Some operations may take longer than a normal HTTP request, including:

- Source discovery.
- Ingestion.
- Reconciliation scans.
- Large historical comparisons.
- Deterministic analysis over large evidence sets.
- External AI requests.
- Large report generation.

### 8.1 Initial execution model

The initial implementation may use a lightweight background-job mechanism within the backend process.

The job mechanism should persist enough state to report progress and recover safely after a restart where supported.

A full distributed task queue is not required unless actual workload or reliability requirements justify it.

### 8.2 Job resource

A long-running operation should expose:

- Job or run ID.
- Operation type.
- Current status.
- Start and completion times.
- Progress information when reliably measurable.
- Current stage where useful.
- Result resource reference.
- Safe error summary.
- Cancellation support, if implemented.

Progress percentages must not be fabricated when the total work is unknown.

### 8.3 Restart behavior

If the backend restarts during an operation, it must reconcile the persisted run state.

A run must not remain indefinitely marked as running when the system can determine that it was interrupted. Safe retries must respect the ingestion and snapshot guarantees defined in `ingestion-and-snapshots.md`.

### 8.4 Cancellation

Cancellation must be an explicit operation and should be supported only where the underlying work can stop safely.

A cancellation request does not prove that all processing has stopped immediately. The API must report the final outcome.

---

## 9. Idempotency and concurrency

### 9.1 Idempotent actions

Where duplicate requests could cause duplicate work or duplicate records, the API should support idempotency keys or an equivalent request-deduplication mechanism.

Potential candidates include:

- Starting ingestion.
- Creating an external analysis request.
- Requesting expensive report generation.
- Creating a decision from an approved recommendation.

The implementation should define the scope and retention of idempotency keys.

### 9.2 State-changing operations

Operations that modify important portfolio state must validate the current state and applicable preconditions.

For example:

- A recommendation cannot be approved if it has already been superseded.
- A plan revision must be based on an appropriate current plan revision.
- A source snapshot cannot be published if it fails publication requirements.
- A goal cannot be marked achieved merely by changing its status field if its acceptance policy requires additional checks.

These controls must be enforced by the backend, not only by frontend workflows.

### 9.3 Optimistic concurrency

For resources that may be updated concurrently, the API should use resource revision numbers, ETags, or another documented concurrency mechanism.

Conflicting updates should return a clear conflict response and allow the client to reload or reconcile the current state.

---

## 10. API security

### 10.1 Local-first deployment

The initial deployment is expected to be local-first, with the desktop frontend communicating with a backend on the same machine.

The service should bind only to the intended local interface by default. It must not expose itself to the local network or the public internet unless a separate deployment policy explicitly permits this.

Localhost binding alone is not a complete authorization model. Other local processes may be able to attempt requests.

### 10.2 Authentication

The authentication mechanism for the desktop client remains an open design decision.

Possible approaches include a locally provisioned application token, a secure local session mechanism, or another suitable desktop-to-backend authorization method.

The implementation must avoid hard-coded shared secrets and must not place credentials in URLs.

The selected mechanism must be compatible with the desktop application's lifecycle, backend startup, and recovery behavior.

### 10.3 Authorization

Every state-changing endpoint must check that the caller is authorized to perform the operation.

If Siddhi is initially a single-user local application, the first implementation may use a simple authorization model, but it must not make future access-control requirements impossible to introduce.

### 10.4 CORS and browser access

CORS should be restricted to the actual frontend origins that need access. It must not be configured as unrestricted simply to make local development easier.

The backend should validate sensitive state-changing requests independently of CORS.

### 10.5 Filesystem and source access

The API must not accept arbitrary filesystem paths and then read them without validation.

Source registration and refresh operations must validate configured locations, enforce allowed scope, and use the source adapters' read-only rules.

The API must not expose arbitrary command execution or general-purpose shell access.

### 10.6 External providers

Provider credentials and external analysis context must be handled by backend services. The frontend must not receive provider secrets or directly submit privileged requests using them.

Security controls should follow established REST guidance on authorization, safe error handling, input validation, and endpoint exposure. <Link url="https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html" title="OWASP REST Security Cheat Sheet"/>.

---

## 11. API documentation and contract governance

### 11.1 OpenAPI

The API should publish a machine-readable OpenAPI document.

FastAPI's OpenAPI integration should be used to document:

- Endpoints.
- HTTP methods.
- Request and response schemas.
- Authentication requirements.
- Error responses.
- Query parameters.
- Resource lifecycle semantics.

Interactive documentation should be configurable and may be restricted or disabled in production deployments where appropriate.

### 11.2 Contract ownership

The backend owns the API contract.

The frontend should consume generated or shared contract definitions rather than independently inventing request and response types.

TypeScript client types may be generated from the OpenAPI specification, or generated artifacts may be maintained through a controlled build process.

The generated client must not become a second, independently edited definition of the contract.

### 11.3 Contract changes

Changes should be classified as:

- Additive and backward-compatible.
- Behavior-changing but schema-compatible.
- Breaking.
- Deprecated.

Breaking changes require an explicit migration plan. Deprecated endpoints should have documented replacement paths and a defined removal policy.

### 11.4 Contract tests

Automated tests must verify that actual endpoint behavior matches the published schema and documented semantics.

The API contract must be reviewed whenever domain models, workflows, or security requirements change.

---

## 12. Observability and diagnostics

The API should provide:

- Request correlation IDs.
- Structured logs.
- Operation duration.
- HTTP status counts.
- Error classification.
- Ingestion and analysis run references.
- Safe diagnostics for failed operations.
- Health and readiness endpoints.

Logs must not expose credentials, full confidential source content, or sensitive external analysis payloads unnecessarily.

Request IDs should be propagated into related application operations and run records where practical, allowing an operator to trace an API request through ingestion or analysis without logging the entire payload.

---

## 13. Testing requirements

The API must be tested for:

1. Request schema validation.
2. Response schema validation.
3. Correct HTTP status codes.
4. Error response consistency.
5. Pagination and filtering.
6. Missing and invalid resource identifiers.
7. Invalid lifecycle transitions.
8. Optimistic concurrency conflicts.
9. Duplicate and retried requests.
10. Authorization of state-changing operations.
11. Source configuration and path validation.
12. Ingestion job status and recovery.
13. Snapshot publication restrictions.
14. Analysis run creation and retrieval.
15. External analysis disclosure checks.
16. Recommendation review and decision separation.
17. API behavior during source-provider outages.
18. Database transaction failures.
19. Request-size and resource limits.
20. CORS and local-interface configuration.
21. OpenAPI contract consistency.
22. Client compatibility with documented responses.
23. Protection against information leakage in errors and logs.
24. Backend restart during long-running operations.

Tests should include both unit tests for application services and integration tests that exercise the API against a temporary database and controlled source fixtures.

---

## 14. Acceptance criteria

The initial API is ready when:

- The API has a documented, versioned base path.
- Resource contracts reflect the approved Siddhi domain model.
- Clients cannot access SQLite directly through the intended application architecture.
- Request and response models are explicit and validated.
- Source-owned data cannot be silently overwritten through Siddhi portfolio endpoints.
- State transitions and approval rules are enforced in the backend.
- Long-running operations expose durable run identifiers and status.
- Errors use consistent schemas and appropriate HTTP status codes.
- Repeated actions can be handled safely where idempotency is required.
- Concurrent updates cannot silently overwrite protected revisions.
- Local deployment has a defined interface-binding and authentication policy.
- Source access and external analysis are protected by backend controls.
- OpenAPI accurately describes the implemented contract.
- Automated tests validate API behavior against that contract.
- The API remains usable for routine deterministic operations when external AI providers are unavailable.

---

## 15. Implementation phases

### Phase 1 — API foundation

Implement:

- FastAPI application setup.
- Versioned route structure.
- Request and response models.
- Standard error handling.
- Health and readiness endpoints.
- OpenAPI publication.
- API tests.

**Deliverable:** A stable API foundation with no direct frontend-to-database access.

### Phase 2 — Core portfolio resources

Implement:

- Goals.
- Initiatives.
- Project references.
- Plans and revisions.
- Milestones.
- Dependencies.
- Decisions.

**Deliverable:** The API can support basic portfolio management through validated application services.

### Phase 3 — Sources, ingestion, and evidence

Implement:

- Source configurations.
- Ingestion runs.
- Snapshot metadata.
- Evidence retrieval.
- Provenance and coverage.
- Refresh and status workflows.

**Deliverable:** The API can expose source ingestion and traceable evidence.

### Phase 4 — Deterministic analysis and reports

Implement:

- Analysis run creation.
- Findings and report retrieval.
- Historical comparisons.
- Goal-specific assessment workflows.

**Deliverable:** The API can support evidence-driven portfolio reviews.

### Phase 5 — External analysis and approval

Implement:

- External analysis requests.
- Request status and result retrieval.
- Recommendation review.
- Decision linkage.
- Disclosure-policy enforcement.

**Deliverable:** Advisory analysis is accessible without bypassing portfolio approval rules.

### Phase 6 — Desktop integration hardening

Implement:

- Desktop-to-backend authentication.
- Concurrency controls.
- Idempotency where required.
- Contract-generated TypeScript client.
- Restart and recovery tests.
- Operational diagnostics.

**Deliverable:** The backend exposes a stable contract for the future desktop frontend.

---

## 16. Open questions

| ID | Question | Why it matters |
|---|---|---|
| API-001 | Should the API initially be local-only, or must it support remote clients from the first release? | Determines network and security architecture |
| API-002 | What authentication mechanism should the desktop client use to communicate with the local backend? | Prevents unauthorized local access |
| API-003 | Should pagination use offset-based or cursor-based pagination? | Affects consistency and implementation complexity |
| API-004 | Which operations require background execution in the first release? | Defines the initial job model |
| API-005 | Should API request and response fields use `snake_case` or `camelCase`? | Establishes a stable client contract |
| API-006 | Which resources require optimistic concurrency control? | Protects against conflicting edits |
| API-007 | Which state-changing operations require idempotency keys? | Prevents duplicate work |
| API-008 | Should interactive API documentation be enabled in packaged desktop builds? | Balances developer convenience and deployment hardening |
| API-009 | What is the minimum supported API versioning and deprecation policy? | Controls future compatibility |
| API-010 | Should generated TypeScript clients be committed to the frontend repository or generated during the build? | Determines contract synchronization workflow |
| API-011 | Which resources should support deletion, archival, or soft deletion? | Affects history and data integrity |
| API-012 | What are the request, response, pagination, and job limits for the initial release? | Prevents resource exhaustion |

---

## 17. Related documentation

- `vision.md`
- `scope-and-roadmap.md`
- `functional-requirements.md`
- `non-functional-requirements.md`
- `system-architecture.md`
- `architectural-decisions.md`
- `domain-model.md`
- `data-model.md`
- `data-ownership.md`
- `application-workflows.md`
- `source-integration.md`
- `ingestion-and-snapshots.md`
- `deterministic-analysis.md`
- `external-analysis.md`
- `security-and-privacy.md`

## 18. Reference material

- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/) — response validation, schema generation, and OpenAPI integration.
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/) — authentication mechanisms and security integration with OpenAPI.
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) — authorization, input handling, error responses, CORS, and endpoint protection.

These references inform the API design. They do not determine the final local authentication mechanism, endpoint inventory, or deployment policy.

**Document status:** Draft for review. The resource contracts, local authentication model, background-job strategy, and concurrency policy must be confirmed before this document is converted into implementation-level OpenSpec requirements.