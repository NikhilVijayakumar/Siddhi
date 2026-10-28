# Siddhi API — Functional Requirements

**Product:** Siddhi (सिद्धि)  
**Document:** `functional-requirements.md`  
**Status:** Draft for review  
**Version:** 0.1  
**Related documents:** [vision](../../knowledge/product/vision.md), [scope and roadmap](../../knowledge/product/scope-and-roadmap.md), [package ownership](README.md)

## 1. Purpose

This document describes the functional capabilities Siddhi API must provide to support portfolio intelligence and strategic planning.

It defines expected system behavior, principal workflows, and functional boundaries. It is a design-baseline document, not yet the final OpenSpec specification. Individual requirements will later be decomposed into testable OpenSpec requirements and scenarios.

Implementation details, source-format specifications, database schemas, and engineering conventions will be documented separately.

This baseline retains stable identifiers. [Draft packages](README.md) own and
refine them for review; conversion to specifications retains this source and
traces decisions rather than deleting or renumbering it. Relevant concepts are
maintained in [independent OKF knowledge](../../knowledge/index.md).

## 2. Functional Objectives

Siddhi API must enable its owner to:

1. Maintain goals and intended outcomes independently of existing projects.
2. Discover projects through Vyasa without duplicating Vyasa's ownership of project inventory.
3. Ingest and normalize supported OpenSpec, OKF, and Git information.
4. Preserve source identity, provenance, refresh status, and historical snapshots.
5. Understand available project capabilities, declared development progress, and supporting evidence.
6. Compare portfolio goals with available projects and capabilities.
7. Identify candidate matches, confirmed relationships, gaps, missing evidence, and unresolved findings.
8. Generate reproducible reports from known inputs and defined analysis rules.
9. Maintain initiatives, plans, milestones, dependencies, and decisions.
10. Capture external AI analysis without confusing recommendations with approved decisions.
11. Review changes over time and revise plans while preserving decision history.
12. Expose these capabilities through a documented API for a separate desktop frontend.

## 3. Actors and External Systems

### 3.1 Primary actor

**Portfolio owner:** Defines goals, reviews evidence, sets priorities, approves decisions, and controls consequential actions.

The initial implementation is designed around a single local portfolio owner. The design should not prevent later expansion to multiple users, but multi-user collaboration is not an initial requirement.

### 3.2 External systems

| System | Functional responsibility |
|---|---|
| Vyasa | Supplies project and repository inventory |
| OpenSpec | Supplies requirements, scenarios, change artifacts, tasks, and declared status |
| OKF | Supplies engineering knowledge and its associated metadata and relationships |
| Git/VCS | Supplies revision history and available release evidence |
| Repository artifacts | Supply supported structured reports or additional project evidence |
| External AI tools or coding agents | Supply optional strategic analysis and recommendations |
| Future Siddhi desktop frontend | Consumes the API and presents information and workflows |

Siddhi must distinguish information obtained from these systems from information it owns.

## 4. Portfolio Management

### FR-001 — Define goals

The system must allow the portfolio owner to create, view, update, archive, and retrieve goals.

A goal should support, as appropriate:

- Stable identifier and title.
- Description and intended outcome.
- Rationale and strategic context.
- Goal category or domain.
- Priority and relevant constraints.
- Target date or review date, when applicable.
- Success criteria and acceptance evidence.
- Assumptions, risks, and unresolved questions.
- Status and historical revisions.

A goal must be allowed to exist before any project or repository is associated with it.

### FR-002 — Represent different types of outcomes

The system must accommodate software products, games, creative works, publications, internal engineering investments, research initiatives, and other portfolio goals.

It must not require every goal to follow the same lifecycle or use identical maturity criteria.

### FR-003 — Manage initiatives

The system must allow the owner to represent a coordinated body of work intended to achieve one or more outcomes.

An initiative may:

- Support multiple goals.
- Depend on other initiatives.
- Use one or more existing projects.
- Exist before a repository is created.
- Contain milestones and a versioned plan.
- Be deferred, paused, completed, or cancelled with an appropriate record of the decision.

### FR-004 — Link projects to portfolio goals

The system must allow goals and initiatives to be associated with projects discovered through Vyasa.

Associations must record their nature and, where relevant, their rationale, evidence, confidence or classification, and approval status.

A candidate association inferred by analysis must not automatically become a confirmed strategic relationship.

### FR-005 — Record priorities and constraints

The system must allow the owner to record priorities, target dates, dependencies, budget or resource constraints when known, strategic assumptions, and decision criteria.

Missing information must remain identifiable as unknown rather than being silently filled with invented values.

### FR-006 — Preserve portfolio history

Meaningful changes to goals, initiatives, priorities, plans, and decisions must be traceable.

The system must retain enough history to explain what changed, when it changed, and the recorded rationale where provided.

## 5. Source Discovery and Ingestion

### FR-007 — Discover projects

The system must retrieve available project and repository inventory from Vyasa through a defined integration interface.

It must retain source identifiers and map source projects to Siddhi's internal references without creating competing project identities unnecessarily.

### FR-008 — Identify supported source artifacts

For each discovered repository or project, the system must identify supported OpenSpec artifacts, OKF knowledge artifacts, Git evidence, and other explicitly supported structured project artifacts.

Discovery must distinguish an artifact that is absent from one that could not be accessed or inspected.

### FR-009 — Parse supported formats

The system must parse supported source formats using verified schema or format information.

It must not assume all repositories use the same OpenSpec schema, OKF format, version, or directory layout.

Unsupported versions and malformed artifacts must be reported explicitly.

### FR-010 — Normalize source information

The system must normalize supported source information into internal records suitable for querying, comparison, reporting, and historical tracking.

Normalized records must retain source references and enough provenance to locate the originating artifact or revision where available.

Normalization must not silently change the meaning or authority of the source record.

### FR-011 — Refresh source data

The system must support explicit source refresh operations.

A refresh must:

1. Identify the sources to inspect.
2. Obtain the latest accessible source information.
3. Parse and normalize supported artifacts.
4. Compare the result with the previous snapshot.
5. Record additions, modifications, removals, and unchanged records.
6. Record refresh time and outcome.
7. Preserve relevant historical state.
8. Report partial failures and unavailable sources.

The exact transactional and partial-refresh behavior will be established during detailed design.

### FR-012 — Track source freshness and failures

The system must expose whether source data is current, stale, unavailable, unsupported, invalid, or never successfully ingested, as applicable.

If a refresh fails, the system may retain the last known successful data, but it must preserve its prior revision and freshness information.

Failed refreshes must not silently replace valid records with incomplete data.

### FR-013 — Support incremental processing

Where source identity and revision information allow it, the system should avoid unnecessary reprocessing of unchanged content.

The system must not rely solely on timestamps when stronger revision or content-hash evidence is available.

The implementation must preserve correctness when source metadata is missing or unreliable.

## 6. OpenSpec Intelligence

### FR-014 — Inventory requirements and development artifacts

The system must expose the available supported OpenSpec artifacts, including applicable requirements, scenarios, changes, tasks, and declared statuses.

The exact inventory depends on the actual OpenSpec schema and artifact formats supported.

### FR-015 — Summarize declared development progress

The system must produce a summary of available OpenSpec development status and identify the source artifacts supporting that summary.

It must distinguish declared task or change completion from independently available implementation or verification evidence.

### FR-016 — Identify missing or incomplete requirement evidence

The system should identify relevant gaps in available requirements or development artifacts, such as missing references, incomplete declared workflows, or unsupported status information, where the supported schema makes these assessments possible.

Such findings must state their basis and must not imply that every repository is required to contain every possible artifact.

### FR-017 — Preserve source authority

Siddhi must not modify OpenSpec requirements, tasks, schemas, or change artifacts as part of routine ingestion or analysis.

## 7. OKF Knowledge Intelligence

### FR-018 — Inventory engineering knowledge

The system must expose supported OKF knowledge packages and artifacts, including available metadata, concepts, decisions, relationships, references, and declared validation status where present in the actual format.

### FR-019 — Assess knowledge availability

The system should summarize the engineering knowledge available for a project or a goal-related capability.

It may identify missing, inaccessible, unlinked, stale, or unsupported knowledge artifacts.

It must distinguish knowledge availability from knowledge correctness, completeness, or practical applicability.

### FR-020 — Keep knowledge independent of requirements

OKF knowledge must be discoverable and usable even when no related OpenSpec requirement exists.

Likewise, a requirement may exist even when the associated engineering knowledge is absent or insufficient.

The system may identify relationships between knowledge and requirements, but must not require a one-to-one mapping.

### FR-021 — Preserve knowledge authority

Routine ingestion and analysis must not rewrite authoritative OKF knowledge artifacts.

Any future publishing workflow must be explicit, authorized, and separately specified.

## 8. Git and Implementation Evidence

### FR-022 — Collect available revision evidence

The system must collect supported Git/VCS evidence, such as commit references, branches, tags, timestamps, and changed paths where available.

The exact evidence set depends on the source access mechanism and repository capabilities.

### FR-023 — Distinguish activity from achievement

The system may use revision activity as supporting evidence of work, but must not treat commit counts, recent commits, or branch existence as proof of meaningful progress or successful delivery.

### FR-024 — Represent verification evidence

Where existing workflows expose test results, build results, release records, or other verification artifacts, Siddhi should ingest supported evidence with source, revision, and timestamp information where available.

Missing verification data must be reported as unknown or unavailable, not as a failed test or a successful release.

### FR-025 — Read without modifying repositories

Routine refresh and analysis must not modify repository contents, check out branches, commit changes, or publish plans.

Any future operation that writes to a repository must have an explicitly defined, authorized workflow.

## 9. Goal-to-Evidence Analysis

### FR-026 — Compare goals with existing capabilities

The system must compare a goal's declared outcomes and constraints with available project information, requirements, engineering knowledge, and other relevant evidence.

The comparison must be based on defined rules and recorded inputs.

### FR-027 — Classify findings

The analysis must distinguish, at minimum, the following concepts:

- **Confirmed relationship:** Supported by sufficiently explicit evidence under defined rules.
- **Candidate match:** Potentially relevant but not yet established.
- **Identified gap:** A requirement or capability is demonstrably missing relative to an explicit criterion.
- **Missing evidence:** Information needed to assess the goal is not available.
- **Unresolved:** Available information is ambiguous, conflicting, or insufficient.
- **Stale or unavailable:** Relevant source data cannot be treated as current.

Exact definitions and classification rules must be finalized during requirements grilling.

### FR-028 — Explain analysis results

Each material finding must include an explanation of its basis and references to the source data or rule that produced it.

Where a conclusion depends on assumptions, incomplete data, or a candidate match, the report must make that limitation visible.

### FR-029 — Generate reproducible reports

The system must generate reports from a defined set of source snapshots, portfolio records, and analysis rules.

A report should record the relevant input versions, generation time, rule or report version, and findings.

Where the same inputs and deterministic rules are used, the analytical findings should be reproducible.

### FR-030 — Compare historical results

The system must allow a new analysis result to be compared with a previous result, identifying meaningful changes in source evidence, findings, gaps, and unresolved questions.

Differences caused by changed inputs must be distinguishable from differences caused by changed analysis rules.

## 10. Planning and Portfolio Reviews

### FR-031 — Create and revise plans

The system must support initiative plans containing relevant goals, intended outcomes, activities or work items, milestones, dependencies, dates, assumptions, and risks.

The detailed plan schema must accommodate different initiative types without forcing every initiative into identical stages.

### FR-032 — Preserve plan versions

Revising a plan must preserve prior versions and record relevant changes and rationale where provided.

A new recommendation must not silently overwrite an approved plan.

### FR-033 — Track milestones and dependencies

The system must record milestone dates, status, dependencies, and relationships to relevant goals or initiatives.

Where dependency information is incomplete or inconsistent, the system must identify the uncertainty rather than fabricate a dependency resolution.

### FR-034 — Support execution reviews

The system must support periodic reviews of current execution, including:

- Progress against the current plan.
- Newly available source evidence.
- Completed, delayed, or unresolved milestones where known.
- Blockers, dependencies, and risks.
- Differences from the previous review.
- Proposed actions and required decisions.

The initial review cadence is weekly, but the underlying review model should not depend on a single fixed schedule.

### FR-035 — Support strategic reviews

The system must support periodic portfolio reviews, initially planned on a monthly cadence, covering:

- Progress toward intended outcomes.
- Commercial opportunities and results where data is available.
- Internal engineering investments and their downstream relationships.
- Neglected goals and unresolved trade-offs.
- Changes in feasibility, constraints, and available capabilities.
- Recommended priority or plan changes.
- Decisions requiring owner approval.

Siddhi must not assume commercial work always takes precedence or that internal work is automatically justified.

### FR-036 — Preserve review and decision history

The system must preserve review reports, proposed actions, approved decisions, and relevant rationale.

It must distinguish recommendations, pending decisions, approved decisions, and implemented actions where evidence is available.

### FR-037 — Avoid mandatory time logging

The system must not require manual entry of hours spent on projects or tasks.

Where execution information is unavailable from source artifacts or explicit owner input, the system must show that limitation.

## 11. External AI and Coding-Agent Workflows

### FR-038 — Prepare analysis briefs

The system must assemble a structured brief containing the relevant goal, portfolio context, available evidence, constraints, known gaps, assumptions, and questions requiring judgment.

The brief should be tailored to the analysis purpose and should not include unrelated or unnecessary private repository content.

### FR-039 — Import external analysis

The system must support importing a structured analysis result produced outside Siddhi.

Imported results must retain their origin and, where available, model or tool identity, generation time, input references, assumptions, recommendations, and uncertainty.

### FR-040 — Validate external results

The system must validate imported results against the expected structure and identify invalid, incomplete, or unsupported references.

External analysis must be treated as a recommendation, not as verified fact simply because it was generated by an AI system.

### FR-041 — Approve recommendations explicitly

The system must allow the owner to review recommendations and record whether they are accepted, rejected, deferred, or require further investigation.

An imported recommendation must not automatically alter approved priorities or publish changes to a repository.

### FR-042 — Support deeper repository investigation

Where the stored evidence is insufficient, Siddhi should support a workflow that requests a structured repository investigation from an authorized coding agent.

The investigation should focus on a defined question and return a structured artifact that Siddhi can validate and ingest.

Routine source parsing and reporting must not depend on this workflow.

## 12. API and Operational Behavior

### FR-043 — Expose documented API operations

The system must expose implemented capabilities through documented HTTP APIs with validated request and response schemas.

The API contract must support independent frontend development and automated testing.

### FR-044 — Validate requests

The API must validate incoming data, reject invalid requests with consistent error responses, and avoid partial state changes when validation or transactional processing fails.

Detailed error formats and transaction boundaries will be defined during API design.

### FR-045 — Expose operation status

Long-running refreshes or analyses should expose their progress or final status through a defined API mechanism.

The initial design must determine whether these operations are synchronous or asynchronous based on expected workload and failure behavior.

### FR-046 — Provide diagnostics

The system must expose suitable health and diagnostic information for application availability, database access, and integration failures without exposing secrets or sensitive repository content.

### FR-047 — Preserve data integrity

The system must use appropriate transaction boundaries and integrity checks to prevent partial operations from silently corrupting portfolio-owned records or historical snapshots.

### FR-048 — Support database evolution

Database schema changes must be applied through controlled migrations. The system must be able to identify its schema version and report migration failures explicitly.

### FR-049 — Enforce access boundaries

The system must constrain filesystem and repository access to configured and authorized locations and mechanisms.

Imported repository content must be treated as data, not as instructions that can override Siddhi's security or operating rules.

### FR-050 — Support reliable local operation

The backend must be operable as a local service, with documented configuration, startup, shutdown, database location, diagnostics, and recovery procedures.

The detailed lifecycle contract will be defined before desktop packaging.

## 13. Cross-Cutting Functional Rules

The following rules apply across the capabilities above.

### 13.1 Provenance

Source-derived and analysis-derived records must preserve traceability to their source, revision or snapshot, and processing context wherever available.

### 13.2 Unknown is not false

Missing information must not automatically be interpreted as a negative result. For example, no recorded test result does not mean tests failed, and no discovered requirement does not prove a capability is absent.

### 13.3 Declared status is not verified status

The system must distinguish what a source declares from what other evidence demonstrates.

### 13.4 Recommendations are not decisions

Strategic recommendations must remain separate from approved portfolio decisions until explicitly accepted.

### 13.5 Source ownership is respected

Routine processing must not silently modify authoritative records in Vyasa, OpenSpec, OKF, or Git.

### 13.6 Historical context is retained

Changes to source evidence, portfolio plans, analysis rules, and decisions must be traceable sufficiently to explain meaningful differences over time.

### 13.7 AI is optional for routine operations

Deterministic ingestion, normalization, snapshot comparison, and defined-rule reporting must operate without external AI.

## 14. Initial End-to-End Workflow

The first usable workflow is intended to validate the core purpose of Siddhi.

1. Discover a project through Vyasa.
2. Retrieve available supported OpenSpec, OKF, and Git evidence.
3. Parse and normalize the evidence.
4. Store the source snapshot, revision references, and ingestion results.
5. Create a portfolio goal independently of the repository.
6. Compare the goal with the available evidence using defined deterministic rules.
7. Generate a report identifying confirmed relationships, candidate matches, gaps, and unknowns.
8. Refresh the source data later and identify changes.
9. Compare the new report with the previous result while preserving both.

This workflow is the proposed first-release target. Exact source coverage and acceptance criteria remain to be confirmed.

## 15. Open Questions for Requirements Grilling

The following questions require resolution before these functional requirements are converted into detailed OpenSpec artifacts.

### Portfolio model

1. What fields are mandatory for a goal at creation?
2. Can priorities use a numeric scale, named levels, or a configurable model?
3. How should an initiative relate to multiple goals?
4. How should actual commercial results be represented when external revenue or sales systems are not integrated?
5. What does it mean for a goal to be achieved, and who confirms achievement?

### Ingestion and source handling

6. Which Vyasa interface and data contract will Siddhi consume?
7. Which OpenSpec and OKF versions must be supported initially?
8. How are repository removals, renamed repositories, and inaccessible sources handled?
9. What snapshot retention policy is appropriate?
10. Which operations require a local checkout, and which must work against remote repositories?

### Analysis

11. Which matching and gap-classification rules are deterministic?
12. Which findings require owner confirmation before being treated as established?
13. How should conflicting source evidence be represented?
14. How are changes in analysis rules reflected in historical reports?
15. Which evidence is sufficient for a confirmed relationship?

### Planning and external analysis

16. What is the minimum viable plan structure?
17. Which actions require explicit approval?
18. What structured format will external analysis results use?
19. How should imported recommendations be linked to their supporting evidence?
20. Which external AI workflows are essential for the first usable release?

### API and operations

21. Which API operations must be synchronous?
22. How should long-running jobs be tracked and cancelled?
23. What local security and authentication model is required?
24. What are the backup and recovery expectations for SQLite?
25. What measurable acceptance criteria establish that the initial release is useful?

## 16. Relationship to OpenSpec and OKF

This document provides the functional overview from which detailed requirements will be derived.

When converted into OpenSpec:

- Each functional area will be decomposed into appropriately scoped requirements.
- Each requirement will include testable scenarios and acceptance criteria.
- Validation failures, missing information, stale data, partial failures, and security boundaries will receive explicit treatment.
- Implementation tasks will be organized into reviewable changes.

When converted into OKF:

- Reusable concepts, domain knowledge, architecture, source formats, design rationale, data semantics, and engineering conventions will be captured as knowledge.
- Knowledge will remain independently useful even where no current requirement refers to it.
- Requirements and later specifications reference knowledge; knowledge never references or depends on requirements, specifications, changes, or implementation. Relationship indexes owned by Siddhi do not impose backlinks in authoritative knowledge.

This document should be reviewed and grilled before either conversion is considered complete.

---

**End of functional requirements document**
