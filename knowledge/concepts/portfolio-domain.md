---
type: Concept
title: Portfolio domain
description: Meanings and relationships of goals, outcomes, initiatives, project references, plans, reviews, and decisions.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Portfolio domain

The portfolio model connects desired results to coordinated investments and
available evidence. It is independent of transport, persistence technology,
source format, and user interface. Product types describe work; they do not
select one compulsory maturity model.

# Intent and contribution

| Concept | Meaning | Important boundary |
|---|---|---|
| Goal | A desired strategic result and reason to invest attention | Can exist before any project or plan |
| Intended outcome | A specific observable result sought by a goal | Distinct from observed result and its assessment |
| Initiative | Coordinated work contributing to one or more goals | Can span projects or exist without a repository |
| Project reference | A source-aware reference to an externally inventoried project | Not a new independently maintained project authority |
| Priority | Owner-controlled relative importance with rationale | Not an automatically authoritative ranking |
| Constraint | A declared condition shaping choices | Different from an inferred assumption |
| Assumption | An unestablished proposition used for planning | Needs review; not silently promoted to fact |

A goal such as publishing a novel can have outcomes for distribution and an
optional commercial result. A reusable capability initiative can support several
product goals. The same project can contribute to multiple initiatives and goals;
linking it expresses relevance, not achievement.

Outcomes can be qualitative, quantitative, or demonstrated through evidence.
Measurements may carry definitions, baselines, targets, units, and dates. A book's
availability and a software capability demonstration need not share assessment
criteria. Revenue, sales, readership, and cost are optional observations; absence
of a commercial source is not permission to invent a value.

Goals can be recorded before their criteria are complete, but an underdefined
goal cannot yet support a meaningful achievement assessment. Whether every goal
eventually needs an explicit outcome, and whether some may remain intentionally
qualitative and outcome-free, remain open modeling choices.

# Planning concepts

A **plan** is a proposed approach for a goal or initiative, not an implementation
record. A **plan revision** captures a particular arrangement of outcomes,
milestones, dependencies, constraints, assumptions, risks, and proposed actions.
Revision origin, predecessor, change summary, and rationale explain how the
approach changed. A newer draft does not implicitly replace an approved revision.

A **milestone** is a significant checkpoint assessable against explicit criteria.
Its target date, dependencies, completion declaration, and evidence are different
facts. A passed date means overdue relative to a plan, not failed outcome;
declared completion does not prove verification.

A **dependency** expresses a directed prerequisite: one item depends on another
capability, milestone, initiative, or approval. Preserve type, rationale, and
whether the relationship is declared or merely suggested. Some dependency types
need acyclic structure; not every relation is a scheduling edge.

Historically meaningful milestones and targets need revision context. Whether
milestones have immutable revision membership, stable identities with versioned
attributes, or another historical representation remains unresolved.

# Review and governance

A **review** is a bounded examination of evidence, plans, assumptions, and choices.
Execution review focuses on near-term milestones and blockers; portfolio review
focuses on investment balance, opportunities, neglected goals, and trade-offs.
Weekly and monthly are proposed cadences, not fixed properties of review entities.
Reviews retain the plan revisions and evidence examined even after a refresh.

A **recommendation** proposes an action such as build, reuse, continue, defer,
investigate, or stop. It carries rationale, alternatives, assumptions, and
uncertainty where available. It can originate from a person, explicit rule,
or external strategic analysis.

A **decision** is an explicit choice by an authorized decision-maker, with issue,
selected option, authority, time, rationale, and affected context. Receiving or
viewing a recommendation does not approve it. Accepting one needs a linked choice;
execution of that choice needs separate evidence. Superseding or reversing a
decision preserves the original context rather than silently editing history.

# Relationship design

- One goal can have several independently assessed outcomes.
- Goals and initiatives can contribute many-to-many; initiatives and projects
  likewise need not have exclusive membership.
- Direct project-to-goal links are a proposed lightweight path, avoiding a forced
  initiative wrapper. Their availability remains a product-model review point.
- A plan has revisions; reviews examine particular revisions, not a floating
  “latest” state. A decision may authorize a revision without demonstrating execution.
- One observation can support several assessments, but sufficiency is evaluated
  separately for each criterion and goal.

Associations deserve their own identity or history when they carry rationale,
approval, effective dates, or provenance. Deleting a link does not delete the
independently owned entities at its ends.

# Lifecycle vocabulary is contextual

Proposed goal states include proposed, active, on hold, achieved, abandoned, and
superseded. Initiatives may additionally be planned, paused, deferred, completed,
cancelled, or archived. Plans distinguish draft, review, approval, and supersession;
recommendations distinguish pending review, acceptance, rejection, deferral, and
investigation. These are illustrative sets, not agreed transitions or a universal
enum. Goal achievement and milestone completion require separately defined policies.

Archival removes a record from active work without invalidating its historical
references. It does not imply failure, source deletion, or automatic archival of
related goals. Hard deletion and retention-policy deletion are separate operations.

# Direction and open questions

Goals before repositories, outcome-oriented evaluation, explicit uncertainty,
independent source domains, human decision control, historical context, and no
mandatory timesheets are established direction. Detailed entity cardinalities,
state transitions, approval roles, custom criteria, partial outcome semantics,
direct-link policy, and commercial measurement representation remain proposals.
This draft asserts no human verification or implementation status.

Related: [evidence semantics](evidence-semantics.md),
[logical data model](../architecture/data-model.md),
[workflow coordination](../architecture/workflow-coordination.md).