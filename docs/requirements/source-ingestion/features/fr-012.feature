# Non-executable acceptance draft; no runner or step definitions.
@FR-012 @NFR-006 @NFR-009 @NFR-013
Feature: Freshness and last-known-good preservation
  Scenario: Expose distinct source states
    Given sources that are current or stale or unavailable or unsupported or invalid or never successfully ingested
    When source status is retrieved
    Then their applicable states remain distinguishable rather than collapsed to absent

  Scenario: Preserve valid data after failure
    Given a valid snapshot with a recorded revision and freshness context
    When a later refresh fails after obtaining incomplete data
    Then the prior valid data remains available with its revision and qualified freshness and failure information