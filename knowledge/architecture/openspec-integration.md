---
type: Architecture
title: OpenSpec evidence integration
description: Schema-aware read-only observation of an ingested project's declarations, artifacts, progress, and archive with provenance and compatibility limits.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# OpenSpec evidence integration

An ingested project's OpenSpec store owns its source-authored behavioral declarations,
scenarios, change artifacts, and recorded workflow state. Siddhi observes those
records and owns its portfolio mappings and assessments. This source-ownership
boundary describes a project being ingested, not the process used to develop Siddhi.
The ingested project's workflow is interpreted on its own terms; it is not replaced
by Siddhi's own development conventions.

OpenSpec declarations and independent engineering knowledge can each exist without
the other. Missing cross-links are not automatically defects. A scenario in a
document is not an executed scenario; a checked task is declared progress, not
proof of correct behavior. Structural validation, implementation evidence, tests,
deployment, and outcome assessment are separate layers.

# Schema-aware discovery

The adapter separates root/configuration discovery, effective schema resolution,
artifact retrieval, parsing, normalization, and evidence interpretation. A source
context identifies project, accessible root, configuration fingerprint, effective
schema name/source/version when known, parser/adapter versions, observation time,
scan coverage, and validation diagnostics. Existence and successful interpretation
are different properties.

Discover maintained declarations, active and archived artifact sets, project-local
schema definitions, task-tracking conventions, and available configuration. The
effective schema can depend on project, user-level, or packaged resolution. Machine
settings are not repository-owned facts; any dependence on them needs explicit
capture rather than an accidental dependency on the operator's environment.

Schema metadata can describe artifact IDs, generated locations, dependencies,
templates, and task tracking. Unknown schema resolution is not permission to assume
a default. Retain safely discoverable artifact references and label unsupported
semantic interpretation. Custom artifact sets do not need to be forced into one
global taxonomy merely to remain discoverable.

# Logical records and relationships

| Record | Useful identity/context | Meaning and limit |
|---|---|---|
| Project context | Project/root, configuration/schema, scan context | Describes the interpretation environment |
| Maintained declaration document | Source identifier/path, revision/fingerprint | Container, not implementation status |
| Behavioral declaration | Native ID or scoped structural identity, unchanged text | Source-authored intent |
| Scenario | Parent declaration, native ID/location, text, revision | Expected behavior, not execution |
| Change set | Project/change ID, locator, schema, observed state | A source-authored proposal or recorded evolution |
| Change artifact | Parent, type from schema, locator, fingerprint, parse state | Custom kinds can remain uninterpreted |
| Task observation | Change/artifact, task ID/location, text, marker, revision | Declared completion only |
| Archive observation | Change identity, archive locator/time, available metadata | Workflow event, not verified outcome |

These are logical entities rather than a physical storage schema. Preserve parent
and delta relationships instead of flattening everything to one progress status.
Portfolio-to-source mappings belong to Siddhi and can be many-to-many; relevance
does not establish achievement.

# Identity, deltas, and status interpretation

Use stable native identifiers within their documented scope. Otherwise use a
documented composite based on source container and structural location, with
ambiguity retained. Similar text alone is insufficient to merge distinct items.
Movement, modification, removal, addition, and unresolved matching are different
comparison results. Source text remains attributable, not silently rewritten.

Custom lifecycle statuses retain their native value. Presence in a maintained
document does not imply completion. Artifact readiness may be source-reported,
derived by Siddhi, or unresolved; retain which basis produced it. A delta can
declare addition, modification, or removal, but unsupported delta syntax does not
establish that an update was applied. Archive status does not establish that every
declared behavior was implemented or that a goal succeeded.

# File and CLI observation methods

A supported CLI can resolve schema and status semantics; direct read-only access
can retain exact text, locators, and fingerprints. A hybrid can provide both but
needs a consistent revision context. If the source changes between reads, record
the inconsistency or safely retry instead of presenting unrelated observations as
one immutable revision.

CLI use needs known availability/version, supported machine-readable output,
separate exit status and diagnostics, bounded execution, controlled arguments,
and a checked non-mutating operation. Successful process exit does not prove full
coverage. File access respects discovered roots, permissions, path containment,
unreadable content, and malformed artifacts. No source-provided command or template
is executed merely because it was encountered.

Validation outcomes distinguish not run, succeeded, issues found, unable to run,
and unknown. Structural validation concerns a particular revision and scope; it
does not verify implementation. The actual non-mutating behavior of a proposed
validation command needs checking before automation.

# Provenance and failure model

Material observations retain project/root, artifact identity and location,
source revision or fingerprint, observation time, configuration/schema context,
adapter/parser versions, relevant CLI version, access/parse status, and limitations.
Parser changes can reinterpret the same content without a source change. Historical
analysis continues to point to its original observations subject to explicit retention.

| Condition | Safe interpretation |
|---|---|
| No store found after sufficient scoped inspection | Scoped discovery absence |
| Inaccessible repository or partial enumeration | Unknown current coverage; keep prior observations |
| Invalid configuration or unresolved schema | Diagnostic, not authoritative default fallback |
| Unknown artifact kind | Identifiable reference, unsupported semantics |
| Malformed individual artifact | Isolated parse failure where consistency permits |
| Missing/incompatible CLI | Approved alternative or explicit compatibility limitation |
| Source changes mid-read | Inconsistent context, qualified result or bounded retry |
| Persistence failure | Not a successful ingestion or publication |

Retries reconcile identities and capture keys; they do not duplicate logical
records or erase earlier history. Ordinary ingestion does not author artifacts,
change task markers, archive work, edit configuration/templates, alter Git history,
or disclose source content externally. Future write-back is a separate capability.

# Compatibility and validation strategy

Fixtures need standard and project-specific schemas, custom artifacts, unknown
versions, malformed metadata, no artifacts despite configuration, unavailable
roots, and partial scans. Identity movement, changed scenarios, task status,
active/archive distinctions, supported/unsupported deltas, and split CLI/file
revision contexts are key cases. Before/after source comparisons help expose mutations.

Local format inspection establishes a useful configuration/schema direction, not
universal compatibility; see [OpenSpec format direction](../technologies/openspec-format-direction.md).
Still open: exact supported versions and schemas, per-operation CLI/file strategy,
fallback identity rules, default archive depth, validation automation, revision
strategy, custom artifact presentation, full-content retention, and mapping policy.

Related: [source adapters](source-adapters.md), [Git evidence](git-evidence.md),
[OKF integration](okf-integration.md), [ingestion](ingestion-and-snapshots.md).