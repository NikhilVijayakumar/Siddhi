# Application Workflows

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `application-workflows.md`  
**Status:** Draft for review  
**Scope:** User-facing and system-level workflows for the Siddhi API and future desktop application.

---

## 1. Purpose

This document describes the principal workflows through which Siddhi discovers project information, maintains portfolio goals, evaluates evidence, supports planning, and helps users make strategic decisions.

It defines:

- Workflow triggers and prerequisites.
- The sequence of operations.
- The information created or updated.
- Expected outcomes and failure handling.
- Human approval boundaries.
- The relationship between deterministic processing and external AI analysis.

It does not define the complete API contract, screen designs, database schema, or implementation details of individual source adapters.

## 2. Workflow principles

### 2.1 Deterministic processing by default

Source discovery, parsing, normalization, deduplication, snapshot comparison, evidence extraction, and routine reporting should use deterministic processing wherever practical.

External AI may support complex interpretation and strategic judgment, but should not be required for ordinary source ingestion or basic portfolio reporting.

### 2.2 Explicit user intent for material decisions

Creating a draft, generating an assessment, or receiving a recommendation must not automatically approve a portfolio decision.

Material changes to priorities, approved plans, and strategic decisions require an explicit action by an authorized user.

### 2.3 Source systems remain authoritative

Siddhi reads information from Vyasa, OpenSpec, OKF, Git, and verification sources without silently changing their records.

Source changes must be performed in the relevant authoritative system unless a separately approved write integration is introduced.

### 2.4 Partial success must remain visible

A workflow may succeed for some sources and fail for others.

Siddhi should preserve successful results, report incomplete coverage, and allow failed stages to be retried without duplicating prior records or erasing historical information.

### 2.5 Historical context must be preserved

A workflow that changes a plan, assessment, priority, or decision must preserve the previous state where the change affects historical interpretation.

A refreshed report should not silently replace the context of a previously approved decision.

### 2.6 Workflows must be proportionate

Siddhi should support a lightweight path for individual projects and goals as well as more involved portfolio reviews.

It must not require every goal to pass through the same number of stages, use the same lifecycle, or adopt a formal approval process that is unnecessary for its scope.

---

## 3. Workflow catalogue

| ID | Workflow | Primary outcome |
|---|---|---|
| WF-001 | Initial application setup | Siddhi is ready to use |
| WF-002 | Configure a source system | A source can be accessed within defined permissions |
| WF-003 | Discover and refresh projects | Current project inventory and source observations are available |
| WF-004 | Ingest engineering information | OpenSpec, OKF, Git, and verification evidence are captured |
| WF-005 | Create and refine a goal | A portfolio goal and intended outcomes are recorded |
| WF-006 | Connect goals to projects and evidence | Portfolio relationships are established |
| WF-007 | Assess goal progress | A traceable evidence-based assessment is produced |
| WF-008 | Generate a portfolio report | Current findings and uncertainty are summarized |
| WF-009 | Create or revise a plan | A proposed or approved plan is recorded |
| WF-010 | Conduct a portfolio review | Progress, risks, assumptions, and decisions are reviewed |
| WF-011 | Request external strategic analysis | AI-assisted recommendations are returned with provenance |
| WF-012 | Approve or reject a recommendation | An explicit decision and rationale are recorded |
| WF-013 | Refresh and compare historical state | Changes since a previous observation are explained |
| WF-014 | Handle source or processing failures | Errors are visible and recovery is controlled |
| WF-015 | Archive or retire portfolio records | Records are removed from active work without losing necessary history |
| WF-016 | Export or back up Siddhi data | Portfolio records and history can be preserved or transferred |

The catalogue is a logical inventory. Not every workflow must be implemented in the first release.

## 4. WF-001 — Initial application setup

**Trigger:** First application launch or creation of a new Siddhi data store.

**Primary actor:** User.

### Main flow

1. Siddhi checks whether its local configuration and data store are initialized.
2. If required, Siddhi creates the initial database and applies schema migrations.
3. Siddhi validates the application configuration.
4. Siddhi initializes the default source-adapter registry.
5. Siddhi checks the availability of required local services and storage.
6. Siddhi presents the user with the current readiness status and any configuration tasks.
7. The user configures source connections and begins discovery when ready.

### Expected result

Siddhi is initialized and ready for configuration without requiring every external source to be available.

### Failure handling

- Database initialization or migration failures must be reported clearly.
- Existing user data must not be overwritten during ordinary initialization.
- Optional source failures must not prevent unrelated local planning functions from operating.
- Repeated initialization must not create duplicate default records.

---

## 5. WF-002 — Configure a source system

**Trigger:** The user adds, changes, enables, disables, or tests a source connection.

**Primary actor:** User.

### Main flow

1. The user selects a supported source type.
2. Siddhi collects the minimum configuration needed for that source.
3. Credentials, if required, are stored through the approved credential mechanism rather than embedded in ordinary source metadata.
4. Siddhi validates the configuration format.
5. Siddhi performs a read-only connection or permission check, where supported.
6. Siddhi records the result, supported capabilities, and any limitations.
7. The user chooses whether to enable the source for discovery or refresh.

### Expected result

Siddhi has a source configuration with a known or explicitly unverified access status.

### Failure handling

- Invalid configuration must be distinguished from authentication failure and source unavailability.
- A failed test must not be represented as a successful connection.
- Credentials must not appear in logs or error messages.
- Disabling a source must not delete its historical observations.
- A successful connection test does not prove that all relevant records are accessible.

---

## 6. WF-003 — Discover and refresh projects

**Trigger:** The user requests discovery or a configured refresh process starts.

**Primary actor:** User or scheduled process.

**Primary source:** Vyasa.

### Main flow

1. Siddhi creates an ingestion run with its requested scope and start time.
2. The Vyasa adapter reads the available project inventory.
3. Siddhi validates the response and records the scan's coverage and errors.
4. Project identities are resolved using stable source identifiers where available.
5. New project references are created where no matching identity exists.
6. Existing references are updated with newly observed metadata.
7. Previous observations are retained according to the snapshot policy.
8. Siddhi compares the new observations with the previous known state.
9. Changes, missing records, unresolved identities, and incomplete coverage are recorded.
10. The ingestion run is marked successful, partially successful, or failed according to the actual outcome.

### Expected result

The user can inspect the discovered projects and understand which records are new, changed, unavailable, or unresolved.

### Important rules

- Discovery must not require checking out repositories unless a separately defined adapter explicitly needs local repository access.
- A project missing from a partial scan must not be marked deleted.
- A changed project name or repository location must not automatically create a duplicate project.
- Project metadata changes must not silently alter existing strategic decisions.
- Source inventory completeness must not be assumed without evidence.

---

## 7. WF-004 — Ingest engineering information

**Trigger:** A project is selected for a deeper scan, or a configured refresh includes engineering sources.

**Primary actor:** User or processing workflow.

**Potential sources:** OpenSpec, OKF, Git, and verification artifacts.

### Main flow

1. Siddhi resolves the project reference and applicable source locations.
2. It determines which source adapters are available and authorized.
3. Each adapter reads the information within its configured scope.
4. The adapter records its ingestion status and coverage.
5. Siddhi captures source observations and applicable version or revision information.
6. Source content is normalized into Siddhi's internal representation.
7. The system creates or updates source-artifact references using identity-resolution rules.
8. New observations are compared with previously captured observations.
9. Evidence candidates are extracted using deterministic rules.
10. Provenance is attached to each observation and derived evidence record.
11. Data-quality issues and processing errors are recorded.
12. The workflow produces an ingestion summary.

### Expected result

Siddhi has a traceable, time-bounded view of the engineering information that was successfully observed.

### Important rules

- OpenSpec and OKF are ingested independently.
- Missing OKF knowledge must not invalidate an OpenSpec requirement.
- Missing OpenSpec requirements must not invalidate OKF knowledge.
- A declared task status must not be treated as proof of working implementation.
- A detected file or keyword must not automatically establish that a goal is satisfied.
- Source content must not be modified during ingestion.

### Partial success

If OpenSpec ingestion succeeds but OKF ingestion fails, Siddhi should retain the successful OpenSpec observations and report the missing OKF coverage. It should not report the entire project scan as fully successful.

---

## 8. WF-005 — Create and refine a goal

**Trigger:** The user creates a new portfolio goal or edits an existing one.

**Primary actor:** User.

### Main flow

1. The user creates a goal with a title and description.
2. Siddhi assigns a stable goal identifier.
3. The user may add one or more intended outcomes.
4. For each outcome, the user may define qualitative criteria, measurable targets, a baseline, a target date, or other applicable evidence of success.
5. The user may assign a priority, constraints, assumptions, and related initiatives.
6. Siddhi validates the record and its relationships.
7. The goal and any revisions are persisted.
8. Siddhi identifies whether sufficient information exists to perform an initial assessment.

### Expected result

A goal is recorded with a clear statement of intent and, where available, a way to evaluate progress.

### Important rules

- The model should not require every goal to use a numerical metric.
- A goal may exist before its outcomes and evidence criteria are fully defined.
- An incomplete goal must be identified as needing clarification rather than automatically rejected.
- Editing a goal must not rewrite prior analysis reports.
- Goal status is a declared planning state, not an independently verified result.

---

## 9. WF-006 — Connect goals to projects and evidence

**Trigger:** The user links a goal or initiative to a project, source artifact, or evidence record.

**Primary actor:** User, with optional deterministic suggestions.

### Main flow

1. The user selects a goal or initiative.
2. Siddhi presents available project references and relevant source artifacts.
3. The user selects the intended relationship.
4. Siddhi validates the referenced identities and permitted relationship type.
5. The user may record a rationale describing how the project or artifact contributes to the goal.
6. Siddhi persists the relationship with provenance and creation time.
7. Relevant existing evidence becomes available to subsequent assessments.

### Expected result

The portfolio model links strategic intentions to relevant projects and evidence.

### Important rules

- A project may link directly to a goal without an initiative.
- One project may contribute to multiple goals.
- A relationship expresses relevance or contribution, not proof of achievement.
- Automatically suggested links remain candidates until accepted when a human decision is required.
- Removing a relationship must not delete the underlying project or evidence.

---

## 10. WF-007 — Assess goal progress

**Trigger:** The user requests an assessment, or a configured workflow runs an assessment after relevant evidence changes.

**Primary actor:** User or deterministic analysis process.

### Main flow

1. Siddhi identifies the goal, its applicable outcomes, and relevant assessment criteria.
2. It selects available evidence within the configured scope.
3. It checks the evidence's provenance, freshness, completeness, and known limitations.
4. It applies the relevant deterministic assessment rules.
5. It records the analysis run and its input references.
6. It produces an assessment for each applicable outcome or criterion.
7. It identifies supported findings, contradictory observations, and missing evidence.
8. It persists the new assessment and links it to the relevant analysis run.
9. It compares the new assessment with the previous assessment where available.
10. It presents the result, supporting evidence, limitations, and changes.

### Expected result

The user receives a traceable assessment of what the available evidence supports, what remains uncertain, and what needs further investigation.

### Important rules

- Insufficient evidence must not automatically mean failure.
- A successful build or test does not automatically prove that a strategic outcome is achieved.
- A change in assessment must be explainable through changed inputs, criteria, or analysis logic.
- A new assessment must not overwrite the historical basis of an earlier decision.
- External AI is not required for routine evidence evaluation.

### Assessment boundary

Siddhi may report that evidence supports an outcome, but declaring a goal achieved should follow an explicit policy appropriate to that goal. A user may need to confirm completion when the outcome requires human judgment.

---

## 11. WF-008 — Generate a portfolio report

**Trigger:** The user requests a report for a goal, initiative, project group, or the portfolio as a whole.

**Primary actor:** User.

### Main flow

1. The user selects the report scope.
2. Siddhi identifies the relevant current goals, plans, source observations, evidence, assessments, and decisions.
3. It determines whether the available information is sufficiently current for the requested report.
4. It runs any required deterministic analysis that has not already been performed for the same inputs and rules.
5. It assembles the relevant findings, milestones, risks, gaps, dependencies, and unresolved questions.
6. It identifies stale, missing, conflicting, or incomplete source information.
7. It produces a report with generation time and provenance.
8. It persists the report or its historical representation.
9. It presents the report to the user.

### Expected result

A report provides a coherent view of portfolio status without obscuring data limitations.

### Report requirements

A report should distinguish:

- Declared status from assessed status.
- Source observations from derived findings.
- Confirmed information from inferred or candidate information.
- Missing information from negative evidence.
- Recommendations from approved decisions.
- Current observations from historical snapshots.

A report must not claim that all sources are current when some sources failed or were not scanned.

---

## 12. WF-009 — Create or revise a plan

**Trigger:** The user creates a plan or decides to change an existing approach.

**Primary actor:** User.

### Main flow

1. The user selects the goal or initiative the plan supports.
2. Siddhi records the proposed approach and relevant assumptions.
3. The user may define milestones, target dates, dependencies, and completion criteria.
4. Siddhi validates relationships and identifies obvious structural issues, such as invalid references.
5. The plan is stored as a draft or proposed revision.
6. Where required by the configured governance policy, an authorized user reviews the revision.
7. The user explicitly approves, rejects, or leaves the revision pending.
8. Siddhi records the outcome and rationale.
9. The active plan revision is updated only according to the applicable approval rules.

### Expected result

A plan or plan revision is recorded with its intended scope, milestones, and status.

### Important rules

- Plan revisions must preserve relevant previous versions.
- Changing a target date must not erase the prior target date from historical records.
- An overdue milestone is a planning observation, not proof that the underlying outcome has failed.
- Approval requirements should be proportionate to the scope of the plan.
- Updating a Siddhi plan must not modify external source systems.

---

## 13. WF-010 — Conduct a portfolio review

**Trigger:** The user initiates a review or a planned review becomes due.

**Primary actor:** User or authorized reviewer.

### Main flow

1. The user selects the review scope.
2. Siddhi assembles the latest available reports, assessments, plan revisions, milestones, dependencies, assumptions, and prior decisions.
3. It identifies stale data and unresolved findings.
4. The user examines progress, evidence gaps, risks, constraints, and trade-offs.
5. The user records review observations and any corrections.
6. The user may propose changes to goals, priorities, plans, or dependencies.
7. Siddhi records those proposals separately from approved changes.
8. Authorized users explicitly approve or reject material decisions.
9. Siddhi records the review, decision outcomes, rationale, and relevant report references.

### Expected result

The review produces a durable record of what was considered, what was decided, and what remains unresolved.

### Important rules

- A review must retain references to the information considered.
- A later refresh must not rewrite the historical review.
- Recommendations generated during the review must remain distinct from the resulting decisions.
- Not every finding needs a formal decision.
- A review may conclude that additional evidence is required before any decision can be made.

---

## 14. WF-011 — Request external strategic analysis

**Trigger:** The user explicitly requests AI-assisted analysis for a defined strategic question.

**Primary actor:** User.

**Potential uses:** Prioritization, opportunity analysis, trade-offs, minimum viable release definition, internal investment justification, and strategic risk assessment.

### Main flow

1. The user identifies the question and scope.
2. Siddhi assembles relevant portfolio records and evidence references.
3. It identifies the information that would be sent to the external service.
4. The configured data-handling policy is applied, including any required confirmation or redaction.
5. Siddhi records the request context and analysis configuration.
6. The external AI service is invoked.
7. Siddhi records the response and its provenance.
8. The response is parsed into structured recommendations where possible.
9. Recommendations are linked to supporting evidence or marked as requiring verification.
10. The user reviews the results and may request clarification or further analysis.

### Expected result

The user receives a structured strategic analysis that is distinguishable from verified facts and approved decisions.

### Important rules

- AI must not be required for routine ingestion and reporting.
- A recommendation must not automatically change portfolio priorities or plans.
- Claims about source facts should be traceable to evidence when possible.
- Unsupported model-generated claims must remain identifiable as unverified.
- Sensitive source information must not be sent contrary to the configured data-handling policy.
- External service failure must not destroy locally stored portfolio data or previous results.

---

## 15. WF-012 — Approve or reject a recommendation

**Trigger:** The user reviews a recommendation and decides whether to act on it.

**Primary actor:** Authorized user.

### Main flow

1. Siddhi presents the recommendation, rationale, supporting evidence, and limitations.
2. The user reviews the proposal.
3. The user accepts, rejects, defers, or requests further investigation.
4. Siddhi records the explicit decision, responsible person or authority, timestamp, and rationale.
5. If accepted, the user identifies the resulting action or approved plan revision where applicable.
6. Siddhi links the decision to the recommendation and affected portfolio records.
7. The system preserves earlier decisions and records supersession or reversal when necessary.

### Expected result

The portfolio contains an explicit decision and a traceable relationship to the recommendation that informed it.

### Important rules

- Receiving a recommendation does not imply approval.
- Opening or viewing a recommendation does not imply approval.
- A recommendation's status and a decision's status are separate.
- The system must not represent an external AI provider as the decision-maker.
- If a decision is reversed, the original decision and its rationale remain available according to the retention policy.

---

## 16. WF-013 — Refresh and compare historical state

**Trigger:** The user requests a refresh or a configured refresh process runs.

**Primary actor:** User or scheduled process.

### Main flow

1. Siddhi identifies the requested sources and scope.
2. It records a new refresh or ingestion job.
3. Source adapters obtain available information.
4. New source observations and snapshots are recorded.
5. Siddhi compares the new observations with the applicable previous snapshots.
6. It identifies additions, modifications, missing records, identity changes, and unresolved differences.
7. Where configured, it reruns affected deterministic analyses.
8. New assessments and findings are linked to their inputs.
9. Siddhi compares the new results with historical assessments and reports.
10. It presents changes, unchanged areas, uncertainty, and failures.

### Expected result

The user can understand what changed since the previous observation and whether that change affects portfolio interpretation.

### Important rules

- A refresh must not erase historical snapshots.
- A changed source record must not automatically change an approved decision.
- A missing record must be distinguished from an inaccessible or incomplete source where possible.
- Only affected analyses should be rerun when the system can reliably identify their dependencies; otherwise, broader analysis may be necessary.
- A new result should identify the analysis and normalization versions used.

---

## 17. WF-014 — Handle source or processing failures

**Trigger:** A source becomes unavailable, access fails, input is invalid, processing fails, or an external service returns an error.

**Primary actor:** System, with user intervention when necessary.

### Main flow

1. Siddhi captures the error category, relevant scope, timestamp, and safe diagnostic details.
2. It identifies which workflow stage failed.
3. Successfully completed stages remain recorded.
4. The workflow is marked successful, partially successful, failed, or cancelled as appropriate.
5. Siddhi identifies whether the failure is recoverable.
6. Where safe, the user or configured process may retry the failed stage.
7. Retry operations reuse stable identities and idempotent processing rules.
8. The system records the retry and its outcome.
9. Reports affected by the failure disclose incomplete or stale coverage.

### Expected result

The user can determine what failed, what succeeded, and whether a retry or corrective action is needed.

### Important rules

- Errors must not silently convert missing information into negative evidence.
- Retrying must not create duplicate goals, source artifacts, evidence, or decisions.
- Credentials and sensitive payloads must not be exposed in diagnostics.
- A failed analysis must not overwrite the last successful report as though it were a new valid result.
- A recovery attempt must not modify source repositories or artifacts unless separately authorized.

---

## 18. WF-015 — Archive or retire portfolio records

**Trigger:** The user decides that a goal, initiative, plan, or other portfolio record is no longer active.

**Primary actor:** Authorized user.

### Main flow

1. The user selects the record to archive or retire.
2. Siddhi identifies relevant active relationships and unresolved dependencies.
3. The system explains any material consequences, such as an initiative still linked to active goals.
4. The user confirms the action where confirmation is required.
5. Siddhi records the archival or retirement event.
6. The record is excluded from applicable active views.
7. Historical evidence, decisions, and reports remain accessible according to policy.

### Expected result

The record is no longer treated as active while its relevant history remains available.

### Important rules

- Archiving a Siddhi record does not delete the external project or source artifact.
- Archiving must not automatically archive all linked records.
- The system must not infer that a goal failed merely because it was retired.
- Hard deletion and retention-policy deletion are separate operations with explicit rules.

---

## 19. WF-016 — Export or back up Siddhi data

**Trigger:** The user requests a backup, export, or transfer of portfolio information.

**Primary actor:** Authorized user or administrator.

### Main flow

1. The user selects the export scope and intended format.
2. Siddhi identifies the included domain records, relationships, history, and source references.
3. The export process applies privacy and sensitive-data exclusions.
4. Siddhi generates an export manifest with format/version information.
5. The export includes sufficient identifiers and relationship information to preserve internal consistency.
6. Siddhi validates the generated artifact to the extent practical.
7. The user receives the export result and any limitations.

### Expected result

The user obtains a portable representation of Siddhi data with clear scope and format information.

### Important rules

- Exports must distinguish Siddhi-owned records from references or copies of external data.
- Credentials and secrets must be excluded.
- A portfolio export does not imply that external source records have been backed up.
- Restore behavior, when supported, must validate the export format and avoid silently overwriting existing data.

The exact formats, restore workflow, and backup strategy remain to be decided.

---

## 20. Workflow coordination and dependencies

### 20.1 Workflow composition

A workflow may call smaller operations, but each operation should have a clear responsibility and observable result.

For example, a project refresh may invoke source ingestion, normalization, evidence extraction, and deterministic analysis. These should remain distinguishable stages rather than one opaque operation.

### 20.2 Idempotency

Operations that may be retried should define their idempotency behavior.

Repeated execution against unchanged source inputs should not create duplicate logical identities or duplicate decisions.

An intentional new analysis run may create a new historical record even when the result is unchanged. That is different from accidentally duplicating the underlying evidence.

### 20.3 Partial completion

Multi-stage workflows should preserve completed stages where safe.

A failure in external AI analysis must not invalidate successfully captured source evidence. A failure in one source adapter must not erase successful results from another adapter.

### 20.4 Concurrency

The implementation must define how concurrent edits and refresh operations are handled.

At minimum:

- A refresh must not silently overwrite a user's newer edits to a Siddhi-owned record.
- Concurrent updates to a plan or decision must be detectable.
- The system should prevent conflicting operations from corrupting persisted state.
- Long-running operations must expose their status.

The exact locking, optimistic concurrency, and job execution mechanisms are implementation decisions.

### 20.5 Background execution

Short, local operations may run synchronously. Longer source scans and analysis tasks may run as background jobs when justified by measured runtime or user experience.

Background execution should not be introduced solely for architectural complexity. The first implementation should use the simplest approach that meets responsiveness and reliability requirements.

---

## 21. Workflow observability

Each material workflow should expose enough information to understand its outcome.

Where applicable, the workflow result should include:

- Workflow or job identifier.
- Requested scope.
- Start and completion timestamps.
- Overall status.
- Successful and failed stages.
- Sources accessed and sources skipped.
- Records discovered, processed, or rejected.
- Relevant data-quality warnings.
- Links to generated snapshots, evidence, reports, or decisions.
- Safe error information and recovery guidance.

Operational logs and user-facing summaries serve different purposes. Logs support diagnosis; workflow summaries explain outcomes in terms users can act upon.

Neither should disclose secrets or unnecessarily reproduce sensitive source content.

---

## 22. First usable release workflow priorities

The first usable release should focus on the smallest complete path that delivers meaningful portfolio intelligence.

### Priority 1 — Essential path

1. Initialize Siddhi and its local data store.
2. Configure and test a Vyasa source.
3. Discover and refresh project references.
4. Create a goal and intended outcome.
5. Link the goal directly to one or more discovered projects.
6. Ingest available OpenSpec, OKF, and Git information for the selected scope.
7. Store source observations with provenance.
8. Generate deterministic findings and an evidence-based assessment.
9. Produce a report that distinguishes supported findings, gaps, conflicts, stale information, and unknowns.
10. Refresh the sources and compare results with a previous observation.

### Priority 2 — Planning and governance

- Create and revise plans.
- Maintain milestones and dependencies.
- Record portfolio reviews.
- Preserve decisions and their rationale.
- Support recommendation approval and rejection.

### Priority 3 — External strategic analysis

- Prepare bounded, traceable analysis requests.
- Apply the approved data-handling policy.
- Store external responses and recommendations.
- Allow the user to review the output and record an explicit decision.

### Priority 4 — Operational maturity

- Scheduled refreshes where justified.
- Expanded retry and recovery controls.
- Backup and export.
- Advanced history retention and configurable assessment criteria.
- Desktop application integration.

These priorities are proposed for review, not a commitment that all items in a priority group must be delivered together.

---

## 23. Open questions

| ID | Question | Impact |
|---|---|---|
| AW-001 | Which operations must require explicit user confirmation in the first release? | Determines approval boundaries |
| AW-002 | Should source refreshes be manual-only initially, or should scheduled refreshes be available from the first release? | Affects scheduling and operations |
| AW-003 | Which assessment steps can run automatically after ingestion, and which require a user request? | Controls processing scope and resource use |
| AW-004 | Should a goal require an explicit completion confirmation even when its outcomes are fully supported by evidence? | Defines completion semantics |
| AW-005 | Which portfolio review types are needed initially, if any? | Prevents unnecessary governance complexity |
| AW-006 | What is the required recovery behavior after partial ingestion or a database/application failure? | Affects job persistence and recovery design |
| AW-007 | Which backup and export formats are required for the first usable release? | Affects portability and testing |
| AW-008 | Which operations need optimistic concurrency protection in the first release? | Affects data integrity |
| AW-009 | Should external AI analysis be available only on explicit request, or also through user-configured workflows? | Affects consent and automation |
| AW-010 | Which workflow status vocabulary should be shared across ingestion, analysis, and reporting? | Improves consistency without forcing unrelated entities into identical lifecycles |

These questions should be resolved during design review. Until then, workflows should default to read-only source access, deterministic processing, explicit approval for material decisions, and visible reporting of incomplete results.

---

## 24. Relationship to other documents

- `vision.md` defines why Siddhi exists and the outcomes it seeks to support.
- `scope-and-roadmap.md` defines boundaries and delivery phases.
- `functional-requirements.md` defines required observable behavior.
- `non-functional-requirements.md` defines quality and operational constraints.
- `system-architecture.md` defines component responsibilities and execution boundaries.
- `architectural-decisions.md` records proposed and accepted design decisions.
- `domain-model.md` defines the concepts and their relationships.
- `data-ownership.md` defines source authority and permitted data handling.
- `data-model.md` defines the logical persisted entities and relationships.
- `scanning-and-evidence.md` defines source discovery and evidence derivation.
- `synchronization.md` defines refresh and change-detection behavior.
- `security-and-privacy.md` defines access, credentials, and data protection.

During the later review phase, the workflows should be checked against the domain and data models. Testable behavior should then be expressed in OpenSpec requirements, while reusable workflow principles and technical knowledge should be captured in OKF independently.

---

**End of document**