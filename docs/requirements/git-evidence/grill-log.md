# Git-evidence desk review

Desk review only; no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. No Git provider or verification source has been selected here.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs a real repository or artifact sample the documents cannot supply.

## Intent

**Q1. Can many recent commits establish a delivered outcome?**
- **Options:** commit count as delivery evidence; commits as supporting activity only; ignore commits entirely.
- **Trade-off:** counting commits rewards volume; ignoring them discards attributable evidence; treating them as support keeps the distinction.
- **Recommendation:** Treat activity only as attributable supporting evidence.
- **Why:** Counts and recency do not demonstrate working behavior or business value.
- **Resolution:** Commits are recorded as activity attributed to a goal or project, with author, time and revision. No finding of achievement or completion may rest on commit volume or recency.
- **Status:** Recommended
- **Feeds:** FR-023
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/git-evidence.md`

## Scope

**Q2. Which access methods and history window are sufficient initially?**
- **Options:** remote provider APIs; local clone only, full history; local clone only, bounded window.
- **Trade-off:** remote APIs add credentials and network dependence; full history costs time and storage; a bounded window is cheap but hides older evidence.
- **Recommendation:** Confirm existing local versus remote capabilities and a bounded collection window from real repositories.
- **Why:** Full history and every provider are not free or implicit requirements.
- **Resolution:** Recommended default: local repository only, read through plumbing commands, last 500 commits per observed branch plus any explicit deeper request. No remote credentials in the first slice; remote access is a later, separately authorized change.
- **Status:** Recommended
- **Feeds:** FR-022; Git access and scope contract
- **Knowledge:** `knowledge/architecture/git-evidence.md`, `knowledge/architecture/source-adapters.md`

## Behaviour

**Q3. Does absence of a test artifact mean tests failed?**
- **Options:** absent test artifact means failure; means success; means unknown.
- **Trade-off:** failure overclaims a negative; success overclaims delivery; unknown is accurate but less satisfying.
- **Recommendation:** Report unknown or unavailable verification rather than success or failure.
- **Why:** No observation is not an observed negative result.
- **Resolution:** With no verification artifact in an observed revision, verification is unknown. A recorded failing result is the only path to "failed"; a recorded passing result is the only path to "passed".
- **Status:** Recommended
- **Feeds:** FR-024
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/git-evidence.md`

## Data

**Q4. How should comparisons survive branch retargeting or shallow history?**
- **Options:** compare branch names; compare commit ids with a coverage flag; refuse comparison in shallow clones.
- **Trade-off:** branch names move; ids with coverage stay reproducible but may be incomplete; refusing comparison loses most of the value in CI checkouts.
- **Recommendation:** Preserve exact observed revisions and coverage limits; agree reconciliation when prior objects are unavailable.
- **Why:** Mutable branch names cannot reproduce historical comparisons on their own.
- **Resolution:** Store commit id, tree id and a shallow/partial flag. A branch is an attribute, not an identity. If a required prior object is missing, the comparison reports "not reproducible" and is not reconstructed.
- **Status:** Recommended
- **Feeds:** FR-022; revision-history policy
- **Knowledge:** `knowledge/architecture/git-evidence.md`, `knowledge/architecture/ingestion-and-snapshots.md`

## Integration

**Q5. Should ordinary refresh check out a branch to obtain evidence?**
- **Options:** check out the target branch; read refs without checkout; copy the repository first.
- **Trade-off:** checkout mutates the owner's working tree; copying is expensive; ref reading is read-only and sufficient for the evidence in scope.
- **Recommendation:** Read existing permitted evidence without checkout, commit or publication.
- **Why:** Routine evidence collection must not modify the owner's repository state.
- **Resolution:** Use read-only plumbing (`rev-parse`, `rev-list`, `cat-file`, `log`) against existing refs. No checkout, fetch, commit, tag or index write is permitted during collection.
- **Status:** Recommended
- **Feeds:** FR-025
- **Knowledge:** `knowledge/architecture/git-evidence.md`, `knowledge/architecture/security-and-privacy.md`

## Architecture

**Q6. Should imported verification results be merged into commit activity totals?**
- **Options:** one combined "delivery" score; separate evidence kinds; verification overrides activity.
- **Trade-off:** combining hides which kind failed; separation keeps the distinction the requirements demand.
- **Recommendation:** Keep verification observations separately attributed to source, revision and time.
- **Why:** Activity and executed verification are different evidence kinds.
- **Resolution:** Evidence rows carry a kind (`activity`, `verification`), source, revision and time. Reports may show both; no field sums them into one number.
- **Status:** Recommended
- **Feeds:** FR-023, FR-024
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/deterministic-analysis.md`

## Acceptance

**Q7. What checks show that collection remains read-only on failure?**
- **Options:** assert no commit was created; compare tree and ref state before and after; trust the adapter.
- **Trade-off:** a commit-only check misses index and ref changes; before/after comparison is cheap and complete for the state that matters.
- **Recommendation:** Compare repository contents and checked-out references before and after successful and failed collection.
- **Why:** Failure handling can accidentally introduce checkout or repair side effects.
- **Resolution:** The acceptance check snapshots HEAD, all refs, the index state and the working-tree status before and after each run, including injected failures, and requires them unchanged.
- **Status:** Recommended
- **Feeds:** FR-025
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/git-evidence.md`

## Ambiguity

**Q8. Which test, build and release artifact formats should be accepted first?**
- **Options:** infer success from filenames or tags; parse a specific CI result format; accept none until formats are agreed.
- **Trade-off:** name inference is false evidence; one parsed format needs a real sample; accepting none leaves verification permanently unknown.
- **Recommendation:** Agree supported real formats and their revision applicability instead of inferring success from filenames or tags.
- **Why:** Release records and Git tags do not establish the same fact.
- **Resolution:** Recommended default: no verification format in the first slice; verification reports unknown. The question closes with one real CI or test-result sample and its revision applicability.
- **Status:** Decision needed
- **Feeds:** FR-024; verification support matrix
- **Knowledge:** `knowledge/architecture/git-evidence.md`, `knowledge/concepts/evidence-semantics.md`
