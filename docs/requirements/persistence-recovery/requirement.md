# Consistent local persistence and recovery

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-047, FR-048, FR-050, NFR-007, NFR-010, NFR-014, NFR-015, NFR-037, NFR-045, NFR-046, NFR-047, NFR-049, NFR-054, NFR-055, NFR-056

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-047](../functional-requirements.md#fr-047--preserve-data-integrity) | Logical operations use integrity checks and appropriate transactions so failures do not silently corrupt owned records or snapshots. |
| [FR-048](../functional-requirements.md#fr-048--support-database-evolution) | Apply controlled migrations, identify schema version and explicitly report migration failures. |
| [FR-050](../functional-requirements.md#fr-050--support-reliable-local-operation) | Operate the local backend with documented configuration, lifecycle, database location, diagnostics and recovery before desktop packaging. |

## Out of scope

Distributed database requirements, guaranteed zero data loss or fixed recovery time without agreement, automatic history deletion, untested downgrade guarantees, and treating a naive live-file copy as a proven backup.

## Data and integration boundaries

SQLite holds portfolio-owned revisions, normalized source projections, snapshots, findings, plans, reviews and operational history with valid relationships. Configuration and secret references remain machine-local where appropriate. Persistence controls publication consistency, not atomicity of independent external sources. No exact table schema, migration library or database filename is settled here.

## NFR responsibilities

| Owned baseline | Responsibility |
|---|---|
| [NFR-007](../non-functional-requirements.md#nfr-007--consistent-persistence) | Prior consistent state or explicitly recoverable partial outcome on logical operation failure. |
| [NFR-010](../non-functional-requirements.md#nfr-010--recovery) | Document and test SQLite/configuration recovery including migration context; time/loss targets remain open. |
| [NFR-014](../non-functional-requirements.md#nfr-014--historical-preservation) | Preserve sufficient evidence, plan, report and decision history under an explicit retention policy. |
| [NFR-015](../non-functional-requirements.md#nfr-015--referential-integrity) | Archival, removal and renaming leave no silent misleading references. |
| [NFR-037](../non-functional-requirements.md#nfr-037--migration-validation) | Test upgrades and safe failures from representative prior schemas. |
| [NFR-045](../non-functional-requirements.md#nfr-045--local-first-operation) | Core retrieval, deterministic analysis and reports work locally from stored inputs without continuous cloud access. |
| [NFR-046](../non-functional-requirements.md#nfr-046--environment-configuration) | Validate environment settings at startup with actionable errors, without source changes. |
| [NFR-047](../non-functional-requirements.md#nfr-047--predictable-lifecycle) | Manage startup, shutdown, jobs and database state predictably; report interrupted work. |
| [NFR-049](../non-functional-requirements.md#nfr-049--database-location-and-backup) | Explicit configurable database location and documented migration/backup management. |
| [NFR-054](../non-functional-requirements.md#nfr-054--bounded-storage-growth) | Expose growth and retained-artifact cost sufficient to apply an agreed policy. |
| [NFR-055](../non-functional-requirements.md#nfr-055--historical-record-policy) | Distinguish durable decisions/plan versions from reconstructible caches; no convenience-driven deletion. |
| [NFR-056](../non-functional-requirements.md#nfr-056--backup-consistency) | Produce consistent backups and documented restores accounting for SQLite transactions/journaling. |

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md): capture and publication boundaries, last-known-good state.
- [portfolio](../portfolio/requirement.md), [planning](../planning/requirement.md), [analysis](../analysis/requirement.md): revision/history consumers and retention constraints.
- [api-operations](../api-operations/requirement.md): observable lifecycle and actionable errors.
- [security](../security/requirement.md): configuration permissions, secrets and retained-content privacy.
- [engineering-quality](../engineering-quality/requirement.md): migration, transaction and interruption fixtures.

## Unresolved questions

Transaction/publication unit, migration mechanism, startup migration policy, database defaults, backup destination/frequency, recovery targets, interrupted-job handling and retention budgets require agreement. Recommended first release: goal-to-evidence report, NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. Recovery and migration scenarios require actual earlier-schema fixtures and restore drills before executable evidence exists.

## Knowledge References

- `knowledge/architecture/persistence.md` — transactions, evolution and backups.
- `knowledge/architecture/configuration-and-secrets.md` — local settings and validation.
- `knowledge/architecture/data-model.md` — logical history and relationship invariants.
- `knowledge/architecture/data-ownership.md` — durable versus reconstructible records.
- `knowledge/architecture/workflow-coordination.md` — interrupted work and lifecycle.
- `knowledge/practices/testing-and-validation.md` — migration and recovery drills.
- `knowledge/practices/knowledge-and-delivery-separation.md` — targets are not approvals.