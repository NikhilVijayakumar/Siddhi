# Non-executable acceptance draft; no runner or step definitions.
@FR-041
Feature: Explicit recommendation review
  Scenario: Record owner review outcomes
    Given imported recommendations awaiting owner review
    When the owner accepts or rejects or defers a recommendation or requests further investigation
    Then the selected review outcome is recorded for the recommendation

  Scenario: Protect approved state on import
    Given approved priorities and a source repository and a new imported recommendation
    When the recommendation becomes available for review
    Then approved priorities are not automatically changed and no repository change is published