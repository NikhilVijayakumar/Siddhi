# tech-03-vyasa-mcp-adapter Specification

## Purpose
Define the read-only bridge from Siddhi to a machine-local Vyasa MCP server: how the
inventory is requested, validated, paged and reported when it cannot be read.

## Requirements

### Requirement: Read Vyasa only through the agreed read-only interface

The Vyasa adapter SHALL obtain inventory through the local stdio MCP interface, SHALL
use only its read-only inventory tools, and SHALL NOT trigger a workspace scan or
modify anything Vyasa owns.

#### Scenario: Read inventory with read-only tools

- **GIVEN** a configured Vyasa MCP executable
- **WHEN** the adapter fetches inventory
- **THEN** it starts one local process, completes the protocol handshake, and calls only
  the read-only inventory tool
- **AND** it closes the process when the read ends, successfully or not

### Requirement: Validate the source contract and fail explicitly

The adapter SHALL check the source's declared contract version and required fields, and
SHALL turn any unsupported or malformed answer into an explicit failure category
instead of guessing, coercing or partially publishing.

#### Scenario: Unsupported schema version

- **GIVEN** a Vyasa answer declaring a contract version the adapter does not support
- **WHEN** the refresh runs
- **THEN** the run fails with category `unsupported_contract`
- **AND** no project is published

#### Scenario: Tool reports an error

- **GIVEN** a Vyasa tool result marked as an error
- **WHEN** the refresh runs
- **THEN** the run fails with category `tool_error`
- **AND** the response exposes the category and run identifier, not the source message

### Requirement: Bound paging and reject a stalled cursor

The adapter SHALL follow the source cursor until the inventory is complete, SHALL bound
the number of pages and projects it accepts, and SHALL fail rather than loop when the
cursor does not advance.

#### Scenario: Cursor repeats

- **GIVEN** a Vyasa read that returns the same cursor twice
- **WHEN** the adapter pages through the inventory
- **THEN** it fails with a protocol failure category
- **AND** nothing is published

### Requirement: Replaceable adapter boundary

The application SHALL depend on an inventory port, not on Vyasa transport, so the
adapter can be replaced behind its contract and automated tests need no live Vyasa.

#### Scenario: Test double supplies the inventory

- **GIVEN** an inventory port implementation that returns a fixed observation
- **WHEN** refresh, listing and retrieval are exercised
- **THEN** the stored projection and responses depend only on the port's answer
- **AND** no Vyasa process is started
