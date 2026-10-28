# Testing and Validation

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `testing-and-validation.md`  
**Status:** Draft for review  
**Scope:** Software testing, source validation, evidence verification, analytical correctness, security testing, and release readiness  
**Implementation status:** Not yet verified in a running system

---

## 1. Purpose

This document defines how Siddhi will be tested and how the correctness, completeness, reliability, and limitations of its outputs will be validated.

Siddhi combines portfolio management, source ingestion, evidence normalization, deterministic analysis, historical comparisons, and optional external AI analysis. Each capability has different validation needs.

The testing strategy must establish that:

- Software components behave according to their contracts.
- Source data is ingested without silently losing or changing its meaning.
- Historical snapshots and provenance are preserved.
- Deterministic analysis produces reproducible results for the same inputs and rule versions.
- Missing or incomplete evidence is not mistaken for success or failure.
- External AI responses cannot bypass validation or automatically approve decisions.
- Security, privacy, recovery, and configuration controls work as intended.
- The system communicates uncertainty and validation limitations honestly.

Testing must be proportionate to the product. The initial system should use a maintainable automated test suite and targeted integration tests rather than introducing a complex testing platform before it is needed.

## 2. Core validation principles

### 2.1 Different claims require different evidence

Siddhi must distinguish the following activities.

| Activity | What it establishes | What it does not establish |
|---|---|---|
| Parsing | Content can be read according to a parser's supported format | Content is truthful, complete, or current |
| Schema validation | A representation satisfies a defined structural schema | Its claims are factually correct |
| Source validation | A source can be accessed and meets defined connection checks | The source contains all expected information |
| Ingestion validation | Collected data meets ingestion and consistency rules | The original source is correct |
| Evidence verification | A specific claim is supported by an appropriate verification method | Every related goal is achieved |
| Software testing | Tested behavior meets specified expectations under tested conditions | The entire system is defect-free |
| Deterministic analysis | Findings follow the configured rules and captured inputs | The rules are strategically correct |
| AI review | A model has produced an advisory interpretation | The interpretation is verified or approved |
| Outcome confirmation | Defined acceptance criteria have been satisfied using appropriate evidence | Unrelated outcomes have been achieved |

These distinctions must be reflected in stored records, API responses, reports, and user-facing descriptions.

### 2.2 Deterministic validation by default

Routine checks such as schema validation, identity matching, freshness evaluation, relationship checks, consistency checks, and rule-based analysis should use deterministic logic.

External AI must not be a prerequisite for routine validation.

AI may assist with ambiguous semantic judgments, opportunity analysis, prioritization, or interpretation, but its output must remain explicitly advisory until reviewed.

### 2.3 Preserve uncertainty

The system must distinguish at least:

- Validated or passed.
- Failed.
- Not evaluated.
- Unknown.
- Incomplete.
- Stale.
- Conflicting.
- Candidate or inferred.
- Unsupported by available evidence.

Not every validation mechanism requires every state. The selected states must reflect what the particular check can actually establish.

Missing data must not be converted automatically into a failed result or a passed result.

### 2.4 Test observable behavior

Tests should verify externally observable behavior and important domain invariants rather than overfitting to internal implementation details.

A refactor that preserves behavior should not require rewriting every test. Conversely, a passing unit test is insufficient if the integration or user-visible workflow is broken.

## 3. Validation domains

Siddhi's validation strategy covers six distinct domains.

### 3.1 Software validation

Verify API behavior, application use cases, domain rules, persistence, migrations, and integration adapters.

### 3.2 Source validation

Verify source accessibility, supported format handling, schema compatibility, identity resolution, completeness declarations, and source freshness.

### 3.3 Evidence validation

Verify provenance, source references, timestamps, verification methods, evidence classification, and the relationship between claims and supporting artifacts.

### 3.4 Analytical validation

Verify deterministic rules, finding classifications, reproducibility, historical comparisons, and handling of missing or conflicting evidence.

### 3.5 AI-output validation

Verify response structure, referenced evidence, uncertainty handling, disclosure policy, and the separation between recommendations and approved decisions.

### 3.6 Operational validation

Verify startup, configuration, security boundaries, backup and restore, failure recovery, resource limits, and release packaging.

## 4. Test architecture

The proposed test architecture should align with the modular backend design.

```text
tests/
  unit/
    domain/
    application/
    analysis/
    validation/
  contract/
    api/
    sources/
    external_analysis/
  integration/
    persistence/
    migrations/
    ingestion/
    adapters/
  security/
    api/
    filesystem/
    secrets/
    disclosure/
  recovery/
    ingestion/
    database/
    configuration/
  end_to_end/
    portfolio_workflows/
    reporting/
```

This is an illustrative structure, not a mandatory directory layout. The actual structure should follow the selected Python and frontend test conventions.

### 4.1 Unit tests

Test isolated domain rules, application logic, classification logic, transformations, and error handling.

Unit tests should be fast and independent of external services. Use fakes or controlled fixtures when the purpose is to validate business logic rather than the behavior of a real dependency.

### 4.2 Contract tests

Verify that API requests and responses conform to the documented API contract and that source adapters honor their declared capabilities.

Contract tests should detect accidental incompatibilities between the backend, future desktop client, and external integration adapters.

### 4.3 Integration tests

Exercise real component boundaries, including:

- Database repositories and transactions.
- Migration sequences.
- Ingestion and snapshot publication.
- Source normalization.
- Rule execution against persisted inputs.
- Secret-store integration where available.
- External AI provider adapters using controlled test endpoints or mocks.

Use temporary databases and isolated filesystem fixtures. Live credentials and production repositories should not be required for ordinary automated tests.

### 4.4 End-to-end tests

Exercise complete user workflows through the API and, when the desktop client exists, through the supported user interface.

The first end-to-end workflow should cover discovery, ingestion, evidence review, goal creation or selection, deterministic analysis, and report generation.

End-to-end tests should remain limited to high-value workflows; most behavioral coverage should reside in lower-level tests.

## 5. Test data and fixtures

### 5.1 Representative source fixtures

Create version-controlled, synthetic fixtures that represent the supported source formats and expected variations.

Fixtures should cover:

- A valid, complete source.
- A valid but empty source.
- A partially available source.
- A stale source snapshot.
- Duplicate identities.
- Conflicting source records.
- Unsupported schema versions.
- Malformed content.
- Missing optional fields.
- Unknown metadata fields.
- Deleted or renamed source artifacts.
- Permission failures.
- Large or unusually nested documents.
- Source content containing misleading instructions or suspicious links.

Use synthetic project names, paths, identifiers, credentials, and personal information. Do not include private repository contents or production secrets in the test suite.

### 5.2 Golden test datasets

Maintain a small set of deterministic fixtures with expected normalized records, evidence classifications, findings, and report summaries.

Golden tests should detect unintended behavior changes when parsing, normalization, rules, or output schemas change.

Expected outputs must be reviewed when a deliberate change modifies behavior. Updating a golden file without understanding the difference must not be treated as successful validation.

### 5.3 Fixture provenance

Each important fixture should document:

- The source format it represents.
- Its intended test scenario.
- Whether it is complete or deliberately partial.
- The expected validation result.
- Any assumptions needed to interpret the expected result.

Fixtures must not silently encode assumptions that conflict with the approved data-ownership or domain rules.

## 6. API and application behavior

The API and application layers must be tested against their documented contracts.

### 6.1 Request validation

Test:

- Valid requests.
- Missing required fields.
- Invalid identifiers and enum values.
- Invalid dates and unsupported ranges.
- Malformed JSON.
- Unexpected content types.
- Oversized requests.
- Invalid pagination parameters.
- Unsupported state transitions.
- Conflicting updates.
- Unauthorized requests under the selected security model.

Responses must use stable error codes and avoid leaking stack traces, secrets, database internals, or sensitive source content.

### 6.2 Application invariants

Test that application use cases enforce rules regardless of whether the request originates from the desktop client, a test client, or another authorized API consumer.

Examples include:

- A recommendation cannot automatically become an approved decision.
- A source cannot be accessed when disabled.
- An analysis result identifies its inputs and rule version.
- An invalid plan transition is rejected.
- An unavailable source does not erase historical evidence.
- A partial ingestion is not reported as a complete refresh.
- A source artifact's declared status is not presented as independent verification.

### 6.3 API compatibility

The API's OpenAPI contract should be checked in CI.

When a change alters a request or response schema, evaluate whether the change is backward-compatible and whether the future desktop client must be updated.

Breaking changes must be deliberate and documented rather than introduced accidentally through internal model changes.

## 7. Persistence and migration validation

Persistence behavior is governed by `persistence-and-migrations.md`.

Tests must verify:

- Fresh database initialization.
- Repository CRUD behavior and identity stability.
- Foreign-key and uniqueness constraints.
- Transaction commit and rollback.
- Historical revision preservation.
- Migration order and schema version tracking.
- Migration failure and recovery.
- Supported upgrades from older database versions.
- Rejection of unsupported newer schema versions.
- Backup creation and restoration.
- Handling of disk-full and permission-denied conditions.
- Database integrity checks.

### 7.1 Migration testing

Every schema migration must be tested against representative prior database states.

Where supported upgrade paths include multiple earlier releases, test those paths rather than only testing the immediately preceding version.

Validation must include data preservation and semantic correctness, not merely successful schema creation.

### 7.2 Ingestion consistency testing

Verify that:

- Failed refreshes preserve the last-known-good published snapshot.
- Partial results remain distinguishable from complete results.
- Retries do not create duplicate logical records.
- Checkpoints advance only after corresponding data is safely committed.
- Staged records are not presented as published evidence.
- Historical snapshots remain available under the defined retention policy.

## 8. Source integration validation

Each adapter must have a documented capability contract and a corresponding test suite.

### 8.1 Adapter-level validation

Test:

- Connection and access failure.
- Supported and unsupported source formats.
- Source identity resolution.
- Schema version detection.
- Completeness and freshness reporting.
- Duplicate and conflicting records.
- Pagination or bounded scanning behavior.
- Timeout and retry handling.
- Permission-denied behavior.
- Safe handling of source removal.
- Read-only behavior.

A successful connection must not automatically mark a source as complete or verified.

### 8.2 Vyasa integration

Validate that Siddhi correctly interprets the actual Vyasa interface and its declared project metadata.

Test:

- Stable project and repository identity.
- Missing or unavailable metadata.
- Discovery completeness and freshness.
- Technology metadata and CI/CD indicators where supplied.
- OpenSpec and OKF presence indicators.
- Repository location and remote origin fields.
- Partial discovery results.
- Changes to the Vyasa response contract.

Siddhi must not assume that a missing field means the corresponding capability does not exist. It should distinguish absent, unknown, unsupported, and explicitly false values according to the source contract.

### 8.3 OpenSpec integration

Validate the actual OpenSpec conventions and schemas used by each repository.

Tests should include:

- Intent-driven artifacts.
- Team-specific schemas and templates.
- Frontend, backend, and QA artifacts where applicable.
- Delta-format requirement changes.
- Unsupported or malformed artifacts.
- Missing optional artifacts.
- Different supported schema versions.
- Task status versus independent verification.
- Source changes between consecutive snapshots.

Do not use a single universal fixture as proof that every repository's OpenSpec workflow is supported.

### 8.4 OKF integration

Validate against the actual OKF implementation and schema selected for the project.

Tests should cover:

- Supported document and metadata formats.
- Unknown metadata preservation.
- Concept and relationship extraction.
- Source-declared validation status.
- Missing and conflicting references.
- Schema incompatibility.
- Changes to knowledge packages.
- Separation of parsed knowledge from independently verified claims.

Public examples or assumed schemas must not substitute for testing against the actual installed format.

### 8.5 Git evidence integration

Tests should verify:

- Repository identity and origin handling.
- Bounded history scans.
- Commit and changed-path extraction.
- Branch and tag interpretation where supported.
- History changes or rewritten references.
- Missing repositories and inaccessible objects.
- Safe behavior for symbolic links and unusual paths.
- No checkout, commit, push, or unintended source modification.

A commit's existence must not be interpreted automatically as evidence that a particular goal has been achieved.

## 9. Evidence validation

Evidence validation must be separate from source parsing and deterministic analysis.

### 9.1 Evidence integrity

Where applicable, verify that each evidence record has:

- A stable evidence identity.
- A source system and source instance.
- A source artifact reference or captured representation.
- Acquisition and observation timestamps.
- A reference to the relevant source snapshot.
- A declared or inferred classification.
- A documented verification method, when verification is claimed.
- A freshness or applicability assessment where relevant.

Not every source can provide every field. Missing fields must be represented honestly rather than filled with fabricated defaults.

### 9.2 Evidence classifications

Tests must verify that the system distinguishes supported classifications such as:

- Confirmed by a specified verification method.
- Declared by a source.
- Inferred from available evidence.
- Candidate match.
- Missing evidence.
- Stale evidence.
- Conflicting evidence.
- Not evaluated.

The exact vocabulary must be aligned with `deterministic-analysis.md` and the domain model.

### 9.3 Goal-to-evidence mapping

Test that evidence is mapped to goals only through explicit relationships or documented matching rules.

A title similarity, keyword match, or shared repository must not automatically establish that a project satisfies a goal.

Where the relationship is inferred, the system should preserve the basis for the inference and expose it for review.

### 9.4 Verification method and scope

A verification result must identify what was verified and by which method.

For example, a successful test run may verify a particular behavior under a particular test environment. It does not prove that every feature works in production or that a strategic objective has been achieved.

Tests must prevent the system from generalizing a narrow verification result into a broader unsupported claim.

## 10. Deterministic analysis validation

Deterministic analysis must be reproducible and explainable.

### 10.1 Reproducibility

For the same captured inputs, rule version, and relevant configuration, an analysis run should produce the same substantive findings.

If output includes execution timestamps or other intentionally variable metadata, tests should compare the deterministic result separately from that metadata.

Every analysis result must identify the inputs and rule version needed to explain its outcome.

### 10.2 Rule correctness

Each rule must have tests for:

- Expected positive cases.
- Expected negative cases.
- Boundary conditions.
- Missing inputs.
- Stale inputs.
- Conflicting inputs.
- Unsupported data.
- Invalid relationships.
- Rule-version changes.

Where a rule evaluates a goal-specific acceptance criterion, test the passed, failed, and not-evaluable cases when that distinction is meaningful.

### 10.3 No universal progress assumptions

Siddhi must not assume that all projects or goals can be measured by a single percentage or lifecycle.

Tests should cover different goal types and acceptance criteria, including criteria that cannot be evaluated automatically.

If a goal lacks sufficient machine-evaluable criteria, the system must report the limitation rather than inventing a progress score.

### 10.4 Historical comparisons

Test that comparisons between analysis runs correctly account for:

- Changed source snapshots.
- Changed goal or plan revisions.
- Changed rule versions.
- New or removed evidence.
- Freshness changes.
- Reclassified findings.
- Previously incomplete source scans.

A change in reported status must be explainable by changed inputs, changed rules, or an explicitly recorded assessment—not by hidden nondeterminism.

## 11. External AI validation

External AI analysis requires both technical validation and policy validation.

### 11.1 Request construction

Test that requests:

- Use the intended provider and model configuration.
- Include only context permitted for the selected workflow.
- Exclude credentials and unnecessary sensitive content.
- Record relevant provider, model, prompt-template, and policy versions.
- Respect configured request-size and timeout limits.
- Fail safely when provider configuration is missing or invalid.

### 11.2 Response validation

Validate responses against the expected structured schema.

Test for:

- Valid responses.
- Missing required fields.
- Invalid enum values.
- Unsupported evidence references.
- Contradictory recommendations.
- Unjustified certainty.
- Malformed JSON or structured output.
- Oversized responses.
- Provider timeouts and rate limits.
- Provider failures and retries.

A syntactically valid response must not automatically be considered factually correct.

### 11.3 Evidence references

Any evidence reference returned by an external model must be checked against the available evidence set.

Unknown or invalid references must be rejected, marked unresolved, or otherwise clearly identified. The system must not fabricate a valid reference to make the response appear complete.

### 11.4 Advisory-only behavior

Test that model output cannot directly:

- Approve a recommendation.
- Change a goal's authoritative state.
- Modify an external source.
- Execute arbitrary code or shell commands.
- Change security configuration.
- Bypass access controls.

A recommendation becomes an approved decision only through the defined authorized workflow.

### 11.5 Evaluation datasets

Maintain a small, versioned evaluation dataset for important AI-assisted workflows, such as strategic prioritization or internal-tool investment analysis.

The dataset should include:

- Clear evidence.
- Incomplete evidence.
- Conflicting evidence.
- Ambiguous project relationships.
- Unsupported assumptions.
- Cases where the correct answer is to defer judgment.

Evaluate output quality against explicit criteria such as evidence grounding, uncertainty handling, relevance, and policy compliance.

AI evaluations are useful for detecting regressions but do not guarantee consistent behavior across models, provider versions, or all possible inputs.

## 12. Security and privacy validation

Security tests must align with `security-and-privacy.md` and `configuration-and-secrets.md`.

Required test areas include:

- API authentication and authorization.
- Loopback binding and remote-exposure defaults.
- Path traversal and symlink handling.
- Read-only source access.
- Malformed and oversized inputs.
- Secret redaction.
- Unauthorized configuration changes.
- Safe database and backup permissions.
- External AI context minimization.
- Prompt-injection resistance.
- Resource exhaustion and bounded execution.
- Error responses that do not reveal sensitive internals.

Use synthetic secrets in tests and verify that they do not appear in logs, reports, API responses, or external AI payloads.

Security testing should include both positive tests demonstrating authorized access and negative tests demonstrating rejection of unauthorized or unsafe behavior.

## 13. Operational and recovery validation

Test operational behavior under normal and failure conditions.

### 13.1 Startup and configuration

- Valid configuration starts successfully.
- Invalid security-critical configuration fails safely.
- Missing optional integrations do not prevent core functionality.
- Unsupported schema versions are reported clearly.
- The API reports readiness accurately.
- Startup and shutdown behavior follow the selected process-lifecycle model.

### 13.2 Ingestion recovery

- Source timeout.
- Source becomes unavailable during a scan.
- Partial scan.
- Invalid response.
- Process interruption.
- Database write failure.
- Retry after interrupted work.
- Restart with an incomplete ingestion run.

Recovery must not present incomplete work as complete or lose the last-known-good state.

### 13.3 Backup and restore

Test that a backup can be created and restored through the documented procedure.

Validation must confirm:

- Database readability.
- Schema compatibility.
- Core record integrity.
- Relationship integrity.
- Historical provenance preservation.
- Correct application behavior after restoration.

A successful backup command alone is not sufficient proof of recoverability.

### 13.4 Resource limits

Test representative large inputs and bounded failure cases.

Measure behavior for:

- Large source inventories.
- Many small documents.
- Large individual documents.
- Long Git histories within the configured limit.
- Repeated ingestion requests.
- Concurrent background jobs.
- Large reports.
- External AI timeouts.

The objective is to verify the configured limits and graceful failure behavior, not to benchmark every possible scale in the first release.

## 14. Frontend and end-to-end validation

When `siddhi-desktop` is implemented, its tests should verify the user-visible workflows and the frontend/backend boundary.

### 14.1 Frontend behavior

Test:

- Form validation and error presentation.
- Loading, success, partial-success, and failure states.
- Display of stale, missing, conflicting, and inferred evidence.
- Clear separation between findings, recommendations, and decisions.
- Confirmation before consequential actions.
- Safe rendering of untrusted source content.
- Handling of backend unavailability and restart.
- Prevention of accidental duplicate operations.

### 14.2 End-to-end scenarios

The first release should have an end-to-end test for the following path:

1. Start Siddhi with an isolated test configuration.
2. Discover or configure a test source.
3. Ingest source metadata and evidence.
4. Confirm the snapshot's completeness and provenance.
5. Create or select a portfolio goal.
6. Run deterministic analysis.
7. Review findings and unresolved evidence.
8. Generate a report.
9. Change the source fixture and refresh.
10. Compare the new analysis with the earlier result.
11. Verify that historical results remain explainable.

The scenario must include at least one incomplete or stale evidence case to ensure the system does not overstate progress.

Use Playwright or another selected browser/desktop automation tool where it provides meaningful end-to-end coverage. Do not make UI automation a substitute for domain and integration tests.

## 15. Performance and reliability validation

Performance targets must be taken from `non-functional-requirements.md` after the reference environment and test data are defined.

Tests should measure:

- API latency for common reads and writes.
- Source discovery and ingestion duration.
- Analysis execution time.
- Report generation time.
- Database growth and query behavior.
- Memory consumption for representative source sizes.
- Recovery time after common failures.

Performance tests must use repeatable datasets and document relevant environment details.

Initial performance testing should focus on the first usable release's expected workload. Larger scale tests can be added when the actual portfolio size and source volume justify them.

Do not claim a performance target is met based solely on a developer's local interactive experience.

## 16. Automation and continuous integration

The project should run an appropriate automated test suite whenever relevant changes are proposed.

A proposed CI sequence is:

1. Formatting and linting.
2. Static type checks.
3. Unit tests.
4. Contract tests.
5. Integration and migration tests.
6. Security-sensitive tests.
7. Dependency vulnerability checks.
8. API schema compatibility checks.
9. Selected end-to-end tests.
10. Test report and artifact publication.

The exact sequence and required gates should reflect execution cost and reliability.

### 16.1 Test classification

Label tests by purpose and execution cost where useful:

- **Fast:** unit and lightweight contract tests.
- **Integration:** real database and adapter boundaries.
- **Security:** authorization, filesystem, secret handling, and disclosure controls.
- **End-to-end:** complete user workflows.
- **Extended:** performance, larger datasets, and longer-running recovery scenarios.

A pull request should run the fast suite and required integration checks. Extended tests may run on a schedule or before release when their cost is disproportionate to routine changes.

### 16.2 Flaky tests

Tests must not be made reliable by repeatedly rerunning them until they pass.

For intermittent failures:

- Capture the failure conditions.
- Determine whether the problem is timing, environment, concurrency, or a real defect.
- Fix the underlying issue or isolate a documented external dependency.
- Track temporarily quarantined tests.
- Avoid treating quarantined tests as passed coverage.

## 17. Test results and validation records

Siddhi should distinguish test execution records from portfolio evidence and strategic assessments.

A test result may be represented as evidence for a specific claim, but only within the test's declared scope.

Where test results are ingested from external CI/CD systems, preserve the source reference and relevant execution metadata.

A validation record should identify, where applicable:

- The object or claim being validated.
- The validation method.
- The source or test environment.
- The execution time.
- The result and scope.
- Relevant tool, rule, or test-suite version.
- The supporting artifact or report reference.
- Limitations or untested conditions.

Do not convert a test pass into a universal quality guarantee. A passing test suite indicates that the included checks passed under the recorded conditions.

## 18. Release readiness

A release candidate should be evaluated against a defined checklist.

### Required release gates

- [ ] Required unit and contract tests pass.
- [ ] Required integration and migration tests pass.
- [ ] Supported upgrade paths are tested.
- [ ] Backup and restoration have been verified.
- [ ] Core ingestion and snapshot consistency scenarios pass.
- [ ] Deterministic analysis produces reproducible findings for fixed fixtures.
- [ ] Missing and conflicting evidence is represented correctly.
- [ ] Security and secret-redaction tests pass.
- [ ] External AI disclosure and response-validation controls pass if AI is included.
- [ ] API contract changes are reviewed.
- [ ] Dependencies and known vulnerabilities are reviewed.
- [ ] No unresolved release-blocking defect remains.
- [ ] Known limitations and accepted risks are documented.
- [ ] The release can be installed, started, and diagnosed using the documented procedure.

The absence of a test failure is not, by itself, evidence that every requirement has been satisfied. Release readiness also depends on whether the relevant requirements have actually been tested.

## 19. Acceptance criteria

The testing and validation strategy is ready for the first usable release when:

1. The project has a documented test structure and execution procedure.
2. Core domain and application rules have automated tests.
3. Source adapters have contract and integration tests against supported formats.
4. Persistence, migration, backup, and recovery behavior are tested.
5. Ingestion preserves the last-known-good state under tested failures.
6. Evidence classifications and provenance rules have explicit expected outcomes.
7. Deterministic analysis is reproducible for fixed inputs and rule versions.
8. External AI output is structurally validated and cannot automatically approve decisions.
9. Security and privacy controls have automated negative tests.
10. The primary discovery-to-report workflow has an end-to-end test.
11. CI runs the agreed required test suite and reports failures clearly.
12. Test fixtures use synthetic or explicitly approved data.
13. Release gates and accepted risks are documented.
14. Test results do not overstate the scope of what was verified.

## 20. Implementation sequence

### Phase 1 — Test foundation

- Select the test framework and test-runner conventions.
- Establish isolated test configuration and temporary database fixtures.
- Create representative synthetic source fixtures.
- Implement unit and API contract tests.
- Integrate the fast test suite into CI.

### Phase 2 — Persistence and ingestion

- Test migration sequences and repository constraints.
- Implement failure-injection tests for ingestion.
- Verify snapshot publication and checkpoint consistency.
- Test backup and restoration.

### Phase 3 — Source and analysis validation

- Add adapter-specific contract tests.
- Validate schema and identity handling.
- Add golden datasets for evidence classification.
- Test deterministic rules and historical comparisons.

### Phase 4 — Security and external AI

- Add authorization and filesystem security tests.
- Verify secret redaction and data-disclosure controls.
- Add external AI response validation and prompt-injection test cases.
- Verify that provider failure does not affect deterministic analysis.

### Phase 5 — End-to-end and release assurance

- Implement the discovery-to-report scenario.
- Add frontend automation when the desktop client exists.
- Validate installation, startup, diagnostics, and recovery.
- Establish release gates and document accepted risks.

This sequence is provisional and should be aligned with the actual first-release scope.

## 21. Open questions

| ID | Question | Why it matters |
|---|---|---|
| TV-001 | Which Python test framework and supporting libraries should be selected? | Establishes test conventions and fixtures. |
| TV-002 | Which frontend and desktop automation tools will be used? | Determines end-to-end coverage after UI implementation. |
| TV-003 | Which source formats and schema versions are officially supported in the first release? | Defines adapter test coverage. |
| TV-004 | What synthetic fixture dataset represents a realistic initial portfolio? | Makes tests repeatable and representative. |
| TV-005 | Which performance targets and reference hardware should be used? | Enables meaningful performance acceptance criteria. |
| TV-006 | Which database upgrade paths must be supported? | Determines migration-test coverage. |
| TV-007 | Which security tests are mandatory release gates? | Defines minimum security assurance. |
| TV-008 | How should external AI evaluation datasets and scoring criteria be maintained? | Enables controlled evaluation across provider or model changes. |
| TV-009 | Which tests must run on every change, and which can run on a schedule? | Balances feedback speed and test depth. |
| TV-010 | What evidence is required to mark a requirement as verified? | Establishes traceability between requirements, tests, and validation results. |
| TV-011 | Which test and diagnostic artifacts may be retained, and for how long? | Affects privacy, reproducibility, and storage. |
| TV-012 | How will test results be ingested from external CI/CD systems, if required? | Defines the boundary between local tests and external verification evidence. |

## 22. Relationship to other documents

This document defines the validation strategy. It must be reconciled with:

- `vision.md` — intended outcomes and success criteria.
- `functional-requirements.md` — required system behavior.
- `non-functional-requirements.md` — performance, reliability, and security targets.
- `domain-model.md` and `data-model.md` — entity and relationship invariants.
- `system-architecture.md` — component boundaries.
- `api-design.md` — API contract and error behavior.
- `persistence-and-migrations.md` — storage and migration correctness.
- `configuration-and-secrets.md` — configuration and credential handling.
- `security-and-privacy.md` — threat model and security requirements.
- `source-integration.md` — adapter contracts.
- `vyasa-integration.md` — project inventory validation.
- `openspec-integration.md` — requirements and change-artifact validation.
- `okf-integration.md` — knowledge package validation.
- `git-evidence.md` — repository evidence.
- `ingestion-and-snapshots.md` — ingestion consistency.
- `deterministic-analysis.md` — rule correctness and reproducibility.
- `external-analysis.md` — AI response validation and advisory boundaries.

OpenSpec requirements should define testable behavioral obligations where appropriate. OKF should retain reusable testing knowledge, validation patterns, and engineering rationale independently of the current requirement set.

## 23. Review status

This document establishes a proposed validation baseline. It does not claim that any test suite, CI pipeline, security assessment, or release gate has already been implemented.

Before implementation, prioritize the test foundation, the discovery-to-report workflow, ingestion failure recovery, and deterministic analysis fixtures. These give Siddhi a reliable foundation before adding the full set of integrations and optional AI-assisted capabilities.






