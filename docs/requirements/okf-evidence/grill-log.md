# OKF-evidence desk review

Desk review only: no interview or user confirmation. The goal-to-evidence report is a recommended first-release goal, NOT an approved release choice. Neither knowledge quality nor profile support is approved here.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs a real source sample the documents cannot supply.

## Intent

**Q1. Does a discoverable concept establish usable engineering knowledge?**
- **Options:** discovery implies usable knowledge; discovery implies nothing; report availability, correctness and applicability separately.
- **Trade-off:** the first overclaims; the second discards a useful signal; separate reporting stays honest at the cost of three fields.
- **Recommendation:** Report availability separately from correctness, completeness and applicability.
- **Why:** A readable document can still be wrong or irrelevant.
- **Resolution:** Each concept carries independent availability, declared-validation and applicability fields. Only the first is established by discovery.
- **Status:** Recommended
- **Feeds:** FR-019
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/okf-integration.md`

## Scope

**Q2. Which OKF versions, profiles and extensions should initial inventory support?**
- **Options:** support the format generally; support this bundle's version and profile only; defer OKF until profiles settle.
- **Trade-off:** general support without fixtures misreads unknown profiles; a single supported pair is provable; deferral removes the evidence type entirely.
- **Recommendation:** Confirm real package/profile fixtures rather than assuming this bundle represents every source.
- **Why:** Profile-required metadata can differ without violating the underlying format.
- **Resolution:** Initial support is OKF v0.2 with the `profile.json` v1 rules used in this repository. Any other version or profile is reported unsupported, and the concept is still inventoried as discoverable but unassessed.
- **Status:** Recommended
- **Feeds:** FR-018; supported-profile contract
- **Knowledge:** `knowledge/architecture/okf-integration.md`, `knowledge/architecture/source-adapters.md`

## Behaviour

**Q3. Must a knowledge concept have an OpenSpec requirement to be discoverable?**
- **Options:** require a requirement link; require nothing; allow optional many-to-many links.
- **Trade-off:** a mandatory link forces invented traceability; no link loses useful navigation; optional links keep both independent.
- **Recommendation:** Discover knowledge independently and permit optional many-to-many relationships.
- **Why:** Knowledge and behavioral obligations have independent purposes.
- **Resolution:** Concepts and requirements are each discoverable alone. A link is stored as a separate relationship record with its own basis and is never required for either side to exist.
- **Status:** Recommended
- **Feeds:** FR-020
- **Knowledge:** `knowledge/practices/knowledge-and-delivery-separation.md`, `knowledge/concepts/portfolio-domain.md`

## Data

**Q4. How should moved concepts and unresolved links retain identity?**
- **Options:** identify by path; identify by frontmatter identifier; merge on title similarity.
- **Trade-off:** paths change on reorganization; identifiers survive moves but may be absent; title merging silently joins unrelated concepts.
- **Recommendation:** Preserve profile identifiers and source/revision context, and agree reconciliation for path-only identities.
- **Why:** Paths and titles can change without establishing a new concept or a reliable merge.
- **Resolution:** Identity is the frontmatter identifier; path is an attribute updated per observation. With no identifier, the path is a weak identity, and two similar titles are reported unresolved rather than merged.
- **Status:** Recommended
- **Feeds:** FR-018, FR-019; concept identity policy
- **Knowledge:** `knowledge/architecture/data-model.md`, `knowledge/architecture/okf-integration.md`

## Integration

**Q5. Can a missing metadata field authorize repairing the source knowledge?**
- **Options:** add the missing field; report the diagnostic; reject the concept.
- **Trade-off:** editing crosses source authority; rejection loses otherwise usable knowledge; a diagnostic keeps both.
- **Recommendation:** Record profile diagnostics without changing the source.
- **Why:** Read-oriented ingestion does not confer publishing authority.
- **Resolution:** Missing or invalid profile metadata yields a diagnostic and marks the concept partially valid. The source file is never written and the concept remains discoverable.
- **Status:** Recommended
- **Feeds:** FR-021
- **Knowledge:** `knowledge/architecture/source-adapters.md`, `knowledge/architecture/security-and-privacy.md`

## Architecture

**Q6. Should declared validation status be stored as a universal truth flag?**
- **Options:** one boolean "validated"; trust the declared status; keep declared scope, validator and revision separately from parse outcome.
- **Trade-off:** a boolean erases scope and time; the third preserves what was actually claimed.
- **Recommendation:** Retain its declared scope, source and available validator/revision context separately from parsing outcome.
- **Why:** A past source declaration is not current universal verification.
- **Resolution:** Validation is a record: what was checked, by what, at which revision. It never becomes a property of the concept itself, and parsing success is stored separately.
- **Status:** Recommended
- **Feeds:** FR-018, FR-019
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/data-model.md`

## Acceptance

**Q7. What proves knowledge and requirements do not require one-to-one mapping?**
- **Options:** only linked concepts; only unlinked concepts; both plus many-to-many links.
- **Trade-off:** linked-only fixtures hide a mandatory coupling; unlinked-only hides link handling; the combination exercises both.
- **Recommendation:** Exercise standalone knowledge, standalone requirements and multiple optional links in controlled fixtures.
- **Why:** Linked-only fixtures would hide a mandatory coupling bug.
- **Resolution:** Fixture set: one concept with no requirement, one requirement with no concept, one concept linked to two requirements, and one requirement linked from two concepts.
- **Status:** Recommended
- **Feeds:** FR-020
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/practices/knowledge-and-delivery-separation.md`

## Ambiguity

**Q8. When should knowledge be labelled stale rather than merely old?**
- **Options:** stale by age threshold; stale on superseding revision; never stale; report age and leave freshness unknown.
- **Trade-off:** an age threshold is arbitrary and wrong for durable concepts; supersession is meaningful but often unavailable; "unknown" is honest but unhelpful alone.
- **Recommendation:** Agree source- and question-specific freshness signals and report unknown freshness where insufficient.
- **Why:** Age alone neither disproves a concept nor establishes current applicability.
- **Resolution:** Stale requires a declared validity window that has expired or a recorded superseding revision. Otherwise the concept reports its last-observed time and freshness "unknown"; age never becomes staleness.
- **Status:** Recommended
- **Feeds:** FR-019; knowledge freshness policy
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/ingestion-and-snapshots.md`
