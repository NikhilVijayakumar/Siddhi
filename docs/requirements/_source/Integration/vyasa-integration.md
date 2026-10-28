# Vyasa Integration

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `vyasa-integration.md`  
**Status:** Draft for review  
**Scope:** Integration between Siddhi and Vyasa, the Workspace Intelligence MCP and project inventory system.

---

## 1. Purpose

Vyasa provides Siddhi with information about discovered projects, repositories, technologies, and available engineering artifacts. Siddhi uses this information to connect projects to strategic goals, assess portfolio coverage, and identify where additional evidence is needed.

This document defines the intended integration contract between the two systems.

It establishes:

- The responsibilities of Vyasa and Siddhi.
- The project information Siddhi needs to consume.
- The expected interface and logical data contract.
- Project identity and source-reference resolution.
- Discovery status, evidence quality, and freshness.
- Read-only access and failure handling.
- Integration testing and acceptance criteria.

The actual Vyasa interface, schema, and response formats must be inspected before implementation. The structures in this document are proposed logical contracts, not claims about existing Vyasa endpoints or database fields.

## 2. Integration principles

### 2.1 Vyasa remains the project inventory authority

Vyasa owns its project inventory and the discovery metadata it maintains.

Siddhi consumes that information but does not become the authoritative owner of Vyasa's project records.

### 2.2 Siddhi owns portfolio intent

Vyasa does not need to understand Siddhi's goals, intended outcomes, priorities, plans, or strategic decisions.

Siddhi maintains those records and creates explicit relationships between them and projects discovered by Vyasa.

### 2.3 Do not duplicate project discovery

Siddhi should reuse Vyasa's available inventory and discovery results instead of building a second independent project scanner.

If Siddhi requires deeper evidence than Vyasa provides, that should be a separately scoped integration with a clearly defined purpose.

### 2.4 Distinguish discovery from verification

Vyasa may report that a repository contains a README, OpenSpec configuration, OKF knowledge, a programming language, a framework, or CI/CD configuration.

Such a report establishes what Vyasa observed or classified, not necessarily that the documentation is complete, the framework is correctly identified, the pipeline works, or the project meets a goal.

Siddhi must preserve this distinction.

### 2.5 Read-only by default

The initial integration must not modify Vyasa-owned project records or trigger source repository changes.

Any future write-back capability must be designed and authorized separately.

### 2.6 Unknown is not equivalent to absent

If Vyasa cannot inspect a repository or cannot determine whether a capability exists, Siddhi must represent the result as unknown or unverified rather than as a confirmed absence.

---

## 3. Responsibilities and boundaries

| Responsibility | Vyasa | Siddhi |
|---|---|---|
| Discover projects and repositories | Owns discovery within its scope | Consumes discovery results |
| Maintain project inventory | Owns inventory records | Maintains a local reference and observation history |
| Identify repository origins | Reports discovered or configured origins | Preserves source provenance and flags discrepancies |
| Detect documentation and engineering artifacts | Reports findings within its scanning capabilities | Uses findings as inputs to portfolio analysis |
| Identify technologies and frameworks | Reports declared or inferred metadata | Interprets the metadata in goal context |
| Report discovery status and limitations | Reports what it can establish | Preserves coverage and freshness information |
| Define goals and intended outcomes | Outside Vyasa's portfolio scope | Owns |
| Link projects to goals and initiatives | Does not need to own these relationships | Owns |
| Assess goal progress | Does not make Siddhi's strategic assessment | Owns assessment and reporting |
| Approve portfolio priorities and decisions | Outside Vyasa's portfolio authority | Owns |
| Modify source repository content | Not part of Siddhi integration | Must not be triggered by ordinary integration |

These responsibilities describe the intended boundary. Existing Vyasa behavior must be verified before deciding which capabilities can be reused directly.

## 4. Integration architecture

The proposed integration flow is:

<box border radius="lg" padding={3} gap={2} align="center">
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **Vyasa**

    <text size="sm" textAlign="center">Project discovery · Repository inventory · Discovery metadata</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box border radius="md" padding={3} width="100%" align="center">
    **Vyasa integration adapter**

    <text size="sm" textAlign="center">Connection · Capability checks · Read-only retrieval · Contract validation</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box background="surface-secondary" radius="md" padding={3} width="100%" align="center">
    **Siddhi project-reference and observation layer**

    <text size="sm" textAlign="center">Identity mapping · Normalization · Provenance · Snapshot history</text>
  </box>
  <icon name="arrow-down" size="lg" />
  <box border radius="md" padding={3} width="100%" align="center">
    **Siddhi portfolio workflows**

    <text size="sm" textAlign="center">Goal linking · Evidence assessment · Reports · Historical comparisons</text>
  </box>
</box>

The adapter isolates Vyasa-specific behavior from Siddhi's domain logic.

The initial implementation should use the simplest supported communication method that fits the actual Vyasa deployment. Options may include a local API, a supported MCP interface, a structured export, or another existing contract. Direct database access should not be assumed.

## 5. Integration scope

### 5.1 Required capabilities

The first usable integration should aim to support:

1. Determine whether Vyasa can be reached through the configured interface.
2. Retrieve project inventory within an explicitly defined scope.
3. Retrieve stable project identifiers where available.
4. Retrieve repository origins and available location metadata.
5. Retrieve declared or discovered technology metadata.
6. Retrieve available documentation and engineering-artifact indicators.
7. Retrieve discovery timestamps and scan-status information where exposed.
8. Distinguish complete results from partial, stale, or failed discovery.
9. Resolve project identities across successive refreshes.
10. Preserve observations and detect changes between refreshes.

The implementation must validate which of these capabilities already exist in Vyasa and which require an extension to its interface.

### 5.2 Optional capabilities

The following may be useful later but should not be prerequisites for basic integration:

- Requesting a targeted rescan of one project.
- Reading detailed scan evidence for individual fields.
- Reading historical discovery results from Vyasa.
- Receiving incremental change notifications.
- Querying projects by technology or artifact availability.
- Triggering an authorized discovery operation through Vyasa.

These capabilities should be added only when the existing interface and user workflow justify them.

### 5.3 Out of scope

The initial integration must not:

- Replace Vyasa's discovery or scanning logic.
- Independently clone all repositories to reconstruct Vyasa's inventory.
- Change project metadata in Vyasa.
- Change OpenSpec requirements or task statuses.
- Change OKF knowledge records.
- Modify Git repositories.
- Infer strategic priority from repository metadata alone.
- Treat a repository's existence as evidence that its associated goal has been achieved.

---

## 6. Project information required by Siddhi

Siddhi needs enough project information to identify a project, understand the available engineering context, and decide which further observations may be relevant.

The following is a proposed logical information contract.

| Information group | Fields or concepts | Purpose |
|---|---|---|
| Project identity | Stable project ID, display name, project type if available | Link observations to the same project |
| Repository identity | Repository ID or stable origin, repository type, origin URL | Identify the associated source repository |
| Repository location | Local location if exposed and permitted, remote locator | Understand how the repository may be accessed |
| Technology | Languages, frameworks, runtimes, relevant tooling | Provide portfolio context |
| Documentation | README and other documentation indicators | Identify available documentation evidence |
| OpenSpec | Presence, discovered configuration or schema metadata, artifact indicators | Identify available requirements evidence |
| OKF | Presence, format or schema metadata, knowledge artifact indicators | Identify available engineering knowledge |
| CI/CD | Presence and available pipeline metadata | Identify potential delivery-process evidence |
| Discovery | Scan time, scan status, coverage, errors or limitations | Interpret freshness and completeness |
| Provenance | Source identifier, field origin, declared versus inferred status where available | Preserve confidence and traceability |

Not every field must be present. The contract should explicitly support optional or unavailable values.

### 6.1 Repository origins and local locations

A repository's remote origin and its local clone location are different attributes.

Siddhi should preserve that distinction.

- A remote origin helps identify a repository across machines and workspaces.
- A local location describes where a particular environment has a working copy.
- A missing local location does not mean that the repository does not exist.
- A local location should be consumed only if the configured Vyasa interface exposes it and its use is permitted.

If the same repository is cloned into multiple local locations, Siddhi should not automatically treat each clone as a separate strategic project.

### 6.2 Technology metadata

Technology information should retain its source classification where available.

For example:

- A language declared by a project owner.
- A language inferred from repository files.
- A framework detected from a manifest.
- A framework inferred from dependency patterns.
- An unknown technology classification.

These observations may have different reliability. Siddhi should not flatten them into a single unqualified claim.

### 6.3 OpenSpec and OKF indicators

Siddhi should distinguish at least the following concepts where Vyasa supplies enough information:

- Whether relevant files or directories were discovered.
- Whether a recognizable configuration or schema was found.
- Whether artifacts were successfully parsed.
- Whether the scan was complete.
- Whether the artifact content has been validated.

These are separate questions. Finding a directory does not prove that the corresponding workflow is configured correctly or that the artifacts are complete.

### 6.4 CI/CD indicators

A CI/CD indicator should describe what Vyasa actually discovered.

For example, a pipeline configuration file may indicate that CI/CD configuration is present. It does not prove that the pipeline runs successfully or that the project has a working release process.

If Vyasa reports only presence or absence, Siddhi must not invent pipeline execution status.

---

## 7. Logical integration contract

The adapter should expose a stable Siddhi-facing contract regardless of the underlying Vyasa transport.

The following examples describe the logical shape of the data, not the exact fields or serialization used by Vyasa.

### 7.1 Project inventory result

A project inventory result should provide:

- The requested discovery scope.
- The project records returned.
- The observation time or source scan time, where available.
- The completeness or status of the result.
- Any continuation token or pagination information.
- Relevant warnings and errors.

The contract must distinguish:

- A successful scan that found no projects.
- A successful scan that found projects.
- A partial scan.
- A failed scan.
- A scan that has not been performed or whose status is unknown.

An empty list without an accompanying success or coverage indication is not sufficient evidence that no projects exist.

### 7.2 Project record

A normalized project record should expose, where available:

- External project identifier.
- Display name.
- Project metadata.
- Associated repository references.
- Discovery metadata.
- Source classification and provenance.
- Last-observed information.

Source-native fields should be retained or traceable when normalization could otherwise lose their meaning.

### 7.3 Repository record

A normalized repository record should expose, where available:

- External repository identifier.
- Remote origin.
- Local location.
- Repository provider or type.
- Relevant source metadata.
- Last-observed information.

A repository may be associated with a project through an explicit relationship rather than being identified solely by the project name.

### 7.4 Capability and status result

The integration should distinguish the following dimensions.

| Dimension | Example values |
|---|---|
| Connection | Available, unavailable, unverified |
| Capability | Supported, unsupported, temporarily unavailable |
| Scan execution | Succeeded, partially succeeded, failed, cancelled |
| Coverage | Complete, partial, unknown |
| Field observation | Observed, inferred, unavailable, conflicting |
| Freshness | Current under policy, stale, unknown |

These are conceptual classifications. The implementation should reuse existing Vyasa status values where appropriate and normalize them without discarding their original meaning.

---

## 8. Identity resolution and deduplication

### 8.1 Preferred identity strategy

Siddhi should use Vyasa's stable project identifier where one is available and reliable.

For repositories, it should use a stable repository identity or a documented origin-based strategy, depending on what Vyasa exposes.

Display names and local paths must not be treated as permanent identities by default.

### 8.2 Duplicate detection

When a project is encountered in a later inventory result, Siddhi should attempt to resolve it to the existing project reference.

The identity-resolution process should consider:

1. Stable source identifiers.
2. Stable repository identifiers.
3. Canonical repository origins where applicable.
4. Additional source metadata as supporting evidence.

Name similarity alone must not be enough to merge records automatically.

### 8.3 Ambiguous identities

If a project cannot be matched confidently, Siddhi should record the unresolved identity or candidate matches.

The system should avoid creating irreversible associations based on uncertain matching.

Where a human decision is needed, the user should be able to resolve the ambiguity without altering the authoritative Vyasa records.

### 8.4 Renames and repository movement

When a project name, repository origin, or local path changes, Siddhi should preserve the previous observation and record the new value.

It should distinguish, where evidence allows:

- A project rename.
- A repository relocation.
- A changed local clone path.
- A different repository.
- An unresolved identity change.

The exact interpretation may depend on Vyasa's identity guarantees.

---

## 9. Refresh and historical observations

Siddhi should maintain its own observation history even if Vyasa also keeps historical discovery data.

A refresh should:

1. Record the requested scope and start time.
2. Read the available Vyasa inventory.
3. Validate the response.
4. Resolve project and repository identities.
5. Record the source observation and its freshness.
6. Compare the new result with previous Siddhi observations.
7. Record detected changes and unresolved differences.
8. Report coverage and errors.
9. Mark the refresh complete, partially complete, or failed.

### 9.1 Do not assume deletion

A project missing from the latest result must not automatically be marked deleted.

The project may have been excluded from the scan, inaccessible, filtered, moved, or omitted because of an error.

Siddhi should record the latest observation and distinguish confirmed deletion from an unresolved absence when Vyasa provides sufficient evidence.

### 9.2 Avoid redundant scanning

Siddhi should not routinely request an expensive rescan if Vyasa already has sufficiently recent and relevant discovery results.

If Siddhi needs fresher information, it should use a supported targeted refresh capability where available. If no such capability exists, the user should be informed of the limitation rather than having Siddhi silently implement a duplicate scanner.

### 9.3 Historical reproducibility

A portfolio report should be able to identify which Vyasa observation informed it.

The report must not silently replace its historical project context when a later refresh changes the inventory.

---

## 10. Integration workflow

### WF-VY-001 — Connect to Vyasa

**Trigger:** First-time configuration or a request to validate the connection.

1. Siddhi loads the configured Vyasa connection details.
2. The adapter validates the configuration.
3. It checks the availability of the supported interface.
4. It determines the available capabilities.
5. Siddhi records the result and any limitations.
6. The user receives a clear connection and capability summary.

A successful connection test must not trigger a full inventory scan unless the operation explicitly requests one.

### WF-VY-002 — Discover projects

**Trigger:** The user requests project discovery or an approved refresh workflow invokes it.

1. Siddhi requests the project inventory within the configured scope.
2. Vyasa returns the available records and discovery status.
3. Siddhi validates the result and checks whether coverage is complete.
4. Project and repository identities are resolved.
5. New project references are created where appropriate.
6. Existing references receive new observations.
7. Siddhi compares the new inventory with previous observations.
8. The user receives a discovery summary.

### WF-VY-003 — Refresh a selected project

**Trigger:** The user requests a refresh for a particular project or Siddhi identifies a relevant need for fresher data.

1. Siddhi resolves the project to its Vyasa identity.
2. It checks whether Vyasa supports targeted retrieval or refresh.
3. It obtains the latest available project and repository information.
4. It records the observation time, status, and coverage.
5. It identifies changes and limitations.
6. It updates Siddhi's normalized view without rewriting the historical observation.
7. It makes the new information available to relevant analysis workflows.

If targeted refresh is unsupported, Siddhi may use a broader supported inventory read or explain why the refresh cannot be performed.

### WF-VY-004 — Use project metadata in a portfolio assessment

**Trigger:** An assessment requires project information from Vyasa.

1. Siddhi resolves the relevant goal and project references.
2. It identifies the most appropriate available Vyasa observations.
3. It checks their freshness and known coverage.
4. It supplies the observations and provenance to the deterministic analysis workflow.
5. The assessment evaluates their relevance to the goal.
6. Siddhi records the resulting findings separately from the source observations.

Vyasa's metadata is input to the assessment, not a strategic conclusion in itself.

---

## 11. Error handling and recovery

The adapter should classify integration failures wherever practical.

| Failure | Expected behavior |
|---|---|
| Vyasa unavailable | Preserve prior observations and report that current data could not be retrieved |
| Invalid connection configuration | Report the configuration issue without starting discovery |
| Authentication or permission failure | Report the access problem without exposing credentials |
| Unsupported capability | Explain that the requested operation is not available |
| Partial inventory response | Preserve successful records and mark coverage as partial |
| Invalid project record | Isolate the affected record where possible and report the parsing issue |
| Duplicate or ambiguous identity | Preserve ambiguity rather than silently merge |
| Missing project in latest scan | Record the absence without assuming deletion |
| Unexpected response format | Fail safely or preserve supported fields with an explicit limitation |
| Siddhi persistence failure | Report the failed operation and use a recovery strategy that avoids duplicate records |

Retries should be limited to appropriate transient failures.

A retry must not duplicate project identities, overwrite historical observations, or modify Vyasa records.

A failed refresh must not make a previously successful observation appear newly verified.

---

## 12. Security and access control

The initial integration should use the minimum access required to read Vyasa's supported project information.

The implementation must:

- Use the configured connection and authentication mechanism.
- Avoid storing credentials in ordinary source metadata.
- Avoid exposing secrets in logs or errors.
- Respect any permissions enforced by Vyasa.
- Limit the scope of retrieved information to Siddhi's declared purpose.
- Avoid sending source information to external AI services through the integration adapter.
- Record access failures and relevant limitations without exposing sensitive content.

If Vyasa provides different visibility levels for different projects, Siddhi must not assume that an incomplete inventory represents the complete workspace.

The integration must also avoid granting Siddhi implicit permission to modify Vyasa-owned records.

---

## 13. Testing and acceptance criteria

The integration is ready for initial use when the following criteria are satisfied.

### Contract and connection

- [ ] Siddhi can validate the configured Vyasa interface.
- [ ] The adapter identifies supported capabilities without assuming unsupported operations.
- [ ] Connection failures are distinguishable from successful empty results.
- [ ] Source-specific response formats are isolated behind the adapter.

### Identity and inventory

- [ ] Siddhi can retrieve the available project inventory.
- [ ] Project references use stable source identities where available.
- [ ] Repeated discovery does not create duplicate logical projects.
- [ ] Ambiguous project identities are not silently merged.
- [ ] Project and repository identity are distinguishable where needed.

### Metadata and provenance

- [ ] Available repository origins and metadata are preserved.
- [ ] Technology and artifact indicators retain their source classification where available.
- [ ] Scan timestamps, status, and coverage limitations are preserved where exposed.
- [ ] A source observation can be traced to the corresponding Siddhi ingestion record.
- [ ] Missing or unsupported fields are not represented as confirmed absence.

### Refresh and failure handling

- [ ] Siddhi can compare a new observation with an earlier one.
- [ ] Partial scans are represented as partial.
- [ ] A missing project is not automatically treated as deleted.
- [ ] Failed refreshes do not erase earlier successful observations.
- [ ] Retry operations do not create duplicate project references.

### Ownership and security

- [ ] Ordinary integration operations do not modify Vyasa records.
- [ ] The adapter does not initiate repository checkout or mutation as a side effect.
- [ ] Credentials are not exposed in logs or error messages.
- [ ] Integration failures are visible to the user.
- [ ] No source content is sent to external AI services by the adapter.

---

## 14. Implementation sequence

### Phase 1 — Inspect the existing Vyasa interface

Confirm:

- The supported connection mechanism.
- The available project and repository fields.
- Stable identity guarantees.
- Discovery timestamps and status information.
- Available filtering, pagination, and refresh capabilities.
- Authentication and permission behavior.
- Existing response schemas and error semantics.

The actual interface and schema should be treated as implementation evidence. Siddhi should not introduce a second competing contract without a clear reason.

### Phase 2 — Implement the Siddhi adapter

- Define the Siddhi-facing integration contract.
- Implement connection validation and capability reporting.
- Retrieve and validate project inventory.
- Normalize project and repository identities.
- Preserve source provenance and observation metadata.
- Add contract tests.

### Phase 3 — Integrate with Siddhi persistence

- Persist project references and source observations.
- Implement identity resolution and duplicate prevention.
- Compare successive observations.
- Report changes, incomplete coverage, and errors.
- Verify that failed ingestion does not damage historical data.

### Phase 4 — Connect portfolio workflows

- Allow users to link projects directly to goals.
- Make Vyasa observations available to deterministic assessments.
- Show source freshness and uncertainty in reports.
- Refresh relevant observations when needed.
- Ensure that portfolio analysis does not alter Vyasa-owned information.

### Phase 5 — Harden and validate

- Test large inventories and partial responses.
- Validate permissions and read-only guarantees.
- Test adapter compatibility with actual Vyasa versions.
- Measure refresh performance.
- Document known limitations and supported capabilities.

---

## 15. Open questions

| ID | Question | Why it matters |
|---|---|---|
| VY-001 | What interface does Vyasa currently expose for project inventory? | Determines how Siddhi should connect |
| VY-002 | Does Vyasa expose stable project and repository identifiers? | Determines reliable identity resolution |
| VY-003 | Which fields are available for repository origin, local location, technology, documentation, OpenSpec, OKF, and CI/CD? | Determines the initial data contract |
| VY-004 | Does Vyasa expose scan timestamps, completeness, errors, and per-field provenance? | Determines how Siddhi can evaluate freshness and reliability |
| VY-005 | Can Siddhi retrieve a selected project without requesting the entire inventory? | Determines targeted refresh behavior |
| VY-006 | Can Siddhi request a refresh through Vyasa, or does Vyasa refresh independently? | Avoids duplicating discovery work |
| VY-007 | How does Vyasa represent declared, inferred, unknown, and unverified metadata? | Prevents loss of important distinctions |
| VY-008 | How are access restrictions and private repository failures represented? | Prevents inaccessible projects from being misclassified |
| VY-009 | Does Vyasa retain historical observations, or must Siddhi preserve all history it needs? | Determines snapshot responsibilities |
| VY-010 | Which transport and authentication mechanism is intended for Siddhi's first release? | Determines the concrete adapter implementation |

These questions should be resolved by examining the actual Vyasa repository, configuration, interface definitions, and tests.

Until that inspection is complete, the proposed contract should remain logical rather than being treated as a final API specification.

## 16. Relationship to other Siddhi documents

- `source-integration.md` defines the general source adapter architecture.
- `data-ownership.md` defines Vyasa's authority over project inventory.
- `data-model.md` defines project references, snapshots, and provenance.
- `application-workflows.md` defines the user workflows that invoke project discovery and refresh.
- `scanning-and-evidence.md` defines how observations become evidence.
- `synchronization.md` defines refresh and historical comparison behavior.
- `security-and-privacy.md` defines access and sensitive-data handling.
- `functional-requirements.md` defines the required observable behavior.
- `architectural-decisions.md` records the final interface and integration choices.

The later OpenSpec conversion should capture testable integration behavior and failure-handling rules. OKF should independently document the reusable integration architecture and its technical rationale.

---

**End of document**