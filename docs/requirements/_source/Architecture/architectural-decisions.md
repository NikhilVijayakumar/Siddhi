# Siddhi API — Architectural Decisions

**Product:** Siddhi (सिद्धि)  
**Document:** `architectural-decisions.md`  
**Status:** Draft for review  
**Version:** 0.1  
**Related documents:** `vision.md`, `scope-and-roadmap.md`, `system-architecture.md`, `non-functional-requirements.md`

## 1. Purpose

This document records significant architectural decisions for Siddhi API.

Each decision explains:

- The problem or context.
- The chosen approach or current proposal.
- The alternatives considered.
- The consequences and trade-offs.
- The status of the decision.

The purpose is to make architectural reasoning explicit, prevent previously rejected approaches from being reconsidered without context, and support informed changes as Siddhi evolves.

This document is a consolidated decision register. Individual decisions may later be moved into separate architecture decision records (ADRs) if the project benefits from maintaining them independently.

## 2. Decision Status

Decisions use the following statuses:

- **Proposed:** Recommended but not yet confirmed by the project owner.
- **Accepted:** Explicitly approved and intended to guide implementation.
- **Superseded:** Replaced by a later decision.
- **Deferred:** Deliberately postponed until additional information is available.

A technically reasonable proposal must not be treated as an accepted decision until its status is changed.

## 3. Decision Summary

| ID | Decision | Current status |
|---|---|---|
| ADR-001 | Use Python for the backend | Proposed |
| ADR-002 | Use FastAPI for the HTTP API | Proposed |
| ADR-003 | Use SQLite for initial local storage | Proposed |
| ADR-004 | Build a modular monolith | Proposed |
| ADR-005 | Keep the desktop frontend in a separate project | Proposed |
| ADR-006 | Keep domain logic independent of the UI | Proposed |
| ADR-007 | Use adapters for external source systems | Proposed |
| ADR-008 | Preserve normalized source data and historical snapshots | Proposed |
| ADR-009 | Treat source systems as authoritative for their own data | Proposed |
| ADR-010 | Keep OpenSpec requirements and OKF knowledge independent | Accepted design principle |
| ADR-011 | Use deterministic processing for routine analysis | Accepted design principle |
| ADR-012 | Separate AI recommendations from approved decisions | Accepted design principle |
| ADR-013 | Use structured external AI handoffs initially | Proposed |
| ADR-014 | Keep routine source processing read-only | Accepted design principle |
| ADR-015 | Version schemas, rules, and generated reports | Proposed |
| ADR-016 | Introduce background jobs only where justified | Proposed |
| ADR-017 | Use explicit database migrations | Proposed |
| ADR-018 | Do not require manual time logging | Accepted design principle |
| ADR-019 | Use API contracts to support independent frontend development | Proposed |
| ADR-020 | Keep deployment local-first initially | Proposed |

The accepted design principles above reflect the previously established product direction. The implementation-specific choices remain proposals pending review.

---

## ADR-001 — Use Python for the Backend

**Status:** Proposed

### Context

Siddhi needs source parsing, data normalization, deterministic analysis, report generation, database operations, and optional AI integration.

These workloads benefit from a language ecosystem with strong support for data processing, validation, automation, and AI tooling.

### Decision

Use Python as the primary backend language.

### Alternatives considered

- **Kotlin with Spring Boot:** Strong application architecture, type safety, and mature enterprise backend capabilities.
- **TypeScript with Node.js:** Could align backend and frontend languages, but would not necessarily simplify the data-processing and AI integration workloads.
- **Python with FastAPI:** Provides a direct fit for data-oriented services and API development.

### Rationale

Python offers a practical balance between parsing diverse engineering artifacts, implementing deterministic rules, integrating external AI tools, and building a testable API.

### Consequences

- The backend requires Python dependency and environment management.
- Static typing, validation, linting, and tests should be used to maintain reliability.
- The frontend remains free to use TypeScript.
- Core business rules must not rely on dynamic behavior that makes their outcomes difficult to test.

## ADR-002 — Use FastAPI for the HTTP API

**Status:** Proposed

### Context

The future desktop application needs a stable HTTP interface. The backend also benefits from request validation and automatically generated API documentation.

### Decision

Use FastAPI with Pydantic models for request and response validation.

### Alternatives considered

- Flask.
- Django and Django REST Framework.
- A backend exposing only command-line interfaces.
- Direct database access from the frontend.

### Rationale

FastAPI provides an API-focused framework, validation, and OpenAPI generation without requiring a large web-platform framework.

### Consequences

- API schemas must be maintained deliberately.
- Business rules must remain outside route handlers.
- API behavior must be tested independently of the frontend.
- The generated OpenAPI specification becomes an important integration contract.

## ADR-003 — Use SQLite for Initial Storage

**Status:** Proposed

### Context

The initial Siddhi deployment is intended to be local-first and single-user. It must retain goals, plans, source snapshots, reports, and decisions without requiring a database server.

### Decision

Use SQLite as the initial database.

### Alternatives considered

- PostgreSQL.
- MongoDB.
- Cloud-hosted database services.
- Files-only persistence.

### Rationale

SQLite reduces deployment complexity and provides transactions, relational integrity, and durable local storage suitable for the initial use case.

### Consequences

- Database access must be isolated behind a persistence layer.
- Write concurrency and long-running transactions must be managed carefully.
- Migrations and backups must be explicit.
- Historical data growth must be measured.
- Moving to a server database later remains possible but is not guaranteed to be a zero-effort change.

The database schema should avoid unnecessary coupling to SQLite-specific behavior where practical.

## ADR-004 — Use a Modular Monolith

**Status:** Proposed

### Context

Siddhi has distinct responsibilities—source integration, ingestion, portfolio management, analysis, reporting, and external AI integration—but the initial workload does not justify separate services for each responsibility.

### Decision

Implement the backend as one deployable Python application with clear internal module boundaries.

### Alternatives considered

- Microservices.
- Multiple independently deployed services.
- A single unstructured application module.

### Rationale

A modular monolith provides straightforward deployment and debugging while preserving the ability to test and evolve individual components.

### Consequences

- Modules need explicit responsibilities and dependency boundaries.
- Shared database access must be coordinated.
- Internal module separation must not be confused with separate process or service boundaries.
- Services should only be extracted if actual scale, deployment, or isolation requirements justify it.

## ADR-005 — Keep the Desktop Frontend Separate

**Status:** Proposed

### Context

Siddhi's initial work focuses on backend functionality. The future UI is planned as React, TypeScript, MUI, and Electron.

### Decision

Develop the API and desktop application as separate projects with an explicit HTTP API contract.

### Alternatives considered

- Build the frontend and backend in one coupled application.
- Put portfolio business rules directly into the Electron frontend.
- Develop a desktop application that directly accesses SQLite.

### Rationale

Separating the projects enables backend testing before the UI exists and avoids coupling portfolio behavior to desktop implementation details.

### Consequences

- API contracts must be designed for independent consumption.
- The desktop application must not access the database directly.
- Local service startup, shutdown, access control, and packaging need explicit design.
- Frontend and backend release compatibility must be managed.

## ADR-006 — Keep Domain Logic Independent of the UI

**Status:** Proposed

### Context

Siddhi may eventually support other API clients, automation, or a web interface.

### Decision

Keep portfolio rules, source interpretation, and deterministic analysis independent of React and Electron.

### Alternatives considered

- Implementing business rules in the frontend.
- Coupling domain services to HTTP request objects.
- Combining data access and business logic in route handlers.

### Rationale

UI-independent logic is easier to test, reuse, and change without breaking the frontend.

### Consequences

- Use application-level operations to coordinate workflows.
- Keep transport-specific models separate from core domain concepts where useful.
- Test domain rules without launching the API server.

## ADR-007 — Use Adapters for External Source Systems

**Status:** Proposed

### Context

Siddhi consumes data from Vyasa, OpenSpec, OKF, Git/VCS, and structured repository artifacts. These sources have different access methods and data formats.

### Decision

Implement explicit adapters for external systems and source formats.

### Alternatives considered

- Embedding source-specific logic throughout the application.
- Assuming every repository uses identical schemas.
- Requiring an AI agent to interpret all sources.

### Rationale

Adapters isolate external changes and make parsers independently testable.

### Consequences

- Each adapter needs a defined contract and failure model.
- Supported formats and versions must be explicit.
- Unsupported formats must be reported rather than silently interpreted.
- Integration tests should use representative fixtures and controlled source responses.

## ADR-008 — Preserve Source Snapshots and Provenance

**Status:** Proposed

### Context

Portfolio analysis must be explainable over time. Source data changes, repositories become unavailable, and analysis rules evolve.

### Decision

Store normalized source observations, identifiable snapshots, and provenance sufficient to explain the evidence used in analysis.

### Alternatives considered

- Keeping only the latest source state.
- Storing only repository URLs.
- Storing only generated summaries.
- Copying all source repositories into Siddhi.

### Rationale

Historical snapshots allow Siddhi to compare changes and explain why findings differ. Provenance connects normalized information to its source.

### Consequences

- Storage and retention policies are required.
- Source identity and revision mapping must be stable.
- Historical records must distinguish observed state from current state.
- Sensitive source content should not be copied unnecessarily.
- Hashes and references may be sufficient for some records, while selected normalized fields may need durable storage.

The exact balance between normalized content, source references, and retained snapshots remains to be defined.

## ADR-009 — Preserve Source Authority

**Status:** Proposed

### Context

Siddhi aggregates information from systems that already own specific records.

### Decision

Each source system remains authoritative for its own domain. Siddhi maintains portfolio-owned information and derived projections rather than replacing those sources.

### Alternatives considered

- Making Siddhi the master database for every source.
- Editing source artifacts automatically to synchronize all information.
- Maintaining duplicate, independently editable copies.

### Rationale

Clear ownership prevents conflicting records and unnecessary synchronization complexity.

### Consequences

- Source data must retain provenance.
- Source updates and Siddhi-owned changes must be handled separately.
- Repository writes require an explicit authorized workflow.
- Cached data may be stale and must be labeled accordingly.

## ADR-010 — Keep OpenSpec and OKF Independent

**Status:** Accepted design principle

### Context

OpenSpec describes requirements and development artifacts, while OKF captures engineering knowledge. Knowledge can exist independently of a current requirement, and requirements can exist before sufficient knowledge is documented.

### Decision

Treat OpenSpec and OKF as independent source systems. Allow cross-references without requiring one to depend on the other.

### Alternatives considered

- Requiring every OKF knowledge item to originate from an OpenSpec requirement.
- Treating all knowledge as requirement attachments.
- Treating requirements as a complete representation of engineering knowledge.

### Rationale

Requirements and knowledge serve different purposes and have different lifecycles.

### Consequences

- The ingestion model must support independent discovery and refresh.
- Missing knowledge and missing requirements must be assessed separately.
- Relationships should be explicit or derived through documented rules.
- Parsing either source must not require the other to exist.

## ADR-011 — Use Deterministic Processing for Routine Analysis

**Status:** Accepted design principle

### Context

Routine source ingestion, normalization, comparison, and report generation should be reliable and repeatable without repeated AI calls.

### Decision

Implement routine processing using explicit code and defined rules. Use AI only when deeper synthesis or judgment is needed.

### Alternatives considered

- Using an AI agent for every source refresh.
- Generating all portfolio reports through free-form model output.
- Mixing deterministic calculations with undocumented model judgments.

### Rationale

Deterministic processing reduces unnecessary cost, improves repeatability, and makes errors easier to diagnose.

### Consequences

- Rules must be explicit and testable.
- Findings must distinguish candidates from established relationships.
- AI-assisted results must be labeled and preserved separately.
- Deterministic output does not imply that the underlying source data is correct.

## ADR-012 — Separate Recommendations from Approved Decisions

**Status:** Accepted design principle

### Context

External analysis may recommend changes to portfolio priorities, investments, or plans. Those recommendations can be useful but are not automatically authoritative.

### Decision

Represent recommendations, proposed decisions, approved decisions, and known execution outcomes as distinct concepts.

### Alternatives considered

- Automatically applying AI recommendations.
- Treating imported reports as approved plans.
- Overwriting an existing plan whenever a new recommendation arrives.

### Rationale

The portfolio owner must retain control of consequential choices, and decision history must remain explainable.

### Consequences

- Approval state must be explicit.
- Plan revisions must preserve prior versions.
- Imported recommendations must retain provenance and uncertainty.
- Publishing changes to repositories requires separate authorization.

## ADR-013 — Start with Structured External AI Handoffs

**Status:** Proposed

### Context

Siddhi needs deeper strategic reasoning for prioritization and trade-offs, but should not depend on one AI provider or make routine operations dependent on a model.

### Decision

Initially support exporting structured evidence briefs and importing structured analysis results. Add direct provider integrations only when justified.

### Alternatives considered

- Integrating multiple AI providers immediately.
- Depending on one provider's proprietary API.
- Using an agent for every portfolio operation.
- Having no external analysis capability.

### Rationale

A structured handoff provides a useful initial workflow while preserving provider independence.

### Consequences

- Input and output schemas must be defined.
- Imported results require validation and provenance.
- The user may need to perform some handoff steps manually initially.
- Provider-specific adapters can be introduced later.

## ADR-014 — Keep Routine Source Processing Read-Only

**Status:** Accepted design principle

### Context

OpenSpec, OKF, Git, and repository artifacts are authoritative sources. Siddhi's routine purpose is to inspect and interpret them.

### Decision

Routine ingestion and analysis must not modify source repositories.

### Alternatives considered

- Automatically writing generated summaries into repositories.
- Automatically updating OpenSpec status.
- Allowing ingestion to trigger arbitrary repository commands.

### Rationale

Read-only processing limits accidental changes and preserves source ownership.

### Consequences

- Source adapters should avoid write permissions where possible.
- Future publishing workflows must be explicit, authorized, and separately tested.
- Repository content must be treated as untrusted input.

## ADR-015 — Version Schemas, Rules, and Generated Reports

**Status:** Proposed

### Context

Source formats and analysis rules will evolve. Historical reports must remain interpretable when the implementation changes.

### Decision

Version relevant database schemas, supported source formats, analysis rules, and generated artifact structures.

### Alternatives considered

- Treating every report as timeless.
- Silently reinterpreting historical records with the latest rules.
- Using unversioned JSON structures for persistent artifacts.

### Rationale

Versioning supports migration, reproducibility, and controlled evolution.

### Consequences

- Version compatibility rules must be documented.
- Historical reports must retain relevant version metadata.
- Changes to source parsers or rules may require explicit reprocessing.
- Migration and compatibility tests become part of the development workflow.

## ADR-016 — Introduce Background Jobs Only Where Justified

**Status:** Proposed

### Context

Some operations, particularly repository ingestion and large analyses, may take longer than a typical HTTP request.

### Decision

Keep short operations synchronous where appropriate. Introduce background-job execution and persisted job status for operations that need it.

### Alternatives considered

- Running all operations synchronously.
- Introducing a distributed job queue immediately.
- Making every application operation asynchronous.

### Rationale

The approach balances simplicity with responsiveness and recoverability.

### Consequences

- Long-running operation boundaries must be identified.
- Job status, retries, cancellation, and failure behavior need defined semantics.
- A persistent job mechanism may be needed if interruption recovery is required.
- The initial implementation should avoid adding a message broker without demonstrated need.

## ADR-017 — Use Explicit Database Migrations

**Status:** Proposed

### Context

Siddhi's schema will evolve as portfolio concepts, source observations, and analysis history become more detailed.

### Decision

Use versioned database migrations with automated validation.

### Alternatives considered

- Manually altering the database during development.
- Recreating the database whenever the schema changes.
- Allowing the application to make untracked schema changes automatically.

### Rationale

Explicit migrations preserve user data and make upgrades reproducible.

### Consequences

- Migration history must be tracked.
- Upgrades must be tested against representative previous schemas.
- Migration failure behavior and backup requirements must be documented.
- Development convenience must not bypass production-safe migration behavior.

## ADR-018 — Do Not Require Manual Time Logging

**Status:** Accepted design principle

### Context

The purpose of Siddhi is portfolio intelligence and outcomes, not employee time tracking.

### Decision

The backend must not require manual hours-per-task or hours-per-project logging.

### Alternatives considered

- Mandatory time sheets.
- Estimating effort from commit counts alone.
- Inferring exact working time from source history.

### Rationale

Time logging adds overhead and does not reliably measure value or progress.

### Consequences

- Planning and review rely on goals, milestones, artifacts, and available evidence.
- Actual effort may remain unknown.
- The system must not infer precise working hours from activity metadata.

## ADR-019 — Maintain a Stable API Contract

**Status:** Proposed

### Context

The backend and future desktop frontend will be developed as separate projects.

### Decision

Use documented API schemas and explicit compatibility practices.

### Alternatives considered

- Sharing internal Python models directly with the frontend.
- Allowing frontend code to access SQLite.
- Defining endpoints only when the UI requires them without a contract strategy.

### Rationale

An explicit contract supports independent implementation and automated integration testing.

### Consequences

- Request and response schemas must be validated.
- Breaking changes must be managed deliberately.
- The generated OpenAPI specification should be tested and reviewed.
- Internal database schemas must not automatically become public API contracts.

## ADR-020 — Keep the Initial Deployment Local-First

**Status:** Proposed

### Context

The initial system is intended for a single portfolio owner and local development workflows.

### Decision

Start with a local Python service, local SQLite storage, and explicitly configured source access.

### Alternatives considered

- Mandatory cloud hosting.
- Multi-tenant hosted architecture from the beginning.
- Distributed services and remote database infrastructure.

### Rationale

A local-first deployment reduces operating complexity and keeps portfolio data under the owner's control.

### Consequences

- The service lifecycle and database location must be clear.
- Backups and recovery must be documented.
- Remote integrations may still require network access.
- Local API security remains necessary.
- Multi-user or cloud deployment requires a future design review rather than being assumed to work automatically.

---

## 4. Decisions Requiring Early Owner Review

The following proposals have the greatest impact on the implementation and should be resolved before the corresponding work begins.

### 4.1 Backend technology

Confirm Python + FastAPI as the initial backend stack.

### 4.2 Persistence

Confirm SQLite as the first database and decide whether an ORM or a lighter data-access approach is appropriate.

### 4.3 Source access

Determine whether the first release must support remote-only repositories or may initially use local checkouts already registered in Vyasa.

### 4.4 Snapshot retention

Determine which normalized source records and historical snapshots must be stored, which can be reconstructed, and what retention policy is required.

### 4.5 Background operations

Determine whether source refresh and analysis need persistent job tracking in the first release.

### 4.6 Local security

Determine which clients can access the local API and what protection is required beyond binding to loopback.

### 4.7 First usable release

Confirm whether the first end-to-end release must stop at deterministic goal-to-evidence reports or also include plan creation and review workflows.

## 5. How Decisions Are Changed

An accepted decision should not be silently edited when the implementation changes.

When a decision is reconsidered:

1. Record the new context or evidence.
2. Explain why the existing decision no longer fits.
3. Compare the relevant alternatives.
4. Document the proposed replacement.
5. Record the approval and consequences.
6. Mark the old decision as superseded and reference its replacement.

This preserves architectural history and prevents future maintainers from losing the reasoning behind significant choices.

## 6. Relationship to OpenSpec and OKF

This document records the reasoning behind architectural choices. It does not replace either requirements or engineering knowledge.

- **OpenSpec** should capture required system behavior, including acceptance criteria for architectural constraints that affect observable behavior.
- **OKF** should capture reusable technical knowledge, architecture concepts, implementation guidance, and relevant design rationale.
- **Architectural decisions** should retain the specific context, alternatives, consequences, and approval status for each choice.

A decision may be referenced from OpenSpec or OKF, but the same decision should not be independently maintained in conflicting versions across all three.

---

**End of architectural decisions document**
