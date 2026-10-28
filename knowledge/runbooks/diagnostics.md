---
type: Runbook
title: Safe operational diagnosis
description: Non-destructive triage for startup, readiness, source, analysis, and interrupted-operation failures.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Safe operational diagnosis

Use this proposed procedure when backend, source refresh, analysis, or maintenance
state cannot be explained. Status interfaces, routes, exports, and events are not
assumed implemented. Use supported inspection only; absent tooling is a limitation,
not permission to dump secrets or edit the database.

# Immediate safety

Confirm operator authorization and the affected instance. Record time, operation
identity if available, safe error category, and last successful action. Do not
share raw environment, configuration, tokens, provider context, or databases in
public support channels. For suspected unauthorized access/disclosure, use the
[incident procedure](security-incidents.md). For corruption/failed upgrades,
preserve the store and use [persistence recovery](persistence-recovery.md).

# Triage sequence

1. Determine whether the process is absent, starting, responsive, or stopping.
   Responsiveness does not prove persistence readiness.
2. Inspect safe startup/configuration diagnostics: types, effective origins,
   permissions, binding, enabled capabilities. Never weaken security to start.
3. Distinguish pending/failed migrations, unsupported schema, denied paths,
   contention, and storage exhaustion through supported inspection.
4. Decide whether failure is global or capability-specific. Optional provider
   outages need not prevent local deterministic work.
5. Follow request to operation identity where supported. Separate latest attempt
   from last successful complete run and preserve observation timestamps.
6. Compare execution, completeness, freshness, and findings. Failed analysis with
   zero findings is not success; unknown cause remains unknown.
7. Identify active usable snapshot and partial staging. Failed collection does
   not prove deletion of earlier records.
8. Select a documented safe action or escalate with uncertainty intact.

# Common conditions

| Condition | Safe investigation | Avoid |
|---|---|---|
| Authentication failed | Assigned reference and issuer read permissions | Printing or guessing credentials |
| Source inaccessible | Missing versus denied versus timeout/format | Broadening roots or switching identity |
| Partial scan | Incomplete scope and retained published view | Marking complete or deleting absent data |
| Analysis failure | Captured input identities and rule version | Interpreting no findings as achieved goals |
| Invalid provider output | Safe outcome and validation category | Treating parseable advice as verified |
| Running after restart | Committed stages and side effects | Blind replay or manual success edits |
| Unavailable logs | Safe fallback and recorded evidence gap | Recursive writes to failed sinks |

# Retry, export, and closure

Retry only with understood side effects, committed state, and deduplication.
Reuse an idempotency association only for the same logical request under its
policy. A timeout does not establish remote failure; cancellation is not proof
that work stopped. Insufficient recovery evidence means uncertain outcome,
not permission to invent success.

If controlled export exists, minimize scope/time range, review categories, redact
secrets/private paths/personal identifiers, restrict permissions, share only with
authorized recipients, and honor size/cleanup limits. Debug still redacts.

After correction, verify the affected capability with bounded synthetic/approved
data. Check accurate readiness/final status, retained history, and no duplicates.
Record cause, action, result, uncertainty, and unverified checks. One successful
retry does not prove a general fix.

Related: [observability](../architecture/observability.md),
[configuration](../architecture/configuration-and-secrets.md).