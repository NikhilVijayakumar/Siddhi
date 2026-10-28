# Siddhi API — Scope and Roadmap

**Product:** Siddhi (सिद्धि)  
**Parent vision:** `vision.md`  
**Document:** `scope-and-roadmap.md`  
**Status:** Draft for review  
**Version:** 0.1

## 1. Purpose

This document defines the scope, boundaries, and proposed implementation roadmap for Siddhi API.

Siddhi API is the backend foundation of Siddhi, a portfolio intelligence and strategic planning system. It consolidates evidence from existing projects and engineering systems, manages portfolio-owned information, performs deterministic analysis, and exposes capabilities through an API.

The purpose of this document is to establish what the backend is responsible for, what it depends on, what it deliberately excludes, and in what order its capabilities should be developed.

Detailed behavior, acceptance criteria, data schemas, and engineering conventions will be documented and validated separately.

## 2. Scope Principles

The following principles govern scope decisions:

1. **Outcome-oriented:** Features should improve portfolio understanding, planning, decisions, or execution.
2. **Source-aware:** Existing systems remain authoritative for information they own.
3. **Deterministic by default:** Routine processing must not require a coding agent or external AI.
4. **Incremental delivery:** Establish reliable ingestion and core portfolio operations before introducing advanced strategic analysis.
5. **Evidence-based:** Distinguish source facts, derived results, external recommendations, and approved decisions.
6. **Modular architecture:** Source adapters, domain logic, analysis, persistence, and API delivery should have clear boundaries.
7. **Local-first initial implementation:** Start with a local SQLite database and a Python API, without requiring a hosted service.
8. **Human-controlled decisions:** Recommendations must not silently change portfolio priorities or modify repositories.
9. **Proportionate scope:** Avoid building infrastructure or features without a demonstrated portfolio need.

## 3. System Boundaries

### 3.1 Siddhi API owns

Siddhi API is responsible for:

- Portfolio goals, intended outcomes, and priorities.
- Initiatives, plans, milestones, dependencies, and portfolio relationships.
- Normalized representations of source information needed for portfolio analysis.
- Historical source snapshots and change records.
- Deterministic comparisons, evidence classifications, gap reports, and summaries.
- External analysis briefs and imported analysis results.
- Plan revisions, approved portfolio decisions, and review history.
- API contracts for the future desktop frontend.
- Provenance linking derived information to its sources and revisions.

### 3.2 Siddhi API consumes

Siddhi API consumes information from existing systems.

| Source | Intended use |
|---|---|
| Vyasa | Discover projects, repositories, locations, and available project metadata |
| OpenSpec | Understand requirements, scenarios, changes, tasks, and declared development status |
| OKF | Discover engineering knowledge, concepts, decisions, relationships, and declared validation metadata |
| Git/VCS | Gather revision history and other available development evidence |
| Repository artifacts | Read explicitly supported project summaries, investigation reports, and other structured evidence |
| External AI tools | Obtain optional strategic analysis and structured recommendations |

Actual integration formats, supported versions, access methods, and capabilities must be confirmed before implementation.

### 3.3 Siddhi API does not own

Siddhi API does not become the authoritative editor or replacement for:

- Vyasa's repository inventory.
- OpenSpec requirements and change artifacts.
- OKF knowledge packages.
- Git history or repository content.
- Existing implementation and test-verification results.

Siddhi may cache, normalize, compare, and reference these records. Refreshing them must not silently rewrite their authoritative sources.

## 4. Functional Scope

### 4.1 Portfolio management

The backend will manage:

- Goals and intended outcomes.
- Initiatives and their relationships to goals.
- Links to existing projects and repositories.
- Priorities, constraints, and relevant assumptions.
- Milestones, dependencies, and planned dates.
- Decisions, approvals, and decision rationale.
- Historical plans and reviews.

Goals must be allowed to exist before a project or repository is available. One initiative may support multiple goals, and one goal may depend on several initiatives.

### 4.2 Source ingestion

The backend will provide a consistent process to:

1. Discover source projects through Vyasa.
2. Access supported source artifacts.
3. Parse source data using the detected or configured schema/version.
4. Normalize supported information into Siddhi's internal representation.
5. Record source identity, revision or content hash, and ingestion metadata where available.
6. Detect additions, modifications, removals, and unchanged records.
7. Preserve historical snapshots.
8. Report unavailable sources, stale information, unsupported formats, and parsing failures explicitly.

Where a source cannot be refreshed, the last known data may be retained, but it must not be presented as current without qualification.

### 4.3 Project and knowledge intelligence

The backend will expose a consolidated view of:

- Project identity and repository references.
- Available OpenSpec requirements and development artifacts.
- Available OKF knowledge and associated metadata.
- Relevant revision and release evidence.
- Relationships between projects, goals, requirements, and capabilities.
- Missing, stale, unavailable, or unsupported information.

A requirement's existence does not prove implementation. An OKF package's existence does not prove its knowledge is complete or correct. Parsing and validation must be represented separately.

### 4.4 Deterministic analysis

The backend will provide reproducible analysis for:

- Goal-to-project and goal-to-capability comparisons.
- Candidate matches between goals and existing assets.
- Missing evidence and identified gaps.
- Declared development progress and available verification evidence.
- Source changes since a previous snapshot.
- Dependencies and potentially blocked outcomes.
- Portfolio summaries generated from stored data and defined templates.

Analysis must distinguish confirmed relationships from candidates and unresolved findings. A textual or keyword match alone must not establish that a goal is satisfied.

### 4.5 Planning and reviews

The backend will support:

- Initial plans and versioned revisions.
- Milestones, dependencies, and intended outcomes.
- Weekly execution-oriented reviews.
- Monthly portfolio and strategic reviews.
- Comparisons between current evidence and earlier plans.
- Recording approved changes and their rationale.
- Tracking unresolved risks, assumptions, and follow-up actions.

Siddhi will not require manual work-hour logging. Progress will instead use available project artifacts, milestones, snapshots, and explicitly supplied status information.

### 4.6 External analysis integration

The initial architecture will support a controlled workflow for external strategic reasoning:

1. Assemble an evidence-based brief from stored portfolio information.
2. Export or present the brief for use with a supported external AI tool or coding agent.
3. Import a structured analysis result.
4. Validate its structure and retain provenance, assumptions, evidence references, and uncertainty.
5. Present recommendations for review.
6. Record the owner's approved decision separately from the recommendation.

Automated calls to multiple AI providers, autonomous prioritization, and automatic execution of recommendations are not prerequisites for the first release.

### 4.7 API capabilities

The backend will expose documented HTTP APIs for the future React and Electron frontend.

The API will cover the domain capabilities that are implemented in each release, including portfolio operations, source refreshes, summaries, analysis reports, plans, and reviews.

The API contract will be versioned and testable independently of the frontend. Endpoint details will be established during API design and requirements definition.

## 5. Technical Scope

### 5.1 Initial technology direction

| Concern | Initial direction |
|---|---|
| Language | Python |
| API framework | FastAPI |
| Validation and data contracts | Pydantic |
| Initial database | SQLite |
| Persistence access | Dedicated repository/data-access layer |
| Database evolution | Versioned migrations |
| Testing | Automated unit, integration, and API contract tests |
| API documentation | OpenAPI generated from the API definitions |
| Source control | Git |
| Frontend | Separate future React + TypeScript + MUI + Electron project |

These choices are the proposed baseline. Detailed implementation decisions and constraints belong in architecture and engineering knowledge documentation.

### 5.2 Architectural boundaries

The implementation should separate:

- API routing and transport.
- Application use cases.
- Portfolio domain logic.
- Source adapters and parsing.
- Persistence and migrations.
- Deterministic analysis.
- Report generation.
- External AI integration.
- Configuration, security, and diagnostics.

The core domain and analysis logic should not depend directly on Electron or UI components.

### 5.3 Initial operating model

The initial target is a local application environment in which Siddhi API runs on the user's machine and stores portfolio-owned data in SQLite.

Repository access must respect configured boundaries and permissions. Remote source access should use supported APIs or other explicit access mechanisms rather than requiring unnecessary clones.

The exact startup, shutdown, packaging, and desktop integration approach will be finalized in the deployment design.

## 6. Explicit Non-Goals

The following are outside the initial scope unless separately justified and approved.

### 6.1 Not a replacement project-management platform

Siddhi is not intended to recreate every task, issue, sprint, or collaboration feature already available in existing development tools.

### 6.2 No mandatory time tracking

The backend will not require recording hours spent on individual tasks or projects.

### 6.3 No automatic repository modification

Source ingestion and analysis are read-oriented by default. Siddhi must not automatically commit code, change requirements, edit OKF knowledge, or publish plans to repositories without an explicit, authorized workflow.

### 6.4 No autonomous portfolio authority

External AI recommendations will not become approved priorities or binding plans without human approval.

### 6.5 No mandatory AI dependency for routine work

Source parsing, normalization, snapshot comparison, deterministic reports, and routine status aggregation must work without a coding agent.

### 6.6 No premature multi-user infrastructure

Distributed services, multi-tenant support, elaborate permission hierarchies, and mandatory cloud hosting are not initial requirements unless a demonstrated need changes the scope.

### 6.7 No universal product maturity framework

Siddhi will not require all commercial products, creative works, experiments, and internal tools to follow identical lifecycle stages.

### 6.8 No implementation-verification claims without evidence

Siddhi will not infer successful execution, testing, or release readiness solely from declared task completion or source-document presence.

## 7. Proposed Implementation Roadmap

The phases below establish a dependency-aware delivery sequence. Exact release boundaries and acceptance criteria will be defined through subsequent requirement analysis.

### Phase 0 — Documentation and design baseline

**Objective:** Establish a coherent and reviewed design before implementation.

Deliverables:

- Vision, scope, and functional overview.
- System boundaries and data ownership.
- Domain model and proposed data model.
- Source integration and ingestion design.
- API and persistence design.
- Security, testing, operations, and deployment guidance.
- Open questions, architectural decisions, and risk register.
- OpenSpec and OKF documentation conventions confirmed against the actual installed formats.

**Exit condition:** Major architectural boundaries are understood, critical assumptions are identified, and initial requirements are ready to be detailed.

### Phase 1 — Backend foundation

**Objective:** Establish a reliable, testable Python API.

Deliverables:

- Python package and application structure.
- Configuration and startup validation.
- FastAPI application and health endpoints.
- SQLite persistence foundation and migrations.
- Logging, diagnostics, error handling, and test infrastructure.
- Initial OpenAPI contract.
- CI validation for code quality and automated tests.

**Exit condition:** The service starts reliably, persists data, exposes documented endpoints, and passes baseline tests.

### Phase 2 — Source integration and ingestion

**Objective:** Reliably import available project and engineering evidence.

Deliverables:

- Vyasa inventory adapter.
- Repository and source identity mapping.
- OpenSpec parser for explicitly supported formats.
- OKF parser for explicitly supported formats.
- Git evidence adapter.
- Normalization and source provenance.
- Snapshot history and change detection.
- Explicit stale, unavailable, invalid, and unsupported states.

**Exit condition:** Supported sources can be ingested repeatedly, changes can be identified, and ingestion failures do not silently corrupt the last known state.

### Phase 3 — Portfolio domain and deterministic analysis

**Objective:** Make the imported evidence useful for portfolio decisions.

Deliverables:

- Goals, initiatives, and outcome management.
- Project and goal relationships.
- Milestones and dependencies.
- Portfolio summaries.
- Goal-to-project and goal-to-capability comparisons.
- Gap and evidence classification.
- Reproducible report generation.
- Historical comparisons.

**Exit condition:** A user can define a goal, compare it with available project evidence, and inspect a report that explains findings and uncertainty.

### Phase 4 — Planning, reviews, and decisions

**Objective:** Connect analysis with controlled portfolio planning.

Deliverables:

- Versioned initiative plans.
- Milestones and target dates.
- Weekly execution review data.
- Monthly portfolio review data.
- Decision records and approval status.
- Plan-versus-evidence comparisons.
- Rationale and history for plan revisions.

**Exit condition:** Plans can be reviewed and revised without losing previous versions or confusing recommendations with approved decisions.

### Phase 5 — External strategic analysis

**Objective:** Enable deeper analysis where deterministic rules are insufficient.

Deliverables:

- Structured evidence brief generation.
- Defined input and output schemas.
- Import and validation of external analysis results.
- Provenance, assumptions, uncertainty, and evidence references.
- Review and approval workflow.
- Optional provider adapters where justified.

**Exit condition:** External recommendations can be captured, traced, reviewed, and approved without making routine backend functionality depend on an AI provider.

### Phase 6 — Desktop integration readiness

**Objective:** Prepare the backend for a separate desktop application.

Deliverables:

- Stable and versioned API contracts.
- Authentication or other access controls appropriate to the local threat model.
- Controlled startup and shutdown.
- CORS and network exposure policies appropriate to the deployment model.
- Database backup and recovery procedures.
- Packaging and installation design.
- Integration tests against representative frontend workflows.

**Exit condition:** The backend can be operated predictably by a separate local desktop application, with documented lifecycle, access, and recovery behavior.

## 8. Dependencies and Constraints

The roadmap depends on several conditions.

- **Vyasa:** The integration must use a confirmed inventory contract rather than assume its current internal implementation.
- **OpenSpec:** Parsing must accommodate the actual installed schemas and artifact formats.
- **OKF:** The parser must follow the actual knowledge format and preserve the independence of knowledge from requirements.
- **Repository access:** Local and remote access methods may differ. Each must define permissions, availability, and failure handling.
- **External AI:** Provider access, output formats, privacy boundaries, and authorization must be defined before automated integrations are introduced.
- **SQLite:** The initial storage model must support historical snapshots and transactional updates without prematurely introducing distributed infrastructure.
- **Future frontend:** API contracts must remain independent of presentation-specific assumptions.

If an external dependency is unavailable, Siddhi should report the limitation explicitly and preserve the integrity of existing records.

## 9. Scope Change Management

New features should be evaluated against the vision and current roadmap.

A proposed addition should identify:

1. The portfolio problem it solves.
2. The expected outcome or benefit.
3. The evidence that the capability is needed now.
4. Its dependencies and risks.
5. Whether an existing system already owns the capability.
6. Its impact on delivery priorities and maintenance.
7. Whether it is necessary for the current phase or can be deferred.

A useful internal framework is not automatically a priority merely because it can be built. Equally, a commercial opportunity should not automatically override foundational work that materially enables multiple outcomes.

Scope changes should be recorded with their rationale and reviewed against the existing plan.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| OpenSpec or OKF formats are assumed incorrectly | Inspect actual schemas and support explicitly identified versions |
| Source data becomes stale | Record refresh timestamps and source availability; expose stale status |
| Declared progress is mistaken for actual completion | Separate declarations from verification evidence |
| Too much time is spent building Siddhi itself | Deliver in bounded phases and validate each phase against practical use |
| External AI produces unsupported conclusions | Require evidence references, uncertainty, validation, and human approval |
| Historical records are overwritten | Preserve snapshots, plan versions, and decision history |
| Future UI forces backend redesign | Establish stable API contracts and keep domain logic UI-independent |
| Repository contents contain unsafe or misleading instructions | Treat imported content as untrusted data and enforce access boundaries |
| Scope expands into a generic management platform | Require explicit justification against the product vision |

## 11. Initial Release Boundary

The first usable release should prioritize a small but complete workflow over implementing every planned feature.

The proposed minimum end-to-end workflow is:

1. Discover a project through Vyasa.
2. Ingest supported OpenSpec, OKF, and Git evidence.
3. Store source metadata and a historical snapshot.
4. Define a portfolio goal independently of the project.
5. Compare the goal with available evidence using deterministic rules.
6. Generate a report that distinguishes matches, candidate matches, gaps, and unknowns.
7. Preserve the inputs and results so the report can be reproduced or compared after refresh.

This workflow demonstrates Siddhi's core value before introducing more advanced planning and external AI features.

The precise initial source coverage, domain schema, and acceptance criteria remain subject to requirements review.

## 12. Relationship to Other Documentation

- `vision.md` defines why Siddhi exists and the outcomes it aims to achieve.
- `scope-and-roadmap.md` defines backend boundaries, exclusions, and delivery sequence.
- `functional-overview.md` will describe end-to-end user workflows and capabilities.
- `system-architecture.md` will detail components and interactions.
- `data-ownership.md` will establish authoritative sources and ownership boundaries.
- `domain-model.md` and `data-model.md` will define domain concepts and persistence structures.
- OpenSpec will hold detailed behavioral requirements and acceptance scenarios.
- OKF will hold reusable engineering knowledge and design explanations.

The same information should not be maintained independently in multiple authoritative locations. Cross-references should connect related documents while preserving their different purposes.

## 13. Open Questions

The following decisions remain open:

1. What source integrations are essential for the first usable release, and which can be deferred?
2. What exact data and operations does the current Vyasa interface expose?
3. Which OpenSpec and OKF versions and formats must be supported initially?
4. Should repository access initially require local checkouts, or must remote-only repositories be supported from the first release?
5. What is the minimum useful set of goal, initiative, outcome, and dependency entities?
6. How should snapshot retention and historical storage be bounded?
7. Which local security model is appropriate for the API and future Electron application?
8. What constitutes sufficient evidence for a finding to be classified as confirmed?
9. Which measurable criteria will determine whether the first release is useful enough to justify further investment?

These questions should be resolved or explicitly deferred before the affected implementation work begins.

---

**End of scope-and-roadmap document**
