# Requirement packages

**Status: draft for review. Not approved for implementation.**

The [functional baseline](functional-requirements.md) retains FR-001–FR-050 and
the [quality baseline](non-functional-requirements.md) retains NFR-001–NFR-056.
Each identifier has exactly one owning package below. A cross-cutting quality
owner coordinates a constraint; other packages must still apply it where relevant.
Ownership does not postpone security, integrity, or testing to a final phase.

Packages refine the baselines without duplicating their full text. Their current
acceptance scenarios are representative drafts, not exhaustive coverage of every
compound obligation. Preserved supporting drafts contain details that still need
reconciliation during product-change design.

## Package ownership

| Package | Functional IDs | Quality IDs |
|---|---|---|
| [Portfolio](portfolio/requirement.md) | 001, 002, 004–006, 037 | — |
| [Planning and reviews](planning/requirement.md) | 003, 031–036 | — |
| [Source ingestion](source-ingestion/requirement.md) | 007–013 | 003, 005, 006, 008, 009, 011–013, 016, 029, 031 |
| [OpenSpec evidence](openspec-evidence/requirement.md) | 014–017 | — |
| [OKF evidence](okf-evidence/requirement.md) | 018–021 | — |
| [Git and verification evidence](git-evidence/requirement.md) | 022–025 | — |
| [Deterministic analysis](analysis/requirement.md) | 026–030 | 017, 018, 020 |
| [External analysis](external-analysis/requirement.md) | 038–042 | 019, 024 |
| [API operations](api-operations/requirement.md) | 043–046 | 001, 002, 030, 040–044, 048, 050–053 |
| [Persistence and recovery](persistence-recovery/requirement.md) | 047, 048, 050 | 007, 010, 014, 015, 037, 045–047, 049, 054–056 |
| [Security](security/requirement.md) | 049 | 021–023, 025–027, 039 |
| [Engineering quality](engineering-quality/requirement.md) | — | 004, 028, 032–036, 038 |

The package Owns lines enumerate the complete IDs for machine checks. Each
package has a requirement document, diagram, eight-dimension grill log, and
Gherkin feature documents. **These logs are desk reviews, not stakeholder
interviews.** Recommended answers are not user decisions; unresolved choices
are explicitly marked Decision needed. No approval or interview is fabricated.

A deep review on 2026-10-29 recorded the options, trade-off and resolution for
all 96 questions. 88 now carry a recommendation that a draft specification may
adopt; 8 remain Decision needed because they need owner input the documents
cannot supply (listed under [known decisions](#historical-detail-and-known-decisions)).
A recommendation is still not an approval.

## Recommended delivery order

1. Establish safe local persistence/access and create an independent goal.
2. Verify the actual Vyasa contract and capture project inventory.
3. Add independently ingestible OpenSpec, OKF, and bounded Git evidence.
4. Link a goal to evidence and generate an explained deterministic report.
5. Add historical comparison, planning/reviews, and external-analysis handoff
   when selected for the release.

This is a recommendation, not an approved release scope. Packages intentionally
group related draft intent; each later change selects a smaller end-to-end
vertical slice rather than implementing a whole adapter or horizontal layer.

## Conversion to OpenSpec

1. Apply knowledge-first. Reuse/update relevant [OKF concepts](../../knowledge/index.md)
   before writing new delivery artifacts.
2. Conduct a real grill-me review one question at a time; record actual answers,
   rationale, and unresolved accepted decisions in the owning package.
3. Resolve baseline conflicts, supported source formats, contracts, and acceptance
   boundaries for the selected slice. Do not infer approval from a validator pass.
4. Create a be-prefixed product change. Follow the authoritative
   [schema](../../openspec/schemas/backend/schema.yaml): proposal → specs →
   api-contract → design → ADR disposition → tasks → implementation/verification.
5. Trace each specification requirement/scenario to the package and stable FR/NFR
   identifiers. Cite knowledge inline in delta requirement text; do not make
   knowledge link back. Do not renumber or delete the original requirement source.
6. Define actual executable tests and run them. Gherkin documents alone have no
   runner or step definitions and prove no implementation behavior.

Two change drafts exist: the documentation-process change and
`be-01-goal-and-persistence` (independent goal on a versioned local database,
delivery step 1). Both are drafts. No unresolved product package has been
converted into an approved product specification.

## Historical detail and known decisions

- [Migration report](../documentation-migration.md) — source maps, preservation,
  gaps, and verification evidence.
- [Retained inputs](_source/README.md) — mixed drafts, explicitly non-authoritative.
- Each package's grill log records package-specific unresolved decisions.
- The 8 remaining owner decisions: the real Vyasa interface/version
  (source-ingestion Q2), accepted verification artifact formats (git-evidence Q8),
  what may leave the machine in a brief and to whom (external-analysis Q5),
  pre-1.0 compatibility plus benchmark targets (api-operations Q8), recovery
  targets (persistence-recovery Q2), retention policy (persistence-recovery Q4),
  local client authentication and origin policy (security Q5), and the reference
  workstation/workload (engineering-quality Q2).

## Knowledge References

- `knowledge/practices/knowledge-and-delivery-separation.md` — ownership, draft status, and safe conversion.
- `knowledge/practices/vertical-slices.md` — small observable delivery units.
- `knowledge/practices/testing-and-validation.md` — acceptance versus executed evidence.