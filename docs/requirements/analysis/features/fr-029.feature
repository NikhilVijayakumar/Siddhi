# Non-executable acceptance draft; no runner or step definitions.
@FR-029 @NFR-017 @NFR-018
Feature: Reproducible reports from recorded inputs
  Scenario: Reproduce equivalent findings
    Given identical normalized snapshots and portfolio revisions and rules and configuration
    When two deterministic reports are generated
    Then their analytical findings are equivalent and each report records input versions and generation time and rule or report version

  Scenario: Do not substitute newer evidence into reproduction
    Given a retained report input set and a newer source snapshot
    When the retained input set is used to reproduce findings
    Then the newer snapshot is not silently substituted for the recorded input