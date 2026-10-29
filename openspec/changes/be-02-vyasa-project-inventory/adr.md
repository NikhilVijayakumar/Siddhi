# Architecture Decision Record: Vyasa project inventory

## 1. Decision Status

- **Status:** Accepted for this change as a draft decision; no human approval recorded
- **Date:** 2026-10-29
- **OpenSpec Change ID:** `be-02-vyasa-project-inventory`
- **Decision owners:** project owner (draft authors; no approval recorded)
- **Related artifacts:** `proposal.md`, `design.md`, `specs/`

## 2. Decision Checkpoint

- [x] **New decision required:** This change fixes the first supported Vyasa interface
  and its transport.
- [ ] **Existing decision applies:** Adapter isolation and source authority were
  already decided; the interface choice was not.
- [ ] **No new ADR required:** The change does make one durable integration decision.

### Rationale

`knowledge/decisions/source-adapter-boundaries.md` already requires adapters behind
declared ports, and `source-authority-and-read-only-ingestion.md` already requires
read-only ingestion. Those govern the shape of the adapter but not which Vyasa
interface Siddhi supports. That choice was the requirement package's remaining owner
decision and is now recorded as
`knowledge/decisions/vyasa-mcp-inventory-interface.md`.

## 3. Context

Vyasa is the intended inventory authority, but its contract was unverified. A
read-only inspection on 2026-10-29 found a local stdio MCP server with read-only
inventory tools, no export command, and no offered HTTP interface. Siddhi needs an
inventory source for the next delivery step and must not become a second scanner or
couple to Vyasa's internal index.

## 4. Decision

Adopt the local Vyasa MCP server over stdio as the first inventory interface, using
only its read-only inventory tool, behind an application port. Do not adopt direct
index access, a bespoke export format, or a second scanner. Implement the small stdio
JSON-RPC exchange with the standard library rather than adding an MCP client
dependency.

## 5. Alternatives Considered

| Alternative | Why rejected |
|---|---|
| Structured export file | No export interface exists; Siddhi would invent and own a format Vyasa does not |
| Direct index/database read | Couples to an internal schema never offered as a contract and bypasses Vyasa's read-only semantics |
| Second scanner | Duplicates the authority Siddhi intends to consume |
| Official MCP client dependency | Heavy for three read-only tool calls over newline-delimited JSON; tests would inherit a live-process dependency |
| Long-lived MCP process | Unearned before refresh cost is measured; adds lifecycle and restart complexity |

## 6. Consequences

- Positive: a real, verified interface is used; the adapter is replaceable; automated
  tests stay offline; no new dependency.
- Negative: the hand-written transport must handle timeouts, stderr, and malformed
  messages; any Vyasa contract drift fails a refresh until the adapter is updated.
- Neutral: the executable path is machine-local configuration; the service starts
  without it and reports the integration as not configured.

## 7. Follow-up

- Confirm cursor stability, authentication, and versioning policy with a second Vyasa
  deployment or a documented Vyasa contract before widening support.
- Delete or retain `ingestion_runs` history once a retention target is agreed.

## 8. Knowledge References

- `knowledge/decisions/vyasa-mcp-inventory-interface.md`
- `knowledge/decisions/source-adapter-boundaries.md`
- `knowledge/decisions/source-authority-and-read-only-ingestion.md`
- `knowledge/decisions/source-history-and-provenance.md`
- `knowledge/architecture/vyasa-integration.md`
- `knowledge/technologies/vyasa-contract-direction.md`
