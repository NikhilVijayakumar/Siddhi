# Non-executable acceptance draft; no runner or step definitions.
@FR-045 @NFR-001 @NFR-002 @NFR-044 @NFR-051
Feature: Observable expensive operations
  Scenario: Observe progress without losing routine responsiveness
    Given a refresh or analysis designated long-running under the agreed workload policy
    When it runs while a routine local request is made
    Then progress or final status remains obtainable and routine API access remains responsive under the reviewed measurement criteria

  Scenario: Report partial failure and safe retry
    Given a tracked operation encounters a source failure
    When its outcome is retrieved
    Then partial failures and relevant warnings and safe-retry limitations are visible without requiring an indefinite held connection