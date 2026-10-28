# Non-executable acceptance draft; no runner or step definitions.
@FR-021
Feature: Knowledge source non-mutation
  Scenario: Read and analyze without rewriting
    Given authoritative OKF concepts and metadata and relationships
    When routine ingestion and analysis run
    Then those authoritative artifacts remain unchanged

  Scenario: Do not repair invalid metadata implicitly
    Given an OKF artifact violates its supported profile
    When ingestion reports the validation limitation
    Then the artifact is not rewritten and no publishing workflow is triggered