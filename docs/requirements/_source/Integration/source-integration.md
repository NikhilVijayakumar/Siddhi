# Source Integration

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `source-integration.md`  
**Status:** Draft for review  
**Scope:** Source adapter architecture, integration contracts, source capabilities, access, normalization boundaries, and failure handling for the Siddhi API.

---

## 1. Purpose

Siddhi integrates information from external engineering and workspace systems to help users understand their portfolio, assess progress, and make strategic decisions.

This document defines how Siddhi accesses those systems without replacing their responsibilities or depending on one universal source format.

It establishes:

- The source adapter architecture.
- The responsibilities and contracts of source integrations.
- The integration boundaries for Vyasa, OpenSpec, OKF, Git, and verification sources.
- Source discovery, identity resolution, and access requirements.
- Normalization and provenance expectations.
- Error handling, retry behavior, and capability reporting.
- Security and testing requirements for source integrations.

This document does not define the full evidence-assessment algorithm, the physical database schema, or the complete synchronization policy.

## 2. Design principles

### 2.1 Sources remain authoritative

Each source retains authority over its own records.

Siddhi reads source information, creates local references, and maintains normalized observations. It does not silently modify the source.

### 2.2 Integrations are capability-based

Not every source supports every operation.

An integration may support project discovery but not source history, or metadata retrieval but not content retrieval. Siddhi must discover or declare supported capabilities rather than assume that all adapters implement an identical feature set.

### 2.3 Adapters isolate source-specific behavior

Source-specific APIs, file layouts, schemas, authentication mechanisms, and parsing rules belong within the corresponding adapter or its supporting modules.

Core portfolio logic should consume normalized contracts instead of directly depending on a particular source's file structure or API.

### 2.4 Routine ingestion is deterministic

Reading, parsing, validating structure, normalizing, deduplicating, and comparing source information should use deterministic code wherever practical.

External AI must not be required to identify a repository, parse a known file format, determine whether a scan completed, or record a source observation.

### 2.5 Source access must be explicit

Each integration must declare what it reads, how it accesses the source, and which permissions it requires.

Source integration must not silently perform repository checkouts, write files into source repositories, commit changes, or modify external records.

### 2.6 Partial coverage must be visible

A source can be reachable while some of its records remain inaccessible or unprocessed.

Siddhi must represent scan coverage and limitations separately from connection status.

### 2.7 Integrations must be replaceable

A source adapter should be replaceable or upgradeable without requiring the portfolio domain model to be rewritten, provided the adapter continues to satisfy the supported contract.

## 3. Integration architecture

The proposed architecture separates source-specific access from application workflows and domain logic.

<box border radius="lg" padding={3} gap={2} align="center">
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **Application workflows**

    <text size="sm" textAlign="center">Configure · Discover · Ingest · Refresh · Compare</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box border radius="md" padding={3} width="100%" align="center">
    **Source integration coordinator**

    <text size="sm" textAlign="center">Scope · Capabilities · Execution · Coverage · Errors</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box background="surface" border radius="md" padding={3} width="100%" align="center">
    **Source adapter contract**

    <text size="sm" textAlign="center">Discovery · Retrieval · Identity · Source observations</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <grid columns={2} gap={2}>
    <grid-item>
      <box background="surface-secondary" radius="md" padding={2} align="center">
        **Vyasa**

        <text size="xs" textAlign="center">Project inventory</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="md" padding={2} align="center">
        **OpenSpec**

        <text size="xs" textAlign="center">Requirements and changes</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="md" padding={2} align="center">
        **OKF**

        <text size="xs" textAlign="center">Engineering knowledge</text>
      </box>
    </grid-item>
    <grid-item>
      <box background="surface-secondary" radius="md" padding={2} align="center">
        **Git / verification**

        <text size="xs" textAlign="center">History and results</text>
      </box>
    </grid-item>
  </grid>
  <icon name="arrow-down" size="lg" />
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **Observation and persistence boundary**

    <text size="sm" textAlign="center">Identity mapping · Snapshots · Provenance · Ingestion history</text>
  </box>
</box>

The diagram describes logical responsibilities. It does not require a separate service for every box.

The initial implementation should use a modular monolith. Source adapters should run within the Siddhi API process unless later evidence justifies separate workers or processes.

## 4. Source integration categories

### 4.1 Vyasa — project discovery

Vyasa is the primary source for Siddhi's project and repository inventory.

The integration should support, where exposed by Vyasa:

- Listing known projects.
- Reading project identifiers and recorded names.
- Reading repository origins and discovered locations.
- Reading declared technology and framework metadata.
- Reading documentation, OpenSpec, and OKF availability indicators.
- Reading inventory scan timestamps and status.
- Identifying changes between successive inventory observations.

Siddhi must not assume that all of these fields are available or verified. It must inspect the actual Vyasa interface and represent unsupported or unavailable information explicitly.

The adapter should not require Siddhi to scan or clone every repository just to obtain the inventory.

If a deeper repository scan is required, that should be a separate capability with its own scope and access rules.

### 4.2 OpenSpec — requirements and change artifacts

The OpenSpec integration reads the actual requirements and change artifacts available in the target project.

Potential information includes:

- Specification identifiers and content.
- Requirements and scenarios.
- Change proposals and specifications.
- Task lists and declared task status.
- Artifact paths and available metadata.
- References among specifications, changes, and tasks.
- Available schema or configuration information relevant to interpretation.

The adapter must follow the installed OpenSpec conventions of the target repository.

It must not assume every repository uses the same schema, artifact names, directory layout, templates, or workflow configuration.

If different teams use different schemas, the adapter should preserve enough information to identify the applicable schema and interpret the artifact accordingly.

The integration reads the source artifacts; it does not create, rewrite, approve, or close OpenSpec artifacts during ordinary ingestion.

### 4.3 OKF — engineering knowledge

The OKF integration reads engineering knowledge according to the actual installed OKF structure and supported interfaces.

Potential information includes:

- Knowledge artifacts and their identifiers.
- Document and record metadata.
- Concepts and relationships.
- Architecture and design rationale.
- Decisions, constraints, and other declared knowledge.
- Available validation or review status.
- References among knowledge artifacts.

The integration must inspect the installed OKF format rather than assume a universal directory layout or schema.

OKF knowledge must remain independently meaningful. A knowledge artifact does not need an OpenSpec requirement to be valid as knowledge, and an OpenSpec requirement does not need an OKF artifact to exist.

The adapter must not claim that an artifact is verified simply because it was discovered or parsed successfully.

### 4.4 Git and version-control sources

Git integration provides repository-history observations where access and tooling permit.

Potential capabilities include:

- Identifying the repository and available remote information.
- Reading commit identifiers and timestamps.
- Reading branches and tags.
- Reading changed paths and commit summaries.
- Observing repository state and relevant revisions.
- Comparing history between observations.

The implementation may support local Git repositories, remote provider APIs, or both. These access modes should be declared separately because their permissions and capabilities differ.

**No checkout or working-tree mutation is permitted in the normal integration path.**

For local repositories, the adapter may read existing Git metadata and history. For remote repositories, it may use supported provider APIs or other explicitly configured read-only access methods.

A full clone or checkout, if ever needed for a particular capability, requires a separately approved design. It must not be an undocumented side effect of project discovery.

### 4.5 Verification sources

Verification integrations read results produced by build, test, release, or other verification systems.

Potential capabilities include:

- Retrieving test results.
- Retrieving build outcomes.
- Identifying the source revision tested or built.
- Retrieving release or deployment metadata.
- Reading timestamps and result details.
- Linking results to a project or repository.

Siddhi should not assume that a verification source is available for every project.

It must distinguish a failed verification run from an unavailable verification source, an unexecuted test suite, and an unknown verification state.

### 4.6 Future source categories

The adapter model should allow additional sources to be introduced without changing the core portfolio domain.

Possible future sources include issue trackers, documentation platforms, delivery systems, and other project-management tools.

These are extension opportunities, not required integrations for the first usable release.

Each additional integration must establish its own authority boundary, permissions, capabilities, and provenance behavior before being enabled.

## 5. Source adapter contract

Each adapter must implement a defined contract that the source integration coordinator can invoke consistently.

The contract should support the following logical operations where applicable.

### 5.1 Capability discovery

The adapter reports which operations it supports, such as:

- Source connection validation.
- Project or artifact discovery.
- Metadata retrieval.
- Content retrieval.
- Revision or history retrieval.
- Incremental change detection.
- Verification-result retrieval.

A capability may be unsupported, supported, or temporarily unavailable.

Unsupported functionality must not be represented as a successful empty result.

### 5.2 Connection validation

The adapter validates whether the configured source can be accessed for the requested operation.

The result should distinguish, where possible:

- Valid configuration and successful access.
- Invalid configuration.
- Authentication failure.
- Insufficient permission.
- Source unavailable.
- Unsupported operation.
- Unknown or unclassified failure.

A connection test should be bounded and should not initiate a full scan.

### 5.3 Discovery

The adapter discovers records within a defined scope.

The result should include:

- The discovered identities.
- The requested scope.
- The source and observation context.
- Pagination or continuation information, where applicable.
- Coverage information.
- Warnings and errors.

Discovery must distinguish a confirmed empty result from an incomplete or failed scan.

### 5.4 Retrieval

The adapter retrieves the content or metadata required for a supported operation.

Retrieval should use stable source identifiers where available. The adapter should avoid repeated broad scans when a direct lookup is supported.

When content cannot be retrieved, the result should retain the known identity and describe the retrieval failure rather than discarding the reference.

### 5.5 Source observation

The adapter returns source observations with sufficient information for Siddhi to preserve provenance.

Where available, observations should include:

- Source-system identity.
- External artifact identifier.
- Artifact type.
- Source revision or version.
- Source locator.
- Observation timestamp.
- Content or metadata payload.
- Content fingerprint, where useful.
- Retrieval status and known limitations.

The adapter reports what it observed. It does not decide whether the observation proves a strategic outcome.

### 5.6 Incremental retrieval

If a source supports change tokens, revision-based retrieval, timestamps, or equivalent mechanisms, the adapter may use them to reduce repeated processing.

Incremental retrieval must be supported by source-specific guarantees. Siddhi must not assume that a timestamp or cursor captures every change unless the source contract establishes that behavior.

If the source cannot reliably provide incremental changes, the adapter may perform a broader scan.

### 5.7 Contract consistency

Adapters should use consistent result and error structures, even when their internal mechanisms differ.

The coordinator should not need to know whether a source was accessed through an API, local filesystem, Git metadata, or structured files to record the outcome of an operation.

The exact Python interfaces and Pydantic models will be specified during implementation design.

## 6. Source configuration and capability records

Each configured source should have a Siddhi-owned configuration record containing only the metadata required to manage the integration.

Conceptual fields include:

- Stable Siddhi source identifier.
- Source type.
- Display name.
- Connection or location reference.
- Adapter identifier and version.
- Enabled or disabled state.
- Configured scope.
- Declared capabilities.
- Last successful access time.
- Last attempted access time.
- Latest known connection status.
- Configuration validation status.

Credentials must be stored separately through the approved credential mechanism. The source configuration record should contain a credential reference where necessary, not the secret itself.

Configuration status, connection status, and scan status must remain distinct.

For example, a source can be correctly configured while temporarily unavailable, or reachable while a particular scan is incomplete.

## 7. Source discovery and identity resolution

### 7.1 Stable identity

Where the source provides a stable identifier, Siddhi should use it to identify the external artifact.

A logical source identity should be based on the source system and its external identifier, not just the display name or current path.

### 7.2 Composite identity

If a source does not provide a stable identifier, Siddhi may use a documented composite identity strategy based on available attributes.

Such strategies must account for renames and relocation where possible.

If two records cannot be matched reliably, the adapter or coordinator should preserve the ambiguity rather than merge them based on a name match alone.

### 7.3 Renames and relocations

A source artifact may retain its identity while its name or locator changes.

When Siddhi detects a likely rename or relocation, it should:

1. Preserve the known source identity.
2. Record the newly observed locator or name.
3. Retain the prior observation according to the snapshot policy.
4. Mark the identity match as confirmed or provisional according to available evidence.

### 7.4 Missing records

A record absent from a scan may have been deleted, moved, filtered out, or made inaccessible.

Siddhi must not automatically classify it as deleted unless the source provides sufficient evidence.

The scan's scope and completeness must be considered before interpreting missing records.

## 8. Normalization boundary

Source adapters should perform the source-specific interpretation needed to return consistent observation structures.

The shared normalization layer should convert those observations into Siddhi's common internal representation.

The two responsibilities should remain distinct:

- **Adapter parsing:** Understand the source format and extract source-native meaning.
- **Shared normalization:** Map common concepts into Siddhi's normalized vocabulary while preserving source-specific information where needed.

For example, different sources may use different names for project identifiers, revision identifiers, timestamps, or status fields. Siddhi can normalize those fields while retaining the original value and its meaning where needed for interpretation.

Normalization must not silently erase important source distinctions.

### 8.1 Unknown and unsupported fields

If a source does not provide a field, Siddhi should represent it as unavailable or unknown rather than invent a value.

If a source provides a new field that the adapter does not understand, the system should handle it according to its schema-evolution policy and record any material limitation.

### 8.2 Status normalization

Source-native statuses should be preserved alongside any normalized classification.

For example, a source's declared task status may be mapped to a Siddhi category for reporting, but the original status must remain traceable.

A normalized status is an interpretation of the source value, not a replacement for it.

### 8.3 Parser and normalization versions

Material changes to parsing or normalization behavior should be versioned.

Siddhi must be able to distinguish observations produced by different adapter or normalization versions when those differences could affect comparisons or analysis.

## 9. Provenance and snapshot integration

Each successfully captured source observation must be traceable to its origin.

At minimum, the integration layer should supply the information required to record:

- Source system and artifact identity.
- Ingestion run.
- Observation time.
- Source revision, when available.
- Adapter and normalization versions.
- Retrieval status.
- Relevant warnings or limitations.

The persistence layer is responsible for recording the corresponding snapshot and normalized representation.

A source adapter must not decide retention policy or delete earlier snapshots.

Source observations and derived evidence must remain separate. The adapter reports the observation; evidence extraction and assessment workflows decide how that observation is used.

## 10. Read-only access and security

### 10.1 Default access model

Source adapters must use the minimum permissions necessary for their declared capabilities.

Ordinary integration workflows must not:

- Write to external project records.
- Modify OpenSpec artifacts.
- Modify OKF knowledge.
- Commit or alter Git history.
- Change verification results.
- Store credentials in source payloads or ordinary logs.

Any future write capability requires an explicit design and authorization boundary.

### 10.2 Credentials

Credential handling must follow the security model defined in `security-and-privacy.md`.

The integration layer should receive credentials through an approved mechanism and should not expose them to unrelated domain services.

Credential rotation or expiration should not invalidate already captured historical observations, although it may prevent future refreshes.

### 10.3 Local repository access

Local repository access should be constrained to explicitly configured locations and required read operations.

The implementation should avoid unnecessary filesystem traversal and should not follow paths outside the approved scope without an explicit policy.

### 10.4 Remote access

Remote access should use supported read-only API permissions or other approved methods.

Access tokens, private repository metadata, and sensitive content must not be included in normal diagnostic output.

### 10.5 External AI boundary

Source integration itself must not send content to external AI services.

External analysis is a separate workflow that selects and prepares the information to share, applies the applicable data-handling policy, and records the request and result.

This prevents a routine refresh from unexpectedly disclosing source content.

## 11. Errors, retries, and partial results

### 11.1 Error categories

Adapters should distinguish the following categories where practical:

- Configuration error.
- Authentication failure.
- Permission denied.
- Source unavailable.
- Unsupported capability.
- Missing artifact.
- Invalid or unexpected source format.
- Incomplete scan.
- Rate limiting.
- Timeout.
- Transient network or process failure.
- Internal adapter error.

The coordinator may map source-specific errors into shared categories while preserving safe diagnostic details.

### 11.2 Retry behavior

Retries should be limited to failures likely to be transient.

Examples include temporary network failures or rate limiting. Invalid configuration, unsupported operations, and persistent permission failures generally require correction rather than repeated automatic attempts.

Retry policy should consider:

- Operation type.
- Source-specific limits.
- Retry count.
- Delay and backoff.
- Overall execution deadline.
- Whether the operation is safe to repeat.

Repeated retrieval must not create duplicate logical source identities or duplicate observations representing the same capture.

### 11.3 Partial results

If some records are processed successfully and others fail, the adapter must report both outcomes.

Siddhi should preserve successful observations and expose incomplete coverage. It must not mark the entire scope as successfully ingested merely because some records were returned.

### 11.4 Cancellation and timeouts

Long-running source operations should have bounded execution behavior.

Where cancellation is supported, Siddhi should record the cancelled state and preserve successfully completed stages.

A timed-out operation must not be represented as a confirmed empty result.

### 11.5 Schema changes

Unexpected source-format changes should be handled safely.

If the adapter can still retrieve part of the source, it may preserve supported fields while marking the interpretation incomplete. If the change prevents reliable interpretation, the affected records should be rejected or marked unsupported rather than silently misparsed.

## 12. Integration execution model

The initial implementation should use the simplest execution model that satisfies the expected workload.

Short local reads and lightweight normalization may execute synchronously. Longer scans, large repository-history reads, or multi-source refreshes may run as background jobs when needed.

Regardless of execution mode:

- Each operation must have an observable outcome.
- Source-specific failures must remain attributable to the relevant adapter and scope.
- Completed stages must be preserved where safe.
- Retries must be idempotent.
- Concurrency must not silently overwrite newer Siddhi-owned changes.
- Long-running operations must not block unrelated local planning operations unnecessarily.

A modular monolith is sufficient for the initial architecture. Separate worker processes or distributed execution should be introduced only when justified by measured requirements.

## 13. Observability

Every integration operation should produce an operational record sufficient to explain its outcome.

Where applicable, record:

- Source identifier and adapter.
- Operation type and requested scope.
- Start and completion timestamps.
- Outcome and coverage.
- Number of records discovered, processed, skipped, or rejected.
- Retry attempts.
- Relevant schema or parser version.
- Error category and safe diagnostic details.

Observability must support diagnosing source problems without logging credentials or unnecessarily copying sensitive source content.

The user-facing summary should explain whether the source was reachable, whether the requested scope was scanned, and which limitations affect the result.

## 14. Testing strategy

Each adapter must be tested independently of the portfolio domain logic.

### 14.1 Contract tests

Verify that each adapter:

- Reports supported and unsupported capabilities correctly.
- Returns consistent result structures.
- Preserves source identity and observation context.
- Distinguishes empty results from failures.
- Reports partial coverage.
- Produces safe error information.

### 14.2 Source-format tests

Use representative source fixtures to verify:

- Valid input parsing.
- Missing fields.
- Unexpected fields.
- Malformed content.
- Schema and configuration differences.
- Version-specific formats.
- Renamed and relocated artifacts where applicable.

OpenSpec and OKF fixtures must reflect the actual formats and conventions used by Siddhi's target repositories.

### 14.3 Identity tests

Verify that:

- Repeated discovery does not create duplicates.
- Renames do not automatically create new identities when stable identity is preserved.
- Ambiguous matches are not silently merged.
- Missing records are not automatically treated as deleted.
- Changed content can be distinguished from unchanged content.

### 14.4 Failure and recovery tests

Verify:

- Authentication and permission failures.
- Source unavailability.
- Timeouts and rate limiting.
- Partial scan recovery.
- Retry behavior.
- Cancellation.
- Adapter upgrades.
- Persistence failures during ingestion.

### 14.5 Read-only guarantees

Tests should establish that ordinary integration operations do not write to source systems or mutate source repositories.

Where feasible, use read-only credentials and isolated fixtures to reinforce this guarantee.

## 15. Proposed implementation structure

The following is an illustrative package organization for `siddhi-api`. Exact module names should follow the final repository conventions.

```text
src/siddhi_api/
├── integrations/
│   ├── contracts/
│   │   ├── adapter.py
│   │   ├── capabilities.py
│   │   ├── results.py
│   │   └── errors.py
│   ├── coordinator.py
│   ├── registry.py
│   ├── identity/
│   ├── normalization/
│   ├── adapters/
│   │   ├── vyasa/
│   │   ├── openspec/
│   │   ├── okf/
│   │   ├── git/
│   │   └── verification/
│   └── testing/
├── application/
│   ├── discover_sources.py
│   ├── ingest_source.py
│   └── refresh_sources.py
├── domain/
├── infrastructure/
└── ...
```

This layout illustrates responsibilities rather than mandating a particular file decomposition.

The integration layer should depend on source access mechanisms and shared contracts. Portfolio workflows should depend on the integration abstractions, not import source-specific parsing logic directly.

## 16. Implementation sequence

A practical implementation sequence is:

### Phase 1 — Integration foundation

- Define the adapter contract and result types.
- Define source identity and capability representation.
- Establish read-only access rules.
- Implement ingestion run and error reporting.
- Create contract tests and representative fixtures.

### Phase 2 — Project discovery

- Implement the Vyasa adapter against the actual available interface.
- Resolve project identities.
- Persist project references and source observations.
- Report coverage and incomplete scans.

### Phase 3 — Engineering source ingestion

- Implement OpenSpec parsing against actual target repository conventions.
- Implement OKF ingestion against its installed schema and format.
- Add Git history observations using approved read-only access.
- Add verification adapters only for sources available in the first release.

### Phase 4 — Evidence integration

- Connect normalized observations to evidence extraction.
- Preserve source and transformation provenance.
- Support comparison with previous snapshots.
- Expose missing and conflicting information to deterministic analysis.

### Phase 5 — Hardening

- Validate authentication and permission boundaries.
- Test partial failures, schema changes, and recovery.
- Measure performance and storage behavior.
- Confirm that ordinary workflows do not modify source systems.

The order of implementation may change depending on which source interfaces are already available and testable.

## 17. Open questions

| ID | Question | Why it matters |
|---|---|---|
| SI-001 | What interface does Vyasa expose for project inventory, and which fields and scan-status indicators are guaranteed? | Determines the first adapter contract and identity strategy |
| SI-002 | Will Siddhi access Vyasa through a local API, direct database access, exported data, or another supported interface? | Determines coupling, permissions, and deployment assumptions |
| SI-003 | Which exact OpenSpec schemas and artifact formats must the first release support? | Prevents assumptions about repository conventions |
| SI-004 | What is the installed OKF structure and its supported method of reading knowledge artifacts? | Determines the OKF adapter design |
| SI-005 | Should Git access initially support local repositories, remote provider APIs, or both? | Affects credentials, performance, and deployment |
| SI-006 | Which verification system or artifact format is available for the first release? | Prevents building a generic integration without a concrete source |
| SI-007 | What source identity guarantees are available for each integration? | Determines duplicate detection and rename handling |
| SI-008 | What are the expected source sizes, rate limits, and refresh frequency? | Determines pagination, incremental scanning, and background execution |
| SI-009 | Which source payloads need to be retained in full, and which can be represented by metadata and references? | Affects storage, privacy, and historical reproducibility |
| SI-010 | What should happen when a source schema changes and only part of its content can be interpreted? | Defines safe compatibility behavior |
| SI-011 | Which source connections require credentials, and where will those credentials be stored? | Defines the security integration boundary |
| SI-012 | Is remote or unattended scheduled ingestion required in the first usable release? | Affects authentication, scheduling, and operational design |

These questions should be resolved by inspecting the actual source interfaces and installed formats, not by inventing assumptions about them.

Until then, the safe defaults are read-only access, capability-based adapters, explicit coverage reporting, deterministic parsing, preserved provenance, and no automatic source deletion or modification.

## 18. Relationship to other documents

- `vision.md` defines Siddhi's purpose and principles.
- `scope-and-roadmap.md` defines which integrations belong in each delivery phase.
- `system-architecture.md` defines the integration layer's position in the overall application.
- `architectural-decisions.md` records the selected adapter, persistence, and execution decisions.
- `domain-model.md` defines the portfolio concepts that use integrated information.
- `data-ownership.md` defines authority boundaries and permitted source operations.
- `data-model.md` defines persisted source references, snapshots, evidence, and provenance.
- `application-workflows.md` defines the user and system workflows that invoke integrations.
- `scanning-and-evidence.md` defines how source observations become evidence.
- `synchronization.md` defines refresh, change detection, and historical comparison.
- `security-and-privacy.md` defines credentials, access controls, and sensitive-data handling.

This document defines the source integration boundary. Detailed scanning and evidence rules should be specified in `scanning-and-evidence.md`, while refresh semantics and change detection belong in `synchronization.md`.

During the later OpenSpec and OKF preparation stage, testable adapter behavior should become requirements, while reusable integration patterns and technical rationale should become independent engineering knowledge.

---

**End of document**