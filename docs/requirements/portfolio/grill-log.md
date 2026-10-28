# Portfolio desk review

Desk review only: no interview or user confirmation occurred. Answers below are recommendations, not settled decisions. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice.

## Intent

**Q1. Can an owner capture an outcome before selecting a project?**
- **Recommendation:** Keep repository association optional at goal creation.
- **Why:** Exploration must not be forced into the current inventory.
- **Status:** Recommended
- **Feeds:** FR-001, FR-002

## Scope

**Q2. Should the initial portfolio workflow collect hours to estimate progress?**
- **Recommendation:** Do not require hours; show the limits of available execution evidence.
- **Why:** Activity accounting is not the stated outcome model.
- **Status:** Recommended
- **Feeds:** FR-037

## Behaviour

**Q3. What turns an inferred project association into a strategic commitment?**
- **Recommendation:** Require an explicit owner confirmation with its evidence and rationale where supplied.
- **Why:** A plausible match must not silently change strategy.
- **Status:** Decision needed
- **Feeds:** FR-004; association approval contract

## Data

**Q4. Which goal fields and priority scale are mandatory at creation?**
- **Recommendation:** Agree a small mandatory identity/outcome set and leave unprovided constraints unknown; confirm the priority representation separately.
- **Why:** Invented dates or budgets distort later comparisons.
- **Status:** Decision needed
- **Feeds:** FR-001, FR-005; creation contract

## Integration

**Q5. Should a renamed Vyasa project create a new portfolio relationship?**
- **Recommendation:** Preserve the source identity mapping and expose ambiguity when identity cannot be established.
- **Why:** Display names do not safely identify projects.
- **Status:** Recommended
- **Feeds:** FR-004; source-ingestion dependency

## Architecture

**Q6. Where should a goal's revision rationale live?**
- **Recommendation:** Retain it with portfolio-owned revision history rather than writing it into source repositories.
- **Why:** Portfolio authority is independent of engineering source authority.
- **Status:** Recommended
- **Feeds:** FR-006; persistence-recovery dependency

## Acceptance

**Q7. How can heterogeneous outcomes demonstrate that no universal lifecycle is imposed?**
- **Recommendation:** Exercise a publication and an internal engineering goal with different success criteria and no time entries.
- **Why:** Software-only fixtures would miss lifecycle coupling.
- **Status:** Recommended
- **Feeds:** FR-002, FR-037

## Ambiguity

**Q8. Who confirms achievement when evidence supports only part of a goal?**
- **Recommendation:** Keep evidence assessment separate from owner-confirmed achievement and agree the confirmation policy before implementation.
- **Why:** A relationship or partial test result does not prove the intended outcome.
- **Status:** Decision needed
- **Feeds:** FR-001, FR-004; achievement policy