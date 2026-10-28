---
type: Product
title: Siddhi scope and proposed roadmap
description: Local-first backend responsibilities, exclusions, dependency-aware sequencing, and unresolved release boundaries.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Scope and proposed roadmap

Siddhi's proposed backend consolidates engineering evidence, maintains
portfolio-owned information, and exposes analysis and planning operations to
independent clients. The roadmap below is a sequencing hypothesis, not a
release commitment, approval record, or claim of implemented capability.

# Responsibility boundaries

Siddhi owns goals, intended outcomes, priorities, initiatives, portfolio
relationships, constraints, plans, milestones, reviews, analysis history,
recommendation records, and explicit portfolio decisions. It maintains
attributable projections of external observations, not replacement source
records. The distinction is detailed in
[data ownership](../architecture/data-ownership.md).

The intended sources are Vyasa for project inventory, OpenSpec for development
artifacts, OKF for engineering knowledge, Git for revision observations, and
explicitly supported repository or verification artifacts. Actual interfaces,
format versions, capabilities, and access methods need confirmation. External
AI supplies optional attributed analysis rather than source authority.

# Capability areas

**Portfolio operations:** represent goals before projects, many-to-many
contributions between goals and initiatives, constraints, priorities, assumptions,
and links to existing projects. Avoid a fixed taxonomy that determines lifecycle.

**Ingestion:** discover, retrieve, detect formats, parse, normalize, identify,
compare, and capture source observations. Preserve revision or hash information
where available, historical context, warnings, and scope. Failed refreshes leave
last-known data visibly qualified rather than masquerading as current data.

**Intelligence and deterministic analysis:** expose what artifacts and revision
evidence are available; identify candidate relationships, explicit gaps,
dependencies, and changes. A keyword match is not outcome satisfaction, and
artifact presence is not completeness or correctness.

**Planning and review:** retain meaningful plan revisions, milestones, target
dates, dependencies, execution reviews, strategic reviews, and approval rationale.
Weekly execution and monthly strategic reviews are proposed cadences, not
mandatory properties of every initiative.

**External analysis:** assemble a bounded evidence brief, export it, import a
structured result, validate its structure and references, and retain assumptions,
uncertainty, and origin. Review precedes explicit decisions. Provider automation
is optional and distinct from this controlled handoff.

**Client interface:** provide documented, testable HTTP contracts for supported
operations, independently of a future desktop presentation layer.

# Technical direction

The proposed starting point is a local Python modular monolith with FastAPI,
Pydantic validation, SQLite, a persistence boundary, versioned migrations, and
automated domain, adapter, persistence, and interface tests. A future separate
React/TypeScript/MUI/Electron application consumes the backend interface.

These technology choices remain proposals. Domain and deterministic rules do
not depend on the desktop framework. Repository access is explicitly configured;
remote access need not imply unnecessary clones. Startup, packaging, security,
backup, and recovery still require design despite the local operating model.

# Proposed dependency-aware sequence

| Stage | Useful capability and rationale | Indicative completion evidence |
|---|---|---|
| Design baseline | Establish purpose, ownership, domain, integration assumptions, risks, and open decisions | Critical assumptions and boundaries are understood |
| Backend foundation | Configuration, startup, health, persistence, migrations, diagnostics, interface documentation, automated checks | Reliable startup and durable local operations |
| Source ingestion | Confirmed adapters, identity mapping, normalization, provenance, snapshots, comparisons, explicit limitations | Repeatable capture without corrupting last-known state |
| Portfolio and deterministic analysis | Goals, contributions, milestones, comparisons, gaps, summaries, historical reports | A goal-to-evidence report explains its findings and uncertainty |
| Planning and decisions | Versioned plans, reviews, dependencies, explicit decisions and rationale | Revision without loss of history or implicit approval |
| External strategic analysis | Bounded briefs, structured results, review, optional provider adapters | Recommendations remain traceable and separate from decisions |
| Desktop readiness | Compatible contracts, local access controls, lifecycle, origin policy, backup, packaging | Predictable operation by a separate local client |

Operational safety is not deferred merely because desktop readiness is listed
last. Appropriate access and recovery controls apply as soon as data is retained
or an interface is exposed.

# Smallest useful path

A proposed first useful path discovers a project through Vyasa, captures supported
engineering and Git observations with a historical snapshot, defines a goal
independently, compares that goal with evidence using explicit rules, and retains
an explainable report. Refresh and comparison demonstrate continuing value.

This favours a small complete workflow over nominal coverage of every capability.
Exact source coverage, whether planning belongs in that release, and the minimum
domain structure remain open. No entire roadmap stage is automatically one release.

# Explicit exclusions

- Recreating task, sprint, issue, or collaboration platforms.
- Mandatory time tracking or inferring exact hours from activity.
- Automatic repository edits, commits, publication, or source-status changes.
- Autonomous prioritization or model output becoming binding plans.
- AI dependency for ordinary capture, comparison, or reports.
- Premature multi-tenancy, distributed services, or compulsory hosting.
- Universal product maturity and claims of readiness without applicable evidence.

# Risks and scope discipline

Assumed source contracts risk incorrect parsing; support detected, confirmed
formats. Staleness and declared progress risk false confidence; expose limitations
and separate declarations from applicable verification. Source content can carry
misleading instructions; treat it as data, not authority to execute actions.
Snapshot growth and privacy conflict with unlimited historical retention;
choose retention deliberately. Owner-controlled decisions and bounded increments
limit AI overreach and excessive investment in Siddhi itself.

A scope addition should explain the portfolio problem, expected benefit,
evidence of need, dependencies, existing ownership, maintenance cost, and whether
it is needed now. Internal reuse and commercial potential both need context,
not automatic priority.

# Open questions

Confirm essential sources, real Vyasa capabilities, supported source formats,
local-checkout versus remote-only coverage, minimum entities, evidence thresholds,
snapshot retention, local API security, export/recovery needs, and measurable
usefulness before treating affected proposals as settled.

Related: [vision](vision.md), [system architecture](../architecture/system-architecture.md),
[workflow coordination](../architecture/workflow-coordination.md).