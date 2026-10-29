# fun-03-project-evidence Specification

## ADDED Requirements

### Requirement: Retrieve checkout-level evidence for a stored project

The system SHALL provide an operation that retrieves the checkout-level evidence for one
known project through the configured source, and SHALL fail with an explicit source error
when that evidence cannot be supplied.

#### Scenario: Retrieve checkout evidence for a stored project

- **GIVEN** a stored project and a configured source that supports targeted retrieval
- **WHEN** the evidence operation runs for that project
- **THEN** it returns the project's checkout-level evidence, including the remote,
  languages, markers, frameworks and per-checkout status or observation time the source
  supplied, without treating an absent optional field as a deletion or failure

#### Scenario: Source cannot supply the evidence

- **GIVEN** a configured source that fails while retrieving the project
- **WHEN** the evidence operation runs
- **THEN** the operation fails with a source error category and leaves stored data
  unchanged

#### Scenario: Source cannot retrieve a single project

- **GIVEN** a configured source that has no targeted retrieval capability
- **WHEN** the evidence operation runs
- **THEN** it reports the unsupported capability instead of returning an empty success
