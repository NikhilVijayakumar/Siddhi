# OpenSpec Integration

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `openspec-integration.md`  
**Status:** Draft for review  
**Scope:** Read-only integration with OpenSpec requirements, change artifacts, schemas, task status, and archived changes.

---

## 1. Purpose

OpenSpec provides structured information about declared system requirements, expected behavior, proposed changes, and implementation task status.

Siddhi consumes this information to understand what a project intends to deliver, identify changes in declared scope, connect requirements to portfolio goals, and determine where implementation or verification evidence may be needed.

This document defines:

- The boundary between OpenSpec and Siddhi.
- The OpenSpec information Siddhi should discover and consume.
- Support for different repository configurations and workflow schemas.
- Requirement, scenario, change, task, and archive interpretation.
- Stable identity, versioning, and provenance.
- Integration failure handling and validation.
- Testing and acceptance criteria.

The document describes the intended integration contract. The exact parser, CLI usage, and supported formats must be verified against the OpenSpec versions and repository configurations that Siddhi will consume.

## 2. Integration principles

### 2.1 OpenSpec owns declared requirements

OpenSpec remains authoritative for requirements and change artifacts maintained through its workflows.

Siddhi may normalize and analyze these records, but must not rewrite them or become their authority.

### 2.2 Requirements and engineering knowledge are independent

OpenSpec requirements do not depend on OKF knowledge to exist or remain valid.

OKF knowledge may exist without an OpenSpec requirement.

Siddhi may link the two when useful, but the absence of a cross-reference must not automatically be treated as an error.

### 2.3 Declared progress is not verified implementation

OpenSpec can report that a task is marked complete or a change is ready for archival. Those declarations are useful workflow evidence, but they do not independently prove that the implementation works or that a strategic outcome has been achieved.

Siddhi must distinguish:

- Requirement declaration.
- Change proposal and specification.
- Declared task progress.
- Structural validation.
- Implementation evidence.
- Test and build results.
- Verified outcome assessment.

These represent different kinds of information.

### 2.4 Inspect the actual schema

OpenSpec supports configurable workflow schemas and project-level configuration. Its official documentation describes schema resolution, configuration, and commands for inspecting changes, specifications, schemas, and task status. <Link url="https://openspec.dev/docs/configuration" title="OpenSpec configuration"/> · <Link url="https://openspec.dev/docs/customize-schemas" title="Custom schemas"/>.

Siddhi must not assume that all repositories use the same artifact names, templates, task-tracking conventions, or directory structures.

### 2.5 Read-only integration

Ordinary Siddhi ingestion must not create changes, edit specifications, update task checkboxes, archive changes, or modify OpenSpec configuration.

Any future write-back integration must be a separate, explicitly authorized capability.

### 2.6 Preserve uncertainty and provenance

Siddhi must retain the difference between what OpenSpec declares, what Siddhi successfully parses, what other sources corroborate, and what remains unknown.

A successful parse is not proof that the source content is complete or correct.

---

## 3. Responsibilities and boundaries

| Responsibility | OpenSpec | Siddhi |
|---|---|---|
| Maintain declared requirements and scenarios | Authority | Read and normalize |
| Maintain change proposals and specifications | Authority | Read and track observations |
| Define workflow schemas and artifact conventions | Authority for its configuration | Inspect and adapt |
| Record declared task progress | Authority for the recorded status | Preserve as declared progress |
| Validate OpenSpec artifacts | Provides its supported validation mechanisms | Record results when explicitly executed or available |
| Establish that implementation works | Not established by declaration alone | Combine relevant evidence from appropriate sources |
| Define portfolio goals and intended outcomes | Outside its scope | Authority |
| Link requirements to portfolio goals | Does not need to own this relationship | Authority |
| Prioritize initiatives and projects | Outside its scope | Authority |
| Approve strategic decisions | Outside its scope | Authority |
| Modify OpenSpec artifacts during ingestion | Not applicable | Prohibited by default |

## 4. Integration architecture

The proposed integration has four logical stages.

<box border radius="lg" padding={3} gap={2} align="center">
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **OpenSpec repository**

    <text size="sm" textAlign="center">Configuration · Schemas · Specs · Active changes · Archived changes</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box border radius="md" padding={3} width="100%" align="center">
    **OpenSpec adapter**

    <text size="sm" textAlign="center">Discovery · CLI or file access · Schema inspection · Parsing</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **Siddhi normalized representation**

    <text size="sm" textAlign="center">Requirements · Scenarios · Changes · Tasks · Provenance</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box border radius="md" padding={3} width="100%" align="center">
    **Evidence and portfolio analysis**

    <text size="sm" textAlign="center">Goal links · Change tracking · Evidence gaps · Reports</text>
  </box>
</box>

The adapter should isolate OpenSpec-specific behavior from Siddhi's domain logic. It should expose normalized records and source observations, not make strategic decisions.

## 5. Source discovery and supported formats

### 5.1 Repository-level discovery

For each project, Siddhi should identify whether OpenSpec is present and determine the accessible OpenSpec root.

Discovery should establish, where available:

- The resolved OpenSpec root.
- The presence of project configuration.
- The configured default schema.
- Project-local schema definitions.
- Available specifications.
- Active changes.
- Archived changes.
- Relevant schema and configuration validation status.
- The scope and completeness of the scan.

The absence of an OpenSpec directory should be recorded as a discovery result only when the repository was actually inspected within a known scope.

If the repository was inaccessible or only partially scanned, OpenSpec availability must remain unknown.

### 5.2 Configuration

Siddhi should inspect the actual project configuration, including the applicable `openspec/config.yaml` or supported equivalent.

Where available, it should preserve:

- The configured default schema.
- Artifact-specific rules.
- Context or operational guidance relevant to interpreting artifacts.
- References to other OpenSpec stores.
- Configuration validation warnings.
- The configuration version or content fingerprint.

Configuration should be treated as source information. Siddhi must not silently rewrite it to fit a universal schema.

Global CLI settings and user-specific configuration may affect how OpenSpec commands behave. Siddhi should distinguish repository-owned configuration from machine-specific settings and avoid depending on a user's global configuration unless that dependency is explicitly part of the integration contract.

### 5.3 Schema discovery

OpenSpec schemas determine the artifacts and templates used by a workflow. The official documentation describes project-level, user-level, and packaged schema resolution. <Link url="https://openspec.dev/docs/customize-schemas" title="OpenSpec schema customization"/>.

Siddhi should discover the effective schema where possible and record:

- Schema name.
- Schema source or resolution location.
- Schema version, if available.
- Artifact definitions.
- Relevant artifact dependencies.
- Task-tracking configuration.
- Validation status and warnings.

If Siddhi cannot determine the effective schema, it must not silently assume the default schema is applicable.

### 5.4 Multiple repository conventions

The integration must support repositories with different OpenSpec conventions.

For example, one repository may use the standard workflow, while another uses team-specific schemas and additional artifacts for UI specifications, API contracts, or test plans.

Siddhi should identify and interpret these conventions from the actual configuration and schema definitions.

It must not require all repositories to adopt a shared schema merely to be discoverable.

Unknown artifact types should be preserved as recognized source artifacts where possible, even if Siddhi cannot yet interpret their contents semantically.

---

## 6. Logical information contract

The following entities describe the information Siddhi needs to extract. They are logical representations, not a requirement to mirror OpenSpec's internal implementation or reproduce every source file as a database table.

### 6.1 OpenSpec Project Context

Represents OpenSpec's configuration and discovery context for a project.

Suggested attributes:

- Siddhi project reference.
- OpenSpec root locator.
- Discovery timestamp.
- Configuration reference.
- Effective schema name, if known.
- Schema source and version, if available.
- Scan coverage.
- Validation status, where available.
- Parser and adapter versions.

The context must distinguish the existence of OpenSpec from successful interpretation of its artifacts.

### 6.2 Specification

Represents a maintained specification and its source identity.

Suggested attributes:

- Stable Siddhi artifact identifier.
- Source project reference.
- OpenSpec root reference.
- Specification identifier or path.
- Display name.
- Source revision or content fingerprint.
- Observation timestamp.
- Applicable schema or format metadata.
- Parse status.

A specification may contain multiple requirements. Siddhi should preserve their individual identities and relationships where the source structure supports this.

### 6.3 Requirement

Represents a declared system requirement.

Suggested attributes:

- Stable Siddhi identifier.
- Source specification reference.
- Source requirement identifier, where available.
- Requirement text.
- Requirement classification, where declared.
- Source location.
- Applicable source revision.
- Observation timestamp.
- Parse status.

Requirement text should not be silently rewritten during normalization.

If the source has no stable requirement identifier, Siddhi should use a documented identity strategy based on the specification, source location, and available structural information. Content similarity alone should not be sufficient to merge distinct requirements.

### 6.4 Scenario

Represents a scenario or example that describes expected behavior associated with a requirement.

Suggested attributes:

- Stable Siddhi identifier.
- Parent requirement reference.
- Source scenario identifier, if available.
- Scenario text.
- Source location.
- Source revision.
- Observation timestamp.

Siddhi should preserve the relationship between a requirement and its scenarios.

It must not assume that a scenario has been executed simply because it appears in a specification.

### 6.5 Change

Represents an OpenSpec change artifact set.

Suggested attributes:

- Stable Siddhi identifier.
- Source project reference.
- Change identifier.
- Source directory or locator.
- Declared goal or description, if available.
- Applicable schema.
- Change state as observed.
- Creation and modification information, where available.
- Active or archived classification.
- Source revision or content fingerprint.
- Observation timestamp.

A change may include several artifacts and may introduce, modify, or remove requirements.

Siddhi should retain those relationships rather than flattening the change into an unstructured status.

### 6.6 Change Artifact

Represents a particular artifact within a change, such as a proposal, specification delta, design document, task list, or repository-specific artifact.

Suggested attributes:

- Stable Siddhi identifier.
- Parent change reference.
- Artifact type.
- Source path or identifier.
- Content fingerprint or source revision.
- Applicable schema.
- Parse status.
- Observation timestamp.

The artifact type should come from the effective schema or source convention where possible. Unknown artifact types should remain identifiable without forcing them into an unrelated standard type.

### 6.7 Task Observation

Represents a task and its declared completion status as observed from an OpenSpec artifact.

Suggested attributes:

- Stable Siddhi identifier.
- Source change reference.
- Source artifact reference.
- Task identifier or source location.
- Task description.
- Declared completion status.
- Observation timestamp.
- Source revision or content fingerprint.

A task's declared status must remain distinguishable from independently verified implementation evidence.

### 6.8 Archive Observation

Represents a change observed in an OpenSpec archive.

Suggested attributes:

- Change reference.
- Archive locator.
- Archive observation timestamp.
- Available completion metadata.
- Source revision or content fingerprint.
- Relationships to the maintained specifications, where identifiable.

Archiving is a source workflow event, not an automatic declaration that every requirement is implemented correctly or that the associated strategic goal is achieved.

---

## 7. Requirements and scenarios

### 7.1 Requirement identity

Siddhi should use a source-provided requirement identifier when one exists and is stable within its documented scope.

Where identity depends on a specification file or a structural location, the identifier should include enough context to distinguish otherwise identical requirement names across specifications.

If a requirement moves or changes substantially, Siddhi should attempt to distinguish:

- The same requirement with an updated location.
- A modified requirement.
- A removed requirement.
- A newly introduced requirement.
- An unresolved identity match.

It must not automatically merge requirements solely because their text is similar.

### 7.2 Requirement changes

Siddhi should compare successive observations to identify changes in requirement content, scenarios, and source relationships.

A changed requirement must remain traceable to its previous observation.

The comparison should preserve the distinction between:

- Source text changed.
- Requirement added or removed.
- Scenario added or removed.
- Requirement identity could not be resolved.
- The source could not be fully scanned.

### 7.3 Declared requirement status

Siddhi should not invent a universal lifecycle status for requirements if the source schema does not define one.

Where a repository or workflow adds custom status metadata, Siddhi may preserve and normalize it while retaining the original source value.

A requirement's presence in a maintained specification does not establish whether the implementation is complete.

### 7.4 Goal mapping

Siddhi may associate requirements with goals and intended outcomes.

Such associations belong to Siddhi unless explicitly authored in OpenSpec through a separately authorized workflow.

A requirement can support several goals, and a goal can depend on several requirements.

The existence of a relationship indicates relevance, not proof of achievement.

---

## 8. Changes, artifacts, and task status

### 8.1 Active changes

Siddhi should discover active changes and their available artifacts.

For each change, it should record:

- Change identity.
- Applicable schema.
- Available artifacts.
- Artifact completion information, where supported.
- Task observations.
- Last observed source state.
- Parse and coverage limitations.

The integration must not assume that all changes use the same number or names of artifacts.

### 8.2 Artifact completion

If OpenSpec exposes artifact completion or dependency status, Siddhi may use it as a declared workflow observation.

It should preserve whether the status was:

- Reported directly by OpenSpec.
- Derived by Siddhi from the source artifacts.
- Unavailable or unresolved.

These classifications must not be conflated.

### 8.3 Task completion

Task checkboxes or equivalent task statuses should be recorded as declared progress.

Siddhi may compare task progress across observations, but it must not conclude that a task has been correctly implemented solely from its completion marker.

Stronger evidence may come from source changes, test results, build results, release artifacts, or other relevant verification sources.

Even then, the relevance and scope of that evidence must be evaluated.

### 8.4 Archived changes

Siddhi should support reading archived changes where accessible.

It should preserve the distinction between an active change and a change that has been archived, along with the available archive context.

The integration must not automatically treat archive status as a verified implementation result.

### 8.5 Requirement deltas

Where change artifacts describe added, modified, or removed requirements, Siddhi should preserve the declared delta and its relationship to the maintained specification.

If the source's delta format cannot be interpreted reliably, the raw or normalized artifact reference should remain available with a parsing limitation.

Siddhi must not silently infer that an unrecognized delta has been applied to the maintained specification.

---

## 9. Schema-aware parsing

### 9.1 Parse according to the effective schema

Siddhi should inspect the effective OpenSpec schema and use the appropriate parser for recognized artifact types.

The parser must not rely solely on fixed filenames or a single global workflow assumption.

### 9.2 Unknown schemas

If the schema is unknown or cannot be resolved, Siddhi should:

1. Record the detected schema name or available metadata.
2. Preserve discoverable artifact references.
3. Parse only structures that can be interpreted safely.
4. Mark unsupported interpretations explicitly.
5. Report the limitation.

It should not silently fall back to an unrelated schema and report a complete scan.

### 9.3 Unknown artifact types

A new or custom artifact should not cause the entire project ingestion to fail if its identity and basic metadata can still be recorded.

Siddhi may store its source reference and metadata while leaving semantic interpretation unsupported.

### 9.4 Parser versioning

Parser and normalization versions should be recorded whenever they may affect the interpretation of source artifacts.

When parser behavior changes, Siddhi should be able to distinguish observations produced by different versions and rerun affected analysis when justified.

### 9.5 Structural validation

Where supported and explicitly executed, OpenSpec validation results may be recorded as source-related verification observations.

Siddhi must distinguish:

- OpenSpec validation was not run.
- Validation succeeded.
- Validation reported issues.
- Validation could not run.
- Validation status is unknown.

Siddhi should not run commands that mutate source artifacts merely to obtain a validation result. It must inspect the command's behavior and options before invoking it.

---

## 10. Integration method

The adapter may use OpenSpec's supported CLI, direct read-only file access, or a combination, depending on the required information and installed version.

OpenSpec documents commands such as `list`, `show`, `status`, `schemas`, `schema`, and `validate`, including machine-readable output for supported commands. <Link url="https://openspec.dev/docs/cli" title="OpenSpec CLI documentation"/>.

The implementation should select the most reliable supported method for each operation.

### 10.1 CLI-based access

CLI-based access may be appropriate when Siddhi needs information that OpenSpec already resolves, such as its effective schema or interpreted task status.

The adapter should:

- Check CLI availability and version.
- Use supported machine-readable output where available.
- Capture exit status separately from standard output.
- Handle warnings and errors.
- Apply execution timeouts.
- Avoid write or archive commands during ordinary ingestion.

A successful CLI invocation must not automatically be interpreted as complete repository coverage. The command's actual scope and result must be considered.

### 10.2 Direct file access

Direct read-only file access may be appropriate for capturing source content, computing fingerprints, or reading artifacts not fully exposed through a supported CLI result.

It should:

- Respect the discovered OpenSpec root.
- Use safe path handling.
- Avoid writing to source files.
- Preserve source paths and relevant file metadata.
- Handle unreadable and malformed files.
- Respect the scope and permissions of the source repository.

### 10.3 Combining CLI and file access

Siddhi may combine the two approaches when necessary, but it must avoid creating contradictory interpretations.

For example, a CLI may report task progress while direct file access supplies the corresponding source text. Both observations should retain their provenance.

If the source changes between the two reads, Siddhi should detect or report the inconsistent observation context rather than assume both results represent the same revision.

### 10.4 Version compatibility

The adapter should record the OpenSpec version when available.

Unsupported versions or changes in output format should produce a visible compatibility warning or controlled failure rather than silently corrupting normalized records.

---

## 11. Provenance and historical observations

Every material OpenSpec observation should be traceable to its source.

Where available, Siddhi should preserve:

- Source project reference.
- OpenSpec root.
- Source artifact path or identifier.
- Source revision or content fingerprint.
- Observation timestamp.
- Applicable schema and configuration.
- Adapter and parser versions.
- CLI version, when relevant.
- Retrieval and parsing status.
- Relevant warnings and limitations.

Siddhi should retain historical observations according to its approved snapshot policy.

A source change must not silently rewrite the evidence supporting an earlier portfolio report or decision.

If a requirement changes, Siddhi should be able to identify the new observation and explain that a previous assessment relied on an earlier version.

---

## 12. Error handling and recovery

| Failure | Expected behavior |
|---|---|
| OpenSpec not discovered | Report absence only when the scanned scope supports that conclusion |
| Repository inaccessible | Preserve prior observations and mark current access as unavailable |
| Invalid configuration | Record the configuration issue and avoid assuming a default schema is authoritative |
| Unknown schema | Preserve artifact references and mark unsupported interpretation |
| Unknown artifact type | Record basic metadata and skip unsupported semantic parsing |
| Malformed specification | Isolate the affected artifact where possible and report a parsing issue |
| Partial repository scan | Preserve successful observations and mark coverage as partial |
| CLI unavailable | Use an approved fallback if available, otherwise report the limitation |
| CLI version incompatible | Report compatibility failure without misinterpreting the output |
| Permission denied | Report access limitations without exposing credentials |
| Source changed during ingestion | Record the inconsistent observation context or retry safely |
| Siddhi persistence failure | Report the failed operation and recover without creating duplicate identities |

A retry should not create duplicate requirements, scenarios, changes, tasks, or source observations representing the same capture.

A failed scan must not erase previously captured OpenSpec history.

---

## 13. Security and read-only guarantees

The integration must use read-only access to repository artifacts and supported read-only CLI operations.

It must not, during normal ingestion:

- Create or update changes.
- Edit specification files.
- Mark tasks complete.
- Archive changes.
- Rewrite project configuration.
- Modify schema templates.
- Commit or modify Git history.
- Send OpenSpec content to external AI services automatically.

External AI analysis is a separate Siddhi workflow. It must select its input explicitly and follow the configured data-handling policy.

If a CLI operation may change files or trigger external side effects, the adapter must not invoke it as part of read-only ingestion without an explicit, separately approved design.

---

## 14. Testing strategy

### 14.1 Repository discovery tests

Verify that Siddhi can distinguish:

- A repository with OpenSpec.
- A repository without OpenSpec within a successfully scanned scope.
- An inaccessible repository.
- A repository with incomplete scan coverage.
- A repository with OpenSpec configuration but no discovered artifacts.

### 14.2 Schema compatibility tests

Test against representative fixtures covering:

- The standard schema.
- Project-specific schemas.
- Different artifact sets.
- Different templates and artifact conventions.
- Missing or invalid schema definitions.
- Unknown schema versions.
- Additional custom artifacts.

### 14.3 Requirement and scenario tests

Verify that:

- Requirements and scenarios retain their source relationships.
- Stable identities are preserved across repeated ingestion.
- Requirement changes are detected.
- Ambiguous requirement identities are not silently merged.
- Missing scenarios are not confused with failed parsing.

### 14.4 Change and task tests

Verify that:

- Active and archived changes are distinguishable.
- Custom artifact sets are handled.
- Task status is captured without claiming independent implementation verification.
- Unknown task formats are handled safely.
- Requirement deltas are interpreted only when the format is supported.

### 14.5 Provenance and recovery tests

Verify that:

- Source observations retain paths, versions, and timestamps where available.
- Parser-version changes are distinguishable.
- Partial scans preserve successful results.
- Failed scans do not erase previous observations.
- Repeated ingestion does not create duplicate logical records.
- Ordinary ingestion does not modify source artifacts.

---

## 15. Acceptance criteria

The initial integration is ready when:

- [ ] Siddhi can discover OpenSpec within an explicitly defined project scope.
- [ ] It can identify the applicable configuration and schema where supported.
- [ ] It can read recognized specifications, requirements, and scenarios.
- [ ] It can discover changes and their supported artifacts.
- [ ] It can capture declared task status without treating it as proof of implementation.
- [ ] It can distinguish active and archived changes.
- [ ] It supports different repository schemas without requiring a universal schema.
- [ ] It preserves unknown artifact references where basic discovery is possible.
- [ ] It records provenance, observation time, and relevant parser/schema versions.
- [ ] It distinguishes missing, inaccessible, malformed, and unsupported source information.
- [ ] It retains historical observations and detects relevant changes.
- [ ] It does not modify OpenSpec artifacts during ordinary ingestion.
- [ ] Its normalized data can be used by Siddhi's evidence and portfolio workflows.

---

## 16. Implementation sequence

### Phase 1 — Inspect actual OpenSpec conventions

Identify representative repositories and inspect:

- OpenSpec versions.
- Configuration files.
- Effective schemas and schema resolution.
- Maintained specifications.
- Active and archived changes.
- Task-tracking conventions.
- Custom artifact types.
- Available CLI output and validation mechanisms.

Include repositories using different team schemas where applicable.

### Phase 2 — Define the adapter contract

Define the Siddhi-facing models for:

- OpenSpec project context.
- Specification and requirement.
- Scenario.
- Change and change artifact.
- Task observation.
- Source observation and provenance.
- Parsing and scan status.

### Phase 3 — Implement read-only ingestion

Implement discovery, schema inspection, parsing, identity resolution, and persistence.

Add tests for supported formats before connecting the adapter to portfolio assessments.

### Phase 4 — Connect to evidence workflows

Expose normalized OpenSpec observations to the evidence extraction and analysis layer.

Ensure that findings distinguish declared progress from implementation and verification evidence.

### Phase 5 — Harden compatibility

Test custom schemas, partial scans, unknown artifacts, version changes, malformed content, and recovery.

Document the supported OpenSpec versions and formats rather than claiming universal compatibility.

---

## 17. Open questions

| ID | Question | Why it matters |
|---|---|---|
| OSI-001 | Which OpenSpec versions must Siddhi support initially? | Determines CLI and file-format compatibility |
| OSI-002 | Which repository schemas and team-specific artifact types must be supported in the first release? | Determines the initial parser scope |
| OSI-003 | Should the adapter prefer CLI interpretation, direct file parsing, or a hybrid approach for each artifact type? | Balances compatibility, provenance, and completeness |
| OSI-004 | How should Siddhi identify requirements when the source has no stable requirement identifier? | Prevents incorrect identity merges |
| OSI-005 | Should archived changes be ingested by default or only when historical analysis requires them? | Affects scan cost and retained history |
| OSI-006 | Which OpenSpec validation commands are safe and useful to execute automatically? | Prevents unintended side effects |
| OSI-007 | Which source revision or fingerprint strategy should be used for local repositories? | Supports reproducible observations |
| OSI-008 | How should custom artifact types be exposed to users when Siddhi cannot interpret them? | Preserves information without overclaiming support |
| OSI-009 | What is the retention policy for full requirement and change-artifact content? | Affects storage, privacy, and historical comparison |
| OSI-010 | Should Siddhi expose source-level requirement-to-goal mappings as user-managed relationships in the first release? | Determines the initial portfolio association experience |

Resolve these questions by inspecting the installed OpenSpec implementations and representative repository fixtures. Do not invent a universal artifact schema to avoid that inspection.

## 18. Relationship to other Siddhi documents

- `source-integration.md` defines the shared adapter architecture.
- `vyasa-integration.md` defines project discovery and identity supplied by Vyasa.
- `data-ownership.md` defines OpenSpec's authority over requirements and change artifacts.
- `data-model.md` defines persisted requirements, changes, snapshots, and evidence relationships.
- `application-workflows.md` defines discovery, ingestion, assessment, and reporting workflows.
- `scanning-and-evidence.md` defines how OpenSpec observations become evidence.
- `synchronization.md` defines refresh and historical comparison.
- `security-and-privacy.md` defines source access and data-handling controls.
- `functional-requirements.md` defines the observable behaviors that must be implemented.
- `architectural-decisions.md` records the final integration and compatibility decisions.

During the later OpenSpec and OKF preparation stage, testable integration behavior should become Siddhi's own OpenSpec requirements. Reusable parsing principles, schema-compatibility guidance, and evidence interpretation rules should be captured as independent engineering knowledge in OKF.

---

**End of document**