---
type: Architecture
title: Ingestion, snapshots, and publication
description: Source-aware capture, versioned manifests, current-view publication, checkpoint safety, recovery, and retained-history trade-offs.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Ingestion, snapshots, and publication

Ingestion captures what was observed and creates usable projections without
becoming the source authority. Independent sources have different identity,
history, deletion, and consistency guarantees. A common framework coordinates them
without pretending those guarantees are identical. Routine capture, normalization,
fingerprinting, comparison, and reporting are deterministic; external reasoning
is a separate optional boundary.

# Separate capture from usable state

Enumeration, retrieval, parsing, normalization, snapshot assembly, persistence,
and publication are distinct stages. A successfully read record does not establish
a complete scan. A successfully retained partial snapshot does not necessarily
qualify to replace the current usable view. This distinction prevents a failed
refresh from turning incomplete observations into apparently complete current state.

The proposed logical flow is configuration → orchestrator → adapter/enumeration →
normalization → identity/fingerprint/validation → snapshot assembly → coverage and
consistency checks → publication → analysis. These can be modules in one application
and transactions in one local store; a streaming platform or distributed workers
are not implied.

The orchestrator owns run tracking, scope, limits, cancellation, checkpoint handling,
retries, assembly, and publication eligibility. Adapters own native access, format,
identity, cursor, revision, deletion, and consistency semantics. Normalization
preserves native fields and provenance. Persistence owns versions, current-view
pointers, manifests, diagnostics, and recovery state.

# Working vocabulary

| Term | Meaning |
|---|---|
| Scan | Attempt to enumerate or inspect a configured scope |
| Ingestion run | Tracked collection and processing execution |
| Batch | Bounded unit of work within a run |
| Observation | Captured source item or source state with provenance |
| Snapshot | Recorded observation of a defined source scope and collection point |
| Manifest | Snapshot identity, scope, coverage, revisions, processing, and outcome |
| Current view | Usable normalized state selected for normal queries |
| Publication | Deliberate switch to a prepared usable result |
| Checkpoint | Source-specific resumable collection position |
| Watermark | Source-specific boundary describing collection progress |
| Tombstone | Retained identity and basis for sufficiently established removal |

A checkpoint is not automatically a watermark, and neither proves full coverage.
An external source may change while scanned. A snapshot is not a promise of an
atomic external copy unless the source and access method support that claim.

# Configuration, capabilities, and runs

Source configuration logically captures stable ID, type, label, access/location,
optional project, enabled state, collection policy, capability declarations,
configuration revision, latest attempt/success, and last publication. Secret
references are separate from ordinary metadata.

Capabilities distinguish full/incremental enumeration, stable identity, revisions,
consistent snapshots, cursors, reliable deletion, validation, comparison, cancellation,
and resumption. An unavailable capability is not silently replaced by weaker
semantics advertised as equivalent.

A run records stable ID, source/configuration revision, trigger, start/end time,
scope, adapter/normalization versions, revision/checkpoint, measured counts,
warnings/errors, snapshot reference, execution outcome, publication state, and
cancellation/recovery context. Counts have defined per-source meanings; discovered,
read, normalized, rejected, unchanged, added, modified, and removed are not synonyms.

Useful execution states include queued, running, succeeded, partially succeeded,
failed, cancelled, and interrupted. They are explanatory draft categories, not a
settled transport enumeration. Success concerns the configured processing scope,
not whether the source is true or the portfolio is healthy. Snapshot and publication
states are recorded separately; process exit without exception does not settle them.

# Collection strategies

| Strategy | Appropriate use | Limit |
|---|---|---|
| Full | Initial capture, no reliable cursor, reinterpretation, reconciliation | Full means the configured scope, not the whole world |
| Incremental | Reliable native cursor/log/revision or established comparison | Timestamp alone has no assumed completeness guarantee |
| Bounded | Selected artifacts, paths, history, or time windows | Says nothing about unobserved scopes |
| Reconciliation | Check incremental divergence, removals, cursor invalidity, rewrites | Runs when source characteristics justify it, not necessarily continuously |

Complete/partial describes coverage; incremental/reconciliation describes method;
diagnostic describes intended use. These are not necessarily exclusive snapshot
types. A reconciliation can be partial, and a complete bounded scan still has a
limited scope.

# Snapshot manifest and consistency

A manifest identifies snapshot, source, run, creation time, source revision or
position, scope, method, adapter/normalization/format versions, coverage, measured
counts, validation summary, warnings/errors, predecessor, publication eligibility,
and publication outcome. Stable snapshot identity differs from source revision,
observation interval, creation time, and publication time.

Use immutable revisions or consistent source reads where available. Otherwise
before/after checks or version tokens may detect mutation; retain residual limits.
Published snapshots are not silently rewritten. Corrections can create a new
snapshot or explicitly versioned replacement with preserved lineage.

# Publication and last-known-good state

Publication depends on completed processing, understood scope, applicable coverage
and validation policy, reconciled identities, successful persistence, and a safe
commit boundary. Prepared versioned records plus an atomic pointer switch avoid
half-replaced datasets. A local transaction cannot make unrelated external sources
an atomic cross-source observation.

Keep distinct latest attempt, latest retained snapshot, current published view,
and last-known-good view. They can identify different runs. Source outage retains
prior usable information with freshness qualifications rather than emptying it.

A useful partial observation can be retained without publication. Some use cases
may intentionally publish independently successful subscopes, but the unit of
publication and partial-state presentation need explicit policy. The architecture
does not silently choose source-wide, project-wide, or portfolio-wide atomicity.

# Identity, fingerprints, and removal

Prefer reliable native IDs or source keys, then documented composite keys or local
mappings. Titles, names, paths, and timestamps are not inherently stable. Retain
unresolved identity rather than forcing uncertain matches.

Fingerprints cover meaningful content, metadata, or relationships under an explicit
canonicalization method, excluding observation time. Source-content change and
normalization-version reinterpretation are different events. Useful classifications
include added, modified, unchanged, reliably moved, reidentified, newly discovered,
no longer observable, unresolved, and reinterpreted.

Removal requires sufficient observation and source semantics. Partial enumeration,
permission loss, filter changes, parsing failure, and unsupported formats cannot
establish deletion. Tombstones preserve prior identity/reference/version, observation
time, and removal basis. No evidence is not evidence of absence.

# Idempotency and checkpoint commit safety

Stable identities and deterministic capture/change keys make repeated windows safe
without claiming exactly-once delivery across external systems. Distinct attempts
can have run records while producing no duplicate logical records or artificial changes.

Capture the starting position and target window, read/normalize/validate, persist
records and run state, commit the applicable snapshot/publication state, then
advance the checkpoint only when its required conditions hold. Failures before
commit leave the window safely replayable. Position advancement cannot skip data
that was only read but not durably recorded.

Checkpoint validity is scoped to source, access/collection method, query/filter
scope, configuration, adapter, and protocol semantics. Material changes can require
invalidation. Invalid/lost positions preserve history and usable state while a
controlled full scan or reconciliation establishes a replacement; no speculative
advancement is safe.

# Validation and failure recovery

Access, enumeration, parsing, source-profile validation, identity reconciliation,
relationship resolution, consistency, persistence, and publication answer separate
questions. Blocking findings depend on source/use-case policy. Optional missing
metadata or a noncritical unresolved relationship need not block all publication;
unknown scope, unsafe identity, persistence failure, or partial results masquerading
as complete are fundamentally different risks.

Failures retain source, stage, scope, records, and safe diagnostics. Isolate records
and independent sources where consistency allows. Distinguish configuration/access,
enumeration, timeout/rate limit, format, identity, validation, persistence,
publication, cancellation/interruption, and internal errors. Invalid configuration
or malformed content does not justify endless retries. Transient failures need
bounded retries respecting source guidance and transaction state.

Recovery reconciles what was read, processed, committed, and published. If assembly
was persisted but publication failed, retry the safe publication step rather than
needlessly scanning again. Interrupted work resumes from a valid checkpoint or
restarts a bounded window. A successful record does not convert an interrupted run
into a complete refresh.

# Retained history and privacy

Run diagnostics, manifests, normalized versions, raw payloads, change/tombstone
records, validation results, checkpoints, and report references can have different
retention periods. Compact metadata and historical normalized versions are a
proposed starting direction, not an approved retention budget. Full repositories,
patches, or knowledge collections are not automatically copied for convenience.

Before pruning, consider retained reviews, reports, decision rationale, descendant
lineage, and investigations. Referenced history needs either preservation or an
explicitly recorded loss of reproducibility under an agreed policy. A fingerprint
alone detects change but cannot reconstruct content. Do not promise exact replay
when payloads, revisions, transformations, or rules are unavailable.

Track snapshot/record growth, database size, raw/diff volume, historical versions,
and abandoned runs. Retention and exports retain the same privacy boundary as
capture. Authorized roots, controlled arguments, untrusted-content isolation,
credential separation, and safe logs protect local and private source data.

# Diagnostics, validation approach, and open choices

Operational views can explain latest attempt/success/publication, current snapshot,
coverage, freshness, changed/rejected counts, position advancement, awaiting
publication, and errors needing intervention. Duration, latency, retries, size,
and unresolved-record counts need consistent definitions rather than cross-source
labels with different hidden meanings.

Validation targets include full/incremental/bounded and partial scans, unchanged
replays, actual removals, source mutation, lost positions, parser upgrades,
duplicates, interruption, persistence/publication failures, last-known-good
preservation, pruning, access constraints, independent source failures, and
historical report reconstruction. Especially important are premature checkpoints,
false removals, duplicate replay, and half-visible publication.

Still open: manual/scheduled triggers, per-source completeness, publication unit,
partial publication policy, actual cursors, raw-content retention, referenced-history
budgets, upgrade reprocessing, cancellation/resume semantics, resource/freshness
limits, and whether capture and analysis initially need separate jobs.

Related: [source adapters](source-adapters.md),
[deterministic analysis](deterministic-analysis.md),
[source history and provenance](../decisions/source-history-and-provenance.md).