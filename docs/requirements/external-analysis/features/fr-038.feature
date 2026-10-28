# Non-executable acceptance draft; no runner or step definitions.
@FR-038 @NFR-024
Feature: Purpose-bounded analysis briefs
  Scenario: Prepare relevant context
    Given a defined analysis purpose and relevant goals and evidence and known gaps and assumptions
    When the owner prepares a structured brief
    Then the brief includes relevant constraints and judgment questions and selected evidence references

  Scenario: Do not disclose unrelated private content
    Given private repository content outside the authorized purpose and no authorization to share it
    When a brief is prepared for external use
    Then that content is not included or sent as a side effect