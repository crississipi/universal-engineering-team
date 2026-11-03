# Pilot Scenario Design Review

## Review status

- Review type: scenario-design review against repository governance and role requirements.
- Rubric version: `pilot-v2`.
- Outcome: all three scenarios are suitable to submit for human pre-run approval after the clarifications recorded below.
- Human approval: **pending for all three scenarios**.
- Model executions: none performed by this review.
- Evaluation scores or post-run decisions: none created.

This review is advisory. It does not set scenario status to `approved`, create approval metadata, authorize model/provider usage, or substitute for the human approval required by the pilot guide.

## Review basis

Reviewed the three scenario specifications and their referenced canonical role skills, including requirement anchors:

| Scenario | Role | Requirement anchor | Canonical artifact |
|---|---|---|---|
| `SCEN-BACKEND-WEBHOOK-VALIDATION` | `backend-developer` | `REQ-BACKEND-01` | `ART-BACKEND` |
| `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW` | `penetration-tester` | `REQ-APPSEC-01` | `ART-SECURITY-ASSESSMENT` |
| `SCEN-DELIVERY-CROSSROLE-WEBHOOK` | `delivery-lead` | `REQ-DELIVERY-01` | `ART-DELIVERY-RECORD` |

The review also checked the role activation rules, ownership declarations, responsibility boundaries, shared execution protocol, evaluation methodology, and pilot run-record template.

## Scenario findings

### 1. Backend Developer — bounded webhook validation

**Design assessment: ready for human approval.**

Strengths:
- Pure, framework-independent implementation with an explicit prohibition on network, persistence, logging, and unrelated abstractions.
- Meaningful numeric safety requirements, including bool rejection, Decimal normalization, and non-finite value rejection.
- Explicit tests and evidence-reporting expectations.
- Direct traceability to the Backend Developer skill's `REQ-BACKEND-01` requirement.

Clarifications applied in `pilot-v2`:
- Defined the intentionally basic email shape rather than leaving “valid basic email” to reviewer interpretation. It is not represented as full RFC validation.
- Defined accepted `unit_price` input types, bool rejection, Decimal conversion behavior for float inputs, and the no-rounding/no-quantization boundary.
- Expanded required test cases to include malformed and unsupported price types, bool price, non-mapping items, and missing item fields.

Remaining limitation:
- The task intentionally defines a small validation boundary, not production-grade provider authentication, schema governance, or persistence behavior. Reviewers must not penalize the agent for omitting excluded features.

### 2. Penetration Tester — static webhook security assessment

**Design assessment: ready for human approval.**

Strengths:
- Explicitly documentation-only; no live target, authorization, traffic, scanning, exploitation, or active testing is implied.
- The fictional handler and supplied context provide enough evidence to identify likely security concerns without asserting unknown controls are absent.
- Requires evidence-based distinction between confirmed observations and risks dependent on unknown database/upstream controls.
- Covers signature verification, duplicate/replay behavior, validation, sensitive-data logging, error handling, remediation, and limitations.
- Direct traceability to the Penetration Tester skill's `REQ-APPSEC-01` requirement.

Clarifications applied in `pilot-v2`:
- Added unique finding IDs and a shared Critical/High/Medium/Low/Informational severity vocabulary with proportionality guidance.
- Requires each severity rating to be justified from static evidence and prerequisites; it must not imply exploitability was validated.

Safety boundary:
- This scenario must remain static-only for every run. Do not add a live endpoint, target URL, exploit execution, or active testing requirement without a separately authorized scenario and scope.

### 3. Delivery Lead — cross-role webhook delivery plan

**Design assessment: ready for human approval after the output clarifications in `pilot-v2`.**

Strengths:
- Combines external integration, persistence, backend behavior, an operational UI, verification, and documentation, which appropriately exercises cross-role coordination.
- Explicitly identifies missing provider signature/retry details and unresolved UI filters/retention.
- States that production deployment is not authorized and no formal handoff contract exists.
- Direct traceability to the Delivery Lead skill's `REQ-DELIVERY-01` requirement.

Clarifications applied in `pilot-v2`:
- Requires a role-activation matrix covering the 17 canonical role IDs, using only the four governed classifications and explaining task-specific triggers.
- Requires every workstream to map to an existing artifact ID and its single canonical owner; ownership gaps must be raised rather than filled with invented artifacts or co-owners.
- Defines the required delivery-ledger fields and requires actual lifecycle vocabulary.
- Separates a proposed plan from execution evidence and explicitly prohibits claims of implementation, verification, approval, handoff, deployment, or release.

Remaining limitation:
- This is a planning/orchestration exercise. It does not test actual cross-agent handoff execution, persistent execution records, or a production delivery.

## Rubric integrity

- Criterion IDs and weights remain intact within each scenario.
- Scenario-specific criterion wording was clarified where necessary for consistent scoring.
- The rubric version was advanced from `pilot-v1` to `pilot-v2` in all three scenarios and the run-record template.
- The pilot guide now defines common score anchors:
  - 0: absent or directly contradicted.
  - 25: major omissions or unsafe handling.
  - 50: partial completion with material gaps.
  - 75: substantially meets the criterion with limited omissions.
  - 100: fully meets the criterion with clear evidence.
  - Intermediate scores require a specific evidence-based explanation.
- Critical failures must continue to be reported separately from weighted averages.

## Human approval checklist

A human reviewer must independently decide whether each scenario is representative and approve it. For each scenario:

1. Read the complete prompt, criteria, and corresponding role skill.
2. Confirm that the scope and exclusions are appropriate for the intended pilot.
3. Confirm that the criteria can be scored from observable output and evidence.
4. Confirm that the `pilot-v2` wording and score anchors are acceptable.
5. If approved, set that scenario's `status` to `approved` and record the real reviewer identity and UTC approval timestamp in `approval.approved_by` and `approval.approved_at`.
6. If changes are needed, keep it in `draft` and record the requested changes through the normal repository review process.

Do not copy placeholder identities or timestamps. Do not approve all three automatically as a batch if the reviewer has not reviewed each scenario individually.

## Execution gate

After the human approvals are recorded and scenario validation passes:

- Run each approved scenario three times, for nine total executions.
- Use the exact approved prompt and `pilot-v2` rubric.
- Record the exact provider, model/version, relevant settings, skill revision, scenario revision, prompt hash, transcript/output references, and UTC timestamp.
- Preserve evidence and redact secrets and unnecessary sensitive data.
- Do not create placeholder run records or post-run reviews.
- Create the post-run review only after the three actual runs for that scenario have been reviewed.

At the time of this review, no pilot model executions, scores, or post-run decisions are claimed.
