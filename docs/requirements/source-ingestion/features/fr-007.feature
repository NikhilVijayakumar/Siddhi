# Non-executable acceptance draft; no runner or step definitions.
@FR-007 @NFR-029
Feature: Inventory through Vyasa authority
  Scenario: Map a discovered project
    Given the agreed Vyasa interface returns a project and repository with source identifiers
    When project discovery runs
    Then internal references retain those identifiers without creating competing project identities

  Scenario: Discovery unavailable without losing local goals
    Given Vyasa cannot be reached and local portfolio records already exist
    When project discovery is attempted
    Then its failure is reported without making unrelated local portfolio records unavailable