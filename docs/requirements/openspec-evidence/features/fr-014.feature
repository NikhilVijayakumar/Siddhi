# Non-executable acceptance draft; no runner or step definitions.
@FR-014
Feature: Supported OpenSpec inventory
  Scenario: Retrieve available development artifacts
    Given a supported schema with requirements and scenarios and changes and tasks and declared statuses
    When the captured OpenSpec inventory is queried
    Then available artifacts and their source references are exposed according to that schema

  Scenario: Do not invent unsupported inventory
    Given a repository uses an unsupported OpenSpec variant
    When inventory is requested
    Then the coverage limitation is visible without inventing requirements or interpreting unknown statuses as supported