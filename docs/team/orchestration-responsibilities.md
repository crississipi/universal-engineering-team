# Orchestration and Coordination Responsibilities

## 1. Purpose

This document defines how work is orchestrated across the 17-role engineering team.

It establishes:

- Who coordinates work at task, package, and cross-role levels.
- How execution responsibilities are distributed.
- How dependencies, parallel work, and handoffs are coordinated.
- How coordination decisions are recorded.
- How blockers and conflicts are escalated.
- The boundaries between orchestration, artifact ownership, and specialist authority.

Orchestration organizes execution. It does not replace the authority or accountability established by the team's ownership and responsibility governance.

## 2. Governing principles

### 2.1 Coordination is not ownership

A person or role coordinating work does not automatically own the artifacts produced by participating roles.

Artifact ownership remains defined in `docs/team/ownership.yml`.

### 2.2 One accountable owner per artifact package

Each artifact package retains one accountable owner.

Contributors may perform work under the applicable package owner's coordination, but do not become co-owners.

### 2.3 Coordination follows task complexity

A small isolated task may be coordinated directly by its accountable owner.

Cross-role work may require Delivery Lead coordination.

Do not activate a dedicated coordination role when coordination overhead would exceed its value.

### 2.4 Specialist authority is preserved

Each specialist retains decision authority within the boundaries defined in `docs/team/responsibility-boundaries.md`.

The coordinator may request clarification, identify conflicts, and arrange escalation, but cannot independently override specialist decisions.

### 2.5 Orchestration must be transparent

Important coordination decisions must be visible to affected owners and participants.

Record changes to scope, dependencies, ownership assignments, blockers, and progression decisions in the task or project record.

### 2.6 Coordination does not imply automatic approval

Scheduling a review, requesting acceptance, or recording a completed activity does not mean that an artifact, handoff, verification result, or release has been approved.

Use the applicable acceptance and authorization rules.

## 3. Orchestration model

The team uses three coordination levels.

### 3.1 Task-level coordination

Task-level coordination is appropriate for a bounded task handled by one accountable owner or a small group with no significant cross-role dependency.

The accountable owner coordinates:

- Task scope and expected outputs.
- Work sequencing within the package.
- Contributor assignments when needed.
- Relevant dependencies.
- Progress and blockers.
- Package-level review and completion.

The Delivery Lead does not need to be activated solely because a task has multiple small implementation steps.

### 3.2 Cross-role coordination

Cross-role coordination is appropriate when work spans multiple artifact packages, accountable owners, or significant execution dependencies.

The Delivery Lead coordinates:

- Work breakdown across affected packages.
- Role activation and participation.
- Dependency identification and sequencing.
- Parallel execution opportunities.
- Cross-role communication.
- Blocker tracking and escalation.
- Integration coordination.
- Delivery status and closure readiness.

Each artifact owner remains accountable for their own package.

### 3.3 Specialist-domain coordination

A specialist owner coordinates work within their domain when a task requires multiple contributions or decisions within that specialist area.

Examples include:

- Solution Architect coordinating architectural analysis.
- API Manager coordinating API contract decisions.
- Database Manager coordinating database design and migration decisions.
- QA Manager coordinating verification strategy and evidence.
- DevOps/SRE coordinating infrastructure and operational readiness.

Specialist-domain coordination does not grant authority over unrelated domains or other artifact package owners.

## 4. Coordination responsibilities by role

### 4.1 Delivery Lead

The Delivery Lead is the primary cross-role coordination role when activated.

Responsibilities:

- Coordinate task breakdown and execution planning.
- Identify affected artifact packages and accountable owners.
- Coordinate role activation and participation.
- Track required and conditional dependencies.
- Identify opportunities for safe parallel execution.
- Maintain cross-role task visibility.
- Track blockers, unresolved decisions, and delivery risks.
- Coordinate escalation through the established governance.
- Organize integration and closure activities.
- Maintain an accurate delivery record.

Boundaries:

- Does not become the owner of specialist artifact packages.
- Does not independently determine specialist technical correctness.
- Does not override domain-owner decisions.
- Does not approve QA, security, accessibility, or performance evidence on behalf of specialists.
- Does not accept security or operational risk without delegated authority.
- Does not treat schedule pressure as a reason to bypass required gates.

### 4.2 Accountable artifact owner

The accountable owner coordinates work within the assigned package.

Responsibilities:

- Define package-level work and expected outputs.
- Identify required contributors.
- Coordinate work within package boundaries.
- Confirm dependencies affecting package outputs.
- Maintain package quality and completeness.
- Communicate changes or blockers to affected consumers.
- Submit outputs for applicable review or acceptance.

Boundaries:

- Cannot change another package's ownership.
- Cannot approve their own output where independent acceptance is required.
- Cannot override another specialist's authority.
- Must communicate changes that affect dependent packages.

### 4.3 Specialist coordinator

A specialist coordinator organizes work within an assigned domain.

Responsibilities:

- Clarify specialist requirements and constraints.
- Coordinate domain-specific contributions.
- Resolve issues within their authority.
- Identify cross-domain impacts.
- Provide technical or assessment outputs to affected owners.
- Escalate conflicts outside their authority.

Boundaries:

- Cannot take ownership of another package through coordination.
- Cannot unilaterally decide matters belonging to another specialist domain.
- Must preserve required cross-domain reviews and acceptance conditions.

### 4.4 Contributors

Contributors perform assigned work within the agreed scope.

Responsibilities:

- Produce assigned outputs.
- Follow relevant contracts, requirements, and technical constraints.
- Communicate progress, assumptions, and blockers.
- Raise concerns when work crosses an ownership or specialist boundary.
- Provide evidence needed for review.

Boundaries:

- Do not independently change package ownership.
- Do not approve outputs on behalf of the accountable owner.
- Do not silently alter agreed interfaces or acceptance conditions.

### 4.5 Consulted specialists

Consulted specialists provide targeted advice or assessments.

Responsibilities:

- Explain relevant domain constraints.
- Identify material risks or conflicts.
- Provide recommendations or required specialist decisions.
- Identify when formal specialist participation is necessary.

Consultation does not automatically create implementation responsibility or artifact ownership.

## 5. Orchestration lifecycle

### Step 1 — Establish the coordination model

Determine whether the task is:

- Owner-coordinated.
- Specialist-domain coordinated.
- Delivery Lead coordinated.

Base the decision on scope, affected packages, dependencies, risk, and coordination needs.

### Step 2 — Identify participants and owners

Consult:

- `docs/team/ownership.yml`
- `docs/team/role-activation-rules.md`
- `docs/team/responsibility-boundaries.md`

Identify accountable owners, required participants, conditional specialists, and contributors.

### Step 3 — Establish the execution plan

Use the workflow lifecycle and dependency rules to establish:

- Work items.
- Expected outputs.
- Accountable owners.
- Dependencies.
- Parallel work opportunities.
- Required handoffs.
- Verification requirements.
- Relevant progression gates.

### Step 4 — Coordinate execution

During execution:

- Track work item status.
- Monitor prerequisite readiness.
- Coordinate cross-role communication.
- Identify conflicting assumptions.
- Keep parallel work within agreed boundaries.
- Escalate blockers and material risks.
- Replan when scope or dependencies change.

### Step 5 — Coordinate integration and review

Ensure that affected owners participate in integration and review.

Confirm:

- Required outputs are available.
- Interfaces and assumptions are compatible.
- Formal handoffs have applicable acceptance decisions.
- Conflicts and defects are assigned.
- Required corrections are tracked.

The coordinator does not substitute their judgment for the required consumer or specialist acceptance decision.

### Step 6 — Coordinate verification and release readiness

Identify the verification and release activities applicable to the task.

Coordinate the required specialists, evidence, decisions, and outstanding risks.

The coordinator must not mark specialist verification as passed without the required evidence or authorized decision.

### Step 7 — Coordinate closure

Confirm:

- Work item statuses are accurate.
- Artifact owners have accounted for required outputs.
- Required handoffs have been resolved.
- Verification evidence is recorded.
- Risks and exceptions are documented.
- Documentation obligations are addressed.
- Outstanding actions have accountable owners.
- Delivery status is accurately recorded.

Closure coordination does not mean unresolved risks or required work can be silently treated as complete.

## 6. Coordination decisions and records

Coordination decisions should be recorded in the task or project record when they materially affect execution.

Examples:

- Coordination model selected.
- Delivery Lead activation or deactivation.
- Accountable owners and contributors.
- Role activation decisions.
- Work breakdown and sequencing.
- Dependency changes.
- Parallel execution boundaries.
- Blocker ownership and next actions.
- Escalation decisions.
- Integration readiness.
- Closure readiness.

Do not introduce a separate permanent governance manifest solely for routine task coordination.

Use the existing task or project record unless a later governance phase explicitly defines a dedicated execution-record schema.

## 7. Communication rules

### 7.1 Communicate with accountable owners

Coordination requests that affect a package must reach its accountable owner.

Contributors may be contacted directly for assigned work, but ownership accountability remains explicit.

### 7.2 Communicate dependency changes

When a prerequisite changes, notify affected dependent owners.

Identify:

- The changed output or condition.
- The affected work items.
- The impact on current assumptions.
- Required corrections or replanning.

### 7.3 Communicate material risks promptly

Security, safety, privacy, data-integrity, and production-stability concerns must be escalated promptly.

Do not delay urgent escalation for routine coordination meetings or status updates.

### 7.4 Keep decisions traceable

Important decisions should include:

- The decision or issue.
- The responsible authority.
- The affected scope.
- The rationale or evidence.
- The resulting action.
- Any unresolved conditions.

Avoid treating informal agreement as a substitute for required documented approval.

## 8. Coordination and decision authority

Use the following decision boundaries:

| Decision | Responsible authority |
|---|---|
| Package-level execution planning | Accountable package owner |
| Cross-role work coordination | Delivery Lead, when activated |
| Specialist-domain technical decisions | Accountable specialist |
| Cross-system architectural conflict | Solution Architect |
| Product scope and priority decisions | Product Analyst within delegated authority; authorized stakeholder when required |
| Handoff acceptance | Consumer owner |
| Quality verification and QA evidence | QA Manager within the defined responsibility |
| Security assessment findings | Penetration Tester within the defined responsibility |
| Accessibility assessment findings | Accessibility Specialist within the defined responsibility |
| Performance assessment findings | Performance Engineer within the defined responsibility |
| Infrastructure and operational decisions | DevOps/SRE within the defined responsibility |
| Release coordination | Release Manager |
| External risk acceptance or authorization | Appropriate authorized stakeholder or risk owner |

This table clarifies coordination boundaries. It does not expand the authority already defined in the responsibility-boundaries and escalation documents.

## 9. Orchestration exceptions

### 9.1 Small isolated tasks

The accountable owner may coordinate a task without activating the Delivery Lead when:

- Scope is bounded.
- Ownership is clear.
- No material cross-role dependency exists.
- Required verification is proportionate and identified.
- No unresolved specialist or risk decision requires coordination.

### 9.2 Expanding tasks

If an isolated task expands across packages or specialist boundaries:

1. Reassess affected packages.
2. Identify additional accountable owners.
3. Reevaluate role activation.
4. Reassess dependencies and parallel work.
5. Activate Delivery Lead coordination when justified.
6. Update the execution record.

### 9.3 Urgent work

Urgent work may use an adapted coordination sequence when necessary to address an immediate incident or risk.

However, urgency does not authorize bypassing required safety, security, privacy, data-integrity, or risk-acceptance controls.

Record deferred activities and complete required follow-up verification and documentation.

## 10. Relationship to other governance documents

Use this document together with:

- `docs/team/ownership.yml` — artifact ownership and eligible contributors.
- `docs/team/responsibility-boundaries.md` — role authority and boundaries.
- `docs/team/role-activation-rules.md` — role activation and participation.
- `docs/team/producer-consumer-matrix.md` — producer-consumer relationships.
- `docs/team/handoff-contract-schema.md` — formal handoff contracts.
- `docs/team/handoff-acceptance-rules.md` — acceptance and rejection decisions.
- `docs/team/handoff-escalation-rules.md` — escalation and conflict resolution.
- `docs/team/workflow-lifecycle.md` — workflow stages and progression gates.
- `docs/team/dependency-execution-rules.md` — dependency-aware execution and parallel work.
- `docs/team/blockers-replanning-and-state-transitions.md` — blocker management, replanning, and workflow state transitions.

## 11. Governing rule

Coordinate work at the lowest level that can manage it effectively.

The accountable owner remains responsible for their artifact package. The Delivery Lead coordinates cross-role execution when needed. Specialists retain their domain authority.

Orchestration must improve execution visibility and coordination without creating duplicate ownership, unauthorized approval, or bypassed governance.
