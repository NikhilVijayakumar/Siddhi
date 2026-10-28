# Non-executable acceptance draft; no runner or step definitions.
@FR-030 @NFR-020
Feature: Qualified historical comparisons
  Scenario: Compare evidence-driven changes
    Given retained previous and current reports with the same rule version and changed evidence
    When reports are compared
    Then meaningful source and finding and gap and unresolved-question differences identify their changed-input basis

  Scenario: Distinguish rule-driven interpretation changes
    Given reports use the same evidence but different analysis rule versions
    When their findings are compared
    Then differences are qualified as rule-version changes rather than presented as source progress