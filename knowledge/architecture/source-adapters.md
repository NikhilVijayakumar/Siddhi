---
type: Architecture
title: Source adapter boundaries
description: Capability-based read-oriented integration, normalized observation contracts, identity resolution, and failure isolation.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Source adapter boundaries

Siddhi consumes independent engineering sources without becoming their authority.
An adapter translates source-specific access and interpretation into attributable
observations; it does not determine strategic success. Capability-based contracts
avoid making every source pretend to offer the same completeness, history, or
incremental guarantees. This is draft architecture, not a claim of working adapters.

# Authority and responsibility

| Source | Native authority | Interpretation boundary |
|---|---|---|
| Vyasa | Available inventory and discovery metadata | Discovery is not verification |
| OpenSpec in an ingested project | Source-authored declarations and workflow state | Declared progress is not working behavior |
| OKF | Knowledge, metadata, relationships, and recorded reviews | Documentation is not implemented capability |
| Git | Observed objects and revision relationships | Activity is not outcome achievement |
| Verification system | Its recorded execution and result | Results apply to a scope and revision |
| Siddhi | Portfolio intent, mappings, assessments, plans, decisions | A local projection does not replace a source |

Verification availability is optional. Failed execution, unavailable access,
unexecuted checks, and unknown result are distinct states. Additional source
categories can use the same boundary after their authority and access are understood.

# Logical composition

Application operations choose a scope and invoke an integration coordinator.
The coordinator selects an adapter, checks capabilities, tracks execution and
coverage, and passes observations to normalization and persistence. Adapters own
source protocols, authentication integration, format detection, and parsing.
Shared normalization maps common concepts while preserving source-native meanings.
Ingestion owns publication and history; analysis owns evidence interpretation.

These are module boundaries within a proposed modular monolith, not a requirement
for separately deployed services or a particular package tree. Keeping source
mechanisms behind ports allows replacement without rewriting portfolio semantics.

# Logical interface

| Operation | Useful result | Important limitation |
|---|---|---|
| Capability inspection | Supported, unsupported, temporarily unavailable operations | Unsupported is not an empty success |
| Connection validation | Configuration, access, permission, availability diagnostics | A bounded check is not a full scan |
| Discovery | Identities, requested scope, continuation, coverage, warnings | Empty records alone do not prove absence |
| Retrieval | Content or metadata for an identity, retrieval outcome | Preserve the known identity if retrieval fails |
| Observation capture | Identity, locator, revision, time, payload/fingerprint, limitations | Capturing a declaration does not verify it |
| Incremental retrieval | Bounded changes with source-defined cursor semantics | Timestamps need a demonstrated completeness guarantee |

A common result envelope lets the coordinator record execution without knowing
whether input came from a filesystem, API, controlled CLI, or export. It does not
erase differences in source consistency. Exact transport and field schemas remain open.

# Configuration and observation records

Source configuration logically contains a stable Siddhi source ID, type, label,
location or connection reference, enabled scope, adapter/version, capability
declarations, configuration revision, and validation status. Latest attempt,
latest successful access, connection state, and scan state answer different questions.
Credentials are separate referenced secrets, not ordinary configuration payloads.

An observation carries source and external artifact identity, artifact type,
locator, source revision when available, observation time, retrieval and parse
outcomes, adapter/normalization versions, payload or retained-content reference,
fingerprint where meaningful, and limitations. The ingestion run connects this
record to its scope and history. The adapter does not choose retention or delete
old snapshots. See [ingestion and snapshots](ingestion-and-snapshots.md).

# Identity and normalization

Prefer native identifiers scoped by source system. A documented composite key or
Siddhi-managed mapping is a fallback, not an assurance that names or paths are
permanent. Renames can preserve identity while changing a locator. Preserve prior
observations and whether the match is confirmed or provisional. Ambiguous matches
remain unresolved rather than being merged by name similarity.

Keep original status alongside normalized classification. Missing fields remain
unknown or unavailable; new fields can be retained without inventing their meaning.
Material parser and normalization changes are versioned so reinterpretation can
be distinguished from source change. No evidence found in an incomplete scan is
not evidence of absence. A missing record may be filtered, moved, inaccessible,
or removed; deletion needs source-appropriate coverage and evidence.

# Read-oriented trust boundary

Routine collection does not write external records, alter repository content,
check out revisions, change task markers, or publish source knowledge. Cloning,
targeted rescanning, or any future write capability needs its own declared scope
and authorization; discovery does not grant those permissions implicitly.

Access uses approved roots and minimum necessary permissions. Validate resolved
paths and controlled command arguments; retrieved documents and responses are
untrusted data, never scripts or operating instructions. Keep secrets and sensitive
source content out of ordinary logs. Routine ingestion does not send content to
external AI: [external analysis](external-analysis.md) is a separate disclosure boundary.

# Failure model and execution

Useful error categories distinguish configuration, authentication, permission,
availability, unsupported capability, missing artifact, unexpected format,
incomplete enumeration, rate limits, timeouts, transient access failures, and
internal adapter errors. Record safe diagnostics and the smallest affected scope.
One malformed record need not prevent independent records or sources from being used.

Bound retries to transient failures, source guidance, execution deadlines, and
repeat safety. Invalid configuration, persistent permission errors, and unknown
formats need correction rather than endless retries. Idempotent identity and
capture keys avoid duplicate logical observations. Cancellation or timeout can
retain completed stages without implying complete coverage or safe publication.

Short bounded reads can be synchronous. Larger scans may justify tracked background
execution, cancellation, and recovery; logical run tracking alone does not justify
distributed workers. Concurrency cannot silently overwrite newer portfolio intent.

Operational records identify source, adapter, operation, scope, start/end times,
counts, coverage, retries, format versions, and safe errors. Counts have source-specific
meaning; connection success and processing success do not establish completeness.

# Validation approach and unsettled choices

Contract fixtures exercise unsupported versus empty results, partial coverage,
identity preservation, and safe diagnostics. Format fixtures cover missing/unknown
fields, malformed content, version differences, and custom conventions. Rename,
ambiguous identity, retry, cancellation, persistence, and upgrade cases expose
duplicate or false-removal risks. Read-only credentials and before/after source
checks strengthen non-mutation testing.

Still unsettled: actual Vyasa transport and guarantees, supported source formats,
verification source, local versus remote Git access, identity fallback policies,
scan sizes/limits, refresh scheduling, full-content retention, and schema evolution
rules. Inspection of actual source contracts is necessary; this architecture
does not establish upstream capabilities.

Related: [Vyasa](vyasa-integration.md), [OpenSpec](openspec-integration.md),
[OKF](okf-integration.md), [Git](git-evidence.md),
[source authority](../decisions/source-authority-and-read-only-ingestion.md).