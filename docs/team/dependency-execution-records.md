# Dependency Execution Records

## 1. Purpose

Dependency execution records document the actual dependency relationships between work items within a specific project execution.

They establish:

- Which work item must precede another work item.
- Why the dependency exists.
- Whether the dependency applies to the current execution.
- Whether the dependency has been satisfied, blocked, or cancelled.
- What evidence supports dependency satisfaction.
- How dependency status changed over time.

Dependency records represent actual execution state. They must not be used as substitutes for reusable workflow governance rules.

## 2. Canonical Storage

Dependency execution records are stored in:

`executions/<execution-id>/dependencies.yml`

The collection belongs to one execution only.

Every dependency record must reference the same execution through its `execution_id`.

The reusable dependency governance rules remain defined in:

`docs/team/dependency-execution-rules.md`

## 3. Dependency Record Structure

Each dependency record must contain:

| Field | Requirement | Description |
|---|---|---|
| `dependency_id` | Required | Stable unique dependency identifier. |
| `execution_id` | Required | Execution containing the dependency. |
| `predecessor_work_item_id` | Required | Work item that provides the prerequisite output or feedback. |
| `successor_work_item_id` | Required | Work item that consumes or depends on the predecessor. |
| `relationship_type` | Required | `required_input`, `conditional_input`, or `feedback`. |
| `purpose` | Required | Explains why the dependency exists. |
| `dependency_condition` | Required | Describes the condition that must be fulfilled. |
| `activation_condition` | Conditional | Defines when a `conditional_input` dependency applies. |
| `status` | Required | Current dependency execution status. |
| `created_at` | Required | Timestamp when the record was created. |
| `updated_at` | Required | Timestamp of the latest record update. |
| `satisfaction_evidence_refs` | Optional | References to evidence supporting satisfaction. |
| `related_decision_ids` | Optional | Related decision record identifiers. |
| `related_blocker_ids` | Optional | Related blocker record identifiers. |
| `external_references` | Optional | References to relevant external resources. |
| `history` | Required | Auditable record of material changes and status transitions. |
| `handoff_execution_refs` | Optional | References to related formal handoff execution records. |

### 3.1 Identifier Format

Dependency identifiers use:

`DEP-<UUID>`

Example:

`DEP-550e8400-e29b-41d4-a716-446655440000`

Identifiers must remain stable throughout the execution record's lifetime.

A dependency must not receive a new identifier merely because its status changes.

### 3.2 Relationship Types

Dependency records use the relationship types already established in the workflow governance rules.

- `required_input`: The successor requires an output from the predecessor before it can proceed with the dependent work.
- `conditional_input`: The successor requires the predecessor's output only when a defined activation condition applies.
- `feedback`: The predecessor provides feedback to the successor. This relationship does not automatically block successor execution.

Relationship types must not be reinterpreted or replaced with work-item states.

## 4. Dependency Status

Dependency status is recorded explicitly and remains separate from work-item state.

The allowed statuses are:

| Status | Meaning |
|---|---|
| `planned` | The dependency has been identified but has not yet become an active execution constraint. |
| `active` | The dependency applies to the execution and its required condition remains unresolved. |
| `satisfied` | The dependency condition has been fulfilled and the required output or feedback is available. |
| `blocked` | The dependency cannot currently be satisfied because of an unresolved blocker. |
| `not_applicable` | A conditional dependency was evaluated and its activation condition does not apply. |
| `cancelled` | The dependency was formally withdrawn through an authorized decision or replanning action. |

### 4.1 Status Compatibility

The following status combinations are permitted:

| Relationship type | Allowed statuses |
|---|---|
| `required_input` | `planned`, `active`, `satisfied`, `blocked`, `cancelled` |
| `conditional_input` | `planned`, `active`, `satisfied`, `blocked`, `not_applicable`, `cancelled` |
| `feedback` | `planned`, `active`, `satisfied`, `blocked`, `cancelled` |

A `not_applicable` status is only valid for a `conditional_input` dependency.

## 5. Status Transitions

Dependency status transitions must follow these rules:

| Current status | Permitted next status |
|---|---|
| `planned` | `active`, `not_applicable`, `cancelled` |
| `active` | `satisfied`, `blocked`, `cancelled` |
| `blocked` | `active`, `satisfied`, `cancelled` |
| `satisfied` | `active`, `cancelled` |
| `not_applicable` | `active`, `cancelled` |
| `cancelled` | None |

### 5.1 Transition Rules

1. A dependency becomes `active` when it applies to the current execution and its condition remains unresolved. A dependency must not remain `planned` after its applicability has been
established and its unresolved condition begins governing dependent work.
2. A dependency becomes `satisfied` only when its required condition has been fulfilled.
3. A dependency becomes `blocked` when an unresolved blocker prevents its satisfaction.
4. A blocked dependency may return to `active` when the blocking condition is resolved but the dependency itself remains unsatisfied.
5. A satisfied dependency may return to `active` if its prerequisite output becomes invalid, unavailable, or otherwise no longer fulfills the dependency condition.
6. A conditional dependency may become `not_applicable` when its activation condition is evaluated and does not apply.
7. A previously `not_applicable` conditional dependency may become `active` if an authorized scope or condition change makes it applicable.
8. A cancelled dependency is terminal. If the same dependency relationship becomes necessary again, create a new record with a new identifier.

Every status transition must be recorded in `history` with its timestamp, previous status, new status, reason, and responsible actor or role.

## 6. Dependency Execution Rules

### 6.1 Work-Item References

Both `predecessor_work_item_id` and `successor_work_item_id` must reference existing work-item records in the same execution.

A dependency must not reference the same work item as both predecessor and successor.

The predecessor and successor must belong to the execution identified by `execution_id`.

### 6.2 Required Inputs

A `required_input` dependency represents a mandatory prerequisite
for the dependent work or applicable progression gate.

When its status is `active` or `blocked`, the successor must not pass
the dependent progression gate or treat the required input as satisfied.

Controlled provisional work may proceed only when the conditions in
`dependency-execution-rules.md` Section 7 are met.

Provisional consumption does not satisfy the dependency, constitute
formal acceptance, or authorize bypassing a required approval, safety,
security, privacy, or data-integrity constraint.

The dependency remains unresolved until its required condition is
fulfilled and the necessary evidence or acceptance is available.

### 6.3 Conditional Inputs

A `conditional_input` dependency applies only when its activation condition is met.

The activation condition must be explicitly documented.

When the condition applies, the dependency becomes `active` and follows the normal satisfaction and blocking rules.

When the condition does not apply, the dependency becomes `not_applicable`.

A conditional dependency must not be silently ignored or assumed to apply without evaluating its activation condition.

### 6.4 Feedback Dependencies

A `feedback` dependency records a feedback relationship between work items.

Feedback dependencies do not automatically block successor execution.

Whether feedback must be addressed before completion depends on the applicable acceptance criteria, decisions, and workflow rules.

### 6.5 Dependency Graph

The execution dependency graph must remain acyclic.

A dependency must not introduce a cycle in the predecessor-successor relationships.

Collaboration relationships may be bidirectional or cyclic, but execution dependencies must preserve a valid acyclic execution order.

A dependency record that creates a cycle must be rejected by validation.

### 6.6 Handoff Relationship

A dependency and a formal handoff execution are separate records.

A dependency may be fulfilled through a formal handoff, but the existence
of a dependency does not automatically establish that a handoff occurred.

When a formal handoff is required, record the related handoff execution
identifier in `handoff_execution_refs`. The handoff execution must
reference the applicable dependency identifier when the relationship
requires traceability in both directions.

Handoff execution records remain authoritative for submission,
resubmission, and acceptance decisions.

Dependency satisfaction must not be inferred solely from the existence
of a handoff record. The required output or feedback must satisfy
the dependency condition.

## 7. Evidence, Decisions, and Blockers

### 7.1 Satisfaction Evidence

When evidence is used to establish dependency satisfaction, its identifier must be recorded in `satisfaction_evidence_refs`.

Evidence references must point to existing evidence records within the same execution.

A dependency must not be marked `satisfied` based on an unverified or nonexistent evidence reference.

### 7.2 Related Decisions

A dependency may reference decisions that establish, modify, or cancel its applicability.

Decision references must use stable decision identifiers from the execution's decision records.

### 7.3 Related Blockers

A dependency with status `blocked` must reference the applicable blocker record when one exists.

Blocker records remain authoritative for blocker details, ownership, resolution actions, and history.

Resolving a blocker does not automatically satisfy the dependency. The dependency must be reassessed against its own condition.

## 8. Change History

Every dependency record must maintain an auditable `history`.

History must preserve material changes, including:

- Initial record creation.
- Relationship or condition changes.
- Activation-condition changes.
- Status transitions.
- Evidence additions or removals.
- Related decision or blocker changes.
- Cancellation and its authorization.

Each history entry should include:

- `timestamp`
- `actor`
- `action`
- `reason`
- `previous_values`, when applicable
- `new_values`, when applicable
- `related_record_ids`, when applicable

Existing history entries must not be silently overwritten or deleted.

The current record fields represent the latest state. History preserves the material changes that produced that state.

## 9. Illustrative YAML Record

The following is an illustrative example only. It is not an actual project execution record.

```yaml
dependencies:
  - dependency_id: "DEP-550e8400-e29b-41d4-a716-446655440000"
    execution_id: "EXE-550e8400-e29b-41d4-a716-446655440001"

    predecessor_work_item_id: "WI-550e8400-e29b-41d4-a716-446655440002"
    successor_work_item_id: "WI-550e8400-e29b-41d4-a716-446655440003"

    relationship_type: "required_input"
    purpose: "The frontend implementation requires the approved API contract."
    dependency_condition: "The API contract must be accepted and available."

    status: "active"

    created_at: "2026-11-01T10:00:00Z"
    updated_at: "2026-11-01T10:00:00Z"

    satisfaction_evidence_refs: []
    related_decision_ids: []
    related_blocker_ids: []
    external_references: []

    history:
      - timestamp: "2026-11-01T10:00:00Z"
        actor: "delivery-lead"
        action: "created"
        reason: "Recorded the required API contract dependency."
        new_values:
          status: "active"
```

The example identifiers and timestamps are illustrative. They must not be copied into an actual execution as real records.

## 10. Validation Requirements

Automated validation must check:

1. Every dependency record has all required fields.
2. Every `dependency_id` is unique within the execution.
3. Every dependency identifier follows the required format.
4. Every record references the correct `execution_id`.
5. Both predecessor and successor work-item references exist.
6. Both referenced work items belong to the same execution.
7. A work item cannot depend on itself.
8. `relationship_type` uses an allowed value.
9. `status` uses an allowed value.
10. The relationship type and status combination is valid.
11. `activation_condition` is present when required for a `conditional_input` dependency.
12. Status transitions follow the permitted transition rules.
13. Material status changes have corresponding history entries.
14. Satisfaction evidence references resolve to existing evidence records.
15. Related decision references resolve to existing decision records.
16. Related blocker references resolve to existing blocker records.
17. A blocked dependency references an applicable blocker record when one exists.
18. The dependency graph is acyclic.
19. Dependency references do not cross execution boundaries.
20. Illustrative examples are not treated as actual execution records.

Validation must report invalid or unresolved references explicitly.

Validators must not fabricate missing records, infer dependency satisfaction, or silently change invalid statuses.

The validation implementation and formal schemas are deferred to Phase 1.4.7.

---

## Governance Relationship

This document defines the structure and rules for actual dependency execution records.

The following documents remain authoritative for their respective concerns:

- `docs/team/dependency-execution-rules.md` - reusable dependency execution governance.
- `docs/team/execution-record-model.md` - canonical execution record architecture.
- `docs/team/role-activation-and-work-item-records.md` - role activation and work-item record requirements.
- `docs/team/handoff-acceptance-rules.md` - formal handoff acceptance requirements.
- `docs/team/blockers-replanning-and-state-transitions.md` - blocker and replanning governance.