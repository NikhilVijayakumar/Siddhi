---
type: Technology
title: Vyasa contract direction and uncertainty
description: Intended inventory role with explicitly unverified transport, schema, identity, status, and access guarantees.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Vyasa contract direction and uncertainty

The local integration direction names Vyasa as the project and repository inventory
source. It is an intended authority boundary, not evidence that a specific upstream
tool, endpoint, table, or response contract exists. **No actual Vyasa repository,
interface definition, running service, response fixture, or contract test has been
inspected here.** No real Vyasa compatibility is claimed.

Unlike the locally observed Markdown/frontmatter and YAML artifact-schema direction,
Vyasa's native serialization and access format remain unknown. Describing it as
a workspace intelligence or MCP system does not establish that Siddhi can query
inventory through a particular MCP tool or that an HTTP/API/export interface exists.

# Desired consumer information, not upstream field claims

The consumer would benefit from stable project/repository identities, repository
origins and permitted locations, technology classifications, engineering-artifact
indicators, source scan times, coverage, errors, pagination, and provenance.
These are logical information needs with optional/unavailable values, not an
invented upstream schema. A presence indicator does not establish parsing,
validation, implementation, or successful pipeline execution.

Source scan time differs from the time inventory is retrieved. Read-only retrieval,
requesting a targeted refresh, and initiating workspace discovery are different
capabilities. None of the latter capabilities is assumed to exist.

# Contract inspection questions

| Area | Evidence needed before claiming support |
|---|---|
| Access | Supported transport/deployment and authentication/permission contract |
| Identity | Native ID scope, stability, rename/transfer/clone behavior |
| Shape | Actual fields, optionality, enums, serialization, versioning policy |
| Inventory scope | Filtering, pagination, visibility restrictions, empty-result meaning |
| Discovery quality | Scan timestamps, complete/partial/failed states, field-level basis |
| Refresh | Selected-project reads, targeted rescan, independent scan lifecycle |
| Incremental/history | Cursor guarantees, deletions, historical observations |
| Failure | Safe error categories, rate limits, retries, timeouts, partial records |

The adapter can expose a stable logical result while preserving those source
differences. Unsupported and unavailable are explicit; an empty record list alone
cannot prove there are no projects. There is no basis to choose direct database
coupling, promise fields, or implement a second scanner to hide missing capabilities.

Related: [Vyasa architecture](../architecture/vyasa-integration.md),
[source adapters](../architecture/source-adapters.md), [technology index](index.md).