# Non-executable acceptance draft; no runner or step definitions.
@FR-026
Feature: Rule-based goal comparison
  Scenario: Compare a goal with captured capabilities
    Given a goal revision with outcomes and constraints and identified project and requirement and knowledge evidence
    When defined rules compare the recorded inputs
    Then comparison results retain the rule basis and relevant input references

  Scenario: Keep routine analysis independent of AI
    Given relevant stored inputs are available and no external AI service is available
    When deterministic comparison is requested
    Then defined-rule comparison can run without obtaining external AI output