---
name: phase-gate-verification
description: >-
  Verifies a Siddhi roadmap phase is complete: every acceptance criterion
  backed by an executed check, no later-phase dependencies leaked in, and
  unverified items reported explicitly. Use before declaring a phase
  complete, or before tagging a release.
---

# Phase Gate Verification

Sources of truth: `knowledge/product/scope-and-roadmap.md` (capability areas,
proposed dependency-aware sequence, explicit exclusions) and
`docs/requirements/README.md` (recommended delivery order, package ownership of each `FR-nnn` / `NFR-nnn`). Acceptance criteria are the Gherkin scenarios in the owning package's `features/` plus its `requirement.md`; scenarios are drafts, and Gherkin text is not an executed check until a runner exists.

## Procedure

1. **Build the matrix.** One row per acceptance criterion and deliverable of
   the phase: criterion, requirement IDs from the owning package (the README
   ownership table maps each ID to a package; include quality IDs, not only
   functional), the
   check that proves it (test ID, command, or manual step), and its result.
2. **Run the checks.** Execute the test suite and every listed command now.
   A result counts only if it was observed in this run; quote the command
   and the decisive output line.
3. **Classify every row:** `verified`, `failed`, `not run`, `unverifiable`
   (no check exists). Never fold `not run` into `verified`.
4. **Leak check.** The phase must not depend on out-of-scope work. Compare
   imports and dependency manifests against the explicit exclusions in
   `knowledge/product/scope-and-roadmap.md`; list any hit.
5. **Cross-cutting checks.**
   - Security: `code-review-security`, `secrets-scan`, and `sca-audit` run on
     the phase's code; check the security package's quality IDs (NFR-021–027, 039).
   - Open decisions: grill-log items marked "Decision needed" for the phase's
     packages are resolved or explicitly accepted, never assumed.
   - Migrations: the SQLite schema migrates from the previous release and from
     empty (`database-integration-testing`).
   - Failure behavior: inaccessible roots, malformed manifests, locked
     index, and missing credentials produce documented statuses or errors.
   - Documentation: `neat-freak` reconciles `docs/` with what was built.
6. **Verdict.** The phase is complete only when every row is `verified`, or
   each remaining row has an explicit, accepted exception.

## Output

The matrix, the leak-check result, the cross-cutting results, and a one-line
verdict. List `failed`, `not run`, and `unverifiable` rows first.
