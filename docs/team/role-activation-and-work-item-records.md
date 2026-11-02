# Role Activation and Work-Item Records

## 1. Purpose

This document defines the canonical record structure and traceability rules for role activations and work items within an execution.

It supplements:

- `role-activation-rules.md`
- `execution-record-model.md`
- `execution-identity-and-traceability.md`
- `blockers-replanning-and-state-transitions.md`
- `docs/team/ownership.yml`

It defines how actual role participation and individual units of work are recorded without changing existing ownership, responsibility, workflow, or handoff governance.

This document defines record policy and conceptual field requirements. Exact YAML schemas and automated validation are deferred to Phase 1.4.7.

## 2. Governing Principles

1. Role activation and work-item records belong to one execution.
2. Every record must have a stable, unique identifier.
3. Every record must explicitly reference its `execution_id`.
4. Role activation must follow the existing 17-role activation rules.
5. Work items must have exactly one assigned role responsible for coordinating and completing the defined work.
6. Work-item assignment does not transfer artifact ownership.
7. A role must be activated before being assigned execution work.
8. Work-item dependencies must follow the dependency execution rules.
9. Work-item states must follow the existing state-transition rules.
10. Material record changes must preserve an auditable history.
11. Records must describe actual decisions and work, not assumed or fabricated activity.
12. Missing information must remain explicitly unresolved rather than being invented.

## 3. Role Activation Records

### 3.1 Purpose

A role activation record documents whether a canonical engineering role participates in a specific execution and the reason for that decision.

It provides traceability between role activation policy, actual participation, and the work items assigned to that role.

### 3.2 Record Identity

Each role activation record must have:

- A unique `activation_id`.
- The parent `execution_id`.
- The canonical `role_id`.

Use the following identifier format:

`ACT-<UUID>`

The UUID must use lowercase canonical format with hyphens.

### 3.3 Activation Classification

The `classification` field must use the existing vocabulary:

| Value | Meaning |
|---|---|
| `required` | Participation is necessary for the applicable task or progression gate. |
| `conditional` | Participation depends on a documented trigger. |
| `optional` | Specialist participation may improve the outcome but is not necessary. |
| `not_activated` | No applicable participation is expected for the execution. |

Do not introduce alternative classification values.

### 3.4 Activation Status

The `activation_status` field records the actual participation condition:

| Value | Meaning |
|---|---|
| `planned` | Activation has been decided, but participation has not started. |
| `active` | The role is currently participating. |
| `completed` | The role's assigned participation has been completed. |
| `deactivated` | Participation has ended before or after completion, with a documented reason. |
| `not_activated` | The role will not participate in this execution. |

Classification and activation status are separate:

- Classification explains why the role is required, conditional, optional, or excluded.
- Activation status describes what happened to its participation.

A role classified as `required` must not be silently marked `not_activated` to bypass a required responsibility or progression gate.

### 3.4.1 Classification and Status Compatibility

The classification and activation status must represent a logically consistent activation decision.

The following combinations are permitted:

| Classification | Permitted activation status |
|---|---|
| `required` | `planned`, `active`, `completed`, `deactivated` |
| `conditional` | `planned`, `active`, `completed`, `deactivated`, `not_activated` |
| `optional` | `planned`, `active`, `completed`, `deactivated`, `not_activated` |
| `not_activated` | `not_activated` |

A conditional role may be marked `not_activated` when its documented trigger does not apply.

An optional role may be marked `not_activated` when participation is not considered necessary.

A required role must not be marked `not_activated`. If required participation cannot proceed, record the blocker and escalate according to the existing governance rules.

A classification change must be recorded in the activation history with its reason.

### 3.5 Required Information

A role activation record must capture:

- Activation ID.
- Execution ID.
- Canonical role ID.
- Activation classification.
- Activation status.
- Reason for the activation decision.
- Participation scope.
- Applicable activation trigger, when conditional.
- Linked work-item IDs, when work items exist.
- Activation and deactivation timestamps, when applicable.
- Material change history.

For conditional participation, record the trigger and whether it applies.

For optional participation, explain why the role was activated or why its participation was unnecessary.

For `not_activated`, record the reason no participation is expected.

### 3.5.1 Canonical Role Activation Fields

The top-level key in `role-activations.yml` is `role_activations`,
whose value is an array of role activation records.

| Field | Requirement | Definition |
|---|---|---|
| `activation_id` | Required | Stable `ACT-<UUID>` identifier. |
| `execution_id` | Required | Parent execution identifier. |
| `role_id` | Required | Canonical role slug from `expected-roles.yml`. |
| `classification` | Required | `required`, `conditional`, `optional`, or `not_activated`. |
| `activation_status` | Required | Canonical activation status. |
| `reason` | Required | Reason for the activation or non-activation decision. |
| `participation_scope` | Required | Description of the role's expected or actual participation boundary. |
| `activation_trigger` | Conditional | Trigger description; required when classification is `conditional`. |
| `activation_trigger_applies` | Conditional | Boolean indicating whether the conditional trigger applies; required when classification is `conditional`. |
| `work_item_ids` | Optional | Work-item identifiers associated with this activation. |
| `activated_at` | Optional | UTC timestamp when participation became active. |
| `deactivated_at` | Conditional | UTC timestamp when participation ended; required when status is `deactivated`. |
| `completed_at` | Conditional | UTC timestamp when the role completed its participation; required when status is `completed`. |
| `created_at` | Required | UTC timestamp when the activation record was created. |
| `updated_at` | Required | UTC timestamp of the latest material update. |
| `history` | Required | Chronological history of material changes. |

For classifications other than `conditional`, omit
`activation_trigger` and `activation_trigger_applies`. Do not use
`null` to represent an inapplicable conditional field.

When classification is `conditional`, both trigger fields are required.
If `activation_trigger_applies` is `false`, the activation status must
be `not_activated`. If it is `true`, the status must be one of
`planned`, `active`, `completed`, or `deactivated`.

For lifecycle timestamps:

- `activated_at` is required when status is `active`, `completed`,
  or `deactivated`.
- `deactivated_at` is required when status is `deactivated`.
- `completed_at` is required when status is `completed`.
- These timestamps are omitted when their corresponding event has not
  occurred.

The compatibility between `classification` and
`activation_status` remains a cross-record/governance validation rule,
not merely an enum check.

Each activation history entry contains:

- `changed_at`: UTC timestamp.
- `changed_by_role`: canonical role slug responsible for the change.
- `change_type`: concise change description.
- `reason`: explanation for the change.
- `previous_values`: optional object containing prior values.
- `new_values`: optional object containing resulting values.
- `related_record_ids`: optional array of related canonical IDs.

The initial history entry records creation. History entries must be
chronological and must not replace the current record fields.

The illustrative collection shape is:

```yaml
role_activations:
  - activation_id: "ACT-<UUID>"
    execution_id: "EXE-<UUID>"
    role_id: "solution-architect"
```

This is a structural excerpt only; it omits other required fields.

### 3.6 Activation and Deactivation

Role activation may change during execution.

When new information, risks, defects, dependencies, or scope changes require specialist participation:

1. Update the activation decision.
2. Record the reason and applicable trigger.
3. Update the activation status.
4. Create or assign the relevant work items.
5. Preserve the previous decision in the record history.

A role may be deactivated when its relevant participation is complete and no unresolved responsibility, required review, dependency, or risk remains.

Deactivation does not remove historical work items or evidence.

Reactivation must be recorded as a material change with its reason. It must not erase the previous participation history.

### 3.7 Activation Constraints

- Only canonical roles from the expected-role manifest may be recorded.
- Do not create duplicate active activation records for the same role within one execution.
- Do not automatically create records for all 17 roles.
- Record roles that were actually evaluated or activated according to the task's planning and activation process.
- Do not treat a contributor's eligibility as proof of actual participation.
- Activation does not automatically establish a formal handoff.

## 4. Work-Item Records

### 4.1 Purpose

A work-item record represents a specific, identifiable unit of work performed during an execution.

Work items provide traceability between planned responsibilities, assigned roles, dependencies, implementation or analysis outputs, verification evidence, and completion.

A work item may represent:

- Requirements analysis.
- Architecture investigation.
- API contract definition.
- Backend or frontend implementation.
- Database design or migration work.
- Integration implementation.
- Test planning or execution.
- Security assessment.
- Performance investigation.
- Accessibility assessment.
- Infrastructure or deployment work.
- Documentation.
- Release preparation.
- Delivery coordination.

These examples do not require every category to exist in every execution.

### 4.2 Record Identity

Each work item must have:

- A unique `work_item_id`.
- The parent `execution_id`.

Use the following identifier format:

`WI-<UUID>`

The UUID must use lowercase canonical format with hyphens.

Work-item identifiers must remain stable when titles, descriptions, assignments, or states change.

### 4.3 Required Information

A work-item record must capture:

- Work-item ID.
- Execution ID.
- Title.
- Objective or description.
- Assigned role.
- Current work-item state.
- Acceptance criteria or completion conditions.
- Creation timestamp.
- Last-updated timestamp.
- Material change history.
- Assigned role activation ID (`activation_id`).

The assigned role and `activation_id` must reference the same canonical role activation record within the same execution.

The referenced activation may have an `activation_status` of `planned` or `active` when the work item is assigned.

The activation must have an `activation_status` of `active` before the assigned role begins executing the work item.

### 4.3.1 Canonical Work-Item Fields

The top-level key in `work-items.yml` is `work_items`, whose value
is an array of work-item records.

| Field | Requirement | Definition |
|---|---|---|
| `work_item_id` | Required | Stable `WI-<UUID>` identifier. |
| `execution_id` | Required | Parent execution identifier. |
| `title` | Required | Short human-readable work-item title. |
| `objective` | Required | Specific objective of the work item. |
| `assigned_role` | Required | Canonical role slug responsible for the work item. |
| `activation_id` | Required | Activation record for the assigned role in this execution. |
| `state` | Required | Canonical work-item state. |
| `acceptance_criteria` | Required | Non-empty array of observable completion conditions. |
| `created_at` | Required | UTC timestamp when the work item was created. |
| `updated_at` | Required | UTC timestamp of the latest material update. |
| `history` | Required | Chronological history of material changes. |
| `artifact_id` | Optional | Related canonical artifact package ID. |
| `scope_boundaries` | Optional | Array of concise scope boundary statements. |
| `contributor_roles` | Optional | Array of canonical role slugs that contribute without becoming co-owners. |
| `dependency_ids` | Optional | Related dependency record identifiers. |
| `input_refs` | Optional | References to inputs used by the work item. |
| `output_refs` | Optional | References to outputs produced by the work item. |
| `evidence_refs` | Optional | Related evidence record identifiers. |
| `related_decision_ids` | Optional | Related decision record identifiers. |
| `related_blocker_ids` | Optional | Related blocker record identifiers. |
| `related_handoff_execution_ids` | Optional | Related handoff execution identifiers. |
| `external_references` | Optional | References to relevant external resources. |
| `planned_completion_at` | Optional | Planned completion timestamp, when established. |
| `completed_at` | Optional | Actual completion timestamp; present only after completion. |

The canonical field name for the work objective is `objective`;
the canonical assigned-role field is `assigned_role`; and the
canonical completion-condition field is `acceptance_criteria`.
Do not introduce aliases such as `description`,
`assigned_role_id`, or `completion_conditions`.

#### Input and output reference objects

Each item in `input_refs` and `output_refs` is an object containing:

- `reference_type`: one of `artifact`, `work_item`,
  `role_activation`, `dependency`, `handoff_execution`,
  `decision`, `evidence`, `blocker`, `replan`, or `external`.
- `reference_id`: identifier of the referenced resource.
- `description`: optional explanation of the relationship.
- `uri`: optional URI when a directly addressable resource exists.

The referenced resource must be traceable. For an `external`
reference, `reference_id` is the external identifier; `uri` may
also be supplied. For internal reference types, the identifier must
resolve to the corresponding canonical record or artifact catalog.

#### Work-item history entries

Each history entry contains:

- `changed_at`: UTC timestamp.
- `changed_by_role`: canonical role slug responsible for the change.
- `change_type`: concise change description.
- `reason`: explanation for the change.
- `previous_values`: optional object containing prior values.
- `new_values`: optional object containing resulting values.
- `related_record_ids`: optional array of related canonical IDs.

The initial history entry records creation. History entries must be
chronological and must not replace the current record fields.

The illustrative collection shape is:

```yaml
work_items:
  - work_item_id: "WI-<UUID>"
    execution_id: "EXE-<UUID>"
    title: "Define API contract"
    objective: "Publish the approved API contract."
    assigned_role: "api-manager"
    activation_id: "ACT-<UUID>"
    state: "not_started"
    acceptance_criteria:
      - "The API contract has been reviewed and approved."
```

This is a structural excerpt only; it omits timestamps and history
required by the canonical record.

### 4.4 Optional and Conditional Information

When applicable, a work-item record may also contain:

- Related artifact package ID.
- Scope boundaries.
- Contributor roles.
- Dependency record IDs (`dependency_ids`).
- Input references.
- Output references.
- Evidence references.
- Related decision IDs.
- Related blocker IDs.
- Related handoff execution IDs.
- Relevant external references.
- Planned or actual completion timestamps.

Optional fields must be omitted when they do not apply or are not known.

Do not invent references merely to populate a record.

### 4.5 Work-Item Assignment

Every work item must have one assigned role responsible for coordinating and completing the defined work.

The assigned role:

- Must be activated for the execution.
- Must operate within its defined responsibility boundaries.
- Must respect the ownership of affected artifact packages.
- Must provide the required outputs and completion evidence.
- Must communicate blockers and dependency changes.

Contributor roles may assist with the work.

Contributors do not become co-owners of the work item or the related artifact package merely through participation.

The assigned role does not automatically become the accountable owner of an artifact package.

The owner declared in `docs/team/ownership.yml` remains accountable for that package.

### 4.6 Work-Item States

The `state` field must use the existing canonical work-item state vocabulary:

| State | Meaning |
|---|---|
| `not_started` | Work has been identified but has not begun. |
| `ready` | Required prerequisites are satisfied and work may begin. |
| `in_progress` | Work is actively being performed. |
| `blocked` | Work cannot proceed because of an unresolved blocker. |
| `in_review` | Work is awaiting the required review or assessment. |
| `changes_requested` | Review identified changes that must be addressed. |
| `completed` | Defined work and its completion conditions have been satisfied. |
| `cancelled` | Work has been formally cancelled with a recorded reason. |

Do not introduce alternative work-item states.

Allowed transitions and their required evidence are governed by:

`blockers-replanning-and-state-transitions.md`

A work item must not be marked `completed` merely because implementation has stopped or an output has been submitted.

Completion must satisfy the work item's defined conditions.

### 4.7 Acceptance and Completion Conditions

Each work item must have observable completion conditions appropriate to its scope.

Examples include:

- A reviewed requirements specification.
- An approved architecture decision.
- A published API contract.
- An implemented and tested feature.
- A completed migration with verification evidence.
- A documented security finding and retest result.
- A verified accessibility remediation.
- A completed release checklist.

Completion conditions must not contradict the parent artifact package's acceptance requirements or established specialist authority.

A work item may be completed while its parent artifact package remains in progress.

Likewise, completing one work item does not automatically complete an entire artifact package or execution.

## 5. Relationship Between Role Activations and Work Items

Role activation records and work-item records are separate record types with explicit references.

The relationship is:

- One execution may have multiple role activation records.
- One execution may have multiple work-item records.
- One activated role may be assigned multiple work items.
- A work item has one assigned role.
- A work item may have contributor roles when justified.
- A role activation record may reference multiple work items.
- A work item must reference an activated role from the same execution.

A role activation does not require a work item immediately when participation consists of consultation or a decision that has not yet produced a discrete task.

When actionable work is identified, create a work item and associate it with the applicable activation record.

Do not create duplicate work items merely because several roles collaborate on one unit of work.

Split work into separate items when independent assignment, dependencies, acceptance, or completion tracking is necessary.

## 6. Relationship to Artifact Ownership

Work-item responsibility must remain distinct from artifact package ownership.

The following rules apply:

1. The artifact owner remains accountable according to `docs/team/ownership.yml`.
2. The assigned work-item role coordinates the specific unit of work.
3. Contributors may perform work without becoming package owners.
4. A work item affecting multiple packages must identify the relevant artifact references when applicable.
5. A work-item record must not redefine package ownership.
6. Ownership changes must follow the existing ownership governance process.

A work item may be assigned to a contributor role while the accountable package owner retains responsibility for the resulting package.

## 7. Relationship to Dependencies and Handoffs

Work-item dependencies must be represented by explicit dependency records within the applicable execution.

Work items may reference their associated dependency records through `dependency_ids`. The dependency records remain the authoritative source for predecessor, successor, relationship type, condition, and dependency status.

Dependency relationships must follow:

`dependency-execution-rules.md`

The execution dependency graph must remain acyclic.

A work item must not be marked `ready` when a required prerequisite remains unresolved, unless the documented provisional-output rules explicitly permit the work to proceed.

Formal cross-role handoffs must reference their applicable handoff contract and execution record.

A dependency does not automatically constitute a formal handoff.

A role activation does not automatically constitute a dependency.

## 8. History and Traceability

Role activation and work-item records must preserve current values and an auditable history of material changes.

Material changes include:

- Activation classification or status changes.
- Activation or deactivation decisions.
- Assignment changes.
- Scope changes.
- Acceptance-condition changes.
- Work-item state transitions.
- Dependency changes.
- Output or evidence reference changes.
- Completion or cancellation decisions.

History entries should capture:

- Changed field or decision.
- Previous value, when available.
- New value.
- Timestamp.
- Actor or responsible role.
- Reason or supporting reference.

History must not be used to fabricate events or imply that an action occurred when it did not.

This model is auditable current-state tracking. It is not a requirement to implement full event sourcing.

## 9. Record Relationships

The conceptual relationships are:

```text
Execution
|
+-- Role Activations
|   |
|   +-- Role Activation Record
|       +-- Assigned Work Item IDs
|
+-- Work Items
    |
    +-- Assigned Role
    +-- Contributor Roles
    +-- Artifact References
    +-- Dependency References
    +-- Input References
    +-- Output References
    +-- Evidence References
    +-- Decision References
    +-- Blocker References
    +-- Handoff Execution References
```

All references must resolve to the appropriate records or governed identifiers.

A missing or unresolved reference must be reported rather than silently repaired.

## 10. Record Storage

Role activation and work-item records use the existing execution directory convention:

```text
executions/
+-- <execution-id>/
    +-- execution.yml
    +-- role-activations.yml
    +-- work-items.yml
```

The two record files contain the collections of their respective record types for that execution.

Do not create separate directories for each role or work item unless a future storage decision explicitly requires it.

Reusable policies and schemas remain outside actual execution directories.

## 11. Relationship to Existing Governance

This document does not replace:

- Role definitions and specialist responsibility boundaries.
- Role activation and participation rules.
- Artifact package ownership.
- Producer-consumer relationships.
- Handoff contracts and acceptance rules.
- Dependency execution rules.
- Work-item state transitions.
- Blocker and replanning governance.
- Project, change, and execution identity requirements.

Where a conflict appears, the established governing document for that subject remains authoritative until the conflict is formally resolved.

## 12. Future Schemas and Validation

Exact YAML schemas and automated validation are deferred to Phase 1.4.7.

The future validators should verify, where practical:

- Unique activation and work-item IDs.
- Valid execution references.
- Valid canonical role IDs.
- Valid activation classifications and statuses.
- Valid work-item states.
- Valid `activation_id` references for assigned work items.
- Consistency between the assigned role and the referenced activation record.
- Activation status eligibility when work is assigned or begins.
- Classification and activation-status compatibility.
- Valid artifact and record references.
- Valid dependency references.
- No duplicate active activation records for the same role within an execution.
- Required fields and conditional field requirements.
- Valid timestamps and auditable history structure.

Validators must report invalid or ambiguous records.

They must not invent assignments, activation decisions, dependencies, completion evidence, or history.

## 13. Maintenance

Changes to these record structures must preserve stable identifiers and historical references.

Any future change to activation classifications, activation statuses, work-item states, or record relationships must be reviewed against the existing governance documents before implementation.