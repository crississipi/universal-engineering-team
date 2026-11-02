# Dependency-Aware Execution and Parallel Work

## 1. Purpose

This document defines how work is sequenced, coordinated, and executed when tasks have dependencies or can proceed in parallel.

It establishes rules for:

- Identifying dependencies between work items.
- Distinguishing required, conditional, and feedback relationships.
- Determining whether work can proceed independently.
- Managing upstream outputs that are incomplete or not yet accepted.
- Preventing dependency cycles from creating execution deadlocks.
- Coordinating parallel work and integration.
- Replanning when dependencies change or work becomes blocked.

This document governs execution planning. It does not replace artifact ownership, responsibility boundaries, role activation, producer-consumer relationships, or formal handoff contracts.

## 2. Governing principles

### 2.1 Dependencies must be explicit

A work item must not be treated as dependent on another item merely because the work involves related roles or artifact packages.

Record a dependency when an identifiable output, decision, condition, or verification result is needed by another work item.

### 2.2 Distinguish collaboration from execution dependency

Roles may collaborate in both directions. For example, an implementation specialist may provide feedback to an architect, and the architect may provide clarification in return.

This does not mean the execution dependency graph must contain a cycle.

The collaboration graph may be bidirectional or cyclic. The graph used to determine execution prerequisites must be acyclic.

### 2.3 Block only what is actually dependent

A blocked work item must not automatically block every task in the project.

Only work items that require the blocked output, decision, or condition are prevented from proceeding.

Independent work should continue when doing so is safe and useful.

### 2.4 Preserve package ownership

Dependency coordination does not transfer artifact ownership.

The accountable owner declared in `docs/team/ownership.yml` remains responsible for the corresponding artifact package.

### 2.5 Partial work may proceed under controlled conditions

A consumer may begin work using an incomplete upstream output when the available portion is sufficiently stable and the remaining uncertainty is understood.

The consumer must not treat provisional information as an accepted final contract or silently assume missing details.

### 2.6 Safety and correctness take priority over parallelism

Do not parallelize work when doing so would bypass required approvals, expose sensitive data, create unsafe changes, or undermine data integrity.

### 2.7 Dependencies must be reassessed

Dependencies may change when scope, architecture, implementation findings, risks, or acceptance conditions change.

Update the execution plan rather than continuing against outdated assumptions.

## 3. Dependency relationship types

Use the relationship types established in `docs/team/producer-consumer-matrix.md`.

### 3.1 `required_input`

The consumer requires a specific upstream output, decision, or condition before it can proceed through the dependent work or relevant progression gate.

Rules:

- Identify the exact required output.
- Identify the producing work item or accountable package owner.
- Identify the consuming work item.
- Do not pass the dependent gate while the required input is unavailable or unacceptable.
- Unrelated work may continue.

A required input does not necessarily prevent all preliminary investigation or planning. It prevents only the work that genuinely depends on the missing input.

### 3.2 `conditional_input`

The dependency applies only when a defined condition is present.

Rules:

- Record the activation condition.
- Evaluate whether the condition applies to the task.
- Activate the dependency when the condition is met.
- Do not create unnecessary blocking dependencies when the condition does not apply.
- Reevaluate the condition if new information changes the task scope or risk.

### 3.3 `feedback`

The relationship represents review, findings, recommendations, or information that may cause another work item to change.

Rules:

- Feedback must identify the affected output or decision.
- Feedback must be assessed by the accountable owner.
- Required corrections must become explicit work items or tracked changes.
- Feedback alone does not automatically block unrelated execution.
- If feedback identifies a safety, security, correctness, or required acceptance issue, apply the relevant blocking or escalation rules.

Feedback relationships do not automatically create formal handoffs.

## 4. Execution dependency model

### 4.1 Work item

A work item is a bounded unit of work with:

- A clear outcome.
- An accountable owner or assigned responsible role.
- Defined scope.
- Expected outputs.
- Relevant acceptance conditions.
- Identified dependencies, if any.
- A current workflow status.

Work items may be smaller than artifact packages. Multiple work items may contribute to one package while the package retains one accountable owner.

### 4.2 Dependency direction

Represent an execution dependency from prerequisite to dependent work.

For example:

`Work A → Work B`

means Work B requires an output, decision, or condition from Work A.

The arrow must not be interpreted as ownership transfer.

### 4.3 Dependency graph

The execution plan forms a directed graph:

- Nodes represent work items.
- Edges represent execution prerequisites.
- A node may have multiple prerequisites.
- A prerequisite may support multiple dependent items.
- Independent nodes may execute in parallel.
- The execution dependency graph must be acyclic.

A cycle in the execution dependency graph indicates that at least one dependency has been incorrectly defined or that the work needs to be decomposed into smaller units.

### 4.4 Dependency graph versus collaboration graph

The collaboration graph represents communication, consultation, review, and feedback between roles.

It may contain cycles.

The execution dependency graph represents prerequisite ordering. It must not contain cycles.

Do not remove legitimate collaboration relationships merely to make the execution graph acyclic. Instead, distinguish feedback from prerequisite dependencies and refine the work breakdown when necessary.

## 5. Dependency identification procedure

During workflow planning:

### Step 1 — Break work into bounded items

Decompose the task into work items that can be assigned, tracked, reviewed, and accepted.

Avoid creating excessively small tasks that add coordination overhead without providing meaningful independence.

### Step 2 — Identify expected outputs

For each work item, record the outputs or decisions another item may need.

Use concrete outputs such as:

- Approved requirements.
- Architecture decisions.
- API or event contracts.
- Database schema or migration definitions.
- Implementation changes.
- Integration mappings.
- Test evidence.
- Security findings.
- Release instructions.

### Step 3 — Identify consumers

Determine which other work items actually require each output.

Use the producer-consumer matrix as a guide, then confirm the dependency against the task's real scope.

Do not assume every candidate relationship applies to every project.

### Step 4 — Classify the relationship

Classify the relationship as:

- `required_input`
- `conditional_input`
- `feedback`

Record the specific prerequisite or activation condition.

### Step 5 — Determine dependency readiness

Assess whether the prerequisite is:

- Not started.
- In progress.
- Available but provisional.
- Submitted for acceptance.
- Accepted.
- Rejected or requiring correction.
- Blocked.
- Not applicable.

These are dependency-readiness descriptions. They do not replace the canonical workflow status vocabulary.

### Step 6 — Check for cycles

Review the execution dependency graph.

If a cycle exists:

1. Identify the work items involved.
2. Determine whether a feedback relationship was incorrectly represented as a prerequisite.
3. Determine whether a work item needs to be decomposed.
4. Identify the smallest independently deliverable output that can break the cycle.
5. Update the dependency plan.
6. Escalate unresolved cross-domain conflicts through established governance.

Do not silently delete a legitimate dependency merely to remove a cycle.

### Step 7 — Determine execution order

Group work into execution waves based on satisfied prerequisites.

Items in the same wave may proceed in parallel only when their work does not create conflicting changes or violate another constraint.

## 6. Rules for parallel execution

### 6.1 Conditions for parallel work

Work items may execute in parallel when:

- Their required prerequisites are available.
- Neither item requires the other's unfinished output.
- Their scopes and ownership boundaries are clear.
- They do not create conflicting modifications to shared resources.
- Shared interfaces and assumptions are sufficiently stable.
- Required security, privacy, safety, and data-integrity constraints can be preserved.
- Integration can be performed and verified afterward.

### 6.2 Examples of valid parallel work

Examples include:

- UX exploration and architecture investigation after the product outcome is sufficiently understood.
- Frontend scaffolding and backend implementation after their shared interface requirements are stable enough.
- Independent implementation tasks in separate modules with established boundaries.
- Documentation preparation using verified existing technical information while implementation proceeds.
- Independent test planning and implementation work when acceptance criteria are sufficiently clear.

These are examples, not mandatory execution sequences. Actual dependencies must be evaluated for each task.

### 6.3 Conditions that prevent parallel execution

Do not proceed in parallel when:

- One work item requires an unresolved decision from another.
- Two work items modify the same resource in incompatible ways.
- A consumer is relying on an unstable or unapproved contract without an agreed provisional basis.
- A required security or safety decision is unresolved.
- A database migration and dependent implementation cannot be coordinated safely.
- Parallel changes would invalidate each other's assumptions or evidence.

### 6.4 Shared-resource coordination

When multiple work items must modify a shared resource:

1. Identify the shared resource.
2. Identify its accountable owner.
3. Define the permitted change boundaries.
4. Agree on sequencing or coordination.
5. Identify integration and conflict-resolution responsibilities.
6. Record any temporary assumptions.
7. Verify the combined result.

Do not create multiple accountable owners for the same artifact package to make parallel work easier.

### 6.5 Parallelism is not a completion shortcut

Parallel work does not remove the need for integration, review, verification, or acceptance.

All required outputs must be reconciled before dependent progression gates can pass.

## 7. Provisional and partial upstream outputs

### 7.1 When provisional consumption is allowed

A consumer may use a provisional output when:

- The producer has identified which parts are stable.
- The incomplete or uncertain parts are explicitly documented.
- The consumer can isolate work that does not depend on unresolved details.
- The accountable owners agree that the provisional use is appropriate.
- No required approval, safety, security, privacy, or integrity constraint is bypassed.

### 7.2 Restrictions

Provisional consumption must not:

- Be represented as formal acceptance.
- Change the producer's ownership or accountability.
- Override a required handoff acceptance check.
- Establish an unapproved external contract.
- Hide unresolved assumptions.
- Be used to bypass a required progression gate.

### 7.3 Reconciliation

When the final upstream output becomes available:

1. Compare it with the provisional version.
2. Identify changed assumptions or interfaces.
3. Assess downstream impact.
4. Update affected work items.
5. Repeat necessary integration and verification.
6. Record unresolved discrepancies.

If the final output invalidates dependent work, replan that work instead of treating the provisional result as authoritative.

## 8. Dependency blocking rules

A work item is blocked when it cannot safely or correctly proceed because a required prerequisite, decision, approval, or condition is unresolved.

When blocking work:

- Identify the blocked work item.
- Identify the missing prerequisite or unresolved condition.
- Identify the producing owner or responsible authority.
- Explain the impact.
- Record the next action.
- Identify unaffected work that may continue.

A blocked item must use the workflow status `blocked`.

### 8.1 Blocking scope

A blocked work item does not automatically block:

- Independent work items.
- Unrelated artifact packages.
- Investigation that does not depend on the missing output.
- Documentation of already verified information.
- Other safe work that does not rely on the unresolved condition.

### 8.2 Blocking a progression gate

A required dependency may prevent a workflow stage or gate from passing even when other work is complete.

Do not mark a gate as passed merely because most of its work items are finished.

### 8.3 Blocker resolution

After the prerequisite is resolved:

1. Confirm that the required output or decision is available.
2. Confirm its acceptance or applicable readiness.
3. Reassess dependent work for stale assumptions.
4. Restore the blocked work item to the appropriate working status.
5. Resume execution.
6. Revalidate affected outputs.

A dependency becoming available does not automatically mean the dependent work is complete or verified.

## 9. Integration and reconciliation

Parallel work must converge through controlled integration.

Before integration is considered ready:

- Required upstream outputs are available.
- Relevant contracts and interfaces are compatible.
- Conflicting changes are resolved.
- Provisional assumptions are reconciled.
- Required handoffs have been accepted where applicable.
- Integration defects are recorded and assigned.
- Relevant tests or checks are identified.

Integration may reveal new dependencies or require rework.

When that happens, update the execution plan and preserve the accountable ownership of affected packages.

## 10. Rework and feedback

When feedback or verification identifies a required change:

1. Identify the affected artifact or work item.
2. Assign the correction to the accountable owner or appropriate responsible role.
3. Identify downstream consumers that may be affected.
4. Determine whether existing outputs or acceptance decisions remain valid.
5. Update dependencies when necessary.
6. Repeat relevant integration and verification.

Do not automatically restart all work when only a bounded portion is affected.

Rework should be limited to the affected scope unless evidence demonstrates broader impact.

## 11. Dependency changes and replanning

Replan when:

- Scope changes.
- A prerequisite is added, removed, or invalidated.
- A dependency becomes conditional or no longer applies.
- A new risk or specialist responsibility is identified.
- A provisional output changes materially.
- A work item is split or merged.
- A blocker changes the execution sequence.
- Integration reveals incompatible assumptions.

Replanning must identify:

- Affected work items.
- Changed dependency relationships.
- Accountable owners.
- Impact on parallel work.
- Updated execution order.
- New or changed acceptance conditions.
- Risks and unresolved decisions.

The Delivery Lead coordinates cross-role replanning when needed. Specialist owners retain authority over their respective domains.

## 12. Dependency planning record

For tasks with meaningful cross-role dependencies, record the following in the task plan or change record:

| Field | Description |
|---|---|
| `dependency_id` | Unique identifier within the task or project record, if tracking requires one. |
| `prerequisite_work_item` | Work item that provides the prerequisite. |
| `dependent_work_item` | Work item that consumes or relies on it. |
| `relationship_type` | `required_input`, `conditional_input`, or `feedback`. |
| `condition` | Activation condition for a conditional relationship, when applicable. |
| `required_output` | Specific output, decision, or condition needed. |
| `readiness` | Current dependency-readiness description. |
| `blocking` | Whether the dependency currently prevents the dependent work or gate from proceeding. |
| `owner` | Accountable owner of the prerequisite output, when applicable. |
| `notes` | Assumptions, limitations, or reconciliation requirements. |

This is a planning aid, not a separate canonical execution-record schema.

When a project or change execution uses canonical dependency records,
the `dependency_id` must follow the identifier and execution-scoping
rules in `docs/team/dependency-execution-records.md`.

Planning notes must reference the canonical dependency identifier
when one exists. They must not create competing dependency identities
or independently redefine dependency status.

Dependency readiness descriptions are planning information and must
not replace the canonical dependency status recorded in `dependencies.yml`.

Do not add dependency records to `ownership.yml` solely to track task execution.

## 13. Relationship to other governance documents

Use this document together with:

- `docs/team/ownership.yml` — accountable artifact package owners.
- `docs/team/responsibility-boundaries.md` — role authority and boundaries.
- `docs/team/producer-consumer-matrix.md` — candidate producer-consumer relationships.
- `docs/team/handoff-contract-schema.md` — formal handoff contracts.
- `docs/team/handoff-acceptance-rules.md` — acceptance and rejection decisions.
- `docs/team/handoff-escalation-rules.md` — escalation and conflict resolution.
- `docs/team/role-activation-rules.md` — task-specific role activation.
- `docs/team/workflow-lifecycle.md` — workflow stages and progression gates.
- `docs/team/blockers-replanning-and-state-transitions.md` — blocker management, replanning, and work-item state transitions.

## 14. Governing rule

Execute work in dependency order. Parallelize only when prerequisites, boundaries, and safety conditions permit it.

Keep the execution dependency graph acyclic, preserve legitimate collaboration and feedback relationships, block only dependent work, and reconcile all provisional outputs before required integration and verification gates.

Artifact ownership remains unchanged throughout execution.
