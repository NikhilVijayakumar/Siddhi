# Change Proposal: Documentation separation

## Why

Siddhi's documentation mixes reusable knowledge, observable requirements, draft designs, and unresolved decisions. Separate these concerns into an independent OKF bundle and traceable draft requirement packages without approving undocumented product behavior or losing source material.

## What Changes

- **tech-01-documentation-separation**: establish independent knowledge, requirement ownership, lossless migration records, and reliable baseline verification.

## Scope and constraints

Documentation/process only. Preserve FR-001–FR-050 and NFR-001–NFR-056.
Retain detailed mixed drafts as non-authoritative historical inputs with old-path
redirects. Extract standalone knowledge and package existing behavioral intent.
Do not implement the application or convert unresolved product drafts into
approved product specifications. Do not invent interview answers.

## Requirement source

The user's instruction to proceed authorizes this documentation migration, not
approval of all pre-existing draft product decisions. Existing baseline documents
and mixed drafts are the inputs; draft packages created here are preparation for
later product changes and interviews.

## Knowledge References

- knowledge/practices/knowledge-and-delivery-separation.md — ownership, drafts, one-way dependencies, and preservation.

## Traceability

- Change ID: openspec-documentation-separation
- Branch: feature/openspec-documentation-separation-migrate-docs
- Roadmap: prerequisite documentation/process work, not a product release.
- Risks: loss of detail, accidental approval, inherited workflow assumptions,
  false-positive requirement validation. Mitigate with archives, draft labels,
  explicit open decisions, baseline ownership, and regression tests.
- Acceptance: 106 IDs uniquely owned, scenario coverage for every FR, independent
  knowledge with valid metadata/indexes, preserved original draft bodies, and
  honest check results.