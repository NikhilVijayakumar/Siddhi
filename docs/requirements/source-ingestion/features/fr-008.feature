# Non-executable acceptance draft; no runner or step definitions.
@FR-008 @NFR-013
Feature: Artifact discovery with scoped absence
  Scenario: Identify supported evidence kinds
    Given a discovered repository containing supported OpenSpec and OKF and Git evidence
    When the authorized artifact scope is inspected
    Then supported artifacts are identified with their source locations

  Scenario: Distinguish access failure from absence
    Given one inspected location contains no artifact and another cannot be accessed
    When discovery reports its findings
    Then the absent artifact and the inaccessible location have distinguishable outcomes