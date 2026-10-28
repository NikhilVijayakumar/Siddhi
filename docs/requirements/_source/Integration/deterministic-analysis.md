# Deterministic Analysis

**Document:** `deterministic-analysis.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Rule-based, reproducible analysis of portfolio data, source snapshots, evidence, plans, and progress indicators

**Related documents:** `vision.md`, `functional-requirements.md`, `non-functional-requirements.md`, `domain-model.md`, `data-model.md`, `data-ownership.md`, `ingestion-and-snapshots.md`, `source-integration.md`, `vyasa-integration.md`, `openspec-integration.md`, `okf-integration.md`, `git-evidence.md`, `application-workflows.md`

---

## 1. Purpose

This document defines how Siddhi performs deterministic analysis of portfolio information.

Siddhi ingests information from multiple independent sources and maintains portfolio-specific records, including goals, initiatives, plans, milestones, decisions, and assessments. Deterministic analysis evaluates this information using explicit rules to produce reproducible findings and reports.

The analysis engine should help answer questions such as:

- Which goals have no associated initiatives?
- Which initiatives have no defined intended outcome?
- What evidence is available for a goal?
- Which evidence sources have not been refreshed recently?
- Which goals have missing, conflicting, stale, or unverified evidence?
- Which milestones are overdue according to the current approved plan?
- Which dependencies remain unresolved?
- Which projects have changed since the previous portfolio review?
- Which requirements are declared complete but lack corresponding verification evidence?
- Which plans have changed since the last review?
- What changed in the portfolio between two recorded snapshots?
- Which assessments need to be revisited because their supporting evidence changed?

The engine must make these results explainable by preserving the rules, inputs, scope, and source references used to produce them.

## 2. Core principles

### 2.1 Deterministic by default

Given the same normalized input data, applicable rules, configuration, and analysis version, the engine should produce the same logical findings.

Routine analysis must not require an external AI service.

### 2.2 Explicit rules over hidden assumptions

Rules must be documented and testable. The engine must not invent thresholds, infer missing values, or treat conventions as mandatory policies unless those rules are explicitly configured.

### 2.3 Findings are not decisions

A finding describes an observation or a result derived from defined rules.

A recommendation proposes an action or interpretation.

A decision records an approved choice by an authorized person or process.

These are separate entities and lifecycle stages.

### 2.4 Source declarations are not independent proof

The engine must preserve the difference between:

- What a source declares.
- What Siddhi observes.
- What deterministic rules derive.
- What independent verification establishes.
- What remains uncertain.

For example, an OpenSpec task marked complete is a source-declared status. It is not proof that the associated software works.

### 2.5 Preserve historical context

Analysis must be traceable to the source snapshots and portfolio revisions used when it ran.

A later source refresh must not silently change the historical explanation for an earlier report.

### 2.6 Avoid false precision

The engine must not manufacture a single universal progress percentage or health score when the underlying data does not support a meaningful comparison.

Different goals may have different success criteria, maturity expectations, and evidence requirements.

---

## 3. Scope

### 3.1 Included

The deterministic analysis engine covers:

1. Portfolio structure and relationship checks.
2. Evidence coverage and classification.
3. Source freshness and ingestion health.
4. Plan, milestone, and dependency checks.
5. Source change detection and historical comparisons.
6. Goal-specific progress indicators based on explicit criteria.
7. Data quality and consistency checks.
8. Evidence sufficiency rules where acceptance criteria are defined.
9. Findings, report generation, and traceability.
10. Identification of assessments that need refreshing.
11. Reproducible analysis runs and historical result comparison.
12. Export of findings for optional external AI analysis.

### 3.2 Excluded

The deterministic engine does not:

- Replace the authoritative source systems.
- Infer business value from commit counts or lines of code.
- Automatically approve recommendations.
- Automatically change priorities or plans.
- Make subjective strategic judgments without explicit rules.
- Require all goals to share the same lifecycle or maturity stages.
- Require mandatory time tracking.
- Treat missing information as a negative result without a defined rule.
- Treat source ingestion success as proof that the source content is correct.
- Use an LLM to perform routine comparisons or counting.
- Claim that a goal has been achieved without evaluating its applicable acceptance criteria.

---

## 4. Architectural position

The deterministic analysis engine sits between normalized portfolio data and the reports or workflows that consume analysis results.

```text
External Sources
      |
      v
Ingestion and Snapshots
      |
      v
Normalized Source Records
      |
      +----------------------+
      |                      |
      v                      v
Portfolio Domain       Source Evidence
      |                      |
      +----------+-----------+
                 |
                 v
       Analysis Input Resolver
                 |
                 v
        Deterministic Rules
                 |
                 v
       Findings and Assessments
                 |
                 v
         Analysis Report
                 |
        +--------+---------+
        |                  |
        v                  v
 Portfolio Reviews    Optional External AI
        |
        v
 Human Decision and Approval
```

The analysis engine should be a module within Siddhi's initial modular monolith. It should not be a separate microservice unless later scale, deployment, or operational requirements justify that separation.

### 4.1 Analysis input resolver

The resolver identifies the data required for an analysis run.

It must establish:

- The portfolio entities in scope.
- The relevant source snapshots.
- The applicable plan and decision revisions.
- The rules and configuration to use.
- The time reference for date-dependent rules.
- The known limitations of the input data.

The resolver must not silently substitute a newer snapshot into a historical analysis.

### 4.2 Rule engine

The rule engine evaluates normalized inputs using explicit, versioned rules.

Rules may be implemented as ordinary Python functions, declarative configuration, or a combination of the two. The initial implementation should favor straightforward, testable code rather than introducing a general-purpose rules platform prematurely.

### 4.3 Finding and report generator

The result generator records findings, supporting evidence references, rule identifiers, severity, uncertainty, and relevant limitations.

Reports should be generated from persisted analysis results rather than recomputing different results whenever a user opens an old report.

---

## 5. Analysis run model

Every analysis execution must have a stable analysis run ID.

### 5.1 Run metadata

An analysis run should record:

- Run ID.
- Analysis type.
- Start and completion times.
- Portfolio scope.
- Relevant source snapshot IDs.
- Goal, initiative, or plan revisions used.
- Rule-set version.
- Analysis implementation version.
- Configuration revision.
- Reference time used for date-dependent rules.
- Completion status.
- Findings generated.
- Warnings and errors.
- Input limitations.

The record should distinguish between the time the analysis ran and the time represented by its inputs.

### 5.2 Run statuses

The engine should support:

- **Succeeded:** the requested analysis completed for its declared scope.
- **Partially succeeded:** results were generated, but some inputs or sub-analyses were unavailable.
- **Failed:** the engine could not produce a usable result.
- **Cancelled:** execution was intentionally stopped.

A successful run may still contain findings that indicate missing or conflicting evidence. Run status describes the execution, not the health of the portfolio.

### 5.3 Reproducibility

For the same logical inputs, rule version, configuration, and reference time, the engine should produce equivalent findings.

Generated timestamps and run identifiers may differ between executions. They must not affect the logical comparison of results.

If a rule depends on the current date, the reference date must be an explicit input. Historical reruns must use the original reference date when the objective is to reproduce the original assessment.

---

## 6. Rule categories

The initial rule library should be organized by purpose.

| Category | Purpose |
|---|---|
| Portfolio integrity | Identify missing or inconsistent portfolio relationships |
| Evidence coverage | Identify whether expected evidence is available |
| Evidence quality | Assess provenance, verification, and limitations |
| Source freshness | Identify evidence that may be outdated |
| Plan consistency | Detect conflicts or missing information in plans |
| Milestone monitoring | Evaluate due dates and completion declarations |
| Dependency analysis | Identify unresolved or blocked dependencies |
| Source change analysis | Summarize changes across source snapshots |
| Goal assessment | Evaluate explicit goal acceptance criteria |
| Data quality | Identify malformed, incomplete, or conflicting records |
| Historical comparison | Compare plans, decisions, evidence, and findings over time |
| Operational integrity | Detect failed ingestion, stale snapshots, or incomplete analysis |

Rules should be independently identifiable and testable. A failure in one non-critical rule should not automatically prevent all other rules from running.

---

## 7. Portfolio integrity analysis

Portfolio integrity rules check whether the portfolio's structure is sufficiently defined for the requested analysis.

Examples include:

- A goal has no intended outcome.
- An initiative has no associated goal.
- A project reference points to a project that can no longer be resolved through Vyasa.
- A milestone references an unknown initiative.
- A dependency references an unknown entity.
- A decision refers to an obsolete plan revision.
- A portfolio mapping points to a source record that has been removed or reidentified.
- A goal has no defined acceptance criteria where the selected assessment requires them.

These conditions are not automatically errors in every context.

For example, an initiative may intentionally exist as exploratory work before being associated with a formal goal. A rule must distinguish between a required relationship and an optional one.

Each rule should define its applicable entity types, prerequisites, and exceptions.

---

## 8. Evidence coverage and quality

### 8.1 Evidence coverage

The engine should determine whether the evidence expected by an explicitly defined assessment is available within the configured scope.

Possible results include:

- Expected evidence is present.
- Expected evidence is absent from a sufficiently inspected scope.
- Evidence is available but cannot be reliably associated with the target.
- Evidence is present but incomplete.
- Evidence is inaccessible.
- Evidence has not been collected.
- Evidence requirements are not defined.

These outcomes must not be collapsed into a simple present/absent flag.

### 8.2 Evidence classifications

The engine should support the shared evidence classifications defined by the broader Siddhi domain model.

| Classification | Meaning |
|---|---|
| Confirmed | Evidence meets the explicit criteria for the stated claim |
| Candidate | Potentially relevant evidence whose association or sufficiency is not established |
| Missing | Expected evidence was not found within a sufficiently covered scope |
| Unknown | Available information is insufficient to determine the state |
| Stale | Evidence may no longer represent the current source state |
| Conflicting | Applicable sources contain inconsistent information |
| Unverified | The required verification standard has not been met |

These classifications describe Siddhi's assessment. They do not overwrite source-declared statuses.

### 8.3 Evidence quality dimensions

Where relevant, the engine should evaluate separate dimensions rather than a single opaque confidence score:

- **Provenance:** Can the evidence be traced to a source?
- **Identity:** Is the source record reliably identified?
- **Freshness:** Is the evidence recent enough for the applicable rule?
- **Coverage:** Was the relevant source scope sufficiently inspected?
- **Verification:** Has the required verification evidence been observed?
- **Consistency:** Does the evidence conflict with other applicable records?
- **Relevance:** Is the association with the goal supported by the defined mapping rules?

The engine must not invent numerical confidence values where no calibrated scoring method exists.

---

## 9. Source freshness and ingestion health

Freshness analysis evaluates whether the information used by a portfolio assessment is sufficiently current for its intended purpose.

The engine may use:

- Last successful ingestion.
- Last successful publication.
- Source revision or observed version.
- Source modification timestamps where trustworthy.
- Source-defined expiry or review dates.
- Time elapsed since the last applicable verification.
- Known failures in recent refresh attempts.

Freshness thresholds must be explicit and appropriate to the source and use case.

For example, the acceptable age of repository metadata may differ from the acceptable age of a production deployment health observation.

### 9.1 Freshness is not correctness

Recent evidence may be incorrect. Old evidence may remain valid.

Freshness rules should report the age and relevant source conditions rather than imply that freshness proves truth.

### 9.2 Unavailable sources

If a refresh fails, the engine should preserve the previous snapshot and classify the current source state as unavailable or stale when applicable.

It must not treat a failed scan as proof that no source records exist.

### 9.3 Assessment invalidation

When a relevant source changes, Siddhi should identify assessments that may need recalculation.

This can be implemented using recorded input dependencies:

- Which snapshots an analysis used.
- Which portfolio revisions it used.
- Which rules were evaluated.
- Which evidence records supported each finding.

A change to an unrelated source should not require every portfolio assessment to be recomputed.

---

## 10. Plan and milestone analysis

Plan analysis evaluates recorded dates, statuses, dependencies, and revisions against explicit rules.

### 10.1 Milestone checks

Possible checks include:

- A milestone's due date has passed and it remains incomplete.
- A milestone is marked complete but required completion evidence is absent.
- A milestone's date changed since the last approved plan revision.
- A dependency remains unresolved when a dependent milestone is due.
- A milestone has no defined completion criteria where such criteria are required.

The engine must distinguish between a recorded status and a verified outcome.

An overdue milestone is a date-based observation. It does not, by itself, establish that the project is failing.

### 10.2 Date semantics

Date-dependent rules must specify:

- The reference date.
- The relevant timezone where timestamps are involved.
- Whether dates are inclusive.
- Which plan revision is authoritative for the assessment.
- Whether the milestone is active, cancelled, archived, or otherwise excluded.

Historical reports must use the original reference date and plan revision to remain explainable.

### 10.3 Plan revisions

When a plan changes, Siddhi should preserve the earlier revision and compare it with the new one.

The engine may identify:

- Milestones added or removed.
- Date changes.
- Dependency changes.
- Changes in declared status.
- Changes in acceptance criteria.
- Changes to intended outcomes or scope.

The engine should report the differences without automatically judging every revision as an improvement or regression.

---

## 11. Dependency analysis

Dependency analysis examines explicit relationships between portfolio entities.

It should support:

- Identifying unresolved dependencies.
- Finding dependencies whose referenced entities cannot be resolved.
- Detecting dependency cycles where the relationship model requires an acyclic graph.
- Identifying downstream entities affected by a known dependency change.
- Reporting dependencies whose evidence is stale or unavailable.
- Distinguishing declared dependencies from inferred candidate relationships.

The engine must not assume all relationship types form an acyclic graph. Cycles may be valid in some knowledge relationships, even if they are invalid in a particular planning dependency model.

Any cycle-detection rule must apply only to relationship types for which cycles are prohibited or require review.

---

## 12. Cross-source consistency analysis

Siddhi brings together information from systems with different authorities. Consistency checks must compare only claims that are meaningfully comparable.

Examples include:

- Vyasa identifies a project as having OpenSpec enabled, but the configured OpenSpec source cannot be accessed.
- An OpenSpec task is declared complete, but no expected verification result is available.
- An OKF concept describes a capability, but the portfolio mapping to the expected project is unresolved.
- Git history shows a relevant change after the snapshot used by a prior assessment.
- A plan references a project that has been removed from the latest sufficiently complete project inventory.
- Two sources declare incompatible lifecycle states for what appears to be the same entity.

### 12.1 Authority-aware comparisons

A disagreement must not automatically be resolved by choosing whichever source was updated most recently.

The applicable source authority must be considered.

For example:

- OpenSpec owns its declared task status.
- Git owns its observed commit history.
- A test system owns its recorded test result.
- Siddhi owns the portfolio assessment derived from those inputs.

The engine should record the conflict and its basis. It must not silently rewrite the source declaration.

### 12.2 Comparison limitations

Before declaring a conflict, the engine must determine whether the two records refer to the same entity, revision, environment, and relevant time period.

Different records may describe different versions or scopes without actually contradicting one another.

---

## 13. Goal-specific progress assessment

Siddhi should assess progress according to each goal's intended outcome and explicit acceptance criteria.

### 13.1 No universal progress formula

The engine must not use a universal progress formula based on:

- Number of commits.
- Lines of code changed.
- Number of documents.
- Number of OpenSpec tasks marked complete.
- Number of milestones marked complete.
- Number of repositories or engineering components created.

Such measures may be useful as activity or coverage indicators, but they do not measure strategic value consistently across different goals.

### 13.2 Rule-based acceptance criteria

Where a goal has explicit, machine-evaluable acceptance criteria, the engine may evaluate them deterministically.

Examples include:

- A required document exists and has passed a specified validation.
- A defined set of required tests has a successful result for a specified revision.
- A required milestone has an approved completion record.
- A specified artifact is present in a sufficiently complete source snapshot.
- A required verification result exists and corresponds to the intended version.

The engine must record which criteria were evaluated, which passed, which failed, and which could not be assessed.

### 13.3 Non-machine-evaluable criteria

Some outcomes require judgment, observation, or human confirmation.

Examples include:

- Whether an internal tool provides sufficient strategic value.
- Whether a capability is genuinely reusable.
- Whether a creative work meets the desired quality.
- Whether a business opportunity is worth further investment.
- Whether an architecture is appropriate for its intended context.

The deterministic engine should identify the evidence relevant to these questions and the criteria that remain unresolved. It should not fabricate an objective answer.

### 13.4 Goal state versus evidence state

Siddhi must keep separate:

- The goal's declared lifecycle status.
- The evidence coverage status.
- The deterministic assessment of defined criteria.
- Any human-approved outcome decision.

These may differ. For example, a goal may remain active even when all currently defined technical criteria pass, because strategic approval or additional acceptance conditions remain outstanding.

---

## 14. Historical comparison and change analysis

The engine should compare selected historical snapshots and portfolio revisions.

Possible comparisons include:

- Source snapshot to source snapshot.
- Portfolio state to portfolio state.
- Plan revision to plan revision.
- Analysis result to analysis result.
- Evidence set before and after a source refresh.
- Findings before and after a rule-set change.

### 14.1 Finding lifecycle

When analysis is repeated, Siddhi should distinguish:

- New findings.
- Findings that remain applicable.
- Findings whose severity or classification changed.
- Findings that are no longer supported by the latest evidence.
- Findings that cannot be reassessed because inputs are unavailable.
- Findings that changed because the rules changed.

A finding disappearing from the latest analysis does not necessarily mean that the underlying issue was resolved. The scope, rule, source coverage, or input data may have changed.

### 14.2 Rule changes

A new rule version may produce different findings even when the source data has not changed.

Reports must preserve the rule version used. Where useful, Siddhi should support comparing results from different rule versions against the same historical inputs.

### 14.3 Historical reproducibility

Historical reports should reference their exact input snapshots, portfolio revisions, configuration, and rules.

If the required historical data has been pruned or is no longer available, Siddhi must report that the analysis cannot be fully reproduced rather than presenting a reconstruction as exact.

---

## 15. Findings and severity

Every finding should have a stable identity or a documented reconciliation strategy.

### 15.1 Logical finding model

A finding should support:

- Finding ID.
- Rule ID and version.
- Analysis run ID.
- Finding category.
- Affected entity or entities.
- Summary.
- Detailed explanation.
- Severity or importance.
- Classification.
- Supporting evidence references.
- Relevant source snapshots.
- Applicable scope.
- First-observed time.
- Last-observed time.
- Resolution or supersession state, where supported.
- Limitations and unresolved questions.

### 15.2 Severity

Severity must be defined by the rule or applicable policy.

For example, a missing optional description may be informational, while a missing required verification result may prevent a particular goal from being classified as achieved.

Severity should not be based solely on the number of affected records.

### 15.3 Findings are not alerts by default

A finding does not automatically require a notification or immediate action.

Notification policies, if introduced, should be separate from the analysis rules. This prevents routine data-quality observations from generating unnecessary alerts.

---

## 16. Rule specification and execution

### 16.1 Rule definition

Each rule should document:

- Stable rule ID.
- Rule name and purpose.
- Rule version.
- Applicable entity types.
- Required input fields.
- Required source coverage.
- Evaluation logic.
- Output finding types.
- Severity or classification logic.
- Exceptions and exclusions.
- Known limitations.
- Unit tests and acceptance examples.

### 16.2 Rule implementation

The initial implementation should use small, focused Python functions or similarly simple deterministic components.

Rules should not:

- Read arbitrary files outside their declared input.
- Call external AI services.
- Modify source systems.
- Change portfolio decisions.
- Depend on uncontrolled wall-clock time.
- Depend on unordered collection iteration where ordering affects the output.
- Hide failures by returning a successful empty result.

### 16.3 Configuration

Thresholds and policy choices should be explicit configuration values or approved portfolio rules.

Examples include:

- Evidence freshness thresholds.
- Required evidence categories for a particular goal type.
- Conditions for classifying a milestone as overdue.
- Source-specific completeness requirements.
- Rules governing which verification evidence is acceptable.

Configuration changes must be versioned or otherwise recorded so that historical analysis remains explainable.

### 16.4 Execution isolation

Where practical, one rule's failure should not prevent independent rules from producing results.

However, a rule must not execute when its required inputs are unavailable or invalid. It should return a clear not-evaluable outcome or diagnostic rather than an unsupported finding.

---

## 17. Report generation

The analysis engine should produce reports that explain both findings and the evidence behind them.

A report should include:

- Analysis run ID.
- Report scope.
- Reference date and time where relevant.
- Source snapshot references.
- Portfolio and plan revisions.
- Rule-set version.
- Findings grouped by relevant entity or category.
- Evidence references.
- Coverage limitations.
- Failed or skipped rules.
- Changes from the previous comparable analysis.
- Any unresolved conflicts.

Reports should distinguish between:

1. Observed facts.
2. Deterministic derivations.
3. Evidence classifications.
4. Recommendations imported from another process.
5. Human-approved decisions.

The report generator must not present an AI recommendation as a deterministic finding simply because both appear in the same report.

---

## 18. Relationship with external AI analysis

Deterministic analysis is the baseline for routine portfolio understanding. External AI is an optional layer for questions that require synthesis, interpretation, or strategic judgment.

### 18.1 Suitable AI use cases

AI may help with:

- Interpreting the implications of a collection of deterministic findings.
- Comparing possible investment priorities.
- Evaluating reuse opportunities across engineering tools.
- Proposing a minimum viable release.
- Identifying strategic trade-offs.
- Explaining possible causes of a gap.
- Proposing questions for a portfolio review.

### 18.2 Handoff contract

When Siddhi sends analysis context to an external AI process, it should include:

- The question or objective.
- Relevant goal and initiative definitions.
- Selected source snapshots.
- Deterministic findings.
- Relevant evidence and provenance references.
- Known conflicts and missing information.
- Constraints and explicit assumptions.
- The requested output format.

The handoff should include only the context required for the task and should respect source confidentiality.

### 18.3 AI output handling

AI output must be stored separately from deterministic findings.

It should record:

- Analysis request ID.
- Model or provider identity when available.
- Input context references.
- Generation time.
- Returned recommendations.
- Explicit assumptions and uncertainty.
- Any human review or approval state.

AI output must not automatically alter priorities, plans, acceptance criteria, source records, or approved decisions.

---

## 19. Performance and scalability

The initial engine should be designed for a local-first application with a modest portfolio and bounded source snapshots.

It should favor:

- Indexed database queries.
- Incremental recomputation where reliable dependency information exists.
- Reuse of unchanged normalized inputs.
- Bounded analysis scope.
- Pagination for large finding collections.
- Efficient comparison of stable IDs and fingerprints.
- Clear separation between analysis computation and report rendering.

The implementation should avoid introducing distributed processing, complex scheduling, or a separate rules service before measured requirements justify them.

Performance targets should be derived from the non-functional requirements and tested against a representative dataset.

---

## 20. Security and data integrity

The analysis engine must:

- Operate on authorized Siddhi records and snapshots.
- Preserve source provenance.
- Treat external source content as untrusted data.
- Avoid executing scripts or commands found in evidence.
- Prevent source content from overriding operational instructions.
- Respect data-access and privacy constraints.
- Avoid exposing sensitive source content in ordinary reports.
- Preserve historical run and rule references.
- Use transactional persistence where necessary.
- Record analysis failures and incomplete results.
- Avoid overwriting source declarations with derived assessments.

Analysis results must remain traceable to the inputs from which they were derived.

---

## 21. Testing requirements

The engine must be tested for:

1. Identical inputs producing equivalent logical findings.
2. Explicit date handling and historical reruns.
3. Missing optional fields.
4. Missing required fields.
5. Unknown source metadata.
6. Partial source coverage.
7. Conflicting source declarations.
8. Stale evidence.
9. Failed and interrupted ingestion.
10. Unresolved portfolio mappings.
11. Invalid dependencies.
12. Applicable dependency cycles.
13. Overdue and completed milestones.
14. Plan revisions and changed acceptance criteria.
15. Goal-specific acceptance rules.
16. Criteria that cannot be evaluated deterministically.
17. Source changes that invalidate previous findings.
18. Rule-version changes.
19. Finding reconciliation across analysis runs.
20. Historical report reproducibility.
21. Independent rule failure.
22. Large evidence sets and bounded analysis.
23. Separation of deterministic findings from AI recommendations.
24. Ensuring no analysis operation modifies authoritative source records.

Tests should include realistic fixtures for Vyasa, OpenSpec, OKF, Git, and verification records, with explicit examples of missing and conflicting evidence.

---

## 22. Acceptance criteria

The deterministic analysis engine is ready when:

- Routine analysis can run without an external AI service.
- Rules have stable identifiers and documented semantics.
- Inputs and outputs are traceable to specific snapshots and portfolio revisions.
- Historical analysis records retain their rule versions and reference times.
- The engine distinguishes observed facts from derived findings and approved decisions.
- Missing evidence is reported only within a sufficiently covered and defined scope.
- Source declarations are not presented as independent verification.
- Goal assessments use goal-specific acceptance criteria rather than a universal progress formula.
- Findings identify their supporting evidence and known limitations.
- Independent rules can fail without unnecessarily blocking unrelated analysis.
- Source changes can identify assessments that may need refreshing.
- Historical comparisons distinguish issue resolution from changed scope or changed rules.
- Reports expose incomplete inputs and skipped rules.
- AI recommendations remain separate from deterministic results.
- Analysis does not modify authoritative external source records.
- Performance is acceptable for the agreed initial portfolio size.

---

## 23. Implementation phases

### Phase 1 — Analysis foundation

Implement:

- Analysis run records.
- Input resolution.
- Rule registration and versioning.
- Finding model.
- Deterministic execution contract.
- Basic report generation.

**Deliverable:** Siddhi can run a small set of rules against recorded portfolio data and produce traceable findings.

### Phase 2 — Evidence and integrity rules

Implement:

- Portfolio integrity checks.
- Evidence coverage and classification.
- Source freshness checks.
- Ingestion health checks.
- Missing and conflicting evidence reports.

**Deliverable:** Siddhi can explain which information is available, missing, stale, or unresolved.

### Phase 3 — Planning and historical analysis

Implement:

- Milestone and dependency rules.
- Plan revision comparison.
- Source snapshot comparison.
- Finding reconciliation.
- Historical analysis references.

**Deliverable:** Siddhi can explain how the portfolio and its evidence have changed between reviews.

### Phase 4 — Goal-specific assessment

Implement explicit acceptance criteria for selected goal types, with clear outcomes for passed, failed, and not-evaluable criteria.

**Deliverable:** Siddhi can assess measurable goal criteria without imposing the same model on every portfolio goal.

### Phase 5 — AI handoff

Provide a controlled interface that packages selected deterministic findings and evidence for optional external strategic analysis.

**Deliverable:** AI can support judgment-intensive questions without becoming the authority for source facts or approved decisions.

---

## 24. Open questions

| ID | Question | Why it matters |
|---|---|---|
| DA-001 | Should rules initially be implemented entirely in Python, or should selected rules be configurable? | Controls complexity and maintainability |
| DA-002 | Which evidence classifications are mandatory in the first release? | Establishes a consistent assessment vocabulary |
| DA-003 | Should goals define their own machine-evaluable acceptance criteria, or should Siddhi support reusable goal-type templates? | Balances flexibility and consistency |
| DA-004 | Which source freshness thresholds should be configurable by source or goal? | Prevents arbitrary stale-evidence rules |
| DA-005 | Which conditions should block a goal from being assessed as achieved? | Defines evidence sufficiency |
| DA-006 | Should the initial release expose a numerical progress measure for any specific goal types? | Avoids an unsupported universal score |
| DA-007 | How should findings be reconciled when a rule changes? | Preserves historical meaning |
| DA-008 | Which historical reports and analysis inputs must be retained? | Defines reproducibility and storage needs |
| DA-009 | Should analysis run automatically after ingestion or only on demand initially? | Controls workflow complexity |
| DA-010 | Which findings should become notifications or review tasks? | Separates analysis from operational alerting |
| DA-011 | What authorization rules apply to evidence and analysis reports? | Defines access boundaries |
| DA-012 | Which goal acceptance criteria should be implemented first as reference examples? | Establishes the initial testable rule set |

---

## 25. Related documentation

- `vision.md`
- `scope-and-roadmap.md`
- `functional-requirements.md`
- `non-functional-requirements.md`
- `system-architecture.md`
- `architectural-decisions.md`
- `domain-model.md`
- `data-ownership.md`
- `data-model.md`
- `application-workflows.md`
- `source-integration.md`
- `vyasa-integration.md`
- `openspec-integration.md`
- `okf-integration.md`
- `git-evidence.md`
- `ingestion-and-snapshots.md`
- `scanning-and-evidence.md`
- `security-and-privacy.md`

**Document status:** Draft for review. The initial rule set, goal acceptance criteria, evidence sufficiency policies, and analysis scheduling model must be agreed before converting this document into implementation-level OpenSpec requirements.