# Non-executable acceptance draft; no runner or step definitions.
@FR-001
Feature: Independent goal lifecycle
  Scenario: Create and retrieve a goal before project selection
    Given the owner has an intended outcome and no associated project
    When the owner creates and retrieves the goal
    Then the goal retains its stable identity and entered outcome without a repository

  Scenario: Revise and archive without losing retrieval
    Given an existing goal with a recorded revision
    When the owner updates and then archives the goal
    Then the archived goal can still be retrieved with its historical revisions