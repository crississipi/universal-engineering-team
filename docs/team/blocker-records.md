# Blocker Records

## 1. Purpose

Blocker records document issues, conditions, or constraints that prevent or materially restrict planned execution work.

They provide traceability for:

- What is blocking execution.
- Which work items or dependencies are affected.
- Who is responsible for coordinating resolution.
- What actions have been attempted.
- What evidence supports the blocker.
- Whether the blocker remains active or has been resolved.
- Whether replanning or escalation is required.

A blocker record documents an execution impediment. It does not automatically change work-item status, dependency status, role activation status, or workflow status.

Those records remain independently authoritative.

## 2. Canonical Location

**File:** `blockers.yml`

**Location:** `executions/<execution-id>/blockers.yml`

Each blocker record belongs to exactly one execution.

## 3. Blocker Identifier

Blocker identifiers must use:

`BLK-<UUID>`

Each blocker identifier must be unique across the repository.

An existing identifier must never be reassigned to another blocker.

## 4. Canonical Blocker Record

Each blocker record must contain:

| Field | Required | Description |
|---|---|---|
| `blocker_id` | Yes | Unique blocker identifier |
| `execution_id` | Yes | Parent execution identifier |
| `title` | Yes | Short descriptive title |
| `description` | Yes | Explanation of the impediment |
| `blocker_type` | Yes | Controlled blocker classification |
| `severity` | Yes | Impact classification |
| `status` | Yes | Current blocker lifecycle status |
| `reported_by_role` | Yes | Role that reported the blocker |
| `responsible_role` | Yes | Role accountable for coordinating resolution |
| `affected_work_item_ids` | Yes | Work items affected by the blocker |
| `affected_dependency_ids` | Optional | Dependencies affected by the blocker |
| `related_handoff_execution_ids` | Optional | Related handoff executions |
| `related_decision_ids` | Optional | Related decisions |
| `evidence_refs` | Optional | Supporting evidence identifiers |
| `resolution_summary` | Conditional | Explanation of how the blocker was resolved |
| `resolution_evidence_refs` | Conditional | Evidence supporting resolution |
| `created_at` | Yes | Record creation timestamp |
| `updated_at` | Yes | Last material update timestamp |
| `resolved_at` | Conditional | Actual resolution timestamp |
| `closed_at` | Conditional | Timestamp when verified closure was recorded |
| `history` | Yes | Material change history |

Required collections may be empty only when their absence is valid under the applicable rules. A blocker must identify at least one affected work item.

Conditional fields must be populated when their applicable status requires them.

Optional fields must be omitted when they do not apply.

## 5. Blocker Types

Use the following controlled vocabulary:

| Type | Description |
|---|---|
| `missing_input` | Required information or artifact is unavailable |
| `dependency` | A prerequisite dependency prevents progress |
| `handoff` | A producer-consumer transfer is blocked |
| `technical` | A technical issue prevents or restricts execution |
| `environment` | A development, testing, or operational environment issue |
| `security` | A security concern prevents safe execution |
| `external` | An external party, system, or service prevents progress |
| `resource` | Required personnel, capacity, or resources are unavailable |
| `approval` | An authorized decision or approval is outstanding |
| `scope` | Scope ambiguity or conflict prevents reliable execution |
| `other` | A blocker that does not fit another approved category |

The `other` classification requires a meaningful explanation.

New blocker types must be introduced through governance review rather than created arbitrarily.

## 6. Severity

Use the following severity levels:

| Severity | Description |
|---|---|
| `low` | Minor impediment with limited impact; work can generally continue |
| `medium` | Material restriction affecting one or more work items |
| `high` | Significant impediment affecting a critical execution path |
| `critical` | Severe impediment requiring immediate escalation or suspension of affected work |

Severity describes impact, not blocker lifecycle status.

A critical blocker does not automatically grant an individual role authority beyond its established governance responsibilities.

## 7. Blocker Status

The blocker lifecycle uses one canonical vocabulary across this specification,
the blocker overview, and the JSON Schema:

| Status | Description |
|---|---|
| `open` | Reported and awaiting assessment or action |
| `in_progress` | Resolution activities are actively underway |
| `blocked` | Resolution cannot currently proceed because another condition prevents it |
| `escalated` | Referred to the appropriate higher or specialist authority for a decision or intervention |
| `deferred` | Resolution has been intentionally postponed through an authorized decision |
| `resolved` | The impediment has been addressed and resolution information is recorded; affected work still requires reassessment |
| `closed` | Resolution has been verified, affected work reassessed, and no further blocker action is required |
| `cancelled` | The blocker is no longer applicable or was recorded in error |

Escalation does not mean the impediment is resolved or that affected work may
resume. The affected work remains blocked whenever its required conditions
remain unsatisfied.

### 7.1 Status Transitions

Only the following transitions are permitted:

| Current status | Permitted next statuses |
|---|---|
| `open` | `in_progress`, `blocked`, `escalated`, `resolved`, `deferred`, `cancelled` |
| `in_progress` | `blocked`, `escalated`, `resolved`, `deferred`, `cancelled` |
| `blocked` | `open`, `in_progress`, `escalated`, `resolved`, `deferred`, `cancelled` |
| `escalated` | `in_progress`, `blocked`, `resolved`, `deferred`, `cancelled` |
| `deferred` | `open`, `in_progress`, `blocked`, `escalated`, `resolved`, `cancelled` |
| `resolved` | `closed` |
| `closed` | Terminal |
| `cancelled` | Terminal |

A blocker may be escalated directly from `open`, `in_progress`, or
`blocked`; urgent risks must not wait for ordinary resolution attempts.
An escalated blocker may return to active resolution when the relevant
authority provides direction.

A blocker must reach `resolved` before it can be `closed`. Closing requires
verification and reassessment of affected work, not merely a proposed fix.

If a closed or cancelled blocker recurs, create a new blocker record and
reference the earlier record through a related record reference or history
entry. Do not silently reopen a terminal record.

### 7.2 Resolution and Closure Requirements

A blocker marked `resolved` must contain:

- `resolution_summary`
- `resolved_at`
- `resolution_evidence_refs`, when verifiable evidence is available

A blocker marked `closed` must contain:

- `resolution_summary`
- `resolved_at`
- `closed_at`
- At least one `resolution_evidence_refs` entry supporting verification

The resolution summary must describe what changed and why the impediment no
longer prevents the affected work. Closure evidence must support verification
that the resolution is effective and the affected work has been reassessed.

A blocker must not be marked resolved merely because someone has started
working on it. If resolution cannot be demonstrated, retain an appropriate
nonterminal status. A resolved blocker must not be closed until the affected
work owner confirms that the blocking condition no longer prevents safe and
correct execution.

### 7.3 Deferred and Cancelled Blockers

A blocker marked `deferred` must reference an authorized decision through
`related_decision_ids`. The decision must establish the rationale and any
applicable conditions for deferral. Deferral does not imply resolution.

A blocker marked `cancelled` must retain a history entry explaining why it
is no longer applicable or why it was recorded in error. Cancellation is
terminal and must not be used as a substitute for resolution.

## 8. Responsibility and Escalation

`reported_by_role` identifies the role that recorded the blocker.

`responsible_role` identifies the role accountable for coordinating its resolution.

The responsible role does not automatically acquire ownership of affected artifact packages.

Artifact ownership remains governed by:

`docs/team/ownership.yml`

Escalation must follow the existing responsibility and escalation rules.

The Delivery Lead coordinates cross-role execution and replanning but is not a universal technical, security, product, or approval authority.

A blocker requiring a decision must be linked to a canonical decision record rather than treating the blocker record itself as authorization.

## 9. Affected Work and Dependencies

Every blocker must identify at least one affected work item.

Affected work item identifiers must resolve to existing work items in the same execution.

`affected_dependency_ids` may reference dependencies affected by the blocker.

The dependency record remains authoritative for dependency status.

A blocker marked `resolved` does not automatically change an affected dependency to `satisfied`.

The dependency must be independently evaluated using the rules in:

`docs/team/dependency-execution-records.md`

Likewise, resolving a blocker does not automatically change affected work items from `blocked` to `ready` or `in_progress`.

The assigned work-item role must reassess the work item against its actual prerequisites.

## 10. Evidence References

Use `evidence_refs` to reference evidence supporting:

- The existence of the impediment.
- Its impact.
- Investigation findings.
- Resolution activities.
- Any remaining limitations.

Artifact package references are resolved against the canonical
artifact ownership catalog in `docs/team/ownership.yml`.

Artifact package identifiers are not execution-scoped record
identifiers. Their validation must not require them to appear in
the execution-specific record collections.

Evidence identifiers must resolve to canonical records in the same execution.

Evidence verification remains governed by:

`docs/team/evidence-records.md`

Do not treat an unverified evidence reference as verified proof.

## 11. History Requirements

The `history` collection must preserve material blocker changes.

Each history entry must contain:

| Field | Required | Description |
|---|---|---|
| `changed_at` | Yes | Timestamp of the change |
| `changed_by_role` | Yes | Role responsible for the change |
| `change_type` | Yes | Classification of the change |
| `reason` | Yes | Explanation for the change |
| `previous_status` | Conditional | Previous blocker status |
| `new_status` | Conditional | New blocker status |
| `changed_fields` | Optional | Other materially changed fields |

History must preserve:

- Initial reporting.
- Assessment.
- Responsibility changes.
- Severity changes.
- Status transitions.
- Escalation.
- Deferral.
- Resolution.
- Cancellation.

Historical information must not be silently overwritten or deleted.

## 12. Relationship to Re-planning

A blocker may require changes to the execution plan.

When replanning is necessary, create a canonical re-planning record in `replans.yml`.

Reference the blocker from the re-planning record.

A blocker record must not independently redefine:

- Work-item assignments.
- Dependency relationships.
- Role activation.
- Workflow stages.
- Artifact ownership.
- Approved scope.

Those changes must be recorded through their respective canonical records and authorized governance processes.

## 13. Illustrative YAML Structure

The following example is illustrative only. It is not an actual execution record.

```yaml
blockers:
  - blocker_id: "BLK-<UUID>"
    execution_id: "EXE-<UUID>"

    title: "External API credentials unavailable"

    description: >
      Required credentials for the external integration
      environment have not been provided.

    blocker_type: "missing_input"
    severity: "high"
    status: "open"

    reported_by_role: "integration-engineer"
    responsible_role: "integration-engineer"

    affected_work_item_ids:
      - "WI-<UUID>"

    affected_dependency_ids:
      - "DEP-<UUID>"

    related_handoff_execution_ids: []

    evidence_refs: []

    created_at: "2026-11-02T10:00:00Z"
    updated_at: "2026-11-02T10:00:00Z"

    history:
      - changed_at: "2026-11-02T10:00:00Z"
        changed_by_role: "integration-engineer"
        change_type: "created"
        reason: "Required external integration credentials are unavailable."
```

The identifiers above are placeholders. Actual records must use real identifiers and references.

## 14. Validation Requirements

The future blocker validator must enforce:

1. Blocker identifiers are unique.
2. Blocker identifiers follow `BLK-<UUID>`.
3. Every blocker references an existing execution.
4. Blocker types use the approved vocabulary.
5. Severity values use the approved vocabulary.
6. Status values use the approved vocabulary.
7. Required fields are present.
8. Every blocker references at least one existing affected work item.
9. Affected work items belong to the same execution.
10. Affected dependency references resolve to dependencies in the same execution.
11. Related handoff and decision references resolve to canonical records.
12. Evidence references resolve to evidence records in the same execution.
13. Referenced roles are valid for the execution.
14. Status transitions follow the permitted transition rules.
15. Resolved blockers include resolution information and a resolution timestamp.
16. Deferred blockers reference an authorized decision.
17. Closed blockers include closure timestamp and verification evidence.
18. Material status changes have corresponding history entries.
19. Terminal records are not silently reopened.
20. A blocker does not independently change dependency or work-item status.
21. Resolution does not automatically imply dependency satisfaction or work-item completion.
22. Historical records are not silently overwritten or deleted.

## 15. Implementation Boundary

This specification defines blocker record structure and governance requirements.

It does not introduce:

- Automatic blocker detection.
- Automatic escalation.
- Automatic work-item reassignment.
- Automatic dependency satisfaction.
- Automatic workflow transitions.
- A new universal approval authority.

Schemas and automated validation are deferred to Phase 1.4.7.

## 16. Acceptance Criteria

- Blocker identifiers and execution ownership are explicit.
- Blocker classifications and severity are controlled.
- Lifecycle states and transitions are defined.
- Reporting and resolution responsibilities are explicit.
- Affected work items and dependencies are traceable.
- Evidence and decision references use canonical identifiers.
- Resolution and deferral requirements are explicit.
- History preserves material changes.
- Replanning is handled through canonical re-planning records.
- Blockers do not independently override other record authorities.
- Validation requirements are documented.
- Examples are clearly illustrative.
