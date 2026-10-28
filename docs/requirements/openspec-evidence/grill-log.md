# OpenSpec-evidence desk review

Desk review only, without interview or user confirmation. Recommended first-release goal: goal-to-evidence report; NOT an approved release choice. No schema coverage is approved by these answers.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs a real source sample the documents cannot supply.

## Intent

**Q1. What does a checked OpenSpec task establish?**
- **Options:** completed implementation; declared completion only; verified behavior.
- **Trade-off:** treating a checkbox as implementation evidence rewards ticking boxes; declaring nothing loses useful progress signal; reporting declaration separately keeps both honest.
- **Recommendation:** Report declared completion, not independently verified implementation.
- **Why:** A source declaration and test evidence answer different questions.
- **Resolution:** A checked task yields "declared complete" with artifact and revision context. Verification remains a separate evidence kind, and its absence is reported as unknown.
- **Status:** Recommended
- **Feeds:** FR-015
- **Knowledge:** `knowledge/architecture/openspec-integration.md`, `knowledge/concepts/evidence-semantics.md`

## Scope

**Q2. Which OpenSpec schemas and artifact variants should the initial adapter recognize?**
- **Options:** support every schema; support the repository's own schema only; parse artifacts generically without schema knowledge.
- **Trade-off:** broad support without fixtures produces silent misreads; one validated schema limits coverage but is provable; schema-blind parsing cannot apply completeness rules.
- **Recommendation:** Confirm versions and representative layouts against real sources before fixing coverage.
- **Why:** Local workflow conventions are not universal upstream guarantees.
- **Resolution:** Initial support is the `backend` schema in this repository, validated by its own change fixtures. Any other schema or version is reported as unsupported, never interpreted.
- **Status:** Recommended
- **Feeds:** FR-014; supported-schema matrix
- **Knowledge:** `knowledge/architecture/openspec-integration.md`, `knowledge/architecture/source-adapters.md`

## Behaviour

**Q3. Should absence of an optional artifact always create a gap?**
- **Options:** any missing artifact is a gap; only missing required artifacts are gaps; no gap from absence at all.
- **Trade-off:** the first invents obligations; the third hides real gaps; schema-scoped rules match what the source actually requires.
- **Recommendation:** Only apply missing-evidence rules where the supported schema and assessed scope make the artifact relevant.
- **Why:** Not every repository owes every possible artifact.
- **Resolution:** A gap requires a schema rule that names the artifact as required for the assessed change scope, plus a fully observed scope. Otherwise the artifact is reported absent but not deficient.
- **Status:** Recommended
- **Feeds:** FR-016
- **Knowledge:** `knowledge/architecture/openspec-integration.md`, `knowledge/concepts/evidence-semantics.md`

## Data

**Q4. How should requirement identity survive file moves and ambiguous titles?**
- **Options:** identify by path; identify by heading title; identify by native identifier with path as an attribute.
- **Trade-off:** path identity breaks on rename; title identity merges unrelated requirements; native identifiers survive both but may be absent.
- **Recommendation:** Preserve native identifiers and revision/location context; agree reconciliation when stable identifiers are absent.
- **Why:** Heading similarity alone can merge unrelated requirements.
- **Resolution:** Identity is the native FR/NFR or change identifier. Path and title are attributes updated per observation. With no stable identifier and an ambiguous title, the artifact is reported unresolved and is never merged with another.
- **Status:** Recommended
- **Feeds:** FR-014; artifact identity contract
- **Knowledge:** `knowledge/architecture/data-model.md`, `knowledge/architecture/openspec-integration.md`

## Integration

**Q5. Should parsing fix a malformed task file in place?**
- **Options:** rewrite the file to the expected shape; report and leave it; skip it silently.
- **Trade-off:** rewriting crosses source authority; skipping hides actionable diagnostics; reporting keeps both intact.
- **Recommendation:** Return diagnostics and leave every authoritative artifact unchanged.
- **Why:** Ingestion is not an authorized authoring workflow.
- **Resolution:** Malformed artifacts yield diagnostics with location and parse failure, recorded against the snapshot. The file is never written.
- **Status:** Recommended
- **Feeds:** FR-017
- **Knowledge:** `knowledge/architecture/source-adapters.md`, `knowledge/architecture/security-and-privacy.md`

## Architecture

**Q6. Where should repository-specific completeness rules be selected?**
- **Options:** one universal rule set; rules selected by detected schema; rules configured per repository by hand.
- **Trade-off:** a universal set produces false incompleteness; hand configuration drifts unnoticed; schema binding keeps the rule basis explainable.
- **Recommendation:** Bind checks to the detected supported schema and retain rule basis with findings.
- **Why:** A universal workflow assumption produces false incomplete-work findings.
- **Resolution:** Each finding records the rule identifier and the schema version it came from. An unsupported schema yields no completeness findings at all.
- **Status:** Recommended
- **Feeds:** FR-016; source-ingestion schema boundary
- **Knowledge:** `knowledge/architecture/openspec-integration.md`, `knowledge/architecture/deterministic-analysis.md`

## Acceptance

**Q7. What fixture demonstrates that declared completion is not verification?**
- **Options:** a fully complete change; a checked task with no test evidence; a change with only unapproved specs.
- **Trade-off:** a complete change hides the distinction; the missing-evidence case makes it observable in one field.
- **Recommendation:** Use a completed task with no test artifact and require separate declaration and unknown-verification reporting.
- **Why:** Happy-path completion counts can conceal false delivery claims.
- **Resolution:** The fixture has one checked task, its artifact present, and no test or verification record. Expected: completion declared, verification unknown, no gap attributed to verification.
- **Status:** Recommended
- **Feeds:** FR-015
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/concepts/evidence-semantics.md`

## Ambiguity

**Q8. Which incomplete workflow states are objectively detectable in the first schema set?**
- **Options:** infer every workflow obligation; detect only what the schema declares; detect nothing until a full workflow model exists.
- **Trade-off:** inference invents obligations; detecting nothing makes the adapter useless; schema-declared checks are provable.
- **Recommendation:** Agree concrete supported checks and show unsupported status interpretations as unresolved.
- **Why:** A parser cannot infer workflow obligations absent from the source contract.
- **Resolution:** Initial checks: an unchecked task in an otherwise complete change; an artifact missing while its schema marks it required; a change with no validation evidence attributed to its tasks. Every other state is reported as unresolved rather than guessed.
- **Status:** Recommended
- **Feeds:** FR-016; initial completeness rules
- **Knowledge:** `knowledge/architecture/openspec-integration.md`, `knowledge/concepts/evidence-semantics.md`
