# External Analysis

**Document:** `external-analysis.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Controlled use of external AI and analytical providers for strategic interpretation, opportunity analysis, prioritization support, and decision preparation

**Related documents:** `vision.md`, `functional-requirements.md`, `non-functional-requirements.md`, `architectural-decisions.md`, `domain-model.md`, `data-ownership.md`, `data-model.md`, `ingestion-and-snapshots.md`, `deterministic-analysis.md`, `application-workflows.md`, `security-and-privacy.md`

---

## 1. Purpose

This document defines how Siddhi requests, manages, evaluates, and records analysis performed by external AI or analytical providers.

Deterministic analysis is the default for routine processing. Some portfolio questions, however, require interpretation, comparison, synthesis, and judgment that cannot be reliably expressed as fixed rules alone.

External analysis may help Siddhi answer questions such as:

- Which initiatives deserve attention given the current goals, evidence, constraints, and available resources?
- Which internal tools have strategic value across multiple projects?
- Where could existing engineering capabilities be reused?
- Which initiatives have overlapping outcomes or competing priorities?
- What is the smallest useful release that would validate an initiative?
- What are the trade-offs between investing in an internal capability and using an existing external solution?
- Which assumptions create the greatest uncertainty in a proposed plan?
- What evidence would most improve a strategic decision?
- What should be reconsidered after a major change in portfolio evidence?
- Which possible opportunities or risks deserve a human review?

External analysis is advisory. Siddhi remains responsible for preserving evidence, managing portfolio plans, recording approved decisions, and maintaining traceability.

## 2. Core principles

### 2.1 Deterministic analysis comes first

Routine collection, normalization, comparison, validation, counting, and rule-based assessment must not depend on external AI.

External analysis should consume the relevant deterministic findings and evidence rather than reproduce routine calculations unnecessarily.

### 2.2 External analysis is advisory

An AI-generated recommendation must not automatically:

- Change a goal's priority.
- Create or approve an initiative.
- Modify a plan or milestone.
- Mark a goal as achieved.
- Resolve a source conflict.
- Update OpenSpec or OKF.
- Modify a repository.
- Approve an investment or resource allocation.
- Replace a previously approved decision.

The user or an explicitly authorized approval workflow must make the relevant decision.

### 2.3 Evidence and interpretation are separate

Siddhi must distinguish:

- Source facts.
- Deterministic findings.
- AI interpretations.
- AI-generated recommendations.
- Human-reviewed conclusions.
- Approved portfolio decisions.

The fact that an AI output references a source does not mean that the source supports every conclusion in the output.

### 2.4 Preserve uncertainty

External analysis must be able to return:

- Insufficient information.
- Multiple plausible options.
- Conflicting evidence.
- Unresolved assumptions.
- Conditional recommendations.
- Questions requiring human clarification.

Siddhi must not require the provider to produce a confident recommendation when the available evidence does not justify one.

### 2.5 Portfolio context must remain balanced

External analysis must not automatically favor commercial projects over internal tools, or internal tools over commercial projects.

An internal capability may support multiple outcomes and have independent strategic value. Analysis should consider direct outcomes, enabling capabilities, reuse potential, constraints, costs, and opportunity costs rather than forcing every initiative into a single product-oriented category.

### 2.6 Preserve the human decision boundary

The external analysis workflow should help decision-makers understand their options, not transfer accountability for portfolio choices to a model.

This separation aligns with risk-management guidance emphasizing governance, documented limitations, provenance, testing, and appropriate human oversight for generative AI systems. <Cite refs={["turn827589search0","turn827589search4"]}/>

---

## 3. Scope

### 3.1 Included

The external analysis capability covers:

1. Defining an analysis objective.
2. Selecting the portfolio scope and relevant context.
3. Building a traceable evidence package.
4. Applying privacy and disclosure controls.
5. Selecting an approved provider or model.
6. Submitting a structured analysis request.
7. Recording request, execution, and response metadata.
8. Validating the response structure.
9. Separating claims, assumptions, findings, and recommendations.
10. Associating recommendations with supporting evidence.
11. Capturing uncertainty, limitations, and alternative options.
12. Supporting human review and approval.
13. Comparing analysis outputs over time.
14. Retaining provenance and audit history.
15. Handling provider failure, malformed responses, and incomplete results.

### 3.2 Excluded

The initial capability does not:

- Require a particular AI provider.
- Require an AI model for routine ingestion or deterministic analysis.
- Allow arbitrary providers to access the entire Siddhi database.
- Send complete repositories or knowledge collections by default.
- Automatically approve AI recommendations.
- Treat generated confidence statements as calibrated probabilities.
- Treat generated citations as verified unless Siddhi independently resolves and checks them.
- Allow an external model to modify source systems.
- Use AI-generated text as a replacement for structured portfolio records.
- Require autonomous multi-agent orchestration.
- Guarantee that an external model's response is correct, unbiased, or complete.

---

## 4. Analysis types

Siddhi should define a limited set of analysis types with explicit objectives and output expectations.

| Analysis type | Purpose | Expected output |
|---|---|---|
| Strategic prioritization | Compare initiatives against goals, constraints, and expected outcomes | Ranked or grouped options with rationale and trade-offs |
| Opportunity analysis | Identify possible opportunities and enabling capabilities | Candidate opportunities, supporting evidence, and validation needs |
| Internal investment assessment | Evaluate the value and cost of developing or maintaining an internal tool | Benefits, costs, dependencies, alternatives, and uncertainties |
| Reuse analysis | Identify capabilities that may support multiple projects | Candidate reuse relationships and required integration work |
| Scope reduction | Propose a minimum useful release | Essential outcomes, deferred scope, assumptions, and acceptance criteria |
| Risk and dependency analysis | Explore strategic consequences of known constraints and dependencies | Risks, affected goals, mitigations, and open questions |
| Evidence-gap analysis | Interpret missing or conflicting evidence | Important gaps and recommended evidence collection |
| Plan review | Examine an existing plan against current evidence and constraints | Potential adjustments, alternatives, and rationale |
| Portfolio review preparation | Summarize important changes and decisions requiring attention | Review brief, unresolved questions, and candidate actions |

These types should be reusable templates, not separate AI subsystems. The initial release should implement only the types that support a real decision-making workflow.

---

## 5. Architectural position

```text id="q2k5du"
Portfolio Records and Source Snapshots
                  |
                  v
       Deterministic Analysis
                  |
                  v
       Analysis Objective and Scope
                  |
                  v
       Evidence Package Builder
                  |
                  v
        Privacy / Policy Checks
                  |
                  v
         Provider Abstraction
                  |
                  v
       External AI or Analytical API
                  |
                  v
        Response Validation
                  |
                  v
      Claims and Recommendation Records
                  |
                  v
          Human Review
                  |
                  v
      Explicit Portfolio Decision
```

External analysis should be implemented as a module within Siddhi's modular monolith initially.

The provider interface should be independent of the portfolio domain so that provider-specific request formats, authentication, and response handling do not leak into goal, initiative, evidence, or decision models.

### 5.1 Core components

**Analysis request service**

Creates and validates a request, establishes its objective, and determines the required output format.

**Context builder**

Selects the relevant goals, initiatives, findings, evidence, constraints, and historical decisions.

**Disclosure policy evaluator**

Determines whether the proposed context is permitted to leave the local environment and whether sensitive information must be excluded or redacted.

**Provider adapter**

Handles provider-specific authentication, request construction, execution, timeouts, and response retrieval.

**Response validator**

Checks that the response meets the requested structure and contains the required fields.

**Recommendation processor**

Converts the response into structured advisory records, preserving the distinction between provider claims and source-backed evidence.

**Review and decision workflow**

Allows users to accept, reject, defer, revise, or request further analysis without automatically changing authoritative portfolio records.

---

## 6. Analysis request lifecycle

Every external analysis request must have a stable request ID.

### 6.1 Request metadata

A request should record:

- Request ID.
- Analysis type.
- Objective and decision question.
- Requesting user or authorized process.
- Portfolio scope.
- Selected goal, initiative, and plan revisions.
- Source snapshot IDs.
- Deterministic analysis run IDs.
- Context package version or fingerprint.
- Disclosure policy applied.
- Provider and model identifier, when available.
- Prompt or template version.
- Requested output schema version.
- Creation time.
- Execution status.
- Completion time.
- Response reference.
- Errors, warnings, and limitations.

The record should allow Siddhi to identify what it asked, what context it supplied, and which provider response was used.

### 6.2 Lifecycle states

The workflow should support:

- **Draft:** objective or context is being prepared.
- **Ready for review:** the request has been assembled and awaits any required approval.
- **Queued:** accepted for execution.
- **Running:** submitted to a provider.
- **Succeeded:** a response was received and passed required structural validation.
- **Partially succeeded:** useful output was received, but some expected content or validation was incomplete.
- **Failed:** no usable result was produced.
- **Cancelled:** intentionally stopped where cancellation is supported.
- **Awaiting human review:** output is available but has not been reviewed.
- **Reviewed:** a reviewer recorded an assessment.
- **Closed:** no further action is expected for this request.

A structurally valid response is not necessarily substantively correct. The `Succeeded` state must not imply that the recommendations have been validated or approved.

### 6.3 Repeated requests

If the same analysis is requested again, Siddhi should create a new request or execution record rather than silently replacing the earlier response.

The new request may reuse a previous context package when it is still appropriate, but it must record the reused context and any differences.

---

## 7. Context and evidence package

The context builder is responsible for selecting the minimum useful information required for a particular analysis.

### 7.1 Context selection

Depending on the analysis type, the context may include:

- Goal definitions and intended outcomes.
- Initiative descriptions and portfolio relationships.
- Approved priorities and constraints.
- Current and prior plan revisions.
- Deterministic findings.
- Relevant source evidence and provenance.
- Engineering knowledge from OKF.
- OpenSpec requirements and declared change status.
- Git change summaries.
- Verification results.
- Previous decisions and their recorded rationale.
- Explicit assumptions and unresolved questions.

The context builder must not include all available data merely because it is accessible.

### 7.2 Context manifest

Each context package should have a manifest recording:

- Context package ID.
- Analysis request ID.
- Included portfolio entities.
- Included snapshot IDs.
- Included finding and evidence references.
- Excluded categories where relevant.
- Selection rules.
- Redactions or transformations applied.
- Context creation time.
- Context version or fingerprint.

Where retaining the full context is permitted, Siddhi may store an exact copy. Otherwise, it should retain the manifest, a fingerprint, and sufficient metadata to explain what was supplied without retaining restricted content.

### 7.3 Evidence references

The context should preserve source references wherever possible.

The model should be asked to distinguish between:

- Statements directly supported by supplied evidence.
- Interpretations derived from that evidence.
- Assumptions introduced for analysis.
- New hypotheses requiring investigation.
- Questions that cannot be answered from the supplied context.

A reference included in an AI response is not automatically proof that the referenced source supports the claim. Siddhi should resolve references against the supplied context or authoritative source before treating them as validated support.

### 7.4 Historical context

When an analysis concerns a historical portfolio review, the context builder must use the relevant historical snapshots and plan revisions rather than silently substituting current state.

If historical context is unavailable, the request must state that limitation.

---

## 8. Provider abstraction

### 8.1 Provider interface

The provider interface should support the logical operations needed by Siddhi, such as:

- Validate provider configuration.
- Submit a structured request.
- Retrieve a response.
- Report execution metadata.
- Handle timeout and error conditions.
- Cancel a request when supported.
- Report model and provider identifiers where available.

Not all providers support the same capabilities. The adapter must declare its supported operations.

### 8.2 Provider configuration

A provider configuration should include:

- Provider ID.
- Provider type.
- Endpoint or service configuration.
- Model identifier.
- Authentication reference.
- Request timeout.
- Token or request-size limits where applicable.
- Supported structured-output features.
- Data handling and retention policy.
- Enabled analysis types.
- Retry policy.
- Configuration revision.

Secrets must be stored through an appropriate credential mechanism, not embedded in ordinary configuration files or analysis records.

### 8.3 Provider selection

Provider selection may be based on:

- Approved provider availability.
- Analysis type and required capabilities.
- Data sensitivity and disclosure policy.
- Context size.
- Operational cost limits.
- Latency expectations.
- Required output format.
- Organizational restrictions.

Siddhi must not automatically route sensitive context to an alternative provider merely because the primary provider fails.

Fallback behavior must comply with the same disclosure policy and require explicit authorization where necessary.

### 8.4 Provider independence

The portfolio domain model must not depend on provider-specific response formats.

Provider adapters should translate external request and response formats into Siddhi's internal analysis contract.

The initial implementation should support a small number of approved providers rather than attempt universal compatibility with every model or API.

---

## 9. Structured output contract

External analysis should return structured output wherever the provider supports it.

The exact schema should be versioned and tailored to the analysis type. The following is a logical contract rather than a commitment to a particular JSON schema.

### 9.1 Recommendation record

Each recommendation should support:

- Recommendation ID.
- Summary.
- Proposed action or option.
- Intended outcome.
- Rationale.
- Supporting evidence references.
- Assumptions.
- Risks and trade-offs.
- Dependencies.
- Uncertainty and limitations.
- Expected validation steps.
- Alternatives considered.
- Applicable goals and initiatives.
- Provider request reference.
- Review status.

### 9.2 Claims and supporting evidence

Where possible, the response should distinguish individual claims from recommendations.

A claim should record:

- Claim text.
- Claim category.
- Supporting evidence references.
- Whether support is direct, inferential, or absent.
- Contradictory evidence, if known.
- Additional evidence needed.

The provider must not be allowed to manufacture source identifiers or invent evidence references. References that cannot be resolved must be marked unresolved.

### 9.3 Alternatives

For judgment-intensive tasks, the output should consider alternatives rather than force a single answer.

For example, a strategic investment assessment may compare:

- Build or extend an internal tool.
- Reuse an existing internal capability.
- Adopt an external solution.
- Reduce scope.
- Defer the initiative.
- Gather more evidence before committing.

Not every analysis type requires every alternative. The template should request only options relevant to the question.

### 9.4 Schema validation

Siddhi must validate required fields, field types, enumerated values, and reference formats.

If the response is malformed, Siddhi may request a bounded correction or mark the request as failed. It must not silently convert malformed content into a valid recommendation by guessing missing values.

Schema validation establishes structural conformance only, not factual correctness.

---

## 10. Trust, evaluation, and uncertainty

### 10.1 No automatic trust in generated claims

External AI outputs must be treated as unverified until their claims have been checked to the level required by the intended use.

The provider's self-reported confidence is not a calibrated probability unless a documented and validated calibration method exists.

Siddhi should prefer explicit uncertainty descriptions, evidence gaps, and conditions over unsupported numerical confidence scores.

### 10.2 Claim validation

Siddhi may apply deterministic checks to generated claims, including:

- Does the referenced source record exist?
- Does the referenced snapshot match the request's context?
- Does the quoted or summarized fact appear in the supplied evidence?
- Does the claim conflict with an explicit source field?
- Does the recommendation refer to a valid goal or initiative?
- Does the proposal contradict an approved constraint?
- Does the response include the required alternatives or assumptions?

These checks can identify unsupported or inconsistent claims, but they cannot establish that every strategic interpretation is correct.

### 10.3 Human review

Human review should be required when an output may materially affect:

- Portfolio priorities.
- Investment decisions.
- Resource allocation.
- Approved scope or deadlines.
- Strategic direction.
- Sensitive data handling.
- A consequential commitment or external communication.

The precise review policy may vary by analysis type and impact.

### 10.4 Evaluation over time

Siddhi should evaluate the usefulness of external analysis using observable outcomes such as:

- Percentage of recommendations accepted, rejected, or deferred.
- Frequency of unsupported evidence references.
- Structural validation failure rate.
- Reviewer-reported usefulness.
- Frequency of recommendations requiring substantial correction.
- Cost and latency by analysis type.
- Whether important risks or alternatives were omitted.

Acceptance rates must not be treated as proof of correctness. A frequently accepted recommendation can still be wrong, and a rejected recommendation can still contain useful insights.

---

## 11. Prompt and instruction management

### 11.1 Versioned templates

Analysis templates should be versioned independently from provider configuration.

Each template should define:

- Intended use.
- Required context.
- Expected output schema.
- Constraints and exclusions.
- Required uncertainty handling.
- Evidence citation expectations.
- Required alternatives or trade-offs.
- Known limitations.

The analysis record must identify the template version used.

### 11.2 Untrusted source content

Retrieved source documents, commit messages, requirement descriptions, and other imported text must be treated as untrusted data.

Siddhi must not allow instructions embedded in those sources to override its policies or change the analysis objective.

The context builder should clearly separate system instructions, the user's question, and quoted source material.

### 11.3 Prompt changes

A prompt or template update may change the output even when the input evidence remains unchanged.

Siddhi should retain the template version and support comparisons between outputs produced using different versions where that comparison is useful.

It must not present a changed recommendation as evidence that the portfolio itself changed unless the underlying inputs also changed.

---

## 12. Privacy and disclosure controls

### 12.1 Default to minimum necessary disclosure

Siddhi should not send the complete local portfolio, source repositories, or knowledge collections to an external provider by default.

The context builder should select only the information required for the requested analysis.

### 12.2 Disclosure policy

Before submission, the system should determine whether the context is permitted for the selected provider.

The policy should consider:

- Source confidentiality.
- Private repository content.
- Credentials and secrets.
- Personal or sensitive information.
- Proprietary technical designs.
- Commercially sensitive plans.
- Provider retention and training terms.
- Contractual or organizational restrictions.

If the system cannot determine whether disclosure is permitted, it should block the request or require an explicit authorized decision according to the configured policy.

### 12.3 Redaction

Where appropriate, Siddhi may remove or mask:

- Secrets and access tokens.
- Unnecessary personal identifiers.
- Private URLs or filesystem locations.
- Irrelevant source content.
- Sensitive implementation details not required by the analysis.

Redaction must not silently remove information essential to the validity of the analysis. If a required fact cannot be shared, the request should record the limitation.

### 12.4 Provider retention

Provider data-retention and model-training behavior must be reviewed as part of provider approval.

Siddhi must not assume that a provider is suitable for confidential information merely because it offers an API.

Provider policy and configuration changes should trigger a review of permitted use cases where material.

---

## 13. Execution, retries, and failure handling

### 13.1 Bounded execution

Every external analysis request should have explicit limits for:

- Execution duration.
- Input size.
- Output size.
- Retry count.
- Provider cost or usage, where measurable.
- Maximum number of follow-up correction requests.

These limits should be configurable and proportionate to the analysis type.

### 13.2 Retry rules

Retries should depend on the failure type.

- Temporary network errors may be retried within a configured limit.
- Rate limits should respect provider retry guidance.
- Invalid credentials require correction.
- Policy denials should not be bypassed through automatic provider switching.
- Malformed responses may receive a bounded correction request.
- A timeout with an uncertain provider outcome must not blindly trigger unlimited duplicate submissions.

If a provider supports request idempotency, Siddhi should use it where appropriate.

### 13.3 Failure states

The system should distinguish:

- Request validation failure.
- Disclosure-policy rejection.
- Provider authentication failure.
- Rate limiting.
- Timeout.
- Provider service failure.
- Invalid or malformed response.
- Unsupported response format.
- Context too large.
- Response validation failure.
- Claim-reference resolution failure.
- Human review rejection.

Failure diagnostics must not expose secrets or unnecessary sensitive context.

### 13.4 Partial responses

A partial response may be retained for troubleshooting or reviewed as incomplete when it contains useful material.

It must not be presented as a fully validated recommendation set if required sections are missing.

The request record should identify which output requirements were satisfied and which were not.

---

## 14. Recommendation review and decision workflow

### 14.1 Review states

A recommendation should support states such as:

- Proposed.
- Awaiting review.
- Accepted for further investigation.
- Accepted for planning.
- Rejected.
- Deferred.
- Superseded.
- Withdrawn.

These states describe the recommendation's review lifecycle. They do not themselves approve a portfolio decision.

### 14.2 Explicit approval

If a recommendation is accepted, Siddhi should record what was approved and by whom.

A user may choose to:

- Adopt the recommendation as the basis for a plan revision.
- Create or update an initiative.
- Change a priority.
- Record a new decision.
- Request further analysis.
- Reject the recommendation with a rationale.
- Defer the choice until more evidence is available.

The corresponding domain operation must be explicit. An AI response must never directly invoke these changes without the required authorization and confirmation.

### 14.3 Decision record

An approved decision should reference:

- The original question or objective.
- The relevant analysis request.
- The recommendation or alternatives considered.
- Supporting source snapshots and findings.
- The decision-maker or authorized process.
- Approval time.
- Decision rationale.
- Accepted assumptions and risks.
- Follow-up actions or review conditions.

This preserves the distinction between the recommendation that was proposed and the decision that was actually made.

---

## 15. Historical analysis and traceability

Siddhi should preserve sufficient information to explain why a recommendation was produced and how it was handled.

An analysis record should link to:

- The original request.
- The context package or its permitted representation.
- Source snapshots and portfolio revisions.
- Deterministic analysis runs.
- Provider and model metadata.
- Template version.
- Response and validation results.
- Claim-validation results.
- Human review events.
- Related decisions and follow-up actions.

If the provider's response is not retained in full because of privacy or contractual restrictions, Siddhi should record that limitation and retain permitted metadata sufficient for auditability.

When a new source snapshot or analysis template becomes available, it should not silently replace the evidence or template associated with an earlier recommendation.

---

## 16. Performance and cost controls

The system should monitor:

- Request duration.
- Provider usage or cost where available.
- Input and output size.
- Failure and retry rates.
- Structural validation failures.
- Cost by analysis type.
- Cost by provider and model.
- Frequency of duplicate or unnecessary analyses.

Before submitting a request, Siddhi should reuse existing deterministic results and select a bounded context.

It should not automatically run expensive strategic analysis after every source refresh. A user-triggered request or an explicitly configured workflow is preferable initially.

If scheduled analysis is introduced later, it should run only when there is a clear decision-making benefit and should respect cost, privacy, and rate limits.

---

## 17. Security and operational safeguards

The external analysis capability must:

- Use approved providers and configured credentials.
- Keep credentials outside source code and ordinary analysis records.
- Apply disclosure checks before submission.
- Enforce request and output limits.
- Treat provider responses as untrusted data.
- Validate all identifiers before associating recommendations with portfolio entities.
- Avoid executing provider-generated code or commands.
- Avoid granting providers direct access to Siddhi's database or local filesystem.
- Prevent source content from overriding system policies.
- Record material failures and policy rejections.
- Support disabling a provider without corrupting existing analysis records.
- Preserve decision and review history.
- Keep external analysis optional so provider outages do not prevent routine portfolio management.

---

## 18. Testing requirements

The external analysis capability must be tested for:

1. Correct construction of an analysis request.
2. Correct selection of relevant evidence.
3. Use of historical rather than current snapshots when required.
4. Disclosure-policy enforcement.
5. Secret and sensitive-data redaction.
6. Provider authentication failure.
7. Timeout and rate-limit handling.
8. Bounded retries.
9. Malformed structured output.
10. Missing required output fields.
11. Invented or unresolved evidence references.
12. Conflicting generated claims.
13. Prompt-injection attempts embedded in source content.
14. Oversized context and output.
15. Provider fallback restrictions.
16. Partial response handling.
17. Human review and recommendation lifecycle transitions.
18. Explicit approval before portfolio changes.
19. Historical traceability across template and provider changes.
20. Cost and request limits.
21. Separation of AI recommendations from deterministic findings.
22. Preservation of approved decisions when later analyses disagree.
23. Provider outage without disruption to routine deterministic analysis.
24. Retention and deletion rules for provider inputs and responses.

Tests should include realistic scenarios involving internal tools, commercial initiatives, shared capabilities, conflicting evidence, and incomplete knowledge.

---

## 19. Acceptance criteria

The external analysis capability is ready when:

- Analysis requests have explicit objectives and bounded scope.
- Context packages identify their source snapshots and portfolio revisions.
- Disclosure policies are evaluated before external submission.
- Provider access is isolated behind an adapter interface.
- Analysis templates and output schemas are versioned.
- Structured responses are validated before becoming recommendations.
- Claims and evidence references remain distinguishable.
- Unresolved references and unsupported claims are explicitly reported.
- AI outputs remain advisory and separate from deterministic findings.
- Human approval is required for consequential portfolio changes.
- Recommendations and decisions have distinct lifecycle records.
- Failures and retries are bounded and traceable.
- Provider outages do not disable deterministic analysis.
- Historical records identify the context and template used.
- Sensitive information is not disclosed without authorization.
- Cost and usage can be monitored where the provider exposes the necessary data.
- The system can be tested using a mock provider without calling a real external service.

---

## 20. Implementation phases

### Phase 1 — Analysis contract and mock provider

Implement:

- Analysis request model.
- Context package manifest.
- Provider interface.
- Structured output contract.
- Mock provider.
- Response validation.
- Request and response persistence.

**Deliverable:** Siddhi can exercise the full analysis workflow without external network access.

### Phase 2 — One approved external provider

Implement:

- Provider configuration.
- Credential handling.
- Request submission.
- Bounded execution and retries.
- Provider metadata capture.
- Disclosure checks.

**Deliverable:** Siddhi can perform a controlled external analysis using a single approved provider.

### Phase 3 — Evidence validation and recommendation records

Implement:

- Claim and reference validation.
- Recommendation lifecycle.
- Human review.
- Decision linkage.
- Historical traceability.

**Deliverable:** Recommendations can be reviewed and acted upon without losing the evidence and rationale behind them.

### Phase 4 — Strategic analysis templates

Implement a small set of practical templates, such as:

- Strategic prioritization.
- Internal investment assessment.
- Reuse analysis.
- Minimum useful release.
- Evidence-gap review.

**Deliverable:** Siddhi supports specific portfolio decisions rather than offering an unbounded general-purpose AI chat.

### Phase 5 — Evaluation and additional providers

Add evaluation metrics, provider comparisons, additional approved integrations, and more advanced workflows only where justified by actual use.

**Deliverable:** Siddhi can improve the quality and operational efficiency of its advisory workflows while retaining provider independence.

---

## 21. Open questions

| ID | Question | Why it matters |
|---|---|---|
| EA-001 | Which external AI provider should be supported first? | Determines initial adapter and operational requirements |
| EA-002 | Which analysis types provide the most immediate portfolio value? | Limits initial scope |
| EA-003 | Which information categories are permitted to leave the local environment? | Defines disclosure policy |
| EA-004 | Should exact context packages be retained, or only manifests and fingerprints for restricted data? | Balances traceability and privacy |
| EA-005 | Which recommendations require mandatory human review? | Establishes approval boundaries |
| EA-006 | Should a user be able to compare multiple providers for the same request? | Adds cost and evaluation complexity |
| EA-007 | What usage or cost limits should apply per request and per analysis type? | Controls operating cost |
| EA-008 | Which output schema should be used for each initial analysis type? | Enables reliable validation |
| EA-009 | Should analysis requests be synchronous initially or support background execution? | Determines execution and recovery design |
| EA-010 | What evaluation criteria will determine whether an AI workflow is useful enough to retain? | Prevents adoption based on subjective impressions alone |
| EA-011 | What retention and deletion requirements apply to external provider inputs and responses? | Defines privacy and auditability |
| EA-012 | Should provider selection remain user-controlled or be determined by policy and analysis type? | Balances simplicity, cost, and governance |

---

## 22. Related documentation

- `vision.md`
- `scope-and-roadmap.md`
- `functional-requirements.md`
- `non-functional-requirements.md`
- `system-architecture.md`
- `architectural-decisions.md`
- `domain-model.md`
- `data-ownership.md`
- `data-model.md`
- `application-workflows.md`
- `ingestion-and-snapshots.md`
- `deterministic-analysis.md`
- `scanning-and-evidence.md`
- `security-and-privacy.md`

## 23. Reference material

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — general guidance for managing AI risks, evaluating system behavior, and establishing governance.
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — guidance on generative AI risk management, including governance, testing, content provenance, and oversight.

These are reference frameworks, not mandatory Siddhi implementation specifications. The appropriate controls must be selected according to Siddhi's actual use cases, data sensitivity, and organizational requirements. <Cite refs={["turn827589search2","turn827589search0"]}/>

**Document status:** Draft for review. The initial provider, permitted data scope, output contract, review policy, and first analysis templates must be agreed before converting this document into implementation-level OpenSpec requirements.