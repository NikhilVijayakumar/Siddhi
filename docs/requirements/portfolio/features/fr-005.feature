# Non-executable acceptance draft; no runner or step definitions.
@FR-005
Feature: Explicit constraints and unknowns
  Scenario: Retrieve entered strategic constraints
    Given the owner knows a priority and a target date and a dependency
    When those values and a strategic assumption are recorded
    Then subsequent retrieval preserves those entered constraints and assumption

  Scenario: Do not invent a budget
    Given the owner has not supplied a budget or resource estimate
    When the goal's constraints are retrieved
    Then the missing budget and resource information remain identifiable as unknown