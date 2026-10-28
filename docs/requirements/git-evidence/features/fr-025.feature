# Non-executable acceptance draft; no runner or step definitions.
@FR-025
Feature: Non-mutating repository observation
  Scenario: Refresh without changing repository state
    Given a repository with known contents and checked-out branch and commits
    When routine refresh and analysis complete
    Then the contents and checkout and commits remain unchanged and no plan is published

  Scenario: Do not repair access by checkout
    Given the desired revision evidence cannot be read through the configured access mechanism
    When routine collection fails
    Then the limitation is reported without checking out another branch or committing source changes