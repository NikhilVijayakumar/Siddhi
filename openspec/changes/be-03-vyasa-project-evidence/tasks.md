# Implementation Tasks: Vyasa project evidence

- **OpenSpec Change ID:** `be-03-vyasa-project-evidence`
- **Status:** In Progress (artifacts drafted)
- **Related artifacts:** `proposal.md`, `specs/fun-03-project-evidence/spec.md`,
  `specs/tech-03-vyasa-mcp-adapter/spec.md`, `api-contract.md`, `design.md`, `adr.md`

## Slice 1: Source retrieval of one project

- [x] 1.1 Failing adapter tests: `get_project` returns a validated detail; unsupported
      version on retrieval fails; unknown identifier fails.
      Red evidence: 4 failed with `AttributeError: 'VyasaMcpSource' object has no attribute
      'get_project'`.
- [x] 1.2 Failing source-port test: the application port exposes the targeted retrieval.
      Red evidence: the port method is added in slice 2 together with the implementation.
- [x] 1.3 Implement the adapter `get_project` capability with the existing bounded session,
      schema validation and failure categories.
      Evidence: `tests/adapters/vyasa/test_mcp_source.py` → 19 passed; scripted scenarios
      cover detail retrieval, unsupported version, tool error, and wrong identifier.

## Slice 2: Evidence read over HTTP

- [x] 2.1 Failing contract tests for `GET /projects/{project_id}/evidence`: stored
      project returns checkout evidence; source failure maps to `503 source_unavailable`;
      source not configured returns `source_not_configured`; unknown stored identifier returns
      `404 project_not_found`.
      Red evidence: 4 failed (route/module did not exist yet).
- [x] 2.2 Implement application evidence retrieval and the HTTP route.
      Evidence: `tests/api/test_project_evidence.py` → 4 passed; full suite → 129 passed,
      1 warning. The live source probe showed the real `get_project` shape — checkout groups
      carrying markers/git/remote/languages/composition/frameworks with per-group status and
      observation times — and the response was corrected to mirror it instead of flattening.

## Slice 3: Verification and closeout

- [ ] 3.1 Full suite, `openspec validate`, reviews, honest gaps, merge, archive.

## Readiness review

- [ ] The proposal's readiness checklist is satisfied before implementation.
