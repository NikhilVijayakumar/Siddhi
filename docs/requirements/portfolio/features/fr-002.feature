# Non-executable acceptance draft; no runner or step definitions.
@FR-002
Feature: Heterogeneous portfolio outcomes
  Scenario: Represent creative and engineering outcomes
    Given a publication goal and an internal engineering investment goal
    When their distinct success criteria and lifecycle information are recorded
    Then both goals retain their own criteria without identical maturity stages

  Scenario: Avoid software-only prerequisites
    Given a research goal with no software release milestone
    When the owner records the intended research outcome
    Then the goal does not require software release evidence to exist