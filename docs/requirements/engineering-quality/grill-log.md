# Engineering-quality desk review

Desk review only, no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. These quality drafts do not claim passing application tests.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input that the documents cannot supply.

## Intent

**Q1. What distinguishes structural acceptance documents from verified application behavior?**
- **Options:** treat Gherkin as tests; treat only executed suites as evidence; report the two separately.
- **Trade-off:** calling Gherkin tests fabricates results; executing everything before the runner exists blocks progress; separate reporting is honest.
- **Recommendation:** Report document checks separately from executed automated tests and their actual results.
- **Why:** Tagged Gherkin without a runner or step definitions is not passing evidence.
- **Resolution:** Every verification report states which checks ran, which were structural only, and what each produced. A scenario with no runner is reported as documented, never as passing.
- **Status:** Recommended
- **Feeds:** NFR-034; verification reporting
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/practices/knowledge-and-delivery-separation.md`

## Scope

**Q2. Which workstation and repository sizes should resource measurements represent?**
- **Options:** enterprise-scale assumptions; no target at all; a documented local reference workload.
- **Trade-off:** enterprise assumptions violate proportionate engineering; no target makes NFR-001 unverifiable; a local reference is measurable now.
- **Recommendation:** Agree reference hardware and typical/largest portfolio fixtures before setting hard memory, storage or latency budgets.
- **Why:** Unmeasured enterprise-scale infrastructure would violate proportionate local operation.
- **Resolution:** Recommended default pending owner input: a four-core developer workstation with 16 GB RAM, one database of 50 goals and 500 projects, and one repository set of 20 local checkouts. The owner's confirmation of hardware and scale is what closes this.
- **Status:** Decision needed
- **Feeds:** NFR-004; reference workload
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/product/scope-and-roadmap.md`

## Behaviour

**Q3. Which failure behaviors must each slice exercise?**
- **Options:** happy path only; every possible failure; the failure classes the slice can actually produce.
- **Trade-off:** happy-path tests hide recovery defects; exhaustive failure matrices stall delivery; slice-relevant failures are testable and meaningful.
- **Recommendation:** Select relevant interruption, outage, invalid-data, failed-transaction, timeout and retry cases for each slice.
- **Why:** Successful execution alone cannot demonstrate recoverable failure behavior.
- **Resolution:** Each change's tasks name the failure classes it introduces and the test that exercises each. A slice with no failure test states why none applies.
- **Status:** Recommended
- **Feeds:** NFR-034, NFR-038
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/practices/vertical-slices.md`

## Data

**Q4. Which supported versions and malformed-source fixtures are required first?**
- **Options:** synthetic happy-path samples; a full version matrix; real versioned fixtures including malformed, stale and conflicting cases.
- **Trade-off:** happy-path samples cannot establish compatibility; a full matrix is premature; targeted real fixtures prove the parser's supported boundary.
- **Recommendation:** Agree real versioned fixtures with missing metadata, staleness and conflict, all reproducible without private repositories.
- **Why:** Synthetic happy-path-only samples cannot establish source compatibility.
- **Resolution:** Fixtures live in the repository and cover: valid current version, malformed document, missing required metadata, stale observation, conflicting duplicate identity. No fixture requires a private repository or credentials.
- **Status:** Recommended
- **Feeds:** NFR-035; initial fixture catalogue
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/source-adapters.md`

## Integration

**Q5. Should routine test runs require live Vyasa or an external AI account?**
- **Options:** require live services; mock everything including contracts; doubles for routine tests plus separate contract checks.
- **Trade-off:** live dependencies make tests flaky and non-reproducible; pure mocks drift from the real contract; the pair keeps routine tests offline and contracts honest.
- **Recommendation:** Isolate external systems with controlled doubles and use separate documented contract compatibility checks.
- **Why:** Network and account state must not determine routine test reproducibility.
- **Resolution:** The default test command runs offline with fixtures and doubles. Any live or contract check is a separate, documented command that never gates routine development.
- **Status:** Recommended
- **Feeds:** NFR-035, NFR-036
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/source-adapters.md`

## Architecture

**Q6. How should significant design and dependency choices be justified?**
- **Options:** no record; a prose paragraph in the PR; a decision concept with alternatives and consequences.
- **Trade-off:** no record loses rationale; prose in a PR is hard to find later; a decision concept is durable and searchable.
- **Recommendation:** Retain architectural alternatives/consequences and dependency purpose with appropriate version constraints and testable updates.
- **Why:** Unexplained frameworks and blurred module boundaries increase maintenance cost.
- **Resolution:** Each significant choice is recorded as a Decision concept in `knowledge/decisions/` or explicitly declined in the change's ADR artifact. Every dependency states its purpose and a version constraint.
- **Status:** Recommended
- **Feeds:** NFR-028, NFR-032, NFR-033
- **Knowledge:** `knowledge/decisions/index.md`, `knowledge/practices/vertical-slices.md`

## Acceptance

**Q7. What coverage criteria should supersede a bare percentage target?**
- **Options:** a coverage percentage gate; a critical-behavior list; both, with the list deciding.
- **Trade-off:** a percentage can be met with unimportant tests; a list needs judgement; the list first is the more honest gate.
- **Recommendation:** Identify critical behaviors and failure risks across all layers before agreeing any numeric coverage threshold.
- **Why:** A high percentage can still omit the integrity and trust boundaries that matter.
- **Resolution:** Critical behaviors: goal revision integrity, transactional rollback, migration recovery, access containment, idempotent ingestion, explicit unknown states. A numeric threshold is added only after these are covered, and never replaces them.
- **Status:** Recommended
- **Feeds:** NFR-034, NFR-038; critical-coverage policy
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/practices/vertical-slices.md`

## Ambiguity

**Q8. Which runtime/dependency versions and acceptance execution tooling are actually supported?**
- **Options:** float to latest; pin nothing; pin the stack and add a Gherkin runner only when it earns its cost.
- **Trade-off:** floating versions break reproducibility; pinning without updates accumulates risk; pinning plus a testable update process is the stated direction.
- **Recommendation:** Confirm support versions and whether a Gherkin runner adds value; do not imply tooling exists merely because scenarios are written.
- **Why:** Proposed stack direction and executable compatibility require different evidence.
- **Resolution:** First slice pins Python 3.12, FastAPI and pytest, records them in the dependency manifest, and runs acceptance scenarios as ordinary pytest tests. A Gherkin runner is not adopted; feature files remain non-executable drafts.
- **Status:** Recommended
- **Feeds:** NFR-033, NFR-034, NFR-036; support and acceptance tooling policy
- **Knowledge:** `knowledge/decisions/python-fastapi-backend.md`, `knowledge/practices/testing-and-validation.md`
