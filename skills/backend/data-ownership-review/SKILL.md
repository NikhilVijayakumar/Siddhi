---
name: data-ownership-review
description: >-
  Reviews Siddhi field ownership and data flow: who owns each field, which
  source wins, what stays machine-local, and how ingestion conflicts are handled.
  Use whenever metadata fields, the SQLite schema, source precedence, or
  ingestion pipeline data change.
---

# Data Ownership Review

Source of truth: `knowledge/architecture/data-ownership.md` (authority matrix,
data categories, refresh/absence/conflict, provenance). This skill is the
checklist; the document wins on any conflict. Behavioral intent lives in
`docs/requirements/source-ingestion/` and `docs/requirements/portfolio/`
(FR-001–013, NFR-003–013); field-level policy is still proposed, so record an
unowned field as an open question rather than inventing a policy.

## Checklist

1. **Owner named.** Every new or changed field appears in the authority matrix
   with its owner category: repository-owned, repository-observed,
   Siddhi-generated, portfolio-owned, machine-local, or derived. A field
   missing from the matrix is a documentation gap; update the doc first.
2. **Precedence applied.** Resolution follows the authority matrix: canonical
   profile over observed evidence, observed evidence over generated drafts.
   Generated drafts are never exported as canonical.
3. **Human values preserved.** Portfolio-owned values (tracking level,
   priority, notes) are authoritative. Siddhi caches them and
   never overwrites them from ingestion.
4. **Machine-local stays local.** Source paths, workspace roots, local
   configuration, and credentials are never written to shared logs, exported files,
   or output for remote callers.
5. **Conflicts surfaced.** When two sources disagree, record a `conflicting`
   status with both evidences. Never resolve a conflict by silently choosing
   the last writer.
6. **Derived stays derived.** Related-project matches and obsolete-project
   candidates are review flags; they never change lifecycle status
   automatically.
7. **Provenance kept.** Ingested and cached values keep their source and
   observation time, so a reader can tell a cached copy from an observation.

## Verification

- A test that a machine-local field never appears in an export payload.
- A test that a scan does not overwrite a portfolio-owned value.
- A test that disagreeing sources produce `conflicting`, not one silent winner.

## Output

Per field touched: owner, source of truth, local/shared storage, and pass /
fail against each checklist item.
