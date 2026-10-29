# tech-03-vyasa-mcp-adapter Specification

## ADDED Requirements

### Requirement: Retrieve a project by identifier

The Vyasa adapter SHALL support targeted retrieval of a single project by its source
identifier through the local read-only stdio interface, SHALL apply the same source schema
version and field validation as inventory reads, and SHALL fail with explicit categories
when the retrieval cannot complete.

#### Scenario: Retrieve one project through the local adapter

- **GIVEN** a local source that answers a `get_project` tool call for the identifier
- **WHEN** the adapter retrieves that project
- **THEN** it returns the validated detail without fetching an inventory page

#### Scenario: Reject an incompatible source detail

- **GIVEN** a source that answers `get_project` with a different schema version or for a
  different identifier
- **WHEN** the adapter retrieves a project
- **THEN** it fails with an unsupported contract or protocol category and publishes no
  evidence
