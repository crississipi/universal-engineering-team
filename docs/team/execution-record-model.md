# Execution Record Architecture and Canonical Record Model

## 1. Purpose

This document defines the architecture and canonical record types used to document actual engineering work performed by the Universal Engineering Team.

It establishes:

- The structure of an engineering execution record.
- The canonical record categories and their responsibilities.
- Relationships between execution records.
- Record organization and storage conventions.
- Traceability requirements across project execution.
- Governance principles for maintaining reliable execution history.

This document defines the record architecture. It does not yet define the complete field-level schemas, validation rules, or automated execution-tracking mechanisms.

## 2. Governing Principles

All execution records must preserve the following principles.

### 2.1 Execution records represent actual work

Execution records document real project or change activity.

They must not contain fabricated:
- Role activations.
- Work-item completion claims.
- Handoff submissions or acceptance decisions.
- Technical or product decisions.
- Verification results.
- Evidence references.
- Blocker resolutions.
- Release outcomes.

Illustrative examples and templates must be explicitly identified as such.

### 2.2 Existing governance remains authoritative

Execution records must reference existing governance definitions rather than duplicate or replace them.

The following remain authoritative:

| Governance area | Source |
|---|---|
| Canonical engineering roles | `docs/team/expected-roles.yml` |
| Artifact ownership | `docs/team/ownership.yml` |
| Responsibility boundaries | `docs/team/responsibility-boundaries.md` |
| Producer-consumer relationships | `docs/team/producer-consumer-matrix.md` |
| Workflow stages and overall workflow statuses | `docs/team/workflow-lifecycle.md` |
| Role activation rules | `docs/team/role-activation-rules.md` |
| Dependency and parallel execution rules | `docs/team/dependency-execution-rules.md` |
| Handoff contract definitions | `docs/team/handoff-contract-schema.md` |
| Handoff acceptance rules | `docs/team/handoff-acceptance-rules.md` |
| Handoff escalation rules | `docs/team/handoff-escalation-rules.md` |
| Blockers and work-item state transitions | `docs/team/blockers-replanning-and-state-transitions.md` |

Execution records capture how these rules were applied to a specific project or change.

### 2.3 Ownership remains unchanged

Execution records must preserve the established single accountable owner for each artifact package.

Recording participation does not:
- Transfer artifact ownership.
- Create a second accountable owner.
- Override specialist decision authority.
- Convert a contributor into an artifact owner.

### 2.4 Record relationships must be explicit

Records must reference related records using stable identifiers.

Relationships must not depend solely on:
- File names.
- Directory names.
- Role names.
- Record ordering.
- Informal descriptions.

### 2.5 Record history must be traceable

Material changes to execution records must remain traceable.

At minimum, changes affecting ownership, state, decisions, dependencies, handoff outcomes, verification, blockers, or final disposition must have an identifiable reason and supporting reference where applicable.

The detailed history and revision mechanism will be defined in a later subphase.

### 2.6 No unnecessary event-sourcing architecture

The execution-record system will use current record values together with an auditable history of material changes.

It will not introduce a separate event-processing platform or require every minor editing action to become an individual event record.

## 3. Execution Record Architecture

An execution represents one identifiable coordinated attempt to perform work for a specific change within a project.

It acts as the root record for all related execution information.

Every record belonging to an execution must be traceable to its execution identifier.

### 3.1 Root execution record

The root execution record establishes:

- Execution identity.
- Project or change description.
- Intended outcome.
- Scope and relevant boundaries.
- Current overall workflow stage and status.
- Primary coordination information.
- References to related execution records.
- Final disposition when the execution is closed.

The root record does not replace the individual work-item, role activation, dependency, handoff, decision, evidence, blocker, or closure records.

### 3.2 Supporting record categories

The canonical execution architecture contains nine record categories:

1. Execution.
2. Work item.
3. Role activation.
4. Dependency.
5. Handoff execution.
6. Decision.
7. Evidence.
8. Blocker and replan.
9. Closure.

Each category has a distinct responsibility and must not duplicate the authoritative purpose of another category.

### 3.3 Project, Change, and Execution Identity

Every execution must identify its parent project and change using stable
identifiers.

The canonical identity hierarchy, identifier formats, generation rules, external references, and traceability requirements are defined in:

`docs/team/execution-identity-and-traceability.md`

Every `execution.yml` record must contain:

- `project_id`
- `change_id`
- `execution_id`

The execution directory name must match `execution_id`.

A project may contain multiple changes, and a change may have multiple
execution instances. Each execution instance has its own directory and
must retain its relationship to the correct project and change.

Child records inherit project and change context from their execution.
They must reference their execution explicitly and must not introduce
conflicting identity relationships.

Exact YAML schemas and automated identity validation are deferred to
Phase 1.4.7.

### 3.4 Role Activation and Work-Item Records

Each execution maintains two distinct record collections:

- `role-activations.yml` records the roles considered and activated for the execution.
- `work-items.yml` records the specific units of work performed during the execution.

Role activation records reference the parent execution and canonical role. They preserve the activation classifications defined in `role-activation-rules.md`.

Work-item records reference the parent execution, assigned role, and applicable work-item state. Their state vocabulary and transitions remain governed by `blockers-replanning-and-state-transitions.md`.

A work item must reference an activated role within the same execution. Assignment does not transfer artifact package ownership.

The canonical record requirements, relationships, and field definitions are documented in:

`docs/team/role-activation-and-work-item-records.md`

Exact schemas and automated validation are deferred to Phase 1.4.7.

## 4. Canonical Record Types

### 4.1 Execution Record

**File:** `execution.yml`

**Purpose:** Establish the identity and overall context of one engineering execution.

It represents the root of the execution record structure.

Its responsibilities include:

- Identifying the parent project, change, and execution.
- Describing the intended outcome.
- Establishing scope and boundaries.
- Identifying the relevant overall workflow stage and status.
- Referencing associated execution records.
- Identifying the responsible coordination authority.
- Recording the final disposition when applicable.

The execution record must distinguish overall workflow status from individual work-item states and formal handoff decisions.

### 4.2 Work-Item Records

**File:** `work-items.yml`

**Purpose:** Record individual units of engineering work.

Each work item represents a defined task or activity that contributes to the execution outcome.

Its responsibilities include:

- Identifying the work item.
- Defining its objective and expected outputs.
- Identifying its accountable task owner.
- Referencing the applicable artifact package when relevant.
- Recording acceptance criteria.
- Recording its current work-item state.
- Identifying dependencies and related records.
- Referencing supporting evidence.
- Recording its final disposition.

Work-item ownership must remain consistent with established artifact ownership and responsibility boundaries.

The work-item state vocabulary must follow:

`docs/team/blockers-replanning-and-state-transitions.md`

A completed work item does not automatically mean the overall execution is verified or released.

### 4.3 Role Activation Records

**File:** `role-activations.yml`

**Purpose:** Record which engineering roles participate in a particular execution and why they are involved.

Its responsibilities include:

- Identifying the activated role.
- Recording its activation classification.
- Recording the reason or applicable activation trigger.
- Identifying its participation scope.
- Referencing relevant work items or artifact packages.
- Recording participation changes when necessary.

Role activation must follow:

`docs/team/role-activation-rules.md`

The record must distinguish:

- Required participation.
- Conditional participation.
- Optional participation.
- Roles that were not activated.

Activation does not automatically create a formal handoff or transfer ownership.


### 4.4 Dependency Records

**File:** `dependencies.yml`

**Purpose:** Record explicit execution dependencies between work items.

Its responsibilities include:

- Identifying the predecessor and successor work items.
- Recording the dependency relationship type.
- Explaining the purpose and condition of the dependency.
- Recording activation conditions when applicable.
- Maintaining the current dependency execution status.
- Recording satisfaction evidence and related decision references.
- Recording related blocker and formal handoff execution references.
- Preserving material changes and status transitions in history.

Dependency records must follow:

`docs/team/dependency-execution-records.md`

Reusable dependency governance rules remain defined in:

`docs/team/dependency-execution-rules.md`

The execution dependency graph must remain acyclic.

Feedback and collaboration relationships may be cyclic when permitted by the governing rules.

A dependency record must not automatically block unrelated work.

Controlled provisional work may proceed only under the conditions defined in the dependency execution rules.

### 4.5 Handoff Execution Records

**File:** `handoff-executions.yml`

**Purpose:** Record actual producer-to-consumer submissions and their outcomes.

These records represent individual handoff executions, not reusable handoff contracts.

Their responsibilities include:

- Identifying the producer and consumer roles.
- Referencing the producer and consumer artifact packages.
- Referencing the applicable handoff contract ID and version.
- Identifying the submitted outputs.
- Referencing required context and supporting evidence.
- Recording acceptance-check results.
- Recording the consumer's overall decision.
- Tracking corrections and resubmissions.
- Recording resolution and escalation references.

Formal handoff executions must follow:

- `docs/team/handoff-contract-schema.md`
- `docs/team/handoff-acceptance-rules.md`
- `docs/team/handoff-escalation-rules.md`

A handoff execution must not modify or redefine its referenced contract.

A submission does not constitute acceptance.

The canonical handoff execution record structure, submission
history, lifecycle transitions, decision references, and validation
requirements are defined in:

`docs/team/handoff-execution-records.md`

### 4.6 Decision Records

**File:** `decisions.yml`

**Purpose:** Record material decisions made during engineering execution.

Decision records may cover:

- Product scope and priorities.
- Architecture and technical direction.
- API and integration contracts.
- Database and data-model choices.
- Security and risk decisions.
- Operational and infrastructure decisions.
- Release and delivery decisions.
- Approved deviations or exceptions.

Their responsibilities include:

- Identifying the decision.
- Recording the issue or question being resolved.
- Recording the available context and alternatives when relevant.
- Identifying the decision authority.
- Recording the selected outcome and rationale.
- Identifying affected work items and artifact packages.
- Referencing supporting evidence.
- Recording superseded or revisited decisions when applicable.

A decision must not be attributed to a role that lacks the required decision authority.

A coordination record does not automatically constitute an approval or specialist decision.

The canonical decision record structure, decision lifecycle,
authority references, outcome requirements, and validation
requirements are defined in:

`docs/team/decision-records.md`

### 4.7 Evidence Records

**File:** `evidence.yml`

**Purpose:** Preserve verifiable information supporting execution claims, acceptance checks, decisions, and completion.

Evidence records are responsible for:

- Identifying the evidence item and its source.
- Recording evidence classification and provenance.
- Recording verification status and accountability.
- Linking evidence to related execution records.
- Preserving evidence history and supersession.
- Maintaining traceability to the claims supported by the evidence.

Evidence records must follow:

`docs/team/evidence-records.md`

Evidence verification does not independently authorize work completion, handoff acceptance, dependency satisfaction, release, or execution closure.

The applicable canonical record and its authorized decision-maker remain responsible for those determinations.

### 4.8 Blocker Records

**File:** `blockers.yml`

**Purpose:** Record execution impediments and preserve their resolution history.

Blocker records are responsible for:

- Identifying the impediment and its classification.
- Recording severity and lifecycle status.
- Identifying affected work items and related dependencies.
- Recording reporting and resolution responsibilities.
- Linking supporting evidence and authorized decisions.
- Preserving investigation, escalation, deferral, and resolution history.

Blocker records must follow:

`docs/team/blocker-records.md`

A blocker does not independently change work-item status, dependency status, role activation, or workflow stage.

Resolution must be evaluated independently by the responsible canonical records.`

### 4.9 Re-planning Records

**File:** `replans.yml`

**Purpose:** Preserve authorized changes to an execution plan and their implementation history.

Re-planning records are responsible for:

- Identifying why re-planning is necessary.
- Recording the proposed and authorized changes.
- Identifying affected work items and related execution records.
- Linking the canonical decision authorizing the changes.
- Recording expected and actual impact.
- Tracking implementation of approved changes.
- Preserving proposal, authorization, and implementation history.

Re-planning records must follow:

`docs/team/replanning-records.md`

Re-planning records do not replace the canonical records being changed.

Approved changes must be applied to the relevant work-item, dependency, role-activation, handoff, or other applicable records.

A re-planning proposal must not be treated as authorization to implement its proposed changes.

### 4.10 Closure Record

**File:** `closure.yml`

**Purpose:** Record the final disposition of an engineering execution.

Its responsibilities include:

- Confirming the final overall workflow status.
- Recording the final execution outcome.
- Confirming applicable work-item dispositions.
- Confirming required handoff resolution.
- Referencing required verification evidence.
- Recording unresolved limitations and accepted risks.
- Recording outstanding follow-up work.
- Identifying the closure decision authority.
- Recording the closure date and relevant references.

Closure must follow the applicable workflow gates and release requirements.

A closure record must not imply successful completion when required work or verification remains unresolved.

## 5. Record Relationships

All supporting records belong to a specific execution.

The root execution identifier provides the primary traceability reference.

The following relationships are expected:

| Source record | Related record | Relationship |
|---|---|---|
| Execution | Work items | Work items belong to the execution |
| Execution | Role activations | Role participation belongs to the execution |
| Execution | Dependencies | Dependencies coordinate work items |
| Execution | Handoff executions | Handoff activity belongs to the execution |
| Execution | Decisions | Decisions are made within the execution |
| Execution | Evidence | Evidence supports execution claims |
| Execution | Blockers and replans | Execution interruptions and plan changes |
| Execution | Closure | Final execution disposition |
| Role activation | Work items | Activated roles participate in assigned work |
| Work item | Dependency | Work items may depend on other work items |
| Work item | Handoff execution | Work items may produce or consume handoff outputs |
| Work item | Evidence | Evidence supports work-item completion and verification |
| Work item | Blocker | A work item may be affected by a blocker |
| Decision | Evidence | Evidence supports or explains a decision |
| Handoff execution | Evidence | Evidence supports submission and acceptance |
| Blocker | Replan | A blocker may trigger an approved replan |
| Closure | Evidence | Evidence supports final disposition |

These relationships describe traceability requirements. They do not imply that every execution must contain every record category.

Only records relevant to the actual execution must be created.

## 6. Storage and Directory Convention

Execution records must be stored separately from reusable team governance documentation.

The canonical directory convention is:

```text
executions/
└── <execution-id>/
    ├── execution.yml
    ├── work-items.yml
    ├── role-activations.yml
    ├── dependencies.yml
    ├── handoff-executions.yml
    ├── decisions.yml
    ├── evidence.yml
    ├── blockers.yml
    ├── replans.yml
    └── closure.yml
```

### 6.1 Directory rules

1. Each independently managed execution has its own directory.
2. The directory name must use the execution's stable identifier.
3. Record files must use the canonical names defined above.
4. Empty record categories do not need fabricated entries.
5. Optional record files may be omitted until relevant records exist.
6. Existing records must not be silently overwritten when execution details change.
7. Supporting binary files and large reports may be stored externally when appropriate, provided their references remain traceable.
8. Sensitive information and secrets must not be stored in execution records.

### 6.2 Separation of governance and execution data

Reusable governance definitions belong under `docs/team/`.

Actual project execution records belong under `executions/`.

Machine-readable schemas will be maintained separately under:

`schemas/executions/`

The exact schema organization will be finalized in Phase 1.4.7.

## 7. Record Integrity and Traceability

Execution records must satisfy these general requirements:

1. Every supporting record must identify its parent execution.
2. Every referenced record must have a stable identifier.
3. Cross-record references must resolve to an existing record when the relationship is declared as established.
4. Referenced roles must use canonical role identifiers.
5. Referenced artifact packages must use canonical artifact identifiers.
6. Handoff executions must reference an existing contract when a formal contract applies.
7. Work-item state changes must follow the approved transition rules.
8. Overall workflow status changes must follow the lifecycle rules.
9. Evidence references must identify their source and verification scope where relevant.
10. Decisions must identify the authority responsible for them.
11. Material record changes must remain traceable.
12. Unresolved or unverified information must be identified honestly rather than presented as confirmed.

Detailed field-level constraints, cross-reference validation, and history requirements will be established in later subphases.

## 8. Record Applicability

Not every execution requires every record category.

Record creation must be proportional to:

- Execution scope.
- Number of participating roles.
- Number of affected artifact packages.
- Dependency complexity.
- Number of formal handoffs.
- Technical and operational risk.
- Verification and approval requirements.
- Release requirements.

Examples:

| Execution type | Expected record emphasis |
|---|---|
| Small isolated bug fix | Execution, work item, applicable evidence, closure |
| Frontend feature | Execution, work items, role activations, relevant dependencies, evidence, closure |
| New API integration | Execution, work items, role activations, dependencies, handoff executions when applicable, decisions, evidence, closure |
| Database migration | Execution, work items, decisions, evidence, blockers when applicable, closure |
| Security-sensitive change | Execution, role activations, work items, decisions, security evidence, handoffs when applicable, closure |
| Cross-system initiative | Full applicable record set with explicit dependencies, handoffs, decisions, evidence, blockers, replans, and closure |

These examples are illustrative. Actual record requirements must be determined from the execution's scope and risk.

## 9. Relationship to Future Execution Governance

This document establishes the architecture for subsequent execution-record work.

The following topics remain to be defined:

| Subphase | Responsibility |
|---|---|
| Phase 1.4.2 | Project, change, execution identity, and traceability identifiers |
| Phase 1.4.3 | Role activation and work-item record structures |
| Phase 1.4.4 | Dependency, handoff, and decision record structures |
| Phase 1.4.5 | Evidence, blocker, and re-planning record structures |
| Phase 1.4.6 | Completion, verification, and closure record structures |
| Phase 1.4.7 | Documentation, machine-readable schemas, validators, and tests |

No field-level schema or automated validator should be introduced before its governing record requirements have been defined and reviewed.

## 10. Maintenance

Changes to the canonical execution record architecture must preserve:

- Existing artifact ownership.
- Responsibility boundaries.
- Workflow stage and overall status definitions.
- Individual work-item state definitions.
- Formal handoff contract governance.
- Specialist decision authority.
- Evidence integrity.
- Historical traceability.

Any structural change must identify affected record types, relationships, references, and migration implications.

Changes must not silently invalidate existing execution records.