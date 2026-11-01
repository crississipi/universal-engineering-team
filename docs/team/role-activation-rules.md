# Role Activation and Participation Rules

## 1. Purpose

This document defines how roles from the 17-role engineering team are selected and activated for individual tasks, projects, and changes.

The purpose is to ensure that:

- The right specialists participate when their expertise is needed.
- Tasks do not activate all 17 roles by default.
- Required specialist participation is not skipped when a defined trigger applies.
- Parallel work is possible when dependencies and responsibilities permit it.
- Role activation does not transfer or duplicate artifact ownership.
- Delivery coordination remains distinct from specialist decision authority.

This document governs role activation and participation. It does not replace role definitions, responsibility boundaries, artifact ownership, producer-consumer relationships, or handoff contracts.

## 2. Governing principles

### 2.1 Activate by responsibility and trigger

Activate a role when the task intersects its defined accountability, decision authority, required input, or specialist verification responsibility.

Do not activate a role solely because its name appears in a package, dependency, or workflow diagram.

### 2.2 Do not require all roles by default

A task may be completed by one role or a small group of roles when its scope and risks permit.

The number of activated roles must be proportionate to the task's complexity, impact, dependencies, and risk.

### 2.3 Preserve one accountable owner

Role activation does not change artifact ownership.

The owner declared in `docs/team/ownership.yml` remains accountable for the corresponding artifact package. Contributors may provide work or specialist input but do not become co-owners.

### 2.4 Specialist authority remains with the specialist

An activated specialist retains the decision authority defined in `docs/team/responsibility-boundaries.md`.

The Delivery Lead coordinates participation and dependencies but cannot replace specialist judgment or approve decisions outside delegated authority.

### 2.5 Conditional participation requires a reason

When a role is activated conditionally, record the applicable trigger or reason in the task plan or change record.

Do not treat every conditional role as automatically required.

### 2.6 Activation can change during execution

New information, implementation discoveries, defects, risks, or scope changes may require additional roles to be activated.

Roles may be deactivated when their relevant work is complete, provided no unresolved responsibility, required review, dependency, or risk remains.

### 2.7 Activation is not a handoff

Activating a role does not automatically create a formal handoff.

Formal handoffs must follow the contracts and acceptance rules defined in:

- `docs/team/handoff-contract-schema.md`
- `docs/team/handoff-acceptance-rules.md`
- `docs/team/handoff-escalation-rules.md`

## 3. Activation classifications

Every role considered during task planning should receive one of the following classifications.

| Classification | Definition | Expected treatment |
|---|---|---|
| `required` | Participation is necessary for the applicable task or progression gate. | Activate and obtain the required contribution or decision before passing the relevant gate. |
| `conditional` | Participation depends on a defined trigger. | Activate when the trigger applies; otherwise leave inactive. |
| `optional` | Specialist input may improve the outcome but is not necessary. | Activate only when useful and proportionate. |
| `not_activated` | No applicable responsibility or trigger has been identified. | No participation is expected. |

A `required` classification is scoped to the task and relevant gate. It does not mean the role must participate throughout the entire lifecycle.

For a `conditional` role, the activation decision must identify the trigger or explain why the trigger does not apply.

An `optional` role must not be used to bypass a required specialist responsibility.

## 4. Participation responsibilities

Activation and participation must preserve the established ownership model.

### 4.1 Accountable owner

The accountable owner:

- Owns the artifact package assigned in `docs/team/ownership.yml`.
- Directs work within the package's defined scope.
- Ensures required outputs meet the package's acceptance expectations.
- Coordinates eligible contributors when needed.
- Retains accountability when work is delegated.

There is one accountable owner per package.

### 4.2 Contributor

A contributor:

- Provides implementation, analysis, evidence, or specialist input within the agreed scope.
- Works under the applicable package owner's coordination.
- Does not become a co-owner merely by participating.
- Does not independently change another package's ownership or acceptance requirements.

Contributor eligibility in the ownership manifest does not mean participation is mandatory.

### 4.3 Consulted specialist

A consulted specialist provides advice or a domain-specific assessment when a task intersects their expertise.

Consultation does not automatically transfer implementation responsibility or artifact ownership.

If the consultation identifies a required specialist action, the task plan must be updated accordingly.

### 4.4 Coordination

The Delivery Lead coordinates role activation when cross-role coordination is needed.

Coordination may include:

- Identifying affected roles and artifact packages.
- Confirming accountable owners.
- Recording activation reasons and dependencies.
- Organizing parallel work.
- Tracking blockers and unresolved decisions.
- Coordinating escalation and closure.

The Delivery Lead does not become the owner of specialist outputs unless explicitly assigned as the accountable owner of the relevant package.

## 5. Role activation rules

The following rules define the default activation triggers for all 17 canonical roles.

These rules must be interpreted according to the actual task scope. They are not a requirement to activate every role listed in a conditional trigger.

### 5.1 Product Analyst — `product-analyst`

**Activate as required when:**

- A new product capability or user-facing behavior needs to be defined.
- Product scope, priorities, or acceptance criteria are unclear.
- A requested change requires a product decision.
- Stakeholder expectations conflict or need clarification.

**Activate conditionally when:**

- A technical change may alter user workflows or business outcomes.
- A defect requires a decision about expected behavior.
- A proposed solution changes previously agreed acceptance criteria.

**May remain inactive when:**

- The task is a clearly scoped internal technical change with established expected behavior and no unresolved product decision.

### 5.2 Solution Architect — `solution-architect`

**Activate as required when:**

- A cross-system or material architectural decision is needed.
- Multiple implementation approaches have significant system-wide trade-offs.
- A change affects architectural boundaries or shared technical standards.
- Conflicting technical decisions require cross-system resolution.

**Activate conditionally when:**

- A localized change introduces a new dependency, technology, or architectural pattern.
- A migration or refactoring may affect multiple system components.
- A specialist identifies an architectural concern requiring resolution.

**May remain inactive when:**

- A bounded implementation follows an established architecture and introduces no material architectural decision.

### 5.3 API Manager — `api-manager`

**Activate as required when:**

- A new or changed API or event contract must be defined or governed.
- API compatibility, versioning, or contract ownership requires a decision.
- Multiple consumers or producers need a consistent interface.

**Activate conditionally when:**

- An implementation change may affect an existing API or event contract.
- An integration exposes or consumes an interface whose contract is unclear.
- A breaking-change assessment is needed.

**May remain inactive when:**

- The task does not create, modify, or materially affect an API or event contract.

### 5.4 Backend Developer — `backend-developer`

**Activate as required when:**

- Server-side application logic must be implemented or changed.
- Backend authorization, validation, domain behavior, or persistence integration is affected.
- Backend defects require implementation changes.

**Activate conditionally when:**

- A frontend or integration change requires backend support.
- A data-model or API change requires corresponding server-side adaptation.

**May remain inactive when:**

- The task is limited to design, documentation, infrastructure, or frontend behavior and requires no backend changes.

### 5.5 Frontend Developer — `frontend-developer`

**Activate as required when:**

- Client-side UI, application state, navigation, or frontend behavior must be implemented or changed.
- Frontend defects require implementation changes.

**Activate conditionally when:**

- An API or backend change affects an existing client.
- Accessibility, performance, or design findings require frontend remediation.
- A workflow change affects the user interface.

**May remain inactive when:**

- The task has no client-side implementation or behavior impact.

### 5.6 UX/UI Designer — `ux-ui-designer`

**Activate as required when:**

- A new or materially changed user flow or interaction needs design decisions.
- Visual hierarchy, interaction behavior, or usability requirements are unresolved.
- A product change requires design definition before implementation.

**Activate conditionally when:**

- Existing screens or interactions may be affected by a technical change.
- Usability findings suggest a design-level issue.
- Accessibility remediation requires a design decision.

**May remain inactive when:**

- The task is a purely technical change that does not affect user experience or interface behavior.

### 5.7 Database Manager — `database-manager`

**Activate as required when:**

- Database schemas, migrations, indexes, constraints, or data integrity rules must change.
- Data retention, backup, recovery, or database-level security requirements need a decision.
- A database migration has material operational or integrity risk.

**Activate conditionally when:**

- Application changes introduce new persistence requirements.
- Performance investigation identifies a database-level concern.
- A data pipeline or integration affects authoritative database structures.

**May remain inactive when:**

- The task does not change or materially affect database structures, integrity, or database operations.

### 5.8 Integration Engineer — `integration-engineer`

**Activate as required when:**

- A new or changed external system integration must be implemented.
- Cross-system mappings, retries, idempotency, reconciliation, or orchestration need definition.
- Integration failures require specialist investigation or remediation.

**Activate conditionally when:**

- A change affects an existing external integration.
- API or event changes may affect an integration consumer or producer.
- An operational issue involves cross-system message delivery or synchronization.

**May remain inactive when:**

- The task has no external-system integration or cross-system orchestration impact.

### 5.9 Data Engineer — `data-engineer`

**Activate as required when:**

- Data pipelines, transformations, ingestion, or data movement must be implemented or changed.
- Data lineage, replay, backfill, or pipeline quality requirements need specialist work.

**Activate conditionally when:**

- An integration changes data supplied to an existing pipeline.
- A database or application change affects downstream data processing.
- Data quality or pipeline reliability issues require investigation.

**May remain inactive when:**

- The task has no pipeline, transformation, ingestion, or data-processing impact.

### 5.10 QA Manager — `qa-manager`

**Activate as required when:**

- A change requires formal acceptance verification or regression evidence.
- Multiple components or roles must be verified against agreed acceptance criteria.
- A release or delivery gate requires QA evidence.
- A defect or change has material quality risk.

**Activate conditionally when:**

- A small isolated change has a proportionate verification approach that does not require formal QA coordination.
- A specialist assessment or production issue requires additional test coverage.

**May remain inactive when:**

- The task is a non-functional administrative activity with no meaningful product or system behavior change and no required verification gate.

Required verification must not be skipped merely because the QA Manager is not activated. Appropriate implementation-level checks or other authorized evidence may still be necessary.

### 5.11 Penetration Tester — `penetration-tester`

**Activate as required when:**

- Authorized security testing or a specialist security assessment is required.
- A material security finding requires independent assessment or retesting.
- A security-sensitive change requires specialist testing under the applicable project policy.

**Activate conditionally when:**

- Authentication, authorization, secrets, sensitive data, external exposure, or trust boundaries change.
- A new dependency or integration introduces a meaningful attack surface.
- A threat-modeling or penetration-testing trigger applies.
- A security incident or suspected vulnerability requires specialist investigation.

**May remain inactive when:**

- No applicable security trigger exists and the change does not materially affect security boundaries.

Security controls and secure implementation practices remain applicable even when the Penetration Tester is not activated. This role does not accept risk or authorize production changes.

### 5.12 DevOps/SRE — `devops-sre`

**Activate as required when:**

- Infrastructure, deployment pipelines, runtime configuration, or operational architecture must change.
- Production rollout, rollback, monitoring, or recovery procedures require specialist work.
- Operational readiness is a required release gate.

**Activate conditionally when:**

- An application change introduces new runtime, scaling, configuration, or observability requirements.
- A database migration affects deployment or recovery.
- A production issue involves availability, reliability, or infrastructure.

**May remain inactive when:**

- The task has no infrastructure, deployment, runtime, or operational impact and does not require an operational readiness decision.

### 5.13 Performance Engineer — `performance-engineer`

**Activate as required when:**

- Performance or capacity targets must be established or formally verified.
- A performance regression or capacity risk requires specialist investigation.
- A material performance-sensitive change requires profiling or benchmarking evidence.

**Activate conditionally when:**

- A change affects high-volume operations, latency-sensitive paths, resource consumption, or scalability.
- Database, frontend, backend, or infrastructure changes introduce measurable performance concerns.

**May remain inactive when:**

- No meaningful performance or capacity impact is expected and no performance gate applies.

### 5.14 Accessibility Specialist — `accessibility-specialist`

**Activate as required when:**

- An accessibility assessment or formal accessibility evidence is required.
- A new or materially changed user flow requires specialist accessibility verification under project policy.
- Accessibility findings require independent assessment or retesting.

**Activate conditionally when:**

- UI, interaction, navigation, forms, content structure, or assistive-technology behavior changes.
- A design or frontend change may affect keyboard access, semantics, contrast, or other accessibility requirements.

**May remain inactive when:**

- The task has no user-facing or accessibility impact and no accessibility assessment gate applies.

Accessibility requirements remain applicable to user-facing implementation even when the specialist is not activated.

### 5.15 Technical Writer/Knowledge Engineer — `technical-writer-knowledge-engineer`

**Activate as required when:**

- Documentation or knowledge deliverables are explicitly part of the task.
- A significant system, API, operational, or architectural change requires corresponding documentation.
- Knowledge transfer or a documented delivery record is required.

**Activate conditionally when:**

- A change affects existing technical documentation, diagrams, runbooks, or knowledge relationships.
- A new workflow, integration, or operational procedure should be documented for maintainability.

**May remain inactive when:**

- The task produces no meaningful documentation or knowledge-maintenance requirement.

Documentation obligations do not disappear merely because this role is inactive. The accountable role must still provide accurate source information and complete any required documentation.

### 5.16 Release Manager — `release-manager`

**Activate as required when:**

- A formal release or controlled deployment is planned.
- Release readiness, change inventory, rollout, rollback, or release communication requires coordination.
- A release authorization process requires this role.

**Activate conditionally when:**

- A change is published, distributed, or delivered through a controlled release process.
- Multiple components or teams must coordinate a release.
- A hotfix or urgent production change requires release coordination.

**May remain inactive when:**

- The task does not involve a release, deployment, publication, or controlled delivery event.

### 5.17 Delivery Lead — `delivery-lead`

**Activate as required when:**

- Work spans multiple roles or artifact packages and requires dependency coordination.
- A project or initiative requires work breakdown, progress tracking, or cross-role blocker resolution.
- Delivery status, risk, or closure must be coordinated across specialists.

**Activate conditionally when:**

- A task initially assigned to one role expands into cross-role work.
- A dependency, blocker, or escalation requires coordination beyond the accountable owner.

**May remain inactive when:**

- A small, isolated task can be planned, executed, verified, and closed by its accountable owner without cross-role coordination.

Delivery Lead activation does not grant authority to override specialist decisions or accept risks outside delegated authority.

## 6. Task characteristics and activation guidance

The following matrix provides a starting point for selecting roles. It is guidance, not a replacement for the role-specific triggers in Section 5.

| Task characteristic | Roles to consider |
|---|---|
| New product capability | Product Analyst, Solution Architect, UX/UI Designer, relevant implementation roles, QA Manager |
| Isolated backend defect | Backend Developer; QA Manager when verification requires coordination; other specialists only when triggered |
| Isolated frontend defect | Frontend Developer; UX/UI Designer or Accessibility Specialist when the issue concerns their domain |
| New or changed API | API Manager, relevant Backend/Frontend/Integration roles, QA Manager when contract verification is required |
| Database schema or migration | Database Manager, affected Backend/Data/Integration roles, QA Manager; DevOps/SRE when operational rollout or recovery is affected |
| External system integration | Integration Engineer, API Manager when contracts are involved, affected Backend/Data roles, QA Manager |
| Data pipeline change | Data Engineer, Database Manager when authoritative structures are affected, Integration Engineer when cross-system mappings are involved, QA Manager |
| Infrastructure or deployment change | DevOps/SRE, Solution Architect when architectural decisions are needed, Release Manager when a controlled release applies |
| Security-sensitive change | Relevant implementation owner, Penetration Tester when a security assessment or testing trigger applies, DevOps/SRE when operational security is affected |
| Performance-sensitive change | Relevant implementation owner, Performance Engineer when specialist analysis or evidence is required |
| Accessibility-sensitive UI change | Frontend Developer, UX/UI Designer as applicable, Accessibility Specialist when assessment or specialist remediation verification is required |
| Documentation-only change | Technical Writer/Knowledge Engineer; source owner consulted when technical facts need confirmation |
| Multi-role initiative | Delivery Lead, relevant accountable owners, and specialists activated by task scope and risk |
| Controlled release | Release Manager, relevant implementation owners, QA Manager when verification evidence is required, DevOps/SRE when operational release work applies |

A task characteristic does not automatically activate every role listed in its row. Apply the actual triggers and required gates.

## 7. Role activation procedure

### Step 1 — Understand the task

Identify:

- Requested outcome.
- Scope and affected system areas.
- Expected behavior or deliverables.
- Known constraints and assumptions.
- User, business, operational, and security impact.
- Whether the task is isolated or cross-role.

The Product Analyst is involved when product scope or acceptance needs clarification. The accountable owner may perform intake for a bounded technical task with established requirements.

### Step 2 — Identify affected artifact packages

Consult `docs/team/ownership.yml` and identify:

- The primary artifact package.
- Other packages whose outputs may be changed or consumed.
- Accountable owners for affected packages.
- Potential producer-consumer relationships.

Do not infer ownership from a role's participation or from free-form descriptions.

### Step 3 — Evaluate activation triggers

For each potentially relevant role:

1. Check its responsibility boundary.
2. Check the role-specific triggers in Section 5.
3. Check task characteristics and risks.
4. Determine whether participation is required, conditional, optional, or unnecessary.
5. Record the reason for required or conditional activation.

### Step 4 — Confirm ownership and participation

Identify the accountable owner for each affected artifact package.

List contributors or consulted specialists only when their participation has a defined purpose.

Do not add contributors merely to make every role appear involved.

### Step 5 — Identify dependencies and handoffs

Consult `docs/team/producer-consumer-matrix.md`.

Determine whether a relationship is:

- `required_input`
- `conditional_input`
- `feedback`

Create a formal handoff only when the work requires one under the established handoff governance.

### Step 6 — Plan participation timing

Specify when each activated role is needed.

A role may participate only during a relevant stage or gate. Continuous participation is not assumed.

### Step 7 — Reassess during execution

Reevaluate activation when:

- Scope changes.
- New dependencies are discovered.
- An implementation crosses a specialist boundary.
- A defect exposes a new risk.
- A verification result requires specialist assessment.
- A release or operational concern emerges.

Record activation changes and their reasons in the task record.

### Step 8 — Close participation

A role may be deactivated when its assigned contribution or decision is complete and no unresolved obligation remains.

Deactivation does not remove artifact ownership, accepted evidence, unresolved risks, or outstanding handoff obligations.

## 8. Participation timing across workflow stages

Role participation should align with the workflow lifecycle defined in `docs/team/workflow-lifecycle.md`.

| Workflow stage | Activation considerations |
|---|---|
| Intake | Identify the requester, accountable owner, and any role needed to clarify the outcome. |
| Qualification | Activate roles needed to clarify scope, feasibility, dependencies, and material risks. |
| Solution Framing | Activate architecture and domain specialists when technical decisions require them. |
| Planning | Confirm affected package owners, contributors, required dependencies, handoffs, and verification responsibilities. |
| Execution | Activate implementation owners and only the specialists needed for the assigned work. |
| Integration and Review | Involve affected producers, consumers, and specialists needed to resolve compatibility or handoff issues. |
| Verification | Activate QA and relevant security, performance, accessibility, data, or operational specialists according to the applicable verification requirements. |
| Release Readiness and Release | Activate Release Manager and DevOps/SRE when the release or deployment process requires them; retain specialist evidence and approvals. |
| Closure | Confirm required artifacts, accepted handoffs, evidence, documentation, risks, and delivery status. Activate coordination or documentation roles when needed. |

A role does not need to attend every stage merely because it was activated for the task.

## 9. Minimum activation record

For cross-role tasks, or whenever conditional specialist activation matters, record the activation decisions in the task plan or change record.

The record should include:

| Field | Description |
|---|---|
| `role` | Canonical role identifier. |
| `activation` | `required`, `conditional`, `optional`, or `not_activated`. |
| `reason` | Responsibility, trigger, or reason for the decision. |
| `scope` | Expected contribution or decision. |
| `workflow_stage` | Stage or gate where participation is needed, when known. |
| `accountable_package` | Relevant artifact package ID, when applicable. |
| `status` | Participation state, if tracked by the project. |

This is a planning record, not a new artifact ownership declaration or formal handoff contract.

Do not add these fields to `ownership.yml` solely to track task-specific participation.

## 10. Escalation and exceptions

If a task owner and a specialist disagree about whether a specialist trigger applies:

1. Record the disputed trigger and its potential impact.
2. Consult the specialist's responsibility boundary.
3. Resolve the matter through the established escalation and conflict-resolution rules.
4. Do not silently omit a specialist when a material risk or required gate remains unresolved.

Urgent security, safety, privacy, data-integrity, or production risks must be escalated promptly.

An exception to a required participation or verification condition must be explicitly authorized by the appropriate authority. Delivery coordination alone does not constitute authorization.

## 11. Relationship to other governance documents

This document must be used together with:

- `docs/team/expected-roles.yml` — canonical role identifiers and order.
- `docs/team/ownership.yml` — artifact package owners and eligible contributors.
- `docs/team/artifact-catalog.md` — artifact package descriptions.
- `docs/team/responsibility-boundaries.md` — role authority and boundaries.
- `docs/team/producer-consumer-matrix.md` — candidate producer-consumer relationships.
- `docs/team/handoff-contract-schema.md` — formal handoff contract structure.
- `docs/team/handoff-acceptance-rules.md` — acceptance and rejection decisions.
- `docs/team/handoff-escalation-rules.md` — escalation and conflict resolution.
- `docs/team/workflow-lifecycle.md` — workflow stages and progression gates.
- `docs/team/blockers-replanning-and-state-transitions.md` — blocker management and replanning that may affect role participation.

## 12. Governing rule

Activate roles according to task scope, responsibility, dependencies, and risk.

Do not activate all roles by default. Do not omit required specialist participation because a task appears small. Do not confuse participation with ownership, handoff, approval, or authority.

The accountable owner remains accountable for the artifact package, specialists retain their domain authority, and the Delivery Lead coordinates cross-role execution without overriding either.
