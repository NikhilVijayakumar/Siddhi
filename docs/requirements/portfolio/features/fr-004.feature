# Non-executable acceptance draft; no runner or step definitions.
@FR-004
Feature: Attributed portfolio associations
  Scenario: Record an owner-approved project contribution
    Given a goal and an initiative and a project discovered through Vyasa
    When the owner records their association with its nature and supplied rationale
    Then the relationship retains its project reference and approval state

  Scenario: Keep inferred relevance unconfirmed
    Given analysis infers a candidate association with supporting evidence
    When the candidate becomes available to the owner
    Then it remains a candidate rather than a confirmed strategic relationship