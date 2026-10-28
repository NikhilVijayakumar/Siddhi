# Non-executable acceptance draft; no runner or step definitions.
@FR-016
Feature: Schema-scoped missing evidence
  Scenario: Explain an incomplete reference
    Given a supported schema permits assessing a required reference that is missing
    When evidence completeness is assessed
    Then a finding identifies the missing reference and its schema-based assessment basis

  Scenario: Avoid universal artifact obligations
    Given the supported project schema does not require a particular artifact
    When its absence is observed
    Then absence alone is not reported as a violation of a universal artifact requirement