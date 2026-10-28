# Source-ingestion desk review

Desk review, not an interview; no user confirmation occurred. The recommended first-release goal is a goal-to-evidence report, NOT an approved release choice. Native contract details below remain unconfirmed.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input or a real source sample, and the block names that input.

## Intent

**Q1. Does inventory ingestion create a second authoritative project registry?**
- **Options:** copy Vyasa inventory into a Siddhi-owned project table; keep only a projection keyed by source identity; call Vyasa live on each read.
- **Trade-off:** a local registry drifts and competes for authority; live reads couple every view to remote availability; a keyed projection keeps provenance and local reads.
- **Recommendation:** Retain Vyasa source identifiers and map them to internal references without competing identities.
- **Why:** Discovery and portfolio ownership have different authorities.
- **Resolution:** Siddhi stores a projection: source identifier, observed attributes, snapshot and observation time. Vyasa remains authoritative for project identity; no field of the projection may be edited locally.
- **Status:** Recommended
- **Feeds:** FR-007, FR-010, NFR-011, NFR-012
- **Knowledge:** `knowledge/architecture/vyasa-integration.md`, `knowledge/architecture/data-ownership.md`

## Scope

**Q2. Which real Vyasa interface and artifact versions are supported first?**
- **Options:** assume a REST interface; assume a JSON export layout; inspect a real sample before naming anything.
- **Trade-off:** assuming an interface produces an adapter nobody can validate; waiting for a sample blocks the first ingestion slice; a staged default with one real sample bounds both.
- **Recommendation:** Inspect the real contract and representative repositories before naming versions, paths or access methods.
- **Why:** An assumed layout or API cannot establish compatibility.
- **Resolution:** Recommended default: read a Vyasa-exported inventory JSON from a configured local path, with the file's declared version recorded per observation. One representative export is the input that closes this question; until then no version, endpoint or field name is specified.
- **Status:** Decision needed
- **Feeds:** FR-007, FR-008, FR-009, NFR-029, NFR-031; adapter support matrix
- **Knowledge:** `knowledge/architecture/vyasa-integration.md`, `knowledge/architecture/source-adapters.md`

## Behaviour

**Q3. Can an inaccessible source be treated as having removed its projects?**
- **Options:** drop unreachable projects; mark them unavailable; mark them removed.
- **Trade-off:** dropping destroys history and misreads an outage as deletion; keeping them silently looks current; marking unavailable preserves both facts.
- **Recommendation:** Retain prior data with unavailable/stale qualifications; establish removal only within sufficiently observed scope.
- **Why:** Access failure is not deletion evidence.
- **Resolution:** Removal requires a completed observation whose declared scope covered the project and did not return it. Any partial or failed observation leaves prior records with an unavailable or stale qualification.
- **Status:** Recommended
- **Feeds:** FR-011, FR-012, NFR-005, NFR-006, NFR-009, NFR-013
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/ingestion-and-snapshots.md`

## Data

**Q4. Which timestamps and revision signals establish unchanged content?**
- **Options:** compare modification times; compare content hashes; compare declared revision identifiers.
- **Trade-off:** mtimes lie across copies and checkouts; hashes are reliable but require reading content; revisions are cheapest when the source provides stable ones.
- **Recommendation:** Prefer reliable revisions or content hashes and distinguish source times from ingestion time; re-evaluate safely when signals are unreliable.
- **Why:** Equal timestamps do not prove equal content.
- **Resolution:** Order of trust: declared revision identifier, then content hash, then re-read. Record source modification time and ingestion time as separate fields; never substitute one for the other.
- **Status:** Recommended
- **Feeds:** FR-013, NFR-003, NFR-016
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/concepts/evidence-semantics.md`

## Integration

**Q5. How should a retry of the same captured revision affect logical records?**
- **Options:** insert a new record per attempt; overwrite the record in place; key the record by source, identity and revision.
- **Trade-off:** per-attempt rows inflate inventory; in-place overwrite loses attempt history; a revision key is idempotent but needs attempt records kept separately.
- **Recommendation:** Preserve attempt outcomes without duplicate logical source records or artificial changes.
- **Why:** Retrying an observation must not inflate inventory or progress.
- **Resolution:** Logical key is (source, source identity). Each successful capture appends an observation carrying the revision or hash; retries append attempt records but never a second logical project.
- **Status:** Recommended
- **Feeds:** FR-011, FR-013, NFR-008
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/architecture/data-model.md`

## Architecture

**Q6. Is partial publication atomic per source, project or portfolio?**
- **Options:** per project; per source snapshot; per portfolio refresh across all sources.
- **Trade-off:** per project publishes fragments as current; per portfolio refresh cannot be atomic across independent sources; per source matches the unit that actually has a manifest.
- **Recommendation:** Agree a publication unit and independently report capture coverage before allowing partial results to replace usable views.
- **Why:** A transaction cannot manufacture cross-source atomic observations.
- **Resolution:** Publication unit is one source snapshot with a manifest. A snapshot replaces the usable view only when it is complete for its declared scope; incomplete snapshots remain queryable as partial and are never published as current.
- **Status:** Recommended
- **Feeds:** FR-011, FR-012, NFR-006; persistence-recovery publication contract
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/architecture/persistence.md`

## Acceptance

**Q7. What demonstrates schema-aware failure isolation?**
- **Options:** a happy-path ingest only; malformed and unsupported sources alongside a good one; a unit test of the parser alone.
- **Trade-off:** a happy path proves nothing about degradation; parser unit tests miss the cross-source read path; the mixed refresh exercises both.
- **Recommendation:** Refresh one supported source alongside malformed and unsupported sources while proving existing portfolio reads remain usable.
- **Why:** A successful happy-path parser does not demonstrate safe degradation.
- **Resolution:** The acceptance fixture refreshes three sources: one valid, one malformed, one with an unsupported declared version. The valid one publishes; the other two record invalid and unsupported states; goal and project reads continue from the last good snapshot.
- **Status:** Recommended
- **Feeds:** FR-009, FR-012, NFR-005, NFR-009, NFR-031
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/source-adapters.md`

## Ambiguity

**Q8. Should interrupted refreshes resume or restart, and when is data stale?**
- **Options:** always resume from a saved cursor; always restart the batch; resume where the source supports it, otherwise restart.
- **Trade-off:** blind resume can skip records if the cursor was not durable; restart is simple but repeats work; capability-based choice costs a per-source declaration.
- **Recommendation:** Agree source-specific checkpoint/retry and freshness policies from actual capabilities; never advance uncommitted progress.
- **Why:** Universal cursor and age assumptions risk skipped records and misleading currency.
- **Resolution:** Resume only when the source declares a resumable checkpoint and the checkpoint was committed before interruption; otherwise restart the batch. Freshness is the source's declared maximum age, else reported as unknown; age alone never marks data current.
- **Status:** Recommended
- **Feeds:** FR-011, FR-012, FR-013; refresh recovery and freshness policy
- **Knowledge:** `knowledge/architecture/ingestion-and-snapshots.md`, `knowledge/architecture/workflow-coordination.md`
