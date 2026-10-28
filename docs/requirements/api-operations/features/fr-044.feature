# Non-executable acceptance draft; no runner or step definitions.
@FR-044 @NFR-042
Feature: Consistent request validation and failure safety
  Scenario: Validate a supported write
    Given an input satisfying the agreed request schema and domain constraints
    When the API processes the operation successfully
    Then its response conforms to the documented response schema

  Scenario: Reject invalid input without partial mutation
    Given an existing consistent portfolio state and a request violating the agreed validation rules
    When the API processes the request
    Then a consistent validation error is returned without partial state changes

  Scenario: Preserve consistency on transactional failure
    Given a valid request whose transactional processing fails
    When the API reports the failure
    Then unintended partial state changes are not left behind and the error follows the agreed category