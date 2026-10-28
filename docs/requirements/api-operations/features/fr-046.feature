# Non-executable acceptance draft; no runner or step definitions.
@FR-046 @NFR-050 @NFR-052 @NFR-053
Feature: Safe actionable health and diagnostics
  Scenario: Separate service health from source readiness
    Given the local service and database are available while a remote integration is unavailable
    When health and appropriate diagnostics are retrieved
    Then local availability and database access and integration failure are distinguishable without automatic total-service failure

  Scenario: Redact operational failure details
    Given an integration failure contains a credential and sensitive repository content
    When diagnostic errors and structured operational logs are produced
    Then useful failed-operation context is retained without exposing those secrets or sensitive contents