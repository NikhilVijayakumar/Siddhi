---
type: Architecture
title: Operational observability and safe diagnostics
description: Health versus readiness, truthful capability status, operation correlation, redaction, and bounded local diagnostics.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Operational observability and safe diagnostics

Observability explains what ran, what failed, what remains usable, and the safest
next action. Local structured logs and persisted summaries are proposed starting
points; remote telemetry and distributed tracing are not implied. No endpoint,
event schema, metrics service, or diagnostic export is asserted implemented.

# Distinct state dimensions

Health means the process responds. Readiness means required initialization and
persistence support offered operations. Starting, ready, degraded, not ready,
and stopping are conceptual lifecycle states, not final enum values.

Optional provider failure can degrade external analysis without disabling local
planning or deterministic processing. A missing required migration can prevent
readiness even when healthy. Checks stay cheap: no scans, provider requests,
full integrity checks, or recovery as a health-probe side effect.

Distinguish configured, last checked reachable, last completed, and currently
executing capability status. Historical observations need timestamps and scope;
previous success is not current connectivity. Unknown is not silently success.

Keep execution outcome, completeness, freshness, data quality, findings, and
approval separate. A completed analysis can find serious gaps; failed execution
with zero findings does not indicate a clean portfolio.

# Structured events and correlation

Use small stable event/error catalogues and safe human summaries. Candidate
fields are timestamp, level, event name, component, request/operation ID,
relevant opaque source/entity ID, duration, outcome, and error category. Not every
event needs every field. `ingestion.run.failed` is illustrative, not published.

DEBUG adds development detail; INFO records lifecycle; WARNING marks partial or
recoverable conditions; ERROR a failed required operation; CRITICAL inability
to continue safely or serious integrity risk. Unconfigured optional providers
are not automatically critical. Summarize repeated transient errors.

Validate supplied request IDs and generate replacements when unsuitable.
Correlation is never authentication. Preserve request identity for the initial
interaction and operation identity for the durable workflow. Propagate context
explicitly or concurrency-safely; mutable global state can mix runs.

# Operation-specific diagnostics

| Operation | Useful safe metadata | Important distinction |
|---|---|---|
| Source validation | Scope, check time, category, next action | Connection versus completeness |
| Ingestion | Attempts, complete/partial scope, measured counts, snapshot | Latest attempt versus last complete refresh |
| Analysis | Inputs/revisions, rule version, missing data | Execution failure versus substantive findings |
| External analysis | Provider/model, purpose, policy version, duration, validation | Provider completion versus accepted advisory result |
| Migration | Step identity, compatible schema, outcome, failure category | Started versus applied |
| Backup/restore | Format, schema, integrity/restore-check result | File created versus proven recoverability |

Counts and percentages reflect actual measurement. Omit unknowns or mark them
unavailable. Partial collection identifies incomplete scope and whether the last
usable published state remains active.

Useful failure categories include unavailable source, authentication failure,
permission denied, timeout, unsupported format, incompatible schema, invalid data,
partial scan, persistence/publication failure, cancellation, and unknown failure.
Reconcile catalogues with adapter/application ports before clients rely on them.

User errors explain affected operation/capability, retained usable data, retry
safety, and corrective action. State uncertainty instead of inventing a cause.
Full stack traces do not belong in ordinary responses.

# Diagnostic access and redaction

Protect detailed diagnostics like other sensitive resources. If unauthenticated
health is needed by a supervisor, expose minimal liveness. Exact health/readiness
namespaces and generic-operation versus resource-run status remain unresolved;
candidate paths are not installed routes.

Never log credential values, authorization headers, sessions, secret URL parameters,
raw context, or complete provider responses by default. Minimize private paths,
endpoints, payloads, and personal identifiers. Response allowlists and sink-level
redaction complement safe construction. Debug does not disable redaction; avoid
putting sensitive values into error formatting before redaction runs.

Retained advisory responses belong in controlled records under their data policy,
not duplicated logs. Bundles need authorized scope, bounded size, preview of data
categories, safe permissions, and cleanup policy. Review before sharing.

# Metrics, retention, and failure integrity

Useful local measurements include durations/errors, ingestion/analysis outcomes,
retries, interrupted jobs, database growth, backup sizes, and limit rejections.
Use bounded labels; paths, URLs, titles, and arbitrary IDs are poor dimensions.
Performance targets need a defined workload and reference environment.

Separate log, security-event, operation-summary, and domain-history retention.
Rotate routine logs. Exact periods, export policy, and remote telemetry approval
remain undecided. Routine local troubleshooting needs no remote transmission.

Noncritical log sink failure should not crash ordinary work, but never claim a
record was persisted if it was not. Security/integrity failures follow safe
fallback policy. Avoid recursively reporting database failure to that same
database. Logs, persisted status, and responses should agree on final outcome.

Restart reconciliation identifies unfinished runs as interrupted, incomplete,
or requiring inspection. Missing completion never proves success. Check committed
publication and side effects before retrying; automatic replay of provider calls
or decisions may duplicate consequences.

# Validation focus

Test concurrent correlation, stable codes, stale observations, partial outcomes,
optional-provider degradation, failed migrations, redaction, retention bounds,
unauthorized diagnostics, sink failure, and restart with incomplete operations.
Use the [diagnostics runbook](../runbooks/diagnostics.md) for safe triage.

Related: [API boundary](api-boundary.md), [persistence](persistence.md),
[configuration](configuration-and-secrets.md), [security](security-and-privacy.md).