# Siddhi API — Domain Model

**Product:** Siddhi (सिद्धि)  
**Document:** `domain-model.md`  
**Status:** Draft for review  
**Version:** 0.1  
**Related documents:** `vision.md`, `scope-and-roadmap.md`, `functional-requirements.md`, `system-architecture.md`, `architectural-decisions.md`

## 1. Purpose

This document defines the core domain concepts of Siddhi API, their responsibilities, relationships, and business meaning.

The domain model provides a shared vocabulary for portfolio management, source intelligence, deterministic analysis, planning, and strategic review.

It is independent of the HTTP API, SQLite schema, source file formats, and future desktop interface.

The model must support software products, games, publications, creative works, internal engineering investments, research, and other initiatives without forcing them into a universal lifecycle.

## 2. Domain Design Principles

1. **Goals precede projects:** A goal may exist before any project or repository exists.
2. **Outcomes differ from activity:** Creating a repository, completing a task, or producing a report is not automatically a successful outcome.
3. **Initiatives can support multiple goals:** Shared capabilities and internal investments may enable several outcomes.
4. **Source ownership is explicit:** Siddhi owns portfolio decisions; external systems remain authoritative for their own records.
5. **Evidence is not truth by default:** Source declarations, derived findings, and verified results must remain distinguishable.
6. **Knowledge and requirements are independent:** OKF knowledge may exist without an OpenSpec requirement, and vice versa.
7. **Recommendations are not approvals:** AI analysis cannot silently change an approved plan or priority.
8. **History matters:** Significant revisions and decisions must retain their historical context.
9. **Unknown is a valid state:** Missing data must not be converted into an invented value or false conclusion.
10. **No mandatory time logging:** The model tracks intended outcomes, plans, milestones, and evidence rather than hours worked.

## 3. Core Conceptual Model

The model is organized into five conceptual areas.

<CodeBlock language="mermaid" editable>
flowchart TD
    Goal["Goal"]
    Outcome["Intended Outcome"]
    Initiative["Initiative"]
    Project["Project Reference"]
    Evidence["Evidence"]
    Analysis["Analysis"]
    Finding["Finding"]
    Plan["Plan"]
    Milestone["Milestone"]
    Review["Review"]
    Recommendation["Recommendation"]
    Decision["Decision"]

    Goal --> Outcome
    Goal <-->|"supported by"| Initiative
    Initiative -->|"uses or coordinates"| Project
    Project --> Evidence
    Evidence --> Analysis
    Goal --> Analysis
    Analysis --> Finding
    Initiative --> Plan
    Plan --> Milestone
    Finding --> Review
    Plan --> Review
    Review --> Recommendation
    Recommendation --> Decision
    Decision -->|"may authorize"| Plan
</CodeBlock>

The diagram shows conceptual relationships. It does not imply that every entity must directly reference every other entity in the database.

## 4. Portfolio Concepts

### 4.1 Goal

**Definition:** A desired result that the portfolio owner intends to achieve.

A goal describes the reason for investing attention or resources. It may be commercial, creative, technical, operational, educational, or strategic.

Examples:

- Publish a commercially distributed novel.
- Release an educational game.
- Make a reusable engineering capability available to several products.
- Validate whether a software product has a viable market.

A goal may exist without a repository, initiative, or implementation plan.

**Conceptual attributes:**

- Stable identifier.
- Title and description.
- Intended result and rationale.
- Goal category, where useful.
- Priority and constraints.
- Target date or review date, when applicable.
- Success criteria.
- Current assessment and status.
- Assumptions, risks, and unresolved questions.
- Creation and revision history.

A goal is not considered achieved merely because related development work is complete. Achievement requires assessment against its declared success criteria and appropriate evidence.

### 4.2 Intended Outcome

**Definition:** The specific result or observable change that a goal seeks to achieve.

A goal may have one or more intended outcomes. An outcome can describe a release, publication, validated capability, commercial result, or another defined result.

Examples:

- A book is published and available through its intended distribution channels.
- A game reaches an explicitly defined release state.
- A reusable framework supports two identified products.
- A market hypothesis is evaluated using specified evidence.

An intended outcome should have its own success criteria where the goal contains multiple independently assessable results.

The domain must distinguish:

- **Intended outcome:** What should happen.
- **Observed result:** What available evidence indicates happened.
- **Outcome assessment:** Whether the observed result satisfies the declared criteria.

Revenue, sales, readership, and other commercial measurements should be optional, depending on the goal. Siddhi must not invent commercial results when no corresponding source or owner-provided evidence exists.

### 4.3 Initiative

**Definition:** A coordinated body of work intended to contribute to one or more goals.

An initiative can represent a commercial product effort, a creative production, an internal framework, a research activity, or another purposeful investment.

An initiative may:

- Support multiple goals.
- Depend on other initiatives.
- Use multiple projects or repositories.
- Have no repository yet.
- Contain one or more plans and milestones.
- Be paused, deferred, resumed, completed, or cancelled.
- Be evaluated independently from the goals it supports.

Conceptual attributes include identifier, title, purpose, initiative type, status, priority, constraints, linked goals, owner-provided assumptions, and history.

The initiative type is descriptive, not a hard-coded lifecycle selector. Different types of initiatives can have different acceptance criteria and planning structures.

### 4.4 Project Reference

**Definition:** Siddhi's reference to a project or repository discovered in an authoritative external system.

A project reference identifies an existing engineering or creative project without taking over its source identity.

It should retain:

- The originating system.
- The source project identifier.
- Repository references where applicable.
- The last known source metadata.
- The latest successful refresh or observed revision.
- Availability and freshness status.

For the initial implementation, Vyasa is the expected authority for project inventory.

A project reference is not necessarily a goal, initiative, or commercial product. One project can support multiple initiatives, and an initiative can exist before a project is created.

### 4.5 Portfolio Priority

**Definition:** An owner-controlled assessment of the relative importance of a goal or initiative within the portfolio.

Priority may consider intended outcomes, urgency, dependencies, constraints, strategic value, feasibility, and available evidence.

The domain should not assume a single universal formula or make AI-generated rankings authoritative.

A priority assessment should preserve its rationale and history when changed. A recommendation to change priority is separate from an approved priority change.

### 4.6 Constraint

**Definition:** A condition that limits or shapes the available choices.

Examples include target dates, available resources, technical dependencies, distribution requirements, budget limits, or access restrictions.

Constraints may apply to goals, initiatives, plans, or individual milestones.

The domain must distinguish explicit constraints from assumptions inferred during analysis. Uncertain constraints should be identified as such.

## 5. Planning Concepts

### 5.1 Plan

**Definition:** A versioned proposal for how an initiative or goal is intended to progress toward its outcome.

A plan may contain:

- Intended outcomes.
- Milestones and target dates.
- Dependencies.
- Proposed activities or work items.
- Constraints and assumptions.
- Risks and unresolved questions.
- Acceptance criteria.
- Current approval state.
- Revision rationale.

A plan is not an implementation record and does not prove that its proposed activities occurred.

### 5.2 Plan Revision

**Definition:** A version of a plan representing a particular approved or proposed arrangement of work.

Each meaningful revision must retain a reference to its predecessor where applicable, its creation time, its author or origin, its changes, and its rationale where available.

A new AI recommendation must not overwrite the currently approved plan.

### 5.3 Milestone

**Definition:** A significant planned point of progress or deliverable that can be assessed against explicit criteria.

A milestone may have:

- Identifier and description.
- Target date, if applicable.
- Dependencies.
- Acceptance criteria.
- Status.
- Relevant evidence references.
- Delay or completion rationale where known.

A milestone's status should distinguish planned, in progress, blocked, completed, deferred, and cancelled where these states are appropriate.

The exact state model must be reviewed before implementation.

Completion should not be inferred from a date passing or a source document existing.

### 5.4 Dependency

**Definition:** A relationship in which progress toward one milestone, initiative, or outcome depends on another.

Dependencies may represent technical prerequisites, shared capabilities, external approvals, or sequencing constraints.

The model should record the dependency type, direction, source or rationale, and resolution status where relevant.

An inferred dependency should remain a candidate until confirmed if the available evidence is insufficient.

### 5.5 Review

**Definition:** A time-bounded assessment of portfolio execution or strategic direction using available evidence.

Two initial review purposes are anticipated:

- **Execution review:** Examines milestones, near-term plans, blockers, and recent evidence.
- **Portfolio review:** Examines outcomes, investment balance, opportunities, priorities, and strategic trade-offs.

A review should retain its inputs, findings, proposed actions, decisions, and references to the plan or source snapshots it evaluated.

Weekly and monthly are initial review cadences, not intrinsic properties of the domain entity.

## 6. Evidence and Source Intelligence

### 6.1 Source System

**Definition:** An external system that provides authoritative records or evidence.

Examples include Vyasa, OpenSpec, OKF, Git/VCS, and supported verification systems.

A source system has an integration identity, supported access mechanism, and relevant format or contract information.

### 6.2 Source Artifact

**Definition:** An identifiable item obtained from a source system.

Examples include an OpenSpec requirement, a change artifact, an OKF knowledge document, a commit, a release tag, or a structured investigation report.

A source artifact should preserve its source identity, locator, revision or content hash where available, and ingestion context.

### 6.3 Source Snapshot

**Definition:** A recorded observation of a source or defined source scope at a particular time.

A snapshot supports historical comparison and helps explain which information was available when an analysis was generated.

A snapshot must distinguish a successfully observed state from a failed or partial observation. Failure to retrieve a source is not evidence that its artifacts have been deleted.

### 6.4 Evidence Record

**Definition:** A normalized, traceable representation of information used to assess a goal, initiative, milestone, or other domain question.

Evidence may be:

- Explicitly declared by a source.
- Observed from source history.
- Derived through a deterministic rule.
- Imported from a verification artifact.
- Supplied by the portfolio owner.
- Proposed by external AI analysis.

Evidence must retain its origin and evidentiary status. These categories must not be treated as interchangeable.

### 6.5 Evidence Assessment

**Definition:** An interpretation of evidence relative to a defined question or criterion.

An assessment may determine that evidence supports a claim, contradicts it, is insufficient, is stale, or remains unresolved.

The existence of evidence is not proof of its truth. For example, a requirement declaring a feature complete and a successful test result are different kinds of evidence.

### 6.6 Source Freshness

**Definition:** The degree to which stored source information reflects the latest successfully observed source state.

Freshness is an operational property, not a judgment about correctness.

The model should distinguish current, stale, unavailable, never retrieved, unsupported, and invalid source states where applicable.

## 7. Analysis Concepts

### 7.1 Analysis Run

**Definition:** A recorded execution of a defined analysis against identifiable inputs and rules.

An analysis run should retain:

- Analysis type.
- Relevant goals and portfolio records.
- Input source snapshots.
- Rule or analysis version.
- Start and completion metadata.
- Outcome and warnings.
- Generated findings and report references.

An analysis run must not silently fetch unrelated new inputs after its recorded input set has been established.

### 7.2 Finding

**Definition:** A specific conclusion or observation produced by analysis.

Examples include:

- A confirmed relationship between a goal and an existing capability.
- A candidate match requiring review.
- An explicitly unmet success criterion.
- Missing evidence needed to assess a goal.
- A conflict between source records.
- A dependency that may block an outcome.

A finding should include its classification, explanation, evidence references, applicable rule, and limitations.

### 7.3 Finding Classification

The initial model should distinguish the following concepts:

| Classification | Meaning |
|---|---|
| Confirmed relationship | Supported by explicit evidence or a defined confirmation rule |
| Candidate match | Potentially relevant but not established |
| Identified gap | A defined criterion is demonstrably unmet |
| Missing evidence | Required information is unavailable |
| Unresolved | Evidence is ambiguous, conflicting, or insufficient |
| Stale or unavailable | The relevant source cannot be treated as current |

These are analytical classifications, not universal statuses for goals or initiatives.

### 7.4 Analysis Report

**Definition:** A stored presentation of findings and supporting context from an analysis run.

The report should preserve the inputs, rules, generation metadata, findings, and limitations needed to explain its conclusions.

A report is a record of analysis, not an approved decision.

### 7.5 External Analysis

**Definition:** A structured result produced by an external AI tool, coding agent, or other authorized analysis provider.

It may contain recommendations, assumptions, alternatives, risks, confidence statements, and requests for further evidence.

The source and provenance must remain visible. An external analysis does not become verified evidence merely because its structure is valid.

## 8. Decisions and Recommendations

### 8.1 Recommendation

**Definition:** A proposed course of action derived from analysis or supplied by an authorized external advisor.

A recommendation may suggest building, reusing, deferring, investigating, continuing, or stopping an initiative.

It should include its rationale, supporting evidence, assumptions, uncertainty, and relevant alternatives where available.

### 8.2 Decision

**Definition:** An explicitly recorded choice made by the portfolio owner or another authorized decision-maker.

A decision should capture:

- The question or issue.
- The selected option.
- The rationale.
- Relevant evidence and recommendations.
- The decision date.
- Approval status and decision authority.
- Consequences or follow-up actions where applicable.

A decision is distinct from its implementation. Siddhi should not mark an action as executed without appropriate evidence.

### 8.3 Decision Revision

**Definition:** A later decision that changes, replaces, or reverses an earlier decision.

The original decision should remain in history. The new decision should reference the earlier decision and explain the changed context or rationale where available.

## 9. Relationships Between the Core Concepts

The following cardinalities are conceptual and must be confirmed before the data model is finalized.

| Relationship | Proposed meaning |
|---|---|
| Goal → Intended outcome | One goal can have multiple outcomes |
| Goal ↔ Initiative | Many-to-many; initiatives may support multiple goals |
| Initiative ↔ Project reference | Many-to-many; projects may support multiple initiatives |
| Initiative → Plan | An initiative may have multiple plan revisions |
| Plan → Milestone | A plan may contain multiple milestones |
| Milestone ↔ Dependency | A milestone may depend on other milestones or initiatives |
| Source system → Source artifact | A source system can expose many artifacts |
| Source artifact → Evidence record | An artifact may produce multiple normalized evidence records |
| Source snapshot → Evidence records | A snapshot may contain many observed records |
| Analysis run → Finding | An analysis run may produce multiple findings |
| Finding → Evidence records | A finding may cite multiple supporting or conflicting records |
| Analysis run → Analysis report | An analysis run may produce one or more reports |
| External analysis → Recommendation | An external analysis may produce multiple recommendations |
| Recommendation → Decision | A recommendation may be accepted, rejected, deferred, or investigated |
| Decision → Plan revision | A decision may authorize a plan revision |
| Review → Analysis and plans | A review may evaluate multiple reports, plans, and evidence snapshots |

The final relational model may introduce explicit association entities when relationships require their own attributes, history, approval state, or provenance.

## 10. Statuses and Lifecycle Semantics

Statuses must reflect the purpose of the entity rather than forcing every entity into one universal lifecycle.

### Goal

A goal may be proposed, active, on hold, achieved, abandoned, or superseded, subject to agreed definitions.

### Initiative

An initiative may be proposed, planned, active, paused, deferred, completed, cancelled, or archived.

### Plan

A plan may be a draft, under review, approved, superseded, or archived.

### Recommendation

A recommendation may be pending review, accepted, rejected, deferred, or under investigation.

### Decision

A decision may be proposed, approved, superseded, or reversed where those distinctions are needed.

### Source snapshot

A snapshot may be successful, partial, failed, or otherwise explicitly classified according to its processing outcome.

These are proposed state sets. Their permitted transitions and meanings must be specified separately. A state must not change merely because an arbitrary date passes or a source becomes unavailable.

## 11. Cross-Cutting Domain Rules

### 11.1 Stable identity

Portfolio entities and source references need stable identifiers that remain valid when display names or repository locations change.

### 11.2 Provenance

Evidence, findings, and reports must retain links to their source records and processing context wherever available.

### 11.3 Explicit uncertainty

The domain must distinguish known facts, owner declarations, derived findings, candidate relationships, and unknown information.

### 11.4 Independent source domains

OpenSpec requirements and OKF knowledge must be independently ingestible and queryable. Relationships between them are optional and must not be assumed.

### 11.5 Historical integrity

Changes to plans, priorities, and decisions must preserve relevant history. Source observations should not be confused with the latest state after a refresh.

### 11.6 No implicit approval

Neither deterministic findings nor external recommendations may silently approve a plan or change portfolio priorities.

### 11.7 No mandatory time tracking

The domain does not require work-hour records. Dates, milestones, source evidence, and explicit assessments are sufficient for the intended planning model.

## 12. Concepts Deliberately Excluded from the Initial Domain

The following should not be introduced as mandatory core entities without a demonstrated need:

- Employee timesheets.
- Universal product maturity stages.
- Mandatory sprint and issue-tracker entities.
- A fixed commercial product taxonomy that dictates lifecycle behavior.
- AI model internals as a prerequisite for portfolio analysis.
- A separate project registry that competes with Vyasa.
- A duplicated requirement or knowledge-authoring system.

Additional concepts may be added when an actual workflow requires them.

## 13. Open Domain Questions

The following questions require review before the domain model is considered stable.

### Goals and outcomes

1. Must every goal have at least one explicitly defined intended outcome at creation, or can outcomes be added later?
2. Can a goal contain several independently assessed outcomes?
3. How should success criteria represent qualitative outcomes, such as publication quality, alongside measurable outcomes, such as sales?

### Initiatives and projects

4. Should a project reference be allowed to connect directly to a goal without an initiative?
5. Can an initiative support a goal without an existing project?
6. Should internal engineering investments and commercial initiatives share the same base model with optional specialized attributes?

### Evidence and analysis

7. Which evidence classifications require explicit human confirmation?
8. How should contradictory evidence be represented?
9. How much source content should be stored locally versus referenced by path, identifier, or hash?
10. Should an evidence assessment be an independent versioned entity when its interpretation may change?

### Planning and decisions

11. Which statuses are necessary for the first release?
12. Can a plan contain milestones without an associated repository or task list?
13. How should partial completion of an intended outcome be represented?
14. Which decision types require formal approval versus a simple recorded choice?

### Commercial outcomes

15. Should revenue, costs, sales, publication status, audience metrics, and other commercial results be first-class optional measurements, or remain extensible evidence records initially?

These questions should be resolved before finalizing the persistence schema and detailed OpenSpec requirements.

## 14. Relationship to Subsequent Documents

- `data-model.md` will translate these domain concepts into logical records, relationships, identifiers, and constraints.
- `data-ownership.md` will formalize authority and synchronization rules.
- `deterministic-analysis.md` will define finding semantics and evidence assessment rules.
- `api-design.md` will define how the domain is exposed through HTTP.
- `persistence-and-migrations.md` will define SQLite storage and schema evolution.
- OpenSpec will specify observable behavior and acceptance scenarios.
- OKF will preserve reusable domain knowledge, concepts, and design rationale.

The domain model should be reviewed before these dependent documents are finalized.

---

**End of domain model document**
