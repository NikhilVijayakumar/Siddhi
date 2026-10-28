---
type: Runbook
title: Database upgrade and recovery safety
description: Failure triage, consistent recovery points, isolated restore validation, and controlled promotion.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Database upgrade and recovery safety

Use this proposed sequence for migration failure, suspected corruption, or restore.
No backup command, repair utility, migration framework, or automatic recovery is
assumed implemented. Use approved supported mechanisms, never improvised SQL
against the only copy.

# Stop and preserve

1. Confirm authority, instance, and failed operation.
2. Prevent new writers through supported shutdown/maintenance access. Do not race
   migrations with ingestion or ordinary writes.
3. Preserve failed state and safe diagnostics with restricted permissions. Record
   application version, known schema/ledger state, operation ID, journal mode if
   known, and failure category.
4. Preserve the last verified recovery point separately; do not overwrite it with
   an unvalidated backup of the failed store.

Copying only the main SQLite file during WAL writes is not a consistent backup.
Coordinate supported backup or fully understood quiescent capture accounting for
sidecars. Avoid sensitive data in filenames/manifests.

# Classify before retry

Distinguish unavailable path, permissions, disk-full, contention, integrity failure,
unsupported newer schema, failed migration, and interrupted work. Inspect ledger
identity and transactional outcome through supported read-only mechanisms.
A started migration is not necessarily applied.

If rollback was complete and bounded retry is documented, an authorized retry
may be safe. Otherwise follow explicit repair/restore. Do not mark migrations
applied manually or assume older binaries downgrade a database.

# Validate restoration separately

1. Select an identified backup with time, format, checksum if recorded, schema,
   and known validation history.
2. Restore to a new controlled location, leaving the previous store untouched.
3. Check readability, integrity, foreign keys, and schema compatibility.
4. Apply supported migrations to the restored copy with its recovery point safe.
   Stop if history is inconsistent or any step fails.
5. Validate representative owned records, relationships, stable identity, revisions,
   provenance, published snapshots, and analysis input references.
6. Exercise a bounded approved application workflow against the isolated copy.
   File existence or a successful restore invocation is insufficient.
7. Confirm credentials, configuration, and external paths separately; they are not
   presumed part of a database backup.

Restoration does not authorize rescans, source writes, provider submission,
or replay of unfinished consequential operations.

# Promotion and interrupted work

Promote only after validation with writers excluded. Keep the previous database
and safe diagnostics until recovery is confirmed under retention policy. Verify
readiness and core access after promotion.

Reconcile pending jobs against committed publication/checkpoints. Staging is not
a published snapshot. Classify interruption honestly; resume/retry only with
understood side effects and deduplication. Never advance checkpoints beyond
corresponding committed data or replace complete views with unverified capture.

# Completion and escalation

Record recovery point, known data-loss window, methods/results, promotion time,
and limitations. Checksums prove matching bytes, not historical truth. Escalate
unsupported upgrade paths, ambiguous migration state, integrity failure, and
uncertain effects rather than repeatedly modifying the store.

Related: [persistence](../architecture/persistence.md), [diagnostics](diagnostics.md),
[testing](../practices/testing-and-validation.md).