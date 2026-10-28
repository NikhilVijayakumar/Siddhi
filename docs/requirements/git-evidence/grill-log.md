# Git-evidence desk review

Desk review only; no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. No Git provider or verification source has been selected here.

## Intent

**Q1. Can many recent commits establish a delivered outcome?**
- **Recommendation:** Treat activity only as attributable supporting evidence.
- **Why:** Counts and recency do not demonstrate working behavior or business value.
- **Status:** Recommended
- **Feeds:** FR-023

## Scope

**Q2. Which access methods and history window are sufficient initially?**
- **Recommendation:** Confirm existing local versus remote capabilities and a bounded collection window from real repositories.
- **Why:** Full history and every provider are not free or implicit requirements.
- **Status:** Decision needed
- **Feeds:** FR-022; Git access and scope contract

## Behaviour

**Q3. Does absence of a test artifact mean tests failed?**
- **Recommendation:** Report unknown or unavailable verification rather than success or failure.
- **Why:** No observation is not an observed negative result.
- **Status:** Recommended
- **Feeds:** FR-024

## Data

**Q4. How should comparisons survive branch retargeting or shallow history?**
- **Recommendation:** Preserve exact observed revisions and coverage limits; agree reconciliation when prior objects are unavailable.
- **Why:** Mutable branch names cannot reproduce historical comparisons on their own.
- **Status:** Decision needed
- **Feeds:** FR-022; revision-history policy

## Integration

**Q5. Should ordinary refresh check out a branch to obtain evidence?**
- **Recommendation:** Read existing permitted evidence without checkout, commit or publication.
- **Why:** Routine evidence collection must not modify the owner's repository state.
- **Status:** Recommended
- **Feeds:** FR-025

## Architecture

**Q6. Should imported verification results be merged into commit activity totals?**
- **Recommendation:** Keep verification observations separately attributed to source, revision and time.
- **Why:** Activity and executed verification are different evidence kinds.
- **Status:** Recommended
- **Feeds:** FR-023, FR-024

## Acceptance

**Q7. What checks show that collection remains read-only on failure?**
- **Recommendation:** Compare repository contents and checked-out references before and after successful and failed collection.
- **Why:** Failure handling can accidentally introduce checkout or repair side effects.
- **Status:** Recommended
- **Feeds:** FR-025

## Ambiguity

**Q8. Which test, build and release artifact formats should be accepted first?**
- **Recommendation:** Agree supported real formats and their revision applicability instead of inferring success from filenames or tags.
- **Why:** Release records and Git tags do not establish the same fact.
- **Status:** Decision needed
- **Feeds:** FR-024; verification support matrix