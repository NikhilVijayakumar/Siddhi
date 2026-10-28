# Siddhi — Vision

**Product:** Siddhi (सिद्धि)  
**Tagline:** From intention to accomplishment.  
**Document:** `vision.md`  
**Status:** Draft for review  
**Version:** 0.1

## 1. Vision Statement

Siddhi is a portfolio intelligence and strategic planning system that helps turn goals and intentions into meaningful, measurable outcomes.

It provides a unified view of commercial products, creative works, engineering initiatives, and internal development investments. It helps identify what exists, what is progressing, what is missing, and what deserves attention next.

Siddhi combines evidence from existing development projects and knowledge systems with deterministic analysis and external AI-assisted strategic reasoning. It enables informed decisions about what to build, what to reuse, what to defer, and where to invest effort.

Its purpose is not simply to track projects. It is to help ensure that ongoing work contributes to the outcomes that matter.

## 2. The Problem

A growing portfolio of software, engineering tools, creative works, and commercial opportunities creates several challenges.

### 2.1 Fragmented project intelligence

Project information is distributed across repositories, requirements, engineering knowledge, source history, and other development artifacts. Understanding the overall state of the portfolio requires bringing these sources together.

### 2.2 Activity does not guarantee outcomes

Engineering work can make continuous progress without producing a commercially usable product, published creative work, or another intended outcome. Individual project progress does not necessarily indicate portfolio-level progress.

### 2.3 Internal investments compete with external outcomes

Internal frameworks, libraries, and developer tools can improve productivity and support multiple projects. However, continued internal development can also consume attention that might otherwise advance commercial products or publications.

Neither internal development nor commercial work should automatically take precedence. Their value must be evaluated in the context of goals, dependencies, opportunities, costs, and constraints.

### 2.4 Planning becomes difficult as the portfolio grows

When many initiatives are active, it becomes difficult to compare their strategic value, identify dependencies, recognize neglected goals, and decide what should happen next.

### 2.5 Important decisions lose their context

Plans change as evidence, capabilities, constraints, and opportunities change. Without preserving the rationale behind decisions, assumptions, and earlier plans, it becomes difficult to understand why priorities changed or whether previous decisions remain valid.

## 3. Intended Outcomes

Siddhi aims to help its owner:

- Maintain a reliable, consolidated view of projects, goals, initiatives, and supporting evidence.
- Connect development activity to intended commercial, creative, and strategic outcomes.
- Identify gaps between intended outcomes and available capabilities, knowledge, implementation evidence, and plans.
- Compare internal engineering investments with product development and other portfolio opportunities.
- Recognize reusable capabilities and initiatives that support multiple outcomes.
- Make explicit decisions about what to build, continue, reuse, defer, investigate, or stop.
- Maintain realistic plans, milestones, dependencies, and review history.
- Detect when actual evidence no longer supports the current plan.
- Preserve decisions, assumptions, uncertainty, and the rationale behind changes.
- Reduce manual status gathering and repetitive reporting without requiring time logging.

These are intended outcomes, not claims that every outcome can be determined automatically.

## 4. Scope of the Portfolio

Siddhi must accommodate different kinds of work without forcing them into one rigid product lifecycle.

The portfolio may include:

- Commercial software products and applications.
- Games and interactive experiences.
- Books, novels, educational content, and other publications.
- Films, music videos, music, and other creative works.
- Internal engineering frameworks, libraries, platforms, and developer tools.
- Research, experiments, and enabling initiatives.

Each goal or initiative has its own intended outcome, scope, constraints, acceptance criteria, and timeline. A small commercial publication and a large software product should not be evaluated against identical maturity expectations.

Internal initiatives may have independent strategic value or support several downstream outcomes. Siddhi should make these relationships visible rather than requiring every internal project to justify itself against a single commercial product.

## 5. Guiding Principles

### 5.1 Outcomes over activity

Measure progress against intended results and supporting evidence, not merely the number of active projects, tasks, commits, or documents.

### 5.2 Evidence before assumptions

Separate confirmed facts, declared status, derived findings, candidate matches, missing information, and unresolved questions. A keyword match, completed task, or recent commit must not be treated as proof that an outcome has been achieved.

### 5.3 Deterministic foundations

Routine extraction, normalization, comparisons, status summaries, change detection, and report generation should be reproducible wherever practical.

AI-assisted reasoning should be used where judgment, synthesis, or strategic interpretation is genuinely valuable.

### 5.4 Clear ownership of information

Siddhi must respect the authority of existing systems:

- Vyasa owns workspace and repository inventory.
- OpenSpec owns requirements and its development artifacts.
- OKF owns engineering knowledge.
- Git and related verification sources provide implementation and revision evidence.
- Siddhi owns portfolio goals, priorities, plans, analyses, decisions, and reviews.

Siddhi may index and interpret information from these systems, but should not silently replace their authoritative records.

### 5.5 Knowledge and requirements are independent

Engineering knowledge does not require an active requirement to exist. Likewise, a requirement may exist before sufficient engineering knowledge is available.

Siddhi must represent both independently and identify relevant relationships without making one dependent on the other.

### 5.6 Human-directed strategic decisions

Siddhi should provide evidence, comparisons, options, risks, and recommendations. Portfolio priorities and consequential decisions remain subject to explicit human approval.

### 5.7 Flexible evaluation

Do not assume that all initiatives need the same maturity stages, scale, release model, or success criteria. Evaluation must reflect each initiative's declared purpose and ambitions.

### 5.8 Minimal administrative overhead

Use existing project artifacts and source history wherever possible. Do not require manual time logging or duplicate data entry merely to maintain portfolio visibility.

### 5.9 Preserve history and rationale

Retain meaningful snapshots, plan revisions, decisions, assumptions, and review outcomes so changes can be explained and earlier reasoning can be revisited.

### 5.10 Build only what is justified

Siddhi is itself an internal engineering investment. Its development should remain proportionate to the portfolio problems it solves, rather than becoming another open-ended tooling project.

## 6. How Siddhi Creates Value

Siddhi combines three complementary capabilities.

**Portfolio intelligence:** Consolidates evidence from projects, requirements, engineering knowledge, and source history to explain the current state.

**Deterministic analysis:** Compares available evidence against goals and plans, highlights gaps and changes, and generates reproducible reports.

**Strategic reasoning:** Prepares structured evidence for external AI tools or coding agents when deeper analysis is required, then preserves the resulting recommendations and approved decisions.

This combination helps distinguish what the system knows, what it has derived, what remains uncertain, and what requires judgment.

## 7. What Siddhi Is Not

Siddhi is not intended to be:

- A replacement for Vyasa, OpenSpec, OKF, Git, or existing verification systems.
- A generic task manager that treats activity as the primary measure of success.
- An autonomous AI agent that makes portfolio decisions without approval.
- A system that assumes every internal project is valuable simply because it is reusable.
- A system that assumes commercial work must always override internal investment.
- A mandatory time-tracking or employee-monitoring system.
- A rigid product lifecycle framework that forces every project through identical stages.
- A system that claims implementation or release readiness without adequate evidence.
- A second source of truth for repository requirements or engineering knowledge.

## 8. Relationship to Siddhi API

Siddhi API is the initial backend implementation of the Siddhi system.

It will provide the core domain logic, source integrations, data ingestion, persistence, deterministic analysis, report generation, planning operations, and integration interfaces.

The initial backend is planned around Python, FastAPI, and SQLite. A separate React, TypeScript, and Electron application is intended to provide the desktop interface later.

The API and desktop application are implementation choices, not the definition of Siddhi's long-term purpose. The core portfolio model and business rules should remain independent of the presentation layer.

## 9. Long-Term Direction

Siddhi should evolve into a dependable portfolio decision-support system that makes it easier to maintain balance between building capabilities and delivering outcomes.

As the portfolio grows, Siddhi should make its evidence more complete, its comparisons more useful, its recommendations more explainable, and its planning more responsive to change—without obscuring uncertainty or increasing administrative overhead unnecessarily.

Success means that the owner can make better-informed decisions about where to invest attention and resources, understand why those decisions make sense, and see whether the portfolio is moving toward its intended outcomes.

## 10. Vision-Level Success Criteria

The vision is being realized when:

1. Portfolio goals can be represented even before a corresponding repository or project exists.
2. Existing projects and their evidence can be understood together without duplicating the authority of source systems.
3. Commercial outcomes and internal investments can be evaluated within the same portfolio while preserving their different purposes.
4. The system can distinguish documented progress from demonstrated outcomes and unknown status.
5. Plans and priorities can change as new evidence becomes available, with earlier decisions and their rationale preserved.
6. Routine portfolio reporting requires substantially less manual gathering and reconciliation.
7. Recommendations are traceable to evidence, assumptions, constraints, and unresolved questions.
8. The owner retains control over priorities, approvals, and consequential actions.

These criteria express the intended direction. Quantitative targets and testable behavioral acceptance criteria will be established in subsequent documentation and OpenSpec requirements.

## 11. Open Questions

The following questions remain for subsequent design and review:

- What is the minimum useful portfolio model for the first release?
- Which source integrations must be available in the initial implementation?
- How should goals, initiatives, products, and outcomes relate when one initiative supports multiple goals?
- Which evidence categories and matching rules should be standardized?
- Which external AI workflows should be supported first?
- What level of local-only operation, backup, and recovery is required?
- Which measurable indicators will demonstrate that Siddhi is improving portfolio decisions rather than adding administrative overhead?

These questions should be resolved through the documentation and design process, not assumed to be settled by this vision.

---

**End of vision document**

