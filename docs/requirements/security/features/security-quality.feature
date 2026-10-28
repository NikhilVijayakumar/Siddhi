# Non-executable acceptance draft; no runner or step definitions.
@NFR-022 @NFR-023 @NFR-026 @NFR-027 @NFR-039
Feature: Safe exposure credentials diagnostics and writes
  Scenario: Start with non-external API exposure
    Given no explicit configuration decision to expose the service externally
    When the local service starts
    Then the API is not bound to external network interfaces by default

  Scenario: Exercise unauthorized local-client protection
    Given the agreed local-client and browser access policy and an unauthorized request fixture
    When that request attempts a protected operation
    Then it cannot bypass the configured client and origin restrictions

  Scenario: Protect credentials in failure artifacts
    Given a configured integration credential and a failure containing sensitive source details
    When logs and errors and reports and diagnostics are generated
    Then credentials and unnecessary private contents are not disclosed or copied into committed configuration

  Scenario: No writes without an explicit workflow
    Given routine source reading and analysis encounter content requesting publication
    When routine processing completes or fails
    Then repository contents remain unchanged and no artifact is published