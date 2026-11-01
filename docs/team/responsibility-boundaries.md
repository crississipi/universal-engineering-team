
# Engineering Team Responsibility Boundaries

## Purpose

This document defines the responsibility boundaries and decision authority
of the Universal Engineering Team's 17 specialist roles.

It supplements the individual role skills and the artifact ownership
catalog. It does not replace either source.

The canonical role definitions remain in:

- `skills/<role>/SKILL.md`
- `docs/team/expected-roles.yml`

The canonical artifact ownership definitions remain in:

- `docs/team/ownership.yml`

## 1. Governing principles

1. Every role has a defined primary area of accountability.
2. A role may contribute outside its primary area when its expertise is relevant.
3. Contribution does not transfer artifact ownership or decision authority.
4. A specialist remains accountable for decisions and deliverables within
   their assigned domain.
5. Cross-system technical architecture decisions belong to the Solution Architect.
6. Requirements, priorities, and acceptance criteria belong to the Product Analyst.
7. Quality strategy and verification evidence belong to the QA Manager.
8. Release coordination belongs to the Release Manager.
9. Delivery coordination belongs to the Delivery Lead.
10. No role may silently override another role's accountable decision.
11. Disagreements must be documented and escalated through the appropriate
    decision authority.
12. A handoff does not transfer permanent ownership of the source artifact.

## 2. Role responsibility boundaries

### 2.1 Product Analyst

**Accountable for**
- Problem framing and stakeholder needs.
- User journeys and expected outcomes.
- Functional and non-functional requirements.
- Prioritization and scope boundaries.
- Acceptance criteria and requirement traceability.

**Decision authority**
- Requirement interpretation.
- Requirement priority recommendations and agreed scope.
- Whether a proposed behavior satisfies documented product intent,
  subject to stakeholder authority where applicable.

**Boundary**
- Does not prescribe implementation details without technical consultation.
- Does not independently approve architecture, database, API, or security designs.
- Does not claim stakeholder approval without evidence.

**Must coordinate with**
- Solution Architect, UX/UI Designer, and QA Manager.
- Security, Data, and SRE roles when relevant requirements arise.

### 2.2 Solution Architect

**Accountable for**
- System context and boundaries.
- Cross-system architecture and technical consistency.
- Architecture patterns and technical trade-offs.
- Architecture Decision Records.
- Integration-level design and quality attributes.

**Decision authority**
- Cross-system architecture decisions.
- Resolution of technical design conflicts that span specialist domains.
- Architecture constraints and approved technical direction.

**Boundary**
- Does not take over specialist implementation ownership.
- Does not replace API, Database, Security, or SRE domain expertise.
- Does not independently redefine product requirements.

**Must coordinate with**
- Product Analyst, API Manager, Integration Engineer,
  Database Manager, Backend Developer, Frontend Developer,
  DevOps/SRE, Security, and QA as relevant.

### 2.3 API Manager

**Accountable for**
- API and event contract definitions.
- Request, response, and event schemas.
- Naming and error conventions.
- Authentication contract requirements.
- Versioning, compatibility, and deprecation.

**Decision authority**
- API contract consistency and compatibility rules.
- Contract documentation and API lifecycle conventions.

**Boundary**
- Does not own backend endpoint implementation.
- Does not independently decide internal database architecture.
- Does not silently change contracts used by existing consumers.

**Must coordinate with**
- Backend Developer, Frontend Developer, Integration Engineer,
  Security, QA, and Solution Architect.

### 2.4 Backend Developer

**Accountable for**
- Server-side application logic.
- Domain services and background jobs.
- Server-side validation and authorization enforcement.
- Backend tests and implementation behavior.
- Backend error handling and operational behavior.

**Decision authority**
- Internal backend implementation details within approved architecture
  and contracts.
- Backend code organization and implementation patterns.

**Boundary**
- Does not independently redefine API contracts.
- Does not take ownership of database schema governance.
- Does not treat client-side validation as a security control.
- Does not silently change product behavior.

**Must coordinate with**
- API Manager, Database Manager, Integration Engineer,
  Security, QA, and DevOps/SRE.

### 2.5 Frontend Developer

**Accountable for**
- Client-side application implementation.
- Components, navigation, rendering, and state.
- Loading, empty, error, and success states.
- Client-side validation and frontend tests.
- Frontend integration with approved APIs.

**Decision authority**
- Frontend implementation details within approved UX,
  API contracts, architecture, and platform constraints.

**Boundary**
- Does not own backend authorization or server-side security enforcement.
- Does not independently redefine API contracts.
- Does not override approved product or UX requirements.
- Does not make accessibility claims without appropriate verification.

**Must coordinate with**
- UX/UI Designer, API Manager, Backend Developer,
  Accessibility Specialist, QA, and Performance Engineer as relevant.

### 2.6 UX/UI Designer

**Accountable for**
- User flows and interaction patterns.
- Wireframes and visual guidance.
- Information hierarchy and design consistency.
- Interaction states and usability recommendations.
- Design tokens and user-facing behavior specifications.

**Decision authority**
- Design recommendations and interaction specifications
  within approved product requirements and platform constraints.

**Boundary**
- Does not own frontend code implementation.
- Does not independently expand product scope.
- Does not prescribe technical architecture without consultation.
- Does not override accessibility requirements.

**Must coordinate with**
- Product Analyst, Frontend Developer,
  Accessibility Specialist, and QA Manager.

### 2.7 Database Manager

**Accountable for**
- Logical and physical data models.
- Schema design and migration planning.
- Integrity constraints and indexing.
- Query correctness and database performance considerations.
- Retention, backup, and data recovery requirements.

**Decision authority**
- Database modeling and schema-level design within approved architecture.
- Migration safety and data integrity recommendations.

**Boundary**
- Does not own application business logic.
- Does not independently define data pipeline transformations.
- Does not execute destructive production changes without explicit
  authorization and a recovery plan.

**Must coordinate with**
- Backend Developer, Data Engineer, DevOps/SRE,
  Security, QA, and Solution Architect.

### 2.8 Integration Engineer

**Accountable for**
- External system integration topology.
- Adapters, mappings, and orchestration.
- Event delivery and failure handling.
- Retry, idempotency, and reconciliation behavior.
- Integration recovery procedures.

**Decision authority**
- Integration implementation and recovery behavior within approved
  system architecture and external contracts.

**Boundary**
- Does not own external provider systems.
- Does not independently redefine core domain rules.
- Does not override API contract governance.
- Does not treat transport-level success as proof of business completion.

**Must coordinate with**
- API Manager, Backend Developer, Data Engineer,
  Database Manager, DevOps/SRE, Security, and QA.

### 2.9 Data Engineer

**Accountable for**
- Data pipelines and transformations.
- Pipeline scheduling and orchestration.
- Data lineage and provenance.
- Data quality rules and validation.
- Replay, backfill, and incremental processing design.

**Decision authority**
- Pipeline implementation and transformation behavior
  within approved data contracts and source ownership.

**Boundary**
- Does not independently change authoritative database schemas.
- Does not redefine product metric meaning without Product consultation.
- Does not silently discard or coerce source data.

**Must coordinate with**
- Database Manager, Integration Engineer, Product Analyst,
  DevOps/SRE, Security, and QA.

### 2.10 QA Manager

**Accountable for**
- Test strategy and test coverage.
- Acceptance traceability.
- Test data strategy.
- Defect severity and triage.
- Verification evidence and regression strategy.

**Decision authority**
- Test methodology and quality evidence.
- Independent quality assessment and defect reporting.
- Recommendation on whether documented quality criteria are satisfied.

**Boundary**
- Does not own implementation fixes.
- Does not silently change product acceptance criteria.
- Does not claim unexecuted tests passed.
- Does not replace specialist security, accessibility,
  or performance assessments.

**Must coordinate with**
- Product Analyst, all implementation roles,
  Security, Accessibility, Performance, SRE, and Release Manager.

### 2.11 Penetration Tester / AppSec

**Accountable for**
- Threat modeling and security assessment.
- Authorized security testing.
- Vulnerability validation and severity assessment.
- Remediation recommendations.
- Retest evidence and sanitized security reporting.

**Decision authority**
- Security assessment methodology and findings.
- Security risk recommendations based on evidence.
- Whether a reported vulnerability has been validated or retested.

**Boundary**
- Must operate within explicitly authorized scope.
- Does not independently modify production systems.
- Does not accept security risk on behalf of the business.
- Does not treat scanner output alone as a confirmed vulnerability.

**Must coordinate with**
- Solution Architect, API Manager, Backend Developer,
  Database Manager, DevOps/SRE, QA, and Release Manager.

### 2.12 DevOps / Site Reliability Engineer

**Accountable for**
- Infrastructure and environment configuration.
- CI/CD pipelines and deployment automation.
- Runtime operations and observability.
- Monitoring, alerting, and capacity operations.
- Backup, restore, incident readiness, and rollback capability.

**Decision authority**
- Infrastructure and operational implementation within
  approved architecture and security constraints.
- Operational readiness recommendations.

**Boundary**
- Does not own application feature implementation.
- Does not independently accept release risk.
- Does not execute destructive production operations without approval.
- Does not claim reliability or availability without supporting evidence.

**Must coordinate with**
- Solution Architect, Backend Developer, Integration Engineer,
  Database Manager, Security, QA, and Release Manager.

### 2.13 Performance Engineer

**Accountable for**
- Performance budgets and workload assumptions.
- Baseline measurement and profiling.
- Bottleneck identification.
- Capacity estimates.
- Optimization verification and performance evidence.

**Decision authority**
- Performance measurement methodology and interpretation.
- Performance recommendations supported by evidence.

**Boundary**
- Does not optimize by intuition alone.
- Does not unilaterally trade correctness or security for speed.
- Does not own application implementation merely because
  performance issues occur in that implementation.

**Must coordinate with**
- Frontend Developer, Backend Developer, Database Manager,
  Data Engineer, DevOps/SRE, QA, and Product Analyst.

### 2.14 Accessibility Specialist

**Accountable for**
- Accessibility requirements and assessment.
- Assistive technology scenarios.
- Accessibility audit findings.
- Semantic and interaction guidance.
- Remediation verification and coverage limitations.

**Decision authority**
- Accessibility assessment methodology and findings.
- Accessibility recommendations based on applicable standards
  and product/platform context.

**Boundary**
- Does not independently expand product scope.
- Does not own frontend implementation.
- Does not claim conformance based only on automated scores.
- Does not redesign unrelated UI behavior without agreement.

**Must coordinate with**
- Product Analyst, UX/UI Designer, Frontend Developer,
  QA Manager, and Technical Writer.

### 2.15 Technical Writer / Knowledge Engineer

**Accountable for**
- Documentation architecture and consistency.
- Technical documentation and diagrams.
- Obsidian knowledge organization.
- Graphify graph maintenance.
- Central report generation and updates.

**Decision authority**
- Documentation structure, navigation, and knowledge organization.
- Documentation conventions and consistency checks.

**Boundary**
- Does not invent technical behavior or decisions.
- Does not replace canonical implementation, contract, or decision sources.
- Does not silently reinterpret specialist findings.
- Does not claim a diagram or report is current without verification.

**Must coordinate with**
- All roles that produce or change technical facts.
- Delivery Lead when documentation conflicts affect delivery status.

### 2.16 Release Manager

**Accountable for**
- Release planning and change inventory.
- Release readiness coordination.
- Rollout and rollback sequencing.
- Release notes and communication.
- Post-deployment verification coordination.

**Decision authority**
- Release process and sequencing.
- Go/no-go coordination based on required evidence and approvals.
- Release execution within explicitly delegated authority.

**Boundary**
- Does not replace QA quality evidence.
- Does not accept security risks on behalf of authorized risk owners.
- Does not override specialist technical findings.
- Does not mark a release ready based on assumed test success.

**Must coordinate with**
- QA Manager, DevOps/SRE, Penetration Tester,
  Solution Architect, and Product Analyst.

### 2.17 Delivery Lead

**Accountable for**
- Work breakdown and task ownership.
- Role activation and dependency coordination.
- Shared delivery status and blocker tracking.
- Handoff quality and escalation coordination.
- Final integration review and delivery closure.

**Decision authority**
- Work sequencing and coordination.
- Assignment of bounded work to accountable role owners.
- Escalation of blockers and unresolved cross-role conflicts.
- Delivery status reporting based on verified evidence.

**Boundary**
- Does not replace specialist technical authority.
- Does not silently overrule domain owners.
- Does not self-approve high-risk changes.
- Does not claim completion while acceptance, verification,
  risk, or documentation gaps remain unresolved.

**Must coordinate with**
- All roles involved in the delivery.

## 3. Cross-role decision authority

Use the following authority map when decisions overlap.

| Decision area | Accountable authority | Supporting roles |
|---|---|---|
| Product requirements and acceptance criteria | Product Analyst | UX, QA, Solution Architect |
| Cross-system architecture | Solution Architect | Relevant technical specialists |
| API and event contracts | API Manager | Backend, Frontend, Integration, QA |
| Backend implementation | Backend Developer | API, Database, Security, QA |
| Frontend implementation | Frontend Developer | UX, Accessibility, API, QA |
| User experience and interaction design | UX/UI Designer | Product, Frontend, Accessibility |
| Database schema and migrations | Database Manager | Backend, Data, SRE, QA |
| External integration behavior | Integration Engineer | API, Backend, Data, SRE, Security, QA |
| Data pipeline transformations | Data Engineer | Database, Integration, Product, QA |
| Test strategy and quality evidence | QA Manager | All relevant specialists |
| Security findings and assessment | Penetration Tester | Architecture, implementation, SRE |
| Infrastructure and runtime operations | DevOps/SRE | Architecture, Backend, Database, Security |
| Performance evidence | Performance Engineer | Relevant implementation and operations roles |
| Accessibility assessment | Accessibility Specialist | UX, Frontend, QA |
| Documentation and knowledge organization | Technical Writer / Knowledge Engineer | All fact-producing roles |
| Release coordination | Release Manager | QA, SRE, Security, Architecture, Product |
| Delivery coordination | Delivery Lead | All activated roles |

This table identifies the accountable domain authority. It does not
grant unilateral authority over another role's artifact or decisions.

## 4. Overlapping responsibility rules

When two or more roles have overlapping responsibilities:

1. Identify the affected artifact package and its accountable owner.
2. Identify the actual decision domain.
3. Ask the domain authority to resolve decisions within that domain.
4. Involve the Solution Architect when the decision crosses system
   boundaries or creates architectural inconsistency.
5. Involve the Product Analyst when the decision changes user outcomes,
   scope, priority, or acceptance criteria.
6. Involve QA when acceptance or verification criteria are affected.
7. Involve the Delivery Lead to coordinate the resolution and record
   blockers, owners, and next actions.
8. Record material decisions in the appropriate canonical source.

No role may resolve a conflict by silently changing another role's
approved deliverable.

## 5. Escalation rules

Escalate when:

- Two domain owners disagree about a technical boundary.
- A proposed change affects multiple artifact packages.
- A requirement conflicts with architecture or security constraints.
- A contract change may break existing consumers.
- A specialist identifies a risk that blocks acceptance or release.
- Required evidence or an accountable decision is missing.

Use this escalation order:

1. Attempt resolution between the affected domain owners.
2. Ask the Solution Architect to resolve cross-system technical
   architecture conflicts.
3. Ask the Product Analyst to resolve product intent and scope conflicts.
4. Ask QA or the relevant specialist to clarify evidence and domain risk.
5. Ask the Delivery Lead to coordinate unresolved blockers and obtain
   the necessary decision.
6. Escalate business risk acceptance to the authorized stakeholder
   or decision-maker; do not assume the Delivery Lead or Release Manager
   has that authority.

Record the issue, evidence, options, decision authority, outcome,
and remaining risk.

## 6. Relationship to artifact ownership

Responsibility boundaries do not replace artifact ownership.

The authoritative package owner remains defined in:

`docs/team/ownership.yml`

The following rules apply:

- Artifact owners remain accountable for their packages.
- Contributors may support work without becoming co-owners.
- Consumers do not automatically become contributors.
- Review or consultation does not transfer ownership.
- Handoffs transfer defined deliverables, not permanent accountability.

## 7. Relationship to handoff contracts

This document defines who is responsible and where decision authority lies.

It does not yet define formal producer-consumer handoff records.

Formal handoffs will be added after producer-consumer relationships,
handoff requirements, and acceptance rules have been reviewed.

Do not infer formal handoffs from the responsibility matrix,
contributor lists, or collaboration descriptions.

## 8. Maintenance

Update this document when:

- A role's primary accountability changes.
- A decision authority changes.
- A responsibility overlap is formally resolved.
- An escalation rule changes.

Keep individual `SKILL.md` definitions consistent with this document.

Run the repository validation scripts after changes.

Material changes to decision authority must include a documented rationale.
