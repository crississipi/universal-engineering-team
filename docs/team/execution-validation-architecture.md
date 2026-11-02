# Execution Validation Architecture

## 1. Purpose

This document defines the architecture, boundaries, and governance principles for validating execution records.

It establishes how YAML execution records are parsed, structurally validated, checked for cross-record consistency, and evaluated against deterministic lifecycle and governance rules.

This document is the architectural reference for Phase 1.4.7.

The individual JSON Schemas are maintained under `schemas/executions/` and are delivered through Phase 1.4.7.2. The cross-record and lifecycle validators remain subsequent implementation work.

## 2. Scope

The validation architecture covers the ten canonical execution record files:

1. `execution.yml`
2. `work-items.yml`
3. `role-activations.yml`
4. `dependencies.yml`
5. `handoff-executions.yml`
6. `decisions.yml`
7. `evidence.yml`
8. `blockers.yml`
9. `replans.yml`
10. `closure.yml`

The corresponding execution records remain governed by their existing specifications under `docs/team/`.

## 3. Architectural Principles

### 3.1 Canonical governance remains authoritative

Validation schemas and scripts must implement the rules already established in the canonical governance documents.

They must not independently redefine role responsibilities, artifact ownership, workflow states, handoff acceptance, or closure authority.

When a conflict is discovered, the governance documents must be reviewed and reconciled before changing the validator.

### 3.2 Structural validation and relationship validation are separate

JSON Schema is responsible for validating the structure of individual YAML documents.

Python validation logic is responsible for checking relationships between records and enforcing rules that require information from multiple records.

Neither layer should duplicate the responsibilities of the other unnecessarily.

### 3.3 Validation is read-only

Validators must never silently:

- Create missing execution records.
- Generate record identifiers.
- Modify existing record values.
- Change lifecycle statuses.
- Accept or reject handoffs.
- Approve decisions.
- Mark evidence as verified.
- Close executions.

Validation reports findings. Authorized users remain responsible for correcting records and making governance decisions.

### 3.4 No fabricated data

Missing records must not be replaced with invented records or assumed completion states.

Optional, conditional, and not-applicable records must be handled according to their governing specifications.

### 3.5 Deterministic validation

Automated validation must produce consistent results for the same input records and validator version.

No paid model API calls or nondeterministic model judgments may be required for ordinary repository or CI validation.

## 4. Schema Architecture

### 4.1 Schema standard

Execution record schemas shall use JSON Schema Draft 2020-12.

Schema files shall use the `.schema.json` extension.

Each schema must declare its JSON Schema dialect and a stable schema identifier.

### 4.2 Schema location

Canonical execution schemas shall be stored under:

`schemas/executions/`

### 4.3 Schema coverage

The architecture shall provide one primary schema for each canonical execution record file:

| Schema | Record file |
|---|---|
| `execution.schema.json` | `execution.yml` |
| `work-items.schema.json` | `work-items.yml` |
| `role-activations.schema.json` | `role-activations.yml` |
| `dependencies.schema.json` | `dependencies.yml` |
| `handoff-executions.schema.json` | `handoff-executions.yml` |
| `decisions.schema.json` | `decisions.yml` |
| `evidence.schema.json` | `evidence.yml` |
| `blockers.schema.json` | `blockers.yml` |
| `replans.schema.json` | `replans.yml` |
| `closure.schema.json` | `closure.yml` |

### 4.4 Schema consistency

Schemas must reflect the actual canonical record structures.

They must not introduce undocumented wrapper objects, alternative field names, or new lifecycle states.

Common definitions should be reused when doing so improves consistency and maintainability.

Schema changes must be reviewed whenever their corresponding governance record specifications change.

### 4.5 Unknown properties

Canonical record objects should reject undocumented properties after their field definitions have been reconciled against the governance specifications.

Legitimate extensions require an explicit governance and schema update.

### 4.6 Canonical field conventions

The shared YAML wrappers, omission/null policy, timestamp format,
identifier conventions, role identifiers, reference rules, and history
boundaries are defined in:

`docs/team/execution-record-field-conventions.md`

The exact root execution fields are defined in
`docs/team/execution-identity-and-traceability.md`.

The exact role activation and work-item fields are defined in
`docs/team/role-activation-and-work-item-records.md`.

Workflow stage identifiers are defined in
`docs/team/workflow-lifecycle.md`.

The ten primary schemas and three shared definition schemas are
maintained under `schemas/executions/`. The schemas must follow these
field sources and must not invent aliases or wrapper structures.


## 5. Validation Layers

### 5.1 Layer 1 — Parsing and File Integrity

Responsibilities:

- Locate the execution directory.
- Confirm the execution root exists.
- Identify required and optional record files.
- Parse YAML safely.
- Reject duplicate YAML mapping keys.
- Reject malformed YAML.
- Reject unsupported document structures.
- Preserve source file and location information for reporting.

Parsing failures must prevent dependent validation from operating on incomplete or unreliable data.

### 5.2 Layer 2 — JSON Schema Validation

Responsibilities:

- Validate required fields.
- Validate data types.
- Validate object and array structures.
- Validate enumerated values.
- Validate identifier formats.
- Validate conditional field requirements.
- Reject unsupported properties where strict validation applies.

Each canonical record file must be checked against its corresponding schema.

### 5.3 Layer 3 — Cross-Record Consistency

Responsibilities:

- Verify record identifiers are unique within their defined scope.
- Verify referenced records exist.
- Verify records belong to the same execution when required.
- Verify canonical role and artifact references.
- Verify work-item and role-activation relationships.
- Verify dependency references.
- Verify handoff execution and submission references.
- Verify decision and evidence references.
- Verify blocker and replanning references.
- Verify closure references.
- Verify required bidirectional relationships where specified.

Cross-record checks must follow the canonical record specifications.

### 5.4 Layer 4 — Lifecycle and Governance Validation

Responsibilities:

- Verify allowed state transitions.
- Verify role activation and work assignment compatibility.
- Verify work-item dependency conditions.
- Verify handoff submission and acceptance consistency.
- Verify decision lifecycle consistency.
- Verify blocker resolution requirements.
- Verify replanning approval requirements.
- Verify evidence verification-state consistency.
- Verify completion, verification, and closure requirements.
- Verify release requirements when release is applicable.

A valid record structure does not automatically mean the execution is governance-compliant.

## 6. Validation Boundaries

### 6.1 Appropriate for automated validation

Automated validation may determine:

- Whether required fields exist.
- Whether values use permitted types and formats.
- Whether identifiers follow defined patterns.
- Whether references resolve.
- Whether referenced records belong to the correct execution.
- Whether a dependency graph contains a cycle.
- Whether a status transition is explicitly permitted.
- Whether mandatory closure references are present.
- Whether a record contradicts a deterministic governance rule.

### 6.2 Not appropriate for deterministic validation

Automated validation must not claim to determine:

- Whether a technical solution is architecturally sound.
- Whether a decision is strategically correct.
- Whether evidence is persuasive enough to prove a qualitative claim.
- Whether a security assessment is professionally adequate.
- Whether a handoff is genuinely useful to its consumer.
- Whether a person has sufficient expertise.
- Whether an exception is reasonable merely because it has been recorded.

These require authorized human review or a separately governed evaluation process.

## 7. Validation Findings

The validation system shall use three finding levels.

| Level | Meaning | Effect |
|---|---|---|
| `ERROR` | A structural failure or mandatory governance violation | Validation fails |
| `WARNING` | An incomplete or questionable condition requiring attention | Validation may pass with warnings |
| `INFO` | An observation that does not represent a violation | No effect on pass/fail |

Every finding should identify, where applicable:

- Finding code.
- Severity.
- Affected execution.
- Source file.
- Record identifier.
- Relevant field or relationship.
- Clear explanation.
- Recommended corrective action.

Finding codes must remain stable once introduced so tests and downstream reporting can depend on them.

## 8. Validation Execution

### 8.1 Single entry point

Execution validation shall be accessible through one primary command-line entry point.

The entry point coordinates the validation layers and produces a consolidated report.

Individual validation modules should remain independently testable.

### 8.2 Validation order

The prescribed execution order is:

1. Validate execution directory and file availability.
2. Parse YAML documents.
3. Validate individual record schemas.
4. Validate record identity and references.
5. Validate cross-record relationships.
6. Validate lifecycle and governance rules.
7. Produce the consolidated report.

A layer must not rely on data that an earlier layer failed to parse or validate safely.

### 8.3 Exit behavior

The validator shall return:

- Exit code `0` when no errors are found.
- Nonzero exit code when one or more errors are found.
- Nonzero exit code for execution failures that prevent reliable validation.

Warnings alone do not cause validation failure unless a later, explicitly governed policy says otherwise.

## 9. Testing Strategy

The validation system must be tested with both valid and invalid fixtures.

Tests must cover:

- Valid execution records.
- Missing required fields.
- Invalid field types.
- Invalid enumerated values.
- Malformed YAML.
- Duplicate YAML keys.
- Duplicate identifiers.
- Missing references.
- Cross-execution references.
- Invalid dependency relationships.
- Dependency cycles.
- Invalid lifecycle transitions.
- Invalid handoff relationships.
- Invalid closure references.
- Conditional and not-applicable records.
- Multiple independent validation findings.

Tests must verify both the finding and its severity.

A test must not pass merely because the validator exits with a nonzero code. It must confirm that the expected finding was produced.

## 10. Error Handling and Reporting

Validation must be resilient enough to report multiple independent problems in one run.

A failure in one record must not prevent validation of unrelated, safely parseable records.

However, dependent checks must be skipped when their required input is invalid or unavailable.

Skipped checks must not be reported as passed.

The report must distinguish:

- Passed checks.
- Failed checks.
- Warnings.
- Informational findings.
- Skipped checks.

The validator must never claim that an unexecuted check passed.

## 11. Maintainability and Change Control

Changes to canonical record specifications must trigger a review of:

1. Corresponding JSON Schemas.
2. Shared schema definitions.
3. Cross-record validation logic.
4. Lifecycle validation logic.
5. Test fixtures.
6. Validator documentation.

Schemas and validators are implementations of governance, not independent sources of authority.

When an inconsistency is discovered, the governance specification must be reconciled before implementation changes are accepted.

## 12. Implementation Roadmap

The architecture shall be implemented through these subphases:

| Subphase | Deliverable |
|---|---|
| 1.4.7.1 | Schema architecture and validation strategy |
| 1.4.7.2 | JSON Schemas for all canonical execution record types |
| 1.4.7.3 | Cross-record reference and consistency validator |
| 1.4.7.4 | Lifecycle and state-transition validator |
| 1.4.7.5 | Automated test fixtures and negative tests |
| 1.4.7.6 | Documentation, validator integration, and final verification |

No later subphase should be considered complete until its implementation and validation results have been reviewed.

## 13. Completion Criteria

### 13.1 Phase 1.4.7.1 — Architecture

Phase 1.4.7.1 is complete when:

- The validation architecture is documented.
- All ten canonical record files are accounted for.
- Schema and validator responsibilities are clearly separated.
- Validation boundaries are explicit.
- Error severity and exit behavior are defined.
- Testing requirements are established.
- The architecture does not contradict existing governance specifications.

### 13.2 Phase 1.4.7.2 — JSON Schemas

Phase 1.4.7.2 is complete when:

- One primary Draft 2020-12 JSON Schema exists for each of the ten canonical execution record files.
- Shared definitions cover canonical identifiers, timestamps, and common field values.
- Schema wrappers and field names match the canonical YAML record specifications.
- Required, optional, and conditional fields follow the shared omission/null policy.
- Controlled values and identifier formats match the governing documents.
- Local schema references resolve and schema files are valid JSON.
- No undocumented record fields or wrapper structures are introduced.
- Remaining cross-record and lifecycle rules are explicitly left to the later validator subphases.

The existence of a schema file alone does not establish that it has been exercised against real execution records. Schema meta-validation, representative fixtures, and end-to-end validator tests are addressed by the subsequent implementation and test subphases.