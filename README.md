# Siddhi (सिद्धि)

## Portfolio Intelligence & Strategic Planning System

**Tagline:** From intention to accomplishment.

**Status:** Initial concept and architecture definition  
**Codename:** Siddhi (सिद्धि)  
**Category:** Personal portfolio management, strategic planning, project intelligence and execution tracking

---

## 1. Overview

Siddhi is a portfolio intelligence and strategic planning system designed to help manage multiple projects, internal engineering investments, commercial products and creative works through a unified, evidence-driven workflow.

The system connects project information, engineering knowledge, development progress and long-term objectives to help answer:

- What projects and capabilities do we currently have?
- What are we building, and why?
- What knowledge is available in each repository?
- What has been completed, what remains, and what is blocked?
- Which commercial opportunities should we pursue?
- Which internal tools and frameworks are genuinely necessary?
- How should we prioritize commercial outcomes alongside internal development?
- What should we work on next?
- Are we progressing toward our intended outcomes?
- When should our plans change based on new evidence?

Siddhi combines deterministic data processing with externally supplied intelligence.

It does not attempt to replace project repositories, OpenSpec, OKF, Vyasa, or existing AI assistants. Instead, it connects these systems, produces structured comparisons, maintains portfolio-level decisions and coordinates deeper analysis when necessary.

The application is responsible for organizing information and tracking decisions. External AI tools and coding agents provide additional analysis and recommendations.

## 2. The Problem

Managing many projects creates two related challenges.

### 2.1 Project-level visibility

Project information is distributed across repositories, documentation, requirements, source code, knowledge packages and development history.

Understanding a project's current state may require inspecting its repository using a coding agent or manually gathering information from multiple files.

This makes it difficult to maintain a consistent portfolio-wide view of:

- Existing projects and their purposes.
- Requirements and development tasks.
- Available engineering knowledge.
- Dependencies and shared capabilities.
- Current milestones and outstanding work.
- The evidence supporting reported progress.

### 2.2 Portfolio-level direction

Project-level tracking alone does not determine whether the overall portfolio is progressing toward the desired outcomes.

Internal tools, reusable frameworks and automation can provide significant value. However, building them can also consume attention that might otherwise go toward releasing a product, publishing a novel, producing a film or completing a game.

The problem is not that internal development should stop. The problem is that internal investments and commercial outcomes need to be evaluated together.

A technically successful internal project is not automatically the most valuable next investment.

Siddhi addresses this by connecting project evidence to explicit goals and using external analysis to evaluate alternatives and recommend priorities.

## 3. Product Vision

Create a deterministic, evidence-driven portfolio management platform that connects project discovery, engineering knowledge, development progress and desired outcomes into a continuous planning and review process.

Siddhi should make it possible to move from a high-level objective to the relevant projects, repositories, requirements, knowledge, dependencies and executable work without repeatedly rediscovering information.

The platform should also make it possible to evaluate the portfolio as a whole, including the relationship between internal engineering investments and commercial ambitions.

Its central principle is:

**The application manages structured data, deterministic analysis and the lifecycle of decisions. External AI provides deeper reasoning when required. Existing engineering systems remain the source of truth for their respective information.**

## 4. Core Design Principles

### 4.1 Deterministic by default

Whenever information can be obtained through parsing, explicit rules, templates or database queries, Siddhi should use those mechanisms instead of invoking an AI model.

Examples include:

- Discovering known projects through Vyasa.
- Parsing OpenSpec and OKF artifacts.
- Counting pending tasks from source status.
- Identifying missing documentation.
- Comparing declared milestones with project records.
- Generating standardized reports.
- Detecting changes between successive snapshots.

AI should not be used to perform routine data extraction that can be implemented reliably through ordinary code.

### 4.2 External intelligence when necessary

Siddhi does not need its own reasoning model.

It should prepare evidence and structured analysis requests for external tools such as:

- ChatGPT
- Gemini
- Claude
- Perplexity
- OpenCode
- Claude Code
- Codex

Different tools may be used for strategic analysis, market research, cross-project reasoning or detailed repository investigation.

The platform should not require a single provider.

### 4.3 Evidence before conclusions

Every reported status, comparison and recommendation should distinguish between:

- Information explicitly present in a source.
- Information calculated deterministically.
- Findings produced by external analysis.
- Decisions approved by the owner.
- Results independently verified by an existing test or verification process.
- Information that remains unknown.

Missing information must not be silently interpreted as success or failure.

### 4.4 Commercial and internal work coexist

Siddhi must support both commercial outcomes and internal development.

Commercial work includes software products, games, novels, books, films, music videos and other products or creative works intended for release, distribution or sale.

Internal work includes frameworks, reusable libraries, developer tools, automation, production pipelines and engineering infrastructure.

These are different kinds of initiatives within one portfolio. Neither category should automatically receive priority over the other.

### 4.5 No mandatory time logging

Siddhi should not depend on manual hour logging to determine project progress.

Progress should primarily be derived from OpenSpec, OKF, Git/VCS information, generated artifacts, defined milestones and other available evidence.

The system can track dates, deadlines, elapsed time, review periods and planned milestones without requiring users to log their working hours.

### 4.6 Preserve source ownership

Siddhi should not duplicate the responsibilities of existing tools.

It should reference and ingest source information, maintain the portfolio-specific data it owns, and retain links to the underlying evidence.

Repository changes should happen only through explicit, authorized workflows.

---

## 5. System Context

Siddhi builds on four principal information sources.

### 5.1 Vyasa — Project Discovery

Vyasa is responsible for discovering and tracking projects and repositories.

It supplies information such as:

- Project identity and repository location.
- Git origin and repository metadata.
- Local repository location where available.
- Programming languages and frameworks.
- Documentation availability.
- OpenSpec and OKF configuration status.
- Agent instructions and development tooling.
- CI/CD and other detected capabilities.

Siddhi should consume Vyasa's existing inventory rather than independently maintain a competing project registry.

### 5.2 OpenSpec — Requirements and Development Progress

OpenSpec provides structured information about what a project is building and why.

Siddhi should consume the information available in the actual OpenSpec installation, including:

- Configuration and schemas.
- Proposals and changes.
- Requirements and scenarios.
- Tasks and implementation plans.
- Declared status and completion information.
- Relevant acceptance criteria and dependencies where documented.

OpenSpec remains authoritative for its requirements and change artifacts.

Siddhi should not create a parallel task-management system that competes with OpenSpec.

### 5.3 OKF — Engineering Knowledge

OKF provides the knowledge associated with a project.

Siddhi should consume the actual OKF artifacts and supported metadata, including available information about:

- Knowledge packages and documents.
- Concepts and technical guidance.
- Engineering decisions and rationale.
- Relationships between knowledge items.
- Declared validation status.
- References and dependencies.
- Known knowledge gaps, where explicitly documented.

The exact extraction model must follow the real OKF specification rather than an invented schema.

Knowledge and requirements remain independent. A repository can contain useful knowledge without active requirements, and requirements can exist before the necessary knowledge has been established.

### 5.4 Git and Version Control

Git/VCS information supplies supporting evidence about repository activity and history.

Where available, Siddhi may use:

- Commit references.
- Branches and merge history.
- Tags and releases.
- Changed files.
- Commit timestamps.
- Repository revisions.
- Links between changes and source artifacts.

Git activity is evidence of development activity, not proof of successful delivery.

A high commit count does not necessarily indicate meaningful progress, and a merged change does not automatically demonstrate that a product is ready for release.

---

## 6. High-Level Architecture

Siddhi consists of five logical layers.

### Layer 1 — Source Systems

Existing repositories, Vyasa, OpenSpec, OKF and Git/VCS.

These systems contain project information, requirements, knowledge, development history and source artifacts.

### Layer 2 — Extraction and Ingestion

Deterministic adapters retrieve and parse available information.

Responsibilities include:

- Discovering available source artifacts.
- Parsing supported formats.
- Mapping records to stable project identities.
- Preserving source references.
- Detecting changed artifacts.
- Updating normalized database records.
- Recording ingestion failures and unknown states.

The ingestion process should not invoke a coding agent merely to read an existing structured file.

### Layer 3 — Portfolio Data and Deterministic Analysis

The portfolio database stores normalized project information, objectives, plans, decisions, milestones, analysis records and historical snapshots.

The analysis engine compares available evidence with declared goals using explicit rules and predefined templates.

Examples include:

- Goal-to-project mapping.
- Requirement-to-deliverable mapping.
- Internal capability-to-commercial outcome mapping.
- Missing evidence reports.
- Pending-work summaries.
- Milestone status comparisons.
- Change detection between snapshots.
- Unresolved dependency reports.

### Layer 4 — External Analysis

When deterministic processing cannot adequately answer a question, Siddhi prepares an analysis brief for an external AI service or coding agent.

The external tool may investigate the evidence, compare alternatives, assess opportunities or recommend a revised plan.

Results are returned in a defined format, reviewed as appropriate and stored with their provenance.

### Layer 5 — Portfolio Interface

The application presents:

- Portfolio overview.
- Projects and repositories.
- Objectives and outcomes.
- Internal development initiatives.
- Commercial roadmap.
- OpenSpec task and change summaries.
- OKF knowledge exploration.
- Deterministic comparison reports.
- External analysis reports.
- Plans, milestones and review history.
- Priority recommendations and approved decisions.

The interface should primarily display stored and computed data. It should not independently invent project status or perform hidden analysis during rendering.

---

## 7. Data Ownership

The system must maintain clear ownership boundaries.

| Information | Source of truth |
|---|---|
| Project and repository inventory | Vyasa |
| Requirements, scenarios and change tasks | OpenSpec |
| Engineering knowledge | OKF |
| Repository history and release evidence | Git/VCS |
| Portfolio objectives and priorities | Siddhi |
| Product and initiative plans | Siddhi planning artifacts |
| Deterministic comparison results | Siddhi analysis engine |
| External analysis reports | Saved analysis artifacts in Siddhi, with source references |
| Approved portfolio decisions | Siddhi |
| Actual implementation and test results | Existing project workflows and verification evidence |

Siddhi may maintain indexed or cached copies of source information for querying and visualization. These copies must not become competing authoritative records.

Every imported record should preserve enough provenance to identify its originating project, source artifact and revision where available.

---

## 8. Structured Project Artifacts

Siddhi should use predefined, versioned formats instead of relying on unstructured text for all operations.

The initial artifact types may include the following.

### 8.1 Project Summary

A standardized description of a repository and its purpose, capabilities, technology stack and current state.

### 8.2 Knowledge Inventory

A structured inventory of available OKF knowledge, its categories, relationships and declared status.

### 8.3 Development Summary

A snapshot of relevant OpenSpec changes, requirements, tasks, dependencies and recorded progress.

### 8.4 Goal Definition

A declaration of an intended outcome, including its purpose, target audience, success criteria, constraints and desired timeline.

### 8.5 Initiative Plan

A plan for a commercial outcome or internal development initiative, including scope, milestones, dependencies, assumptions and expected results.

### 8.6 Deterministic Comparison Report

A report comparing declared objectives with available project data and identifying matches, gaps, unresolved relationships and evidence limitations.

### 8.7 Repository Investigation Report

A detailed investigation produced by a coding agent when existing structured information is insufficient.

### 8.8 External Analysis Report

A structured set of findings, assumptions, options, risks and recommendations produced by an external AI tool.

### 8.9 Review Report

A record of the portfolio state at a review point, changes since the previous review, decisions made and subsequent actions.

All formats should include stable identifiers, schema versions and relevant source references. Exact fields and serialization formats must be defined during detailed design.

---

## 9. Portfolio Model

Siddhi should model the relationship between goals, initiatives, projects, capabilities and execution evidence.

### 9.1 Objectives and Goals

An objective represents an intended outcome or strategic direction.

A goal may define a measurable or verifiable result, target date, constraints and success criteria.

Goals can exist before a repository or project has been created.

### 9.2 Commercial Outcomes

Commercial outcomes represent products or creative works intended for release, distribution or sale.

Examples include:

- Software products.
- Games.
- Novels and books.
- Short films and musical videos.
- Publishing catalogues.
- Other creative or commercial offerings.

The scope and expected quality of each outcome should reflect its own objectives, available resources, experience and ambitions.

Siddhi must not impose fixed commercial maturity categories that assume every product follows the same scale or progression.

### 9.3 Internal Initiatives

Internal initiatives represent investments in reusable capabilities, tools, frameworks, automation, production infrastructure and engineering knowledge.

An internal initiative may support multiple commercial outcomes, improve an existing workflow or have independent strategic value.

Its justification should be explicit enough to evaluate its value, dependencies, maintenance burden and opportunity cost.

### 9.4 Projects and Repositories

Projects represent the actual development efforts that produce capabilities or outcomes.

A project may support multiple goals, and a goal may depend on several projects.

Repositories are linked to projects through Vyasa's inventory and the appropriate stable identifiers.

### 9.5 Capabilities and Dependencies

Capabilities represent functionality, knowledge or infrastructure needed by one or more initiatives.

Dependencies describe the relationships between initiatives, deliverables, capabilities and work items.

Siddhi should reuse existing capability information where possible rather than assume that every requirement requires a new project.

---

## 10. Deterministic Analysis Engine

The deterministic engine is a core part of Siddhi.

It should produce repeatable results from defined inputs and rules.

### 10.1 Project Inventory Analysis

Examples:

- List all known projects.
- Identify projects without required artifacts.
- Find repositories with missing or outdated summaries.
- Compare project configurations.
- Identify unknown or stale source information.

### 10.2 OpenSpec Analysis

Examples:

- List changes and their recorded statuses.
- Summarize pending tasks.
- Identify declared dependencies.
- Compare planned milestones with current records.
- Associate documented requirements with portfolio outcomes where explicit mappings exist.

### 10.3 OKF Analysis

Examples:

- Inventory available knowledge packages.
- Group knowledge by supported categories.
- Identify missing references or metadata.
- Map declared knowledge relationships to required capabilities.
- Highlight goals for which relevant knowledge has not been located.

The absence of a knowledge document does not necessarily prove that the underlying capability is absent.

### 10.4 Goal-to-Project Comparison

Compare declared goal requirements against known projects, capabilities, artifacts and milestones.

Each relationship should be classified using explicit rules, for example:

- Explicitly matched.
- Candidate match.
- Missing evidence.
- Unresolved.
- Confirmed gap, where the relevant criteria support that conclusion.

A simple keyword match must not be treated as proof that a requirement is satisfied.

### 10.5 Change Detection

Compare successive snapshots to identify:

- New projects or repositories.
- Added or removed artifacts.
- Changed OpenSpec status.
- New knowledge packages.
- Changed dependencies.
- Revised milestones.
- Updated plans.
- Newly available evidence.

Change detection should support incremental ingestion and focused replanning.

### 10.6 Reproducibility

Deterministic reports should record the input snapshot, rule or template version and generation timestamp.

The same inputs and rule versions should produce consistent results.

---

## 11. External AI and Coding-Agent Integration

Siddhi does not attempt to reproduce the reasoning capabilities of external AI systems.

It provides a consistent workflow for using them.

### 11.1 Supported Analysis Providers

Potential tools include:

- ChatGPT.
- Gemini.
- Claude.
- Perplexity.
- OpenCode.
- Claude Code.
- Codex.

Support may begin with prepared briefs and manually imported reports. Provider APIs, agent execution and other integrations can be added independently.

The architecture must not require all providers to expose identical capabilities.

### 11.2 When to Use External Analysis

External analysis may be required when:

- Comparing commercial opportunities.
- Evaluating whether an internal investment is justified.
- Developing a detailed product plan.
- Resolving ambiguous requirements.
- Evaluating trade-offs between possible approaches.
- Assessing the feasibility of a proposed outcome.
- Revising a roadmap after significant changes.
- Investigating conflicting or incomplete evidence.

### 11.3 When to Use a Coding Agent

A coding agent should be used when an analysis requires detailed repository investigation beyond the available structured data.

Examples include:

- Understanding the actual capabilities of an existing framework.
- Investigating implementation details that are not documented.
- Identifying reusable functionality in a repository.
- Examining whether a deliverable exists in a usable form.
- Producing a detailed repository inventory.
- Gathering evidence needed for a product or architecture decision.

The system should prepare a focused investigation request and specify the expected output format.

The coding agent should save its generated artifact in the designated repository location where appropriate. Siddhi then ingests the artifact and makes the resulting information available for subsequent planning.

### 11.4 Analysis Lifecycle

Every managed analysis should follow a defined lifecycle:

1. Identify the question.
2. Collect relevant existing data.
3. Generate an analysis brief.
4. Select an appropriate external tool.
5. Execute the analysis or export the brief.
6. Import the resulting report.
7. Record provenance, assumptions and unresolved questions.
8. Review the findings.
9. Approve or reject proposed decisions.
10. Update the plan when authorized.

Routine data extraction and standard reporting should not require a coding agent.

### 11.5 Provider Independence

The application should define a common analysis contract rather than depend on a provider-specific response format.

Provider adapters should be replaceable.

The same underlying analysis request should remain usable across different tools, subject to their individual capabilities and access permissions.

---

## 12. Planning and Replanning

Planning is a managed workflow rather than an unstructured conversation.

### 12.1 Initial Planning

The workflow should be:

1. Define the desired outcome or initiative.
2. Gather relevant project and portfolio data.
3. Run deterministic comparisons.
4. Identify missing evidence and unresolved questions.
5. Generate a structured analysis brief.
6. Obtain external analysis.
7. Save the resulting plan and rationale.
8. Review and approve the plan.
9. Associate the plan with relevant projects, milestones and OpenSpec changes.

The resulting plan should contain enough structure to support tracking without duplicating OpenSpec's implementation tasks.

### 12.2 Plan Versioning

Plans should be versioned.

Each version should record:

- Plan identity and version.
- Creation and revision timestamps.
- Relevant evidence snapshot.
- Goals and constraints.
- Milestones and target dates.
- Dependencies and assumptions.
- Recommendations and rationale.
- Approval status.
- Changes from the preceding version.

Previous versions must remain available for comparison.

### 12.3 Replanning

Replanning may be triggered by:

- A significant change in development status.
- A blocked milestone.
- A new dependency.
- A change in available capabilities.
- A changed commercial opportunity.
- A revised objective.
- A significant deviation from the approved plan.
- A scheduled review.

The application should first refresh its data and determine what changed.

It should then decide, through explicit workflow rules, whether a deterministic report is sufficient or whether new external analysis is warranted.

A new plan should not silently overwrite an approved plan. The revised version should preserve the rationale for the change and follow the required approval process.

---

## 13. Weekly and Monthly Reviews

Siddhi should support recurring portfolio reviews without requiring time logging.

### 13.1 Weekly Review

The weekly review focuses on execution and near-term priorities.

It should summarize:

- What changed since the previous review.
- Which OpenSpec tasks or changes progressed.
- Which milestones were reached or missed.
- Which initiatives are blocked.
- Which dependencies changed.
- Whether immediate priorities need adjustment.
- What work should be prioritized next.

A weekly review may use deterministic data alone or request external analysis where judgment is needed.

### 13.2 Monthly Review

The monthly review focuses on the overall portfolio and its strategic direction.

It should evaluate:

- Progress toward commercial outcomes.
- Progress on internal capabilities.
- Whether internal investments are enabling intended outcomes.
- Whether existing projects remain justified.
- Whether goals and assumptions remain valid.
- Whether milestones and target dates require revision.
- Whether important outcomes have been neglected.
- Which opportunities deserve more or less attention.

External analysis can help assess trade-offs and recommend priorities.

The owner remains responsible for approving important changes.

### 13.3 Historical Comparison

Every review should be preserved so that the system can compare:

- Previous and current plans.
- Previous and current project states.
- Expected and actual milestone progression.
- Changes in priorities.
- Decisions and their subsequent outcomes.

The system should not treat a revised target as evidence that the original target was achieved.

---

## 14. Portfolio Prioritization

Siddhi must support a balanced portfolio containing both commercial outcomes and internal initiatives.

It should not impose a universal rule that commercial work always takes precedence or that internal development must stop.

### 14.1 Prioritization Inputs

External analysis should consider relevant evidence such as:

- Strategic importance.
- Commercial opportunity and uncertainty.
- Intended audience or customer needs.
- Time sensitivity.
- Scope and feasibility.
- Available capabilities.
- Dependencies and blocking relationships.
- Expected reuse across initiatives.
- Maintenance and opportunity costs.
- Progress toward existing commitments.
- Available time and resources, where provided.
- Consequences of delaying an initiative.

### 14.2 Internal Investment Evaluation

Internal initiatives should be assessed in relation to their intended value.

The system should help answer:

- Which outcomes benefit from this capability?
- Can the intended outcome proceed with existing tools?
- What is the minimum capability needed now?
- What future scale or complexity would justify additional investment?
- What maintenance costs will the capability introduce?
- Would deferring the work materially affect a planned release?
- Does the investment have independent strategic value?

Possible recommendations include proceeding, reducing scope, deferring, investigating further or discontinuing an initiative.

These are recommendations, not automatic decisions.

### 14.3 Portfolio Balance

The application should expose cases where internal development is progressing while commercial outcomes are stalled or receiving insufficient attention.

It should also recognize cases where an internal investment is the highest-value choice because it enables multiple outcomes.

The objective is to make trade-offs visible and deliberate.

### 14.4 Recommendation Provenance

Every external prioritization recommendation should record its rationale, supporting evidence, assumptions, unresolved questions and review status.

The application should distinguish the external recommendation from the owner's approved priority.

---

## 15. Database and Ingestion Requirements

The database is an operational representation of the portfolio, not the authoritative home for every project artifact.

### 15.1 Ingestion

The ingestion pipeline should:

- Fetch available structured data from known sources.
- Parse supported formats deterministically.
- Normalize records.
- Preserve stable identities.
- Track source revisions and hashes where available.
- Update changed records without duplicating them.
- Record ingestion failures.
- Represent unknown or unavailable information explicitly.

### 15.2 Incremental Updates

The application should avoid unnecessarily reprocessing unchanged artifacts.

Where feasible, it should compare source revisions or content hashes and update only affected records.

### 15.3 Source References

Imported records should preserve relevant source paths, repository identity, revision information and links to source artifacts.

Users should be able to navigate from a portfolio view to the original evidence.

### 15.4 Historical Snapshots

The application should preserve sufficient historical information to support plan comparisons, review reports and explanations of changes over time.

### 15.5 Data Quality

The ingestion system should distinguish:

- Successfully parsed.
- Missing.
- Unsupported format.
- Stale.
- Invalid.
- Incomplete.
- Not yet scanned.

It should not silently convert parsing errors into empty or successful records.

---

## 16. User Interface

The interface should make the portfolio easy to understand without requiring users to read every repository document.

### 16.1 Portfolio Dashboard

Display:

- Active objectives.
- Commercial outcomes and internal initiatives.
- Current priorities.
- Upcoming milestones.
- Blocked and stalled work.
- Recent progress.
- Unresolved decisions.
- Latest review results.
- Analysis requests awaiting attention.

### 16.2 Project Explorer

Allow navigation through:

- Projects and repositories.
- OpenSpec changes and tasks.
- OKF knowledge packages.
- Available project summaries.
- Repository investigation reports.
- Source evidence and revisions.

### 16.3 Goal and Outcome Views

For each goal, display:

- Intended result.
- Current plan.
- Linked projects.
- Required capabilities.
- Milestones.
- Dependencies.
- Relevant OpenSpec changes.
- Related OKF knowledge.
- Deterministic gap reports.
- External recommendations.
- Approved decisions and review history.

### 16.4 Internal Initiative Views

Display the purpose, beneficiaries, expected capabilities, dependencies, maintenance considerations and related outcomes of each internal initiative.

### 16.5 Analysis Workspace

Provide a workspace for:

- Reviewing deterministic findings.
- Preparing analysis briefs.
- Selecting an external analysis tool.
- Importing reports.
- Comparing recommendations.
- Reviewing assumptions.
- Approving decisions.
- Requesting further investigation.

### 16.6 Roadmap and Review Views

Provide timeline, milestone and dependency visualizations, alongside weekly and monthly review reports.

Visual progress should be derived from defined source data and milestone criteria, not arbitrary percentages.

---

## 17. Security and Permissions

Siddhi may handle private repositories, unpublished creative works, commercial plans, credentials-related metadata and confidential technical information.

The design must therefore include:

- Secure storage of any credentials used for integrations.
- Least-privilege repository access.
- Explicit authorization before repository modifications.
- Controlled export of data to external AI providers.
- Clear identification of which files and information are included in an analysis brief.
- Protection of private source code and unpublished creative material.
- Audit records for important data changes and approvals.
- Safe handling of untrusted repository content and generated reports.

External analysis must use only the information authorized for the selected tool.

The application should not assume that all project data can be sent to every provider.

Repository modifications and significant portfolio decisions should require explicit authorization under the relevant workflow.

---

## 18. Non-Goals

Siddhi is not intended to:

1. Replace Vyasa's project-discovery responsibilities.
2. Replace OpenSpec's requirements and change-management workflows.
3. Replace OKF's engineering knowledge system.
4. Replace Git or the project's existing verification tooling.
5. Become a duplicate task-management system.
6. Require manual logging of working hours.
7. Implement its own foundational reasoning model.
8. Invoke coding agents for routine extraction or reporting.
9. Autonomously rewrite repository requirements or knowledge.
10. Treat AI recommendations as verified facts.
11. Force every project into the same maturity stages.
12. Automatically prioritize commercial work over every internal investment.
13. Claim that a project is successful merely because its tasks or documentation are complete.
14. Require all external AI providers to be integrated through APIs in the initial release.

---

## 19. Implementation Roadmap

Implementation should proceed incrementally, with deterministic data foundations established before advanced planning features.

### Phase 1 — Source Integration

- Inspect the actual Vyasa data contract.
- Inspect the installed OpenSpec format and configuration.
- Inspect the actual OKF specification and artifact formats.
- Define stable project and repository identities.
- Implement deterministic extraction and ingestion.
- Preserve source references and revision information.
- Establish the portfolio database and data-quality reporting.

**Exit criteria:** Siddhi can retrieve, normalize and display the supported source information without using an AI agent for routine extraction.

### Phase 2 — Portfolio Model

- Define objectives, goals and initiatives.
- Model relationships between projects and outcomes.
- Define portfolio planning artifacts.
- Support commercial and internal initiatives.
- Implement source-linked project views.
- Add historical snapshots.

**Exit criteria:** Goals can exist independently of repositories, and projects and capabilities can be linked to multiple outcomes.

### Phase 3 — Deterministic Analysis

- Implement goal-to-project comparisons.
- Implement knowledge and requirement inventory reports.
- Identify missing evidence and unresolved mappings.
- Generate standardized summaries from templates.
- Implement change detection and repeatable reports.

**Exit criteria:** The application can produce useful portfolio reports without external AI.

### Phase 4 — Planning and External Analysis

- Define analysis request and report schemas.
- Generate context-specific analysis briefs.
- Support importing reports from external AI tools.
- Support structured repository investigation artifacts.
- Track analysis provenance and approval status.
- Version plans and preserve previous decisions.

**Exit criteria:** External analysis can be incorporated into the portfolio without making the application dependent on one provider.

### Phase 5 — Reviews and Prioritization

- Implement weekly review reports.
- Implement monthly portfolio reviews.
- Compare planned and current states.
- Record approved priorities.
- Support milestone and roadmap revisions.
- Identify when additional analysis is warranted.

**Exit criteria:** Siddhi supports a repeatable planning, execution and review cycle.

### Phase 6 — Advanced Integrations

- Add provider-specific adapters where justified.
- Automate selected analysis workflows.
- Improve cross-project dependency visualization.
- Support additional analysis and review triggers.
- Introduce more advanced portfolio comparison capabilities.

**Exit criteria:** Integrations improve efficiency without compromising the deterministic core or source ownership boundaries.

---

## 20. Initial Acceptance Criteria

The first useful version of Siddhi should satisfy the following conditions.

### Source integration

- It can retrieve project information from Vyasa.
- It can parse supported OpenSpec artifacts.
- It can parse supported OKF artifacts.
- It can associate records with the correct project and repository.
- It preserves source references.
- It reports missing, unsupported and invalid data explicitly.

### Deterministic processing

- Standard project reports are generated from templates.
- The same source snapshot and rule versions produce consistent reports.
- Goal-to-project comparisons identify evidence and unresolved mappings.
- Routine extraction does not invoke external AI.
- The system can detect relevant changes between successive snapshots.

### Planning

- Goals can be created before a repository exists.
- Commercial and internal initiatives can coexist in the same portfolio.
- Plans can reference projects, capabilities, milestones and OpenSpec changes.
- Plans can be versioned and compared.
- Previous decisions remain accessible.

### External analysis

- Analysis briefs can be generated from available evidence.
- Reports can be imported and linked to their source requests.
- Recommendations remain distinct from approved decisions.
- Coding-agent investigation is reserved for cases requiring deeper repository evidence.
- Provider-specific integration is not required for the initial release.

### Reviews

- Weekly and monthly reports can be generated from available data.
- The system distinguishes source progress from plan revisions.
- It can identify stalled commercial outcomes and internal initiatives.
- It supports portfolio-wide prioritization without a fixed rule that one initiative category must always win.

---

## 21. Open Design Decisions

The following decisions should be settled through detailed design rather than assumed in this README.

1. **Technology stack:** Select the implementation stack based on the existing environment and integration requirements.
2. **Database:** Choose the storage technology and schema after defining the data model and historical-query requirements.
3. **OKF extraction contract:** Confirm the actual OKF format and supported metadata.
4. **Vyasa integration:** Determine whether Siddhi consumes an existing API, MCP interface, generated artifact or a combination.
5. **Plan artifact location:** Define which planning artifacts live only in Siddhi and which must also be published to project repositories.
6. **External analysis workflow:** Decide the initial balance between manual export/import and provider-specific automation.
7. **Priority evaluation:** Define the structured inputs and output format for external recommendations without hard-coding a universal scoring model prematurely.
8. **Review cadence:** Establish default weekly and monthly review behavior and how missed reviews are handled.
9. **Permissions:** Define repository access, external data-sharing permissions and approval boundaries.
10. **Data retention:** Define the retention policy for snapshots, analysis reports and superseded plans.

These decisions should be documented in the relevant architecture, functional requirements, data model and security documents.

---

## 22. Summary

Siddhi is a portfolio intelligence and strategic planning system built around deterministic data processing and externally supplied reasoning.

Vyasa identifies the projects and repositories. OpenSpec provides requirements and development status. OKF provides engineering knowledge. Git/VCS provides supporting development evidence.

Siddhi connects these sources to goals, commercial outcomes and internal investments. It uses predefined formats and deterministic rules to collect information, compare the current state against intended outcomes and generate repeatable reports.

When deeper judgment is needed, Siddhi prepares structured analysis requests for external AI tools or coding agents. Their findings are saved, reviewed and incorporated into versioned plans and approved decisions.

Weekly and monthly reviews close the loop by comparing updated evidence with previous plans and identifying where priorities or timelines should change.

**The intended result is not simply better project tracking. It is a disciplined system for turning available capabilities, engineering effort and strategic intent into completed and released outcomes while continuing to invest in the internal tools that genuinely enable them.**
