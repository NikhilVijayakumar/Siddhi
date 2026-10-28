# Non-executable acceptance draft; no runner or step definitions.
@FR-043 @NFR-030 @NFR-040 @NFR-041 @NFR-043 @NFR-048
Feature: Documented UI-independent capabilities
  Scenario: Consume an implemented operation independently
    Given an implemented capability exposed through HTTP with generated contract documentation
    When an independent client and contract test use its documented request and response schemas
    Then validated behavior is available without duplicating portfolio rules in the client

  Scenario: Prevent silent unbounded contract drift
    Given a growing collection and a proposed breaking public schema change
    When the API contract is reviewed for delivery
    Then bounded retrieval is defined and the breaking change requires an explicit compatibility strategy