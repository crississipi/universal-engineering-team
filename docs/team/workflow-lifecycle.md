
# Engineering Workflow Lifecycle

## Purpose

This document defines the standard lifecycle for engineering work
performed by the Universal Engineering Team.

It establishes:

- The stages through which work progresses.
- Entry and exit conditions for each stage.
- Rules for progressing, pausing, and revisiting work.
- The relationship between workflow stages, overall workflow status, and individual work-item states.
- Minimum evidence required for responsible workflow progression.
- Rules for adapting the workflow to different task sizes and risks.

This document governs workflow progression. It does not replace:

- `docs/team/ownership.yml`
- `docs/team/artifact-catalog.md`
- `docs/team/responsibility-boundaries.md`
- `docs/team/producer-consumer-matrix.md`
- `docs/team/handoff-contract-schema.md`
- `docs/team/handoff-acceptance-rules.md`
- `docs/team/handoff-escalation-rules.md`

## 1. Governing Principles

1. Every work item must have a defined objective and accountable task owner.
2. Work must progress through appropriate stages based on its scope,
   complexity, dependencies, and risk.
3. Not every task requires every specialist role or workflow stage.
4. Independent work may proceed in parallel when dependencies permit.
5. Required dependencies must be satisfied before dependent work proceeds.
6. Artifact ownership remains governed by `ownership.yml`.
7. Workflow coordination does not transfer artifact ownership.
8. Formal handoffs must follow approved handoff contracts when applicable.
9. Decisions and verification claims must have supporting evidence.
10. Security, safety, privacy, data integrity, and production stability
    concerns must not be bypassed for schedule convenience.
11. A task must not advance through a required gate based on assumptions.
12. Workflow stages describe the type of work being performed; overall workflow status describes the project or change condition; work-item states describe individual execution conditions.

## 2. Workflow Overview

The standard engineering lifecycle consists of nine stages:

1. Intake
2. Qualification
3. Solution Framing
4. Planning
5. Execution
6. Integration and Review
7. Verification
8. Release Readiness and Release
9. Closure

The lifecycle is adaptable.

A small, isolated task may require only a subset of these stages.
A complex or high-risk initiative may require more detailed activities
within individual stages.

Skipping a stage must not mean skipping a required decision,
dependency, verification, or approval.

## 3. Workflow Stages

### Stage 1 — Intake

**Purpose:** Capture a new request, issue, change, or engineering initiative.

Typical activities:

- Record the request or issue.
- Identify the requesting source.
- Capture the desired outcome.
- Record known constraints and context.
- Identify urgency and potential impact.
- Reference available supporting materials.

Minimum expected information:

- Work item identifier.
- Request description.
- Desired outcome.
- Request source or origin.
- Known constraints, if available.

**Exit condition:**

The request is recorded and ready for qualification.

Incomplete requests may remain in intake while clarification is obtained.

No implementation commitment is implied by intake.

### Stage 2 — Qualification

**Purpose:** Determine whether the request is sufficiently understood
to proceed and identify its initial delivery boundaries.

Typical activities:

- Clarify the problem and intended outcome.
- Identify affected users, systems, or components.
- Determine whether requirements or acceptance criteria need definition.
- Identify obvious dependencies and constraints.
- Identify potential security, privacy, quality, accessibility,
  performance, and operational concerns.
- Determine whether the request should proceed, be deferred, or be cancelled.

**Exit condition:**

The work has a sufficiently clear objective and an initial understanding
of its scope, constraints, and expected outcome.

A request that cannot be sufficiently clarified remains pending
or is deferred with a recorded reason.

### Stage 3 — Solution Framing

**Purpose:** Establish an appropriate technical and functional approach
before committing to implementation.

Typical activities:

- Assess affected system boundaries.
- Identify technical alternatives where necessary.
- Review relevant existing architecture and contracts.
- Identify specialist constraints.
- Identify significant trade-offs.
- Record architecture decisions when required.
- Determine whether additional investigation or a technical experiment
  is necessary.

Solution framing is particularly important for:

- Cross-system changes.
- New integrations.
- Significant data-model changes.
- New infrastructure or deployment patterns.
- Security-sensitive changes.
- Changes affecting multiple artifact packages.

A small, isolated change may use an existing approved approach without
requiring a separate architecture activity.

**Exit condition:**

An implementation approach exists at the level of detail required
by the task's complexity and risk.

Unresolved architectural decisions that block implementation must
be recorded and escalated appropriately.

### Stage 4 — Planning

**Purpose:** Convert the approved scope and solution approach into
an executable work plan.

Typical activities:

- Break down work into manageable tasks.
- Identify task owners.
- Identify affected artifact packages.
- Identify required and conditional dependencies.
- Identify applicable formal handoffs.
- Determine which tasks may run in parallel.
- Establish acceptance and verification expectations.
- Identify documentation requirements.
- Identify relevant risks and release implications.

The work plan must distinguish:

- Required inputs.
- Conditional inputs.
- Feedback relationships.
- Independent work.
- Work that cannot safely proceed until a dependency is satisfied.

**Exit condition:**

The work is sufficiently decomposed, ownership is clear, and required
dependencies and verification expectations are understood.

The Delivery Lead coordinates the plan without taking over specialist
implementation or decision authority.

### Stage 5 — Execution

**Purpose:** Perform the approved implementation and engineering work.

Typical activities:

- Implement assigned changes.
- Produce or update owned artifacts.
- Follow approved technical contracts and decisions.
- Maintain relevant tests.
- Document material implementation decisions.
- Report progress, blockers, and changed assumptions.
- Coordinate with dependent roles when necessary.

Independent tasks may execute in parallel.

A task must not proceed through an unsatisfied required dependency
when doing so would create incompatible, unsafe, or invalid work.

**Exit condition:**

Assigned implementation work is ready for integration and review,
or an explicit blocker or scope change has been recorded.

Implementation completion alone does not establish verification.

### Stage 6 — Integration and Review

**Purpose:** Confirm that individual outputs work together and remain
consistent with approved requirements and contracts.

Typical activities:

- Integrate relevant implementation outputs.
- Review affected interfaces and schemas.
- Check cross-package compatibility.
- Resolve integration defects.
- Review implementation against approved decisions.
- Confirm required handoff outputs and context.
- Record review findings and required corrections.

Formal handoff acceptance must follow the applicable contract
and acceptance rules.

**Exit condition:**

The relevant outputs are integrated sufficiently to proceed
to verification.

Unresolved integration defects or required handoff failures must
remain open or blocked.

### Stage 7 — Verification

**Purpose:** Establish whether the delivered change satisfies
its applicable acceptance, quality, and risk requirements.

Typical activities:

- Execute the planned tests.
- Evaluate acceptance criteria.
- Review regression results.
- Perform relevant security assessments.
- Perform relevant performance assessments.
- Perform relevant accessibility assessments.
- Review operational requirements.
- Record defects, limitations, and evidence.
- Retest corrected issues.

Specialist verification is activated according to the actual
scope and risk of the change.

Passing one verification activity does not imply that unrelated
verification requirements have passed.

**Exit condition:**

Applicable acceptance criteria and required verification gates
have been satisfied, with supporting evidence.

Unresolved required findings prevent verification completion unless
an explicitly authorized decision permits a documented exception.

### Stage 8 — Release Readiness and Release

**Purpose:** Determine whether verified work is ready for release
and coordinate its controlled delivery.

Typical activities:

- Review the change inventory.
- Confirm required verification evidence.
- Review security and operational concerns.
- Confirm deployment requirements.
- Review monitoring and rollback readiness.
- Confirm required approvals and risk decisions.
- Coordinate release sequencing.
- Execute the authorized release.
- Perform relevant post-release verification.

Release activities apply only when the work requires deployment,
publication, distribution, or another controlled delivery event.

A verified change does not automatically become authorized for release.

**Exit condition:**

When release is required, the authorized release process has been
completed and its outcome recorded.

When release is not applicable, the work may proceed directly
to closure after verification.

### Stage 9 — Closure

**Purpose:** Establish a reliable record of the completed, deferred,
or cancelled work.

Typical activities:

- Confirm the final work item status.
- Confirm affected artifact updates.
- Confirm required handoffs are resolved.
- Record verification evidence and decisions.
- Record unresolved limitations or accepted risks.
- Confirm relevant documentation updates.
- Record outstanding follow-up work.
- Produce a concise delivery summary.

**Exit condition:**

The work item has a recorded final disposition and its required
delivery evidence is available.

A task must not be represented as successfully completed when
required work remains unresolved.

## 4. Workflow Stage Adaptation

The lifecycle is a standard reference, not a mandatory waterfall.

Adaptation must consider:

- Scope and complexity.
- Number of affected artifact packages.
- Cross-system dependencies.
- Security and operational exposure.
- Data integrity implications.
- User impact.
- Verification requirements.
- Release requirements.

Examples:

| Work type | Typical workflow |
|---|---|
| Small isolated bug fix | Intake, Qualification, Planning, Execution, Verification, Closure |
| Frontend feature | Intake, Qualification, Solution Framing, Planning, Execution, Review, Verification, Release if required, Closure |
| New API integration | Full lifecycle with contract, integration, security, and operational considerations |
| Database migration | Full lifecycle with data integrity, migration safety, backup, and recovery considerations |
| Infrastructure change | Qualification, Solution Framing, Planning, Execution, Operational Verification, Release if required, Closure |
| Cross-system initiative | Full lifecycle with explicit architecture decisions and dependency coordination |

These are illustrative paths, not automatic role assignments.

Required verification and approval gates must remain satisfied
even when a stage is combined with another stage.

## 5. Workflow Stages and Overall Workflow Status

Workflow stages and overall workflow status are separate concepts.

A stage describes the type of work currently being performed in the
project or change lifecycle.

Overall workflow status describes the current execution or delivery
condition of the project or change as a whole.

Individual work-item states are a separate, more detailed execution
model. They are defined in:

`docs/team/blockers-replanning-and-state-transitions.md`

The canonical overall workflow status vocabulary is:

- `proposed`
- `planned`
- `in_progress`
- `blocked`
- `in_review`
- `verified`
- `released`
- `deferred`
- `cancelled`

### Overall workflow status meanings

| Status | Meaning |
|---|---|
| `proposed` | Request recorded but not yet approved for execution |
| `planned` | Scope, ownership, and execution approach sufficiently defined |
| `in_progress` | The overall project or change is actively being executed |
| `blocked` | Overall workflow progression cannot safely or correctly continue |
| `in_review` | Overall outputs are undergoing integration, review, or verification |
| `verified` | Applicable overall acceptance and verification requirements passed |
| `released` | Required release or delivery event completed |
| `deferred` | Overall work intentionally postponed with a recorded reason |
| `cancelled` | Overall work discontinued with a recorded reason |

### Overall workflow status transition rules

1. `proposed` may transition to `planned`, `deferred`, or `cancelled`.
2. `planned` may transition to `in_progress`, `blocked`, `deferred`,
   or `cancelled`.
3. `in_progress` may transition to `in_review`, `blocked`, `deferred`,
   or `cancelled`.
4. `blocked` returns to the appropriate previous overall workflow
   status after its blocking condition is resolved.
5. `in_review` may transition to `verified`, `blocked`, `in_progress`,
   `deferred`, or `cancelled`.
6. `verified` may transition to `released` when a release is required.
7. `verified` may proceed to closure when release is not applicable.
8. `released` represents completed release activity, not merely
   a release intention.
9. `deferred` work may be reconsidered through an explicit planning
   decision.
10. `cancelled` work must not silently return to active execution.
    Reauthorization must be recorded.

A workflow returning from `blocked` must resume at the appropriate
overall workflow status. Resolving a blocker does not automatically
mean the workflow is verified.

If a verified or released change requires additional work, record
the follow-up or explicitly reopen the workflow with its reason
and traceability.

### Terminal disposition

The normal successful overall workflow path ends in:

- `verified` when no release is required.
- `released` when a release is required.

`deferred` and `cancelled` represent non-successful or postponed
dispositions and must retain their reasons.

The overall workflow does not require a separate `completed` status.
Individual work items may use `completed` under the separate
work-item state model.

## 6. Workflow Gates

The following gates protect workflow progression.

| Gate | Required condition |
|---|---|
| Qualification gate | Objective and initial scope sufficiently understood |
| Solution gate | Required technical decisions resolved or explicitly recorded |
| Planning gate | Task ownership and required dependencies identified |
| Integration gate | Relevant outputs are compatible and integrated |
| Verification gate | Applicable acceptance and verification requirements satisfied |
| Release gate | Required approvals, readiness, and risk decisions recorded |
| Closure gate | Final disposition, evidence, and follow-up actions recorded |

Not every task needs a separate review meeting or approval ceremony
for every gate.

The evidence and decision must nevertheless exist when the gate applies.

A gate must not be bypassed because a milestone or deadline is approaching.

## 7. Dependency and Rework Behavior

Dependencies are governed by the producer-consumer matrix
and approved handoff contracts.

Apply the following rules:

1. Required inputs block dependent work when unavailable.
2. Conditional inputs become blocking only when their activation
   condition applies.
3. Feedback relationships may trigger corrections or reassessment.
4. Independent work may continue when it does not depend on the
   unresolved item.
5. Partial upstream outputs may be used only when their limitations
   are understood and the consumer can safely proceed.
6. Changes to approved requirements or contracts must be recorded.
7. Rework must identify the affected output and required verification.
8. A rejected or incomplete handoff must follow the established
   acceptance and resubmission rules.

The existence of a relationship in the producer-consumer matrix
does not automatically mean that a formal handoff is active.

## 8. Blocked Work

Individual work-item blocker classification, severity, records,
ownership, resolution, and state transitions are governed by:

`docs/team/blockers-replanning-and-state-transitions.md`

An individual work item must be marked `blocked` when it cannot
safely or correctly proceed because of an unresolved condition.

An overall workflow must only be marked `blocked` when the blocking
condition prevents overall workflow progression or a required
workflow gate from being satisfied.

A blocked work item does not automatically make the entire project
or change blocked. Independent work may continue when its
prerequisites, boundaries, and safety conditions permit it.

Overall workflow blocker handling must preserve the following:

- The affected work and dependencies are identified.
- The blocking condition and delivery impact are recorded.
- The accountable owners remain identifiable.
- Appropriate specialist or stakeholder authority is engaged.
- The workflow resumes only when its applicable conditions are met.

A blocker being resolved does not automatically mean that an
individual work item is ready, completed, or verified.

A blocked overall workflow must not be marked verified or released
merely because it has stopped progressing.

Detailed blocker and escalation procedures are documented in:

- `docs/team/blockers-replanning-and-state-transitions.md`
- `docs/team/handoff-escalation-rules.md`

## 9. Workflow Coordination

The Delivery Lead coordinates the overall workflow by:

- Maintaining delivery visibility.
- Coordinating work breakdown and task ownership.
- Tracking dependencies and blockers.
- Coordinating role activation according to the approved activation rules.
- Communicating schedule and delivery impacts.
- Coordinating escalations.
- Tracking unresolved actions.
- Confirming that closure records are complete.

The Delivery Lead does not:

- Replace artifact owners.
- Make specialist implementation decisions.
- Approve security findings on behalf of risk owners.
- Override QA verification decisions.
- Override accessibility or performance findings.
- Authorize changes outside delegated authority.
- Treat coordination status as proof of technical completion.

Detailed coordination and execution rules are defined in:

- `docs/team/role-activation-rules.md`
- `docs/team/dependency-execution-rules.md`
- `docs/team/orchestration-responsibilities.md`
- `docs/team/blockers-replanning-and-state-transitions.md`

## 10. Relationship to Existing Governance

Workflow progression must remain consistent with the established
governance documents.

| Concern | Governing source |
|---|---|
| Canonical roles | `docs/team/expected-roles.yml` |
| Artifact ownership | `docs/team/ownership.yml` |
| Artifact definitions | `docs/team/artifact-catalog.md` |
| Responsibility boundaries | `docs/team/responsibility-boundaries.md` |
| Producer-consumer dependencies | `docs/team/producer-consumer-matrix.md` |
| Handoff contracts | `docs/team/handoff-contract-schema.md` |
| Handoff acceptance | `docs/team/handoff-acceptance-rules.md` |
| Handoff escalation | `docs/team/handoff-escalation-rules.md` |
| Workflow lifecycle | `docs/team/workflow-lifecycle.md` |
| Role activation | `docs/team/role-activation-rules.md` |
| Dependency-aware execution | `docs/team/dependency-execution-rules.md` |
| Orchestration and coordination | `docs/team/orchestration-responsibilities.md` |
| Blockers, replanning, and work-item states | `docs/team/blockers-replanning-and-state-transitions.md` |

No workflow stage creates a new artifact owner or changes an existing
role's decision authority.

## 11. Maintenance

Update this document when workflow stages, transition rules,
or progression gates change.

Before changing the lifecycle:

1. Review the impact on role responsibilities.
2. Review existing ownership and handoff rules.
3. Confirm that required verification and risk gates remain intact.
4. Review the impact on workflow orchestration.
5. Update related documentation consistently.
6. Run all applicable repository validators.

Do not introduce new mandatory workflow stages without a clear
delivery or governance justification.
