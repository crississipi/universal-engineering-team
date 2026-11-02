# Handoff Execution Records

## 1. Purpose

Handoff Execution Records track the actual transfer of work or deliverables between roles during a specific project execution.

They connect reusable handoff contracts to real execution activity while preserving submission history, acceptance decisions, and the current handoff state.

A handoff contract defines the reusable producer-consumer requirements. A handoff execution record documents an actual instance of that transfer.

This document defines the canonical structure and governance rules for handoff execution records.

## 2. Record Storage

Handoff execution records are stored in:

`executions/<execution-id>/handoff-executions.yml`

The file contains a collection of independent handoff execution records belonging to the same execution.

The canonical top-level YAML key is `handoff_executions`, and its
value is an array of handoff execution mappings. The key must be present
even when no formal handoff execution exists for the execution.

Illustrative structural excerpt:

```yaml
handoff_executions:
  - handoff_execution_id: "HEX-<UUID>"
    execution_id: "EXE-<UUID>"
    handoff_contract_id: "<contract-id>"
```

The excerpt is not a complete record; all required fields in this
specification must be present in an actual handoff execution.

Reusable handoff contracts remain defined in:

`docs/team/handoffs.yml`

The handoff contract is authoritative for:

- Producer and consumer roles.
- Source artifact package.
- Consumer artifact package, when applicable.
- Required outputs.
- Required context.
- Acceptance checks.
- Handoff purpose and activation conditions.

The execution record must reference the applicable contract rather than duplicate its requirements.

## 3. Handoff Execution Identity

Each independent handoff transfer instance must have a unique identifier.

Format:

`HEX-<UUID>`

Example:

`HEX-550e8400-e29b-41d4-a716-446655440000`

Multiple independent handoff execution records may reference the same handoff contract within one execution.

A handoff contract identifies a reusable relationship. A handoff execution record identifies one actual transfer instance.

A new independent handoff execution record is required when a new transfer instance is initiated after a previously accepted or cancelled instance.

Resubmissions belonging to the same transfer instance must remain within the existing handoff execution record.

## 4. Handoff Execution Record Structure

Each handoff execution record must support the following fields:

| Field | Required | Description |
|---|---|---|
| `handoff_execution_id` | Yes | Unique handoff execution identifier. |
| `execution_id` | Yes | Parent execution identifier. |
| `handoff_contract_id` | Yes | Reference to the reusable handoff contract. |
| `instance_name` | Yes | Short descriptive name for this transfer instance. |
| `purpose` | Yes | Purpose of the actual transfer. |
| `from_role` | Yes | Producer role. |
| `to_role` | Yes | Consumer role. |
| `artifact_id` | Yes | Producer artifact package identifier. |
| `consumer_artifact_id` | Conditional | Consumer artifact package identifier when the contract defines one. |
| `producer_work_item_id` | Yes | Work item responsible for producing the handoff output. |
| `consumer_work_item_id` | Yes | Work item responsible for receiving or using the output. |
| `dependency_ids` | No | Related dependency execution record identifiers. |
| `current_status` | Yes | Current handoff execution lifecycle status. |
| `current_submission_id` | Conditional | Identifier of the latest submission when one exists. |
| `current_decision_id` | Conditional | Identifier of the latest canonical decision associated with the handoff. |
| `submissions` | Yes | Ordered history of submissions. |
| `created_at` | Yes | Record creation timestamp. |
| `updated_at` | Yes | Most recent record update timestamp. |
| `external_references` | No | References to external systems or records. |
| `history` | Yes | Chronological record of material lifecycle changes. |

The `consumer_artifact_id` is required only when the referenced handoff contract defines a consumer artifact package.

The `current_submission_id` must reference a submission within the same handoff execution record.

The `current_decision_id` must reference a canonical decision in the same execution's `decisions.yml`.

The handoff execution record must not independently store decision outcomes, rejection codes, decision authority, or decision rationale. Those belong to the canonical decision record.

## 5. Submission Records

Each submission represents one producer delivery attempt within a handoff execution instance.

A submission must have a unique identifier.

Format:

`SUB-<UUID>`

Each submission must contain:

| Field | Required | Description |
|---|---|---|
| `submission_id` | Yes | Unique submission identifier. |
| `submitted_at` | Yes | Submission timestamp. |
| `submitted_by_role` | Yes | Producer role responsible for submission. |
| `output_refs` | Yes | References to submitted outputs. |
| `context_refs` | No | References to required supporting context. |
| `notes` | No | Additional submission information. |
| `acceptance_checks` | Yes | Results of applicable contract acceptance checks. |
| `decision_id` | Conditional | Canonical decision associated with this submission. |

Submission IDs must be unique within the execution.

Every submission must preserve its original output references, context references, timestamp, and acceptance-check results.

A subsequent submission must not overwrite or replace the contents of an earlier submission.

### 5.1 Acceptance Check Results

Acceptance checks must reference the corresponding acceptance check identifiers defined in the reusable handoff contract.

Each check result must use one of these values:

- `passed`
- `failed`
- `not_applicable`
- `not_verified`

Acceptance-check results document verification evidence. They do not independently constitute an acceptance decision.

The consumer role remains responsible for evaluating the submission and recording the appropriate canonical decision.

## 6. Canonical Decision References

Handoff decisions must be recorded in the execution's canonical `decisions.yml`.

The handoff execution record references those decisions using `current_decision_id` and the applicable submission's `decision_id`.

The canonical decision record is authoritative for:

- Decision status.
- Decision outcome.
- Rejection code, when applicable.
- Decision proposer and decider.
- Decision authority.
- Options considered.
- Selected option.
- Decision rationale.
- Impact summary.
- Related evidence and affected records.

Handoff-specific decision outcomes are:

- `accepted`
- `partially_accepted`
- `rejected`
- `blocked`

These outcomes are recorded in the canonical decision record's `decision_outcome` field when the decision type is `handoff_acceptance`.

A rejected handoff decision must use a valid rejection code defined in `docs/team/handoff-acceptance-rules.md`.

A blocked outcome is not a rejection. It indicates that acceptance cannot currently proceed.

The handoff execution record's `current_status` must remain consistent with the latest applicable canonical handoff decision.

## 7. Handoff Execution Status

The `current_status` field must use one of these values:

| Status | Meaning |
|---|---|
| `planned` | The transfer instance has been created but submission work has not started. |
| `in_progress` | The producer is preparing or revising the handoff output. |
| `submitted` | A submission has been delivered and awaits consumer evaluation. |
| `partially_accepted` | The consumer has accepted only the separable and safe portions of a submission. |
| `accepted` | The consumer has accepted the required handoff outputs. |
| `rejected` | The consumer has rejected the submitted handoff. |
| `blocked` | The transfer or acceptance process cannot currently proceed. |
| `cancelled` | The transfer instance has been cancelled through an authorized decision or applicable governance process. |

### 7.1 Status Transitions

Permitted lifecycle transitions:

- `planned` → `in_progress`
- `planned` → `cancelled`
- `in_progress` → `submitted`
- `in_progress` → `blocked`
- `in_progress` → `cancelled`
- `submitted` → `accepted`
- `submitted` → `partially_accepted`
- `submitted` → `rejected`
- `submitted` → `blocked`
- `partially_accepted` → `in_progress`
- `partially_accepted` → `blocked`
- `rejected` → `in_progress`
- `rejected` → `blocked`
- `blocked` → `in_progress`
- `blocked` → `submitted` when a previously blocked submission can proceed without requiring a new submission.
- `blocked` → `cancelled`

Additional rules:

1. `accepted` is terminal for that handoff execution instance.
2. `cancelled` is terminal for that handoff execution instance.
3. A new transfer after acceptance or cancellation requires a new handoff execution record.
4. A rejected submission may be revised and resubmitted within the same handoff execution record.
5. A partially accepted submission may be followed by additional work within the same handoff execution record.
6. Every material status transition must be recorded in `history`.
7. Status changes must have a supporting decision or documented operational reason as applicable.
8. A timeout or absence of consumer response must never be treated as acceptance.

## 8. Resubmission and Submission History

Resubmissions must remain within the same handoff execution record when they belong to the same transfer instance.

Each resubmission creates a new submission entry with a new `submission_id`.

Previous submissions must remain unchanged.

The record must preserve:

- Every submission.
- The original submission timestamp.
- The submitted outputs and supporting context.
- Acceptance-check results for each submission.
- The canonical decision associated with each submission, when available.
- The chronological relationship between submissions and decisions.

`current_submission_id` must point to the latest submission.

`current_decision_id` must point to the latest canonical decision associated with the handoff execution.

A previous decision must not be overwritten when a new submission or decision is recorded.

## 9. Partial Acceptance

Partial acceptance is permitted only when the accepted outputs are separable, independently usable, and safe to use without relying on rejected or incomplete outputs.

The canonical decision record must document the partial acceptance outcome and explain:

- Which outputs were accepted.
- Which outputs remain incomplete or rejected.
- What additional work is required.
- Whether downstream work may proceed.
- Any associated dependency impact.

Partial acceptance does not automatically satisfy the entire dependency.

The corresponding dependency execution record must be updated independently according to its own status and satisfaction criteria.

## 10. Dependency Traceability

A handoff execution may fulfill one or more dependency execution records.

The `dependency_ids` field must reference valid dependency records in the same execution.

When a dependency is fulfilled through a formal handoff, the relationship must be traceable in both directions:

- The handoff execution record references the dependency through `dependency_ids`.
- The dependency execution record references the handoff through `handoff_execution_refs`.

A handoff execution record must not independently change the status of a dependency record.

Dependency status remains authoritative in `dependencies.yml`.

A blocked or rejected handoff may require the related dependency to become blocked, but that transition must be recorded in the dependency record with the appropriate reason and history.

A partially accepted handoff must not automatically mark a required dependency as satisfied.

## 11. Work Item and Role Traceability

The producer and consumer work item references must resolve to valid work items in the same execution.

The producer work item must be assigned to the role identified by `from_role`.

The consumer work item must be assigned to the role identified by `to_role`.

Both roles must have valid role activation records in the same execution.

The producer and consumer work items must follow the canonical role activation and work-item governance rules.

A handoff execution record does not transfer artifact ownership.

The accountable artifact owner remains the role defined in the canonical artifact ownership catalog.

## 12. History and Auditability

Every material change to a handoff execution record must be preserved in its `history`.

History entries must contain:

- `changed_at`
- `changed_by_role`
- `change_type`
- `previous_value`, when applicable.
- `new_value`, when applicable.
- `reason`

History must preserve material events, including:

- Initial handoff planning.
- Work commencement.
- Submission creation.
- Consumer evaluation.
- Acceptance decisions.
- Rejection decisions.
- Partial acceptance.
- Blocking and unblocking.
- Resubmission.
- Cancellation.

History entries must be chronological.

Previous submissions and decisions must never be deleted or silently overwritten to represent a newer state.

## 13. External References

The `external_references` field may contain references to records outside the current execution.

Examples include:

- External ticket identifiers.
- Third-party issue references.
- External document references.
- External approval records.
- Links to other systems.

External references must be explicitly identified as external and must not be treated as execution-scoped record identifiers.

## 14. Validation Requirements

Future schema and validator implementation must enforce the following:

### 14.1 Identity and References

- Every handoff execution ID is unique.
- Every record has a valid parent execution ID.
- Every handoff contract reference resolves to a valid reusable contract.
- Producer and consumer roles match the referenced handoff contract.
- Artifact package references resolve against `docs/team/ownership.yml`.
- Producer and consumer work item references resolve within the same execution.
- Role activation references are valid and consistent with the assigned work item roles.
- Dependency references resolve within the same execution.
- Canonical decision references resolve within the same execution.
- Submission IDs are unique within the execution.

### 14.2 Submission Integrity

- Every submission contains a valid submission ID and timestamp.
- Every submission identifies the producer role.
- Output references are present.
- Acceptance checks reference valid contract check identifiers.
- Acceptance-check results use the permitted vocabulary.
- Previous submissions remain preserved.
- Each submission's decision reference resolves to the appropriate canonical decision when provided.

### 14.3 Decision Consistency

- Decision lifecycle and authority are validated through the canonical decision record.
- Handoff outcomes are recorded only in the canonical decision record.
- Rejection codes are validated against the canonical rejection-code vocabulary.
- `current_decision_id` references the latest applicable canonical decision.
- The handoff execution status is consistent with the latest applicable handoff decision.
- A missing decision must not be interpreted as implicit acceptance.

### 14.4 Lifecycle and History

- Status values use the permitted vocabulary.
- Status transitions follow the defined lifecycle.
- Terminal statuses cannot be reopened.
- Every material transition has a history entry.
- History entries are chronological.
- Resubmissions do not overwrite previous submissions.
- Accepted or cancelled instances cannot be reused for a new independent transfer.

### 14.5 Dependency and Work Item Consistency

- Dependency references are bidirectional where applicable.
- A handoff does not automatically satisfy a dependency.
- Partial acceptance does not automatically satisfy the entire dependency.
- Producer and consumer work items match the declared roles.
- Handoff records do not change artifact ownership.

## 15. Relationship to Other Governance Documents

This document must be read together with:

- `docs/team/handoffs.yml` — reusable handoff contracts.
- `docs/team/handoff-acceptance-rules.md` — acceptance, rejection, and escalation rules.
- `docs/team/decision-records.md` — canonical decision records and decision lifecycle.
- `docs/team/dependency-execution-records.md` — dependency execution state and traceability.
- `docs/team/role-activation-and-work-item-records.md` — role activation and work-item assignments.
- `docs/team/execution-record-model.md` — canonical execution record architecture.
- `docs/team/execution-identity-and-traceability.md` — execution identity and record references.
- `docs/team/workflow.md` — workflow orchestration and execution governance.

These documents remain authoritative within their respective responsibilities.

## 16. Implementation Boundary

This document defines the governance and record model for handoff execution.

It does not introduce:

- A new handoff contract format.
- A replacement for canonical decision records.
- A replacement for dependency execution records.
- A new artifact ownership mechanism.
- Automated acceptance based solely on status or elapsed time.
- An event-sourcing architecture.

Schemas, validators, and automated tests for handoff execution records are deferred to Phase 1.4.7.

Until those are implemented, records must follow this specification and the existing governance documents.