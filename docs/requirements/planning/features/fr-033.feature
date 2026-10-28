# Non-executable acceptance draft; no runner or step definitions.
@FR-033
Feature: Milestones and uncertain dependencies
  Scenario: Inspect milestone relationships
    Given an initiative milestone with a date and status and a known dependency
    When the owner retrieves the milestone
    Then the milestone retains those values and its initiative and goal links

  Scenario: Expose an unresolved dependency
    Given a milestone dependency whose target cannot be established
    When the plan is inspected
    Then dependency uncertainty is identified without a fabricated resolution