## ADDED Requirements

### Requirement: Report and evolve the database schema version

The system SHALL record its schema version, report it through diagnostics, and apply
schema changes only through ordered, versioned migrations.

#### Scenario: Fresh database at the current version

- **GIVEN** no database file exists
- **WHEN** the service starts
- **THEN** it creates the database at the current schema version
- **AND** diagnostics report that version

#### Scenario: Database ahead of the application

- **GIVEN** a database whose recorded version is newer than the application supports
- **WHEN** the service starts
- **THEN** startup fails with an actionable error naming both versions
- **AND** the existing data is left unmodified

### Requirement: Fail closed when a migration fails

A failing migration SHALL leave the prior schema and data usable and SHALL be reported
explicitly rather than retried silently.

#### Scenario: Migration fails mid-run

- **GIVEN** a database at an earlier schema version
- **WHEN** a migration raises an error
- **THEN** the earlier schema version and its data remain readable
- **AND** startup reports the migration failure and the version reached

### Requirement: Serve only on the local interface with safe diagnostics

The service SHALL bind to the loopback interface by default and SHALL expose health
information that separates service availability, database access and integration
readiness without revealing secrets, file paths or stored content.

#### Scenario: Default startup

- **GIVEN** default configuration
- **WHEN** the service starts
- **THEN** it listens on `127.0.0.1` only
- **AND** no external interface is opened

#### Scenario: Database unavailable at startup

- **GIVEN** a database path that cannot be opened
- **WHEN** the service starts
- **THEN** the health response reports database access as unavailable
- **AND** the error names the setting, not its secret value or the file's contents

### Requirement: Configure local operation without editing source

Database location, bind address and log level SHALL come from machine-local
configuration or environment values validated at startup, and SHALL never require a
source change.

#### Scenario: Invalid configured value

- **GIVEN** a bind address that is not a loopback address and no explicit override
- **WHEN** the service starts
- **THEN** startup fails with an error naming the setting
- **AND** the failure is reported without opening a network socket
