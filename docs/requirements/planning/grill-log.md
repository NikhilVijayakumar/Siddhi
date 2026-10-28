# Planning desk review

Desk review only; no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. Recommendations here do not approve planning scope.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input that the documents cannot supply.

## Intent

**Q1. Can an initiative coordinate goals before a repository is created?**
- **Options:** require an existing repository; require at least one goal with evidence; allow a repository-free initiative.
- **Trade-off:** requiring a repository makes planning follow inventory; requiring evidence blocks early intent; repository-free initiatives express intent honestly.
- **Recommendation:** Permit repository-free initiatives linked to multiple outcomes.
- **Why:** Planning should express intended work rather than mirror source inventory.
- **Resolution:** An initiative may exist with no project reference, may link zero or more goals, and may be created before any repository exists.
- **Status:** Recommended
- **Feeds:** FR-003
- **Knowledge:** `knowledge/concepts/portfolio-domain.md`, `knowledge/product/vision.md`

## Scope

**Q2. Which plan fields are essential for the first useful planning slice?**
- **Options:** a full stage-gate model; outcome, milestone, dependency and risk only; free-form notes.
- **Trade-off:** a stage model forces one lifecycle onto different initiative types; free-form notes cannot be compared; the minimal structured set supports review without imposing stages.
- **Recommendation:** Confirm the minimum outcome, milestone, dependency and risk representation before including full planning in a release.
- **Why:** Different initiative types need different stages and detail.
- **Resolution:** Minimum plan: initiative intent, milestones (title, optional target date, status), dependencies (from, to, kind), risks (statement, severity, mitigation optional), and a versioned plan revision. No stages, gates or approval workflow in the first slice.
- **Status:** Recommended
- **Feeds:** FR-031; minimum plan contract
- **Knowledge:** `knowledge/concepts/portfolio-domain.md`, `knowledge/architecture/data-model.md`

## Behaviour

**Q3. Should newly imported advice replace the current approved plan?**
- **Options:** import replaces the plan; import appends a proposal; import is rejected while a plan is approved.
- **Trade-off:** replacement destroys the audit trail; rejection loses advice; a proposal keeps both.
- **Recommendation:** Retain it as a proposal until an explicit revision is approved.
- **Why:** Recommendation arrival is not an owner decision.
- **Resolution:** Imported advice creates a proposed revision. The current approved revision stays effective until the owner approves a new one, and the proposal records which advisory records it cites.
- **Status:** Recommended
- **Feeds:** FR-032, FR-036
- **Knowledge:** `knowledge/architecture/workflow-coordination.md`, `knowledge/concepts/evidence-semantics.md`

## Data

**Q4. Which dependency inconsistencies should block plan revision?**
- **Options:** block every cycle; block nothing; block only self-links and duplicates, report the rest.
- **Trade-off:** blocking every cycle rejects legitimate reciprocal relationships; blocking nothing stores nonsense; a narrow block set plus visible reporting keeps the plan usable.
- **Recommendation:** Preserve unknown targets and conflicts visibly; agree blocking rules by relationship type rather than assume every cycle is invalid.
- **Why:** Uncertain dependencies cannot safely be resolved by invented links.
- **Resolution:** Reject self-dependency and an exact duplicate edge. Report cycles and unknown targets as warnings attached to the revision; never invent a target or delete an edge to resolve them.
- **Status:** Recommended
- **Feeds:** FR-033; dependency validation policy
- **Knowledge:** `knowledge/architecture/data-model.md`, `knowledge/architecture/workflow-coordination.md`

## Integration

**Q5. How should a review use a delayed source refresh?**
- **Options:** wait for a fresh refresh; use the last available data silently; use the captured data and state its limits.
- **Trade-off:** waiting blocks review indefinitely; silent staleness misleads; stating freshness keeps the review honest.
- **Recommendation:** Reference the captured evidence and expose its freshness and coverage limitations.
- **Why:** A stale observation cannot establish current milestone completion.
- **Resolution:** A review cites the snapshot identifiers it used and reports each as current, stale or unavailable. A milestone may not be marked complete from a stale observation.
- **Status:** Recommended
- **Feeds:** FR-034; source-ingestion dependency
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/concepts/evidence-semantics.md`

## Architecture

**Q6. Must review records depend on an automatic weekly scheduler?**
- **Options:** require a scheduler; require manual review only; decouple review meaning from its trigger.
- **Trade-off:** a scheduler couples meaning to infrastructure; manual-only loses cadence; trigger-independent records support both.
- **Recommendation:** Keep review meaning independent of triggering; retain weekly and monthly as initial cadence proposals.
- **Why:** Manual and differently timed reviews must preserve comparable history.
- **Resolution:** A review record stores its own period, trigger (manual or scheduled) and cited evidence. Nothing in the record's semantics depends on a scheduler existing.
- **Status:** Recommended
- **Feeds:** FR-034, FR-035; review trigger design
- **Knowledge:** `knowledge/architecture/workflow-coordination.md`, `knowledge/architecture/persistence.md`

## Acceptance

**Q7. How do we show that internal investments and commercial work receive balanced review?**
- **Options:** revenue-ranked review; equal-weight review; trade-offs shown without automatic precedence.
- **Trade-off:** revenue ranking hides internal value; forced equality ignores real asymmetry; showing trade-offs keeps the judgement with the owner.
- **Recommendation:** Test both with known and missing results, showing trade-offs without automatic precedence.
- **Why:** Neither revenue absence nor internal reuse claims settle strategic value.
- **Resolution:** Fixture: one commercial and one internal initiative, each with one known and one missing result. Expected: both reviews appear, neither outranks the other automatically, and the missing results stay visible as unknown.
- **Status:** Recommended
- **Feeds:** FR-035
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/concepts/portfolio-domain.md`

## Ambiguity

**Q8. What evidence moves an approved action into an implemented state?**
- **Options:** approval implies implementation; any commit implies implementation; action-specific execution evidence.
- **Trade-off:** approval-as-implementation hides non-delivery; any-commit conflates activity with the action; action-specific evidence is precise but needs a mapping.
- **Recommendation:** Agree action-specific execution evidence and retain pending or unknown implementation when absent.
- **Why:** Approval alone proves intent, not execution.
- **Resolution:** Each action names its evidence kind (merged change, published artifact, or owner-attested record). Implemented requires a matching record; otherwise the action stays pending or unknown. Approval never sets implementation.
- **Status:** Recommended
- **Feeds:** FR-036; decision lifecycle contract
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/workflow-coordination.md`
