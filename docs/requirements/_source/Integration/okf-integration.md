# OKF Integration

**Document:** `okf-integration.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Read-only integration with OKF engineering knowledge  
**Depends on:** `vision.md`, `scope-and-roadmap.md`, `functional-requirements.md`, `system-architecture.md`, `data-ownership.md`, `data-model.md`, `source-integration.md`  
**Related integration:** `openspec-integration.md`

---

## 1. Purpose

This document defines how Siddhi discovers, reads, interprets, records, and uses engineering knowledge maintained through OKF.

OKF provides knowledge that can help Siddhi understand the engineering assets, systems, designs, conventions, decisions, dependencies, and technical capabilities associated with portfolio projects.

Siddhi uses this knowledge to support questions such as:

- What engineering capabilities already exist?
- Which projects or initiatives depend on a shared internal tool?
- What technical foundations support a proposed outcome?
- Which architectural decisions or constraints affect a plan?
- What engineering knowledge is available, missing, outdated, or awaiting validation?
- Can an existing capability be reused instead of developed again?
- What evidence supports the assessment of a goal or initiative?

The integration must preserve the distinction between **knowledge being present, knowledge being declared valid, and knowledge being independently verified**.

## 2. Design principles

### 2.1 OKF remains the knowledge authority

OKF remains authoritative for its knowledge documents, concept metadata, relationships, provenance, and any validation status defined by the actual OKF implementation.

Siddhi must not silently rewrite, reinterpret as fact, or replace the authoritative source content.

### 2.2 Siddhi owns portfolio interpretation

Siddhi owns the portfolio-level interpretation of knowledge, including:

- How knowledge relates to goals, initiatives, projects, and intended outcomes.
- Whether available knowledge appears relevant to a goal.
- Whether additional evidence or clarification is required.
- Which knowledge gaps may affect a plan.
- The strategic implications and recommendations derived from the available evidence.

These assessments belong to Siddhi. They must not be written back into OKF as if they were source-authored facts.

### 2.3 Do not assume a universal knowledge taxonomy

OKF implementations and knowledge collections may use different concept types, metadata fields, schemas, and conventions.

Siddhi must discover and respect the actual format and validation rules used by each configured knowledge source. It must not require every source to use a fixed taxonomy such as `architecture`, `decision`, `capability`, or `component`.

Where a concept cannot be mapped to a known Siddhi category, Siddhi must preserve it as a generic knowledge item rather than discard it.

### 2.4 Parsing is not verification

Successful parsing proves that Siddhi could read a document according to its parser's rules. It does not prove that the content is correct, current, complete, or implemented.

Likewise, a source-declared validation or review status must be represented according to its actual meaning. Siddhi must not turn a source status into a stronger assurance than the source supports.

### 2.5 Independent operation

OKF knowledge must remain useful without Siddhi, and Siddhi must remain usable when OKF is unavailable.

The integration may enrich portfolio assessments, but the absence of OKF must not prevent users from defining goals, maintaining plans, or recording decisions.

## 3. Scope

### 3.1 Included

The integration covers:

1. Identifying configured OKF knowledge sources.
2. Discovering their locations and applicable format or schema.
3. Reading knowledge documents and supported metadata.
4. Extracting stable concept identities and document relationships.
5. Capturing source provenance and available lifecycle or validation information.
6. Creating normalized knowledge records and source snapshots in Siddhi.
7. Detecting additions, modifications, removals, and source-access failures.
8. Linking knowledge to portfolio entities where supported by explicit references or user-confirmed mappings.
9. Assessing knowledge relevance and freshness without modifying source knowledge.
10. Reporting missing, conflicting, stale, unsupported, or unavailable knowledge.
11. Providing evidence to deterministic portfolio analysis and optional external AI analysis.

### 3.2 Excluded

The initial integration does not:

- Create, edit, delete, or reorganize OKF knowledge documents.
- Automatically fix knowledge validation errors.
- Automatically author new concepts or relationships.
- Assume every OKF document describes a project, feature, or deliverable.
- Treat a concept title or keyword match as proof of a capability.
- Infer that an engineering capability is implemented merely because documentation describes it.
- Make OKF validation equivalent to build, test, deployment, or production verification.
- Require an LLM to parse routine metadata or detect ordinary file changes.
- Make Siddhi's portfolio classifications part of the OKF source of truth.
- Require OpenSpec requirements to exist before OKF knowledge can be ingested.

## 4. Source ownership and boundaries

| Information | Authority |
|---|---|
| Knowledge document content | OKF source |
| Concept metadata and source-defined type | OKF source |
| Source-defined concept relationships | OKF source |
| Source-defined provenance and validation information | OKF source |
| Repository identity and project inventory | Vyasa |
| Requirements, scenarios, and change status | OpenSpec |
| Git history and repository change evidence | Git/VCS |
| Build, test, and release results | Their originating verification systems |
| Portfolio goals, priorities, plans, and milestones | Siddhi |
| Portfolio-to-knowledge mappings and assessments | Siddhi |
| Knowledge relevance and portfolio gap assessments | Siddhi |
| Strategic recommendations and approved portfolio decisions | Siddhi |

Siddhi may cache normalized representations of OKF data. These representations are derived records, not replacements for the source.

## 5. Integration architecture

The OKF integration follows the common source-adapter architecture defined in `source-integration.md`.

```text
Configured OKF Source
        |
        v
Source Discovery and Access
        |
        v
Format / Schema Detection
        |
        v
OKF Reader and Parser
        |
        v
Normalized Knowledge Records
        |
        +------> Source Snapshot and Provenance
        |
        v
Change Detection and Freshness Assessment
        |
        v
Portfolio Evidence and Knowledge Mapping
        |
        v
Deterministic Analysis and Reports
        |
        +------> Optional External AI Analysis
```

The integration must separate source access, parsing, normalization, persistence, and portfolio interpretation. This prevents changes in an OKF implementation from unnecessarily changing the portfolio domain model.

### 5.1 Adapter responsibilities

The adapter must:

- Identify the configured source and its access method.
- Establish the actual format and schema applicable to the source.
- Read supported documents without modifying them.
- Extract available metadata and relationships.
- Preserve the original source identity and location.
- Report parse and access errors at an appropriate level.
- Produce normalized records for Siddhi.
- Expose capabilities and limitations to the ingestion service.

The adapter must not make strategic decisions or approve portfolio changes.

### 5.2 Supported access methods

The implementation may support one or more of the following, based on the actual OKF installation:

- Read-only filesystem access.
- Reading an OKF directory inside an already available repository.
- Reading a repository snapshot supplied by an approved source adapter.
- Invoking a supported OKF CLI for discovery, inspection, or validation.
- Reading a machine-readable export if the installed implementation provides one.

The first implementation should prefer the simplest reliable, read-only method that exposes the required information.

A CLI should not become a mandatory runtime dependency merely because it is available. Conversely, direct parsing should not replace an existing supported interface if doing so would bypass important schema or validation semantics.

The final choice remains an implementation decision pending inspection of the actual OKF setup.

## 6. Source discovery and configuration

Each configured OKF source should have a Siddhi source configuration containing the following logical information where applicable:

| Field | Purpose |
|---|---|
| Source ID | Stable Siddhi identifier for the configured source |
| Source name | Human-readable name |
| Source type | Identifies the OKF integration |
| Repository reference | Optional link to the owning project or repository |
| Source location | Approved directory, bundle, or supported access reference |
| Format/version | Detected or declared format information |
| Schema reference | Applicable schema or validation configuration, if any |
| Access method | Filesystem, repository adapter, CLI, or other supported method |
| Enabled state | Whether ingestion is permitted |
| Last successful scan | Timestamp of the latest successful scan |
| Last attempted scan | Timestamp of the latest attempt |
| Scan outcome | Success, partial success, failure, or another defined status |
| Configuration revision | Identifies the configuration used for an ingestion run |

These fields describe the integration configuration, not mandatory fields that must exist in every OKF source.

### 6.1 Discovery rules

Discovery must:

1. Confirm that the configured location is accessible.
2. Identify the applicable OKF format and version when possible.
3. Locate the documents recognized by that format.
4. Identify schema or validation configuration where applicable.
5. Report unsupported or ambiguous configurations.
6. Record the discovered source structure and scan outcome.

Discovery must not silently select a different source when the configured source is missing or inaccessible.

If multiple schema definitions or format conventions appear to apply, Siddhi must report the ambiguity and use only a resolution rule that is explicitly supported by the actual implementation.

## 7. Knowledge normalization

Siddhi requires a normalized internal representation for portfolio analysis. This representation must retain the source information needed to explain where each record came from.

### 7.1 Logical knowledge record

Each normalized knowledge record should support the following fields where available:

| Field | Description |
|---|---|
| Knowledge record ID | Stable Siddhi identifier |
| Source ID | Configured OKF source |
| Source concept ID | Native identifier defined by the source format |
| Source path or URI | Location of the source document |
| Concept type | Original source-declared type |
| Title | Source title, or a documented fallback when absent |
| Description | Source description when present |
| Metadata | Supported metadata preserved without loss |
| Content reference | Reference to retained source content or a snapshot |
| Relationships | Parsed source-defined links or references |
| Provenance | Source attribution and origin information |
| Source status | Original lifecycle or validation status when available |
| Content fingerprint | Used for deterministic change detection |
| First observed | First successful observation by Siddhi |
| Last observed | Most recent successful observation |
| Last changed | Latest observed source-content change |
| Source revision | Commit, revision, or version when available |
| Parse status | Result of Siddhi's parsing process |
| Snapshot reference | Link to the ingestion snapshot that supplied the record |

The actual schema may expose only a subset of these fields. Missing values must remain explicitly unavailable rather than being fabricated.

### 7.2 Preserve original metadata

Normalization must not erase source-specific information simply because Siddhi does not yet understand it.

The adapter should retain:

- Original type names.
- Recognized standard fields.
- Additional source-defined metadata.
- Original source identifiers and paths.
- Parsed relationships.
- Relevant validation or parsing diagnostics.

Unknown fields should be retained where feasible, subject to security and storage constraints.

The normalized model should separate source metadata from Siddhi-derived fields so that a portfolio assessment cannot accidentally overwrite the original source value.

### 7.3 Concept identity

The adapter must use the identity rules of the actual OKF implementation.

If the source defines a concept ID from a relative document path, the adapter should preserve that identifier. If the source provides a stable identifier independent of path, that identifier should be used according to the source contract.

Siddhi must not assume that titles are unique or stable.

If a source document is moved or renamed, the adapter should distinguish between a confirmed move and a deletion followed by an addition only when available evidence supports that distinction. Otherwise, the result should be recorded as an identity change that requires reconciliation.

## 8. Relationships and portfolio mapping

Knowledge relationships can help Siddhi understand how engineering concepts relate to each other and to portfolio entities.

### 8.1 Source-defined relationships

The adapter should capture supported relationships such as document links, references, or other explicit relationship metadata.

Each relationship should retain:

- Source and target identifiers.
- Relationship type, when defined.
- Originating document.
- Resolution status.
- Provenance and observation snapshot.

An unresolved reference must not be silently discarded. It should be represented as unresolved when retaining it is useful to later analysis.

### 8.2 Portfolio mappings

Siddhi may associate knowledge records with:

- Projects discovered by Vyasa.
- Goals and intended outcomes.
- Initiatives and milestones.
- Engineering capabilities.
- Decisions, dependencies, and constraints.
- Other relevant knowledge records.

A mapping may be based on:

1. An explicit stable reference in the source.
2. A configured mapping rule.
3. A deterministic match using reliable identifiers.
4. A candidate association proposed by an analysis process.
5. A user-confirmed association.

Siddhi must retain the mapping method and confidence or certainty classification where applicable.

A candidate mapping must not be treated as a confirmed relationship without an established approval rule.

Keyword overlap, similar titles, or a shared directory alone are insufficient to prove that a concept satisfies a goal or belongs to a particular initiative.

### 8.3 Cross-system relationships

Siddhi may use OpenSpec, Vyasa, Git, verification records, and OKF together.

For example, an OKF concept may describe an architectural capability, an OpenSpec change may describe a requirement to extend it, Git history may show relevant source changes, and a verification artifact may provide test evidence.

These records should remain separate evidence sources connected through explicit or assessed relationships. They must not be collapsed into a single unsupported assertion that the capability is complete.

## 9. Validation, trust, and freshness

### 9.1 Distinguish validation layers

Siddhi must distinguish at least the following concepts:

| Layer | What it establishes |
|---|---|
| Source access | Siddhi could access the configured source |
| Parsing | Siddhi could interpret a document using its parser |
| Format or schema validation | A source validator reported a result against its applicable rules |
| Source-declared review or verification | The source records a particular review or verification event |
| Portfolio assessment | Siddhi assessed the relevance or sufficiency of knowledge for a goal |
| Implementation verification | A separate source provides evidence of actual implementation or behavior |

These layers are not interchangeable.

A document may parse successfully but fail schema validation. A document may pass schema validation while describing an obsolete design. A verified knowledge concept may still lack evidence that a specific implementation is deployed.

### 9.2 Source validation

If the installed OKF implementation exposes a supported validation operation, Siddhi may invoke it in read-only mode and record the result.

A validation observation should include:

- Source and bundle reference.
- Validator identity and version, where available.
- Applicable schema or format version.
- Execution time.
- Outcome.
- Errors and warnings, or a reference to the detailed report.
- Scope of validation.
- Source revision or snapshot to which the result applies.

Siddhi must not represent a validation result as current if the corresponding source has changed since validation.

If validation is not available, Siddhi should record that it was not performed. It must not infer a successful validation from successful parsing.

### 9.3 Trust and verification

Where the source format supports provenance or verification metadata, Siddhi should preserve the original declarations and their meaning.

A source-declared verification event is evidence that a verification or review was recorded. It is not automatically independent certification or proof of truth.

Siddhi may use source trust metadata as an input to its assessments, but it must preserve the distinction between:

- What the source declares.
- What Siddhi has directly observed.
- What an independent verification artifact establishes.
- What remains an inference or recommendation.

### 9.4 Freshness

Siddhi should track source freshness using observable information such as:

- Last successful ingestion.
- Source modification timestamp.
- Git commit or revision.
- Source-declared review or expiry metadata.
- Source-defined lifecycle status.
- Age of the latest applicable validation or verification result.

Freshness rules should be configurable or derived from an explicitly agreed policy.

An old document is not automatically false. A recent modification is not automatically correct. Siddhi should report the relevant signals and avoid making stronger claims than those signals justify.

If the source is unavailable, Siddhi must distinguish between the last known snapshot and the current source state.

## 10. Ingestion and change detection

### 10.1 Ingestion workflow

A typical ingestion run consists of:

1. Resolve the configured source.
2. Establish access and source identity.
3. Discover applicable documents and metadata.
4. Read and parse the supported content.
5. Apply available format or schema validation, if configured.
6. Normalize concepts and relationships.
7. Compute deterministic fingerprints for supported source content.
8. Compare records with the previous successful snapshot.
9. Record additions, modifications, removals, and unresolved identities.
10. Persist normalized records, provenance, diagnostics, and snapshot metadata.
11. Update source freshness and scan status.
12. Make the resulting evidence available to portfolio analysis.

Steps that fail must be reported. A partial scan must not be reported as a fully successful scan.

### 10.2 Deterministic change detection

Where practical, content fingerprints should be calculated from a stable representation of the source document and relevant metadata.

The fingerprinting strategy must be documented and tested to avoid false changes caused only by irrelevant serialization differences.

The integration should distinguish:

- New knowledge records.
- Modified content or metadata.
- Removed records.
- Unchanged records.
- Identity changes or uncertain moves.
- Records that could not be read.
- Records that could not be parsed.
- Records excluded by the applicable format rules.

A failed scan must not cause every previously observed record to be marked as deleted.

### 10.3 Snapshot integrity

Every ingestion run should produce a snapshot record containing:

- Source identity.
- Run ID.
- Start and completion times.
- Source revision or observed version, when available.
- Number of discovered, parsed, accepted, rejected, and unchanged records.
- Number of additions, modifications, and removals.
- Validation outcome, if performed.
- Warnings and errors.
- Overall completion status.

The implementation should preserve enough historical information to compare portfolio assessments over time without retaining unlimited duplicate content.

The exact content-retention and snapshot-pruning policy is an open decision.

## 11. Use in portfolio analysis

OKF data is an input to Siddhi's deterministic analysis engine and optional external strategic analysis.

### 11.1 Deterministic analysis

Deterministic processing should handle tasks such as:

- Counting and categorizing known concepts.
- Listing concepts associated with a project or initiative.
- Finding unresolved links.
- Detecting missing or malformed metadata.
- Comparing snapshots and reporting changes.
- Identifying declared stale or deprecated knowledge.
- Reporting missing knowledge mappings.
- Identifying knowledge sources that have not been refreshed.
- Comparing explicit references against expected relationships.
- Generating traceable reports of evidence availability and gaps.

These tasks should not require an LLM.

### 11.2 Strategic interpretation

External AI may help evaluate questions such as:

- Does the available engineering knowledge support the proposed goal?
- Can existing internal tools enable several portfolio outcomes?
- Which architectural or capability gaps may affect delivery?
- What additional evidence is needed before approving an investment?
- Are there opportunities to reuse existing capabilities?
- What trade-offs should decision-makers consider?

AI outputs must be recorded as assessments or recommendations with provenance and appropriate uncertainty. They must not automatically become verified source facts or approved portfolio decisions.

### 11.3 Evidence classifications

For knowledge-related portfolio assessments, Siddhi should support a classification model consistent with the broader portfolio evidence model, including:

- **Confirmed:** Explicitly supported by the required evidence and applicable acceptance rules.
- **Candidate:** Potentially relevant but not sufficiently established.
- **Missing:** Expected evidence has not been found within the defined search scope.
- **Unknown:** Available information is insufficient to determine the state.
- **Stale:** Evidence may no longer reflect the current source state.
- **Conflicting:** Sources provide inconsistent information.
- **Unverified:** The available information has not met the required verification standard.

These classifications apply to Siddhi's assessment of evidence, not as a replacement for the source's own statuses.

A report must state the scope of the search or ingestion on which a missing-evidence conclusion is based. A concept not found in an incomplete scan cannot be confidently declared absent.

## 12. Error handling and recovery

The integration should handle errors at the smallest useful scope.

| Failure | Expected behavior |
|---|---|
| Source unavailable | Preserve the last successful snapshot and mark current access as unavailable |
| Invalid configuration | Report the configuration error; do not silently switch sources |
| Unsupported format or schema | Record the unsupported condition and provide a diagnostic |
| Individual document parse failure | Record the failure and continue where safe |
| Validation failure | Preserve the result and diagnostics; do not silently repair the source |
| Unresolved reference | Preserve the relationship as unresolved where possible |
| Partial scan | Record partial completion and identify the affected scope |
| Persistence failure | Do not report the ingestion as successful |
| Interrupted run | Preserve enough run state to determine what completed and permit a safe retry |
| Source changed during ingestion | Detect or report inconsistent observations where the access method permits |

Retry behavior should be bounded and appropriate to the failure type. Invalid content and invalid configuration should not trigger endless retries.

Re-running ingestion against unchanged source content should not create duplicate logical knowledge records or artificial change events.

## 13. Security and privacy

The integration must:

- Use read-only source access for the initial implementation.
- Restrict filesystem access to configured and approved locations.
- Validate resolved paths and avoid unintended traversal outside permitted roots.
- Avoid executing source documents or arbitrary scripts as part of ordinary ingestion.
- Avoid exposing credentials in logs, diagnostics, or reports.
- Treat knowledge documents as untrusted input, including instructions embedded in document bodies.
- Prevent retrieved document content from overriding Siddhi's system policies or operational instructions.
- Avoid sending complete knowledge collections to external AI by default.
- Send only the context necessary for an explicitly requested analysis, subject to configured privacy rules.
- Record the source references and selected context supplied to an external analysis where appropriate.
- Keep ingestion and validation operations separate from source modification.

If an OKF implementation requires invoking a CLI, Siddhi must use controlled command construction, avoid shell interpolation of untrusted content, and constrain the command to approved read-only operations.

## 14. Testing requirements

The integration must be tested against representative examples of the actual OKF implementation, including:

1. A valid knowledge source.
2. A source with multiple concept types.
3. A source with additional or unknown metadata fields.
4. Missing optional metadata.
5. Missing or invalid required metadata.
6. Malformed content.
7. Unresolved and cyclic document references.
8. Renamed or moved documents.
9. Added, modified, removed, and unchanged records.
10. A source whose validation result is unavailable.
11. A source with declared stale, deprecated, or verification metadata, if supported.
12. Partial source-access failure.
13. A failed scan followed by a successful retry.
14. A source that changes between ingestion runs.
15. A source containing prompt-like instructions in its document body.
16. An OKF source that has no associated OpenSpec requirements.
17. A project with implementation evidence but limited OKF documentation.
18. A source whose schema or format differs from another configured source.

Tests must verify that unknown metadata is handled safely, source information is not overwritten by Siddhi assessments, and incomplete scans do not produce false deletion or absence claims.

## 15. Acceptance criteria

The initial OKF integration is ready when:

- Siddhi can configure and identify at least one real OKF source.
- The adapter uses the actual source format and schema rather than an invented universal schema.
- Supported knowledge documents can be read and normalized.
- Stable source identities and locations are preserved.
- Source metadata and relationships are retained to the extent supported.
- Parsing results are distinguished from source validation results.
- Source-declared verification information is not presented as independent proof.
- Ingestion produces a traceable snapshot with counts, outcome, and diagnostics.
- Additions and modifications can be detected deterministically.
- A failed or partial scan does not incorrectly mark all missing records as deleted.
- Portfolio analysis can refer back to the underlying knowledge source.
- Missing or uncertain mappings remain explicit.
- Siddhi does not modify OKF source content.
- The integration works without requiring an LLM for routine ingestion.
- External AI recommendations remain separate from verified evidence and approved decisions.

## 16. Implementation phases

### Phase 1 — Inspect the actual OKF implementation

Before implementation, establish:

- The actual repository or installed package.
- The specification version and supported extensions.
- The knowledge bundle structure and schema files.
- The available CLI or API, if any.
- The validation and metadata conventions.
- The actual identifiers used for knowledge concepts.
- How the knowledge source is associated with a Vyasa project or repository.
- How the source is versioned and accessed.

**Deliverable:** A verified source contract and a small set of representative fixtures.

### Phase 2 — Read-only ingestion

Implement:

- Source configuration and discovery.
- Read-only access.
- Parsing and normalization.
- Source identity and provenance.
- Snapshot persistence.
- Parse diagnostics and scan outcomes.

**Deliverable:** Siddhi can ingest an OKF source and display its knowledge inventory without modifying the source.

### Phase 3 — Change tracking and validation

Implement:

- Deterministic fingerprints.
- Snapshot comparison.
- Addition, modification, and removal detection.
- Validation integration if supported.
- Freshness and failure reporting.

**Deliverable:** Siddhi can reliably report what changed and what could not be assessed.

### Phase 4 — Portfolio evidence integration

Implement:

- Explicit project and goal mappings.
- Knowledge relationship traversal.
- Evidence classification and gap reporting.
- Deterministic portfolio reports.
- Cross-references to OpenSpec and other evidence sources where available.

**Deliverable:** Siddhi can use OKF as one independent evidence source for assessing portfolio goals and initiatives.

### Phase 5 — Optional strategic analysis

Add external AI workflows for deeper knowledge interpretation, opportunity assessment, reuse analysis, and strategic trade-offs.

**Deliverable:** Traceable recommendations that remain separate from authoritative source records and approved decisions.

---

## 17. Open questions

These questions must be resolved during the design review or implementation discovery. They are not assumed to have been decided.

| ID | Question | Why it matters |
|---|---|---|
| OKFI-001 | Which exact OKF implementation, repository, version, and schema are used by the project? | Determines the real source contract |
| OKFI-002 | Is the knowledge source a standalone bundle, a directory inside a repository, or a separate repository? | Determines discovery and access |
| OKFI-003 | Should Siddhi parse the source directly, invoke an OKF CLI, or use a hybrid approach? | Determines implementation complexity and compatibility |
| OKFI-004 | What stable identity should Siddhi use when a knowledge document is moved or renamed? | Prevents incorrect identity changes |
| OKFI-005 | Which metadata and relationship types are actually present in the existing knowledge collection? | Defines the initial normalization scope |
| OKFI-006 | Which source validation commands and verification signals are available, and what do they guarantee? | Prevents overstated confidence |
| OKFI-007 | How should source snapshots and historical content be retained and pruned? | Balances auditability and storage |
| OKFI-008 | How are OKF sources linked to projects discovered by Vyasa? | Enables portfolio-level mapping |
| OKFI-009 | Which knowledge-to-goal mappings can be automatic, and which require user confirmation? | Controls false associations |
| OKFI-010 | Should external AI receive only selected concepts, or can users explicitly authorize a larger context? | Defines privacy and cost boundaries |

## 18. Related documentation

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
- `scanning-and-evidence.md`
- `security-and-privacy.md`

---

## 19. Reference material

The following public references describe Open Knowledge Format and related tooling. They are useful for orientation but **do not establish which schema or tooling the Siddhi project actually uses**.

- [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — format concepts, Markdown documents, metadata, provenance, and trust signals. The repository notes that this copy is a frozen snapshot, so the canonical specification should be confirmed before implementation. <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md>
- [OKF CLI](https://github.com/okfcli/okf) — an example of tooling for validation, listing, inspection, search, and graph operations.
- [OKF-Schema documentation](https://okf-schema.readthedocs.io/en/stable/) — an example of a stricter schema-based approach that adds constraints beyond the minimal format.

These references illustrate why the adapter should inspect the real source contract instead of treating every OKF-compatible knowledge collection as identical.

**Document status:** Draft for review. The source format, schema, validation semantics, and access method must be verified against the actual OKF implementation before this document is converted into implementation-level OpenSpec requirements.