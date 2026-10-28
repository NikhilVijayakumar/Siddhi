# Non-executable acceptance draft; no runner or step definitions.
@FR-047 @NFR-007 @NFR-014 @NFR-015
Feature: Consistent records and history
  Scenario: Commit a logically related revision
    Given related portfolio records and historical snapshots in a consistent state
    When a logical operation passes integrity checks and commits
    Then valid relationships and the required historical context are retained

  Scenario: Fail without silent partial corruption
    Given an operation changing related portfolio records and snapshot references
    When failure occurs inside its agreed transaction boundary
    Then the prior consistent state is preserved or a defined safely recoverable partial outcome is explicitly recorded