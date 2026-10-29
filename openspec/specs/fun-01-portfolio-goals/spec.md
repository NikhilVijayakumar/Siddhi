# fun-01-portfolio-goals Specification

## Purpose
Lets the portfolio owner capture, read back, revise, list and retire goals that need no project, repository or initiative reference, keeping every unrecorded field explicitly unknown and every change in an append-only history.

## Requirements

### Requirement: Capture a goal before any project exists

The system SHALL let the portfolio owner create a goal with no project, repository or
initiative reference, and SHALL return the created goal with a stable identifier.

#### Scenario: Create a repository-free goal

- **GIVEN** no projects exist in the database
- **WHEN** the owner creates a goal with a title, an outcome type and no other field
- **THEN** the goal is stored with a stable identifier and status `active`
- **AND** the response names every field that remains unrecorded

#### Scenario: Create a goal for a non-software outcome

- **GIVEN** an owner capturing a publication or internal-investment outcome
- **WHEN** the goal is created with that outcome type
- **THEN** no lifecycle stage, maturity criterion or time-entry field is required
- **AND** the goal is retrievable exactly as created

### Requirement: Retrieve and list goals

The system SHALL return a goal by identifier and SHALL list goals with bounded,
cursor-based pagination. Listing SHALL NOT require reading any source adapter.

#### Scenario: List goals across a page boundary

- **GIVEN** more goals than one page can return
- **WHEN** the owner lists goals
- **THEN** a bounded page is returned with an opaque cursor
- **AND** following the cursor returns the remaining goals without duplicates

#### Scenario: Unknown goal identifier

- **GIVEN** an identifier that no goal uses
- **WHEN** the owner retrieves it
- **THEN** the response is a not-found error
- **AND** no other goal's data appears in the response

### Requirement: Revise a goal and retain its history

Every material goal change SHALL append a revision recording the prior state, the
changed fields, the change time and the owner-supplied reason when one was given.

#### Scenario: Revise a goal

- **GIVEN** an existing goal
- **WHEN** the owner changes its priority with a reason
- **THEN** the goal returns the new value
- **AND** a new revision records the prior value, the new value, the time and the reason

#### Scenario: Reject a stale revision

- **GIVEN** a goal the owner has already revised
- **WHEN** an update supplies an outdated expected revision
- **THEN** the response is a conflict error
- **AND** the stored goal and its revisions are unchanged

### Requirement: Archive a goal without deleting it

Archiving SHALL remove a goal from default active listings while preserving its
identifier, content and full revision history.

#### Scenario: Archive and retrieve

- **GIVEN** an active goal with at least one revision
- **WHEN** the owner archives it
- **THEN** it no longer appears in the default listing
- **AND** retrieving it by identifier still returns it with its history

#### Scenario: Archive twice

- **GIVEN** an already archived goal
- **WHEN** it is archived again
- **THEN** the request succeeds without creating a second archival revision

### Requirement: Absent information stays explicitly unknown

A field the owner has not supplied SHALL be reported as unknown rather than filled
with an invented value, a default date, a zero priority or an empty success criterion.

#### Scenario: Goal with unrecorded constraints

- **GIVEN** a goal created without a target date or constraints
- **WHEN** the goal is retrieved
- **THEN** those fields are null and named as unrecorded
- **AND** no substitute date, budget or priority score is returned

### Requirement: Reject invalid changes atomically

The system SHALL validate every write, reject invalid input with a structured error,
and leave stored goals, revisions and schema version unchanged when a write fails.

#### Scenario: Invalid outcome type

- **GIVEN** an existing goal
- **WHEN** an update supplies an outcome type outside the supported set
- **THEN** the response is a validation error naming the field
- **AND** no goal row or revision row changes

#### Scenario: Blank title

- **GIVEN** a create request with an empty title
- **WHEN** it is submitted
- **THEN** the request is rejected as invalid
- **AND** no goal is created
