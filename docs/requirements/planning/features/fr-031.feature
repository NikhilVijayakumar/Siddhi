# Non-executable acceptance draft; no runner or step definitions.
@FR-031
Feature: Outcome-oriented plans
  Scenario: Record relevant planning detail
    Given an initiative with intended outcomes
    When the owner records activities and milestones with dependencies and known dates and risks
    Then the plan retains those details and its goal relationships

  Scenario: Avoid identical stages for different work
    Given a research initiative and a product initiative with different planning needs
    When the owner creates their plans
    Then both plans can represent their relevant work without identical lifecycle stages