# Blockers, Replanning, and Workflow State Transitions

## 1. Purpose

This document defines the rules for identifying, recording, managing, escalating, and resolving execution blockers; determining when replanning is required; and controlling valid workflow state transitions.

It establishes a consistent execution model across the 17 engineering roles while preserving:

- Single accountable ownership of each artifact package.
- Specialist decision authority within each role's domain.
- Explicit producer-consumer dependencies.
- Controlled handoff acceptance and rejection.
- Dependency-aware parallel execution.
- Traceable decisions, changes, and verification evidence.

These rules apply to project-level workflows, change-level workflows, and individual work items.

## 2. Governing Principles

### 2.1 Ownership is retained

A blocker does not transfer ownership of the affected work item or artifact package.

The accountable owner remains responsible for:
- Understanding the impact of the blocker.
- Providing relevant context and evidence.
- Coordinating resolution within their authority.
- Updating the work item's state.
- Confirming that work can safely resume.

The Delivery Lead may coordinate cross-role resolution but does not become the owner of specialist deliverables.

### 2.2 Block only affected work

A blocker must not automatically stop the entire project or every participating role.

Only work that:
- Directly depends on the blocked item;
- Cannot safely or correctly proceed without the missing input;
- Would violate a required approval, verification, or safety gate; or
- Has been explicitly stopped by an authorized decision

must remain blocked.

Independent work may continue when its boundaries, assumptions, and interfaces are sufficiently clear.

### 2.3 No implicit approval

The following do not constitute approval or completion:

- A response deadline expiring.
- A blocker being closed without verification.
- A downstream task continuing with provisional input.
- A workflow stage advancing.
- A contributor reporting that their work is finished.
- A Delivery Lead coordinating a resolution.

Required acceptance, review, security, quality, accessibility, performance, and release decisions remain subject to their respective authorities and evidence requirements.

### 2.4 Preserve traceability

Material blocker decisions and replanning decisions must be recorded with enough information to reconstruct:

- What changed or prevented progress.
- Which work items and artifact packages were affected.
- Who made or authorized the decision.
- What evidence supported the decision.
- Which dependencies or assumptions changed.
- What must happen before work can resume or close.

## 3. Workflow Stage, Overall Workflow Status, Work-Item State, and Handoff Decision

These are four separate dimensions and must be recorded independently.

### 3.1 Workflow stages

The overall workflow lifecycle uses the following nine stages,
as defined in `docs/team/workflow-lifecycle.md`:

1. Intake
2. Qualification
3. Solution Framing
4. Planning
5. Execution
6. Integration and Review
7. Verification
8. Release Readiness and Release, when applicable
9. Closure

A workflow stage describes the overall type of work being performed.
It does not describe the current execution state of every individual
task.

### 3.2 Overall workflow status

The overall project or change has a separate workflow status.

Its canonical vocabulary, meanings, transition rules, and terminal
dispositions are defined in:

`docs/team/workflow-lifecycle.md`

This document does not redefine that vocabulary.

Overall workflow status must not be confused with the state of an
individual work item. For example, one task may be `blocked` while
the overall workflow remains `in_progress` because independent work
can continue.

### 3.3 Work-item states

Individual tasks and other explicitly tracked units of work use
the following canonical states:

### 3.4 Handoff decisions

Handoff decisions continue to use the separate vocabulary defined in `docs/team/handoff-acceptance-rules.md`:

- `accepted`
- `partially_accepted`
- `rejected`
- `blocked`

Acceptance-check results remain:

- `passed`
- `failed`
- `not_applicable`
- `not_verified`

A handoff decision must not be substituted for a work-item state.

For example:
- A work item may be `in_review` while its submitted handoff is awaiting a decision.
- A handoff may be `blocked` while the receiving work item is also `blocked`.
- A handoff may be `partially_accepted` while the producer addresses the remaining outputs.
- A handoff may be `rejected` while the producer's work item moves to `changes_requested`.

The relationship between the two states must be explicitly recorded when both are tracked.

The `completed` work-item state does not replace the overall
workflow status `verified` or `released`.

A completed work item means that its own defined completion criteria
have been satisfied. Overall verification and release remain subject
to the lifecycle gates and applicable specialist approvals.

## 4. Blocker Management

### 4.1 What qualifies as a blocker

A blocker exists when a specific condition prevents work from proceeding safely, correctly, or in accordance with an established requirement.

Examples include:

- Missing required upstream artifact or contract.
- Unresolved technical decision that materially affects implementation.
- Missing access, environment, infrastructure, or external service dependency.
- Failed required acceptance or verification check.
- Unresolved security, privacy, safety, or data-integrity concern.
- Conflicting requirements or incompatible interface assumptions.
- Missing stakeholder decision or authorization.
- An unavailable external provider or dependency that prevents required work.

A question, inconvenience, preference disagreement, or ordinary task dependency is not automatically a blocker. Its actual effect on execution must be assessed.

### 4.2 Blocker classification

Use the following classifications to describe the primary nature of a blocker:

| Classification | Description |
|---|---|
| `dependency` | A required upstream task, artifact, or input is unavailable. |
| `technical` | A technical decision, defect, or incompatibility prevents progress. |
| `access_environment` | Required credentials, permissions, infrastructure, or environment are unavailable. |
| `external` | A third-party provider, stakeholder, or external system prevents progress. |
| `requirements` | Requirements, scope, or acceptance criteria are incomplete or conflicting. |
| `verification` | Required review, test, or verification evidence is missing or unsuccessful. |
| `security_safety` | A security, privacy, safety, or integrity concern requires action or authorization. |
| `resource` | A necessary resource or authorized participant is unavailable. |

Classification describes the nature of the blocker. It does not assign authority or determine priority by itself.

### 4.3 Blocker severity

Use the following severity levels:

| Severity | Meaning | Expected handling |
|---|---|---|
| `critical` | Immediate risk to security, privacy, safety, data integrity, or production stability; or a condition requiring an immediate stop. | Stop affected work and escalate immediately to the appropriate authority. |
| `high` | A required dependency or decision prevents a significant workflow milestone or multiple dependent work items. | Prompt owner-led resolution and Delivery Lead coordination when cross-role impact exists. |
| `medium` | A defined work item cannot proceed, but independent work and the broader workflow can continue. | Resolve through normal owner-led coordination and agreed response windows. |
| `low` | A limited impediment with a known workaround or negligible immediate schedule impact. | Track and resolve without unnecessarily stopping unrelated work. |

Severity must be based on actual impact and risk, not job title, perceived urgency, or the number of participants involved.

A security or safety concern must not be downgraded solely to preserve a delivery date.

### 4.4 Blocker record

Every material blocker must have a traceable record.

A blocker record should contain:

| Field | Requirement |
|---|---|
| `id` | Unique blocker identifier. |
| `title` | Short, descriptive blocker title. |
| `description` | Concrete explanation of the blocking condition. |
| `classification` | One of the classifications in Section 4.2. |
| `severity` | `critical`, `high`, `medium`, or `low`. |
| `reported_by` | Role or person reporting the blocker. |
| `accountable_owner` | Owner of the affected work item. |
| `affected_work_items` | Identifiers of directly affected tasks. |
| `affected_artifacts` | Relevant artifact package IDs, when applicable. |
| `dependencies` | Relevant prerequisite, handoff, or external dependency references. |
| `evidence` | Logs, failed checks, decisions, missing inputs, or other supporting references. |
| `impact` | Effect on scope, correctness, safety, dependencies, or delivery. |
| `resolution_owner` | Person or role coordinating the resolution, if different from the accountable owner. |
| `next_action` | Concrete next step needed to resolve or reassess the blocker. |
| `status` | Current blocker status. |
| `created_at` | Creation timestamp. |
| `updated_at` | Most recent update timestamp. |
| `resolution_evidence` | Evidence supporting closure, when resolved. |

The blocker record must not contain secrets, access tokens, passwords, or other sensitive credentials. Use approved secure references where access is required.

### 4.5 Blocker statuses

The canonical blocker status vocabulary is defined in
`docs/team/blocker-records.md` and implemented by
`schemas/executions/blockers.schema.json`. The complete vocabulary is:

- `open`
- `in_progress`
- `blocked`
- `escalated`
- `deferred`
- `resolved`
- `closed`
- `cancelled`

These are blocker-record statuses only. They must not be substituted for
work-item states, workflow statuses, dependency statuses, or handoff
decisions.

`escalated` records referral to the appropriate authority; it does not mean
the blocker is resolved or that affected work may resume.
`deferred` requires an authorized decision and does not imply resolution.
`resolved` records that the impediment has been addressed with resolution
information. `closed` is permitted only after verification and reassessment
of affected work. `cancelled` is terminal and must retain its rationale.

The permitted transitions and status-specific record requirements are
defined in `docs/team/blocker-records.md`.

### 4.6 Blocker ownership

The accountable owner of the affected work item remains responsible for tracking the blocker.

The person or role responsible for implementing the resolution may differ.

Examples:

- A Backend Developer may own a blocked backend work item while the Database Manager resolves a schema dependency.
- A Frontend Developer may own a blocked frontend work item while the UX/UI Designer clarifies an interaction requirement.
- An Integration Engineer may own a blocked integration task while an external provider or API owner supplies missing information.
- A Release Manager may coordinate a release blocker while the specialist owner provides the required verification evidence.

The Delivery Lead coordinates blockers that affect multiple roles, dependencies, milestones, or delivery commitments.

### 4.7 Blocker resolution

A blocker may be resolved through:

- Supplying the missing required input.
- Completing or revising an upstream dependency.
- Making and recording an authorized decision.
- Correcting the underlying defect or incompatibility.
- Providing required access or environment readiness.
- Completing a required verification or approval.
- Formally changing scope through an authorized replanning decision.
- Cancelling affected work through an authorized scope decision.

Resolution must be supported by evidence or a traceable decision reference.

After resolution:
1. The blocker owner records the resolution evidence.
2. The affected work-item owner reassesses the work item.
3. Relevant dependent work items are reassessed.
4. Work resumes only when the required prerequisites and safety conditions are satisfied.
5. The blocker is closed after the affected work has been appropriately reassessed.

Resolving one blocker does not automatically resolve other blockers or make every dependent task ready.

## 5. Replanning Rules

### 5.1 Purpose of replanning

Replanning is a controlled adjustment to an existing execution plan when new information, decisions, dependencies, or constraints materially affect the approved approach.

Replanning must preserve traceability to the previous plan and must not silently change approved requirements, artifact ownership, or specialist decisions.

### 5.2 Replanning triggers

Replanning is required when one or more of the following materially changes:

- Product scope, priority, or acceptance criteria.
- Architecture or a significant technical decision.
- Artifact ownership or responsibility boundaries.
- Required inputs or producer-consumer dependencies.
- Work-item prerequisites or execution order.
- Role activation or required specialist participation.
- External service, provider, or environment availability.
- Delivery milestones or agreed commitments.
- Verification, security, privacy, accessibility, or performance requirements.
- Release strategy, deployment conditions, or rollback approach.
- A blocker invalidates an existing plan or makes its assumptions unsafe.

Minor task adjustments that do not affect approved scope, dependencies, ownership, acceptance criteria, or material delivery commitments may be handled by the accountable work-item owner and recorded in the task.

### 5.3 Replanning assessment

Before changing a plan, the accountable owner and relevant coordinators must assess:

1. What changed and why?
2. Which requirements, decisions, assumptions, or constraints are affected?
3. Which work items and artifact packages are directly affected?
4. Which dependencies must be added, removed, reordered, or revalidated?
5. Which roles must be activated, consulted, or informed?
6. Can unaffected work continue independently?
7. Does the change require specialist review or stakeholder authorization?
8. What happens to existing outputs, evidence, and in-progress work?
9. What new risks or blockers are introduced?
10. What must be communicated to downstream consumers?

The assessment must be proportionate to the impact of the change.

### 5.4 Replanning authority

Authority depends on the type of decision:

| Decision area | Accountable authority |
|---|---|
| Product scope, priorities, and acceptance criteria | Product Analyst within delegated authority; otherwise the authorized stakeholder. |
| Cross-system architecture and technical trade-offs | Solution Architect. |
| API and event contract changes | API Manager within API governance responsibilities. |
| Database schema, integrity, and migration decisions | Database Manager within database responsibilities. |
| Specialist implementation approach | Accountable specialist artifact owner within their domain. |
| Quality strategy and verification evidence | QA Manager within quality responsibilities. |
| Security findings and security verification | Penetration Tester within security assessment responsibilities; risk acceptance remains with an authorized risk owner. |
| Infrastructure and operational readiness | DevOps/SRE within operations responsibilities. |
| Performance budgets and performance evidence | Performance Engineer within performance responsibilities. |
| Accessibility requirements and verification | Accessibility Specialist within accessibility responsibilities. |
| Release planning and release coordination | Release Manager within release responsibilities. |
| Cross-role coordination and delivery plan tracking | Delivery Lead. |

The Delivery Lead coordinates replanning and maintains the execution overview but cannot independently approve specialist decisions, change product acceptance criteria, accept security risk, or waive required verification gates.

When a change affects multiple authority domains, all relevant domain owners must participate. Cross-system technical conflicts follow the established escalation rules.

### 5.5 Replanning record

A material replanning decision must record:

- Decision or change identifier.
- Reason for replanning.
- Reference to the previous plan or affected work items.
- Description of the proposed change.
- Affected requirements and artifact packages.
- Dependency and role-activation impact.
- Scope, risk, and delivery impact.
- Relevant specialist assessments.
- Decision authority and approval references.
- Revised work sequence and next actions.
- Communication requirements.
- Date and current status.

A decision that changes an approved requirement, interface, architecture, or acceptance condition must be reflected in its authoritative source document or record.

A replanning record does not replace the authoritative requirement, contract, ADR, artifact, or approval record.

### 5.6 Preserving previous work

Replanning must not silently discard completed or in-progress work.

Affected work must be classified as one of the following:

- `retain`: still valid under the revised plan.
- `revise`: remains useful but requires modification.
- `revalidate`: may remain valid, but evidence or compatibility must be checked.
- `supersede`: replaced by a new approved output or decision.
- `cancel`: no longer required under the authorized revised scope.

The accountable owner determines the technical disposition within their domain. Relevant consumers must be informed when previously supplied outputs change or become invalid.

### 5.7 Replanning and dependency integrity

After replanning:

- Required prerequisites must be explicit.
- Conditional dependencies must retain their activation conditions.
- Feedback relationships must remain distinguishable from execution prerequisites.
- The execution dependency graph must remain acyclic.
- New parallel work must satisfy the dependency and safety conditions in `docs/team/dependency-execution-rules.md`.
- Existing handoff contracts must not be silently rewritten during an active execution.
- Contract changes must follow the established contract versioning and approval process.
- Affected consumers must be notified when an input changes, is superseded, or becomes invalid.

A change to one dependency must not automatically invalidate unrelated work.

## 6. Replanning and Blocker Coordination

### 6.1 Coordination levels

Use the existing orchestration model:

1. **Work-item level:** Accountable owner handles local blockers and adjustments.
2. **Specialist-domain level:** Relevant specialist owner coordinates domain-specific resolution.
3. **Cross-role level:** Delivery Lead coordinates dependencies, impact assessment, and replanning.
4. **Authorized stakeholder level:** External scope, business, or risk decisions are referred to the appropriate authorized authority.

Coordination must occur at the lowest level that can safely and effectively resolve the issue.

### 6.2 Escalation

Escalation follows `docs/team/handoff-escalation-rules.md`.

- Producer and consumer attempt direct resolution where appropriate.
- Specialist-domain conflicts go to the accountable domain owner.
- Cross-system technical conflicts go to the Solution Architect.
- Product or business decisions outside delegated authority go to the authorized stakeholder.
- Risk acceptance goes to the authorized risk owner.
- The Delivery Lead coordinates cross-role escalation and records delivery impact.

Critical security, privacy, safety, data-integrity, and production-stability concerns require immediate escalation.

Normal response windows are agreed per task or project. Expiration of a response window does not constitute acceptance or approval.

## 7. Work-Item State Transitions

### 7.1 Allowed transitions

The following transitions are permitted:

| Current state | Next state | Conditions |
|---|---|---|
| `not_started` | `ready` | Required prerequisites and activation conditions are sufficiently satisfied. |
| `not_started` | `cancelled` | Work is formally removed through an authorized scope decision. |
| `ready` | `in_progress` | Accountable owner or assigned contributor begins execution. |
| `ready` | `blocked` | A newly identified condition prevents safe or correct execution. |
| `ready` | `cancelled` | Work is formally discontinued through an authorized decision. |
| `in_progress` | `blocked` | A required condition prevents further safe or correct progress. |
| `in_progress` | `in_review` | Defined outputs are submitted with required context and evidence for review. |
| `in_progress` | `completed` | Work has no separate required review gate and all completion criteria are satisfied. |
| `in_progress` | `cancelled` | Work is formally discontinued through an authorized decision. |
| `blocked` | `ready` | Blocking conditions are resolved or an authorized revised plan makes execution possible. |
| `blocked` | `cancelled` | Work is formally discontinued through an authorized decision. |
| `in_review` | `completed` | Required review and acceptance conditions are satisfied. |
| `in_review` | `changes_requested` | Review identifies changes required before completion. |
| `in_review` | `blocked` | Review cannot proceed because required input, access, decision, or evidence is unavailable. |
| `changes_requested` | `ready` | Required corrections are understood and prerequisites for further work are satisfied. |
| `changes_requested` | `blocked` | A separate blocking condition prevents correction. |
| `changes_requested` | `cancelled` | Work is formally discontinued through an authorized decision. |

Any transition not listed above is prohibited unless this governance document is formally revised and approved.

### 7.2 State transition requirements

Every material state transition must record:

- Work-item identifier.
- Previous state.
- New state.
- Transition timestamp.
- Person or role making the update.
- Reason for the transition.
- Relevant blocker, dependency, decision, or evidence reference.
- Next action or responsible owner, when applicable.

State changes must reflect actual execution conditions. They must not be used to make a dashboard, milestone, or delivery report appear more favorable.

### 7.3 Entering `blocked`

Before or when moving a work item to `blocked`:

1. Describe the specific blocking condition.
2. Identify the directly affected work item and dependencies.
3. Create or reference a blocker record.
4. Identify the accountable owner and resolution owner.
5. Assess which dependent tasks are also affected.
6. Identify independent work that can continue.
7. Escalate based on severity and authority.

A blocked work item must not remain in `in_progress` merely because someone is still discussing its blocker.

### 7.4 Leaving `blocked`

A work item may leave `blocked` only when:

- The blocking condition is resolved or an authorized plan change removes the dependency.
- Supporting evidence or a decision reference is recorded.
- Required prerequisites are available.
- Applicable safety and approval constraints are satisfied.
- The accountable owner confirms that work may resume.

The normal transition is:

`blocked` → `ready` → `in_progress`

A direct transition from `blocked` to `completed` is not allowed. The work must be reassessed and any remaining work or verification performed.

### 7.5 Entering `in_review`

A work item may enter `in_review` only when:

- The defined reviewable output exists.
- Required context and references are supplied.
- Applicable acceptance checks are identified.
- Known limitations and unresolved issues are disclosed.
- The receiving reviewer or accountable consumer is identified when required.

Submission for review does not imply acceptance.

### 7.6 Entering `completed`

A work item may enter `completed` only when:

- Its defined completion criteria are satisfied.
- Required outputs are available.
- Required acceptance or verification activities are complete.
- Relevant evidence and references are recorded.
- Outstanding blockers that prevent completion are resolved.
- Required downstream coordination or notification is performed.

When a separate formal handoff is required, its acceptance decision must follow the handoff acceptance rules. Work-item completion must not be used to bypass that decision.

### 7.7 Cancellation

Cancellation requires an authorized scope or planning decision.

A cancelled item must retain:

- Cancellation reason.
- Decision authority.
- Affected requirements and dependencies.
- Disposition of existing outputs.
- Downstream consumer notifications.
- Any residual risk or follow-up work.

Cancellation is not a substitute for marking difficult, delayed, or blocked work as complete.

## 8. Overall Workflow Progression and Gates

### 8.1 Stage progression

The overall workflow advances according to the lifecycle defined in `docs/team/workflow-lifecycle.md`.

Stage progression is based on the applicable stage exit conditions, not on a simple count of completed work items.

For example:

- Execution may continue while independent tasks are blocked.
- Integration and review may begin for completed, sufficiently stable outputs while unrelated implementation continues.
- Verification may proceed for outputs whose required inputs are available.
- Release readiness cannot bypass required quality, security, accessibility, performance, or operational gates.
- Closure requires the applicable delivery and documentation records.

### 8.2 Stage advancement conditions

Before advancing a workflow stage, the coordinator must confirm:

1. The stage's required outputs and exit conditions are satisfied.
2. Required work-item states are accurate.
3. Critical and high-severity blockers have been assessed and appropriately handled.
4. Dependencies for the next stage are explicit.
5. Required role activation and specialist participation are satisfied.
6. Required approvals and evidence are available.
7. Remaining work, risks, and accepted limitations are documented.
8. The next stage can proceed without violating an established constraint.

A stage may remain open while permitted parallel work continues. Advancing a stage does not automatically mark all work items in the previous stage as completed.

### 8.3 Release and closure gates

Release readiness and release must follow the release governance and required specialist evidence.

Closure must not occur solely because implementation has stopped.

Before closure, the Delivery Lead coordinates confirmation that:

- Required deliverables and their ownership records are accounted for.
- Required handoffs have reached the appropriate decisions.
- Required verification evidence is recorded.
- Remaining blockers and unresolved issues have an explicit disposition.
- Relevant documentation and knowledge records are updated.
- Release and operational records are available when applicable.
- Final delivery status and follow-up actions are communicated.

The Delivery Lead coordinates closure but does not independently approve specialist evidence or accept risk.

## 9. Parallel Work During Blockers and Replanning

Parallel work may continue when:

- It does not require the unavailable prerequisite.
- Its scope and interfaces are sufficiently defined.
- Its assumptions are documented.
- It does not create an unsafe or incompatible implementation.
- Any provisional inputs are explicitly identified.
- Required reconciliation can occur before the relevant acceptance or release gate.

Work must pause when continuing would:

- Violate a required dependency.
- Introduce unacceptable security, privacy, safety, or data-integrity risk.
- Depend on an unresolved decision that materially changes correctness.
- Make an irreversible change without required authorization.
- Bypass a required review, verification, or approval gate.

Provisional work must be identified as provisional and must be reconciled against the authoritative output before dependent completion or release.

Parallel execution is not permission to ignore unresolved blockers.

## 10. Communication and Reporting

### 10.1 Required notifications

Relevant affected parties must be informed when:

- A blocker affects their work or dependency.
- A blocker is escalated or its severity changes.
- A plan or prerequisite changes.
- A previously supplied artifact is revised, superseded, or invalidated.
- Work resumes after a blocker is resolved.
- A work item is cancelled.
- A workflow stage advances or a required gate is not satisfied.

Notifications should be proportional to impact. Avoid notifying every role about unrelated local blockers.

### 10.2 Status reporting

A workflow status report should distinguish:

- Current workflow stage.
- Work-item state counts or significant item states.
- Open blockers by severity.
- Escalated blockers and required decisions.
- Replanning decisions and their impact.
- Completed and pending acceptance or verification gates.
- Work continuing in parallel.
- Next actions, owners, and relevant dependencies.

A status report must not imply that blocked, unverified, or unaccepted work is complete.

## 11. Exceptions and Governance

### 11.1 Small or isolated tasks

A small task may use a lightweight blocker or replanning record when the impact is limited and easily understood.

However, security, privacy, safety, data-integrity, approval, and formal handoff requirements cannot be waived merely because a task is small.

### 11.2 Urgent work

Urgent work may use an abbreviated coordination process when necessary to address an immediate issue.

The process must still preserve:
- Appropriate decision authority.
- Required safety constraints.
- A traceable decision.
- Relevant evidence.
- Follow-up documentation.

Urgency does not authorize unauthorized risk acceptance or bypass mandatory safeguards.

### 11.3 Changes to this governance

Changes to canonical states, transition rules, blocker classifications, or decision authority must be reviewed as governance changes.

Existing records must remain interpretable. Historical states and decisions must not be silently rewritten to match a newer vocabulary.

## 12. Relationship to Other Governance Documents

This document must be read together with:

- `docs/team/workflow-lifecycle.md` — overall workflow lifecycle and stages.
- `docs/team/role-activation-rules.md` — required, conditional, optional, and inactive role participation.
- `docs/team/dependency-execution-rules.md` — dependency-aware execution and parallel work.
- `docs/team/orchestration-responsibilities.md` — coordination responsibilities and orchestration levels.
- `docs/team/responsibility-boundaries.md` — role accountability and decision authority.
- `docs/team/producer-consumer-matrix.md` — producer-consumer relationships.
- `docs/team/handoff-contract-schema.md` — formal handoff contract structure.
- `docs/team/handoff-acceptance-rules.md` — handoff acceptance, rejection, and resubmission.
- `docs/team/handoff-escalation-rules.md` — escalation and conflict resolution.
- `docs/team/ownership.yml` — canonical artifact package ownership and handoff declarations.

If a conflict is identified, do not silently override the existing governance. Record the conflict and resolve it through the appropriate authority before changing the governing rule.

## 13. Governing Principle

Blockers must be visible, bounded, owned, and resolved through evidence or authorized decisions.

Replanning must be deliberate, traceable, and proportionate to impact.

Workflow states must reflect actual execution conditions.

The Delivery Lead coordinates the overall flow, accountable owners retain their work, and specialist authorities retain their domain decisions.

No workflow transition, blocker closure, or delivery milestone can substitute for required acceptance, verification, or risk authorization.