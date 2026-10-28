# Data Ownership and Authority

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `data-ownership.md`  
**Status:** Draft for review  
**Scope:** Siddhi API and its source-system integrations  
**Purpose:** Define data authority, ownership, permitted access, derived information, synchronization, and change-control rules.

---

## 1. Purpose

Siddhi consolidates information from multiple engineering and planning systems to help users understand portfolio progress, assess goals, identify gaps, and make informed decisions.

It must not become an alternative source of truth for information already owned by another system.

This document establishes:

- Which system owns each category of information.
- Which information Siddhi may read, copy, normalize, derive, or retain.
- How source provenance and freshness are represented.
- How conflicting, missing, stale, or changed information is handled.
- How Siddhi distinguishes source facts from analysis and approved decisions.
- Which data changes require explicit user approval.

These rules apply regardless of whether information is accessed through a file, API, repository, local database, or future integration.

## 2. Core principles

### 2.1 Authority follows the information, not the application

A system is authoritative for a particular category of information, not necessarily for every fact associated with an entity.

For example, Vyasa may be authoritative for a project's discovered repository location, while Git provides evidence of repository history and OpenSpec defines the project's requirements.

Siddhi must preserve these distinctions instead of selecting one source as universally authoritative.

### 2.2 Siddhi owns its planning and analysis records

Siddhi is the authority for information created and maintained specifically within Siddhi, including its goals, portfolio priorities, plans, reviews, analysis runs, and approved strategic decisions.

It may reference external projects and artifacts without assuming ownership of their underlying records.

### 2.3 Source observations must remain distinguishable from interpretation

Siddhi must distinguish:

- **Source data:** Information retrieved from an authoritative source.
- **Normalized data:** A structured representation of source data.
- **Evidence:** An observation relevant to a goal, initiative, or decision.
- **Assessment:** An interpretation of evidence against a criterion or intended outcome.
- **Recommendation:** A proposed action or conclusion.
- **Decision:** An explicitly approved choice made by an authorized person.

These categories must not be treated as interchangeable.

### 2.4 Reading does not imply permission to write

Access to a source does not grant Siddhi permission to modify it.

Source ingestion is read-only by default. Any future write integration requires an explicit capability definition, authorization model, and approval policy.

### 2.5 Missing information is not negative evidence

If Siddhi cannot find a requirement, knowledge artifact, test result, or implementation record, it must not automatically conclude that the item does not exist or that the work has failed.

It must represent the uncertainty and, where possible, explain the limits of the search.

### 2.6 Independent systems remain independent

OpenSpec requirements and OKF engineering knowledge have separate purposes and ownership.

A requirement may exist before its supporting knowledge is documented. Knowledge may exist without a corresponding requirement. Neither system should be treated as valid only when the other contains a matching record.

Cross-references may improve traceability, but must not create an implicit dependency or transfer ownership.

## 3. Data ownership matrix

The following matrix defines the proposed authority boundaries.

| Data category | Authoritative owner | Siddhi's permitted role |
|---|---|---|
| Project and repository inventory | Vyasa | Read, normalize, reference, and retain sourced snapshots |
| Repository origin and discovered location | Vyasa for its declared inventory; Git configuration for repository-local origin evidence | Record both where available, preserve discrepancies |
| Project technology metadata | Vyasa for its recorded inventory; repository artifacts as supporting evidence | Normalize and classify with provenance |
| Requirements, scenarios, and change artifacts | OpenSpec | Read and analyze without becoming the authority |
| Engineering knowledge and knowledge relationships | OKF | Read, index, reference, and analyze without becoming the authority |
| Source code and repository history | Git/VCS | Read available history and retain relevant observations |
| Test, build, and release results | The system or artifact that produced each result | Ingest observations and retain their origin and context |
| Portfolio goals and intended outcomes | Siddhi | Create, maintain, revise, and archive |
| Portfolio priorities and strategic constraints | Siddhi | Maintain with rationale, author, and history |
| Initiatives and portfolio-level relationships | Siddhi | Maintain relationships to external projects and evidence |
| Plans, milestones, and dependencies | Siddhi | Maintain and revise with historical versions |
| Reviews and approved portfolio decisions | Siddhi | Record decisions, responsible approvers, rationale, and revisions |
| Source snapshots and ingestion history | Siddhi | Retain according to the approved retention policy |
| Normalized evidence and deterministic findings | Siddhi | Generate, version, and reproduce where inputs and rules permit |
| External AI analysis and recommendations | The external provider produces the output; Siddhi owns its local record and context | Store as attributed analysis, not verified source fact |
| Approved or rejected recommendations | Siddhi | Record the explicit decision and its rationale |
| Application configuration and operational state | Siddhi | Maintain locally under defined security and retention rules |

This matrix is a baseline. Specific source fields may require more precise ownership rules when their schemas and update behavior are inspected.

## 4. Ownership boundaries by system

### 4.1 Vyasa — workspace and project intelligence

Vyasa supplies project inventory and repository-related metadata within its defined scope.

Siddhi may use this information to:

- Discover candidate projects for portfolio goals.
- Identify repositories and their recorded locations.
- Understand available technologies and documentation indicators.
- Identify whether relevant OpenSpec or OKF structures are reported.
- Detect changes between inventory snapshots.
- Link Siddhi goals and initiatives to existing projects.

Siddhi must not:

- Treat an inventory record as proof that a project is actively maintained.
- Treat a detected documentation directory as proof of completeness or correctness.
- Change Vyasa-owned project metadata through ordinary ingestion.
- Automatically delete a Siddhi project reference because a project disappears from the latest inventory.
- Assume that an inventory scan is a complete or successful scan unless the source reports sufficient evidence.

If Vyasa reports a project that cannot currently be accessed, Siddhi should preserve the reference and represent its accessibility or freshness separately.

### 4.2 OpenSpec — requirements and change artifacts

OpenSpec owns the requirements and change-management artifacts created and maintained through its workflows.

Siddhi may read and analyze:

- Requirements and scenarios.
- Change proposals and specifications.
- Task lists and their declared status.
- Change identifiers and lifecycle metadata.
- Available relationships among requirements, changes, and specifications.

Siddhi must not:

- Rewrite requirements to fit a portfolio assessment.
- Create or close OpenSpec tasks as a side effect of analysis.
- Treat a declared task status as proof of successful implementation.
- Treat the presence of a specification as proof that its requirements are satisfied.
- Require every requirement to have a corresponding OKF knowledge artifact.

If Siddhi later supports creating or updating OpenSpec artifacts, that must be a separately authorized integration, not an extension of read-only ingestion.

### 4.3 OKF — engineering knowledge

OKF owns the engineering knowledge maintained within its own conventions and structures.

Siddhi may read and analyze:

- Knowledge documents and structured records.
- Technical concepts and relationships.
- Architecture and design rationale.
- Decisions and constraints represented in OKF.
- Declared validation or review status, where supported.
- References between knowledge artifacts.

Siddhi must not:

- Modify OKF knowledge during ordinary ingestion.
- Treat a missing requirement link as evidence that knowledge is invalid.
- Assume that all knowledge must originate from an OpenSpec requirement.
- Infer that a document is technically verified merely because it exists.
- Replace OKF's own metadata or validation semantics with Siddhi-specific interpretations.

Siddhi may maintain its own mapping between a knowledge artifact and a portfolio goal, but that mapping belongs to Siddhi unless explicitly authored in OKF through a future authorized integration.

### 4.4 Git and version-control systems

Git/VCS provides repository history and related evidence, subject to the access and data available to Siddhi.

Siddhi may observe:

- Commit identifiers and timestamps.
- Branches and tags.
- Changed paths and commit summaries.
- Available release references.
- Repository accessibility and observation time.
- Other history metadata supported by the adapter.

These observations may help assess whether a project has changed, but they are not sufficient by themselves to prove progress toward a goal.

Siddhi must not:

- Commit, merge, checkout, reset, or rewrite repositories during ordinary ingestion.
- Infer that a recent commit represents useful progress without examining relevant context.
- Infer that a lack of recent commits means a project is abandoned.
- Assume a tag is a production release without supporting release evidence.
- Treat commit messages as verified statements of completed work.

Repository access must follow the applicable permissions and security policy.

### 4.5 Verification and operational evidence

Build systems, test reports, release records, and other verification sources remain authoritative for the observations they actually produce.

Siddhi may record the result, source, scope, timestamp, relevant version or commit, and available supporting details.

It must distinguish between:

- A test result that was observed.
- A test result that applies to the relevant revision.
- A test result that is current enough for a particular assessment.
- A conclusion that a goal or requirement is satisfied.

The last item requires an explicit assessment rule and adequate supporting evidence; it must not be inferred solely from a successful build or test run.

### 4.6 Siddhi-owned portfolio records

Siddhi owns its own strategic and planning records, including:

- Goals and intended outcomes.
- Portfolio priorities and constraints.
- Initiatives and their relationships.
- Project-to-goal and initiative-to-goal mappings.
- Plans, plan revisions, milestones, and dependencies.
- Reviews, assumptions, and portfolio decisions.
- Analysis runs, reports, findings, and recommendations.
- User-defined assessment criteria and relevant configuration.

Siddhi may revise these records according to its own authorization and audit rules.

Changes to these records must not silently modify source-system records.

A link to a Vyasa project, OpenSpec artifact, or OKF knowledge record is a reference; it does not transfer ownership of that record to Siddhi.

## 5. Data categories and change permissions

Siddhi should classify stored data into the following categories.

### 5.1 Source references

Identifiers, paths, URLs, and other locators used to refer to source records.

- May be stored and refreshed by Siddhi.
- Must retain the source system and identity context.
- Must not be assumed permanent if the source supports renaming or relocation.
- Must not be used to silently recreate a missing source record.

### 5.2 Source snapshots

A captured view of source information at a particular observation time.

- Must be distinguishable from the current state of the source.
- Should preserve enough information to explain later analysis and comparisons.
- Must record the source and observation time.
- Should be immutable after capture, except for explicitly defined metadata corrections or retention operations.
- Must not be represented as current merely because Siddhi still retains it.

### 5.3 Normalized records

Structured representations created from source data so that different source formats can be analyzed consistently.

- Are maintained by Siddhi.
- Must retain their source references and transformation/version information where practical.
- May be regenerated when parsing or normalization rules change.
- Must not replace the original source record or falsely imply that the normalized representation is source-authored.

### 5.4 Evidence records

Observations derived from source snapshots or direct source reads that may be relevant to a portfolio question.

Evidence should preserve:

- The originating system and artifact.
- The observation or capture time.
- The applicable repository revision or source version, where available.
- The method used to obtain or derive the evidence.
- The relationship to the relevant goal, outcome, initiative, or criterion.
- Any known limitations.

Evidence and its interpretation should be stored separately so that later assessments can change without rewriting the historical observation.

### 5.5 Assessments and findings

Assessments are Siddhi's interpretation of evidence against a defined criterion.

They must identify, where applicable:

- The evidence used.
- The assessment rule or analysis version.
- The assessment time.
- The classification and confidence or uncertainty.
- The reasons for the result.
- Missing or conflicting inputs.

Re-running an assessment may produce a different result when inputs, rules, or criteria change. The new result must not silently overwrite the history needed to explain the difference.

### 5.6 Recommendations and decisions

Recommendations may originate from deterministic analysis, an external AI service, or an authorized user.

A recommendation is not an approved decision.

An approved decision must record its decision status, responsible person or authority, timestamp, rationale, and relevant context. Rejection, supersession, or reversal should preserve the previous decision and the reason for the change.

External AI output must not automatically change an approved priority, plan, milestone, or strategic decision.

## 6. Source ingestion and synchronization

### 6.1 Read-only default

Source adapters must use read-only access for normal discovery, ingestion, and refresh operations.

Any future write capability must define:

- The specific source and records it may change.
- The permitted operations.
- The user or service identity under which it acts.
- The authorization and confirmation requirements.
- Failure handling and audit behavior.
- Whether changes can be reversed.

Write access to one source must not imply write access to other sources.

### 6.2 Ingestion is not validation

Successful parsing means that Siddhi could interpret the available input according to its parser. It does not establish that the source content is accurate, complete, current, or technically correct.

Each ingestion run should record the outcome and, where supported:

- Source identity.
- Start and completion time.
- Scope of the scan.
- Source version or revision.
- Number of records discovered, processed, skipped, or rejected.
- Errors and access limitations.
- Parser or adapter version.

Partial ingestion must not be presented as a complete source snapshot.

### 6.3 Idempotency

Repeated ingestion of unchanged source data should not create misleading duplicate source identities or duplicate evidence.

Where the source supports stable identifiers, Siddhi should use them. Where it does not, Siddhi must use a documented matching strategy and preserve ambiguity rather than merging records solely because their names look similar.

### 6.4 Changed and deleted source records

When a source record changes or disappears:

- Preserve prior observations according to the retention policy.
- Record the latest observation and its time.
- Distinguish source deletion from inaccessible, moved, renamed, filtered, or undiscovered records when evidence allows.
- Avoid deleting linked Siddhi goals, initiatives, decisions, or historical reports automatically.
- Mark references as unresolved or unavailable when the cause cannot be established.

A missing record is not proof that its underlying work or knowledge never existed.

### 6.5 Conflicts between sources

Siddhi must not resolve conflicting facts by silently choosing whichever source was read most recently.

Instead, it should:

1. Identify the conflicting observations.
2. Preserve their source identities and timestamps.
3. Apply an explicitly defined authority rule when one exists.
4. Mark unresolved conflicts as such.
5. Allow an authorized user to record a resolution where necessary.

The authority rule should be specific to the data field or claim being evaluated.

## 7. Provenance and auditability

Every material derived finding should be traceable to its inputs and method.

Where applicable, Siddhi should retain:

- Source system and source artifact identifier.
- Source revision, version, or snapshot identifier.
- Observation and ingestion timestamps.
- Transformation or parser version.
- Assessment criteria and analysis version.
- External analysis provider and model metadata, where available.
- User changes, approvals, and decision rationale.

Provenance should support answers to questions such as:

- What source information supported this finding?
- When was that information observed?
- Was the assessment based on current or historical data?
- Which rule or analysis version produced the result?
- Why did the result change after a refresh?
- Who approved the resulting decision?

Siddhi must not claim reproducibility when required inputs, source revisions, or processing details are unavailable.

## 8. Freshness, confidence, and uncertainty

Freshness and confidence are different concepts.

- **Freshness** describes how recently the source was observed and whether its state is known to have changed.
- **Confidence** describes how strongly the available evidence supports a particular assessment.
- **Completeness** describes whether the required scope of information was available.
- **Verification** describes whether an appropriate validation process has been performed and recorded.

A recently retrieved record can still be incomplete or unverified. A well-supported historical record can still be stale for a current decision.

Siddhi should not collapse these dimensions into a single status without an explicit, documented rule.

Where source coverage is unknown or incomplete, the report must expose that limitation.

## 9. Access control, privacy, and sensitive information

Siddhi should collect only information needed for its declared portfolio intelligence and planning purposes.

It must:

- Respect the permissions of connected source systems.
- Avoid collecting secrets, credentials, or unrelated personal data into portfolio snapshots.
- Keep connection credentials separate from source evidence and reports.
- Avoid including secret values in logs, errors, and generated reports.
- Limit access to local data and API operations according to the approved security model.
- Avoid sending source content to external AI services unless the operation is explicitly authorized and its data scope is clear.
- Record external analysis provenance without unnecessarily duplicating sensitive source content.
- Define retention and deletion behavior for both local records and externally generated analysis.

A local-first architecture does not by itself guarantee security. Authentication, local API exposure, filesystem permissions, backups, and external data transfer still require explicit controls.

## 10. Retention, correction, and deletion

Siddhi must define retention rules for source snapshots, derived evidence, analysis runs, reports, and audit records before relying on them for long-term historical comparisons.

The retention policy should distinguish:

- Current normalized views.
- Historical source snapshots.
- Derived evidence and assessments.
- Approved decisions and their revisions.
- Operational logs and temporary ingestion data.
- Credentials and other sensitive configuration.

Corrections to Siddhi-owned data should preserve an appropriate history of material changes. Corrections to source-owned information must be made in the authoritative source, not by silently editing Siddhi's copy.

Deletion of a local reference must not be treated as deletion of the source record. Similarly, removing a source record must not automatically erase all historical decisions that relied on it.

Where privacy, legal, or security obligations require deletion, the implementation must define how those obligations interact with audit history and retained derived records.

## 11. External AI data ownership

External AI services may receive selected context and return analysis, recommendations, or structured findings.

Siddhi owns the record of the request context it submitted, the response it received, and how the response was used within Siddhi, subject to provider terms and applicable data-handling requirements.

The external model does not become the authority for source facts or portfolio decisions.

Siddhi must distinguish:

- Source facts included in the prompt.
- Context assembled or summarized by Siddhi.
- Model-generated claims and interpretations.
- Recommendations generated by the model.
- Human-reviewed conclusions.
- Approved portfolio decisions.

AI outputs must not be presented as verified merely because they are detailed, confident, or well formatted. Where feasible, material claims should link back to evidence and be checked independently.

## 12. Ownership enforcement and tests

Ownership rules must be enforced through architecture and tests, not only documented as conventions.

Expected controls include:

1. Source adapters expose only the operations required for their declared capabilities.
2. Normal ingestion paths do not invoke source-write operations.
3. Siddhi-owned changes do not mutate source snapshots.
4. Assessment revisions do not silently rewrite historical source observations.
5. External AI recommendations cannot bypass the decision-approval workflow.
6. Conflicting source observations remain inspectable.
7. Missing source records do not trigger automatic deletion of dependent Siddhi records.
8. Reports preserve provenance and clearly identify uncertainty.
9. Logs and errors do not expose credentials or unauthorized source content.
10. Repeated ingestion of unchanged data does not create misleading duplicates.

Tests should cover successful ingestion, partial scans, permission failures, renamed and missing records, conflicting observations, parser upgrades, assessment revisions, and rejected or superseded recommendations.

## 13. Open questions

The following policies require explicit decisions before implementation details are finalized.

| ID | Question | Why it matters |
|---|---|---|
| DO-001 | Which source fields from Vyasa are authoritative, and which should be independently verified against Git or repository artifacts? | Prevents false assumptions about project metadata |
| DO-002 | How long should Siddhi retain raw or normalized source snapshots? | Determines storage cost and historical comparison capability |
| DO-003 | Should every refresh preserve a complete snapshot, or should Siddhi retain only changes plus periodic full snapshots? | Affects storage, recovery, and reproducibility |
| DO-004 | What is the correction policy when an earlier source observation or derived assessment is found to be wrong? | Preserves auditability without retaining misleading results as current |
| DO-005 | Which local users or processes may approve strategic decisions, and how is their authority established? | Prevents unapproved changes to portfolio priorities |
| DO-006 | What source content may be sent to external AI services, and what redaction or confirmation is required? | Controls disclosure and privacy risks |
| DO-007 | What deletion and archival rules apply to goals, initiatives, source references, reports, and audit history? | Prevents accidental loss of historical context |
| DO-008 | How should source permissions and inaccessible repositories be represented in the user experience? | Avoids confusing missing evidence with evidence of absence |
| DO-009 | Which source fields need explicit field-level authority rules when sources disagree? | Avoids broad and potentially incorrect precedence rules |
| DO-010 | Which data should be exportable, and in what format, for backup, migration, or independent review? | Supports portability and user control |
| DO-011 | What local API security and credential-storage model will be used by the backend and desktop application? | Defines the practical security boundary |
| DO-012 | Which retention and deletion rules apply to externally generated AI requests and responses? | Aligns local auditability with data-minimization obligations |

These questions should be resolved through the design-review process. Until then, the document establishes conservative defaults: read-only source access, explicit provenance, no silent conflict resolution, no automatic approval of recommendations, and no automatic deletion of historical portfolio records.

## 14. Relationship to other Siddhi documents

This document defines authority and permitted data handling. It does not define the complete schema or implementation.

- `vision.md` defines the intended purpose and principles of Siddhi.
- `scope-and-roadmap.md` defines the system boundary and delivery phases.
- `functional-requirements.md` defines expected system behavior.
- `non-functional-requirements.md` defines quality and operational expectations.
- `system-architecture.md` defines the major components and their responsibilities.
- `architectural-decisions.md` records design choices and their status.
- `domain-model.md` defines the principal business concepts and relationships.
- `data-model.md` will define the logical persisted data structures and their relationships.
- `scanning-and-evidence.md` will define how source information becomes evidence.
- `synchronization.md` will define refresh, change detection, and synchronization behavior.
- `security-and-privacy.md` will elaborate access controls, credential handling, privacy, and data protection.

The same ownership rule may be referenced across these documents, but the authoritative policy should remain clear and consistent. During the later OpenSpec and OKF preparation stage, behavioral obligations can become requirements, while reusable concepts, architecture rationale, and engineering guidance can be captured as independent knowledge artifacts.

---

**End of document**