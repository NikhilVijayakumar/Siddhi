# Non-executable acceptance draft; no runner or step definitions.
@FR-020
Feature: Independent knowledge and requirements
  Scenario: Use standalone knowledge
    Given a supported OKF package with no related OpenSpec requirement
    When knowledge is discovered and queried
    Then the knowledge remains discoverable and usable without creating a requirement

  Scenario: Retain a requirement without matching knowledge
    Given a requirement with absent or insufficient related engineering knowledge
    When optional knowledge relationships are inspected
    Then the requirement remains available without a forced one-to-one mapping