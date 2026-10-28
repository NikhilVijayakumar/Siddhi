# Persistence-recovery desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. Backup budgets, transaction units and lifecycle details remain unapproved.

## Intent

**Q1. Which core capabilities must remain usable without cloud availability?**
- **Recommendation:** Keep local record retrieval and deterministic reports usable from available stored inputs, with source limitations visible.
- **Why:** Local-first operation does not guarantee remote freshness but must not require continuous cloud access.
- **Status:** Recommended
- **Feeds:** FR-050, NFR-045

## Scope

**Q2. What recovery-time, data-loss and backup-frequency targets are acceptable?**
- **Recommendation:** Agree them from portfolio value and workstation risk before prescribing a backup schedule or recovery guarantee.
- **Why:** The baseline explicitly leaves these targets open.
- **Status:** Decision needed
- **Feeds:** NFR-010, NFR-049, NFR-056; recovery policy

## Behaviour

**Q3. What should happen when a logically grouped write fails halfway through?**
- **Recommendation:** Preserve the prior consistent state or expose a defined recoverable partial outcome; never silently corrupt records.
- **Why:** Attempted processing is not a committed valid state.
- **Status:** Recommended
- **Feeds:** FR-047, NFR-007

## Data

**Q4. Which historical records can be pruned and what budget should trigger review?**
- **Recommendation:** Separate durable decisions and plan revisions from reproducible caches, expose growth and agree reference-aware retention before deletion.
- **Why:** Storage inconvenience alone does not justify loss of decision context or reproducibility.
- **Status:** Decision needed
- **Feeds:** NFR-014, NFR-015, NFR-054, NFR-055; retention policy

## Integration

**Q5. How should machine-local settings and database paths be supplied?**
- **Recommendation:** Use supported configurable values with startup validation and actionable safe errors, without source-code edits.
- **Why:** Workstation-specific paths and credentials are not portable domain metadata.
- **Status:** Recommended
- **Feeds:** FR-050, NFR-046, NFR-049

## Architecture

**Q6. Should startup apply migrations automatically and resume interrupted work?**
- **Recommendation:** Agree migration and interrupted-job policies; always identify schema version, preserve consistency and report failures or interrupted state.
- **Why:** Silent auto-retry can repeat consequential work or hide failed evolution.
- **Status:** Decision needed
- **Feeds:** FR-048, FR-050, NFR-047; startup and migration contract

## Acceptance

**Q7. What proves a migration and backup are recoverable rather than merely created?**
- **Recommendation:** Upgrade representative old schemas, inject migration failures and restore consistent backups while checking history and relationships.
- **Why:** Successful file creation is not evidence of a usable recovery path.
- **Status:** Recommended
- **Feeds:** FR-048, NFR-010, NFR-037, NFR-056

## Ambiguity

**Q8. Which consumer-visible unit must be atomic when a refresh spans multiple sources?**
- **Recommendation:** Reconcile the transaction boundary with source-ingestion's publication policy before choosing tables or commit points.
- **Why:** Local transaction safety and external snapshot consistency are different guarantees.
- **Status:** Decision needed
- **Feeds:** FR-047, NFR-007; snapshot publication contract