---
name: data-ownership-review
description: >-
  Reviews Siddhi field ownership and data flow: who owns each field, which
  source wins, what stays machine-local, and how ingestion conflicts are handled.
  Use whenever metadata fields, the SQLite schema, source precedence, or
  ingestion pipeline data change.
---

# Data Ownership Review

Source of truth: `docs/requirements/data-ownership.md` (ownership categories
§3, sources of truth §4, field matrix §5, precedence §6). This skill is the
checklist; the document wins on any conflict.

## Checklist

1. **Owner named.** Every new or changed field appears in the field-level
   ownership matrix (§5) with its owner category: repository-owned,
   repository-observed, Siddhi-generated, portfolio-owned, provider-owned,
   machine-local, or derived. A field missing from the matrix is a
   documentation gap; update the doc first.
2. **Precedence applied.** Resolution follows §6: canonical profile over
   detected evidence, detected evidence over generated drafts. Generated
   drafts are never exported as canonical.
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
7. **Provenance kept.** Synced and provider values keep their source and
   timestamp, so a reader can tell a cached copy from an observation.

## Verification

- A test that a machine-local field never appears in the sync payload.
- A test that a scan does not overwrite a portfolio-owned value.
- A test that disagreeing sources produce `conflicting`, not one silent winner.

## Output

Per field touched: owner, source of truth, local/shared storage, and pass /
fail against each checklist item.
