---
name: deterministic-scanner
description: >-
  Guards Siddhi's ingestion pipeline and source adapter code: deterministic extraction, evidence
  and provenance for every value, explicit observation statuses, read-only
  ingestion from untrusted sources. Use whenever source discovery, file
  inventory, an adapter, or metadata resolution is added or changed.
---

# Deterministic Scanner

Sources of truth: `knowledge/architecture/source-adapters.md` (authority,
interface, trust boundary) and `knowledge/concepts/evidence-semantics.md`
(observation, absence, conflict, provenance). This skill is the checklist; the
documents win on any conflict.

## Rules

1. **No inference.** Metadata comes from deterministic rules over recognized
   evidence (manifests, config files, Git metadata). Never call an LLM, never
   guess from prose. A README that mentions "React" is not evidence of a React
   dependency.
2. **Evidence for every value.** Each reported value carries an evidence
   object: `source_type`, `source_ref`, `observed_at`, and `revision` (null when
   unknown). Never fabricate a field you cannot establish.
3. **Missing is not false.** Record the observation outcome the documented
   vocabulary supports (observed, declared, not found in scope, unknown,
   unsupported, inaccessible, stale, conflicting). An empty collection means
   "inspected, none found"; an unassessed field gets an explicit status, never
   an empty list.
4. **Read-only and non-executing.** Never run, import, build, or install
   repository content. No `subprocess` on repository scripts, no `exec`, no
   unpickling, no YAML loaders that construct objects.
5. **Bounded.** Respect configured roots and exclusions; resolve symlinks and
   refuse paths that escape a root; enforce file-size and count limits;
   report hits as `inaccessible` or `unsupported`, not as crashes.
6. **Minimal content.** Store facts and locations, not raw document bodies,
   unless the spec explicitly allows it.
7. **Versioned interpretation.** Changing how an adapter interprets a source
   bumps the recorded normalization version, so stale observations can be
   invalidated.

## Tests every adapter change needs

- Positive: recognized evidence yields the value with correct evidence.
- Absent: no evidence yields the not-found status, not an error.
- Invalid: malformed manifest yields `conflicting`/`unknown` with evidence, and
  ingestion continues.
- Boundary: symlink escaping the root, oversized file, unreadable file.

Use `pytest-skill` for test patterns (`tmp_path` fixture repos), `test-strategy`
for layer placement.

## Output

For a review: list each rule above as pass / fail / not applicable, with
`file:line` for each failure.
