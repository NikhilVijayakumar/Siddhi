# OKF-evidence desk review

Desk review only: no interview or user confirmation. The goal-to-evidence report is a recommended first-release goal, NOT an approved release choice. Neither knowledge quality nor profile support is approved here.

## Intent

**Q1. Does a discoverable concept establish usable engineering knowledge?**
- **Recommendation:** Report availability separately from correctness, completeness and applicability.
- **Why:** A readable document can still be wrong or irrelevant.
- **Status:** Recommended
- **Feeds:** FR-019

## Scope

**Q2. Which OKF versions, profiles and extensions should initial inventory support?**
- **Recommendation:** Confirm real package/profile fixtures rather than assuming this bundle represents every source.
- **Why:** Profile-required metadata can differ without violating the underlying format.
- **Status:** Decision needed
- **Feeds:** FR-018; supported-profile contract

## Behaviour

**Q3. Must a knowledge concept have an OpenSpec requirement to be discoverable?**
- **Recommendation:** Discover knowledge independently and permit optional many-to-many relationships.
- **Why:** Knowledge and behavioral obligations have independent purposes.
- **Status:** Recommended
- **Feeds:** FR-020

## Data

**Q4. How should moved concepts and unresolved links retain identity?**
- **Recommendation:** Preserve profile identifiers and source/revision context, and agree reconciliation for path-only identities.
- **Why:** Paths and titles can change without establishing a new concept or a reliable merge.
- **Status:** Decision needed
- **Feeds:** FR-018, FR-019; concept identity policy

## Integration

**Q5. Can a missing metadata field authorize repairing the source knowledge?**
- **Recommendation:** Record profile diagnostics without changing the source.
- **Why:** Read-oriented ingestion does not confer publishing authority.
- **Status:** Recommended
- **Feeds:** FR-021

## Architecture

**Q6. Should declared validation status be stored as a universal truth flag?**
- **Recommendation:** Retain its declared scope, source and available validator/revision context separately from parsing outcome.
- **Why:** A past source declaration is not current universal verification.
- **Status:** Recommended
- **Feeds:** FR-018, FR-019

## Acceptance

**Q7. What proves knowledge and requirements do not require one-to-one mapping?**
- **Recommendation:** Exercise standalone knowledge, standalone requirements and multiple optional links in controlled fixtures.
- **Why:** Linked-only fixtures would hide a mandatory coupling bug.
- **Status:** Recommended
- **Feeds:** FR-020

## Ambiguity

**Q8. When should knowledge be labelled stale rather than merely old?**
- **Recommendation:** Agree source- and question-specific freshness signals and report unknown freshness where insufficient.
- **Why:** Age alone neither disproves a concept nor establishes current applicability.
- **Status:** Decision needed
- **Feeds:** FR-019; knowledge freshness policy