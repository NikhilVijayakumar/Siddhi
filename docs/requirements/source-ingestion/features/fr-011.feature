# Non-executable acceptance draft; no runner or step definitions.
@FR-011 @NFR-005 @NFR-008
Feature: Explicit comparable refreshes
  Scenario: Record snapshot changes and outcome
    Given selected accessible sources and a prior successful snapshot with records of each change kind
    When an explicit refresh obtains and normalizes their latest supported content
    Then additions and modifications and supported removals and unchanged records are reported with refresh time and historical state

  Scenario: Retry a partially failed refresh
    Given one source succeeded and another failed during a refresh
    When the same unchanged successful input is retried
    Then partial failures remain reported and retrying does not duplicate logical source records