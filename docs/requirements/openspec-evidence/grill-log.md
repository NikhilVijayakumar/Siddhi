# OpenSpec-evidence desk review

Desk review only, without interview or user confirmation. Recommended first-release goal: goal-to-evidence report; NOT an approved release choice. No schema coverage is approved by these answers.

## Intent

**Q1. What does a checked OpenSpec task establish?**
- **Recommendation:** Report declared completion, not independently verified implementation.
- **Why:** A source declaration and test evidence answer different questions.
- **Status:** Recommended
- **Feeds:** FR-015

## Scope

**Q2. Which OpenSpec schemas and artifact variants should the initial adapter recognize?**
- **Recommendation:** Confirm versions and representative layouts against real sources before fixing coverage.
- **Why:** Local workflow conventions are not universal upstream guarantees.
- **Status:** Decision needed
- **Feeds:** FR-014; supported-schema matrix

## Behaviour

**Q3. Should absence of an optional artifact always create a gap?**
- **Recommendation:** Only apply missing-evidence rules where the supported schema and assessed scope make the artifact relevant.
- **Why:** Not every repository owes every possible artifact.
- **Status:** Recommended
- **Feeds:** FR-016

## Data

**Q4. How should requirement identity survive file moves and ambiguous titles?**
- **Recommendation:** Preserve native identifiers and revision/location context; agree reconciliation when stable identifiers are absent.
- **Why:** Heading similarity alone can merge unrelated requirements.
- **Status:** Decision needed
- **Feeds:** FR-014; artifact identity contract

## Integration

**Q5. Should parsing fix a malformed task file in place?**
- **Recommendation:** Return diagnostics and leave every authoritative artifact unchanged.
- **Why:** Ingestion is not an authorized authoring workflow.
- **Status:** Recommended
- **Feeds:** FR-017

## Architecture

**Q6. Where should repository-specific completeness rules be selected?**
- **Recommendation:** Bind checks to the detected supported schema and retain rule basis with findings.
- **Why:** A universal workflow assumption produces false incomplete-work findings.
- **Status:** Recommended
- **Feeds:** FR-016; source-ingestion schema boundary

## Acceptance

**Q7. What fixture demonstrates that declared completion is not verification?**
- **Recommendation:** Use a completed task with no test artifact and require separate declaration and unknown-verification reporting.
- **Why:** Happy-path completion counts can conceal false delivery claims.
- **Status:** Recommended
- **Feeds:** FR-015

## Ambiguity

**Q8. Which incomplete workflow states are objectively detectable in the first schema set?**
- **Recommendation:** Agree concrete supported checks and show unsupported status interpretations as unresolved.
- **Why:** A parser cannot infer workflow obligations absent from the source contract.
- **Status:** Decision needed
- **Feeds:** FR-016; initial completeness rules