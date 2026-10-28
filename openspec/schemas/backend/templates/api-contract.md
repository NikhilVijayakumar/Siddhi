# Interface and Data Contract: {{change-name}}

- **OpenSpec Change ID:** `{{change-id}}`
- **Proposing team:** be (backend team)
- **Related proposal:** `proposal.md`
- **Related specifications:** `specs/`
- **Related design:** `design.md`

## 1. Purpose

Describe the interface contract this change establishes: affected HTTP endpoints,
application operations, source adapter calls, or manual analysis export/import,
the payloads they exchange, the errors they return, and the data the change stores.
Include CLI commands only when affected and other upstream interfaces only when
selected or touched by the approved change. Do not mandate synchronization or
provider automation, or imply these interfaces already exist in the skeleton.

## 2. Scope

Identify the operations, entities, and integrations affected by this contract,
and any explicitly excluded from it.

## 3. Interface Surface

For each affected operation, state the full contract. Coding agents build
against this section, so an unstated default is a decision nobody made.

| Operation | Boundary / transport | Access / authority | Input | Success output | Errors |
|---|---|---|---|---|---|
| Name | HTTP method/path / application operation / source adapter call / manual export/import / CLI only if affected | Authorized data, roots, paths, or credentials used | Fields and types | Fields, types, evidence | Conditions, codes, and HTTP status if applicable |

## 4. Error Model

State which conditions produce which error, what shape the error takes, and
what the response must not reveal. State whether errors are retryable and
whether they are safe to surface to the user.

| Condition | Error code | Response shape | Safe to show the user |
|---|---|---|---|
| Condition | Code | Shape | Yes / No |

## 5. Trust Boundary

State which inputs are trusted configuration and which are untrusted
repository or provider content, which paths and data each operation may read
or return, and which data stays machine-local versus portable or explicitly
authorized for export. Record applicable authorization failures, requests outside
configured source/workspace boundaries, and missing or invalid credentials.
Do not invent an access policy where approval is still pending.

Use general security review guidance for HTTP/application and source boundaries.
Consult `mcp-server-review` only when an MCP interface is actually touched or
selected as an upstream source interface, not merely because local paths,
credentials, or untrusted data are involved.

## 6. Data Model

State the entities, fields, types, constraints, provenance, and invariants
that affected application payloads, SQLite records, and import/export formats
must hold. Use `data-ownership-review` for ownership and precedence; inherited
checklists do not require a synchronized index or another product's layout.

| Entity | Field | Type | Required | Constraint or invariant |
|---|---|---|---|---|
| Name | Name | Type | Yes / No | Rule |

State the integrity rules that the persistence layer must guarantee and the
behavior when a constraint is violated.

## 7. Migrations and Backward Compatibility

State how any existing HTTP/application consumers, stored data, and affected
source or import/export formats survive this change: migration steps, their
order, compatibility, and rollback. Include CLI compatibility only when affected.
State explicitly when no migration is required; do not invent existing consumers
or stored production data.

Consult `api-contract-testing` for affected contracts and
`database-integration-testing` for migration and constraint verification.

## 8. Traceability

| Requirement | Operation | Field or rule | Acceptance scenario |
|---|---|---|---|
| Requirement ID | Operation name | Field or invariant | Scenario name |

## 9. Contract Review

- [ ] Every affected operation is listed with request, response, and errors.
- [ ] The error model states which conditions produce which error.
- [ ] The trust boundary is stated per operation, including applicable authorization, source/workspace boundary, and credential failures.
- [ ] The data model states the invariants affected payloads, stored records, and import/export formats must hold.
- [ ] Migration and backward compatibility are stated.
- [ ] Every requirement in scope is traced to an operation or rule.
- [ ] Unresolved contract questions are recorded as explicit open questions.

**Status:** Draft / Ready for design
