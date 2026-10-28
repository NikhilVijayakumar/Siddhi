# Analysis desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report; NOT an approved release choice. Classification and rule proposals remain subject to review.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input that the documents cannot supply.

## Intent

**Q1. Should routine goal comparison depend on external AI availability?**
- **Options:** require an AI service; deterministic rules only; AI with a deterministic fallback.
- **Trade-off:** an AI dependency breaks offline reproducibility; deterministic-only limits nuance; a fallback duplicates two rule systems.
- **Recommendation:** Use defined deterministic rules over recorded inputs without requiring an AI service.
- **Why:** Reproducible baseline analysis must remain available locally.
- **Resolution:** The analysis engine is deterministic and rules are versioned. External advice enters only through the separate advisory import path and never changes a deterministic finding.
- **Status:** Recommended
- **Feeds:** FR-026, FR-029, NFR-017
- **Knowledge:** `knowledge/architecture/deterministic-analysis.md`, `knowledge/decisions/modular-monolith.md`

## Scope

**Q2. Which initial rules can establish a confirmed relationship or identified gap?**
- **Options:** a broad rule library; one rule per evidence kind with explicit sufficiency; similarity scoring as the primary mechanism.
- **Trade-off:** a broad library cannot be justified without evidence samples; similarity produces plausible but unprovable relationships; per-evidence-kind rules are narrow but defensible.
- **Recommendation:** Agree criterion-specific sufficient evidence and a small explicit rule library; keep keyword similarity only a candidate signal.
- **Why:** Relevance alone does not establish a relationship or prove absence.
- **Resolution:** Initial library is two rules: (1) an explicit declaration by the owner or an authoritative source establishes the relationship it names; (2) a named required artifact is an identified gap only when the assessed scope was fully observed. Keyword overlap yields candidates only.
- **Status:** Recommended
- **Feeds:** FR-026, FR-027; initial rule and sufficiency policy
- **Knowledge:** `knowledge/architecture/deterministic-analysis.md`, `knowledge/concepts/evidence-semantics.md`

## Behaviour

**Q3. Should an inaccessible repository produce a negative capability finding?**
- **Options:** treat unreachable as absent; treat unreachable as unknown; treat unreachable as a gap.
- **Trade-off:** absence overclaims; a gap blames the project for an access failure; unknown with scope is accurate.
- **Recommendation:** Report missing or stale/unavailable evidence with its scope instead of a demonstrable gap.
- **Why:** Unknown evidence cannot establish falsehood.
- **Resolution:** Unavailable or stale inputs produce a "missing evidence" qualification naming the affected scope. A confirmed gap additionally requires a fully observed scope and a named criterion.
- **Status:** Recommended
- **Feeds:** FR-027, FR-028
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/ingestion-and-snapshots.md`

## Data

**Q4. Which input and time context must be frozen for reproduction?**
- **Options:** record the reference time only; record snapshots and rule versions; record the whole database file.
- **Trade-off:** a timestamp alone cannot reproduce inputs; rule and snapshot references are sufficient and auditable; copying the database is heavy and still ambiguous.
- **Recommendation:** Record relevant portfolio revisions, snapshots, rule/configuration versions and applicable reference time before evaluating rules.
- **Why:** Hidden current state changes would make identical-input claims misleading.
- **Resolution:** The report records: portfolio entity revisions used, source snapshot identifiers, rule-set version, configuration version and reference time. Rendering never re-reads live state.
- **Status:** Recommended
- **Feeds:** FR-029, NFR-017, NFR-018
- **Knowledge:** `knowledge/architecture/deterministic-analysis.md`, `knowledge/architecture/data-model.md`

## Integration

**Q5. How should conflicting declarations and verification evidence be resolved?**
- **Options:** latest source wins; authoritative source wins; retain both and mark unresolved.
- **Trade-off:** latest-wins rewrites history; authority-first resolves most cases but hides genuine disagreement; retaining both with a rule basis is auditable.
- **Recommendation:** Retain both with authority and revision context; agree claim-specific resolution rules rather than latest-source-wins.
- **Why:** Sources can describe different scopes or disagree legitimately.
- **Resolution:** Precedence for a named claim: owner declaration, then authoritative source declaration, then derived candidate. Equal-authority disagreement is reported as unresolved with both records, never silently merged.
- **Status:** Recommended
- **Feeds:** FR-027, FR-028; conflict handling contract
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/data-ownership.md`

## Architecture

**Q6. Can a historical report silently read today's evidence during rendering?**
- **Options:** re-read current data at render time; render the retained context only; re-read and mark differences.
- **Trade-off:** re-reading changes the meaning of an old report; retained-only can show inputs that no longer exist; the third option is honest but doubles the report surface.
- **Recommendation:** Render retained report context and explicitly qualify unavailable reproduction inputs.
- **Why:** A historical result must not change meaning on retrieval.
- **Resolution:** Rendering uses recorded snapshots and revisions. If a referenced snapshot has been pruned, the report states which input is unavailable rather than substituting current data.
- **Status:** Recommended
- **Feeds:** FR-029, FR-030, NFR-018, NFR-020
- **Knowledge:** `knowledge/architecture/deterministic-analysis.md`, `knowledge/architecture/persistence.md`

## Acceptance

**Q7. What should the fixed-input reproducibility assertion compare?**
- **Options:** byte-identical output; equivalent logical findings; identical run identifiers.
- **Trade-off:** byte equality fails on harmless metadata; run-identity equality tests nothing; logical equivalence targets the actual claim.
- **Recommendation:** Compare equivalent logical findings while allowing different generation times and run identities.
- **Why:** Operational metadata differs without changing analytical conclusions.
- **Resolution:** The comparison orders findings canonically and compares category, subject, criterion, evidence references and rule version. Generation time, run id and row order are excluded.
- **Status:** Recommended
- **Feeds:** FR-029, NFR-017
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/deterministic-analysis.md`

## Ambiguity

**Q8. Are finding categories exclusive, and how should rule-only changes be displayed?**
- **Options:** one exclusive category per finding; orthogonal qualifications; a single free-text label.
- **Trade-off:** exclusivity forces a stale candidate to pick one lossy label; free text cannot be compared; orthogonal fields keep both facts.
- **Recommendation:** Confirm the final vocabulary and comparison presentation; preserve separate freshness and uncertainty qualifications and explicit rule-change attribution.
- **Why:** A candidate can also be stale, and changed interpretation is not changed source evidence.
- **Resolution:** Category (confirmed, candidate, gap, missing evidence, unresolved) is one field; freshness and uncertainty are independent fields. A comparison records whether a difference came from source data or from a rule-version change.
- **Status:** Recommended
- **Feeds:** FR-027, FR-030, NFR-020; finding and comparison contract
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/deterministic-analysis.md`
