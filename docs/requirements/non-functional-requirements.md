# Siddhi API — Non-Functional Requirements

**Product:** Siddhi (सिद्धि)  
**Document:** `non-functional-requirements.md`  
**Status:** Draft for review  
**Version:** 0.1  
**Related documents:** [vision](../../knowledge/product/vision.md), [scope and roadmap](../../knowledge/product/scope-and-roadmap.md), [functional baseline](functional-requirements.md), [package ownership](README.md)

## 1. Purpose

This document defines the quality attributes and operational constraints expected of Siddhi API.

Functional requirements describe what the system must do. Non-functional requirements describe how reliably, securely, efficiently, consistently, and maintainably it must do it.

These requirements apply to the initial local-first Python API with SQLite storage and should remain relevant when the separate React, TypeScript, and Electron frontend is introduced.

Quantitative targets in this document are proposed starting points for review. They must be validated against representative workloads before becoming binding acceptance criteria.

All identifiers remain stable and are uniquely owned by the [draft packages](README.md).
Ownership coordinates a cross-cutting constraint; it does not exempt other
capabilities from security, integrity, recovery, or testing obligations. Later
specifications retain links to this source and relevant [knowledge](../../knowledge/index.md).

## 2. Design Principles

Siddhi API should follow these principles:

1. **Correctness before speed:** Source information and portfolio decisions must not be corrupted to improve performance.
2. **Explicit uncertainty:** Missing, stale, unsupported, and conflicting data must remain distinguishable.
3. **Reproducibility:** Deterministic operations should produce explainable results from recorded inputs and rules.
4. **Least privilege:** Access to repositories, files, credentials, and external services must be restricted to what an operation requires.
5. **Recoverability:** Failures must not silently destroy previously valid data or historical records.
6. **Maintainability:** Components should be independently testable and changeable.
7. **Proportionate engineering:** The initial implementation should avoid infrastructure and operational complexity that is not justified by actual needs.
8. **Portability:** Core backend logic should not depend on Electron or a particular user interface.
9. **Traceability:** Important findings and decisions should be explainable through source evidence, rules, and recorded rationale.
10. **Controlled evolution:** Database schemas, API contracts, parsers, and stored artifacts should evolve through explicit versioning and migration procedures.

## 3. Performance and Responsiveness

### NFR-001 — API responsiveness

Routine operations such as retrieving a goal, listing projects from the local database, and retrieving a previously generated report should respond promptly under the expected local workload.

**Proposed initial targets:**

- Simple local read requests: 95th percentile within 500 ms.
- Simple local write requests: 95th percentile within 1 second, excluding unusually expensive operations.
- Health checks: normally within 200 ms.

These targets exclude external service latency and should be measured on a documented reference environment.

### NFR-002 — Long-running operations

Repository scanning, source ingestion, large comparisons, and external AI operations must not cause the API to become unresponsive.

The implementation must define which operations are synchronous and which run as background jobs. Long-running operations should expose their status and report errors without requiring the caller to hold an HTTP connection open indefinitely.

### NFR-003 — Incremental processing

When reliable revision identifiers or content hashes are available, the system should avoid reparsing unchanged content unnecessarily.

Incremental processing must not compromise correctness when source metadata changes, becomes unavailable, or cannot be trusted.

### NFR-004 — Resource efficiency

The initial application should run on a typical developer workstation without requiring a dedicated server, distributed database, or GPU.

Routine deterministic operations must not require an AI model or coding agent.

Memory and storage use should be measured against representative repositories and portfolio sizes before establishing hard limits.

## 4. Reliability and Availability

### NFR-005 — Failure isolation

A failure in one source integration must not automatically prevent unrelated portfolio operations from working.

The system should support partial refresh results when appropriate, clearly identifying which sources succeeded, failed, or could not be assessed.

### NFR-006 — Preservation of valid data

A failed or incomplete refresh must not silently replace a valid previous snapshot with incomplete data.

Portfolio-owned records and historical snapshots must be protected against unintended partial updates.

### NFR-007 — Consistent persistence

Database operations that logically belong together must use appropriate transaction boundaries.

If an operation fails, the system must either preserve the prior consistent state or record a clearly defined partial outcome that can be safely recovered.

### NFR-008 — Idempotent operations

Repeating a refresh, ingestion, or other supported retryable operation with unchanged inputs should not create duplicate source records or unintended duplicate portfolio entities.

Where an operation cannot be idempotent, its behavior must be explicitly documented.

### NFR-009 — Graceful degradation

If Vyasa, a remote repository, or an external AI service is unavailable, Siddhi should continue to provide operations that can be completed from available local data.

The system must communicate the limitations of results derived from stale or incomplete information.

### NFR-010 — Recovery

The application must have documented procedures for backing up and restoring its SQLite database and relevant local configuration.

Recovery procedures must account for schema migrations and preserve important portfolio history.

Recovery time and data-loss targets remain to be agreed.

## 5. Data Integrity and Consistency

### NFR-011 — Source provenance

Source-derived records must retain enough provenance to identify their origin, revision or snapshot, and ingestion context where that information is available.

### NFR-012 — Source authority

Siddhi must not silently alter authoritative information in Vyasa, OpenSpec, OKF, or Git.

Normalized data may be stored locally, but its relationship to the authoritative source must remain explicit.

### NFR-013 — Explicit data states

The system must distinguish, where applicable:

- Current and successfully ingested.
- Stale but previously available.
- Unavailable.
- Never retrieved.
- Unsupported format or version.
- Invalid or partially parsed.
- Conflicting or unresolved evidence.

Absence of data must not be interpreted as proof that the corresponding fact is false.

### NFR-014 — Historical preservation

The system must preserve sufficient history to explain meaningful changes in source evidence, plans, analysis results, and portfolio decisions.

Retention and archival policies must balance auditability, storage use, and the sensitivity of stored information.

### NFR-015 — Referential integrity

Portfolio entities, source records, snapshots, analysis results, and decisions must maintain valid relationships.

Deletion, archival, source removal, and repository renaming must not leave silent or misleading references.

### NFR-016 — Time and revision semantics

Timestamps must have a documented meaning and consistent representation. The system must distinguish source event time, source modification time, ingestion time, and analysis generation time where relevant.

Unavailable timestamps must not be fabricated.

## 6. Determinism and Reproducibility

### NFR-017 — Deterministic processing

For a fixed set of normalized inputs, rule versions, and configuration, deterministic analysis should produce equivalent findings.

Operations must not depend on unspecified ordering, machine-local time, or hidden mutable state where these would change the result.

### NFR-018 — Analysis provenance

Generated reports must record the relevant source snapshots, portfolio state, rule or report version, and generation metadata needed to explain their results.

### NFR-019 — Separation of deterministic and AI-generated results

AI-generated recommendations must be distinguishable from deterministic findings.

External AI output must not be represented as verified fact merely because it was imported successfully.

### NFR-020 — Historical comparability

When analysis rules or schemas change, the system must identify the relevant versions so that differences caused by changed rules can be distinguished from differences caused by changed source data.

The system should not imply that reports generated under different rules are directly comparable without qualification.

## 7. Security and Privacy

### NFR-021 — Least-privilege access

Filesystem and repository access must be limited to configured and authorized locations and operations.

The initial implementation should use read-only access for source ingestion wherever practical.

### NFR-022 — Local API exposure

The local API must not be exposed to external network interfaces by default without an explicit, documented configuration decision.

The deployment design must address loopback binding, browser access, cross-origin requests, and unauthorized local requests.

### NFR-023 — Secret management

Credentials and tokens must not be hardcoded into source code, committed configuration, logs, or generated reports.

The system must support appropriate secure configuration and credential handling for each integration.

### NFR-024 — External data sharing

Repository content, unpublished creative work, portfolio strategy, and other potentially sensitive data must not be sent to external AI services without an explicitly authorized workflow.

The system should minimize external payloads to the information necessary for the requested analysis.

### NFR-025 — Untrusted source content

Repository files, documentation, and imported AI output must be treated as untrusted input.

Instructions embedded in source content must not override system security policies, authorize file access, or trigger unintended actions.

### NFR-026 — Safe diagnostics

Logs, error messages, and diagnostic endpoints must avoid exposing credentials, sensitive file contents, unpublished work, or unnecessary private repository details.

### NFR-027 — Controlled write operations

The backend must not write to source repositories or publish artifacts as a side effect of routine reading or analysis.

Any future write-enabled integration must use explicit authorization and a defined operation boundary.

## 8. Maintainability and Modularity

### NFR-028 — Separation of concerns

API transport, application use cases, domain logic, source parsing, persistence, analysis, reporting, and external AI integration must have clear responsibilities.

### NFR-029 — Replaceable adapters

Source integrations should use defined adapter contracts so one integration can be changed or replaced without rewriting the portfolio domain.

### NFR-030 — UI independence

Core portfolio rules and deterministic analysis must not depend on React, Electron, or presentation-layer behavior.

### NFR-031 — Schema-aware parsing

Source parsers must identify supported formats and versions explicitly.

A new or unsupported source schema must not be silently interpreted using assumptions intended for a different version.

### NFR-032 — Explicit architectural decisions

Significant architecture choices, constraints, and trade-offs must be documented so that future maintainers can understand why the implementation was designed that way.

### NFR-033 — Controlled dependencies

Dependencies should be selected for a clear purpose, pinned or constrained appropriately, and updated through a testable process.

Unnecessary frameworks and infrastructure should be avoided in the initial implementation.

## 9. Testability and Quality Assurance

### NFR-034 — Automated test coverage

The system must support automated tests for domain behavior, API contracts, source parsing, persistence, migrations, analysis rules, and error handling.

Coverage percentages should be established after identifying critical behavior rather than used as the sole measure of quality.

### NFR-035 — Reproducible test fixtures

Representative source fixtures should cover supported OpenSpec and OKF versions, malformed artifacts, missing metadata, stale sources, and conflicting evidence.

Tests must not require access to private production repositories or external AI services for routine validation.

### NFR-036 — Integration isolation

External systems should be replaceable by test doubles or controlled fixtures in automated tests.

Contract tests should verify compatibility with the documented integration interfaces.

### NFR-037 — Migration validation

Database migrations must be tested against representative earlier schema versions.

Where feasible, tests should verify both successful upgrades and safe handling of migration failures.

### NFR-038 — Failure-path testing

Testing must cover interrupted refreshes, unavailable sources, invalid data, failed transactions, external timeouts, and retry behavior.

### NFR-039 — Security testing

Tests should cover input validation, filesystem boundaries, secret leakage, unauthorized operations, and handling of untrusted repository content.

## 10. API Quality and Compatibility

### NFR-040 — API documentation

All publicly exposed API operations must have documented request and response schemas, validation behavior, and error responses.

OpenAPI documentation should be generated from the actual API implementation rather than maintained as an unrelated manual specification.

### NFR-041 — Contract stability

Changes to API contracts must be managed deliberately.

Breaking changes should use an explicit compatibility or versioning strategy and must not silently break the separately developed desktop frontend.

### NFR-042 — Consistent errors

API errors must be structured and consistent enough for clients to distinguish validation failures, missing resources, conflicts, unavailable integrations, and internal failures.

Error responses must not expose internal secrets or unnecessary implementation details.

### NFR-043 — Pagination and bounded responses

Collection endpoints must support suitable pagination or other bounded retrieval strategies where result sizes may grow significantly.

Large source artifacts and analysis results must not be returned indiscriminately when a smaller summary or reference is sufficient.

### NFR-044 — Operation lifecycle

Long-running jobs must have a defined lifecycle, including status, completion, failure, and safe retry behavior. Cancellation should be supported where it can be implemented without corrupting data.

The precise lifecycle contract remains a design decision.

## 11. Portability and Deployment

### NFR-045 — Local-first operation

The initial backend must operate locally with SQLite and must not require a continuously available cloud service for core portfolio operations.

Remote source integrations may require network access, but local data retrieval, defined-rule analysis, and report generation should work from available stored information.

### NFR-046 — Environment configuration

Environment-specific values must be configurable without modifying application source code.

Configuration must be validated at startup, with actionable errors for missing or invalid required values.

### NFR-047 — Predictable lifecycle

Startup, shutdown, background jobs, and database access must be managed predictably.

The service must not leave unmanaged processes or partially completed operations without reporting their state.

### NFR-048 — Frontend integration readiness

The backend must expose a stable interface suitable for consumption by a separate Electron desktop application.

Frontend packaging must not require duplicating portfolio business rules in the frontend.

### NFR-049 — Database location and backup

The SQLite database location must be explicit and configurable through supported settings.

The application must document how database files, migrations, backups, and recovery are managed.

## 12. Observability and Diagnostics

### NFR-050 — Structured operational logging

Logs should provide sufficient context to diagnose failures and understand operations, including correlation or operation identifiers where useful.

Logs must not include unnecessary sensitive source content.

### NFR-051 — Refresh and job reporting

Each refresh or analysis operation must report its outcome and relevant warnings, including partial failures and unsupported sources.

### NFR-052 — Health checks

The service should expose a basic health endpoint and, where appropriate, separate diagnostic information for database access and integration readiness.

A remote source being unavailable must not necessarily mean the entire local service is unhealthy.

### NFR-053 — Actionable error reporting

Errors should identify the failed operation and provide enough information for diagnosis without disclosing secrets or treating untrusted input as executable instructions.

## 13. Data Retention and Storage Growth

### NFR-054 — Bounded storage growth

The system must monitor or expose enough information to understand database growth and the cost of retaining source snapshots and historical reports.

A retention policy should be defined for large or reproducible derived artifacts.

### NFR-055 — Historical record policy

The system must distinguish records that require durable historical retention—such as approved decisions and plan revisions—from source-derived caches that may be refreshed or reconstructed.

No history should be deleted solely because it is inconvenient to store; retention decisions must follow an explicit policy.

### NFR-056 — Backup consistency

Backups must represent a consistent database state and have documented restoration procedures.

The implementation should avoid relying on copying a live database file without considering SQLite's transaction and journaling behavior.

## 14. Proposed Initial Acceptance Targets

The following targets are a starting point for discussion, not yet approved commitments.

| Quality attribute | Proposed target |
|---|---|
| Simple local read latency | P95 ≤ 500 ms on a documented reference machine |
| Simple local write latency | P95 ≤ 1 second, excluding long-running work |
| Health endpoint | Normally ≤ 200 ms |
| Deterministic report reproduction | Equivalent findings for identical normalized inputs, rules, and configuration |
| Refresh safety | Failed refresh does not silently destroy the last known valid snapshot |
| Data provenance | Every source-derived record retains source references where available |
| External AI dependency | No AI required for routine ingestion and deterministic reports |
| Testability | Critical domain, parsing, persistence, API, and failure paths have automated tests |
| Security defaults | Local API is not externally exposed by default |
| Recovery | Backup and restoration procedure is documented and tested |

Performance figures must be measured under representative workloads. Reliability, security, and data-integrity expectations should be treated as mandatory design concerns even where quantitative targets remain open.

## 15. Open Questions

The following decisions need resolution before the non-functional requirements are finalized.

### Performance and scale

1. What is the expected number of projects and repositories in the initial portfolio?
2. What are the approximate sizes of typical and largest repositories?
3. How much historical source and report data should be retained?
4. What reference workstation should be used for performance measurements?

### Reliability and recovery

5. What data-loss tolerance is acceptable for portfolio-owned records?
6. How frequently should backups be created, and where should they be stored?
7. What recovery time is acceptable after database corruption or application failure?
8. Should refreshes resume after interruption, or restart from the beginning?

### Security

9. Will the API be used only by the local desktop application, or must other local tools access it?
10. Is authentication required even when the service binds only to loopback?
11. What information may be shared with external AI providers?
12. Which filesystem roots and repository credentials may the backend access?

### Operations and maintainability

13. Which background-job execution model is appropriate for the first release?
14. Which Python and dependency versions will be supported?
15. What level of API backward compatibility is required during early development?
16. Which operating systems must the backend and eventual desktop application support?

These questions should be answered according to actual use cases and risks rather than by adopting enterprise-scale targets prematurely.

## 16. Relationship to Other Documentation

- `vision.md` defines Siddhi's purpose and intended outcomes.
- `scope-and-roadmap.md` defines the initial delivery boundaries and sequence.
- `functional-requirements.md` describes required behavior.
- `system-architecture.md` will explain the component structure and interaction boundaries.
- `data-model.md` and `persistence-and-migrations.md` will define the storage model and evolution strategy.
- `security-and-privacy.md` will detail the threat model, access boundaries, and data-sharing controls.
- OpenSpec will hold the final, testable quality requirements and acceptance scenarios.
- OKF will preserve reusable engineering knowledge, rationale, and implementation guidance.

This document provides the quality baseline. Final non-functional requirements should be converted into testable OpenSpec scenarios where applicable, while reusable principles and technical explanations should be retained in OKF.

---

**End of non-functional requirements document**
