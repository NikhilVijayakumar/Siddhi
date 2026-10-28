# Non-executable acceptance draft; no runner or step definitions.
@FR-035
Feature: Balanced strategic reviews
  Scenario: Compare portfolio trade-offs
    Given commercial results and internal investment relationships and a neglected goal
    When the owner prepares a strategic review
    Then the review presents outcome progress and constraints and trade-offs and recommendations requiring decisions

  Scenario: Avoid invented commercial superiority
    Given commercial results are unavailable and an internal investment has an unproven benefit
    When a strategic review is prepared outside the initial monthly cadence
    Then missing results remain visible and neither kind of work receives automatic priority