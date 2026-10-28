---
type: Architecture
title: Persistence and recoverable evolution
description: Repository ports, transaction ownership, historical consistency, schema migration, backup, and restoration.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Persistence and recoverable evolution

A local SQLite store is the proposed initial mechanism. Repository ports keep
application/domain meaning independent of connections, SQL, and ORM sessions.
No physical schema, migration chain, backup facility, or recovery guarantee is
asserted as implemented by this draft.

# Authority and stored meaning

Persist owned goals, plans, decision revisions, assessments, connection metadata,
operation history, snapshots, provenance, analysis inputs, rule versions, and
reports. Capturing external records does not transfer source authority. Prefer
bounded permitted representations, references, and fingerprints to indiscriminate
copies. Ordinary tables do not hold provider secrets or unbounded repository data.

Stable opaque application identity differs from source identity, scoped by source
system and instance. Titles and paths are not durable global identities. Use
primary, foreign-key, uniqueness, and required-value constraints where valid.
Enable and test foreign-key enforcement on every SQLite connection.

Deletion is relationship-specific. Broad cascades must not erase the context of
decisions or analyses. Use revisions, retirement, tombstones, or deliberate
cleanup where history matters. Storage integrity does not prove source truth.

# Transactions and visibility

Application use cases own logical transaction boundaries. A unit of work can
coordinate repositories in one commit; repositories do not invent independent
cross-domain commits. Avoid obscure nested transactions; explicit savepoints
serve a defined partial-rollback need. Keep network calls/scans outside writes.

Capture and normalize externally, stage bounded results, verify declared scope
and completeness, then atomically publish the eligible snapshot and active-view
reference. Advance the matching checkpoint only with safely committed data.
If these cannot share one transaction, design a recoverable protocol that cannot
skip unpublished data. Staging is never implicitly the published view.

A partial/failed scan does not silently replace a complete usable snapshot or
prove absent records were deleted. Choose publication scope explicitly: source,
project, or broader refresh. Durable observations and promoted current state are
different. Atomicity should preserve useful independently completed scopes
without falsely claiming a complete portfolio refresh.

Plan revision creation plus its active pointer, or decision revision plus current
state, are atomic owned changes. Analysis captures exact input snapshots,
portfolio revisions, rule version, and relevant settings. Mixed inputs cannot be
called reproducible without qualification.

# Concurrency and bounded failure

Keep writes short, bound busy-timeout/retry, and report lock contention safely.
Revisions protect concurrent user/background edits. Retries preserve logical
identity rather than duplicating completed actions. Disk-full, permission, and
interrupted-write conditions must not be reported as saved data.

WAL is a candidate after deployment/backup testing, not a cure for SQLite's
single-writer constraint. Protect journal/sidecar files like the main store.
Schedule expensive integrity checks proportionately rather than on every read.

# Ordered migrations and compatibility

Use immutable ordered migration identities with a ledger recording version,
description, successful application time, and checksum or equivalent identity.
Record success only after completion. Correct applied history with a new
migration, not an edited historical body.

Migrations are deterministic local transformations. They do not fetch repositories,
call providers, reconstruct missing facts externally, rewrite user rationale,
or require interaction after beginning. Structural transformation differs from
semantic reinterpretation: preserve original meaning or explicitly version the
transformation and supersession. Do not label transformed values independently
verified facts or silently recalculate away historical analysis.

Before upgrade, inspect schema/ledger, establish exclusive migration access,
check compatibility/integrity, and create a recoverable consistent backup.
Coordinate active writers and backup capture. Apply supported steps in order,
validate schema and representative data, then enable ordinary operations.

Stop on failure and never mark the failed step applied. Use transactional rollback
only where supported; otherwise follow the defined repair/restore procedure.
Reject unsupported newer schemas. Binary downgrade is not database rollback.
Supported upgrade ranges and skipped-release paths need explicit testing.

# Backup, export, and restoration

A backup restores the store; an export transfers selected data. Partial JSON
exports are not full recovery mechanisms. Safe backup metadata identifies format,
creation time, schema/application version, integrity result, and optional checksum.

Use a SQLite-supported consistent backup mechanism. Copying only the main file
while WAL writes are active is not presumed safe. Preserve the last verified
recovery point rather than replacing it with an unvalidated copy.

Restore separately, check integrity/compatibility, apply supported upgrades to
the copy, validate core records, relationships, revisions, and provenance, and
only then promote. Preserve the previous store and safe diagnostics until
confirmed. Restoration does not authorize source writes, automatic rescans,
provider disclosure, or blind replay of unfinished consequential operations.

Database backups do not automatically include repositories, OS secrets, launch
settings, or exported files. File existence or a successful backup call is weaker
evidence than tested restoration. See the [recovery runbook](../runbooks/persistence-recovery.md).

# Retention and open choices

Separate current projections, payload history, provenance, decisions, analysis,
logs, external responses, and staging. Metadata can outlive sensitive payloads,
but explain reproducibility limits. Cleanup respects historical explanation and
explicit deletion obligations, including backup/export copies.

Choose database/migration libraries, upgrade range, publication scope, revision
rules, backup frequency/location/encryption, retention, interchange format,
concurrency bounds, and restart reconciliation. Test rollback, constraints,
checkpoint safety, migration interruption, restoration, contention, permissions,
and storage exhaustion before claiming recoverability.

Related: [API boundary](api-boundary.md), [configuration](configuration-and-secrets.md),
[security](security-and-privacy.md), [observability](observability.md),
[test layers](../practices/testing-and-validation.md).