# Re-planning Records

## 1. Purpose

Re-planning records document authorized changes to an execution plan after its initial planning or during execution.

Re-planning may be necessary when:

- A blocker prevents planned work from proceeding.
- A dependency changes or becomes unsatisfied.
- A handoff is rejected, partially accepted, or blocked.
- New evidence changes an earlier assumption.
- An approved decision changes scope or technical direction.
- A risk or external condition materially affects execution.
- Work must be reassigned, deferred, added, cancelled, or reordered.

Re-planning preserves the reason for a plan change, its authorization, its impact, and the resulting execution state.

A re-planning record documents a plan change. It does not independently authorize changes outside the authority of the responsible decision-maker.

## 2. Canonical Location

**File:** `replans.yml`

**Location:** `executions/<execution-id>/replans.yml`

Each re-planning record belongs to exactly one execution.

## 3. Re-planning Identifier

Re-planning identifiers must use:

`RPL-<UUID>`

Each identifier must be unique across the repository.

An existing identifier must never be reassigned to another re-planning record.

## 4. Canonical Re-planning Record

Each record must contain:

| Field | Required | Description |
|---|---|---|
| `replan_id` | Yes | Unique re-planning identifier |
| `execution_id` | Yes | Parent execution identifier |
| `title` | Yes | Short description of the plan change |
| `reason` | Yes | Why re-planning is necessary |
| `trigger_type` | Yes | Controlled classification of the trigger |
| `status` | Yes | Current re-planning lifecycle status |
| `proposed_by_role` | Yes | Role proposing the change |
| `coordinated_by_role` | Yes | Role coordinating the re-planning activity |
| `decision_id` | Conditional | Canonical decision authorizing the change |
| `affected_work_item_ids` | Yes | Work items affected by the change |
| `affected_dependency_ids` | Optional | Dependencies affected by the change |
| `affected_role_activation_ids` | Optional | Role activations affected by the change |
| `affected_handoff_execution_ids` | Optional | Handoff executions affected by the change |
| `affected_blocker_ids` | Optional | Blockers related to the change |
| `affected_artifact_ids` | Optional | Artifact packages affected by the change |
| `changes` | Yes | Explicit description of proposed or approved plan changes |
| `impact_summary` | Yes | Expected or actual execution impact |
| `evidence_refs` | Optional | Supporting evidence identifiers |
| `created_at` | Yes | Record creation timestamp |
| `updated_at` | Yes | Last material update timestamp |
| `implemented_at` | Conditional | Timestamp when approved changes were implemented |
| `history` | Yes | Material change history |

Conditional fields must be populated when their applicable status requires them.

Optional fields must be omitted when they do not apply.

A re-planning record must identify at least one affected work item.

## 5. Trigger Types

Use the following controlled vocabulary:

| Type | Description |
|---|---|
| `blocker` | A blocker requires a change to the execution plan |
| `dependency_change` | A dependency changes, becomes blocked, or becomes unsatisfied |
| `handoff_outcome` | A handoff outcome requires execution changes |
| `new_evidence` | New evidence changes an execution assumption or planned activity |
| `decision_change` | An authorized decision changes the execution plan |
| `scope_change` | An authorized scope change affects planned work |
| `risk_change` | A material risk changes execution priorities or sequencing |
| `resource_change` | Available resources or capacity materially change |
| `external_change` | An external condition affects planned execution |
| `other` | A trigger that does not fit another approved category |

The `other` classification requires a meaningful explanation.

A trigger identifies why re-planning was initiated. It does not establish authorization to implement the proposed changes.

## 6. Re-planning Status

Use the following statuses:

| Status | Description |
|---|---|
| `proposed` | A plan change has been proposed |
| `under_review` | The proposal is being assessed |
| `approved` | The required authority has approved the proposed changes |
| `rejected` | The proposal was rejected |
| `in_progress` | Approved changes are being implemented |
| `completed` | Approved changes have been implemented and recorded |
| `withdrawn` | The proposal was withdrawn before implementation |

### 6.1 Status Transitions

Permitted transitions:

| Current status | Permitted next statuses |
|---|---|
| `proposed` | `under_review`, `withdrawn` |
| `under_review` | `approved`, `rejected`, `withdrawn` |
| `approved` | `in_progress`, `completed` |
| `in_progress` | `completed` |
| `rejected` | Terminal |
| `completed` | Terminal |
| `withdrawn` | Terminal |

A rejected, completed, or withdrawn re-planning record must not be silently reopened.

If additional changes become necessary, create a new re-planning record and reference the earlier record where relevant.

## 7. Authorization Requirements

Re-planning proposals and re-planning authorization are separate responsibilities.

`proposed_by_role` identifies the role that initiated the proposal.

`coordinated_by_role` identifies the role coordinating the activity.

Neither field automatically grants approval authority.

A re-planning record may become `approved` only after the applicable authority has authorized the proposed changes.

Approval must be represented by a canonical decision record in:

`decisions.yml`

The approved re-planning record must reference that decision through `decision_id`.

The decision record remains authoritative for:

- Who authorized the change.
- The authority under which it was approved.
- The approved option.
- The rationale.
- Any conditions or limitations.

The Delivery Lead may coordinate cross-role re-planning but is not a universal approval authority.

Technical, product, security, quality, operational, and other decisions must follow their applicable governance authority.

## 8. Recording Proposed Changes

The `changes` collection must describe each proposed or approved plan change clearly enough for implementation and review.

Each change entry should contain:

| Field | Required | Description |
|---|---|---|
| `change_type` | Yes | Classification of the plan change |
| `target_record_ref` | Yes | Canonical record affected |
| `previous_value` | Conditional | Previous value when changing an existing value |
| `proposed_value` | Yes | Proposed or approved new value |
| `reason` | Yes | Why the change is necessary |

Use the following controlled `change_type` values:

- `work_item_assignment`
- `work_item_status`
- `work_item_scope`
- `work_item_sequence`
- `work_item_addition`
- `work_item_cancellation`
- `dependency_change`
- `role_activation`
- `handoff_plan`
- `artifact_scope`
- `workflow_schedule`
- `other`

The `other` classification requires a meaningful explanation.

Changes must reference canonical record identifiers.

Do not use free-form references when an applicable canonical record exists.

A proposed change must not be treated as implemented merely because it appears in the re-planning record.

## 9. Implementation Requirements

Once approved, changes must be applied to the appropriate canonical execution records.

Examples:

- Work-item assignment changes must update the affected work-item records and preserve their history.
- Work-item scope changes must update the affected work-item records and preserve the previous scope.
- Dependency changes must update the canonical dependency records.
- Role activation changes must update the canonical role-activation records.
- Handoff planning changes must update the applicable handoff execution records.
- Artifact ownership changes must follow artifact ownership governance.
- Workflow stage changes must follow workflow lifecycle governance.

The re-planning record provides the consolidated traceability of the change.

It does not replace the canonical records being changed.

A re-planning record must not be marked `completed` until its approved changes have been implemented and the affected records have been updated.

## 10. Impact Assessment

`impact_summary` must describe the expected impact before approval and the actual material impact when implementation is completed.

Consider applicable effects on:

- Scope and deliverables.
- Work-item assignments.
- Dependency relationships.
- Role activation.
- Handoff execution.
- Artifact ownership and production.
- Schedule and sequencing.
- Verification requirements.
- Security, quality, accessibility, and operational requirements.
- Release readiness.
- External stakeholders.

Only material and relevant effects need to be recorded.

Do not invent estimates or claim an impact has been measured without supporting evidence.

## 11. Evidence and Related Records

Use `evidence_refs` to reference supporting evidence.

Possible supporting evidence includes:

- Blocker investigation results.
- Failed or successful test results.
- Handoff acceptance or rejection evidence.
- Dependency evaluation results.
- Updated requirements.
- External system records.
- Authorized decision evidence.

Evidence identifiers must resolve to canonical evidence records in the same execution.

A re-planning record may also reference related blockers, dependencies, work items, role activations, handoff executions, and artifact packages.

References must resolve to the applicable canonical records.

The source records remain authoritative for their own statuses and content.

## 12. History Requirements

The `history` collection preserves material changes to the re-planning record.

Each history entry must contain:

| Field | Required | Description |
|---|---|---|
| `changed_at` | Yes | Timestamp of the change |
| `changed_by_role` | Yes | Role responsible for the change |
| `change_type` | Yes | Classification of the change |
| `reason` | Yes | Explanation for the change |
| `previous_status` | Conditional | Previous re-planning status |
| `new_status` | Conditional | New re-planning status |
| `changed_fields` | Optional | Other materially changed fields |

History must preserve:

- Proposal creation.
- Review activities.
- Approval or rejection.
- Withdrawal.
- Implementation progress.
- Completion.
- Material changes to proposed or approved changes.
- Changes to affected records.

Approved changes must not be silently altered after approval.

If approved changes require modification, initiate a new re-planning record and obtain the necessary authorization.

## 13. Illustrative YAML Structure

The following example is illustrative only. It is not an actual execution record.

```yaml
replans:
  - replan_id: "RPL-<UUID>"
    execution_id: "EXE-<UUID>"

    title: "Replan external integration work"

    reason: >
      Required external credentials are unavailable,
      preventing the planned integration test activities.

    trigger_type: "blocker"
    status: "proposed"

    proposed_by_role: "integration-engineer"
    coordinated_by_role: "delivery-lead"

    affected_work_item_ids:
      - "WI-<UUID>"

    affected_dependency_ids:
      - "DEP-<UUID>"

    affected_blocker_ids:
      - "BLK-<UUID>"

    changes:
      - change_type: "work_item_sequence"
        target_record_ref: "WI-<UUID>"
        previous_value: "before integration testing"
        proposed_value: "after external credentials are provisioned"
        reason: "External credentials are not yet available."

    impact_summary: >
      Integration testing may be delayed.
      Unaffected implementation work may continue
      where its prerequisites are satisfied.

    evidence_refs: []

    created_at: "2026-11-02T10:00:00Z"
    updated_at: "2026-11-02T10:00:00Z"

    history:
      - changed_at: "2026-11-02T10:00:00Z"
        changed_by_role: "integration-engineer"
        change_type: "created"
        reason: "Re-planning proposal created."
```

The identifiers and values above are placeholders. Actual records must use real identifiers and reflect the actual approved plan.

## 14. Validation Requirements

The future re-planning validator must enforce:

1. Re-planning identifiers are unique.
2. Identifiers follow `RPL-<UUID>`.
3. Every record references an existing execution.
4. Trigger types use the approved vocabulary.
5. Status values use the approved vocabulary.
6. Change types use the approved vocabulary.
7. Required fields are present.
8. At least one affected work item is identified.
9. All affected record references resolve to records in the same execution.
10. Referenced roles are valid for the execution.
11. Approved records reference an authorized decision.
12. The referenced decision is approved and authorizes the applicable changes.
13. Rejected, completed, and withdrawn records are terminal.
14. Status transitions follow the permitted lifecycle.
15. Changes to canonical records are consistent with the approved decision.
16. Completed records have evidence that the approved changes were implemented, where applicable.
17. Material status changes have corresponding history entries.
18. Approved changes cannot be silently modified.
19. Re-planning does not independently override artifact ownership or decision authority.
20. Historical records are not silently overwritten or deleted.

## 15. Implementation Boundary

This specification defines re-planning record structure and governance requirements.

It does not introduce:

- Automatic replanning.
- Automatic work-item reassignment.
- Automatic dependency changes.
- Automatic role activation.
- Automatic approval of plan changes.
- Automatic schedule estimation.
- A new universal approval authority.

Schemas and automated validation are deferred to Phase 1.4.7.

## 16. Acceptance Criteria

- Re-planning identifiers and execution ownership are explicit.
- Trigger types and change types are controlled.
- Lifecycle states and transitions are defined.
- Proposal, coordination, and approval responsibilities are distinct.
- Approval is traceable through canonical decision records.
- Affected work items and related records are traceable.
- Proposed changes are distinguishable from implemented changes.
- Approved changes update the appropriate canonical records.
- Impact assessment requirements are explicit.
- History preserves material changes.
- Re-planning does not override existing governance authority.
- Validation requirements are documented.
- Examples are clearly illustrative.