# Completion, Verification, and Closure Records

## 1. Purpose

This document defines the canonical execution closure record used to establish whether an execution has completed its planned work, whether the resulting outputs have been adequately verified, and whether the execution is formally authorized to close.

The closure record provides a traceable summary of the final state of an execution. It links completion and verification conclusions to the canonical work items, role activations, dependencies, handoff executions, decisions, evidence, blockers, replanning records, and release records where applicable.

This specification defines the record structure, lifecycle, closure requirements, authority boundaries, exception handling, history requirements, and future validation expectations.

It does not define or replace:

- Workflow stages and lifecycle rules in `workflow-lifecycle.md`.
- Work-item states and role activation rules in `role-activation-and-work-item-records.md`.
- Dependency states and execution rules in `dependency-execution-records.md`.
- Handoff contract requirements in `handoff-acceptance-rules.md`.
- Handoff execution states in `handoff-execution-records.md`.
- Decision authority and decision lifecycle in `decision-records.md`.
- Evidence provenance and verification states in `evidence-records.md`.
- Blocker lifecycle and resolution rules in `blocker-records.md`.
- Replanning approval and implementation rules in `replanning-records.md`.
- Release responsibilities and release readiness requirements in the applicable release governance documentation.

The existing governance documents remain authoritative for their respective subjects. This document defines how their records are evaluated and referenced when an execution is prepared for closure.

## 2. Core Principles

### 2.1 Completion, verification, and closure are separate conclusions

These concepts must remain distinct:

- **Completion** answers: Has the execution's approved work been completed, or have remaining items been formally cancelled or excluded through authorized decisions?
- **Verification** answers: Has the completed work been checked against its applicable acceptance criteria, with sufficient evidence and no unaccepted verification failures?
- **Closure** answers: Have all required closure conditions been evaluated and has an authorized decision formally closed the execution?

Completion must not be inferred solely from work-item status counts.

Verification must not be inferred solely from completion status, the existence of evidence records, or an approval statement.

Closure must not be inferred solely from completion or verification. It requires an explicit closure decision and a corresponding closure record state.

### 2.2 One canonical closure record per execution

Each execution has one canonical closure record in:

`executions/<execution-id>/closure.yml`

The record ID uses:

`CLS-<UUID>`

A closure record belongs to exactly one execution and must reference the same `execution_id` as the execution root record.

Do not create multiple competing closure records for the same execution. Revisions, review attempts, corrections, and closure decisions must be retained in the same record's history.

### 2.3 Canonical records remain authoritative

The closure record summarizes and references the state of other records. It does not replace or duplicate them.

For example:

- Work-item completion is established by the canonical work-item records.
- Dependency satisfaction is established by dependency records.
- Handoff acceptance is established by handoff execution and decision records.
- Blocker resolution is established by blocker records.
- Verification is supported by evidence records and applicable acceptance criteria.
- Approval is established by the canonical decision record.
- Release completion is established by the applicable release records.

The closure record must not silently change the state of another record.

### 2.4 No fabricated completion or verification claims

Only actual, traceable execution data may support closure conclusions.

Do not invent:

- Completed work items.
- Passed tests or verification checks.
- Evidence references.
- Handoff acceptance.
- Dependency satisfaction.
- Blocker resolution.
- Approvals or decisions.
- Release completion.
- Dates, reviewers, or responsible roles.

If information has not been verified, record it as `not_verified`, `not_started`, or the appropriate unresolved state. Do not convert missing information into a successful result.

### 2.5 Exceptions require explicit authorization

A remaining item may be accepted as an exception only when:

1. The exception is explicitly documented.
2. Its impact and residual risk are described.
3. An authorized decision approves the exception.
4. The affected records are referenced.
5. Any required follow-up action is recorded.

An exception does not automatically make a failed check pass. It documents an authorized acceptance of a known deviation or outstanding condition.

### 2.6 Closure is terminal

Once an execution is formally closed, it must not be reopened or have its completed execution scope silently changed.

If additional work is required after closure, create a new change and execution under the existing project, following the execution identity and traceability rules.

A closed execution may be referenced by a later execution for historical context, corrective work, or follow-up. It remains closed.

## 3. Record Location and Identity

### 3.1 Canonical location

Each execution stores its closure record at:

`executions/<execution-id>/closure.yml`

The record is part of the execution directory alongside:

- `execution.yml`
- `work-items.yml`
- `role-activations.yml`
- `dependencies.yml`
- `handoff-executions.yml`
- `decisions.yml`
- `evidence.yml`
- `blockers.yml`
- `replans.yml`

### 3.2 Record identity

The closure record uses:

`CLS-<UUID>`

The `execution_id` must match the execution root record.

The closure record must not be copied into another execution and reused as though it belonged to that execution. A new execution requires its own closure record and identity.

### 3.3 One record, multiple review attempts

A closure review may be attempted more than once.

For example:

1. Closure preparation begins.
2. A review identifies unresolved dependencies.
3. The closure record is returned to preparation.
4. The dependencies are resolved.
5. Verification is completed.
6. A new closure review is performed.
7. An authorized decision approves closure.

These attempts remain part of the same closure record and its history. They must not be represented as multiple independent closure records.

## 4. Canonical Record Structure

The following is the canonical conceptual structure for `closure.yml`. It is a specification example, not an actual execution record.

```yaml
closure:
  closure_id: "CLS-<UUID>"
  execution_id: "EXE-<UUID>"

  completion:
    status: "incomplete"
    summary: ""
    completed_work_item_ids: []
    cancelled_work_item_ids: []
    outstanding_work_item_ids: []
    completion_evidence_refs: []

  verification:
    status: "not_started"
    summary: ""
    verification_scope: ""
    verified_work_item_ids: []
    failed_work_item_ids: []
    not_verified_work_item_ids: []
    evidence_refs: []

  closure_status: "not_started"

  closure_checks: []

  exceptions: []

  required_record_refs:
    role_activation_ids: []
    work_item_ids: []
    dependency_ids: []
    handoff_execution_ids: []
    decision_ids: []
    evidence_ids: []
    blocker_ids: []
    replan_ids: []
    release_record_refs: []

  closure_summary: ""
  residual_risks: []
  follow_up_references: []

  created_at: ""
  updated_at: ""
  # proposed_at, reviewed_at, and closed_at are omitted until applicable.

  history: []
```

The fields and nested structures are defined in the following sections. Optional and conditional fields must be omitted when they do not apply or are not yet known; YAML `null` is not a substitute for omission. Required fields must not be omitted from an actual record. The example is illustrative and its empty strings are placeholders, not acceptable values for required non-empty text fields.

## 5. Field Definitions

### 5.1 Top-level identity fields

| Field | Requirement | Description |
|---|---|---|
| `closure_id` | Required | Unique closure record ID using `CLS-<UUID>`. |
| `execution_id` | Required | Canonical execution ID to which the closure record belongs. |
| `closure_status` | Required | Current closure lifecycle status. |
| `created_at` | Required | Timestamp when the closure record was created. |
| `updated_at` | Required | Timestamp of the most recent record update. |
| `history` | Required | Append-only history of material closure record changes. |

### 5.2 Completion object

The `completion` object describes whether the approved execution work has been completed.

| Field | Requirement | Description |
|---|---|---|
| `status` | Required | Completion conclusion. |
| `summary` | Required | Concise explanation of the completion conclusion. |
| `completed_work_item_ids` | Required | Work items whose canonical state is `completed`. |
| `cancelled_work_item_ids` | Required | Work items whose canonical state is `cancelled`. |
| `outstanding_work_item_ids` | Required | Work items that are not completed or cancelled. |
| `completion_evidence_refs` | Optional | Evidence references supporting the completion conclusion. |

Allowed completion statuses:

- `incomplete`
- `complete`
- `complete_with_exceptions`

Definitions:

- `incomplete`: At least one in-scope work item remains unfinished, or the completion assessment is not sufficiently established.
- `complete`: All approved in-scope work has been completed, with no outstanding work requiring an exception.
- `complete_with_exceptions`: The planned work is complete for closure purposes, but one or more explicitly documented and authorized exceptions remain.

Rules:

1. A work item may appear in `completed_work_item_ids` only when its canonical work-item state is `completed`.
2. A work item may appear in `cancelled_work_item_ids` only when its canonical state is `cancelled`.
3. A work item must not appear in more than one of the three work-item lists.
4. Every in-scope work item must be accounted for.
5. Work items in `not_started`, `ready`, `in_progress`, `blocked`, `in_review`, or `changes_requested` are outstanding.
6. Outstanding work items prevent ordinary completion.
7. Outstanding work must not be silently omitted from the completion assessment.
8. A cancelled work item requires the applicable authorized decision or other approval required by existing governance.
9. Work added or changed by an approved replanning record must be included in the completion assessment.
10. Work explicitly excluded from scope must have a traceable approved decision or applicable scope record. Do not treat unapproved scope removal as completion.
11. A `complete_with_exceptions` conclusion requires each exception to be recorded in the `exceptions` collection and approved through a canonical decision record.
12. Completion status must not be set to `complete` merely because all work-item records currently present are completed. The approved scope and replanning history must also be checked.

### 5.3 Verification object

The `verification` object describes whether the completed work has been checked against applicable requirements and acceptance criteria.

| Field | Requirement | Description |
|---|---|---|
| `status` | Required | Overall verification conclusion. |
| `summary` | Required | Explanation of verification coverage and result. |
| `verification_scope` | Required | Description of what was verified and the applicable boundaries. |
| `verified_work_item_ids` | Required | Work items with sufficient successful verification evidence. |
| `failed_work_item_ids` | Required | Work items with one or more unresolved failed verification results. |
| `not_verified_work_item_ids` | Required | Work items for which verification is incomplete or insufficient. |
| `evidence_refs` | Required | Evidence record IDs supporting the verification assessment. |

Allowed verification statuses:

- `not_started`
- `in_progress`
- `passed`
- `passed_with_exceptions`
- `failed`

Definitions:

- `not_started`: Verification has not begun.
- `in_progress`: Verification is underway but is not complete.
- `passed`: Applicable verification requirements have passed and are supported by sufficient evidence.
- `passed_with_exceptions`: Verification is sufficiently complete for closure, but explicitly documented and authorized verification exceptions remain.
- `failed`: One or more required verification conditions have failed or cannot be accepted.

Rules:

1. Verification must be based on applicable requirements, acceptance criteria, and approved scope.
2. Each verification conclusion must be supported by traceable evidence where evidence is applicable.
3. Evidence references must point to canonical evidence records in the same execution unless an explicitly permitted external reference is used through the evidence record.
4. Evidence must not be treated as verified merely because a file, log, screenshot, or report exists.
5. The evidence record's verification status and provenance requirements remain authoritative.
6. Invalid or superseded evidence must not be used as the sole support for a successful verification conclusion.
7. `verified_work_item_ids`, `failed_work_item_ids`, and `not_verified_work_item_ids` must not overlap.
8. Every completed in-scope work item requiring verification must be accounted for.
9. A work item may be classified as verified only when its applicable acceptance criteria have sufficient supporting evidence.
10. A work item with an unresolved required verification failure belongs in `failed_work_item_ids`.
11. A work item with missing, incomplete, or inconclusive verification belongs in `not_verified_work_item_ids`.
12. A verification failure must not be relabeled as an exception merely to make closure possible. An authorized decision must explicitly accept the residual condition, its impact, and the risk.
13. `passed_with_exceptions` requires documented exceptions and their corresponding approved decisions.
14. `passed` requires no outstanding required verification failures or unverified items.
15. If a work item does not require a separate verification activity, the reason and applicable acceptance basis must be documented. Do not infer that verification is unnecessary.
16. Verification status must not be derived from the number of evidence records alone.

### 5.4 Closure checks

The `closure_checks` collection records the evaluation of closure readiness conditions.

Each check uses the following structure:

```yaml
closure_checks:
  - check_id: "CHK-<stable-identifier>"
    category: "work_item_completion"
    description: ""
    result: "not_verified"
    related_record_refs: []
    evidence_refs: []
    notes: ""
```

Fields:

| Field | Requirement | Description |
|---|---|---|
| `check_id` | Required | Stable identifier unique within the closure record. |
| `category` | Required | Closure condition category. |
| `description` | Required | Specific condition being evaluated. |
| `result` | Required | Result of the closure check. |
| `related_record_refs` | Required | Canonical records relevant to the check. |
| `evidence_refs` | Required | Evidence supporting the check result, when applicable. |
| `notes` | Required | Explanation, including why a check is not applicable or not verified. |
| `checked_by_role` | Conditional | Role responsible for performing the check. |
| `checked_at` | Conditional | Timestamp when the check was performed. |

Allowed check results:

- `passed`
- `failed`
- `not_applicable`
- `not_verified`

Allowed categories:

- `scope_accounting`
- `role_activation_completion`
- `work_item_completion`
- `dependency_resolution`
- `handoff_resolution`
- `decision_resolution`
- `evidence_completeness`
- `verification_completion`
- `blocker_resolution`
- `replanning_completion`
- `release_readiness`
- `release_completion`
- `documentation_completion`
- `security_requirements`
- `quality_requirements`
- `operational_readiness`
- `accessibility_requirements`
- `delivery_requirements`
- `other`

Rules:

1. Every check must evaluate a specific closure condition.
2. A check must not be marked `passed` without a defensible basis.
3. A check may be `not_applicable` only when the condition genuinely does not apply to the execution.
4. The reason for `not_applicable` must be documented.
5. A required check marked `failed` or `not_verified` prevents closure unless the underlying condition is resolved or explicitly accepted through an authorized exception.
6. A non-applicable check must not be used to conceal missing work or missing evidence.
7. `checked_by_role` identifies the role that performed the check; it does not automatically grant approval authority.
8. Closure checks supplement the canonical record states. They do not replace them.
9. The set of checks must cover all applicable closure requirements for the execution.
10. Repeated review attempts must be represented in history. The current check result must reflect the latest valid assessment.

### 5.5 Exceptions

The `exceptions` collection documents unresolved conditions that are explicitly accepted for closure.

Each exception uses the following structure:

```yaml
exceptions:
  - exception_id: "EXC-<stable-identifier>"
    category: "verification"
    description: ""
    reason: ""
    impact_summary: ""
    residual_risk: ""
    affected_record_refs: []
    evidence_refs: []
    accepted_by_decision_id: "DEC-<UUID>"
    follow_up_references: []
    status: "approved"
```

Fields:

| Field | Requirement | Description |
|---|---|---|
| `exception_id` | Required | Stable identifier unique within the closure record. |
| `category` | Required | Type of exception. |
| `description` | Required | Condition being accepted. |
| `reason` | Required | Why the condition remains unresolved or deviates from the expected state. |
| `impact_summary` | Required | Known impact on scope, quality, security, operations, delivery, or users. |
| `residual_risk` | Required | Risk remaining after the exception is accepted. |
| `affected_record_refs` | Required | Records affected by the exception. |
| `evidence_refs` | Required | Evidence supporting the exception assessment, when available. |
| `accepted_by_decision_id` | Required | Canonical approved decision authorizing acceptance. |
| `responsible_role` | Conditional | Role accountable for any follow-up responsibility. |
| `follow_up_references` | Required | References to follow-up work, decisions, risks, or later executions. |
| `status` | Required | Exception approval status. |

Allowed exception categories:

- `scope_deviation`
- `incomplete_work`
- `verification_gap`
- `verification_failure`
- `dependency_exception`
- `handoff_exception`
- `blocker_exception`
- `documentation_gap`
- `security_risk`
- `quality_risk`
- `operational_risk`
- `release_exception`
- `external_constraint`
- `other`

Allowed exception statuses:

- `proposed`
- `approved`
- `rejected`
- `withdrawn`

Rules:

1. Every exception must have a unique ID within the closure record.
2. Every approved exception must reference a canonical decision record.
3. The referenced decision must belong to the same execution and have an approved status.
4. The decision must explicitly authorize the specific exception being recorded.
5. The decision authority must be valid under existing governance.
6. A proposed, rejected, or withdrawn exception does not authorize closure.
7. A general approval must not be interpreted as acceptance of unrelated exceptions.
8. The exception must describe the actual residual condition and its impact.
9. Security, privacy, safety, legal, or other prohibited conditions cannot be made acceptable merely by recording an exception. Existing safety and policy restrictions remain controlling.
10. Any mandatory control or requirement that cannot be waived under applicable governance must remain a closure blocker.
11. Follow-up work must be traceable. If it will be performed after closure, identify the responsible role and the later change, execution, or approved tracking record when available.
12. An exception must not silently modify a work-item, dependency, handoff, or blocker record.
13. A `complete_with_exceptions` completion status requires at least one approved exception relevant to completion.
14. A `passed_with_exceptions` verification status requires at least one approved exception relevant to verification.
15. An exception does not change a failed closure check to `passed`. The check result must accurately describe the condition; the exception records its authorized acceptance.

### 5.6 Required record references

The `required_record_refs` object provides an index of the canonical records considered during closure.

| Field | Requirement | Description |
|---|---|---|
| `role_activation_ids` | Required | Role activation records considered for closure. |
| `work_item_ids` | Required | Work-item records included in the approved execution scope. |
| `dependency_ids` | Required | Dependency records evaluated for closure. |
| `handoff_execution_ids` | Required | Handoff execution records evaluated for closure. |
| `decision_ids` | Required | Decision records relevant to completion, verification, exceptions, and closure. |
| `evidence_ids` | Required | Evidence records considered in completion and verification. |
| `blocker_ids` | Required | Blocker records considered for closure. |
| `replan_ids` | Required | Replanning records considered for closure. |
| `release_record_refs` | Required | Applicable release record references; an empty list is valid when release is not applicable. |

Rules:

1. References must use canonical record IDs or the repository's approved external-reference format.
2. References must resolve to actual records.
3. Execution-scoped records must belong to the same execution.
4. Artifact package IDs must resolve through the canonical ownership catalog, not be treated as execution-scoped record IDs.
5. The reference lists must account for all relevant records, including records created through approved replanning.
6. A record must not be omitted merely because its state is inconvenient for closure.
7. An empty list is valid only when there are genuinely no applicable records of that type.
8. These lists are indexes, not substitutes for evaluating the referenced records.
9. `release_record_refs` may be empty when release is not applicable. The reason must be documented in the release readiness check or closure summary.
10. If a release is applicable, the relevant release records must be included and evaluated.

### 5.7 Closure decision and authority fields

| Field | Requirement | Description |
|---|---|---|
| `closure_decision_id` | Required before closure approval | Canonical decision record authorizing or rejecting execution closure. |
| `proposed_by_role` | Conditional | Role that proposed closure. |
| `coordinated_by_role` | Conditional | Role coordinating the closure process. |
| `closure_authorized_by_role` | Conditional | Role exercising the applicable closure authority. |

Rules:

1. Closure approval must be recorded in `decisions.yml`.
2. The closure record must reference that decision using `closure_decision_id`.
3. The decision must belong to the same execution.
4. The decision must use the `execution_closure` decision type.
5. The decision must have an approved status for closure to proceed.
6. The decision must explicitly identify the execution and the closure outcome it authorizes.
7. The decision's proposer and decider must follow the authority rules in `decision-records.md`.
8. A role that prepares or coordinates closure does not automatically have authority to approve it.
9. The Delivery Lead may coordinate closure but is not automatically the universal closure approver.
10. The applicable approval authority must be determined from the existing responsibility and decision governance.
11. The producer of a deliverable must not self-approve its own handoff acceptance. Existing handoff acceptance rules remain in force.
12. Closure approval does not override unresolved mandatory security, safety, privacy, or policy restrictions.

### 5.8 Closure summary and follow-up fields

| Field | Requirement | Description |
|---|---|---|
| `closure_summary` | Required | Final concise account of execution completion, verification, closure outcome, and material exceptions. |
| `residual_risks` | Required | Risks remaining at closure, or an empty list when none remain. |
| `follow_up_references` | Required | References to approved follow-up work, later executions, or other tracking records. |

Rules:

1. The closure summary must accurately reflect the canonical record states.
2. Residual risks must not be omitted because an exception was approved.
3. Follow-up references must be traceable.
4. An empty follow-up list is valid when no follow-up is required.
5. Follow-up work does not keep the current execution open when it has been explicitly approved for a later execution or tracking process.
6. Closure must not be used to hide unresolved work that still belongs in the current execution scope.

### 5.9 Timestamps

| Field | Requirement | Description |
|---|---|---|
| `created_at` | Required | Closure record creation timestamp. |
| `updated_at` | Required | Most recent material update timestamp. |
| `proposed_at` | Conditional | Timestamp when closure was formally proposed. |
| `reviewed_at` | Conditional | Timestamp of the latest completed closure review. |
| `closed_at` | Conditional | Timestamp when closure was formally approved and recorded as closed. |

Rules:

1. Timestamps must use the repository's canonical timestamp format.
2. `created_at` must not be later than `updated_at`.
3. `closed_at` must exist only when `closure_status` is `closed`.
4. `closed_at` must correspond to the approved closure decision and closure history event.
5. Review timestamps must represent actual review activity.
6. Do not fabricate timestamps for missing historical events.

## 6. Closure Lifecycle

### 6.1 Allowed closure statuses

The `closure_status` field uses the following vocabulary:

- `not_started`
- `in_preparation`
- `in_review`
- `blocked`
- `closed`
- `cancelled`

Definitions:

| Status | Meaning |
|---|---|
| `not_started` | No formal closure preparation has begun. |
| `in_preparation` | Closure information and readiness checks are being assembled. |
| `in_review` | The closure package is undergoing formal review. |
| `blocked` | Closure cannot proceed because one or more required conditions remain unresolved. |
| `closed` | Closure has been formally approved and recorded. |
| `cancelled` | The execution was cancelled under applicable governance and is being formally ended without normal completion. |

### 6.2 Allowed transitions

| Current status | Allowed next status |
|---|---|
| `not_started` | `in_preparation`, `cancelled` |
| `in_preparation` | `in_review`, `blocked`, `cancelled` |
| `in_review` | `in_preparation`, `blocked`, `closed`, `cancelled` |
| `blocked` | `in_preparation`, `cancelled` |
| `closed` | No transition |
| `cancelled` | No transition |

Rules:

1. Every transition must be recorded in `history`.
2. Every transition must include a timestamp and reason.
3. A transition to `in_review` requires a prepared closure assessment.
4. A transition to `blocked` requires a description of the unresolved conditions and references to related records.
5. A blocked closure may return to `in_preparation` when the blocking conditions have been resolved or formally addressed.
6. A closure review that identifies missing or failed checks must return to preparation or become blocked; it must not proceed to `closed` without addressing those checks.
7. A transition to `closed` requires an approved closure decision and satisfaction of the closure requirements in this document.
8. A transition to `cancelled` requires the applicable authorized cancellation decision or approval.
9. `closed` and `cancelled` are terminal statuses.
10. A terminal closure record must not be reopened by editing its status.
11. If additional work is required after closure or cancellation, create a new change and execution.
12. A failed closure decision must be recorded in `decisions.yml`. The closure record may return to `in_preparation` or `blocked` as appropriate, with the failed review retained in history.

### 6.3 Closure cancellation

Cancellation is not equivalent to successful completion.

When an execution is cancelled:

- The cancellation must be authorized under applicable governance.
- The cancellation decision must be referenced.
- Completed work must remain accurately recorded.
- Incomplete and cancelled work items must remain distinguishable.
- Unresolved dependencies, handoffs, blockers, and risks must be documented.
- The closure summary must state that the execution was cancelled rather than completed.
- Any retained outputs and follow-up work must be referenced.
- The execution must not be represented as successfully delivered merely because it has reached a terminal state.

A cancelled execution may have incomplete completion and verification statuses. Its terminal status records the authorized ending of the execution, not successful delivery.

## 7. Closure Readiness Requirements

Before closure can be approved, the closure assessment must evaluate all applicable conditions below.

### 7.1 Scope accounting

- The approved execution scope is identifiable.
- All approved work items are included in the closure assessment.
- Approved replanning changes are reflected in the current work-item and dependency records.
- Removed, deferred, or cancelled scope has the required authorization.
- No material in-scope work has been silently omitted.
- Any work explicitly moved to a later execution is traceable.

### 7.2 Role activation completion

- Role activation records have been reviewed.
- No role remains active while its assigned execution work is being represented as finished.
- Required roles have appropriate terminal activation states.
- Conditional and optional roles that were not activated are accurately recorded as `not_activated` where applicable.
- Deactivated roles and incomplete assignments have traceable explanations.
- Role activation completion does not imply that every work item assigned to that role is complete.

### 7.3 Work-item completion

- Every in-scope work item has been evaluated.
- Work-item states are consistent with the completion assessment.
- No work item remains in an active or review state without an explicit, authorized exception.
- Cancelled work items have appropriate authorization.
- Work-item evidence and artifact references are traceable.
- The canonical work-item records remain the authority for their states.

### 7.4 Dependency resolution

- Every applicable dependency has been reviewed.
- Required dependencies are `satisfied` or have another explicitly permitted and authorized disposition.
- Conditional dependencies have been evaluated against their activation conditions.
- Feedback dependencies have been considered and their relevant outcomes recorded.
- Dependencies marked `not_applicable` have a defensible reason.
- Cancelled dependencies have the required authorization.
- Blocked dependencies have been resolved or explicitly accepted under applicable governance.
- The dependency graph remains valid and acyclic.
- No required dependency is silently ignored because its successor work item is already marked completed.

### 7.5 Handoff resolution

- Every applicable handoff execution has been reviewed.
- Required handoffs have been accepted or otherwise formally dispositioned under applicable governance.
- Partial acceptance is not treated as full acceptance of the entire handoff.
- Rejected, blocked, or incomplete handoffs are resolved or explicitly handled through authorized decisions and exceptions.
- Submission and decision history remains intact.
- Handoff dependency references are consistent with the dependency records.
- No handoff is assumed accepted because the producer submitted an artifact or because time elapsed.

### 7.6 Decision resolution

- Material decisions affecting execution scope, implementation, acceptance, exceptions, release, and closure are traceable.
- No decision requiring approval remains merely proposed or under review.
- Rejected, withdrawn, and superseded decisions are not treated as approvals.
- Decisions that authorize exceptions are linked to the correct exceptions.
- The closure decision is explicitly recorded and approved before closure.
- Decision authority follows `decision-records.md`.

### 7.7 Evidence completeness

- Required evidence has been identified.
- Evidence references resolve to actual evidence records.
- Evidence provenance is sufficient for the claims being made.
- Invalid or superseded evidence is not used as the sole support for successful verification.
- Evidence verification states are considered.
- Missing evidence is identified rather than inferred.
- Evidence records are not modified or replaced merely to make closure checks pass.

### 7.8 Verification completion

- Applicable acceptance criteria have been identified.
- Required tests, reviews, inspections, or other verification activities have been evaluated.
- Results are supported by evidence.
- Failed and unverified work is explicitly identified.
- Any accepted verification exception has the required authorization.
- The verification summary accurately states its coverage and limitations.
- Verification does not claim broader coverage than the evidence supports.

### 7.9 Blocker resolution

- Every blocker relevant to the execution has been reviewed.
- Resolved blockers have resolution summaries and supporting references where applicable.
- Deferred blockers have the required authorized decision and follow-up reference.
- Cancelled blockers have an appropriate reason and authorization.
- Open or in-progress blockers are not silently treated as resolved.
- Residual risks from unresolved blockers are documented.
- Blocker resolution does not automatically change the status of affected work items or dependencies.

### 7.10 Replanning completion

- Every replanning record has been reviewed.
- Approved replanning changes have been applied to the canonical records.
- Rejected or withdrawn replans have not been applied as approved changes.
- Replans still in progress are resolved or explicitly handled.
- The final execution scope and sequence reflect approved changes.
- The closure record references the relevant replanning records.

### 7.11 Release readiness and release completion

Release checks are conditional.

When release is applicable:

- Applicable release readiness requirements have been evaluated.
- Required release approvals are recorded.
- Release evidence and release records are traceable.
- Release status and outcome are consistent with the applicable release governance.
- Failed, deferred, or cancelled release activity is accurately represented.
- A release is not marked complete solely because closure is being prepared.

When release is not applicable:

- The closure assessment must explicitly record that release is not applicable.
- The reason must be documented.
- `release_record_refs` may be an empty list.

Closure must not force an unnecessary release stage onto executions for which release does not apply.

### 7.12 Documentation and delivery

- Required documentation and knowledge outputs have been evaluated.
- Required handoff and delivery outputs are traceable.
- The final delivery summary accurately reflects the delivered scope.
- Known limitations, accepted exceptions, and follow-up responsibilities are documented.
- External recipients are not represented as having received or accepted outputs without evidence.

### 7.13 Other domain-specific requirements

Security, quality, operations, performance, accessibility, and other specialist requirements must be evaluated when applicable to the execution scope.

The closure assessment must not assume that every specialist requirement applies to every execution. Equally, it must not omit a relevant specialist requirement simply because the corresponding role was not activated.

Applicability must be grounded in the approved scope, requirements, and existing governance.

## 8. Closure Approval Conditions

An execution may transition to `closed` only when all of the following conditions are met:

1. The execution identity is valid and traceable.
2. The approved scope has been accounted for.
3. Completion has been assessed and its conclusion is supported by canonical records.
4. Verification has been assessed and its conclusion is supported by sufficient evidence.
5. Required closure checks have passed or are legitimately `not_applicable`.
6. Failed or unverified required checks have been resolved or explicitly accepted through an authorized exception.
7. Applicable dependencies have been resolved or formally dispositioned.
8. Applicable handoffs have been resolved or formally dispositioned.
9. Relevant decisions are finalized.
10. Evidence references are valid and traceable.
11. Blockers have been resolved or explicitly accepted under applicable governance.
12. Replanning records have been finalized and their approved changes applied.
13. Release requirements have been satisfied when release is applicable.
14. Documentation and delivery requirements have been evaluated.
15. Residual risks and follow-up work have been documented.
16. The closure decision exists in `decisions.yml`, belongs to the same execution, uses `execution_closure`, and has an approved status.
17. The closure decision was made by an authorized role.
18. The closure record contains a final summary, timestamps, and history entry documenting the closure.

A closure decision must not be approved solely because a deadline has passed, a project manager requests closure, or all visible work items appear complete.

If a required condition is unresolved, the closure must remain in preparation or blocked unless an authorized exception is permitted by applicable governance.

## 9. Relationship to Workflow Lifecycle

The closure record supports the `Closure` workflow stage defined in `workflow-lifecycle.md`.

The normal lifecycle remains:

Intake → Qualification → Solution Framing → Planning → Execution → Integration and Review → Verification → Release Readiness and Release (conditional) → Closure.

Rules:

1. Closure follows verification.
2. When release is applicable, the applicable release readiness and release activities must be addressed before closure.
3. When release is not applicable, closure may follow verification without an artificial release stage.
4. Entering the Closure workflow stage does not mean the execution is already closed.
5. A closure record may be in preparation, in review, or blocked while the workflow is in its closure stage.
6. The workflow must not be marked `released` unless release actually occurred and is supported by the applicable release records.
7. The workflow must not be represented as successfully closed until the closure record has `closure_status: closed`.
8. An execution cancelled under authorized governance must be represented as cancelled, not as successfully completed or released.
9. Workflow stage, workflow status, completion status, verification status, and closure status remain separate concepts.
10. Closure does not transfer package ownership or change the accountable owners defined in `ownership.yml`.

## 10. Closure History and Auditability

### 10.1 History structure

The `history` collection records material changes to the closure record.

Each history entry uses the following conceptual structure:

```yaml
history:
  - event_id: "HIS-<UUID>"
    event_type: "closure_status_changed"
    previous_value: "in_preparation"
    new_value: "in_review"
    reason: ""
    actor_role: ""
    related_record_refs: []
    occurred_at: ""
```

Fields:

| Field | Requirement | Description |
|---|---|---|
| `event_id` | Required | Unique history event ID. |
| `event_type` | Required | Type of material change. |
| `previous_value` | Conditional | Previous value when applicable. |
| `new_value` | Conditional | New value when applicable. |
| `reason` | Required | Explanation for the change. |
| `actor_role` | Required | Role responsible for the recorded action. |
| `related_record_refs` | Required | Related canonical record references. |
| `occurred_at` | Required | Timestamp of the actual event. |

### 10.2 History event types

The following event types are permitted:

- `closure_record_created`
- `completion_assessed`
- `verification_assessed`
- `closure_check_added`
- `closure_check_updated`
- `exception_proposed`
- `exception_approved`
- `exception_rejected`
- `exception_withdrawn`
- `closure_review_started`
- `closure_review_completed`
- `closure_blocked`
- `closure_unblocked`
- `closure_decision_recorded`
- `closure_status_changed`
- `closure_cancelled`
- `closure_approved`
- `closure_summary_updated`
- `follow_up_reference_added`
- `record_corrected`

Additional event types may be introduced through a documented governance change.

### 10.3 History rules

1. History is append-only.
2. Existing history entries must not be silently overwritten or deleted.
3. Material changes to completion, verification, closure checks, exceptions, authority, decisions, or follow-up references must be recorded.
4. A correction must explain what was incorrect and what was corrected.
5. History must not be used to conceal unauthorized changes to canonical records.
6. The actor role and timestamp must reflect the actual event.
7. A history entry must not claim that a decision was approved before the decision record supports that approval.
8. Closure approval must produce a history entry linking the approved closure decision.
9. A terminal `closed` or `cancelled` status must not be changed through a normal update.
10. A correction to a closed record may clarify historical information without reopening the execution or changing its substantive closure outcome. Any substantive new work requires a new execution.

## 11. Relationship to Other Execution Records

| Record type | Closure relationship |
|---|---|
| Execution | Provides the project, change, and execution identity. |
| Role activation | Establishes which roles were activated and their final activation states. |
| Work item | Establishes the actual state and scope of assigned work. |
| Dependency | Establishes whether required inputs and predecessor conditions were satisfied or formally dispositioned. |
| Handoff execution | Establishes submission, acceptance, rejection, blocking, and transfer history. |
| Decision | Establishes authorized scope changes, exceptions, cancellation, and closure approval. |
| Evidence | Supports completion, verification, and closure conclusions. |
| Blocker | Establishes unresolved constraints, resolution, deferral, or cancellation. |
| Replanning | Establishes approved changes to work, dependencies, assignments, and execution plans. |
| Release | Establishes release readiness and release outcome when applicable. |
| Closure | Summarizes the final assessment and records formal closure authorization. |

The closure record must reference canonical records rather than copying their full contents.

## 12. Record Integrity and Consistency Rules

The following conditions must hold:

1. `closure_id` is unique across the repository.
2. `execution_id` matches the execution root record.
3. The execution contains no more than one canonical closure record.
4. Every referenced execution-scoped record belongs to the same execution.
5. Every referenced ID resolves to a valid canonical record.
6. Completion work-item lists contain no duplicates or overlapping IDs.
7. Verification work-item lists contain no duplicates or overlapping IDs.
8. Completion and verification summaries are consistent with their respective lists and canonical records.
9. A work item cannot be recorded as completed if its canonical state is not `completed`.
10. A work item cannot be recorded as cancelled if its canonical state is not `cancelled`.
11. Closure check IDs and exception IDs are unique within the closure record.
12. Approved exceptions reference valid approved decision records.
13. A closure decision references a valid approved decision record with the correct decision type.
14. The closure decision belongs to the same execution.
15. `closed_at` exists if and only if `closure_status` is `closed`.
16. A closed record has an approved closure decision and a corresponding history event.
17. A cancelled record has the applicable cancellation authorization and history event.
18. Terminal closure statuses cannot transition to another status.
19. No failed or unverified required check is silently treated as passed.
20. No missing evidence is silently treated as successful verification.
21. Required records are not omitted from the closure reference index.
22. Release references are required when release applies and may be empty when release does not apply.
23. An exception does not modify the status of its affected canonical records.
24. An approved exception must be specific to the condition it authorizes.
25. The final closure summary and residual risk statements must not contradict the canonical records.

## 13. Example Closure Record

The following example is illustrative only. It demonstrates the shape of a closure record and does not represent an actual project, approval, test result, or execution.

```yaml
closure:
  closure_id: "CLS-00000000-0000-4000-8000-000000000001"
  execution_id: "EXE-00000000-0000-4000-8000-000000000001"

  completion:
    status: "complete"
    summary: "All approved in-scope work items are completed."
    completed_work_item_ids:
      - "WI-00000000-0000-4000-8000-000000000001"
      - "WI-00000000-0000-4000-8000-000000000002"
    cancelled_work_item_ids: []
    outstanding_work_item_ids: []
    completion_evidence_refs:
      - "EVD-00000000-0000-4000-8000-000000000001"

  verification:
    status: "passed"
    summary: "Applicable acceptance criteria were verified with supporting evidence."
    verification_scope: "Approved functional and integration scope."
    verified_work_item_ids:
      - "WI-00000000-0000-4000-8000-000000000001"
      - "WI-00000000-0000-4000-8000-000000000002"
    failed_work_item_ids: []
    not_verified_work_item_ids: []
    evidence_refs:
      - "EVD-00000000-0000-4000-8000-000000000001"

  closure_status: "closed"

  closure_checks:
    - check_id: "CHK-WORK-001"
      category: "work_item_completion"
      description: "All approved in-scope work items are completed or formally cancelled."
      result: "passed"
      related_record_refs:
        - "WI-00000000-0000-4000-8000-000000000001"
        - "WI-00000000-0000-4000-8000-000000000002"
      evidence_refs: []
      notes: "All in-scope work items were accounted for."
      checked_by_role: "delivery-lead"
      checked_at: "2026-01-01T10:00:00Z"

    - check_id: "CHK-VERIFY-001"
      category: "verification_completion"
      description: "Required verification activities have passed."
      result: "passed"
      related_record_refs:
        - "EVD-00000000-0000-4000-8000-000000000001"
      evidence_refs:
        - "EVD-00000000-0000-4000-8000-000000000001"
      notes: "Verification evidence was reviewed."
      checked_by_role: "qa-manager"
      checked_at: "2026-01-01T10:15:00Z"

    - check_id: "CHK-RELEASE-001"
      category: "release_completion"
      description: "Determine whether release is applicable."
      result: "not_applicable"
      related_record_refs: []
      evidence_refs: []
      notes: "This illustrative execution does not require a release."
      checked_by_role: "release-manager"
      checked_at: "2026-01-01T10:20:00Z"

  exceptions: []

  required_record_refs:
    role_activation_ids:
      - "ACT-00000000-0000-4000-8000-000000000001"
    work_item_ids:
      - "WI-00000000-0000-4000-8000-000000000001"
      - "WI-00000000-0000-4000-8000-000000000002"
    dependency_ids: []
    handoff_execution_ids: []
    decision_ids:
      - "DEC-00000000-0000-4000-8000-000000000001"
    evidence_ids:
      - "EVD-00000000-0000-4000-8000-000000000001"
    blocker_ids: []
    replan_ids: []
    release_record_refs: []

  closure_decision_id: "DEC-00000000-0000-4000-8000-000000000001"

  proposed_by_role: "delivery-lead"
  coordinated_by_role: "delivery-lead"
  closure_authorized_by_role: "delivery-lead"

  closure_summary: "The illustrative execution completed its approved scope, passed applicable verification, and received formal closure approval."
  residual_risks: []
  follow_up_references: []

  created_at: "2026-01-01T09:00:00Z"
  updated_at: "2026-01-01T10:30:00Z"
  proposed_at: "2026-01-01T09:30:00Z"
  reviewed_at: "2026-01-01T10:25:00Z"
  closed_at: "2026-01-01T10:30:00Z"

  history:
    - event_id: "HIS-00000000-0000-4000-8000-000000000001"
      event_type: "closure_record_created"
      new_value: "not_started"
      reason: "Illustrative closure record creation."
      actor_role: "delivery-lead"
      related_record_refs: []
      occurred_at: "2026-01-01T09:00:00Z"

    - event_id: "HIS-00000000-0000-4000-8000-000000000002"
      event_type: "closure_status_changed"
      previous_value: "in_review"
      new_value: "closed"
      reason: "Illustrative closure approval after required checks."
      actor_role: "delivery-lead"
      related_record_refs:
        - "DEC-00000000-0000-4000-8000-000000000001"
      occurred_at: "2026-01-01T10:30:00Z"

    - event_id: "HIS-00000000-0000-4000-8000-000000000003"
      event_type: "closure_approved"
      new_value: "closed"
      reason: "Illustrative authorized closure decision."
      actor_role: "delivery-lead"
      related_record_refs:
        - "DEC-00000000-0000-4000-8000-000000000001"
      occurred_at: "2026-01-01T10:30:00Z"
```

The example is illustrative and must not be copied into an actual execution as evidence that work, verification, or approval occurred. Actual records must use generated IDs, real timestamps, and references to records that exist. The use of `delivery-lead` as the proposer, coordinator, and authorized role in this hypothetical example does not establish universal Delivery Lead approval authority. In a real execution, `closure_authorized_by_role` must match the authorized decider recorded in the approved `execution_closure` decision, and that authority must be supported by the applicable governance.

## 14. Future Schema and Validator Requirements

Schema and automated validator implementation is deferred to Phase 1.4.7.

The future implementation must validate at least the following.

### 14.1 Structure and identity

- Required fields and allowed field types.
- Valid closure, execution, and referenced record ID formats.
- Unique closure IDs.
- One canonical closure record per execution.
- Valid execution identity and record location.
- Valid nested collection structures.
- Timestamp format and chronological consistency.

### 14.2 Completion

- Allowed completion statuses.
- Valid work-item references.
- No duplicate or overlapping work-item lists.
- Every in-scope work item accounted for.
- Consistency between completion lists and canonical work-item states.
- Approved scope and replanning changes considered.
- Appropriate authorization for cancelled work.
- Exception requirements for `complete_with_exceptions`.

### 14.3 Verification

- Allowed verification statuses.
- Valid evidence and work-item references.
- No duplicate or overlapping verification lists.
- Verification coverage of applicable completed work.
- Evidence records exist and belong to the correct execution.
- Evidence verification and supersession states are respected.
- No unsupported successful verification conclusion.
- Exception requirements for `passed_with_exceptions`.

### 14.4 Closure checks

- Unique check IDs.
- Allowed categories and results.
- Required explanations for `not_applicable`.
- Required evidence or record references where applicable.
- No closure approval while mandatory checks remain failed or unverified without authorized handling.

### 14.5 Exceptions

- Unique exception IDs.
- Allowed categories and statuses.
- Valid affected record references.
- Valid approved decision references.
- Decision type and execution identity consistency.
- Required impact, reason, and residual risk descriptions.
- Follow-up traceability.
- Restrictions on exceptions that cannot be waived.

### 14.6 Closure decision and authority

- Closure decision exists in `decisions.yml`.
- Decision belongs to the same execution.
- Decision type is `execution_closure`.
- Decision status is approved for successful closure.
- Authorized decision-maker and applicable authority rules are satisfied.
- Closure history references the decision.

### 14.7 Lifecycle and history

- Allowed closure status values.
- Valid lifecycle transitions.
- Terminal status enforcement.
- Required closure and cancellation authorization.
- `closed_at` consistency with closure status.
- Required history entries for material transitions.
- Append-only history expectations.
- No reopening of closed or cancelled executions.

### 14.8 Cross-record consistency

- Work-item, activation, dependency, handoff, decision, evidence, blocker, and replanning references resolve.
- All execution-scoped references belong to the same execution.
- Artifact IDs resolve through the canonical ownership catalog.
- Handoff and dependency relationships remain consistent.
- Approved replanning changes are reflected in canonical records.
- Blocker resolution does not silently alter dependent records.
- Release references are consistent with release applicability.
- Closure summaries do not contradict canonical record states.

Automated validation must distinguish between a structurally valid record and a semantically justified closure conclusion. A schema can verify shape and references; it cannot independently prove that a test was performed or that a human review was adequate.

Model-assisted scenario evaluation and human review remain separate from deterministic repository validation.

## 15. Governance and Change Control

Changes to this specification must preserve:

- One canonical closure record per execution.
- Separation of completion, verification, and closure.
- Stable record identity and traceability.
- Canonical ownership and authority boundaries.
- Explicit approval for exceptions.
- Terminal closure behavior.
- Accurate evidence provenance.
- No fabricated execution records or verification claims.

Any change to record fields, lifecycle vocabulary, closure conditions, or approval requirements must be reflected in the execution record model, workflow documentation, schemas, validators, and relevant tests when those components are implemented.

Existing execution records must not be silently reinterpreted under changed rules. Any migration or compatibility change must be documented and traceable.