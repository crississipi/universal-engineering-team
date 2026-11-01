# Handoff Escalation and Conflict-Resolution Rules

## Purpose

This document defines how the Universal Engineering Team identifies,
records, escalates, and resolves handoff disputes, cross-role conflicts,
and delivery blockers.

It supplements:

- `docs/team/responsibility-boundaries.md`
- `docs/team/handoff-contract-schema.md`
- `docs/team/handoff-acceptance-rules.md`
- `docs/team/producer-consumer-matrix.md`
- `docs/team/workflow.md`

This document does not create additional roles, transfer artifact
ownership, or grant one role universal authority over other specialists.

## 1. Governing principles

1. Resolve disagreements at the lowest appropriate level before escalating.
2. Escalate based on the subject and impact of the decision, not role seniority.
3. Preserve the existing responsibility and decision-authority boundaries.
4. Record the disagreement, supporting evidence, affected work, and
   requested decision.
5. Do not silently override another role's accountable decision.
6. Do not treat silence, inactivity, or an expired response window as approval.
7. Do not allow an unresolved dispute to be represented as accepted,
   verified, or complete.
8. The Delivery Lead coordinates escalation but does not replace
   specialist decision authority.
9. The Solution Architect resolves cross-system technical conflicts
   within architecture authority, not specialist decisions outside it.
10. Product, security, quality, and operational risks must be decided
    by the appropriate authorized authority.
11. A decision must include its rationale, scope, and consequences.
12. Escalation does not transfer ownership of the affected artifact.

## 2. What must be escalated

Escalation is appropriate when one or more of the following occurs:

- Producer and consumer cannot agree on whether a contract requirement
  has been satisfied.
- A handoff contract is ambiguous, contradictory, or incomplete.
- A required output is blocked by an unresolved dependency.
- Two specialist roles propose incompatible technical approaches.
- A decision affects multiple artifact packages or system boundaries.
- A proposed change conflicts with approved requirements or architecture.
- A security, privacy, safety, quality, accessibility, or operational
  concern cannot be resolved within the current work.
- A required decision or response has exceeded its agreed response window.
- Work is stalled because ownership or decision authority is unclear.
- A decision creates material scope, schedule, cost, or release impact.

Do not escalate routine implementation preferences that fall within
an individual specialist's decision authority.

## 3. Escalation levels

### Level 1 — Direct resolution

**Participants:** The directly involved producer and consumer, or
the specialists involved in the disagreement.

Use this level for:

- Missing context.
- Clarification of an existing acceptance check.
- Evidence review.
- Small corrections.
- Misunderstandings about a handoff's scope.
- Technical disagreements contained within one specialist domain.

Expected actions:

1. Identify the exact point of disagreement.
2. Reference the applicable contract, requirement, decision, or evidence.
3. Explain each position and its impact.
4. Agree on a correction, clarification, or decision request.
5. Record the outcome in the relevant task or handoff execution record.

The producer and consumer should attempt direct resolution before
requesting escalation unless an urgent risk requires immediate action.

### Level 2 — Specialist domain authority

**Authority:** The accountable owner of the affected specialist domain.

Escalate when direct discussion does not resolve a disagreement that
falls within a defined specialist responsibility.

Examples:

| Disagreement | Relevant decision authority |
|---|---|
| API contract definition or compatibility | API Manager |
| Backend implementation behavior | Backend Developer |
| Frontend implementation behavior | Frontend Developer |
| UX and interaction design | UX/UI Designer |
| Database schema or migration safety | Database Manager |
| Integration behavior and recovery | Integration Engineer |
| Data transformation and lineage | Data Engineer |
| Test methodology and quality evidence | QA Manager |
| Security findings and assessment | Penetration Tester |
| Infrastructure and operational readiness | DevOps/SRE |
| Performance measurement and interpretation | Performance Engineer |
| Accessibility assessment and findings | Accessibility Specialist |
| Documentation structure and knowledge representation | Technical Writer / Knowledge Engineer |
| Release process and sequencing | Release Manager |

The specialist owner reviews the evidence and decides within their
established responsibility and authority.

A specialist owner must not use domain authority to independently
change another role's requirements, contracts, or artifact ownership.

### Level 3 — Cross-domain or system-level resolution

**Primary coordination authority:** Solution Architect for cross-system
technical design conflicts.

Use this level when:

- Two or more specialist domains have incompatible technical constraints.
- A proposed solution changes system boundaries or integration patterns.
- A design decision affects multiple packages.
- Local specialist decisions create system-wide inconsistency.
- A technical conflict cannot be resolved within one specialist domain.

The Solution Architect:

1. Establishes the affected system boundaries and constraints.
2. Collects the positions and evidence from the relevant specialists.
3. Identifies feasible alternatives and trade-offs.
4. Records the architecture decision and affected packages.
5. Identifies required follow-up work and owners.

The Solution Architect does not:

- Take over specialist implementation.
- Override API, database, security, QA, accessibility, or operational
  assessment authority.
- Accept business or security risk on behalf of an authorized risk owner.
- Change product requirements without the appropriate product decision.

If the disagreement is not fundamentally architectural, route it to
the relevant domain authority instead.

### Level 4 — Authorized stakeholder or risk-owner decision

Use this level when the unresolved decision requires authority outside
the engineering team's defined specialist responsibilities.

Examples include:

- Product scope or priority trade-offs requiring stakeholder approval.
- Budget, schedule, or commercial trade-offs outside engineering authority.
- Acceptance of residual business or security risk.
- Conflicting stakeholder requirements.
- A decision that requires an exception to an approved business policy.
- An unresolved conflict for which no engineering role has decision authority.

The relevant authorized stakeholder or risk owner makes the decision.

The Delivery Lead coordinates the request, ensures the alternatives
and consequences are documented, and tracks the resulting action.

The team must not invent an internal role or assume that the Delivery Lead,
Release Manager, Solution Architect, or Penetration Tester can accept
a risk outside their authority.

If no authorized decision-maker is identified, record the issue as
blocked and request identification of the appropriate authority.

## 4. Decision routing by subject

Use this routing guide to avoid escalating every disagreement to the
same role.

| Decision subject | Primary authority | Escalation when unresolved |
|---|---|---|
| Requirements, scope, priority, acceptance criteria | Product Analyst, subject to stakeholder authority | Authorized product stakeholder |
| Cross-system architecture and technical trade-offs | Solution Architect | Authorized stakeholder if business authority or risk acceptance is required |
| API and event contract | API Manager | Solution Architect for cross-system impact; authorized stakeholder for external business trade-offs |
| Specialist implementation details | Relevant implementation owner | Solution Architect only when cross-system architecture is affected |
| Database schema and migration safety | Database Manager | Solution Architect for architecture impact; authorized operational authority for production risk |
| Test strategy and quality evidence | QA Manager | Product Analyst for acceptance-criteria ambiguity; authorized stakeholder for acceptance exceptions |
| Security findings | Penetration Tester for assessment and findings | Authorized security/business risk owner for risk acceptance |
| Infrastructure and operational readiness | DevOps/SRE | Solution Architect for architecture impact; Release Manager for release coordination |
| Performance findings | Performance Engineer | Solution Architect when cross-system design is affected; Product Analyst for product trade-offs |
| Accessibility findings | Accessibility Specialist | Product Analyst for requirement ambiguity; authorized stakeholder for approved exceptions |
| Release sequencing and coordination | Release Manager | Delivery Lead for delivery dependency coordination; authorized stakeholder for unresolved go/no-go authority |
| Delivery dependencies and blocker tracking | Delivery Lead | Relevant domain authority or authorized stakeholder based on the decision subject |

This table routes decisions to existing authorities. It does not grant
new decision powers.

## 5. Handoff acceptance disputes

When a producer challenges a consumer's rejection or partial acceptance:

1. The producer identifies the disputed acceptance check or rejection reason.
2. The producer provides evidence and explains why the requirement
   is considered satisfied.
3. The consumer explains the failed check and its supporting evidence.
4. Both parties verify the applicable contract ID and version.
5. Both parties attempt resolution at Level 1.
6. If unresolved, escalate according to the subject of the dispute.

Use the following routing:

- Contract interpretation or acceptance-check ambiguity:
  review the applicable contract and involve the accountable package
  owners.
- Technical correctness within one specialist domain:
  involve that domain's accountable owner.
- Cross-system technical consequences:
  involve the Solution Architect.
- Product requirement or acceptance-criteria ambiguity:
  involve the Product Analyst and, where necessary, the authorized
  product stakeholder.
- Security assessment disagreement:
  involve the Penetration Tester for assessment clarification.
  Risk acceptance remains with the authorized risk owner.

A consumer must not reject a submission based on a requirement that
does not exist in the applicable contract.

A producer must not treat disagreement with a rejection as automatic
acceptance.

Until the dispute is resolved, preserve the current decision and record
the handoff as unresolved or blocked as appropriate.

## 6. Response windows and timeout behavior

Response windows must be agreed at the project or task level based on:

- Urgency and risk.
- Work dependency.
- Delivery milestone.
- Complexity of the requested decision.
- Availability of required evidence and decision-makers.

Do not impose one universal response deadline on every handoff.

When no response window has been defined:

1. The Delivery Lead requests that the responsible parties establish
   a reasonable response window.
2. The agreed window and accountable responder are recorded.
3. The affected task remains visible in delivery tracking.

When an agreed response window expires:

1. Mark the issue as overdue or blocked in the relevant delivery record.
2. Notify the responsible role and Delivery Lead.
3. Escalate according to the decision subject and impact.
4. Record the next action and accountable responder.

A timeout must never:

- Automatically accept a handoff.
- Automatically reject a handoff.
- Transfer artifact ownership.
- Authorize a production change.
- Accept a security or business risk.
- Mark a task as verified or complete.

If an issue remains unresolved after escalation, keep it open and
identify the authority or information still required.

## 7. Urgent risk and stop-work conditions

Urgent security, privacy, safety, data integrity, or production stability
concerns must not wait for the normal escalation sequence.

The person identifying the concern must:

1. Record the observed issue and available evidence.
2. Notify the responsible specialist owner and relevant operational
   or security authority.
3. Recommend containment or suspension of the affected activity
   where appropriate.
4. Avoid unauthorized production changes or destructive actions.
5. Ensure the Delivery Lead and Release Manager are informed when
   delivery or release is affected.

The role with authority over the affected system or operation determines
the immediate technical action within its responsibility.

The Penetration Tester reports and validates security findings but does
not independently accept security risk or authorize production changes.

The Release Manager coordinates release impact but does not override
specialist risk findings.

The Delivery Lead coordinates the response but does not authorize
actions outside delegated authority.

A concern may be closed only when the appropriate owner records the
resolution or an authorized risk owner explicitly records an accepted
risk decision.

## 8. Conflict-resolution record

Every escalated issue should record:

- Issue or escalation identifier.
- Project, task, or handoff execution reference.
- Applicable contract ID and version, if relevant.
- Date identified.
- Roles and artifact packages affected.
- Description of the disagreement or blocker.
- Evidence and references.
- Decision subject and required authority.
- Impact on dependent work, schedule, quality, and release.
- Alternatives considered.
- Current escalation level.
- Current status.
- Decision, rationale, and decision-maker.
- Required follow-up actions and accountable owners.
- Resolution date or next review point.

Do not store credentials, access tokens, private keys, or unnecessary
sensitive data in an escalation record.

The repository location and technical format for escalation records
will be established separately if required.

## 9. Deadlock and unresolved authority

A deadlock exists when the relevant parties cannot reach a decision
after the appropriate escalation path has been followed.

When a deadlock occurs:

1. Confirm that the issue has been routed to the correct decision authority.
2. Confirm that the decision request includes evidence, constraints,
   alternatives, and consequences.
3. Identify whether the disagreement is technical, product-related,
   quality-related, operational, or a risk-acceptance matter.
4. Identify an authorized decision-maker if the matter is outside
   engineering authority.
5. Keep affected work blocked when proceeding would violate an
   unresolved required input, safety constraint, or approval gate.
6. Continue independent work only when it does not depend on the
   unresolved decision and does not create additional risk.
7. Record the decision or the reason no authorized decision is available.

The Delivery Lead may recommend sequencing alternatives, scope isolation,
or deferral to reduce delivery impact.

The Delivery Lead must not manufacture consensus or mark a deadlock
resolved without a documented decision from the appropriate authority.

## 10. Decision recording and follow-through

Every resolved escalation must result in one or more of:

- A clarified existing requirement or contract.
- An approved contract version change.
- An architecture decision record.
- A specialist implementation decision.
- A documented product or scope decision.
- A documented risk decision by an authorized risk owner.
- A revised task plan or dependency.
- A deferred or cancelled work item with a reason.

The accountable owner updates the relevant artifact or decision record.

The Delivery Lead updates delivery tracking and communicates the
resulting dependency, status, and next actions.

The Release Manager updates release coordination records when the
decision affects release readiness or sequencing.

The Technical Writer / Knowledge Engineer updates relevant documentation
when the decision changes verified technical or operational knowledge.

Do not treat a conversation or verbal agreement as a durable decision
when the outcome materially changes scope, architecture, risk, or
acceptance expectations.

## 11. Relationship to other handoff rules

This document defines escalation and conflict-resolution behavior.

`docs/team/handoff-contract-schema.md` defines reusable handoff contracts.

`docs/team/handoff-acceptance-rules.md` defines acceptance, rejection,
partial acceptance, and resubmission behavior.

`docs/team/responsibility-boundaries.md` defines role accountability
and decision authority.

`docs/team/workflow.md` describes the overall delivery and handoff process.

These documents must be interpreted together.

Escalation does not create a new artifact owner, reviewer requirement,
or approval authority.

## 12. Maintenance

Update this document when escalation paths, decision authority,
or conflict-resolution procedures change.

Before changing the rules:

1. Confirm the affected role responsibilities.
2. Confirm that no existing role is given authority outside its domain.
3. Review the impact on handoff acceptance and delivery workflow.
4. Update related documentation consistently.
5. Run all applicable repository validators.

Never resolve a recurring conflict by silently expanding a role's authority.