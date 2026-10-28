# Observability and Diagnostics

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `observability-and-diagnostics.md`  
**Status:** Draft for review  
**Scope:** Application health, structured logging, ingestion and analysis diagnostics, operational history, and troubleshooting  
**Implementation status:** Not yet verified in a running system

---

## 1. Purpose

This document defines how Siddhi reports its operational state and helps users and developers diagnose failures.

Siddhi integrates with source systems, stores historical snapshots, runs deterministic analysis, and may invoke external AI providers. Failures can occur at different boundaries, and a single generic error message is insufficient to explain what happened.

The system must make it possible to answer questions such as:

- Is the backend running and ready to accept requests?
- Can Siddhi access its database?
- Which sources were scanned successfully, partially, or unsuccessfully?
- When was a source last refreshed successfully?
- Why did an ingestion or analysis run fail?
- Which snapshot and rules produced a report?
- Is a result incomplete because of missing evidence or because a technical operation failed?
- Is an issue transient, persistent, or awaiting user action?
- What is the safest next step to resolve the problem?

Observability must be useful in a local-first application without requiring a centralized monitoring service or transmitting private portfolio data to an external telemetry provider.

## 2. Design principles

### 2.1 Explain the state, not just the error

Diagnostics should identify the affected operation, relevant source or entity, failure category, and safe corrective action where known.

A generic message such as “Operation failed” is insufficient when the system can safely provide more context.

### 2.2 Separate operational failure from analytical findings

A source timeout is an operational failure. Missing evidence for a goal is an analytical finding. A conflicting source record is a data-quality condition.

These conditions must not be merged into a single success/failure status.

### 2.3 Prefer structured diagnostics

Logs and operational records should use stable event names, error codes, timestamps, and relevant identifiers.

Human-readable messages should accompany structured fields but must not become the sole machine-readable interface.

### 2.4 Keep routine operation local

The initial implementation should use local logs, health endpoints, and persisted operation records.

Centralized telemetry, remote dashboards, and third-party monitoring services are optional future capabilities, not requirements for the first release.

### 2.5 Protect sensitive information

Diagnostics must not expose credentials, private source content, unnecessary personal information, or complete AI context packages.

Debugging convenience must not override the security and privacy rules in `security-and-privacy.md`.

### 2.6 Keep observability proportionate

Implement enough diagnostics to troubleshoot the first usable release. Avoid introducing a full distributed tracing platform, metrics server, or complex monitoring stack before the architecture requires one.

## 3. Observability scope

Siddhi should observe five categories of activity.

| Category | Examples | Primary purpose |
|---|---|---|
| Application health | Startup, shutdown, readiness, database availability | Determine whether the system can operate |
| Source operations | Discovery, connection checks, ingestion, parsing | Explain source availability and refresh outcomes |
| Analysis operations | Rule execution, finding generation, report creation | Explain analytical execution and reproducibility |
| External analysis | Provider calls, response validation, timeouts | Explain advisory workflow outcomes |
| Maintenance operations | Migrations, backups, restoration, configuration changes | Support recovery and safe operation |

These categories share diagnostic conventions but have different retention and severity requirements.

## 4. Operational state model

### 4.1 Application state

The backend should expose a clear distinction between process health and operational readiness.

Proposed states include:

- **Starting:** initialization is in progress.
- **Ready:** required components are available for normal operations.
- **Degraded:** the backend is running, but one or more optional or non-critical capabilities are unavailable.
- **Not ready:** a required dependency or initialization step prevents normal operation.
- **Stopping:** shutdown is in progress.

These are conceptual states. The API may use health endpoints and response fields rather than exposing every state as a separate status.

### 4.2 Health versus readiness

A lightweight health check should establish that the process is responsive.

Readiness should establish that the backend can perform the operations it claims to support, including access to required persistence.

An optional integration being unavailable must not necessarily make the whole application unready. For example, Siddhi should remain usable for deterministic analysis when an external AI provider is unavailable.

### 4.3 Capability-level status

Where useful, expose status at the capability level:

- Database available.
- Source adapter configured.
- Source reachable.
- Last ingestion successful.
- Analysis engine available.
- External AI provider configured.
- External AI provider reachable, if checked.
- Backup or migration operation in progress.

A configured provider must not be represented as reachable unless a check actually established reachability. A previous successful check must not be presented as proof of current availability.

## 5. Structured logging

### 5.1 Log format

Use structured logs with a consistent schema. JSON is a suitable candidate for machine-readable log output, while the desktop application may also present readable summaries.

A log event may contain:

| Field | Purpose |
|---|---|
| `timestamp` | Event time in a consistent timezone-aware format |
| `level` | Severity |
| `event_name` | Stable event identifier |
| `message` | Safe human-readable explanation |
| `component` | Component that emitted the event |
| `operation_id` | Identifier for the operation or job |
| `request_id` | Identifier for an API request, when applicable |
| `source_id` | Siddhi source identifier, when relevant |
| `entity_id` | Relevant Siddhi-owned entity identifier, when applicable |
| `error_code` | Stable error category, when applicable |
| `duration_ms` | Elapsed time, where meaningful |
| `outcome` | Success, partial, failed, cancelled, or another defined result |

The final schema should be small and consistent. Not every event needs every field.

### 5.2 Stable event names

Prefer stable event identifiers such as:

- `application.startup.completed`
- `application.startup.failed`
- `database.connection.failed`
- `source.validation.completed`
- `ingestion.run.started`
- `ingestion.run.completed`
- `ingestion.run.failed`
- `snapshot.publication.completed`
- `analysis.run.completed`
- `analysis.run.failed`
- `external_analysis.request.failed`
- `backup.completed`
- `migration.failed`

Names are illustrative. The implementation should define and document its actual event catalogue.

Event names and error codes should remain stable enough for diagnostics, tests, and future UI components to rely on them.

### 5.3 Severity levels

Use severity levels consistently.

| Level | Intended use |
|---|---|
| `DEBUG` | Detailed development diagnostics |
| `INFO` | Normal lifecycle events and important successful operations |
| `WARNING` | Recoverable issues, partial results, or conditions requiring attention |
| `ERROR` | A required operation failed |
| `CRITICAL` | The application cannot safely continue or a serious integrity condition exists |

A missing optional AI provider should not automatically generate a critical error. Repeatedly logging the same transient issue at error level should also be avoided where a single operation summary can explain the failure.

### 5.4 Log verbosity

The default local log level should be suitable for normal operation without producing excessive detail.

Debug logging may be enabled temporarily for troubleshooting. It must not disable secret redaction or other security controls.

Security-relevant events must not disappear merely because the ordinary log level is reduced. Their recording should follow the audit and security-event policy.

## 6. Request and operation correlation

Siddhi must be able to trace an operation across its relevant application components.

### 6.1 Request correlation

Each API request should have a correlation identifier. If a caller provides a request identifier, the backend must validate it before accepting it for logging or propagation.

The backend should generate its own identifier when no valid identifier is supplied.

Correlation identifiers must not be treated as authentication credentials or authorization tokens.

### 6.2 Long-running operations

Ingestion, analysis, report generation, and external AI requests may run longer than an ordinary API request.

Each such operation should have a stable operation or job identifier. Logs, status endpoints, and persisted operation records should use that identifier consistently.

The API request identifier and operation identifier serve different purposes:

- The request identifier connects the initial HTTP interaction to its diagnostics.
- The operation identifier connects the longer-running workflow and its subsequent status changes.

### 6.3 Cross-component propagation

Where an operation invokes multiple internal services or adapters, propagate the relevant operation identifier explicitly.

Avoid relying solely on process-global mutable state, which can associate logs with the wrong request when operations run concurrently.

## 7. Source and ingestion diagnostics

Source ingestion is a core capability and needs more detailed operational visibility than a single overall status.

### 7.1 Source status

For each configured source, Siddhi should be able to report, where applicable:

- Source identifier and type.
- Enabled or disabled state.
- Last attempted validation time.
- Last known validation outcome.
- Last ingestion attempt.
- Last successful complete ingestion.
- Last partial or failed ingestion.
- Current ingestion operation, if any.
- Last published snapshot.
- Snapshot completeness and freshness.
- A safe error category and suggested next action.

Do not expose credentials or unnecessary private connection details in source-status responses.

### 7.2 Ingestion-run summary

An ingestion-run record should identify:

- The source and scan scope.
- Start and completion times.
- The operation outcome.
- Whether the scan was complete, partial, incremental, or diagnostic.
- Counts of records discovered, accepted, rejected, added, changed, or removed, where those counts are available and meaningful.
- Validation warnings.
- Retry information.
- The resulting snapshot, if one was published.
- A safe error summary when the operation failed.

Counts must describe what the adapter actually measured. If the source cannot reliably report a count, the field should be omitted or marked unavailable rather than guessed.

### 7.3 Failure categories

Use stable categories such as:

- `source_unavailable`
- `authentication_failed`
- `permission_denied`
- `timeout`
- `unsupported_format`
- `schema_incompatible`
- `invalid_source_data`
- `partial_scan`
- `persistence_failed`
- `publication_failed`
- `cancelled`
- `unknown_failure`

The exact catalogue must align with the source-adapter contract.

The same error category may have different corrective actions depending on the source type and operation.

### 7.4 Partial success

Partial ingestion must be visible as partial, not silently converted into success.

Diagnostics should identify the incomplete scope where known and indicate whether the last-known-good snapshot remains active.

A failed or partial refresh must not imply that previously observed source records have been deleted.

## 8. Analysis and report diagnostics

Analysis diagnostics should explain how an analysis run executed without confusing execution status with the quality of its findings.

### 8.1 Analysis-run metadata

Record, as appropriate:

- Analysis-run identifier.
- Start and completion times.
- Goal, initiative, or portfolio scope.
- Input source snapshot identifiers.
- Relevant plan or decision revisions.
- Rule-set version.
- Execution outcome.
- Counts of findings by classification.
- Missing or excluded inputs.
- Warnings and validation failures.
- Report reference, if generated.

This information must be sufficient to understand which inputs produced the result.

### 8.2 Execution status versus finding status

These are separate dimensions.

An analysis run may complete successfully and report serious portfolio gaps. That is not an execution failure.

Conversely, an analysis run may fail before producing findings. That must not be reported as a successful analysis simply because no gaps were returned.

### 8.3 Report diagnostics

A report should identify its generation time and the relevant analysis run, input snapshots, and rule version.

Where information is incomplete or stale, the report should expose that limitation.

The report must not imply that a missing finding means a goal is achieved unless the applicable rule and evidence support that conclusion.

## 9. External AI diagnostics

External AI operations require visibility into provider execution without exposing sensitive context.

For each request, retain relevant metadata such as:

- Request and operation identifiers.
- Provider and model identifiers.
- Workflow or analysis purpose.
- Template or policy version.
- Start time and duration.
- Outcome and safe failure category.
- Retry count.
- Usage or cost information, if reliably supplied by the provider.
- Response-validation outcome.
- Whether the result was accepted for review.

Do not log full prompts, complete context packages, credentials, or raw provider responses by default.

If storing the full response is necessary for auditability, store it under the applicable data-retention and access policy, rather than duplicating it into ordinary operational logs.

A provider timeout, invalid response, or unavailable credential must be distinguishable from a completed analysis that returned an unfavorable recommendation.

## 10. Database and maintenance diagnostics

Database and maintenance operations should produce actionable status information.

### 10.1 Database

Report relevant failures such as:

- Database cannot be opened.
- Database is not writable.
- Transaction failed.
- Lock contention exceeded the retry policy.
- Integrity check failed.
- Migration is pending or failed.
- Database schema version is unsupported.
- Storage is insufficient for the requested operation, where detectable.

Avoid logging complete SQL statements with sensitive parameter values.

### 10.2 Migrations

Migration diagnostics should include the migration identifier, start time, outcome, and a safe failure reason.

The system must not report a successful upgrade if the migration did not complete.

### 10.3 Backup and restore

Report:

- Backup or restore operation identifier.
- Start and completion times.
- Outcome.
- Backup format and schema version, where available.
- Integrity-validation result.
- Safe failure category.

Do not describe a backup as verified solely because a file was created. A validated restoration test is stronger evidence of recoverability.

## 11. Metrics and resource diagnostics

The initial implementation should collect a small set of local operational metrics where they are useful.

Candidate metrics include:

- API request count and duration.
- API error count by safe error category.
- Ingestion duration and outcome.
- Number of partial or failed source scans.
- Analysis duration and outcome.
- External AI request duration and failure count.
- Database size.
- Backup size.
- Number of incomplete or failed jobs.
- Retry counts.
- Resource-limit rejections.

Metrics must use bounded labels. Do not use arbitrary repository paths, full URLs, goal titles, or other high-cardinality or sensitive values as metric labels.

### 11.1 No unnecessary telemetry

The first release does not need to send metrics to a remote monitoring service.

If remote telemetry is introduced later, it must be separately reviewed for privacy, data minimization, security, consent or approval requirements, and operational value.

### 11.2 Resource limits

Diagnostics should help identify resource exhaustion, including:

- Large source inputs.
- Excessive concurrent jobs.
- Database growth.
- Repeated retries.
- Long-running parsing or analysis.
- Disk exhaustion.

Metrics should support diagnosis without becoming a second, unbounded data store.

## 12. Diagnostic API

The API should expose a minimal, stable set of operational endpoints.

A proposed baseline is:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Confirm the process is responsive |
| `GET /ready` | Report whether required components are ready |
| `GET /api/v1/system/status` | Report safe application and capability status |
| `GET /api/v1/operations/{operation_id}` | Retrieve a long-running operation's status |
| `GET /api/v1/operations/{operation_id}/diagnostics` | Retrieve safe operation-specific diagnostics, if needed |
| `GET /api/v1/sources/{source_id}/status` | Retrieve source status and last refresh information |

These endpoints are proposals and must be reconciled with `api-design.md`.

### 12.1 Response requirements

Diagnostic responses should:

- Use stable status and error codes.
- Include operation or request identifiers where appropriate.
- Distinguish current state from last known state.
- Include timestamps for historical observations.
- Avoid exposing secrets and sensitive internals.
- Avoid implying a fresh connectivity check occurred when the status is based on an earlier result.

Health endpoints should be lightweight and should not trigger full source scans or expensive integrity checks.

### 12.2 Access control

Operational diagnostics can reveal internal paths, source configuration, and project activity. They must follow the same authorization and disclosure rules as other API resources.

A public or unauthenticated health endpoint, if required by the process manager, must reveal only the minimum information necessary to establish process health.

## 13. User-facing diagnostics

Siddhi should present operational issues in language suitable for its intended users.

For example:

**Technical condition:** Source authentication failed.

**User-facing message:** “Siddhi could not access this source because its credentials were rejected.”

**Suggested action:** “Check the credential assigned to this source and verify that it has read access.”

**Technical detail:** A stable error code and operation identifier may be available for troubleshooting.

The UI should avoid exposing full stack traces to ordinary users. Authorized diagnostic views may provide additional technical detail, subject to redaction.

### 13.1 Actionable errors

Where possible, a diagnostic should explain:

1. What operation failed.
2. Which source or capability was affected.
3. Whether existing data remains available.
4. Whether retrying is safe.
5. What the user can do next.

If the cause is uncertain, the message should say so rather than asserting an unverified explanation.

### 13.2 Safe retries

The UI should distinguish operations that are safe to retry from those that require inspection or explicit confirmation.

A retry must not accidentally duplicate a decision, create duplicate evidence, or publish an incomplete snapshot.

## 14. Diagnostic retention and privacy

Operational records and domain history serve different purposes.

Operational logs explain execution. Domain records explain portfolio decisions and historical evidence. Their retention policies should be defined independently.

The system should:

- Apply a configurable, bounded log-retention policy.
- Avoid logging sensitive source content.
- Redact secrets and sensitive connection parameters.
- Restrict access to diagnostic exports.
- Limit the size of diagnostic bundles.
- Make it clear when a diagnostic bundle includes paths, project metadata, or error details.
- Avoid including raw AI prompts or responses unless explicitly required and approved.
- Delete temporary diagnostics according to the defined cleanup policy.

The exact retention periods and export rules remain open decisions.

## 15. Failure handling and diagnostic integrity

Diagnostics must remain useful when the system is itself experiencing failures.

### 15.1 Logging failures

If writing an ordinary log fails, the application should not crash solely because a non-critical diagnostic event could not be written.

For critical integrity or security failures, the application must fail safely and use the safest available reporting mechanism.

It must not silently claim that an event was durably recorded when the logging operation failed.

### 15.2 Avoid recursive failures

Diagnostic code must not repeatedly trigger the same failed operation while trying to report the failure.

For example, a database-unavailable condition should not cause an unbounded attempt to write each diagnostic event back into the unavailable database.

### 15.3 State consistency

Persisted operation records, logs, and API responses should agree on the final outcome of a completed operation.

If the system crashes before recording completion, the operation should be identifiable as interrupted, incomplete, or requiring reconciliation after restart.

A missing completion event must not be interpreted as proof of success.

## 16. Testing and validation

Observability must itself be tested.

### 16.1 Logging tests

Verify that:

- Structured events contain the required fields.
- Event names and error codes are stable.
- Request and operation identifiers propagate correctly.
- Concurrent operations do not mix correlation identifiers.
- Secrets and sensitive payloads are redacted.
- Log retention and size limits work.
- Logging failures do not cause unsafe recursive failures.

### 16.2 Status tests

Verify that:

- Process health and readiness are distinct.
- Optional provider failure does not incorrectly make deterministic analysis unavailable.
- Stale source status is not presented as a fresh check.
- Partial ingestion is not presented as complete.
- Analysis execution status is separate from findings.
- Unsupported database versions and failed migrations are reported correctly.

### 16.3 Recovery tests

Verify that:

- Interrupted operations can be identified after restart.
- Failed ingestion preserves the published snapshot.
- Database failures do not produce false completion events.
- Backup and restore outcomes are accurately reported.
- Retry behavior does not create duplicate logical records.

### 16.4 Diagnostic security tests

Verify that unauthorized callers cannot access protected diagnostics and that responses do not disclose secrets, full private paths, raw source payloads, or sensitive AI context.

## 17. Acceptance criteria

The observability and diagnostics implementation is ready for the first usable release when:

1. The application exposes separate process-health and readiness signals.
2. Logs use a documented structured format and stable event identifiers.
3. Requests and long-running operations can be correlated.
4. Source status distinguishes last successful refresh from the most recent attempt.
5. Partial, failed, and complete ingestion outcomes are distinguishable.
6. Analysis execution failures are distinct from analytical findings.
7. Analysis reports retain references to their inputs and rule versions.
8. Database, migration, backup, and recovery failures produce actionable diagnostics.
9. External AI failures can be investigated without logging sensitive prompts or credentials.
10. Diagnostic responses follow access-control and redaction policies.
11. Logs and metrics have bounded storage and cardinality.
12. Operational diagnostics are covered by automated tests.
13. The system does not claim an operation succeeded when completion was not safely established.
14. A user can identify the next troubleshooting action for common startup, source-access, and ingestion failures.

## 18. Implementation sequence

### Phase 1 — Basic health and logging

- Define the structured log schema.
- Establish request and operation identifiers.
- Implement process health and readiness.
- Add safe startup and database diagnostics.
- Define log rotation and retention.

### Phase 2 — Source and ingestion diagnostics

- Persist ingestion-run status.
- Add source status and refresh summaries.
- Record completeness, validation warnings, and failure categories.
- Expose operation status through the API.

### Phase 3 — Analysis and AI diagnostics

- Record analysis inputs and rule versions.
- Add execution summaries and finding counts.
- Record external AI request outcomes and response-validation status.
- Implement safe error messages for provider failures.

### Phase 4 — Recovery and maintenance diagnostics

- Add migration, backup, and restore diagnostics.
- Identify interrupted jobs after restart.
- Add resource and database-size metrics.
- Validate diagnostic consistency under failure.

### Phase 5 — Desktop troubleshooting

- Display source and operation status in the desktop client.
- Present actionable error messages.
- Provide a controlled diagnostic export where required.
- Verify that the UI does not expose sensitive technical details to unauthorized callers.

This sequence is provisional and should be aligned with the agreed first-release scope.

## 19. Open questions

| ID | Question | Why it matters |
|---|---|---|
| OD-001 | Which logging library and structured output format should be used? | Determines logging conventions and integration effort. |
| OD-002 | How long should operational logs and failed-operation records be retained? | Balances troubleshooting value, privacy, and storage. |
| OD-003 | Which operational metrics must be available in the first release? | Prevents unnecessary instrumentation. |
| OD-004 | Should diagnostic export be included in the first usable release? | Affects supportability and disclosure risk. |
| OD-005 | How should interrupted jobs be reconciled after a backend restart? | Determines persisted operation state and recovery behavior. |
| OD-006 | Which health information can be exposed without authentication? | Depends on the local API threat model. |
| OD-007 | Should logs be file-based, database-backed, or split by purpose? | Affects performance, recovery, and retention. |
| OD-008 | What is the maximum supported diagnostic bundle size? | Controls storage and accidental disclosure risk. |
| OD-009 | Which source and analysis status fields belong in the desktop UI? | Establishes a useful and comprehensible troubleshooting experience. |
| OD-010 | Are remote telemetry or centralized monitoring ever required? | Determines whether a future telemetry architecture is necessary. |

## 20. Relationship to other documents

This document defines operational visibility and troubleshooting behavior. It must be reconciled with:

- `system-architecture.md` — component boundaries and runtime behavior.
- `api-design.md` — health endpoints, operation resources, and error contracts.
- `persistence-and-migrations.md` — persistence and recovery diagnostics.
- `configuration-and-secrets.md` — effective configuration and secret redaction.
- `security-and-privacy.md` — logging safety, access controls, and data retention.
- `source-integration.md` — adapter errors and source validation.
- `ingestion-and-snapshots.md` — run state, completeness, and publication.
- `deterministic-analysis.md` — analysis status and reproducibility.
- `external-analysis.md` — provider failures and response validation.
- `testing-and-validation.md` — tests for diagnostic behavior.
- `non-functional-requirements.md` — performance, reliability, and operational targets.

Operational diagnostics must explain what the system knows and what it has verified. They must not turn an unknown state into a false success, nor confuse a technical failure with a strategic or evidence-related finding.

## 21. Review status

This document establishes a proposed baseline for observability and diagnostics. It does not claim that structured logging, health endpoints, persisted operation records, or diagnostic exports have already been implemented.

Before implementation, prioritize structured logging, request/operation correlation, source-refresh summaries, and clear failure states. Those capabilities provide the foundation for diagnosing the rest of Siddhi without introducing unnecessary monitoring infrastructure.






