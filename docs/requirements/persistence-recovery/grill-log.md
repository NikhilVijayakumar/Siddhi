# Persistence-recovery desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. Backup budgets, transaction units and lifecycle details remain unapproved.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs an owner risk decision that the documents cannot supply.

## Intent

**Q1. Which core capabilities must remain usable without cloud availability?**
- **Options:** full availability only when online; read-only local fallback; full local operation with source limitations visible.
- **Trade-off:** online-only breaks the local-first premise; read-only blocks capture; full local operation with qualified freshness is the stated model.
- **Recommendation:** Keep local record retrieval and deterministic reports usable from available stored inputs, with source limitations visible.
- **Why:** Local-first operation does not guarantee remote freshness but must not require continuous cloud access.
- **Resolution:** The service starts, serves reads, accepts goal and planning writes, and produces reports with only the local database and configuration. Every source-derived field shows its last observation and staleness.
- **Status:** Recommended
- **Feeds:** FR-050, NFR-045
- **Knowledge:** `knowledge/architecture/persistence.md`, `knowledge/decisions/local-first-sqlite.md`

## Scope

**Q2. What recovery-time, data-loss and backup-frequency targets are acceptable?**
- **Options:** no stated targets; a fixed daily backup with 24-hour loss window; targets derived from measured portfolio value.
- **Trade-off:** no targets make recovery unverifiable; a fixed schedule may over- or under-protect; derived targets need a value judgement only the owner can make.
- **Recommendation:** Agree them from portfolio value and workstation risk before prescribing a backup schedule or recovery guarantee.
- **Why:** The baseline explicitly leaves these targets open.
- **Resolution:** Recommended default pending owner input: one backup per day retained for 14 days, recovery point objective 24 hours, recovery time objective one hour, all measured by a restore drill. The owner's acceptance of those numbers is what closes this question.
- **Status:** Decision needed
- **Feeds:** NFR-010, NFR-049, NFR-056; recovery policy
- **Knowledge:** `knowledge/architecture/persistence.md`, `knowledge/runbooks/persistence-recovery.md`

## Behaviour

**Q3. Can a failed operation leave a partially written state?**
- **Options:** leave whatever was written; roll back everything; commit a defined recoverable partial outcome.
- **Trade-off:** leaving state silently corrupts; full rollback is impossible for multi-step jobs that already published; a defined partial outcome is recoverable and visible.
- **Recommendation:** Preserve the prior consistent state or expose a defined recoverable partial outcome; never silently corrupt records.
- **Why:** Attempted processing is not a committed valid state.
- **Resolution:** Single-transaction writes roll back completely. Multi-step jobs commit only at declared units and record each unit; an interrupted job reports the committed units and the stage that failed.
- **Status:** Recommended
- **Feeds:** FR-047, NFR-007
- **Knowledge:** `knowledge/architecture/persistence.md`, `knowledge/architecture/workflow-coordination.md`

## Data

**Q4. Which historical records can be pruned and what budget should trigger review?**
- **Options:** prune anything old; never prune; separate durable records from reproducible caches and set a size review trigger.
- **Trade-off:** blanket pruning destroys decision context; never pruning grows without bound; separation preserves meaning while bounding cost.
- **Recommendation:** Separate durable decisions and plan revisions from reproducible caches, expose growth and agree reference-aware retention before deletion.
- **Why:** Storage inconvenience alone does not justify loss of decision context or reproducibility.
- **Resolution:** Recommended default pending owner input: goals, revisions, decisions, approvals and published snapshots are never pruned; only reproducible parse caches are eligible, and only when no retained report references them. A size threshold triggers owner review rather than automatic deletion.
- **Status:** Decision needed
- **Feeds:** NFR-014, NFR-015, NFR-054, NFR-055; retention policy
- **Knowledge:** `knowledge/architecture/persistence.md`, `knowledge/architecture/data-ownership.md`

## Integration

**Q5. How should machine-local settings and database paths be supplied?**
- **Options:** hardcoded defaults; a committed settings file; environment variables and a machine-local file, validated at startup.
- **Trade-off:** hardcoding blocks portability; a committed file leaks machine paths; validated local configuration is standard and explicit.
- **Recommendation:** Use supported configurable values with startup validation and actionable safe errors, without source-code edits.
- **Why:** Workstation-specific paths and credentials are not portable domain metadata.
- **Resolution:** Database path, bind address and source roots come from environment variables or a machine-local, uncommitted settings file. Startup validates each value and fails with a message naming the setting and not the secret.
- **Status:** Recommended
- **Feeds:** FR-050, NFR-046, NFR-049
- **Knowledge:** `knowledge/architecture/configuration-and-secrets.md`, `knowledge/architecture/data-ownership.md`

## Architecture

**Q6. Should startup apply migrations automatically and resume interrupted work?**
- **Options:** apply silently and resume everything; require a manual migration step; apply versioned migrations at startup, never auto-resume work.
- **Trade-off:** silent resume can repeat consequential work; a manual step blocks routine startup; a controlled startup migration with no auto-resume is safe and usable.
- **Recommendation:** Agree migration and interrupted-job policies; always identify schema version, preserve consistency and report failures or interrupted state.
- **Why:** Silent auto-retry can repeat consequential work or hide failed evolution.
- **Resolution:** Startup checks the recorded schema version, applies forward migrations inside a transaction after a pre-migration backup, and fails closed on error. Interrupted jobs are reported as interrupted and require an explicit new run.
- **Status:** Recommended
- **Feeds:** FR-048, FR-050, NFR-047; startup and migration contract
- **Knowledge:** `knowledge/architecture/persistence.md`, `knowledge/architecture/workflow-coordination.md`

## Acceptance

**Q7. What proves a migration and backup are recoverable rather than merely created?**
- **Options:** assert the migration file exists; assert the new schema version; upgrade a real old schema, inject a failure, and restore a backup into a working database.
- **Trade-off:** existence checks prove nothing; a full drill costs fixture work and proves the actual claim.
- **Recommendation:** Upgrade representative old schemas, inject migration failures and restore consistent backups while checking history and relationships.
- **Why:** Successful file creation is not evidence of a usable recovery path.
- **Resolution:** Three checks: upgrade from the previous schema with history intact; a failing migration leaves the prior schema and data usable; a restored backup passes the same integrity and relationship assertions as the live database.
- **Status:** Recommended
- **Feeds:** FR-048, NFR-010, NFR-037, NFR-056
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/runbooks/persistence-recovery.md`

## Ambiguity

**Q8. Which consumer-visible unit must be atomic when a refresh spans multiple sources?**
- **Options:** the whole refresh; each source snapshot; each project record.
- **Trade-off:** whole-refresh atomicity across independent sources is not achievable; per-project publishes fragments; per-source matches the actual observation unit.
- **Recommendation:** Reconcile the transaction boundary with source-ingestion's publication policy before choosing tables or commit points.
- **Why:** Local transaction safety and external snapshot consistency are different guarantees.
- **Resolution:** Adopt the source-snapshot unit from source-ingestion: one transaction per publication, one usable view per source. Cross-source consistency is never promised; reports name the snapshot each source contributed.
- **Status:** Recommended
- **Feeds:** FR-047, NFR-007; snapshot publication contract
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/architecture/persistence.md`
