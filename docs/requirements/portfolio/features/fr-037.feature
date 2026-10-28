# Non-executable acceptance draft; no runner or step definitions.
@FR-037
Feature: Portfolio operation without time logging
  Scenario: Review an outcome without entered hours
    Given the owner has never entered project or task hours
    When the owner uses the goal and review workflows
    Then manual time entries are not prerequisites for those workflows

  Scenario: Expose absent execution information
    Given neither source artifacts nor owner input provides execution evidence
    When the owner inspects the goal's execution context
    Then the lack of execution information is visible rather than replaced with estimated hours