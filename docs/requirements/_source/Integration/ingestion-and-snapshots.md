# Ingestion and Snapshots

**Document:** `ingestion-and-snapshots.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Shared source ingestion, snapshot creation, incremental refresh, history, recovery, and normalized-view management

**Related documents:** `source-integration.md`, `data-ownership.md`, `data-model.md`, `domain-model.md`, `application-workflows.md`, `vyasa-integration.md`, `openspec-integration.md`, `okf-integration.md`, `git-evidence.md`, `security-and-privacy.md`

---

## 1. Purpose

This document defines the shared ingestion and snapshot mechanism used by Siddhi to collect information from external source systems, preserve what was observed, and make normalized evidence available for portfolio analysis.

Siddhi integrates with several independent sources:

- **Vyasa:** project and repository inventory.
- **OpenSpec:** requirements, scenarios, change artifacts, and declared task status.
- **OKF:** engineering knowledge and source-defined metadata.
- **Git:** commits, references, tags, and version-control history.
- **Verification systems:** build, test, quality, release, and deployment evidence where available.
- **Other approved sources:** additional integrations introduced as the system evolves.

Each source has its own data model, authority, update behavior, and access limitations. Siddhi needs a common ingestion framework without forcing all sources into identical collection strategies.

The framework must support:

1. Controlled, read-only source access.
2. Full and incremental collection where supported.
3. Deterministic normalization and change detection.
4. Traceable, versioned snapshots.
5. Historical comparison and portfolio review.
6. Safe recovery from partial failures.
7. Clear distinctions between observed facts, derived records, assessments, and recommendations.

## 2. Core design principles

### 2.1 Source authority remains external

Siddhi does not become the authority for repository inventory, requirements, engineering knowledge, or verification results merely because it stores normalized copies.

Each adapter must preserve the identity of the originating source and the meaning of its fields.

### 2.2 Separate collection, processing, and publication

A source scan is not the same as a successful ingestion run, and a successful ingestion run is not necessarily a complete snapshot.

Siddhi must distinguish:

- The attempt to access and enumerate a source.
- The records successfully retrieved.
- The records successfully parsed and normalized.
- The snapshot produced from those records.
- The normalized view made available to portfolio analysis.

This separation prevents incomplete scans from appearing as complete current state.

### 2.3 Deterministic processing by default

Routine source reading, parsing, normalization, fingerprinting, deduplication, comparisons, and reporting must be deterministic.

External AI is optional and belongs in a separate analysis stage. It must not be required for ordinary ingestion or used to conceal source-processing failures.

### 2.4 Historical observations must be explainable

Siddhi should retain enough historical information to explain what it knew when a portfolio assessment or report was produced.

A refresh must not silently overwrite the only record of an earlier observation.

### 2.5 Prefer the simplest reliable collection strategy

Not every source needs a streaming pipeline, event bus, or continuous background worker.

The initial implementation should favor bounded scans, explicit refresh operations, deterministic processing, and recoverable transactions. More sophisticated scheduling or incremental mechanisms should be added when source behavior and actual requirements justify them.

## 3. Terminology

The following terms have specific meanings in this document.

| Term | Meaning |
|---|---|
| Source | An external system or configured data location |
| Source configuration | Siddhi's settings for accessing and collecting from a source |
| Scan | An attempt to enumerate or inspect a source |
| Ingestion run | A tracked execution that collects, processes, and records source information |
| Ingestion batch | A bounded unit of work within a run |
| Source record | A source item retrieved or identified by an adapter |
| Normalized record | Siddhi's internal representation of a source record |
| Snapshot | A recorded observation of a defined source scope at a particular collection point |
| Snapshot manifest | Metadata describing a snapshot's scope, coverage, revision, and outcome |
| Current normalized view | The latest usable Siddhi representation of source information |
| Checkpoint | A source-specific position or cursor used to resume incremental collection |
| Watermark | A source-specific boundary used to describe how far collection has progressed |
| Fingerprint | A deterministic digest used to detect content changes |
| Evidence record | A source-derived or system-derived record available to portfolio assessment |
| Assessment | Siddhi's interpretation of evidence against a goal, criterion, or policy |
| Publication | Making a completed ingestion result the current usable view |
| Tombstone | A retained marker indicating that a previously observed source item was removed or no longer present within a sufficiently observed scope |

A checkpoint is not automatically a watermark, and neither proves that a source has been fully scanned. Their meanings depend on the source adapter's contract.

## 4. Architectural overview

```text id="7nb2vr"
Source Configuration
        |
        v
Ingestion Orchestrator
        |
        v
Source Adapter
        |
        v
Scan / Enumeration / Incremental Read
        |
        v
Raw Observation Metadata
        |
        v
Parsing and Normalization
        |
        v
Identity, Fingerprint and Validation
        |
        v
Snapshot Assembly
        |
        v
Coverage and Consistency Checks
        |
        v
Atomic Publication of Usable View
        |
        v
Evidence and Portfolio Analysis
        |
        v
Reports, Reviews and Historical Comparison
```

The architecture should separate these responsibilities logically even if the initial implementation places them in one Python application and one SQLite database.

### 4.1 Ingestion orchestrator

The orchestrator coordinates runs and manages:

- Source configuration.
- Run identity and status.
- Adapter invocation.
- Bounded execution and cancellation.
- Checkpoint handling.
- Snapshot assembly.
- Error classification.
- Safe retries.
- Publication eligibility.
- Operational diagnostics.

It should not contain source-specific parsing rules.

### 4.2 Source adapters

Each adapter defines:

- Source access method.
- Discovery and enumeration behavior.
- Stable identity rules.
- Supported fields and record types.
- Version or revision signals.
- Incremental collection capabilities.
- Deletion-detection semantics.
- Pagination and resource limits.
- Error handling and retry guidance.
- Validation capabilities.
- Source-specific freshness interpretation.

An adapter must explicitly declare which capabilities it supports. The orchestrator must not assume every source provides a reliable change cursor, consistent snapshot, or complete deletion feed.

### 4.3 Normalization service

The normalization service converts supported source records into Siddhi's internal models.

It must preserve:

- Original source identifiers.
- Source-specific fields where feasible.
- Source status and declared metadata.
- Provenance and source location.
- Revision or version context.
- Parsing and validation outcomes.

Normalization must not convert an unknown field into an invented meaning or silently replace a source declaration with a Siddhi assessment.

### 4.4 Persistence and publication

Persistence manages:

- Ingestion run records.
- Source snapshots and manifests.
- Normalized record versions.
- Current normalized views.
- Provenance and diagnostics.
- Checkpoints.
- Historical comparison metadata.
- Publication status.

A completed run should become visible as the current normalized view only after it satisfies the applicable publication rules.

---

## 5. Source configuration and capabilities

Each configured source must have a stable Siddhi source ID and an explicit configuration.

A source configuration should support the following information where applicable:

| Field | Purpose |
|---|---|
| Source ID | Stable Siddhi identifier |
| Source type | Vyasa, OpenSpec, OKF, Git, verification, or another adapter |
| Display name | Human-readable source label |
| Access method | Filesystem, CLI, API, or other supported mechanism |
| Source location/reference | Configured location or external source identity |
| Associated project | Optional Vyasa project reference |
| Enabled state | Whether collection is permitted |
| Collection policy | Full, incremental, bounded, or source-specific |
| Capability declaration | Supported collection and validation operations |
| Configuration revision | Identifies the settings used by a run |
| Last attempted run | Most recent attempt |
| Last successful run | Most recent successful collection |
| Last published snapshot | Latest snapshot made available for use |

Secrets must be stored through an appropriate credential mechanism and must not be embedded in ordinary source metadata.

### 5.1 Capability declaration

Adapters should report whether they support:

- Full enumeration.
- Incremental enumeration.
- Stable source identities.
- Source revisions or versions.
- Consistent point-in-time snapshots.
- Change cursors or checkpoints.
- Reliable deletion detection.
- Source-side validation.
- Direct comparison or change queries.
- Cancellation and resumable execution.

Unsupported capabilities must remain explicit.

For example, an OKF filesystem adapter may enumerate documents and compare fingerprints, while a remote verification API may expose incremental updates and a server-provided cursor. The shared framework must accommodate both without pretending their consistency guarantees are identical.

---

## 6. Ingestion run lifecycle

Every ingestion execution must have a stable run ID.

### 6.1 Run record

A run record should include:

- Run ID.
- Source ID.
- Source configuration revision.
- Trigger type.
- Start time and completion time.
- Adapter and normalization versions.
- Intended collection scope.
- Observed source revision or checkpoint, if available.
- Run outcome.
- Counts of discovered, read, normalized, rejected, unchanged, added, modified, and removed records where meaningful.
- Warnings and errors.
- Snapshot ID, if created.
- Publication status.
- Cancellation or recovery details where applicable.

Counts must reflect what the adapter actually measured. They should not be presented as comparable across different source types without a defined meaning.

### 6.2 Run states

The shared lifecycle should support at least these states:

- **Queued:** accepted but not started.
- **Running:** collection or processing is underway.
- **Succeeded:** the configured scope completed successfully and required results were persisted.
- **Partially succeeded:** useful results were collected, but a known portion of the configured scope failed or could not be assessed.
- **Failed:** the run could not produce a usable result under the applicable policy.
- **Cancelled:** execution was intentionally stopped.
- **Interrupted:** execution ended unexpectedly and recovery status has not yet been reconciled.

Snapshot creation and publication status should be tracked separately from the run outcome where necessary. For example, a run may successfully produce a partial snapshot that is retained for diagnostics but not published as the current complete view.

### 6.3 Run completion

A run must not be marked successful merely because the adapter process returned without an exception.

Completion requires the configured scope to be reconciled against the adapter's declared capabilities and the applicable acceptance rules.

A run may be partially successful if the system can safely retain useful results and clearly identify the incomplete scope.

---

## 7. Collection strategies

### 7.1 Full scan

A full scan enumerates the configured source scope and collects the records required to represent it.

Use this approach when:

- Initializing a source.
- The source does not provide reliable incremental signals.
- The prior checkpoint is invalid.
- A schema or normalization change requires reprocessing.
- A reconciliation scan is needed to verify incremental state.

A full scan should establish the scope it actually examined. If enumeration is incomplete, the result must not be treated as a complete representation of the source.

### 7.2 Incremental scan

An incremental scan collects changes since a previously established source position or snapshot.

It may use:

- A stable revision.
- A provider-supplied cursor.
- A source-specific change log.
- A reliable modified-since mechanism.
- A Git revision range.
- Deterministic comparison against a prior complete enumeration.

The adapter must document the semantics and limitations of its incremental mechanism.

If the source does not provide reliable incremental signals, Siddhi must not invent a cursor or assume that timestamps alone guarantee complete change detection.

### 7.3 Bounded scan

A bounded scan collects a deliberately limited subset, such as:

- A defined Git history range.
- A specific set of OpenSpec artifacts.
- Selected OKF documents.
- A defined time window of verification events.

The resulting snapshot must identify the scope and limitations. A bounded scan cannot establish that records outside its scope are absent.

### 7.4 Reconciliation scan

A reconciliation scan compares the stored view with a sufficiently complete observation of the source.

It is useful for detecting:

- Missed incremental changes.
- Removed records.
- Invalid checkpoints.
- Source history rewrites.
- Changes in collection capabilities.
- Unexpected divergence between the source and Siddhi.

Reconciliation should be scheduled or triggered according to source characteristics and practical needs. It need not run continuously.

---

## 8. Snapshot semantics

A snapshot records what Siddhi observed about a defined source scope at a particular collection point.

It is not necessarily a perfect atomic copy of the external source. Some sources can change while being scanned, and some cannot provide consistent point-in-time reads.

### 8.1 Snapshot types

Siddhi should distinguish the following logical snapshot types:

**Complete snapshot**

The configured scope was enumerated and processed successfully according to the source's declared capabilities and publication policy.

**Partial snapshot**

Some records or subscopes were observed, but the configured scope could not be fully assessed.

**Incremental snapshot**

The snapshot represents a defined change interval or source position rather than a full enumeration.

**Diagnostic snapshot**

An observation retained for troubleshooting or history that is not eligible to replace the current usable view.

**Reconciliation snapshot**

A snapshot produced to compare or re-establish alignment between the source and Siddhi's stored view.

These categories describe different properties and may be represented by separate fields rather than one mutually exclusive status. For example, a reconciliation snapshot may be complete or partial.

### 8.2 Snapshot manifest

Each snapshot should have a manifest containing:

- Snapshot ID.
- Source ID.
- Run ID.
- Snapshot type.
- Creation time.
- Source revision or checkpoint, if available.
- Collection scope.
- Adapter and normalization versions.
- Schema or format version, where applicable.
- Coverage status.
- Record counts.
- Validation summary.
- Warnings and errors.
- Predecessor snapshot, where applicable.
- Publication eligibility and publication outcome.

The manifest must allow a later report to explain which source observation it used.

### 8.3 Snapshot consistency

If a source supports an immutable revision or a consistent snapshot mechanism, Siddhi should use that capability where practical.

If a source changes during collection and cannot provide a consistent view, the adapter should record the limitation. It may use before-and-after revision checks, provider version tokens, or other source-specific consistency signals where available.

A snapshot must not be described as atomic or point-in-time consistent unless the source and collection method actually support that claim.

### 8.4 Snapshot identity

Snapshot IDs must be unique and stable after creation.

A snapshot should not be silently rewritten in place after publication. Corrections should produce a new snapshot or a clearly versioned replacement with an audit trail.

The implementation should distinguish:

- The identity of a snapshot.
- The source revision represented.
- The time Siddhi collected it.
- The time it was published for use.

These timestamps can differ.

---

## 9. Current normalized view

The current normalized view is the latest usable representation of a source's information in Siddhi.

It is optimized for application queries and portfolio analysis. It does not replace historical snapshots.

### 9.1 Publication policy

A new snapshot should replace the current view only when:

1. The run has completed the required processing.
2. The configured scope is understood.
3. The result satisfies the applicable completeness and validation policy.
4. Stable record identities have been reconciled.
5. Persistence has succeeded.
6. The publication operation can be committed safely.

A partial or diagnostic snapshot may be retained without replacing the current complete view.

Some sources may explicitly permit partial publication for selected use cases. Such behavior must be an intentional source-specific policy, not a general fallback.

### 9.2 Atomic publication

Where the persistence mechanism supports transactions, publication should update the current-view pointer and associated records within a transaction or equivalent safe commit boundary.

For larger snapshots, Siddhi may prepare a new version separately and switch the current-view reference only after preparation succeeds.

This avoids exposing a partially replaced dataset if the process fails halfway through publication.

### 9.3 Current state versus last-known-good state

Siddhi should distinguish:

- **Latest attempt:** the most recent collection attempt, whether successful or not.
- **Latest observed snapshot:** the latest snapshot successfully recorded.
- **Current published view:** the snapshot currently used for normal queries.
- **Last-known-good view:** the latest snapshot that satisfied the required publication policy.

These may point to different runs.

If a source becomes unavailable, Siddhi must preserve the last-known-good view and mark its freshness accordingly. It must not erase usable historical information simply because a refresh failed.

---

## 10. Identity, fingerprints, and change detection

### 10.1 Stable source identity

Every normalized record must have an identity strategy appropriate to its source.

Preferred identity sources include:

1. A stable native source identifier.
2. A stable source-defined key.
3. A documented composite key using reliable source fields.
4. A Siddhi-managed mapping when the source lacks a stable identifier.

Titles, file names, directory names, and timestamps should not be assumed to be permanent identifiers unless the source contract guarantees that property.

### 10.2 Fingerprints

Siddhi may calculate a deterministic fingerprint from the relevant source content and metadata.

Fingerprint inputs should be defined per adapter. The calculation should exclude fields that change only because Siddhi collected the record again, such as the latest observation timestamp.

Where serialization differences are irrelevant, canonicalization should be used before hashing.

Fingerprints should support detection of:

- Unchanged content.
- Changed content.
- Changed source metadata.
- Changed relationships.
- Changes in the normalized representation caused by parser or schema upgrades.

A parser upgrade must not automatically be reported as a source-content change. Source changes and normalization-version changes should be distinguishable.

### 10.3 Change classifications

The shared framework should support classifications such as:

- Added.
- Modified.
- Removed.
- Unchanged.
- Moved or renamed, when reliably identified.
- Reidentified.
- Newly discovered.
- No longer observable.
- Unresolved.
- Reinterpreted due to a normalization change.

The adapter must define which classifications it can establish reliably.

### 10.4 Removal detection

A record may be marked removed only when the collection method provides sufficient evidence that it no longer exists within the relevant source scope.

A record absent from a partial scan must not be marked removed.

When deletion cannot be established, Siddhi should record the record as not observed, inaccessible, or unresolved, according to the available evidence.

A tombstone should preserve the prior record identity, source reference, last-known version, removal-observation time, and basis for the removal classification.

---

## 11. Idempotency and checkpoint safety

### 11.1 Idempotent processing

Repeated processing of the same source revision or collection window should not create duplicate logical records or artificial change events.

The framework should use stable source identities, snapshot IDs, run IDs, and deterministic change keys to make retries safe.

If the same source item is observed again with changed content, Siddhi should update the current normalized representation and preserve the earlier version where required by the retention policy.

### 11.2 Checkpoint lifecycle

A checkpoint may be advanced only after the corresponding records and ingestion state have been persisted successfully.

For an incremental run, the expected sequence is:

1. Capture the starting checkpoint.
2. Establish the bounded collection window or target position.
3. Read the relevant changes.
4. Normalize and validate the results.
5. Persist the records and run metadata.
6. Commit the resulting snapshot or current-view update.
7. Advance the checkpoint only when the applicable persistence and publication rules are satisfied.

If a run fails before its checkpoint is committed, a retry must be able to reprocess the same window safely.

The framework should not claim exactly-once delivery across external systems. Its practical guarantee should be safe, idempotent processing within the capabilities of each source and the Siddhi persistence layer.

### 11.3 Checkpoint scope

A checkpoint must be scoped to the source and collection method that produced it.

It may also depend on:

- Source configuration revision.
- Adapter version.
- Query or enumeration scope.
- Filter configuration.
- Source schema or protocol version.

A checkpoint must not be reused after a material change in scope or semantics unless the adapter explicitly establishes that reuse is safe.

### 11.4 Invalid or lost checkpoints

If a checkpoint becomes invalid, Siddhi should:

1. Record the condition.
2. Preserve prior snapshots and the current usable view.
3. Avoid advancing the checkpoint speculatively.
4. Attempt a controlled reconciliation or full rescan if supported.
5. Publish a replacement only after it meets the applicable policy.

---

## 12. Validation and quality gates

Validation must be layered and source-aware.

### 12.1 Validation layers

| Layer | Question answered |
|---|---|
| Access validation | Can Siddhi access the configured source? |
| Enumeration validation | Was the intended scope discovered? |
| Parsing validation | Can the source content be interpreted? |
| Schema validation | Does the content satisfy the applicable source schema, if supported? |
| Identity validation | Can records be assigned stable identities? |
| Referential validation | Can expected relationships be resolved? |
| Consistency validation | Does the snapshot satisfy the source-specific completeness rules? |
| Persistence validation | Were records and snapshot metadata stored successfully? |
| Publication validation | Is the snapshot safe to use as the current view? |

These checks must not be collapsed into a single generic "valid" flag.

### 12.2 Blocking and non-blocking findings

The framework should distinguish findings that prevent publication from warnings that allow publication.

Examples of potentially blocking conditions include:

- The configured source identity cannot be established.
- The required scope could not be enumerated.
- A source-specific consistency requirement failed.
- Record identities cannot be reconciled safely.
- Persistence did not complete.
- A partial result would otherwise be presented as complete.

Examples of warnings may include:

- Optional metadata is missing.
- Some non-essential fields could not be parsed.
- A supported but non-critical relationship remains unresolved.
- The source does not expose a verification signal.

The exact policy must be configured by source type and use case. A missing optional field in OKF must not necessarily block ingestion of every other knowledge document.

### 12.3 Parsing does not establish truth

Successful ingestion means that Siddhi collected and processed data according to the applicable rules. It does not prove that source declarations are accurate.

The framework must preserve source-declared status and validation results separately from Siddhi's own processing outcomes.

---

## 13. Failure handling and recovery

### 13.1 Failure isolation

Where possible, an error in one source must not prevent unrelated sources from being ingested.

Likewise, a malformed record should not automatically prevent the processing of every other record unless the source's consistency contract requires all-or-nothing processing.

The run must identify the affected source, scope, records, and processing stage.

### 13.2 Failure categories

The framework should classify failures such as:

- Configuration failure.
- Access or authentication failure.
- Enumeration failure.
- Rate limit or timeout.
- Parsing failure.
- Unsupported schema or format.
- Identity or reconciliation failure.
- Validation failure.
- Persistence failure.
- Publication failure.
- Cancellation or interruption.
- Internal processing error.

Failure categories should support meaningful diagnostics, retries, and operational reports.

### 13.3 Retry policy

Retries should be bounded and based on failure type.

- Temporary access failures may be retried.
- Rate-limited requests should respect source guidance.
- Invalid configuration should require correction.
- Malformed content should be recorded rather than retried indefinitely.
- Persistence failures should retry only when the transaction and run state can be reconciled safely.
- Interrupted runs should resume from a safe checkpoint or restart the affected bounded operation.

### 13.4 Recovery and reconciliation

Recovery must preserve a clear distinction between:

- What was committed successfully.
- What was only read.
- What was partially processed.
- What was published.
- What remains to be retried.

If publication fails after a snapshot has been persisted, Siddhi should retain the snapshot and reconcile its publication state rather than unnecessarily repeating the entire source scan.

---

## 14. Historical retention and storage

Siddhi must balance historical explainability, storage cost, privacy, and source licensing or access restrictions.

### 14.1 Information to retain

The retention policy should consider separate categories:

- Run records and diagnostics.
- Snapshot manifests.
- Normalized record versions.
- Source-provided raw content or immutable copies, if retained.
- Change records and tombstones.
- Validation results.
- Checkpoints and recovery state.
- Portfolio reports and their source snapshot references.

These categories do not need identical retention periods.

### 14.2 Default design direction

The initial design should favor retaining compact metadata and normalized historical versions needed to explain portfolio changes.

Full raw-content retention should be decided separately for each source. Siddhi should not copy complete repositories or entire knowledge collections merely to make ingestion easier.

Where raw content is not retained, the snapshot must still preserve enough source identity, revision information, fingerprints, and provenance to explain what was observed, subject to the source's available capabilities.

### 14.3 Pruning

Pruning must not remove information that is still required to interpret a retained report or an approved decision's rationale.

Before removing an older snapshot, Siddhi should determine whether it is referenced by:

- A portfolio review.
- An analysis report.
- A decision or decision revision.
- A later snapshot's lineage.
- An unresolved investigation or audit requirement.

If a snapshot is removed under an approved policy, its removal should be recorded where required.

### 14.4 Storage limits

The implementation should monitor:

- Number of snapshots per source.
- Number of normalized records.
- Database size.
- Retained raw content and diff size, where applicable.
- Historical version growth.
- Failed and abandoned ingestion runs.

Storage controls should be proportionate to the local-first deployment. Sophisticated archival infrastructure should not be introduced without a demonstrated need.

---

## 15. Security and privacy

The ingestion framework must:

- Use configured, authorized source access.
- Respect source permissions and access scopes.
- Use read-only operations unless a separate future feature is explicitly authorized.
- Restrict filesystem access to approved locations.
- Avoid executing source-provided scripts during ordinary ingestion.
- Protect credentials and tokens.
- Avoid logging secrets or sensitive source content unnecessarily.
- Validate paths, identifiers, and query parameters.
- Treat retrieved content as untrusted input.
- Prevent source content from overriding Siddhi's operational instructions.
- Apply privacy rules before sending content to external AI.
- Record the source context supplied to external analysis where appropriate.
- Avoid exposing local filesystem paths or private repository metadata to unauthorized API clients.

Retention and export must follow the same privacy rules as initial ingestion. Storing content locally does not remove the need to control access to it.

---

## 16. Observability and operational reporting

Siddhi should provide enough information to answer:

- Which sources have been configured?
- When was each source last scanned?
- Which scans succeeded, partially succeeded, or failed?
- Which snapshot is currently published?
- How fresh is the current view?
- Which sources have not been refreshed recently?
- Which errors require intervention?
- How many records were discovered, changed, rejected, or removed?
- Which checkpoints were advanced?
- Which snapshots are awaiting publication or reconciliation?

Operational reports should use clear language and distinguish a technical failure from a source that simply has no new changes.

Useful metrics include:

- Run duration.
- Success and failure counts.
- Records processed.
- Processing and publication latency.
- Snapshot size.
- Time since last successful scan.
- Time since last successful publication.
- Retry count.
- Number of unresolved or quarantined records.

Metrics must have documented definitions so that the same label does not imply different measurements across adapters.

---

## 17. Testing requirements

The ingestion framework must be tested for:

1. Initial full scans.
2. Incremental scans.
3. Bounded scans.
4. Complete and partial snapshots.
5. Repeated ingestion of unchanged source content.
6. Source records modified between scans.
7. Record additions and confirmed removals.
8. Incomplete enumeration.
9. Source changes during collection.
10. Invalid or lost checkpoints.
11. Parser and normalization version changes.
12. Schema evolution and unknown fields.
13. Duplicate source records.
14. Interrupted runs.
15. Persistence failures.
16. Publication failures.
17. Safe retries and reconciliation.
18. A failed run followed by a successful run.
19. A source that becomes unavailable after a successful scan.
20. A partial scan that must not replace the last-known-good view.
21. Retention and pruning of historical snapshots.
22. Access-control and untrusted-content handling.
23. Independent failure of multiple configured sources.
24. Historical report reproducibility using recorded snapshot references.

Tests must prove that a checkpoint is not advanced prematurely, retries do not create duplicate logical records, and incomplete scans do not produce false deletion or absence claims.

---

## 18. Acceptance criteria

The shared ingestion framework is ready when:

- Every configured source has a stable Siddhi identity.
- Every run records its source, scope, timing, outcome, and processing version.
- Adapters declare their collection capabilities and limitations.
- Full, incremental, and bounded scans are distinguished.
- Snapshots have stable identities and traceable manifests.
- The system separates observed snapshots from the current published view.
- Incomplete scans cannot silently replace the last-known-good view.
- Normalized records preserve source identity and provenance.
- Fingerprinting and change detection are deterministic for a fixed source state and configuration.
- Repeated processing is idempotent within the supported source and persistence guarantees.
- Checkpoints advance only after the corresponding processing and persistence conditions are met.
- Removal detection respects scan completeness and source semantics.
- Failed runs preserve prior usable data.
- Publication is atomic or otherwise protected against partially visible updates.
- Historical snapshots support portfolio review and report traceability.
- Source-specific failures do not unnecessarily block unrelated sources.
- Routine ingestion does not require external AI.
- Retention and privacy rules apply to raw content, normalized records, and historical snapshots.
- The framework exposes operational status and actionable diagnostics.

---

## 19. Implementation phases

### Phase 1 — Shared ingestion foundation

Implement:

- Source configuration.
- Run IDs and lifecycle.
- Adapter capability declarations.
- Bounded execution.
- Basic normalization contracts.
- Error and diagnostic records.

**Deliverable:** Siddhi can execute and track a read-only ingestion run for one source.

### Phase 2 — Snapshot persistence and publication

Implement:

- Snapshot manifests.
- Normalized record persistence.
- Source provenance.
- Last-known-good view.
- Safe publication.
- Idempotent record handling.

**Deliverable:** Siddhi can preserve a source observation and expose a consistent usable view.

### Phase 3 — Change detection and incremental refresh

Implement:

- Stable identities and fingerprints.
- Snapshot comparison.
- Source-specific checkpoints.
- Incremental refresh where supported.
- Removal semantics.
- Reconciliation and safe retry.

**Deliverable:** Siddhi can refresh sources efficiently without losing historical context or incorrectly marking records as absent.

### Phase 4 — Operational resilience and retention

Implement:

- Failure classification.
- Interrupted-run recovery.
- Retry policies.
- Operational reports.
- Retention and pruning.
- Storage and performance measurements.

**Deliverable:** The ingestion system can recover from expected failures and remain understandable to its operator.

### Phase 5 — Cross-source evidence integration

Integrate the shared framework with:

- Vyasa project discovery.
- OpenSpec artifact ingestion.
- OKF knowledge ingestion.
- Git evidence collection.
- Verification evidence collection.

**Deliverable:** Siddhi can combine independent source snapshots into traceable portfolio assessments.

### Phase 6 — Advanced scheduling and analysis

Add background scheduling, more sophisticated incremental strategies, and optional AI-assisted interpretation when justified by real usage.

**Deliverable:** Reduced manual refresh effort without unnecessary operational complexity.

---

## 20. Open questions

| ID | Question | Why it matters |
|---|---|---|
| IS-001 | Should source refresh initially be manual, scheduled, or both? | Determines orchestration complexity |
| IS-002 | Which sources require historical raw-content retention versus normalized metadata only? | Affects privacy, storage, and reproducibility |
| IS-003 | What constitutes a complete snapshot for each source type? | Controls safe publication and removal detection |
| IS-004 | Which source-specific checkpoints and incremental mechanisms are available? | Determines refresh efficiency and correctness |
| IS-005 | What should happen when a source scan is partial but still yields useful evidence? | Determines publication policy |
| IS-006 | Which snapshots must be retained for portfolio reviews and approved decisions? | Defines historical retention |
| IS-007 | Should a parser or normalization upgrade trigger full reprocessing? | Affects migration and historical comparison |
| IS-008 | Which operations should be cancellable, resumable, or restart-only? | Determines recovery behavior |
| IS-009 | What are the initial resource limits for scan duration, records, history, and content size? | Protects local performance |
| IS-010 | What are the minimum freshness expectations for each source? | Supports useful stale-evidence reporting |
| IS-011 | Should source ingestion and portfolio analysis execute as separate jobs in the first release? | Affects application and job architecture |
| IS-012 | What retention and export policy applies to sensitive source content? | Defines privacy and operational constraints |

---

## 21. Reference material

The following references provide useful background for the design principles in this document:

- [Microsoft Learn: Delta Lake architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/deployment-guide/delta-lake) — discusses separation of original ingested data from refined representations, incremental processing, and lineage. Its specific platform choices are not requirements for Siddhi. <Link url="https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/deployment-guide/delta-lake" title="Read the architecture guide"/>.
- [Data pipeline architecture patterns](https://adr.dtt.digital.wa.gov.au/reference-architectures/data-pipelines.html) — describes source adapters, source positions, idempotent processing, and recovery boundaries. <Link url="https://adr.dtt.digital.wa.gov.au/reference-architectures/data-pipelines.html" title="Read the pipeline patterns"/>.
- [Incremental sync RFC](https://github.com/satishbabariya/etl/blob/main/docs/rfc/RFC-0007-incremental-sync.md) — discusses resumable snapshots and why incomplete snapshots should not automatically be treated as complete state. <Link url="https://github.com/satishbabariya/etl/blob/main/docs/rfc/RFC-0007-incremental-sync.md" title="Read the incremental-sync RFC"/>.

These references inform general ingestion design. Siddhi's actual guarantees must be established through its source contracts, implementation, and tests.

**Document status:** Draft for review. Source-specific snapshot guarantees, publication policy, checkpoint semantics, and retention rules must be finalized before deriving implementation-level OpenSpec requirements.