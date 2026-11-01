# Handoff Acceptance, Rejection, and Resubmission Rules

## Purpose

This document defines how a receiving role evaluates a submitted handoff,
records its decision, requests corrections, and confirms completion.

The canonical handoff contract definitions are maintained in:

`docs/team/ownership.yml`

The contract structure is defined in:

`docs/team/handoff-contract-schema.md`

Candidate producer-consumer relationships are documented in:

`docs/team/producer-consumer-matrix.md`

This document governs the evaluation of an individual handoff execution.
It does not create or approve formal handoff contracts.

## 1. Governing principles

1. Evaluate a submission against the approved handoff contract and its
   version applicable to that submission.
2. Acceptance decisions must be based on observable evidence.
3. The consumer must not introduce new requirements during evaluation.
4. Every failed check must identify the unmet requirement and explain
   the correction needed.
5. A blocked handoff is not automatically a rejected handoff.
6. Partial acceptance is permitted only when accepted outputs are
   independently usable and safe to consume.
7. The producer remains accountable for correcting its submitted outputs.
8. The consumer remains accountable for its acceptance decision.
9. Acceptance does not transfer ownership of either artifact package.
10. A handoff decision must not be recorded as verified unless the
    applicable checks were actually performed.

## 2. Evaluation baseline

The consumer evaluates the submission against:

- The handoff contract ID.
- The contract version applicable to the submission.
- The producer and consumer roles.
- The producer and consumer artifact packages.
- The declared relationship type.
- The required outputs.
- The required context.
- The acceptance checks.
- Any activation condition that applies.

The contract version must be recorded with the handoff execution.

A later contract change must not silently change the evaluation criteria
for a submission already made under an earlier version.

If the contract is ambiguous, contradictory, or materially incomplete,
the consumer must request clarification rather than inventing a new
acceptance requirement.

A material contract change must be reviewed through the appropriate
contract-maintenance process. It must not be applied retroactively
without explicit agreement.

## 3. Acceptance-check results

Each acceptance check must receive one of the following results.

### `passed`

The check is satisfied.

The consumer records enough evidence to explain how the check was verified.

### `failed`

The check is not satisfied.

The consumer records:

- The acceptance check that failed.
- The observed condition.
- The relevant evidence or reproduction details.
- The correction required.

A failure must be tied to the approved contract, not personal preference.

### `not_applicable`

The check does not apply to the current handoff execution.

The consumer records why it does not apply.

A check must not be marked `not_applicable` merely because it is difficult
to verify or because the expected output is missing.

### `not_verified`

The consumer cannot establish whether the check passed or failed.

Examples include:

- Required evidence is unavailable.
- A dependency needed for verification is unavailable.
- The submitted material cannot be inspected in the current environment.
- The check requires access that has not been provided.

The consumer must explain what is preventing verification.

A required check left `not_verified` prevents full acceptance.

## 4. Overall handoff decisions

The consumer records one overall decision.

### `accepted`

Use when:

- Every required output has been provided.
- All applicable acceptance checks have passed.
- Any `not_applicable` check has a documented justification.
- No unresolved issue prevents the consumer from safely using the output.

The consumer records the acceptance evidence and the decision.

### `partially_accepted`

Use when:

- Some outputs have passed their applicable checks.
- Other outputs remain failed, not verified, or unresolved.
- The accepted outputs can be used independently.
- Partial use does not create an unsafe, inconsistent, or misleading result.

The consumer must identify:

- Accepted outputs.
- Outstanding outputs.
- Failed or unverified checks.
- Any restrictions on using the accepted portion.
- The remaining action and accountable producer.

Partial acceptance does not mean the entire handoff is complete.

The unresolved portion remains open until accepted, explicitly withdrawn,
or otherwise resolved through an approved decision.

### `rejected`

Use when one or more required outputs or acceptance checks fail and
the submitted handoff cannot be accepted as delivered.

The rejection must identify:

- The failed output or acceptance check.
- The applicable contract requirement.
- Evidence supporting the finding.
- The required correction.
- Whether the issue affects the entire submission or only a specific part.

A rejection must not be used to enforce requirements absent from
the applicable contract.

### `blocked`

Use when a fair acceptance decision cannot be made because of a
dependency, ambiguity, unavailable evidence, access limitation,
or another issue outside the consumer's ability to resolve directly.

The consumer records:

- The reason evaluation is blocked.
- The affected outputs or checks.
- What information, decision, access, or dependency is needed.
- The role or party expected to provide it, if known.
- Whether any independent portion can still be evaluated.

A blocked decision does not establish that the producer's output is defective.

## 5. Standard rejection reasons

Use one or more of these reason codes when rejecting a submission.

| Reason code | Meaning |
|---|---|
| `missing_output` | A required output was not submitted. |
| `incomplete_output` | A submitted output is missing required content or coverage. |
| `failed_acceptance_check` | A defined acceptance check was performed and failed. |
| `invalid_or_inconsistent_output` | The output is malformed, contradictory, or inconsistent with its declared contract. |
| `missing_required_context` | Required context needed to interpret or use the output was omitted. |
| `unsupported_claim` | A claim or verification statement is not supported by the submitted evidence. |
| `unsafe_or_prohibited_content` | The submission contains a security, privacy, safety, or policy issue that prevents safe consumption. |
| `scope_mismatch` | The submitted output does not correspond to the agreed handoff scope. |

The reason code is a classification, not a substitute for an explanation.

Every rejection must include a concise description and supporting evidence.

If the actual issue is an unclear or contradictory contract, use
`blocked` and request contract clarification instead of assigning
an unsupported rejection reason.

## 6. Resubmission procedure

When a handoff is rejected or partially accepted:

1. The consumer records the decision and required corrections.
2. The producer reviews the failed checks and supporting evidence.
3. The producer corrects the affected outputs within its ownership boundary.
4. The producer submits a new revision and identifies what changed.
5. The producer identifies which rejection findings or outstanding
   checks each change addresses.
6. The consumer evaluates the new revision against the applicable
   contract version.
7. The consumer records the new decision and evidence.

A resubmission must preserve the relationship to the original handoff
execution and its previous decisions.

Do not overwrite or erase earlier submissions and decisions.

The producer must not claim that a failed check has passed unless
the correction has been verified.

The consumer should reassess affected checks and any other checks
whose result may have changed because of the correction.

Unchanged, previously accepted outputs do not need to be re-evaluated
unless the new submission affects their validity or consistency.

## 7. Partial acceptance rules

Partial acceptance is allowed only when all of the following are true:

1. The handoff contains separable outputs or independently assessable
   portions.
2. The accepted portion satisfies its applicable acceptance checks.
3. The accepted portion can be used without relying on unresolved outputs.
4. The accepted portion does not create an unsafe, inconsistent,
   or misleading downstream result.
5. The consumer documents the exact accepted and outstanding portions.

Do not partially accept:

- A tightly coupled output whose components must work together.
- A security-sensitive output when unresolved issues make partial use unsafe.
- An output whose correctness depends on an unresolved prerequisite.
- A result whose partial use would violate an explicit contract condition.

When partial acceptance is not safe, use `rejected` or `blocked`,
as supported by the actual evidence.

Partial acceptance must not be used to hide unresolved mandatory work.

## 8. Feedback and conditional handoffs

The relationship type affects how the consumer interprets the decision.

### `required_input`

The consumer needs the accepted output before completing the dependent
work.

A rejected or blocked required input prevents completion of the work
that depends on it.

Unrelated work may continue when it does not rely on the unavailable output.

### `conditional_input`

The contract applies only when its activation condition is satisfied.

If the condition does not apply, the handoff is not required for that
project scope.

Record the reason for non-activation in the relevant project or delivery
coordination record when needed.

### `feedback`

Feedback communicates findings, recommendations, or verification results.

The receiving role evaluates the feedback and determines the appropriate
action within its own responsibility boundary.

Feedback does not automatically block the receiving package from starting
or completing.

It becomes a completion or release condition only when an approved
requirement, risk decision, or acceptance criterion makes it one.

## 9. Acceptance authority and responsibility

The accountable owner of the consumer package is responsible for the
handoff acceptance decision.

The consumer may request relevant specialist input when a check falls
outside its expertise.

Specialist input supports the decision but does not silently transfer
the consumer's accountability.

The producer may provide clarification and evidence but must not
self-approve its own handoff.

The Delivery Lead coordinates unresolved delivery impact and blockers.
The Delivery Lead does not override specialist acceptance findings
or assume ownership of specialist outputs.

No additional mandatory reviewer role is created by this procedure.

## 10. Completion criteria

An individual handoff execution is complete when:

- Its overall decision is `accepted`; or
- Its accepted and unresolved portions have been explicitly resolved
  through an approved process.

A `partially_accepted`, `rejected`, or `blocked` execution is not
fully accepted.

A handoff must not be marked complete solely because:

- A file was uploaded.
- A message was sent.
- The producer says the work is finished.
- The consumer has not responded.
- A deadline has passed.

Absence of a response is not acceptance.

## 11. Execution evidence

An execution record should capture:

- Handoff contract ID and version.
- Project, task, or change identifier.
- Producer submission reference and revision.
- Submission timestamp.
- Acceptance-check results.
- Overall decision.
- Rejection reason codes, when applicable.
- Evidence and correction requests.
- Resubmission references.
- Outstanding blockers and next actions.
- Decision timestamp and accountable consumer role.

Store evidence references rather than copying secrets or sensitive
material into the handoff record.

The repository location and technical format for execution records
will be established separately if required.

## 12. Relationship to escalation

This document defines acceptance and correction behavior.

It does not define:

- Response deadlines.
- Escalation time limits.
- Retry or resubmission limits.
- Conflict-resolution authority beyond existing role boundaries.
- Timeout behavior.
- Deadlock resolution.

These topics are addressed in Phase 1.2.5.

Until then, unresolved issues must be recorded and coordinated rather
than silently treated as accepted or rejected.

## 13. Maintenance

Update this document when acceptance, rejection, or resubmission
behavior changes.

When a contract's acceptance checks change:

1. Review the affected producer and consumer responsibilities.
2. Update the handoff contract and its version where required.
3. Confirm the new checks are observable and evidence-based.
4. Review affected downstream consumers.
5. Update relevant documentation.
6. Run the applicable repository validators.

Never introduce new acceptance requirements through an execution
decision alone.