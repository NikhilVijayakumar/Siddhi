# Non-executable acceptance draft; no runner or step definitions.
@FR-049 @NFR-021 @NFR-025 @NFR-039
Feature: Configured access boundaries resist untrusted instructions
  Scenario: Read a permitted source
    Given a source location and operation explicitly authorized by configured access policy
    When the backend retrieves the source through its permitted mechanism
    Then access remains within that configured scope

  Scenario: Refuse an unauthorized path escape
    Given an input path resolves outside the authorized source locations under the agreed containment policy
    When source access is requested
    Then the unauthorized location is not read and the boundary failure is safely reported

  Scenario: Ignore authority claims embedded in source content
    Given a repository document or imported result instructs the backend to override its operating rules and read another location
    When the content is processed as evidence
    Then the instructions grant no access and trigger no unintended action