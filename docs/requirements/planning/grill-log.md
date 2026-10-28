# Planning desk review

Desk review only; no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. Recommendations here do not approve planning scope.

## Intent

**Q1. Can an initiative coordinate goals before a repository is created?**
- **Recommendation:** Permit repository-free initiatives linked to multiple outcomes.
- **Why:** Planning should express intended work rather than mirror source inventory.
- **Status:** Recommended
- **Feeds:** FR-003

## Scope

**Q2. Which plan fields are essential for the first useful planning slice?**
- **Recommendation:** Confirm the minimum outcome, milestone, dependency and risk representation before including full planning in a release.
- **Why:** Different initiative types need different stages and detail.
- **Status:** Decision needed
- **Feeds:** FR-031; minimum plan contract

## Behaviour

**Q3. Should newly imported advice replace the current approved plan?**
- **Recommendation:** Retain it as a proposal until an explicit revision is approved.
- **Why:** Recommendation arrival is not an owner decision.
- **Status:** Recommended
- **Feeds:** FR-032, FR-036

## Data

**Q4. Which dependency inconsistencies should block plan revision?**
- **Recommendation:** Preserve unknown targets and conflicts visibly; agree blocking rules by relationship type rather than assume every cycle is invalid.
- **Why:** Uncertain dependencies cannot safely be resolved by invented links.
- **Status:** Decision needed
- **Feeds:** FR-033; dependency validation policy

## Integration

**Q5. How should a review use a delayed source refresh?**
- **Recommendation:** Reference the captured evidence and expose its freshness and coverage limitations.
- **Why:** A stale observation cannot establish current milestone completion.
- **Status:** Recommended
- **Feeds:** FR-034; source-ingestion dependency

## Architecture

**Q6. Must review records depend on an automatic weekly scheduler?**
- **Recommendation:** Keep review meaning independent of triggering; retain weekly and monthly as initial cadence proposals.
- **Why:** Manual and differently timed reviews must preserve comparable history.
- **Status:** Recommended
- **Feeds:** FR-034, FR-035; review trigger design

## Acceptance

**Q7. How do we show that internal investments and commercial work receive balanced review?**
- **Recommendation:** Test both with known and missing results, showing trade-offs without automatic precedence.
- **Why:** Neither revenue absence nor internal reuse claims settle strategic value.
- **Status:** Recommended
- **Feeds:** FR-035

## Ambiguity

**Q8. What evidence moves an approved action into an implemented state?**
- **Recommendation:** Agree action-specific execution evidence and retain pending or unknown implementation when absent.
- **Why:** Approval alone proves intent, not execution.
- **Status:** Decision needed
- **Feeds:** FR-036; decision lifecycle contract