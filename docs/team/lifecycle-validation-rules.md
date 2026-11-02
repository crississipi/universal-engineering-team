# Execution Lifecycle and State-Transition Validation

## 1. Purpose

This document defines the deterministic lifecycle checks implemented for
Phase 1.4.7.4. It supplements the canonical record specifications and
`execution-validation-architecture.md`.

The validator is:

`scripts/validate-execution-lifecycle.py`

It validates one execution directory and is read-only. It does not update
record values, create missing history, approve decisions, resolve blockers,
or infer that a transition occurred.

## 2. Invocation and Scope

Run from the repository root:

```powershell
python scripts/validate-execution-lifecycle.py "executions/EXE-<uuid>"
```

The supplied execution directory must be a direct child of `executions/`
and contain the ten canonical YAML record files with their documented
top-level wrappers.

The validator checks lifecycle state values, explicit transition history,
history chronology, current-state consistency, and status-specific
requirements. JSON Schema and cross-record reference validation remain
separate layers.

## 3. Shared History and Timestamp Rules

All canonical records must have valid UTC `created_at` and `updated_at`
timestamps. History timestamps must be timezone-aware UTC timestamps and
must be chronological.

The validator checks that:

- A history entry is a mapping.
- Its record-specific timestamp field is valid.
- Its `reason` is a non-empty explanation.
- History does not begin before `created_at`.
- `updated_at` is not earlier than `created_at` or the latest history event.
- Where a history entry records a new lifecycle value, the latest recorded
  value agrees with the current record field.
- Where both previous and new lifecycle values are recorded, the previous
  value agrees with the preceding recorded lifecycle value.

The canonical timestamp field varies by record type:

| Record | History timestamp field |
|---|---|
| Execution, work item, role activation, handoff, decision, evidence, blocker, replan | `changed_at` |
| Dependency | `timestamp` |
| Closure | `occurred_at` |

The validator does not manufacture an initial status or infer an omitted
historical transition. The current state remains authoritative when the
history does not contain a corresponding status event; required history
structure and timestamps are still checked.

## 4. Overall Workflow Status and Stage

The execution's `workflow_status` must use the canonical vocabulary from
`workflow-lifecycle.md`. Its `workflow_stage` must use the canonical
machine-readable stage identifiers from
`execution-identity-and-traceability.md`.

Recorded overall workflow status transitions are checked against the
governed transition rules. A transition out of `blocked` must resume the
most recent non-blocked status recorded for that execution.

Workflow stage history is checked for continuity and agreement with the
current stage. The validator deliberately does not impose a strict numeric
stage order: the workflow is adaptable, and skipping a stage does not
authorize skipping its required decisions, dependencies, verification, or
approval gates.

When `final_disposition` is present or required by the terminal workflow
status, its status must match the current workflow status and it must
contain a summary and UTC `recorded_at` timestamp.

## 5. Work-Item State Transitions

The validator enforces the exact transitions in
`blockers-replanning-and-state-transitions.md`:

| Current state | Permitted next states |
|---|---|
| `not_started` | `ready`, `cancelled` |
| `ready` | `in_progress`, `blocked`, `cancelled` |
| `in_progress` | `blocked`, `in_review`, `completed`, `cancelled` |
| `blocked` | `ready`, `cancelled` |
| `in_review` | `completed`, `changes_requested`, `blocked` |
| `changes_requested` | `ready`, `blocked`, `cancelled` |
| `completed` | Terminal |
| `cancelled` | Terminal |

Each recorded transition must have a previous and new state, must be
permitted, and must continue from the preceding recorded state.

A work item in `completed` state requires UTC `completed_at`. The
timestamp must not precede `created_at` or be later than `updated_at`.
`completed_at` must be omitted for other current states. Optional
`planned_completion_at`, when present, must be a UTC timestamp.

A work item in `cancelled` state must reference at least one related
approved scope or planning decision. The validator checks that the decision
is approved; it does not infer that the decision-maker had authority beyond
the canonical decision-authority governance.

## 6. Role Activation

The validator checks classification/status compatibility:

| Classification | Permitted activation status |
|---|---|
| `required` | `planned`, `active`, `completed`, `deactivated` |
| `conditional` | `planned`, `active`, `completed`, `deactivated`, `not_activated` |
| `optional` | `planned`, `active`, `completed`, `deactivated`, `not_activated` |
| `not_activated` | `not_activated` |

Conditional activation must have a boolean `activation_trigger_applies`.
A false trigger requires `not_activated`; a true trigger cannot be
`not_activated`.

Current `active`, `completed`, and `deactivated` statuses require
`activated_at`. A `completed` status requires `completed_at`; a
`deactivated` status requires `deactivated_at`.

The governance permits reactivation but does not define a complete
activation-status transition matrix. The validator therefore checks
activation history chronology, continuity where prior/new values are
recorded, and agreement between the latest recorded status and the current
status. It does not invent a stricter activation transition matrix.

## 7. Dependency Status

The validator enforces relationship/status compatibility:

- `not_applicable` is valid only for `conditional_input`.
- A `not_applicable` conditional dependency must retain its
  `activation_condition`.
- Recorded status changes must follow the dependency transition table in
  `dependency-execution-records.md`.
- The latest recorded status must agree with the current dependency status.

The dependency transition table is:

| Current status | Permitted next status |
|---|---|
| `planned` | `active`, `not_applicable`, `cancelled` |
| `active` | `satisfied`, `blocked`, `cancelled` |
| `blocked` | `active`, `satisfied`, `cancelled` |
| `satisfied` | `active`, `cancelled` |
| `not_applicable` | `active`, `cancelled` |
| `cancelled` | Terminal |

## 8. Handoff Execution

The validator enforces the handoff lifecycle transition table in
`handoff-execution-records.md`. It also checks:

- Submission records are mappings and their `submitted_at` timestamps
  are valid UTC timestamps in chronological order.
- `submitted`, `partially_accepted`, `accepted`, and `rejected`
  statuses require `current_submission_id`.
- `partially_accepted`, `accepted`, and `rejected` statuses require
  `current_decision_id`.
- Recorded status history is continuous and agrees with `current_status`.

The validator does not treat submission as acceptance. Canonical decision
outcomes and the identity of the current submission are checked by the
cross-record validator.

## 9. Decision Lifecycle

The validator enforces the decision transition table in
`decision-records.md`:

| Current status | Permitted next status |
|---|---|
| `proposed` | `under_review`, `withdrawn` |
| `under_review` | `approved`, `rejected`, `withdrawn` |
| `approved` | `superseded` |
| `rejected` | Terminal |
| `superseded` | Terminal |
| `withdrawn` | Terminal |

Approved and rejected decisions require `decided_at` and
`decided_by_role`. Decisions still proposed, under review, or withdrawn
must not carry `decided_at`. A superseded decision retains its original
decision timestamp and authority information.

Decision authority itself is not inferred from the role slug. It remains
governed by the applicable responsibility and decision-authority rules.

## 10. Evidence Verification Status

The validator checks that evidence uses one of the canonical values:

- `unverified`
- `verified`
- `invalid`
- `superseded`

It checks status history continuity and current-state agreement.
`verified` evidence requires `verified_by_role` and non-empty
`verification_notes`. `invalid` evidence requires non-empty
`verification_notes`.

A superseded evidence record must be referenced by a newer record through
that newer record's `supersedes_evidence_id`. This follows the direction
defined in `evidence-records.md`; the older record does not point forward
through its own `supersedes_evidence_id`.

The evidence specification does not define a complete transition matrix,
so the validator does not invent one. Evidence provenance and substantive
verification adequacy remain review responsibilities.

## 11. Blocker Lifecycle

The validator enforces the blocker transition table in
`blocker-records.md`:

| Current status | Permitted next status |
|---|---|
| `open` | `in_progress`, `blocked`, `resolved`, `deferred`, `cancelled` |
| `in_progress` | `blocked`, `resolved`, `deferred`, `cancelled` |
| `blocked` | `open`, `in_progress`, `deferred`, `cancelled` |
| `deferred` | `open`, `in_progress`, `cancelled` |
| `resolved` | Terminal |
| `cancelled` | Terminal |

A resolved blocker requires a non-empty `resolution_summary` and UTC
`resolved_at`. `resolved_at` is omitted for other current statuses.
A deferred blocker must reference a related approved decision.

## 12. Replanning Lifecycle

The validator enforces the transition table in `replanning-records.md`:

| Current status | Permitted next status |
|---|---|
| `proposed` | `under_review`, `withdrawn` |
| `under_review` | `approved`, `rejected`, `withdrawn` |
| `approved` | `in_progress`, `completed` |
| `in_progress` | `completed` |
| `rejected` | Terminal |
| `completed` | Terminal |
| `withdrawn` | Terminal |

Approved, in-progress, and completed replans require an approved
authorizing decision. A completed replan requires UTC `implemented_at`;
that timestamp is omitted for other statuses. The approved changes must
still be reconciled with the affected canonical records by review and
cross-record validation.

## 13. Closure Lifecycle

The validator enforces the closure transition table in
`closure-records.md`:

| Current status | Permitted next status |
|---|---|
| `not_started` | `in_preparation`, `cancelled` |
| `in_preparation` | `in_review`, `blocked`, `cancelled` |
| `in_review` | `in_preparation`, `blocked`, `closed`, `cancelled` |
| `blocked` | `in_preparation`, `cancelled` |
| `closed` | Terminal |
| `cancelled` | Terminal |

A closed execution requires:

- Completion status `complete` or `complete_with_exceptions`.
- Verification status `passed` or `passed_with_exceptions`.
- An approved `execution_closure` decision.
- UTC `closed_at`.
- A `closure_status_changed` history event whose new value is `closed`.
- A `closure_approved` history event that references the closure decision.
- The closure event timestamp to agree with `closed_at`.

A cancelled execution requires an approved cancellation decision and a
`closure_cancelled` or status-change history event recording cancellation.
A cancelled execution is not represented as successfully completed.
When `closure_authorized_by_role` is supplied for a closed execution, it
must match the approved closure decision's `decided_by_role`; the matching
role identifier does not independently prove decision authority.

Completion and verification exceptions must be represented by approved
exception records. The cross-record validator separately resolves their
decision references and checks decision approval.

## 14. Findings and Exit Behavior

Findings use stable `LIFE###` codes and the shared validation reporter.

- Exit code `0`: no lifecycle errors were found.
- Exit code `1`: one or more lifecycle errors were found.
- Exit code `2`: invocation or execution-directory failure prevents
  reliable validation.

A pass means only that the deterministic lifecycle checks implemented by
this script passed. It does not establish JSON Schema validity,
cross-record validity, substantive decision authority, evidence quality,
security adequacy, or human approval.

## 15. Explicit Non-Goals

This validator does not:

- Rewrite record statuses or history.
- Infer missing historical transitions.
- Infer workflow stage progression from a strict waterfall.
- Invent a role-activation or evidence transition matrix where governance
  has not defined one.
- Judge whether evidence is persuasive or sufficient for a qualitative
  claim.
- Determine whether a decision-maker has authority merely from their role
  identifier.
- Approve a handoff, exception, replan, release, or execution closure.
- Replace JSON Schema or cross-record validation.
