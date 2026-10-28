# Non-executable acceptance draft; no runner or step definitions.
@NFR-004 @NFR-028 @NFR-032 @NFR-033 @NFR-034 @NFR-035 @NFR-036 @NFR-038
Feature: Reproducible proportionate engineering quality
  Scenario: Measure local deterministic resource use
    Given representative agreed repositories and portfolio fixtures on a documented workstation
    When routine deterministic operations are measured
    Then memory and storage results are recorded without requiring a dedicated server or distributed database or GPU or AI service

  Scenario: Exercise responsibilities independently
    Given domain and analysis tests using controlled application ports
    When those tests run without HTTP transport or UI state or native source parsing
    Then portfolio rules remain testable independently of those infrastructure concerns

  Scenario: Explain a significant architectural choice
    Given a design introduces a significant architectural trade-off
    When the design is reviewed
    Then its context and alternatives and consequences are documented rather than inferred from code

  Scenario: Validate a dependency change deliberately
    Given a dependency proposed for a clear purpose with appropriate version constraints
    When the dependency is added or updated
    Then relevant automated tests are used to evaluate the change without introducing unnecessary infrastructure

  Scenario: Cover critical behavior across backend layers
    Given identified critical domain and API and parser and persistence and migration and analysis and error behaviors
    When a delivery slice's verification evidence is reviewed
    Then executed automated coverage is mapped to those risks rather than judged solely by a coverage percentage

  Scenario: Reproduce difficult source fixtures offline
    Given controlled supported-version and malformed and missing-metadata and stale and conflicting-evidence fixtures
    When routine fixture tests run without private repositories or external AI services
    Then those cases remain reproducible and their actual outcomes are recorded

  Scenario: Isolate integration availability
    Given external systems are replaced with controlled doubles implementing documented interfaces
    When isolated tests and applicable contract checks run
    Then external availability does not determine routine test outcomes and compatibility evidence is distinguished from simulated behavior

  Scenario: Exercise recovery-relevant failures
    Given fixtures for interrupted refresh and unavailable source and invalid data and failed transaction and external timeout and retry
    When relevant failure-path tests are executed
    Then safety and retry outcomes are asserted and any failed or unavailable check is reported honestly