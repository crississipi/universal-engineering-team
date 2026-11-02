# Decision Records

## 1. Purpose

Decision records preserve significant decisions made during an execution and establish their rationale, authority, impact, and traceability.

They provide a canonical record of:

- What was decided.
- Why the decision was necessary.
- Which alternatives were considered.
- Who proposed the decision.
- Who authorized or rejected it.
- Which authority governed the decision.
- Which execution records are affected.
- What evidence supports the decision.
- Whether the decision has been superseded or withdrawn.

Decision records provide accountability and prevent important execution decisions from existing only in conversations, informal notes, or undocumented assumptions.

A decision record does not automatically authorize actions outside the decision-maker's established authority.

## 2. Canonical Location

**File:** `decisions.yml`

**Location:** `executions/<execution-id>/decisions.yml`

Each decision record belongs to exactly one execution.

Reusable decision governance rules remain defined in:

- `docs/team/responsibility-boundaries.md`
- `docs/team/orchestration-responsibilities.md`
- `docs/team/handoff-acceptance-rules.md`

## 3. Decision Identifier

Decision identifiers must use:

`DEC-<UUID>`

Each decision identifier must be unique across the repository.

An existing decision identifier must never be reassigned to another decision.

## 4. Canonical Decision Record

Each decision record must contain:

| Field | Required | Description |
|---|---|---|
| `decision_id` | Yes | Unique decision identifier |
| `execution_id` | Yes | Parent execution identifier |
| `decision_type` | Yes | Controlled decision classification |
| `title` | Yes | Short descriptive title |
| `context` | Yes | Situation or problem requiring a decision |
| `decision_status` | Yes | Current decision lifecycle status |
| `decision_outcome` | Conditional | Domain-specific outcome when required |
| `rejection_code` | Conditional | Applicable rejection classification |
| `proposed_by_role` | Yes | Role proposing the decision |
| `decided_by_role` | Conditional | Role responsible for the decision |
| `decision_authority` | Yes | Authority basis for the decision |
| `options_considered` | Yes | Alternatives considered |
| `selected_option` | Conditional | Selected option or outcome |
| `rationale` | Yes | Explanation supporting the decision |
| `impact_summary` | Yes | Expected or actual material impact |
| `affected_record_refs` | Yes | Related canonical execution record identifiers |
| `evidence_refs` | Optional | Supporting evidence identifiers |
| `supersedes_decision_id` | Optional | Previous decision replaced by this decision |
| `related_decision_ids` | Optional | Related decision identifiers |
| `created_at` | Yes | Record creation timestamp |
| `updated_at` | Yes | Last material update timestamp |
| `decided_at` | Conditional | Actual decision timestamp |
| `history` | Yes | Material decision history |

Conditional fields must be populated when their applicable status or decision type requires them.

Optional fields must be omitted when they do not apply.

An empty `affected_record_refs` collection is permitted only when the decision genuinely does not affect another execution record. Explain the situation in `context` and `impact_summary`.

## 5. Decision Types

Use the following controlled vocabulary:

- `product_scope`
- `architecture`
- `api_contract`
- `data_management`
- `implementation`
- `integration`
- `security`
- `quality`
- `operations`
- `performance`
- `accessibility`
- `handoff_acceptance`
- `release`
- execution_closure
- `delivery`
- `other`

`execution_closure`: Formal approval or rejection of an execution's closure after completion, verification, and applicable closure requirements have been assessed.

An execution closure decision must reference the execution's canonical closure record. Approval must not be granted solely because the execution has reached the Closure workflow stage. The decision-maker must have the applicable authority under existing governance.

The closure record references this decision through `closure_decision_id`. A successful closure requires the decision status to be `approved`. A rejected or withdrawn closure decision does not authorize closure.

The `other` classification requires a meaningful explanation.

New decision types must be introduced through governance review rather than created arbitrarily for individual records.

## 6. Decision Lifecycle Status

Use the following statuses:

| Status | Description |
|---|---|
| `proposed` | Decision has been recorded but not yet submitted for formal review |
| `under_review` | Decision is being evaluated by the appropriate authority |
| `approved` | Decision has been authorized |
| `rejected` | Decision proposal has been rejected |
| `superseded` | A newer decision has replaced this decision |
| `withdrawn` | Decision proposal has been withdrawn before authorization |

### 6.1 Permitted Status Transitions

| Current status | Permitted next statuses |
|---|---|
| `proposed` | `under_review`, `withdrawn` |
| `under_review` | `approved`, `rejected`, `withdrawn` |
| `approved` | `superseded` |
| `rejected` | Terminal |
| `superseded` | Terminal |
| `withdrawn` | Terminal |

Rejected, superseded, and withdrawn decisions must not be silently reopened.

If a rejected or withdrawn proposal needs reconsideration, create a new decision record.

If an approved decision needs to be replaced, create a new decision record and reference the previous decision through `supersedes_decision_id`.

### 6.2 Decision Authorization

A decision may be marked `approved` only after authorization by the applicable decision authority.

`decided_by_role` identifies the role responsible for the decision.

`decision_authority` explains the authority under which the decision was made.

The decision-maker must be authorized under the existing responsibility and escalation rules.

The Delivery Lead coordinates execution but is not a universal approval authority.

The Solution Architect may coordinate resolution of cross-system technical conflicts within the established governance boundaries, but must not automatically approve decisions outside that authority.

A role must not approve its own decision merely because it proposed or produced the associated artifact.

## 7. Domain-Specific Decision Outcomes

Decision lifecycle status and domain-specific outcome are separate dimensions.

`decision_status` records the lifecycle of the decision.

`decision_outcome` records the result within the decision's domain.

### 7.1 Handoff Acceptance Decisions

For decisions with:

`decision_type: handoff_acceptance`

Use the following controlled outcomes:

- `accepted`
- `partially_accepted`
- `rejected`
- `blocked`

Every handoff acceptance decision must contain `decision_outcome`.

For a `rejected` outcome, `rejection_code` must contain an applicable rejection code defined in:

`docs/team/handoff-acceptance-rules.md`

The approved rejection codes are:

- `missing_output`
- `incomplete_output`
- `failed_acceptance_check`
- `invalid_or_inconsistent_output`
- `missing_required_context`
- `unsupported_claim`
- `unsafe_or_prohibited_content`
- `scope_mismatch`

### 7.2 Lifecycle and Outcome Independence

The decision lifecycle must continue to follow the decision status transition rules.

A decision with an outcome of `partially_accepted` may have a lifecycle status of `approved` when the authorized decision-maker has approved that partial acceptance.

A decision with an outcome of `accepted` may also have a lifecycle status of `approved`.

A decision with an outcome of `rejected` must not be interpreted as an approved handoff.

A decision with an outcome of `blocked` must not be interpreted as authorization to proceed.

A handoff decision's lifecycle status must never substitute for its domain-specific outcome.

### 7.3 Handoff Record Consistency

The canonical handoff execution record must reference the decision through its `current_decision_id` or applicable submission `decision_id`.

The handoff execution record and decision record must agree on their domain-specific outcome.

The decision record remains authoritative for:

- Decision rationale.
- Proposer.
- Decision-maker.
- Decision authority.
- Decision lifecycle.
- Domain-specific decision outcome.

The handoff execution record remains authoritative for:

- Transfer instance.
- Submission history.
- Producer and consumer context.
- Current submission reference.
- Current handoff execution status.

A decision must not duplicate the full handoff submission history.

## 8. Decision Options and Rationale

### 8.1 Options Considered

`options_considered` records the meaningful alternatives evaluated.

Each option should contain:

- `option_id`
- `description`
- `advantages`
- `disadvantages`
- `constraints`

At least one option must be recorded.

The selected option must correspond to an option that was actually considered, except when a domain-specific outcome uses a documented controlled outcome instead.

### 8.2 Selected Option

`selected_option` identifies the approved alternative or recorded outcome.

A decision marked `approved` must identify its selected option or domain-specific outcome.

A rejected or withdrawn decision may omit `selected_option` when no alternative was authorized.

### 8.3 Rationale

`rationale` must explain why the decision was selected or rejected.

It should address relevant considerations such as:

- Requirements.
- Technical constraints.
- Security implications.
- Operational impact.
- Cost or resource implications.
- Risks.
- Alternatives considered.
- Applicable governance requirements.

Avoid unsupported claims and undocumented assumptions.

## 9. Impact and Related Records

`impact_summary` describes the expected or actual material effects of the decision.

Consider relevant effects on:

- Product scope.
- Architecture.
- API contracts.
- Data structures.
- Implementation.
- Integrations.
- Security.
- Quality.
- Operations.
- Performance.
- Accessibility.
- Release.
- Delivery.

Use `affected_record_refs` to reference canonical execution records affected by the decision.

Possible references include:

- Work items: `WI-<UUID>`
- Role activations: `ACT-<UUID>`
- Dependencies: `DEP-<UUID>`
- Handoff executions: `HEX-<UUID>`
- Evidence: `EVD-<UUID>`
- Blockers: `BLK-<UUID>`
- Re-planning records: `RPL-<UUID>`

Artifact package references use canonical identifiers defined in:

`docs/team/ownership.yml`

Artifact package identifiers are not execution-specific records. They must be resolved against the ownership catalog rather than execution record collections.

All execution-scoped references must belong to the same execution.

The decision record must not duplicate the full content of the referenced records.

## 10. Evidence References

Use `evidence_refs` to identify supporting evidence.

Evidence references must resolve to canonical records in the same execution.

Evidence verification remains governed by:

`docs/team/evidence-records.md`

A decision must not treat an unverified evidence item as verified proof.

The decision-maker remains responsible for evaluating whether the available evidence is sufficient for the decision.

## 11. Supersession and Related Decisions

When an approved decision is replaced:

1. Create a new decision record.
2. Reference the previous decision through `supersedes_decision_id`.
3. Record the reason for replacement.
4. Update the previous decision's status to `superseded`.
5. Preserve the previous decision's history.
6. Identify affected records requiring reassessment or modification.

The new decision must not silently erase the earlier decision.

`related_decision_ids` may reference other decisions that provide relevant context or dependencies.

Supersession relationships must not form cycles.

## 12. History Requirements

The `history` collection preserves material changes to a decision record.

Each history entry must contain:

| Field | Required | Description |
|---|---|---|
| `changed_at` | Yes | Timestamp of the change |
| `changed_by_role` | Yes | Role responsible for the change |
| `change_type` | Yes | Classification of the change |
| `reason` | Yes | Explanation for the change |
| `previous_status` | Conditional | Previous decision lifecycle status |
| `new_status` | Conditional | New decision lifecycle status |
| `changed_fields` | Optional | Other materially changed fields |

History must preserve:

- Initial proposal.
- Review activity.
- Approval or rejection.
- Withdrawal.
- Supersession.
- Material changes to rationale or impact.
- Changes to affected records.
- Changes to decision authority when permitted.

Approved decisions must not be silently modified.

If an approved decision requires material modification, create a new decision record and follow the supersession rules.

## 13. Illustrative YAML Structure

The following examples are illustrative only. They are not actual execution records.

### 13.1 General Architecture Decision

```yaml
decisions:
  - decision_id: "DEC-<UUID>"
    execution_id: "EXE-<UUID>"

    decision_type: "architecture"
    title: "Use a modular service architecture"

    context: >
      The project requires independent service boundaries
      to support maintainability and integration.

    decision_status: "approved"

    proposed_by_role: "solution-architect"
    decided_by_role: "solution-architect"

    decision_authority: >
      Approved under the project's established
      architecture decision authority.

    options_considered:
      - option_id: "OPT-1"
        description: "Modular service architecture"
        advantages:
          - "Clear service boundaries"
          - "Independent module development"
        disadvantages:
          - "Requires interface coordination"
        constraints:
          - "Must follow the approved API contracts"

      - option_id: "OPT-2"
        description: "Single tightly coupled application"
        advantages:
          - "Simpler initial structure"
        disadvantages:
          - "Greater coupling as the system grows"
        constraints: []

    selected_option: "OPT-1"

    rationale: >
      The modular architecture better supports the
      project's maintainability and integration needs.

    impact_summary: >
      Service boundaries and integration contracts
      must be defined before dependent implementation.

    affected_record_refs:
      - "WI-<UUID>"

    evidence_refs: []

    created_at: "2026-11-02T10:00:00Z"
    updated_at: "2026-11-02T10:30:00Z"
    decided_at: "2026-11-02T10:30:00Z"

    history:
      - changed_at: "2026-11-02T10:00:00Z"
        changed_by_role: "solution-architect"
        change_type: "created"
        reason: "Architecture decision proposed."

      - changed_at: "2026-11-02T10:30:00Z"
        changed_by_role: "solution-architect"
        change_type: "status_changed"
        reason: "Architecture decision approved."
        previous_status: "under_review"
        new_status: "approved"
```

### 13.2 Handoff Acceptance Decision

```yaml
decisions:
  - decision_id: "DEC-<UUID>"
    execution_id: "EXE-<UUID>"

    decision_type: "handoff_acceptance"
    title: "Partially accept API contract handoff"

    context: >
      The producer submitted the API contract.
      The response schema passed review, but the
      error-handling specification requires revision.

    decision_status: "approved"
    decision_outcome: "partially_accepted"

    proposed_by_role: "api-manager"
    decided_by_role: "backend-developer"

    decision_authority: >
      Consumer acceptance authority under the
      applicable handoff acceptance contract.

    options_considered:
      - option_id: "OPT-1"
        description: "Accept all submitted outputs"
        advantages:
          - "Allows immediate downstream implementation"
        disadvantages:
          - "Error-handling requirements remain incomplete"
        constraints:
          - "All mandatory acceptance checks must pass"

      - option_id: "OPT-2"
        description: "Partially accept separable outputs"
        advantages:
          - "Allows safe use of completed outputs"
        disadvantages:
          - "Remaining output requires resubmission"
        constraints:
          - "Accepted outputs must be independently usable"

      - option_id: "OPT-3"
        description: "Reject the entire submission"
        advantages:
          - "Avoids accepting incomplete deliverables"
        disadvantages:
          - "Delays all downstream work"
        constraints: []

    selected_option: "OPT-2"

    rationale: >
      The response schema is independently usable.
      Error-handling requirements remain incomplete
      and must be resubmitted.

    impact_summary: >
      Downstream work may use the accepted response
      schema, but work requiring the incomplete
      error-handling specification remains restricted.

    affected_record_refs:
      - "HEX-<UUID>"

    evidence_refs: []

    created_at: "2026-11-02T10:00:00Z"
    updated_at: "2026-11-02T10:30:00Z"
    decided_at: "2026-11-02T10:30:00Z"

    history:
      - changed_at: "2026-11-02T10:00:00Z"
        changed_by_role: "api-manager"
        change_type: "created"
        reason: "Handoff decision submitted for review."

      - changed_at: "2026-11-02T10:30:00Z"
        changed_by_role: "backend-developer"
        change_type: "decision_recorded"
        reason: "Separable outputs partially accepted."
        previous_status: "under_review"
        new_status: "approved"
```

The identifiers, timestamps, roles, and outcomes above are illustrative placeholders. Actual records must use real identifiers and authorized decision-makers.

## 14. Validation Requirements

The future decision validator must enforce:

1. Decision identifiers are unique.
2. Identifiers follow `DEC-<UUID>`.
3. Every decision references an existing execution.
4. Decision types use the approved vocabulary.
5. Lifecycle statuses use the approved vocabulary.
6. Required fields are present.
7. Conditional fields are present when required.
8. Referenced roles are valid for the execution.
9. Decision authority is consistent with existing governance.
10. Approved decisions identify a selected option or applicable domain-specific outcome.
11. Options and selected-option references are internally consistent.
12. Affected execution record references resolve to existing records in the same execution.
13. Artifact package references resolve against the canonical ownership catalog.
14. Evidence references resolve to evidence records in the same execution.
15. Supersession references resolve to valid decision records.
16. Supersession relationships do not form cycles.
17. Status transitions follow the permitted lifecycle.
18. Material changes preserve history.
19. Approved decisions are not silently modified.
20. Handoff acceptance decisions require a valid `decision_outcome`.
21. Handoff outcomes use only the approved vocabulary.
22. Rejected handoff decisions include an applicable `rejection_code`.
23. Decision lifecycle status and domain-specific outcome are validated independently.
24. Referenced handoff execution and submission records agree with the canonical decision outcome.
25. Non-handoff decisions do not use handoff-specific outcomes or rejection codes unless an explicitly approved decision type defines them.
26. Decision records do not independently override existing responsibility or approval authority.

## 15. Implementation Boundary

This specification defines decision record structure and governance requirements.

It does not introduce:

- Automatic decision approval.
- A new universal approval authority.
- Automatic changes to work-item status.
- Automatic dependency satisfaction.
- Automatic handoff acceptance.
- Automatic role activation.
- Automatic workflow transitions.
- Replacement of existing escalation rules.

Schemas and automated validation are deferred to Phase 1.4.7.

## 16. Acceptance Criteria

- Decision identifiers and execution ownership are explicit.
- Decision types use a controlled vocabulary.
- Lifecycle states and transitions are defined.
- Decision proposal and approval authority are distinct.
- Options and rationale are traceable.
- Domain-specific outcomes are separate from lifecycle status.
- Handoff acceptance decisions have explicit outcomes.
- Rejection codes follow existing handoff acceptance rules.
- Affected records and supporting evidence are traceable.
- Supersession preserves historical decisions.
- History requirements are explicit.
- Validation requirements are documented.
- Examples are clearly illustrative.