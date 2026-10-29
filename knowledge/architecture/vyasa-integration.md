---
type: Architecture
title: Vyasa inventory integration
description: Proposed inventory consumption boundary, logical project observations, identity reconciliation, freshness, and upstream contract uncertainty.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Vyasa inventory integration

Vyasa is the intended inventory authority for discovered projects and repositories.
Siddhi consumes that inventory and owns portfolio intent, goal relationships,
assessments, and decisions. Reusing an inventory avoids building a second project
scanner merely to discover the same repositories. Deeper evidence collection is
a separately scoped source capability, not a hidden side effect of inventory access.

The Vyasa interface available on this machine was inspected read-only on 2026-10-29:
a local MCP server over stdio, exposing read-only tools backed by a local index. That
observation covers one deployment and one index version, not a compatibility
commitment for other deployments. See
[Vyasa contract direction](../technologies/vyasa-contract-direction.md).

# Adapter and transport choices

The flow is inventory source → access/capability adapter → project references and
observations → portfolio interpretation. Source-specific transport and validation
stay inside the adapter. A supported local API, MCP interface, structured export,
or other existing contract may be suitable; direct database access is not assumed.
Transport selection depends on the real deployment and supported compatibility boundary.

Connection validation is a bounded access/capability check, not an instruction to
rescan a workspace. Inventory reading, selected-project retrieval, and triggering
an upstream rescan are separate capabilities. Targeted rescans, history queries,
incremental notifications, detailed field evidence, and filtering are possible
extensions only if the real source exposes them and their cost is authorized.

# Observed Vyasa MCP surface

The interface inspected on 2026-10-29 is a stdio MCP server whose tools are
read-only and answer from an existing local index without scanning. Inventory
access uses three tools:

| Tool | Answer |
|---|---|
| `search_projects` | One page of project summaries, with filters and an opaque cursor |
| `get_project` | One project's identity and aliases, checkouts, remote, languages, markers, frameworks |
| `get_index_status` | Freshness, the latest scan run, and counts by project state |

Each answer is JSON carried as tool-result text with `schema_version` `"1"` and a
`data` object; inventory answers also carry `meta` with `generated_at`,
`index_version`, and `freshness` (`current`, `stale`, `partial`, `unknown`).
Failure is a tool result with `isError: true` and a JSON `error` object carrying
`code` and `message`; the codes seen are `unavailable` (no index) and
`internal_error`. Every observed tool is annotated read-only and never rescans.

A project summary carries `project_id` (32 hexadecimal characters), `display_name`,
`state` (`active`, `missing`, `inaccessible`), `identity_status` (`resolved`,
`provisional`, `ambiguous`), `providers`, `has_open_candidates`, `matched`, and
`languages`; a page carries `limit`, `next_cursor`, and `has_more`. `get_project`
adds aliases, checkouts with their remote status, and per-group `status` plus
`observed_at`. `get_index_status` reports the latest scan run with `status`,
`finished_at`, and counts, plus project counts by state.

A `missing` or `inaccessible` project state is a source claim about a known
project, not evidence that the project was deleted. Deletion can only be
established from a complete observation whose scope includes the project.

# Logical information groups

| Group | Desired information where available | Interpretation |
|---|---|---|
| Project | Native ID, name, optional type, repository associations | A strategic project need not equal one checkout |
| Repository | Native ID or stable origin, provider/type | Origin and local location are different attributes |
| Location | Remote locator, permitted local location | No local path does not mean no repository |
| Technology | Languages, frameworks, runtimes, tools | Retain declared versus inferred classification |
| Documentation | README and other artifact indicators | Presence is not completeness or correctness |
| OpenSpec/OKF | Presence, configuration/format indicators, parse context | Discovery, parsing, and validation are separate |
| CI/CD | Configuration presence and available metadata | A pipeline file is not a passing execution |
| Discovery | Scan time, scope, status, coverage, errors | Missing guarantees remain explicit unknowns |
| Provenance | Field origin, source classification, observation context | Do not flatten claims of different reliability |

Optional values are necessary because this is not a claim that Vyasa supplies
every group. Retain source-native fields or traceable references when normalization
would otherwise lose meaning. Multiple local clones of one origin are not
automatically distinct portfolio projects; one project may also reference several
repositories through explicit relationships.

# Inventory result semantics

An inventory result logically couples records with requested scope, source scan
time if exposed, Siddhi observation time, continuation information, completeness,
warnings, and errors. A successful empty scope, successful nonempty scope, partial
scan, failure, and unperformed or unknown scan are different observations. An empty
list without execution and coverage context cannot prove that no projects exist.

Keep these dimensions independent:

- Connection: available, unavailable, unverified.
- Capability: supported, unsupported, temporarily unavailable.
- Execution: succeeded, partial, failed, cancelled.
- Coverage: complete, partial, unknown.
- Field basis: observed, inferred, unavailable, conflicting.
- Freshness: current under an explicit policy, stale, unknown.

These are explanatory categories, not finalized enumerations. Preserve native
status and its meaning alongside any normalized classification.

# Identity and reconciliation

Prefer a reliable source-scoped project identifier and repository identifier.
Where unavailable, a documented origin-based strategy may support reconciliation;
its handling of origin aliases, transfers, and mirrors needs confirmation.
Display names, local paths, and name similarity do not establish stable identity.

Resolve in order of reliable native IDs, reliable repository IDs, documented
canonical origins, and supporting metadata. Retain unresolved candidates when
those signals disagree. Human reconciliation can adjust Siddhi's mapping without
changing Vyasa's authoritative inventory. Renames, repository movement, changed
local clone paths, genuinely different repositories, and uncertain changes are
different cases; preserve earlier values and the basis of any identity match.

# Refresh and history

A refresh captures scope and run identity, retrieves and validates available
inventory, reconciles identities, stores provenance and freshness, compares with
prior applicable observations, and records changes and limitations. A selected
project refresh first checks whether targeted retrieval is supported; broader
inventory reads or an explicit limitation are safer than inventing a second scanner.

Reuse sufficiently relevant upstream observations rather than routinely requesting
expensive rescans. Source scan time is not the time Siddhi read the result. A new
read of stale inventory does not make the underlying inventory current.

A project missing from a refresh may be filtered, inaccessible, moved, or omitted
by failure. Confirmed deletion needs adequate source semantics and scope. Historical
reports identify their inventory observation; later refreshes do not silently
replace their context. Siddhi's retained observation history remains a separate
concern even if Vyasa eventually exposes upstream history.

# Failure, security, and diagnostics

Unavailability retains prior observations with failed-refresh context. Invalid
configuration stops access early; authentication and permission errors expose no
secrets. Unsupported capabilities remain explicit. Isolate invalid records where
safe, retain good observations from partial results, and preserve ambiguous
identities rather than merging them. Unexpected formats can be rejected or partially
interpreted only with stated limitations. Persistence failure is not ingestion success.

Bound retries to transient failures and reconcile committed state to avoid duplicate
projects or observations. Failed refreshes do not erase history or newly verify
old observations. Ordinary access neither changes Vyasa records nor checks out or
mutates repositories. Project visibility limits qualify the apparent workspace
inventory. Credentials are separate secrets, and inventory access does not authorize
external AI disclosure.

# Validation and unresolved contract

Representative real-source fixtures are needed for capabilities, complete/partial
and empty/failed results, identity and origin behavior, optional metadata, unknown
fields, and field provenance. Repeat, rename, relocation, access restriction,
format-change, persistence, and recovery cases are especially important. One
inspected deployment and one index version are not a compatibility guarantee.

The observed surface leaves these contract questions open: authentication and
permission behavior beyond a local stdio process; the protocol version and
`schema_version` change policy; cursor stability guarantees; the meaning of
per-checkout `status` and `observed_at` during partial or interrupted scans;
targeted rescans and upstream history; and how a project keeps identity across
renames, transfers, and clone moves. No human acceptance or general Vyasa
compatibility is asserted by this draft.

Related: [source adapters](source-adapters.md),
[ingestion and snapshots](ingestion-and-snapshots.md),
[evidence semantics](../concepts/evidence-semantics.md).