# Analysis desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report; NOT an approved release choice. Classification and rule proposals remain subject to review.

## Intent

**Q1. Should routine goal comparison depend on external AI availability?**
- **Recommendation:** Use defined deterministic rules over recorded inputs without requiring an AI service.
- **Why:** Reproducible baseline analysis must remain available locally.
- **Status:** Recommended
- **Feeds:** FR-026, FR-029, NFR-017

## Scope

**Q2. Which initial rules can establish a confirmed relationship or identified gap?**
- **Recommendation:** Agree criterion-specific sufficient evidence and a small explicit rule library; keep keyword similarity only a candidate signal.
- **Why:** Relevance alone does not establish a relationship or prove absence.
- **Status:** Decision needed
- **Feeds:** FR-026, FR-027; initial rule and sufficiency policy

## Behaviour

**Q3. Should an inaccessible repository produce a negative capability finding?**
- **Recommendation:** Report missing or stale/unavailable evidence with its scope instead of a demonstrable gap.
- **Why:** Unknown evidence cannot establish falsehood.
- **Status:** Recommended
- **Feeds:** FR-027, FR-028

## Data

**Q4. Which input and time context must be frozen for reproduction?**
- **Recommendation:** Record relevant portfolio revisions, snapshots, rule/configuration versions and applicable reference time before evaluating rules.
- **Why:** Hidden current state changes would make identical-input claims misleading.
- **Status:** Recommended
- **Feeds:** FR-029, NFR-017, NFR-018

## Integration

**Q5. How should conflicting declarations and verification evidence be resolved?**
- **Recommendation:** Retain both with authority and revision context; agree claim-specific resolution rules rather than latest-source-wins.
- **Why:** Sources can describe different scopes or disagree legitimately.
- **Status:** Decision needed
- **Feeds:** FR-027, FR-028; conflict handling contract

## Architecture

**Q6. Can a historical report silently read today's evidence during rendering?**
- **Recommendation:** Render retained report context and explicitly qualify unavailable reproduction inputs.
- **Why:** A historical result must not change meaning on retrieval.
- **Status:** Recommended
- **Feeds:** FR-029, FR-030, NFR-018, NFR-020

## Acceptance

**Q7. What should the fixed-input reproducibility assertion compare?**
- **Recommendation:** Compare equivalent logical findings while allowing different generation times and run identities.
- **Why:** Operational metadata differs without changing analytical conclusions.
- **Status:** Recommended
- **Feeds:** FR-029, NFR-017

## Ambiguity

**Q8. Are finding categories exclusive, and how should rule-only changes be displayed?**
- **Recommendation:** Confirm the final vocabulary and comparison presentation; preserve separate freshness and uncertainty qualifications and explicit rule-change attribution.
- **Why:** A candidate can also be stale, and changed interpretation is not changed source evidence.
- **Status:** Decision needed
- **Feeds:** FR-027, FR-030, NFR-020; finding and comparison contract