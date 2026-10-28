# Persistence and Migrations

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `persistence-and-migrations.md`  
**Status:** Draft for review  
**Scope:** Backend persistence, database transactions, schema evolution, data recovery, and migration safety  
**Implementation status:** Not yet verified in a running system

---

## 1. Purpose

This document defines how Siddhi persists its own data, evolves its database schema, and protects information during application upgrades, ingestion failures, and recovery.

The persistence layer must support Siddhi's local-first architecture while preserving historical evidence, source provenance, planning decisions, and reproducible analysis results.

The document distinguishes three concerns:

1. **Logical data model:** The entities and relationships Siddhi needs to represent.
2. **Persistence design:** How those entities are stored, retrieved, and updated.
3. **Schema migrations:** How the stored representation evolves safely between application versions.

The persistence implementation must support the domain and data-ownership rules defined in `domain-model.md`, `data-model.md`, and `data-ownership.md`. It must not redefine the authority of external systems.

## 2. Design principles

### 2.1 Persistence is an implementation detail

Application and domain logic must not depend directly on SQLite-specific SQL, database connections, or ORM session behavior.

Use repository or persistence interfaces at appropriate domain boundaries. SQLite is the proposed initial implementation, not an assumption that every future deployment must use the same database engine.

### 2.2 Preserve historical truth

Siddhi must retain the history necessary to explain:

- What the system knew at a particular point in time.
- Which source scan or snapshot produced an evidence record.
- Which rules and inputs produced an analysis result.
- Which plan or decision revision was active at the time.
- What recommendation was presented and what decision followed.
- Which migration or software version changed the stored representation.

Historical records must not be silently rewritten merely to make the current view convenient.

### 2.3 Protect the last-known-good state

A failed ingestion, analysis run, or database migration must not leave the application presenting incomplete or corrupt data as the latest complete state.

Where a source refresh is partial, Siddhi must preserve the previous usable view and explicitly record the partial outcome.

### 2.4 Make operations recoverable

Database operations must have defined transaction boundaries, failure behavior, and recovery expectations.

A retry must not create duplicate logical records or advance a checkpoint beyond successfully persisted data.

### 2.5 Keep persistence proportionate

The initial implementation should use one local database and a small number of well-defined persistence abstractions. Distributed databases, event-streaming infrastructure, and elaborate storage frameworks are out of scope unless demonstrated requirements justify them.

## 3. Proposed technology and scope

| Area | Proposed baseline | Status |
|---|---|---|
| Database | SQLite | Proposed |
| Database access | Python persistence/repository layer | Proposed |
| Schema changes | Versioned, ordered migrations | Required capability |
| Transaction management | Explicit transaction boundaries | Required capability |
| Schema version tracking | Database migration ledger | Required capability |
| Data interchange | Versioned export format | To be designed |
| Backup and restore | Consistent database backup and validated restoration | Required capability |
| Multi-user concurrent writes | Not an initial requirement | Open for future review |
| Remote database | Not in initial scope | Deferred |

The precise Python database library, ORM choice, and migration framework remain implementation decisions. The chosen libraries must support explicit transactions, predictable migrations, testable repository behavior, and SQLite's concurrency characteristics.

## 4. Persistence boundaries

Siddhi owns its portfolio and planning records, but it does not own the source systems from which engineering evidence is obtained.

### 4.1 Data Siddhi owns

Siddhi's database is authoritative for its own records, including:

- Goals and intended outcomes.
- Initiatives and portfolio priorities.
- Plans, plan revisions, milestones, and dependencies.
- Reviews, assumptions, and constraints.
- Decisions and decision revisions.
- Source connection configuration and ingestion history.
- Normalized source snapshots and evidence references.
- Evidence assessments and deterministic analysis results.
- Reports, external analysis requests, imported responses, and recommendation reviews.
- Application configuration that is explicitly designated for database storage.
- Operational records needed for diagnosis and recovery.

### 4.2 Data Siddhi consumes

Siddhi may retain normalized or captured representations of external information from:

- Vyasa project inventory.
- OpenSpec requirements and change artifacts.
- OKF engineering knowledge.
- Git repositories and source-control metadata.
- Existing build, test, verification, and release artifacts.

Retaining a source representation does not transfer authority for the underlying record to Siddhi.

Where licensing, privacy, security, or storage constraints prohibit retaining full source content, Siddhi should store a permitted summary, stable reference, fingerprint, or limited evidence excerpt instead.

### 4.3 Data that must remain outside the database

Unless a separately approved requirement establishes otherwise, do not store:

- Provider API keys or other secrets in ordinary application tables.
- Arbitrary repository files copied solely for convenience.
- Full Git repository histories or complete diffs without a defined use case.
- Temporary working files that can be safely regenerated.
- Unbounded copies of external source documents.
- Derived metrics that can be cheaply recalculated and have no historical or audit value.

Secret storage, file storage, and backup protection must be defined by the relevant security and operations documents.

## 5. Persistence architecture

The persistence flow is:

**API → application use case → domain rules → repository interface → SQLite implementation**

The API layer must not issue SQL directly. The domain layer must not import SQLite-specific types.

A proposed module structure is:

```text
src/siddhi/
  domain/
    portfolio/
    planning/
    evidence/
    analysis/
  application/
    goals/
    ingestion/
    analysis/
    decisions/
  persistence/
    database.py
    unit_of_work.py
    migrations/
    repositories/
    models/
  integrations/
    vyasa/
    openspec/
    okf/
    git/
  api/
```

This is illustrative. The actual package layout should follow the architecture and project conventions established during implementation.

### 5.1 Repository responsibilities

Repositories should provide domain-oriented operations rather than exposing arbitrary database access.

Examples include:

- Save and retrieve a goal.
- Retrieve a specific plan revision.
- Publish a completed source snapshot.
- Retrieve evidence associated with a snapshot.
- Record an analysis run and its findings.
- Retrieve the full revision history of a decision.

Repositories must not independently implement cross-domain business workflows. Application use cases coordinate operations involving multiple repositories.

### 5.2 Unit of work and transaction ownership

An application use case should define the transaction boundary for a logically atomic operation.

A unit-of-work abstraction may coordinate repository operations within one database transaction.

The design must avoid nested transaction behavior that is difficult to reason about. Savepoints may be used where a concrete workflow requires partial rollback within a larger transaction, but their use must be explicit.

External network calls, repository scans, and AI-provider requests must not normally run inside long-lived database transactions.

## 6. Logical storage groups

The physical schema should follow the logical data model rather than mirror external source formats exactly.

The following groups are proposed.

### 6.1 Portfolio and planning

| Data group | Examples | Persistence expectation |
|---|---|---|
| Portfolio | Goals, outcomes, initiatives, project references | Durable records |
| Planning | Plans, milestones, dependencies | Durable records |
| Revisions | Plan revisions, decision revisions | Historical records |
| Reviews | Review sessions, findings, review notes | Durable history |
| Decisions | Decision records and their rationale | Durable history |

Stable identifiers must survive application restarts and routine edits. A human-readable title must not be used as the sole identifier.

### 6.2 Source integration and ingestion

| Data group | Examples | Persistence expectation |
|---|---|---|
| Source configuration | Source type, enabled state, safe configuration | Durable, with secret separation |
| Ingestion run | Start/end time, status, scope, errors | Durable execution history |
| Snapshot manifest | Source identity, scope, completeness, timestamps | Durable |
| Normalized source record | Project metadata, requirements, knowledge records | Durable within retention policy |
| Source identity mapping | External identity to Siddhi identity | Durable |
| Checkpoint | Last safely committed incremental position | Durable and recoverable |

### 6.3 Evidence and analysis

| Data group | Examples | Persistence expectation |
|---|---|---|
| Evidence record | Commit reference, requirement, test result | Durable according to retention policy |
| Evidence provenance | Source, snapshot, artifact reference | Durable |
| Evidence assessment | Classification, confidence, reason, assessor | Durable and revision-aware |
| Analysis run | Inputs, rule version, execution outcome | Durable |
| Finding | Gap, conflict, stale evidence, candidate match | Durable |
| Report | Structured result and generation metadata | Durable where historical comparison matters |

### 6.4 External analysis

| Data group | Examples | Persistence expectation |
|---|---|---|
| Analysis request | Purpose, selected context, template version | Durable |
| Provider execution | Provider/model metadata, outcome, usage where available | Durable |
| Imported response | Structured response and provenance | Durable within privacy policy |
| Recommendation | Proposed action and supporting references | Durable |
| Review or decision | Human disposition and rationale | Durable |

The exact table boundaries, normalization strategy, and relationship cardinalities must be finalized against `data-model.md` before migrations are implemented.

## 7. Identity, constraints, and relationships

### 7.1 Stable identifiers

Use stable, opaque identifiers for application-owned entities. UUIDs or another consistently implemented identifier strategy are acceptable candidates.

External source identities must be retained separately from Siddhi's internal IDs.

A source identity should normally be scoped by source system and source instance. A project identifier from one inventory must not automatically be treated as identical to a similarly named project from another source.

### 7.2 Database constraints

Use database constraints wherever they can reliably enforce an invariant, including:

- Primary keys.
- Required fields.
- Unique source identities within their defined scope.
- Foreign keys for owned relationships.
- Valid uniqueness rules for migration versions.
- Appropriate uniqueness for idempotency keys and ingestion checkpoints.

Application validation is still necessary for complex domain rules. Database constraints and application validation serve complementary purposes.

### 7.3 Foreign keys and deletion

Foreign-key enforcement must be explicitly enabled and tested for every database connection where SQLite is used.

Deletion policies must be defined per relationship. Do not apply cascading deletion indiscriminately.

In particular:

- Deleting a goal must not silently erase historical analysis reports that referenced it.
- Removing a project from a source inventory must not automatically erase prior source snapshots or evidence.
- Retiring a decision must not remove its earlier revisions.
- Deleting temporary operational data must not delete records required to explain historical decisions.

Prefer explicit archival, retirement, tombstoning, or controlled retention cleanup where history matters.

## 8. Transaction and consistency requirements

### 8.1 Atomic publication of source snapshots

A completed source snapshot must become visible as a coherent unit.

The proposed workflow is:

1. Create an ingestion-run record.
2. Read the external source outside the final publication transaction.
3. Normalize and validate the collected records.
4. Persist the snapshot and its associated records in bounded transactions or staging storage.
5. Verify the snapshot's declared completeness and internal consistency.
6. Publish the snapshot and update the current-view pointer or equivalent state atomically.
7. Advance the ingestion checkpoint only after the corresponding data is safely committed.
8. Mark the run completed or partially completed with an explicit status.

For large ingestions, staging records may be committed incrementally. They must remain distinguishable from the published current view until publication succeeds.

A partial scan must not silently replace a previously complete snapshot.

### 8.2 Analysis-run consistency

An analysis run must identify the exact inputs against which it was executed, including relevant source snapshots, goal or plan revisions, and analysis-rule version.

Where possible, the application should read a consistent database view for the analysis input set.

If the inputs change during a run, Siddhi must either use the captured input version or record that the result is based on a mixed or incomplete input set. It must not claim reproducibility without sufficient input identity.

### 8.3 Multi-record updates

Operations such as creating a plan revision and updating its active revision reference should be atomic.

The same applies to recording a decision revision and updating the current decision state.

Application failures must not leave partially updated records that appear to represent a completed business operation.

### 8.4 Concurrency

SQLite is suitable for an initial local-first, single-user application, but concurrent writes require deliberate handling.

The initial implementation should:

- Keep write transactions short.
- Configure and test a bounded busy-timeout policy.
- Avoid concurrent write operations that contend unnecessarily.
- Define retry behavior for transient lock contention.
- Return a clear application error when an operation cannot safely complete.
- Use optimistic concurrency or revision checks for records that may be edited through multiple clients or background jobs.

WAL mode may be considered after testing the intended deployment and backup behavior. It is not a substitute for transaction design, and it does not eliminate SQLite's single-writer constraint.

## 9. Schema migration strategy

### 9.1 Versioned, ordered migrations

Every schema change must be represented by an ordered, versioned migration.

The database must record which migrations have been applied, including enough metadata to identify the migration and its successful application.

A migration ledger should include, as appropriate:

- Migration version or unique identifier.
- Human-readable description.
- Applied timestamp.
- Migration checksum or equivalent immutable identity.
- Application version that introduced the migration, if available.

The migration ledger must be updated only when the migration has completed successfully.

A previously applied migration must not be silently edited. Corrections should use a new migration, with an explicit repair strategy where necessary.

### 9.2 Migration responsibilities

A migration may:

- Create, alter, or remove database objects.
- Add or change indexes and constraints.
- Transform stored data into a new representation.
- Backfill fields where the transformation is deterministic and safe.
- Update schema metadata.

A migration must not:

- Access external repositories or source systems to reconstruct missing information.
- Make external API calls.
- Invoke an AI provider.
- Silently overwrite user-authored decisions or rationale.
- Treat absent source evidence as proof that an entity no longer exists.
- Depend on an interactive user session to finish after it has begun.

Migrations should be deterministic and repeatable in testing. Where the database engine cannot provide a fully transactional operation for a particular schema change, the migration must define a safe recovery path.

### 9.3 Upgrade sequence

A proposed upgrade sequence is:

1. Identify the database file and current schema version.
2. Confirm the database can be opened and inspected.
3. Acquire the appropriate migration lock.
4. Check database integrity and migration history.
5. Create a recoverable backup or verify an equivalent recovery point.
6. Validate that the application version supports the current database version.
7. Apply pending migrations in order.
8. Run required post-migration checks.
9. Update migration metadata only after successful completion.
10. Release the migration lock and allow normal application operations.

If a migration fails, the application must not report the database as successfully upgraded.

The application should provide an actionable error and preserve a recoverable state. Automatic rollback is acceptable only when the migration's transaction and rollback semantics are well defined.

### 9.4 Upgrade compatibility

Each release must define which database schema versions it can open and whether it supports direct upgrades from older versions.

For an early local-first product, a sequential migration chain is likely sufficient. If users may skip many releases, migration tests must cover the supported upgrade paths, not only the immediately preceding version.

Downgrading application binaries must not be assumed to make a newer database schema compatible with an older application.

A downgrade should be supported only when explicitly designed and tested. Otherwise, recovery should use a compatible application version or restore a verified backup.

## 10. Data migrations and semantic changes

Schema changes and domain-semantic changes are not the same.

For example, renaming a column is a structural change. Changing the meaning of an evidence classification is a semantic change that may affect historical interpretation.

When a semantic change occurs:

1. Identify affected entities and stored results.
2. Decide whether old records retain their original meaning or require a versioned reinterpretation.
3. Preserve the original value or record where historical explanation depends on it.
4. Record the transformation rule and migration version.
5. Distinguish migrated values from independently verified facts.
6. Recalculate derived records only when the inputs and transformation are sufficiently defined.
7. Preserve the original analysis run or mark superseded results explicitly rather than silently replacing history.

Historical reports must remain interpretable even when the current rules or domain vocabulary evolve.

## 11. Migration failure and recovery

### 11.1 Failure handling

If a migration fails:

- Stop subsequent migrations.
- Do not mark the failed migration as applied.
- Record a safe diagnostic where operational logging is available.
- Prevent normal application operations if the current application cannot safely use the partially upgraded schema.
- Preserve the original recovery point.
- Explain the next recovery action without exposing sensitive database content.

If a migration has transactional rollback support, use it. If it cannot be fully rolled back, follow its documented recovery procedure rather than automatically rerunning it against an unknown state.

### 11.2 Backup before upgrade

A backup must be consistent with SQLite's actual journal mode and write state. Copying only the main database file while WAL-mode writes are active may produce an incomplete backup.

The implementation should use a SQLite-supported consistent backup mechanism or another verified approach appropriate to the selected journal mode.

The upgrade process should not overwrite the only known-good backup with an unverified copy.

### 11.3 Restore procedure

A restore workflow should:

1. Identify the backup and its recorded schema version.
2. Verify that the backup is readable and passes appropriate integrity checks.
3. Restore it to a controlled location.
4. Confirm that the application version supports its schema.
5. Run any required migrations on the restored copy.
6. Validate core records and relationships.
7. Make the restored database active only after validation succeeds.
8. Preserve diagnostic information and the previous database until recovery is confirmed.

Restoration must not trigger an unrequested rescan or write to external repositories.

### 11.4 Recovery limitations

A local database backup does not automatically include external source repositories, provider credentials, arbitrary exported files, or external services.

The backup and restore documentation must state exactly what is included and what must be reconfigured or reacquired.

## 12. Backups, exports, and retention

### 12.1 Database backups

The initial system should support creating a consistent backup of the Siddhi database.

Backup metadata should identify:

- Creation time.
- Database schema version.
- Application version, if known.
- Backup format.
- Integrity-check outcome.
- Optional checksum.

Backup frequency, retention count, storage location, and encryption requirements remain open decisions.

### 12.2 Export versus backup

A **backup** is intended to restore a database to a usable state.

An **export** is intended to transfer selected Siddhi-owned data or produce a portable report.

These are distinct operations. A JSON export of goals and reports must not be represented as a full database backup unless it includes all necessary data and restoration semantics.

A portable export should have a documented schema version and a defined policy for stable IDs, provenance references, and omitted sensitive fields.

### 12.3 Retention

Retention rules must distinguish:

- Current normalized source records.
- Historical source snapshots.
- Ingestion-run logs.
- Evidence records and assessments.
- Analysis runs and reports.
- External AI requests and responses.
- Operational diagnostics and temporary data.

Historical records needed to explain decisions must not be removed by a generic cleanup process.

Retention policies must consider storage growth, source content sensitivity, and the user's ability to understand historical comparisons. Large source payloads may need shorter retention than metadata, fingerprints, or decision history.

## 13. Database integrity and operational checks

The application should expose internal health information sufficient to determine whether the database is usable without revealing sensitive records.

Appropriate checks may include:

- Database open/read/write availability.
- Current schema version.
- Pending or failed migrations.
- Database integrity-check status where scheduled or required.
- Foreign-key constraint violations.
- Incomplete ingestion runs.
- Unpublished or abandoned staging snapshots.
- Checkpoint consistency.
- Available disk space where reliably measurable.

Integrity checks must be scheduled or triggered proportionately. Expensive full-database checks should not run on every ordinary API request.

A health response must distinguish application process health from database readiness.

## 14. Security and privacy

- Store the database in an application-controlled data directory with restrictive filesystem permissions.
- Do not place the database, backups, or secrets inside source repositories by default.
- Apply appropriate permissions to backup and export files.
- Avoid logging SQL parameters or complete records that may contain sensitive data.
- Validate all values before persistence and use parameterized database operations.
- Restrict filesystem paths and prevent user-controlled values from selecting arbitrary database files.
- Define whether database encryption is required based on the threat model and deployment environment; do not assume SQLite provides transparent encryption by default.
- Handle interrupted writes and disk-full conditions without presenting uncommitted records as saved.
- Ensure temporary exports and staging data are cleaned up according to explicit rules.

The security model must address both the primary database and any sidecar files used by the selected SQLite journal mode.

## 15. Testing requirements

Persistence and migration tests must cover:

### 15.1 Repository behavior

- Correct creation, retrieval, updates, and relationship handling.
- Stable identity across application restarts.
- Constraint enforcement.
- Missing-record and conflicting-update behavior.
- Preservation of historical revisions.
- Correct transaction rollback on failure.

### 15.2 Migration behavior

- Fresh database creation from the initial schema.
- Sequential upgrades across supported schema versions.
- Migration failure before completion.
- Retry or recovery after an interrupted migration.
- Detection of modified or inconsistent migration history.
- Data preservation during schema and semantic changes.
- Behavior when the database schema is newer than the application supports.

### 15.3 Ingestion and consistency

- Failed refresh preserves the last-known-good view.
- Partial scans do not replace complete views without an explicit policy.
- Duplicate retries do not create duplicate logical records.
- Checkpoints advance only after safe persistence.
- Staging records cannot be mistaken for published records.
- Analysis runs retain their input snapshot and rule-version references.

### 15.4 Recovery and operations

- Consistent backup during the supported write conditions.
- Restoration from a valid backup.
- Rejection or clear reporting of a corrupt or incompatible backup.
- Disk-full and permission-denied scenarios.
- Database lock contention and bounded retry behavior.
- Integrity and foreign-key checks.
- Application startup against supported and unsupported database versions.

Tests should use isolated temporary databases and representative historical data. Migration tests must validate both schema shape and preserved meaning, not merely confirm that the migration command returns successfully.

## 16. Acceptance criteria

The persistence implementation is ready for its first usable release when:

1. A fresh database can be created from versioned migrations.
2. Application use cases access persistence through defined interfaces.
3. Core entities have stable identities and appropriate relationship constraints.
4. Historical revisions and evidence provenance survive application restarts.
5. Failed ingestion cannot silently replace the last-known-good published view.
6. Source checkpoints and snapshot publication follow explicit transaction rules.
7. Supported schema upgrades are ordered, tested, and recoverable.
8. Migration failures are detectable and do not produce a false success state.
9. A consistent backup can be created and successfully restored.
10. The application rejects unsupported schema versions with an actionable error.
11. Retention does not silently erase records required for historical explanation.
12. Database and backup access follows the approved security policy.
13. Automated tests cover transaction rollback, migrations, ingestion consistency, and recovery.
14. The selected database and migration libraries are documented and pinned according to the project's dependency policy.

## 17. Implementation sequence

### Phase 1 — Persistence foundation

- Select the database access and migration libraries.
- Establish the application data directory and database lifecycle.
- Implement connection configuration, transaction management, and migration tracking.
- Create the initial schema for the minimum first-release entities.
- Add repository and migration tests.

### Phase 2 — Domain persistence

- Persist goals, initiatives, plans, milestones, and decisions.
- Implement revision and archival behavior.
- Enforce identity and relationship constraints.
- Add backup and restore support.

### Phase 3 — Source evidence persistence

- Persist source configurations, ingestion runs, snapshot manifests, normalized records, and evidence.
- Implement staging and atomic publication.
- Add checkpoint recovery and idempotency.
- Verify last-known-good behavior.

### Phase 4 — Analysis and history

- Persist analysis inputs, rule versions, findings, reports, and external analysis provenance.
- Support historical comparison.
- Implement retention rules and storage-growth checks.

### Phase 5 — Upgrade readiness

- Test supported multi-version upgrade paths.
- Validate backup-before-upgrade and restore procedures.
- Test interrupted migrations and incompatible application/database versions.
- Document operational recovery procedures.

This sequence is provisional and should be aligned with the agreed first-release scope.

## 18. Open questions

| ID | Question | Why it matters |
|---|---|---|
| PM-001 | Which Python database access library and migration framework should be selected? | Determines transaction, mapping, and migration implementation. |
| PM-002 | What is the minimum supported database upgrade path? | Determines how many older schema versions must remain upgradeable. |
| PM-003 | Should backup creation be manual, scheduled, or both? | Affects usability, storage, and recovery expectations. |
| PM-004 | Where should the database and backups live on each supported operating system? | Affects portability, permissions, and packaging. |
| PM-005 | Is database encryption at rest required for the first release? | Depends on the threat model and handling of sensitive source material. |
| PM-006 | Which historical source payloads must be retained, and for how long? | Controls storage growth and evidence reproducibility. |
| PM-007 | Should source snapshots use staging tables, versioned record tables, or another publication strategy? | Affects atomic visibility and ingestion scalability. |
| PM-008 | Which records are immutable, revisioned, or safely replaceable? | Determines schema design and audit history. |
| PM-009 | What concurrency model is required for background jobs and future desktop clients? | Affects write coordination and optimistic concurrency. |
| PM-010 | Is portable export/import required for the first usable release? | Influences the data interchange contract and recovery scope. |
| PM-011 | How should the system behave when the database is healthy but a migration is pending or failed? | Determines startup and readiness behavior. |
| PM-012 | What is the expected upper bound for source evidence and snapshot storage? | Helps validate SQLite, indexing, and retention decisions. |

## 19. Relationship to other documents

This document defines persistence behavior and migration safety. It does not replace:

- `domain-model.md` — domain concepts and their relationships.
- `data-model.md` — logical entities and persistence mapping.
- `data-ownership.md` — source authority and ownership boundaries.
- `ingestion-and-snapshots.md` — source scan, snapshot, and publication semantics.
- `deterministic-analysis.md` — reproducibility and analysis behavior.
- `api-design.md` — API contract and request-level behavior.
- `non-functional-requirements.md` — performance, reliability, security, and portability expectations.
- `security-and-privacy.md` — the detailed security and privacy threat model.

Any conflict between this document and an approved domain or ownership decision must be resolved before implementation. Database convenience must not override source authority, provenance, historical integrity, or explicit user decisions.

## 20. Review status

This document is a proposed persistence baseline, not a claim that a database schema or migration framework has already been implemented.

Before implementation, reconcile the proposed storage groups and transaction boundaries with the logical data model, select the database and migration libraries, and resolve the first-release backup, retention, and migration-support requirements.






