# Non-executable acceptance draft; no runner or step definitions.
@FR-034
Feature: Execution reviews
  Scenario: Compare execution context
    Given a current plan and a prior review and newly available evidence
    When the owner prepares an execution review
    Then the review includes plan progress and milestone changes and blockers and risks and proposed actions

  Scenario: Review outside the initial weekly cadence
    Given an urgent execution review is needed between weekly reviews
    When the owner records the review with incomplete milestone evidence
    Then the review can be retained with its timing and unresolved milestone limitations