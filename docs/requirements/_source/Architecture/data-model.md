# Data Model

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `data-model.md`  
**Status:** Draft for review  
**Scope:** Logical data model for the Siddhi API  
**Design principle:** Preserve source authority, provenance, history, and the separation between evidence, assessment, recommendation, and decision.

---

## 1. Purpose

This document defines the logical data model used by Siddhi to maintain portfolio goals, planning information, external source references, evidence, analysis, and decisions.

It describes:

- The information Siddhi must persist.
- The entities and relationships between them.
- Identity and reference strategies for external systems.
- Historical versioning and provenance.
- The separation of source data from derived information.
- Data integrity and lifecycle rules.
- Logical constraints that future database schemas must enforce.

This is a logical model, not a final SQL schema. Database tables, indexes, serialization formats, ORM mappings, and migration scripts will be designed after the model is reviewed and the unresolved decisions are settled.

## 2. Modeling principles

### 2.1 Siddhi owns only its own domain records

Siddhi owns its goals, intended outcomes, initiatives, plans, priorities, reviews, decisions, and analysis history.

It does not own the underlying project inventory, requirements, engineering knowledge, source code, or verification results held by external systems.

### 2.2 External entities are referenced, not duplicated as authorities

Siddhi may maintain a normalized representation of external information for analysis. Each representation must remain linked to its source identity and observation history.

A local copy must not be mistaken for the current authoritative source record.

### 2.3 Observations and assessments are separate

A source observation records what Siddhi obtained or derived from a source at a particular time.

An assessment interprets one or more observations against a goal, outcome, or criterion.

An assessment may change when evidence, rules, or interpretation changes. That must not require rewriting the original observation.

### 2.4 Historical records are first-class data

Siddhi must be able to explain what it knew, which sources it consulted, which rules it applied, and which decisions were made at a particular point in time.

Important revisions should create history rather than silently overwrite the only copy of the previous state.

### 2.5 Unknown is a valid state

Missing, inaccessible, stale, conflicting, or insufficient information must not be forced into a binary success/failure classification.

The model must support uncertainty explicitly.

### 2.6 Relationships do not imply lifecycle coupling

A Siddhi goal can reference a project without requiring an initiative. An initiative can reference several projects. An OKF knowledge artifact can exist without an OpenSpec requirement.

Deleting or archiving one record must not automatically delete independently owned records linked to it.

## 3. Logical model overview

The model is organized into seven logical areas.

<box border radius="lg" padding={3} gap={3}>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **A. Portfolio domain**

    <text size="sm">Goal · Intended Outcome · Initiative · Project Reference · Priority · Constraint</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **B. Planning and governance**

    <text size="sm">Plan · Plan Revision · Milestone · Dependency · Review · Decision · Decision Revision</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **C. Source integration**

    <text size="sm">Source System · Source Artifact Reference · Ingestion Run · Source Snapshot · Normalized Record</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **D. Evidence and assessment**

    <text size="sm">Evidence Record · Evidence Assessment · Assessment Criterion · Analysis Run · Finding</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **E. Reporting and external analysis**

    <text size="sm">Analysis Report · External Analysis Request · External Analysis Result · Recommendation</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **F. Operations**

    <text size="sm">Refresh Job · Processing Error · Adapter Version · Data Quality Observation</text>
  </box>
  <box background="surface-secondary" radius="md" padding={3} gap={1}>
    **G. Cross-cutting records**

    <text size="sm">Stable IDs · Provenance · Audit Events · Record Versions · Relationships · Retention Metadata</text>
  </box>
</box>

These are logical groupings. They do not require separate services, databases, or Python packages for every category.

## 4. Portfolio domain entities

### 4.1 Goal

A **Goal** represents a strategic intention or desired change that Siddhi tracks over time.

Examples might include delivering a commercial product, improving engineering capability, validating a creative product concept, or establishing an internal tool that enables multiple downstream initiatives.

A goal should not be required to fit a universal product category or maturity lifecycle.

Core attributes:

| Attribute | Meaning |
|---|---|
| `goal_id` | Stable Siddhi identifier |
| `title` | Human-readable name |
| `description` | Explanation of the intended strategic change |
| `goal_type` | Optional user-defined classification |
| `status` | Current declared lifecycle status |
| `priority_id` | Optional link to a portfolio priority |
| `created_at` | Creation timestamp |
| `updated_at` | Latest material update |
| `archived_at` | Optional archival timestamp |
| `created_by` | User or process responsible for creation, where available |

A goal may have one or more intended outcomes. The model should not require every goal to have a measurable outcome at creation time, but it should identify goals that cannot yet be assessed meaningfully.

A goal's status is a declared planning state. It is not itself evidence that the goal has been achieved.

### 4.2 Intended Outcome

An **Intended Outcome** describes a result that would provide evidence of progress toward a goal.

Core attributes:

- `outcome_id`
- `goal_id`
- `title`
- `description`
- `measurement_definition`, where applicable
- `target_value`, where applicable
- `unit`, where applicable
- `baseline_value`, where applicable
- `target_date`, where applicable
- `status`
- `created_at`
- `updated_at`

An outcome may be quantitative, qualitative, or evidence-based.

Not every outcome needs a numerical target. For example, a goal may require a technical capability to be demonstrated or an assumption to be validated.

Measurement definitions and target revisions should be versioned when changes would materially affect how progress is assessed.

### 4.3 Initiative

An **Initiative** represents a coordinated body of work intended to advance one or more goals.

Core attributes:

- `initiative_id`
- `title`
- `description`
- `status`
- `owner_reference`, where available
- `start_date`, where applicable
- `target_date`, where applicable
- `created_at`
- `updated_at`
- `archived_at`, where applicable

Initiatives may group work across multiple projects. A project may also contribute directly to a goal without belonging to a Siddhi initiative.

Initiative status must not automatically determine goal status.

### 4.4 Goal and initiative relationships

The model should support these relationships:

- One goal to many intended outcomes.
- Many goals to many initiatives.
- Many goals to many external project references.
- Many initiatives to many external project references.
- Direct project-to-goal relationships even when no initiative exists.

The direct project-to-goal relationship is important because the portfolio model should not force every piece of work through an extra planning entity.

Relationship records should include, where useful:

- Relationship type.
- Rationale.
- Creation timestamp.
- Optional effective dates.
- Optional declared owner.
- Lifecycle status.

A relationship should be independently maintainable without modifying the referenced source project.

### 4.5 Project Reference

A **Project Reference** represents a project discovered through an external source, particularly Vyasa.

It is not the authoritative project record.

Core attributes:

- `project_reference_id` — stable Siddhi identifier.
- `source_system_id` — source that supplied the reference.
- `source_artifact_id` — external project identity.
- `display_name` — latest normalized name.
- `last_observed_at` — latest successful observation.
- `availability_status` — whether the source reference is currently resolvable.
- `metadata_snapshot_id` — optional link to the latest applicable observation.

Siddhi should avoid creating multiple project references for the same external project when a reliable source identity is available.

Names, repository paths, and URLs may change. They must not be used as permanent identities unless the source system defines them as stable identifiers.

### 4.6 Portfolio Priority

A **Portfolio Priority** represents a strategic preference or ranking used when evaluating competing opportunities.

Core attributes:

- `priority_id`
- `name`
- `description`
- `priority_method`
- `priority_value` or `rank`, where applicable
- `effective_from`
- `effective_until`, where applicable
- `rationale`

The model should support both ordered priorities and richer assessment methods without requiring every portfolio to use a single universal scoring formula.

Priority revisions should preserve history. A later ranking must not erase the earlier strategic context.

### 4.7 Constraint and Assumption

A **Constraint** records a limitation that affects planning or decision-making, such as budget, available capacity, a technical restriction, or a dependency.

An **Assumption** records a proposition currently accepted for planning purposes but not yet established as fact.

Suggested common attributes:

- Stable identifier.
- Title and description.
- Type.
- Scope.
- Status.
- Source or author.
- Validity period, where relevant.
- Rationale.
- Last reviewed timestamp.

Constraints and assumptions should be linked to the goals, initiatives, plans, or decisions they affect.

An assumption should be capable of being validated, invalidated, superseded, or left unresolved. It must not be silently promoted to a verified fact.

## 5. Planning and governance entities

### 5.1 Plan

A **Plan** describes an intended approach for advancing a goal or initiative.

Core attributes:

- `plan_id`
- `title`
- `scope_type`
- `scope_id`
- `status`
- `current_revision_id`
- `created_at`
- `updated_at`

A plan may apply to a goal, an initiative, or another explicitly supported planning scope.

### 5.2 Plan Revision

A **Plan Revision** captures a particular version of a plan.

Core attributes:

- `plan_revision_id`
- `plan_id`
- `revision_number`
- `content` or structured plan representation
- `created_at`
- `created_by`
- `change_summary`
- `rationale`
- `supersedes_revision_id`, where applicable

Revisions preserve how the intended approach changed over time.

Siddhi should distinguish an approved plan revision from a draft or proposed revision. Creating a new revision must not automatically make it approved.

### 5.3 Milestone

A **Milestone** represents a significant checkpoint or expected result within a plan.

Core attributes:

- `milestone_id`
- `title`
- `description`
- `plan_id`
- `target_date`, where applicable
- `status`
- `completion_criteria`
- `created_at`
- `updated_at`

A milestone may be associated with one or more intended outcomes and evidence assessments.

A milestone marked complete is a planning record, not proof that the underlying result has been verified.

### 5.4 Dependency

A **Dependency** represents a relationship in which progress or completion of one item depends on another.

It may connect supported entities such as:

- Goals.
- Initiatives.
- Milestones.
- Other planning records.

Core attributes:

- `dependency_id`
- `dependent_entity_type`
- `dependent_entity_id`
- `prerequisite_entity_type`
- `prerequisite_entity_id`
- `dependency_type`
- `status`
- `rationale`

Dependency types and permitted combinations should be explicitly defined. The model should reject invalid self-dependencies and detect cycles where the selected dependency type requires an acyclic graph.

External project dependencies should be represented as references rather than copied into Siddhi as owned projects.

### 5.5 Review

A **Review** records a structured examination of progress, evidence, assumptions, plans, or decisions.

Core attributes:

- `review_id`
- `review_type`
- `scope_type`
- `scope_id`
- `review_date`
- `reviewer_reference`, where available
- `summary`
- `findings`
- `created_at`

A review may refer to an analysis report and a specific plan revision.

The review record must preserve the context examined. A future assessment may differ, but that should not rewrite the historical review.

### 5.6 Decision and Decision Revision

A **Decision** records a deliberate choice made by an authorized person or process.

Examples include approving a priority, selecting a plan, accepting a recommendation, or deciding to stop an initiative.

Core attributes:

- `decision_id`
- `title`
- `scope_type`
- `scope_id`
- `decision_status`
- `decision_maker_reference`
- `decided_at`
- `rationale`
- `supersedes_decision_id`, where applicable

A **Decision Revision** or equivalent immutable decision event should preserve changes to the decision and its rationale.

The model must distinguish proposed, approved, rejected, superseded, and withdrawn decisions where those states are applicable.

A recommendation and its acceptance must remain separate records linked by an explicit relationship. AI output cannot create an approved decision merely by being stored.

## 6. Source integration entities

### 6.1 Source System

A **Source System** identifies an external system from which Siddhi obtains information.

Examples include Vyasa, OpenSpec, OKF, Git, and a build or test reporting system.

Core attributes:

- `source_system_id`
- `source_type`
- `display_name`
- `configuration_reference`
- `adapter_name`
- `adapter_version`
- `enabled_status`
- `created_at`
- `updated_at`

Secrets and credentials must not be stored directly in ordinary source metadata records. The source record should reference an approved credential mechanism where necessary.

A source system may contain many projects, repositories, documents, or other source artifacts.

### 6.2 Source Artifact Reference

A **Source Artifact Reference** identifies a record, document, repository, requirement, knowledge artifact, or verification result within a source system.

Core attributes:

- `source_artifact_id` — stable Siddhi-side identifier.
- `source_system_id`
- `external_identifier`
- `artifact_type`
- `display_name`
- `canonical_locator`, where available.
- `first_observed_at`
- `last_observed_at`
- `availability_status`

The pair of source-system identity and stable external identifier should be used for identity resolution where supported.

If an external source has no stable identifier, Siddhi may use a documented composite identity strategy. Ambiguous matches must be preserved as unresolved rather than automatically merged.

Source references should support renaming and relocation without losing historical identity.

### 6.3 Ingestion Run

An **Ingestion Run** represents a bounded attempt to read and process information from one or more source scopes.

Core attributes:

- `ingestion_run_id`
- `source_system_id`
- `scope_definition`
- `started_at`
- `completed_at`
- `run_status`
- `adapter_version`
- `records_discovered`
- `records_processed`
- `records_skipped`
- `records_failed`
- `error_summary`

Run statuses should distinguish successful completion from partial completion, failure, cancellation, and other applicable outcomes.

A successful individual record parse does not imply that the whole source scan was complete.

### 6.4 Source Snapshot

A **Source Snapshot** represents an observation of source information at a particular point in time.

Core attributes:

- `source_snapshot_id`
- `source_artifact_id`
- `ingestion_run_id`
- `observed_at`
- `source_revision`, where available.
- `content_hash`, where appropriate.
- `payload_reference` or normalized snapshot content.
- `capture_status`
- `schema_or_format_version`

Snapshots support historical comparisons and help explain which source state informed a finding.

The model should support partial observations and explicitly distinguish an unavailable snapshot from a valid empty result.

Snapshot payload storage may be implemented separately from snapshot metadata. This allows storage strategy to change without changing the logical identity of a snapshot.

### 6.5 Normalized Record

A **Normalized Record** represents structured information derived from a source snapshot for use in Siddhi.

It may contain normalized project metadata, requirement summaries, knowledge metadata, Git observations, or verification results.

Core attributes:

- `normalized_record_id`
- `source_snapshot_id`
- `record_type`
- `normalization_version`
- `normalized_payload`
- `created_at`

Normalized records must retain provenance to their input snapshot and transformation version.

They are derived representations, not replacements for source records.

Where practical, normalization should be deterministic for identical inputs and the same normalization version.

### 6.6 Source identity and versioning

Source identity and source revision are separate concepts.

An artifact may keep the same identity while its content changes. Conversely, it may be renamed or relocated while retaining the same identity.

Siddhi should therefore track:

- Stable artifact identity.
- Source revision or version, if available.
- Observation time.
- Content fingerprint, where appropriate.
- Locator changes.
- Availability changes.

A content hash can help detect change, but it does not prove semantic equivalence or correctness.

## 7. Evidence and assessment entities

### 7.1 Evidence Record

An **Evidence Record** captures an observation that may support or challenge a claim about a goal, outcome, initiative, milestone, or decision.

Examples include a requirement's declared status, a knowledge artifact's existence, a commit observation, or a test result associated with a particular revision.

Core attributes:

- `evidence_id`
- `evidence_type`
- `source_artifact_id`, where applicable.
- `source_snapshot_id`, where applicable.
- `normalized_record_id`, where applicable.
- `observed_at`
- `recorded_at`
- `claim_or_observation`
- `evidence_payload` or structured attributes.
- `derivation_method`
- `derivation_version`
- `limitations`
- `provenance_reference`

Evidence may be directly sourced or derived from several source observations.

Where evidence is derived, the contributing input evidence or snapshots must be traceable.

Evidence records should be immutable in their substantive content after creation. Corrections should create a replacement or correction record with a link to the earlier record, rather than silently rewriting history.

### 7.2 Evidence Assessment

An **Evidence Assessment** records an interpretation of evidence against a goal, outcome, milestone, or assessment criterion.

Core attributes:

- `assessment_id`
- `assessment_scope_type`
- `assessment_scope_id`
- `criterion_id`
- `assessment_status`
- `assessment_result`
- `rationale`
- `analysis_run_id`
- `assessed_at`
- `supersedes_assessment_id`, where applicable.

The assessment scope identifies what is being evaluated. The evidence relationships identify what was considered.

Possible result classifications include:

- Supported.
- Partially supported.
- Contradicted.
- Insufficient evidence.
- Not assessed.
- Conflicting evidence.
- Stale evidence.

These classifications should be applied only where appropriate to the assessment method. They are not universal lifecycle states for every entity.

A change in assessment result must not rewrite the evidence that informed the earlier assessment.

### 7.3 Assessment Criterion

An **Assessment Criterion** defines what evidence is relevant and how it is evaluated for a particular purpose.

Core attributes:

- `criterion_id`
- `name`
- `description`
- `scope_type`
- `evaluation_method`
- `rule_version`
- `required_inputs`
- `applicability_conditions`
- `created_at`
- `status`

Criteria may be configured by users or supplied by a versioned deterministic analysis rule.

A criterion must not be assumed applicable to every goal. Different goals can require different standards of evidence and verification.

When a criterion changes materially, the new version should be distinguishable from previous versions.

### 7.4 Evidence-to-scope relationships

Evidence may relate to several goals, outcomes, or initiatives, but its interpretation may differ by context.

For example, one internal tool release could support the progress of one engineering goal while also enabling several downstream product initiatives.

The relationship between evidence and a portfolio entity should therefore be represented separately when it needs its own metadata.

Useful relationship attributes include:

- Evidence identifier.
- Target entity type and identifier.
- Relationship type.
- Relevance rationale.
- Link provenance.
- Creation timestamp.
- Optional assessment context.

This allows Siddhi to reuse one observation without incorrectly asserting that it proves every linked goal has been achieved.

## 8. Analysis and reporting entities

### 8.1 Analysis Run

An **Analysis Run** records a specific execution of a deterministic analysis or evaluation workflow.

Core attributes:

- `analysis_run_id`
- `analysis_type`
- `scope_type`
- `scope_id`
- `started_at`
- `completed_at`
- `run_status`
- `input_snapshot_references`
- `analysis_version`
- `configuration_version`
- `output_summary`
- `error_summary`

The run should identify the source observations and rules used to produce its results.

Routine ingestion, parsing, normalization, comparison, and reporting should not require an AI coding agent or external LLM.

External AI analysis should be represented separately, even when it is launched as part of a broader workflow.

### 8.2 Finding

A **Finding** represents a conclusion produced by an analysis run.

Examples include:

- A goal has insufficient evidence.
- A linked source is no longer accessible.
- A milestone is overdue according to the current plan.
- A source observation conflicts with another source.
- A relevant knowledge artifact was not found within the scanned scope.
- A plan depends on an unresolved prerequisite.

Core attributes:

- `finding_id`
- `analysis_run_id`
- `finding_type`
- `severity`, where applicable.
- `classification`
- `title`
- `description`
- `scope_type`
- `scope_id`
- `created_at`
- `finding_status`

Findings should link to their supporting evidence, relevant criteria, and applicable source observations.

A finding about missing information must identify the search scope or coverage limitations when available. It must not claim that a record does not exist globally when Siddhi only searched a limited scope.

### 8.3 Analysis Report

An **Analysis Report** is a persisted presentation of findings and assessments for a defined scope and point in time.

Core attributes:

- `report_id`
- `report_type`
- `scope_type`
- `scope_id`
- `analysis_run_id`
- `generated_at`
- `report_version`
- `summary`
- `content_reference`
- `freshness_summary`

Reports should preserve their historical context. A newly generated report may supersede an earlier report for current use, but it should not silently overwrite the earlier report if that report is part of the decision history.

Reports must distinguish source facts, derived findings, uncertainty, and recommendations.

## 9. External AI analysis and recommendations

### 9.1 External Analysis Request

An **External Analysis Request** records a request sent to an external AI service.

Core attributes:

- `external_analysis_id`
- `provider_reference`
- `model_reference`, where available.
- `request_purpose`
- `input_scope`
- `input_snapshot_references`
- `prompt_or_template_version`
- `requested_at`
- `request_status`
- `data_handling_metadata`

Sensitive request content should be stored only when necessary and permitted. Where the full prompt is not retained, the model should preserve sufficient non-sensitive provenance to explain the request.

### 9.2 External Analysis Result

An **External Analysis Result** records the returned response and any structured extraction performed by Siddhi.

Core attributes:

- `external_result_id`
- `external_analysis_id`
- `received_at`
- `result_status`
- `raw_response_reference`, where retained.
- `structured_result`
- `parsing_version`
- `limitations`
- `review_status`

A model response must remain distinguishable from source-derived facts.

Parsing a response successfully does not verify the claims it contains.

### 9.3 Recommendation

A **Recommendation** represents a proposed course of action generated by a user, deterministic analysis, or external AI analysis.

Core attributes:

- `recommendation_id`
- `source_type`
- `source_reference`
- `scope_type`
- `scope_id`
- `recommendation_text`
- `rationale`
- `supporting_evidence_references`
- `created_at`
- `recommendation_status`

Possible statuses include proposed, under review, accepted, rejected, deferred, and superseded, as applicable.

The recommendation's status is separate from the status of any resulting decision.

An accepted recommendation should link to an explicit decision record. Acceptance must not be inferred merely because a plan or priority later changes.

## 10. Refresh and operational entities

### 10.1 Refresh Job

A **Refresh Job** represents a requested or scheduled source refresh or analysis operation.

Core attributes:

- `job_id`
- `job_type`
- `scope_definition`
- `requested_at`
- `started_at`
- `completed_at`
- `job_status`
- `execution_summary`
- `related_ingestion_run_ids`
- `related_analysis_run_ids`

The model should allow a job to include several ingestion runs and analysis runs while preserving each run's independent outcome.

A job failure must not erase successful observations already recorded by earlier completed stages.

### 10.2 Processing Error

A **Processing Error** records an error associated with ingestion, normalization, analysis, reporting, or external AI processing.

Core attributes:

- `error_id`
- `operation_type`
- `related_job_id`
- `related_run_id`
- `source_reference`, where applicable.
- `error_category`
- `occurred_at`
- `recoverability`
- `safe_diagnostic_details`

Errors must not contain credentials, secrets, or unnecessary sensitive source content.

### 10.3 Data Quality Observation

A **Data Quality Observation** records a limitation or issue affecting the reliability of available data.

Examples include:

- Incomplete scan coverage.
- Missing source identifiers.
- Unresolvable references.
- Conflicting values.
- Unexpected schema changes.
- Stale observations.
- Invalid or incomplete source records.

Core attributes:

- `quality_observation_id`
- `scope_type`
- `scope_id`
- `quality_issue_type`
- `severity`
- `detected_at`
- `description`
- `related_source_references`
- `resolution_status`

A data quality issue should not be confused with a negative finding about the underlying project's performance.

## 11. Cross-cutting identity and provenance model

### 11.1 Stable identifiers

Every Siddhi-owned entity must have a stable identifier that does not depend on its display name or mutable description.

Identifiers should remain stable across ordinary edits and application restarts.

The exact identifier format is an implementation decision.

### 11.2 Entity references

Relationships between records should identify both the entity type and the stable identifier where polymorphic references are required.

For relationships that can be expressed through explicit domain associations, typed relationships are preferable to unconstrained references.

The implementation must validate that referenced entities exist and are of permitted types.

### 11.3 Provenance links

Provenance should be represented explicitly, not only embedded in prose.

Depending on the relationship, a provenance link may identify:

- Source system.
- Source artifact.
- Source snapshot.
- Normalized record.
- Evidence record.
- Analysis run.
- External analysis request or result.
- User or process responsible for a change.

The same source observation may support several findings. Provenance should be reusable rather than copied inconsistently into each report.

### 11.4 Time semantics

The model should distinguish at least:

- **Observed time:** When the source information was observed or reported.
- **Recorded time:** When Siddhi stored the observation.
- **Effective time:** When a value or decision is intended to apply, where relevant.
- **Decision time:** When a decision was explicitly made.
- **Processing time:** When ingestion or analysis occurred.

These timestamps serve different purposes and must not be treated as interchangeable.

All persisted timestamps should use a consistent representation, with timezone information preserved where applicable.

## 12. Lifecycle, revision, and deletion rules

### 12.1 Mutable current records and historical revisions

Some entities require a current editable representation, while others should be immutable observations.

The model should distinguish:

- Current editable domain records.
- Versioned plan, criterion, and decision records.
- Immutable source snapshots and evidence observations.
- Append-only ingestion and analysis history.
- Derived reports that may be superseded by later reports.

Not every database row requires a separate revision table. The implementation should choose the simplest structure that preserves the required history.

### 12.2 Archival

Goals, initiatives, and other long-lived domain entities should support archival where appropriate.

Archival means that an entity is no longer actively maintained or displayed in the default working view. It does not mean that historical references become invalid.

Archived entities may still be relevant to previous decisions and reports.

### 12.3 Deletion

Deletion rules must be explicit for each entity category.

- Removing a source reference must not delete the authoritative source record.
- Losing access to a source must not automatically delete historical snapshots.
- Archiving a goal must not automatically remove its decisions and reports.
- Deleting a draft should not delete independent evidence records it referenced.
- Retention and privacy obligations may require special handling of payloads or sensitive data.

Referential integrity should be preserved unless a deliberate, documented deletion policy says otherwise.

### 12.4 Version compatibility

Normalized records and analysis results must retain enough version information to identify which transformation or rule version produced them.

When parsing or analysis logic changes, Siddhi should be able to distinguish older results from newly calculated results.

A migration of the persisted database schema must not be confused with a change in the meaning of a business assessment.

## 13. Logical relationship summary

| Parent or source | Relationship | Child or target |
|---|---|---|
| Goal | One-to-many | Intended Outcome |
| Goal | Many-to-many | Initiative |
| Goal | Many-to-many | Project Reference |
| Initiative | Many-to-many | Project Reference |
| Plan | One-to-many | Plan Revision |
| Plan | One-to-many | Milestone |
| Plan or planning entity | May have multiple | Dependencies |
| Source System | One-to-many | Source Artifact Reference |
| Source Artifact Reference | One-to-many | Source Snapshot |
| Ingestion Run | One-to-many | Source Snapshot |
| Source Snapshot | One-to-many, as needed | Normalized Record |
| Source Snapshot or normalized record | May contribute to multiple | Evidence Records |
| Evidence Record | May support multiple | Evidence Assessments |
| Assessment Criterion | One-to-many | Evidence Assessments |
| Analysis Run | One-to-many | Findings |
| Analysis Run | May produce | Analysis Report |
| External Analysis Request | One-to-many or versioned | External Analysis Results |
| Recommendation | May result in | Decision |
| Decision | May have revisions or superseding decisions | Decision history |
| Review | May reference | Reports, plans, outcomes, and decisions |

The cardinalities above are logical expectations, not a complete physical schema. Exact constraints should be finalized when the domain model and database implementation are reviewed.

## 14. Data integrity requirements

The eventual implementation should enforce the following invariants:

1. Every Siddhi-owned entity has a stable identifier.
2. External artifact identity includes its source-system context.
3. A source snapshot identifies the source artifact and observation context from which it originated.
4. Normalized records identify their source snapshot and transformation version.
5. Evidence records preserve traceable provenance.
6. Assessments identify their scope, criterion, and analysis context.
7. Historical assessments remain distinguishable from current assessments.
8. Approved decisions cannot be created implicitly from recommendations.
9. Source disappearance does not automatically delete dependent Siddhi history.
10. Partial ingestion is distinguishable from complete ingestion.
11. Analysis results identify the rules and inputs used to produce them, to the extent available.
12. Invalid entity relationships and unsupported relationship types are rejected.
13. Archiving does not silently invalidate historical relationships.
14. Source records are never modified by the normal ingestion path.
15. Sensitive data is excluded from ordinary diagnostics and stored payloads unless explicitly justified and permitted.

These invariants should later be translated into functional requirements, database constraints, and automated tests.

## 15. Proposed persistence mapping

The logical entities will eventually be mapped to a relational persistence model, with SQLite proposed for the initial local-first backend.

A practical initial design should use:

- Relational records for core portfolio entities and relationships.
- Explicit tables or equivalent structures for source identities, snapshots, ingestion runs, evidence, assessments, decisions, and analysis history.
- Structured payload storage for source data whose shape varies significantly between systems.
- Database migrations for schema evolution.
- Repository or data-access boundaries so application logic does not depend directly on SQLite implementation details.

The logical model does not require every source artifact payload to be stored as relational columns. Source-specific payloads may be stored in a structured representation while their identity, provenance, and lifecycle metadata remain queryable.

The frontend must not access the database directly. All persisted state should be managed through the backend's application and persistence layers.

SQLite, the payload format, ORM, and exact table decomposition remain subject to the architecture decision process.

## 16. Open questions

| ID | Question | Impact |
|---|---|---|
| DM-001 | Should every goal have one or more intended outcomes, or may some goals remain intentionally qualitative and outcome-free? | Determines validation and assessment rules |
| DM-002 | Should project-to-goal relationships always be allowed directly without an initiative? | Affects portfolio association design |
| DM-003 | Should evidence observations be strictly immutable, with corrections represented as new records? | Determines audit and correction behavior |
| DM-004 | Which entities require full revision history, and which only require creation/update timestamps? | Controls implementation complexity |
| DM-005 | Should source snapshots be retained as complete payloads, content-addressed objects, or a hybrid of snapshots and change records? | Affects storage and reproducibility |
| DM-006 | Which assessment classifications are universal, and which should be defined by each assessment method? | Prevents misleading generic status semantics |
| DM-007 | Should goal and initiative relationships have effective dates or historical revisions? | Supports reconstruction of past portfolio structure |
| DM-008 | How should identity be resolved when a source does not provide stable external identifiers? | Affects duplicate detection and source continuity |
| DM-009 | Which decision and approval roles are required in the first release? | Affects authorization and decision history |
| DM-010 | How should sensitive source payloads and external AI request/response content be retained or deleted? | Affects privacy and retention |
| DM-011 | What is the minimum history required to reproduce a past analysis result? | Determines snapshot and version-retention requirements |
| DM-012 | Should custom goal types, statuses, and assessment criteria be user-configurable from the first release? | Affects schema flexibility and validation |

## 17. Relationship to other documents

This document should be read alongside:

- `domain-model.md` — domain concepts, definitions, and conceptual relationships.
- `data-ownership.md` — authority boundaries and permitted data handling.
- `system-architecture.md` — component responsibilities and data flows.
- `functional-requirements.md` — observable system behavior.
- `non-functional-requirements.md` — integrity, performance, security, and reliability expectations.
- `architectural-decisions.md` — design decisions and their status.
- `scanning-and-evidence.md` — source discovery and evidence derivation.
- `synchronization.md` — refresh, change detection, and source-state handling.
- `security-and-privacy.md` — access control, sensitive data, and retention requirements.

During the documentation review, this model should be checked against the domain model and data-ownership policy for consistency. Once the model is agreed, its behavioral constraints can be converted into OpenSpec requirements, while the reusable entity definitions, provenance concepts, and design rationale can be captured as independent OKF knowledge.

---

**End of document**