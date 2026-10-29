---
type: Decision
title: Vyasa MCP inventory interface
description: Use the local read-only Vyasa MCP tools as the first project inventory interface, keeping inventory access behind a replaceable adapter.
status: draft
generated: { by: Big Pickle/opencode, at: 2026-10-29T00:00:00Z }
---

# Context

Vyasa is the intended authority for discovered projects and repositories. The
integration direction did not fix a transport: a structured export, a service API, an
MCP interface, or direct index access were all open. One local Vyasa deployment was
inspected read-only on 2026-10-29 and exposes an MCP server over stdio with read-only
inventory tools and no export command. Siddhi needs an inventory interface now to
attach portfolio intent to real projects without becoming a second scanner.

# Decision

Proposed: the first supported Vyasa interface is its local MCP server over stdio,
using only the read-only project inventory tools. Access stays behind an application
port and is replaceable; nothing outside the adapter depends on the MCP transport,
the answer envelope, or the source's vocabulary. Inventory reads never trigger a
Vyasa scan, and neither direct index coupling nor a structured-export interface is
adopted.

# Alternatives considered

- A structured export file would be simpler to test but no export interface exists,
  and inventing one would make Siddhi responsible for a format Vyasa does not own.
- Reading Vyasa's index directly would couple Siddhi to an internal storage schema
  that the source has not offered as a contract, and would bypass its read-only
  semantics.
- Building a second scanner would duplicate the authority Siddhi intends to consume.
- The official MCP client library would remove hand-written protocol code but adds a
  dependency for a newline-delimited JSON exchange over three tools; the transport is
  small enough to implement with the standard library.

# Consequences

Siddhi must tolerate a source that changes without notice: an unsupported contract
version, unknown state, or malformed answer fails one refresh explicitly instead of
being coerced, and prior valid inventory stays readable. The adapter is bound to a
machine-local executable path, so tests replace the port and never start Vyasa; a
scripted local process verifies the transport. Replacing the interface later means a
new adapter, not changes to portfolio rules. Authentication, cursor stability, scan
coverage semantics, and versioning policy remain open and are not claimed.

Related: [Vyasa inventory integration](../architecture/vyasa-integration.md),
[Vyasa contract direction](../technologies/vyasa-contract-direction.md),
[source adapter boundaries](source-adapter-boundaries.md).
