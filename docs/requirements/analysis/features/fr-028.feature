# Non-executable acceptance draft; no runner or step definitions.
@FR-028
Feature: Explain material findings
  Scenario: Trace a finding to evidence and rule
    Given a material finding derived from a defined rule and captured source evidence
    When its explanation is retrieved
    Then its basis includes applicable source references and the producing rule

  Scenario: Disclose a candidate's limitations
    Given a finding depends on an assumption and incomplete data and a candidate match
    When the finding is reported
    Then those limitations are visible rather than presented as an established conclusion