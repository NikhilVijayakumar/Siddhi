# Portfolio desk review

Desk review only: no interview or user confirmation occurred. Answers below are recommendations, not settled decisions. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input that the documents cannot supply, and the block names that input.

## Intent

**Q1. Can an owner capture an outcome before selecting a project?**
- **Options:** require a discovered project; require an initiative; allow the goal alone.
- **Trade-off:** requiring a project makes the portfolio mirror inventory; allowing the goal alone costs an unlinked record that may never acquire evidence.
- **Recommendation:** Keep repository association optional at goal creation.
- **Why:** Exploration must not be forced into the current inventory.
- **Resolution:** Adopt a goal-only creation path. Goal identity, revision and archival are complete with zero project references; an unlinked goal is a normal state, not a defect.
- **Status:** Recommended
- **Feeds:** FR-001, FR-002
- **Knowledge:** `knowledge/concepts/portfolio-domain.md`, `knowledge/architecture/data-ownership.md`

## Scope

**Q2. Should the initial portfolio workflow collect hours to estimate progress?**
- **Options:** collect hours per goal; derive progress from activity; record no effort data.
- **Trade-off:** hours give a familiar number but turn the product into time accounting; no effort data leaves progress explicitly qualitative.
- **Recommendation:** Do not require hours; show the limits of available execution evidence.
- **Why:** Activity accounting is not the stated outcome model.
- **Resolution:** No effort or hours field in the first slice. Where execution evidence is absent, the goal reports "not assessed", never zero progress.
- **Status:** Recommended
- **Feeds:** FR-037
- **Knowledge:** `knowledge/product/vision.md`, `knowledge/concepts/evidence-semantics.md`

## Behaviour

**Q3. What turns an inferred project association into a strategic commitment?**
- **Options:** associate automatically on a match; keep a candidate until the owner confirms; never associate automatically.
- **Trade-off:** automatic association inflates strategy with guesses; never associating hides useful evidence; confirmation costs one review action per relationship.
- **Recommendation:** Require an explicit owner confirmation with its evidence and rationale where supplied.
- **Why:** A plausible match must not silently change strategy.
- **Resolution:** Two states only: candidate (with basis and confidence) and committed (owner confirmation, time, optional reason). Analysis can only create candidates; no other transition is permitted.
- **Status:** Recommended
- **Feeds:** FR-004; association approval contract
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/data-ownership.md`

## Data

**Q4. Which goal fields and priority scale are mandatory at creation?**
- **Options:** a rich mandatory form; a minimal identity set with explicit unknowns; free-form text only.
- **Trade-off:** a rich form blocks capture and invites invented dates; free-form text cannot be compared; a minimal set needs explicit unknown states.
- **Recommendation:** Agree a small mandatory identity/outcome set and leave unprovided constraints unknown; confirm the priority representation separately.
- **Why:** Invented dates or budgets distort later comparisons.
- **Resolution:** Mandatory: title, outcome type (software, creative, research, internal investment, other), status. Recorded as explicit unknown when not supplied: description, rationale, success criteria, priority (`low`, `normal`, `high`, `critical` plus note; no numeric score), target or review date, constraints, assumptions, risks.
- **Status:** Recommended
- **Feeds:** FR-001, FR-005; creation contract
- **Knowledge:** `knowledge/architecture/data-model.md`, `knowledge/concepts/portfolio-domain.md`

## Integration

**Q5. Should a renamed Vyasa project create a new portfolio relationship?**
- **Options:** match on display name; match on the source identifier; ask the owner each time the name changes.
- **Trade-off:** name matching silently splits or merges projects; identifier matching survives renames but shows the old name until re-observed.
- **Recommendation:** Preserve the source identity mapping and expose ambiguity when identity cannot be established.
- **Why:** Display names do not safely identify projects.
- **Resolution:** The source identifier is the only identity key. A rename is a new observation of the same identity; a missing or ambiguous identifier yields an unresolved reference, never a new relationship.
- **Status:** Recommended
- **Feeds:** FR-004; source-ingestion dependency
- **Knowledge:** `knowledge/architecture/data-ownership.md`, `knowledge/architecture/source-adapters.md`

## Architecture

**Q6. Where should a goal's revision rationale live?**
- **Options:** in the source repository; in the portfolio record; in the analysis report.
- **Trade-off:** writing to a repository crosses source authority; keeping rationale only in a report loses it when the report is deleted; portfolio revision history keeps it with the record.
- **Recommendation:** Retain it with portfolio-owned revision history rather than writing it into source repositories.
- **Why:** Portfolio authority is independent of engineering source authority.
- **Resolution:** Every goal change appends a revision (prior state, changed fields, time, actor, supplied reason). Nothing is ever written back to Vyasa, OpenSpec, OKF or Git.
- **Status:** Recommended
- **Feeds:** FR-006; persistence-recovery dependency
- **Knowledge:** `knowledge/architecture/data-model.md`, `knowledge/architecture/persistence.md`

## Acceptance

**Q7. How can heterogeneous outcomes demonstrate that no universal lifecycle is imposed?**
- **Options:** one software fixture; one fixture per outcome type; a publication plus an internal engineering goal.
- **Trade-off:** software-only fixtures hide lifecycle coupling; a full matrix is expensive; two dissimilar outcomes catch the coupling at low cost.
- **Recommendation:** Exercise a publication and an internal engineering goal with different success criteria and no time entries.
- **Why:** Software-only fixtures would miss lifecycle coupling.
- **Resolution:** The acceptance fixture pair is a publication goal (acceptance by external publication) and an internal investment goal (acceptance by reuse or capability). Both must complete the same workflow without a shared stage model and without time entries.
- **Status:** Recommended
- **Feeds:** FR-002, FR-037
- **Knowledge:** `knowledge/concepts/portfolio-domain.md`, `knowledge/product/vision.md`

## Ambiguity

**Q8. Who confirms achievement when evidence supports only part of a goal?**
- **Options:** automatic achievement from evidence; owner judgement alone; separate evidence assessment and owner confirmation.
- **Trade-off:** automatic achievement overclaims; owner judgement without evidence is unauditable; separation costs one explicit record.
- **Recommendation:** Keep evidence assessment separate from owner-confirmed achievement and agree the confirmation policy before implementation.
- **Why:** A relationship or partial test result does not prove the intended outcome.
- **Resolution:** Analysis may report evidence as supporting, contradicting, partial or unavailable for a named criterion. Only an owner-recorded achievement decision closes the goal, and it cites whichever evidence the owner relied on.
- **Status:** Recommended
- **Feeds:** FR-001, FR-004; achievement policy
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/practices/knowledge-and-delivery-separation.md`
