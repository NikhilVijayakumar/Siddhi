# fun-02-project-inventory Specification

## Purpose
Define how the system observes the project inventory Vyasa reports: an explicit,
complete read that publishes project summaries with their source state, observation
times and freshness, while leaving stored data untouched when the source fails.

## Requirements

### Requirement: Refresh Vyasa inventory explicitly

The system SHALL refresh project inventory only when explicitly asked, SHALL read the
agreed Vyasa inventory to completion, and SHALL record the run with its outcome, source
freshness and counts of added, updated, removed and unchanged projects.

#### Scenario: Record a completed refresh

- **GIVEN** a reachable Vyasa index with projects
- **WHEN** the owner asks for an inventory refresh
- **THEN** every project on every page is stored with its native identifier
- **AND** the run records its start time, finish time, outcome, source freshness and
  counts of added, updated, removed and unchanged projects

#### Scenario: Repeat an unchanged refresh

- **GIVEN** a completed refresh and an unchanged Vyasa inventory
- **WHEN** the owner refreshes again
- **THEN** every project is counted unchanged and no project is duplicated
- **AND** each project keeps its first observation time and gains the new observation time

### Requirement: Preserve prior valid inventory when a refresh fails

A refresh that cannot obtain a complete inventory SHALL NOT publish partial data, and
the previously observed projects SHALL remain readable with their own observation time.

#### Scenario: Source unavailable after a valid refresh

- **GIVEN** a completed refresh with stored projects
- **WHEN** a later refresh fails because Vyasa is unreachable
- **THEN** the refresh is reported as unavailable with a run identifier
- **AND** a failed run records the outcome and failure category
- **AND** the stored projects are still returned unchanged

#### Scenario: Failure during paging

- **GIVEN** a Vyasa read that succeeds for the first page and fails for the second
- **WHEN** the refresh runs
- **THEN** no project from the first page is published
- **AND** the failed run is recorded

### Requirement: List and retrieve observed projects

The system SHALL list observed projects with bounded cursor pagination and SHALL return
one project by its native identifier. Listing and retrieval SHALL NOT contact Vyasa.

#### Scenario: List projects across a page boundary

- **GIVEN** more observed projects than one page can return
- **WHEN** the owner lists projects
- **THEN** a bounded page is returned with an opaque cursor
- **AND** following the cursor returns the remaining projects without duplicates

#### Scenario: Filter by project state

- **GIVEN** observed projects in more than one state
- **WHEN** the owner lists projects for one state
- **THEN** only projects in that state are returned

#### Scenario: Unknown project identifier

- **GIVEN** an identifier that no observed project uses
- **WHEN** the owner retrieves it
- **THEN** the response is a not-found error

### Requirement: Distinguish source state, freshness and observation time

Each stored project SHALL keep the source's own state and identity status, and SHALL
distinguish the source's freshness from the time Siddhi observed it. A source state of
`missing` or `inaccessible` SHALL NOT be reported as deletion.

#### Scenario: Report a missing project without deleting it

- **GIVEN** a project Vyasa reports as `missing`
- **WHEN** the owner lists or retrieves it
- **THEN** it is returned with state `missing`
- **AND** its observation time and the freshness of the run that observed it are shown

#### Scenario: Distinguish stale inventory from a fresh read

- **GIVEN** a completed refresh whose source reported freshness `stale`
- **WHEN** the owner retrieves a project from that refresh
- **THEN** the project reports freshness `stale` and its own observation time

### Requirement: Remove only from a complete observation

The current project view SHALL contain only projects present in the latest completed
refresh. A project absent from that refresh SHALL be removed from the view, while a
failed or incomplete refresh SHALL remove nothing.

#### Scenario: Project absent from a complete read

- **GIVEN** a stored project that the next completed Vyasa read does not return
- **WHEN** the refresh completes
- **THEN** the project is no longer in the current view
- **AND** the run counts it as removed

### Requirement: Local portfolio work survives Vyasa failure

Failure or absence of the Vyasa integration SHALL NOT make goals or previously
observed projects unavailable.

#### Scenario: Vyasa not configured

- **GIVEN** no Vyasa executable is configured
- **WHEN** the owner lists goals, reads a project or asks for a refresh
- **THEN** goal and project reads are served normally
- **AND** the refresh reports that the source is unavailable rather than failing the service
