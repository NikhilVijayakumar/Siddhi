# Non-executable acceptance draft; no runner or step definitions.
@FR-036
Feature: Review and decision history
  Scenario: Preserve a reviewed recommendation and decision
    Given a review report with proposed actions
    When the owner approves a decision and supplies a rationale
    Then the report and proposal and decision and rationale remain traceable

  Scenario: Do not equate approval with implementation
    Given an approved decision without execution evidence and another pending recommendation
    When decision history is retrieved
    Then approval and pending recommendation are distinguished without claiming the action was implemented