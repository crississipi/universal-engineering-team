# Handoff Contract Schema

## Purpose

This document defines the standard structure for formal producer-to-consumer
handoff contracts in the Universal Engineering Team.

The canonical handoff contract records are maintained in:

`docs/team/ownership.yml`

This document defines the contract schema. It does not create or approve
individual handoffs.

The producer-consumer relationships that may become formal handoffs are
documented in:

`docs/team/producer-consumer-matrix.md`

Only reviewed and approved relationships may be added to the canonical
handoff manifest.

## 1. Contract principles

1. Every formal handoff connects one producing role to one consuming role.
2. Every handoff references a declared producer artifact package and a
   declared consumer artifact package.
3. The producing role must be the accountable owner and primary producer
   of the producer package.
4. The consuming role must be the accountable owner of the consumer package.
5. A handoff transfers defined outputs, not artifact ownership.
6. A producer remains accountable for the correctness and completeness
   of its source package.
7. A consumer remains accountable for its own package and decisions.
8. A contributor relationship does not automatically establish a handoff.
9. A producer-consumer matrix relationship does not become a formal
   handoff until it has been reviewed and approved.
10. A contract must define outputs and acceptance checks precisely enough
    for the consumer to assess the submission without guessing.

## 2. Canonical contract structure

Each entry under `handoffs` in `docs/team/ownership.yml` represents
a reusable handoff contract definition.

The contract does not represent an individual transfer execution.

### Required fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable, unique handoff contract identifier. |
| `contract_version` | string | Version of the contract definition. |
| `from_role` | string | Canonical role responsible for producing the handoff. |
| `to_role` | string | Canonical role responsible for receiving the handoff. |
| `artifact_id` | string | ID of the producer's source artifact package. |
| `consumer_artifact_id` | string | ID of the consumer's artifact package. |
| `relationship_type` | string | `required_input`, `conditional_input`, or `feedback`. |
| `purpose` | string | Why the consumer needs the handoff. |
| `required_outputs` | list of strings | Specific outputs the producer must provide. |
| `required_context` | list of strings | Supporting information needed to interpret and use the outputs. |
| `acceptance_checks` | list of strings | Observable checks the consumer uses to assess the submission. |
| `status` | string | Contract lifecycle state: `proposed`, `active`, or `deprecated`. |

### Conditional field

| Field | Type | Description |
|---|---|---|
| `activation_condition` | string | Explains when the contract applies. Required for `conditional_input`; may also clarify other relationship types. |

## 3. Field rules

### `id`

Use a stable identifier with this format:

`HOF-<PRODUCER>-<CONSUMER>-<SEQUENCE>`

Example:

`HOF-API-BACKEND-001`

The identifier must remain stable when wording, outputs, or repository
locations change.

Do not reuse an identifier for a different producer-consumer relationship.

### `contract_version`

Use a quoted version string, initially `1.0`.

Increment the version when a change materially affects the contract's
required outputs, context, or acceptance checks.

A version change does not require a new contract ID unless the relationship
itself has materially changed.

### `from_role` and `to_role`

Both values must use canonical role IDs from:

`docs/team/expected-roles.yml`

The source role must own the producer artifact package.

The receiving role must own the consumer artifact package.

A handoff must not assign accountability to a contributor merely because
that contributor helped produce the output.

The same role cannot be both the producer and consumer of one handoff.

### `artifact_id`

References the producer artifact package in `ownership.yml`.

The package must exist, and its owner and primary producer must match
`from_role`.

### `consumer_artifact_id`

References the consumer artifact package in `ownership.yml`.

The package must exist, and its owner must match `to_role`.

This field makes the package-to-package relationship explicit rather
than relying on role names alone.

### `relationship_type`

Allowed values:

- `required_input`: The consumer needs the output before completing
  the work that depends on it.
- `conditional_input`: The handoff applies only when a defined project
  condition or scope trigger exists.
- `feedback`: The output communicates findings, recommendations, or
  verification results that may require the receiving package to change.

The value must agree with the reviewed producer-consumer matrix.

### `purpose`

State the specific reason the consumer needs the output.

Avoid generic descriptions such as "for collaboration" or "for development."

### `activation_condition`

For `conditional_input`, state the condition that activates the handoff.

Do not use vague conditions such as "when necessary" or "if applicable"
without explaining what makes the condition applicable.

For `required_input` and `feedback`, this field may be omitted when
the relationship is unconditional within its approved scope.

### `required_outputs`

List concrete deliverables or information that the producer must provide.

Each entry should be independently understandable and verifiable.

Avoid vague entries such as:

- Relevant files.
- Complete documentation.
- Necessary information.
- All required details.

Prefer specific outputs such as:

- Approved OpenAPI specification for the affected endpoints.
- Request and response schemas with representative examples.
- Documented authentication and authorization requirements.
- Error response definitions for the supported failure cases.

Only include outputs within the producer package's responsibility.

### `required_context`

List the context needed to interpret and safely consume the outputs.

Depending on the relationship, this may include:

- Relevant requirement or task identifiers.
- Scope and assumptions.
- Applicable environment or version.
- Referenced architecture or design decisions.
- Known limitations or unresolved questions.
- Links or references to supporting evidence.

Do not include credentials, access tokens, passwords, private keys,
or other secrets in a handoff.

### `acceptance_checks`

List observable checks the receiving role can perform.

Checks must assess whether the submitted outputs are usable for the
declared purpose.

Prefer checks that can be answered with evidence, such as:

- Required schema files are present and parse successfully.
- All affected endpoints have request and response definitions.
- Referenced requirements and decisions are identifiable.
- Documented error behavior covers the agreed failure cases.

Do not use subjective checks such as "looks good" or "is complete"
without defining what completeness means.

The evaluation, rejection, partial acceptance, and resubmission
procedures are defined in:

`docs/team/handoff-acceptance-rules.md`

### `status`

Allowed values:

- `proposed`: Defined but not approved for operational use.
- `active`: Reviewed and approved for use.
- `deprecated`: Retained for reference but no longer the preferred contract.

New contracts must begin as `proposed`.

A proposed contract must not be treated as an active delivery requirement.

## 4. Illustrative YAML example

The following example illustrates the schema only. It is not an approved
handoff and must not be copied into the canonical manifest as an active
contract without relationship review.

```yaml
handoffs:
  - id: HOF-API-BACKEND-001
    contract_version: "1.0"
    from_role: api-manager
    to_role: backend-developer
    artifact_id: ART-API-CONTRACT
    consumer_artifact_id: ART-BACKEND
    relationship_type: conditional_input
    purpose: >
      Provide the approved API contract required to implement
      the affected backend endpoints.
    activation_condition: >
      The project includes backend implementation of an API or
      event interface governed by the API contract package.
    required_outputs:
      - Approved API specification for affected endpoints.
      - Request and response schemas with representative examples.
      - Authentication and authorization requirements.
      - Error response and compatibility definitions.
    required_context:
      - Relevant requirement or task identifiers.
      - Applicable API version.
      - Referenced architecture decisions.
      - Known limitations and unresolved contract questions.
    acceptance_checks:
      - Required API specification is present and parses successfully.
      - Affected endpoints have request and response definitions.
      - Authentication and error behavior are documented.
      - Referenced requirements and architecture decisions are identifiable.
    status: proposed
```

## 5. Contract versus execution record

A contract defines what must be transferred whenever an approved
relationship is activated.

An execution record documents one actual transfer using that contract.

Execution records may later capture:

- Handoff contract ID and contract version.
- Project, task, or change identifier.
- Producer submission reference.
- Submission timestamp.
- Consumer decision.
- Acceptance or rejection evidence.
- Requested corrections and resubmission references.
- Escalation status and resolution.

Execution records are not stored as additional contract definitions
in `ownership.yml`. Their storage and lifecycle will be defined
separately if required.

## 6. Storage and references

The canonical contract definitions belong in:

`docs/team/ownership.yml`

The schema and field definitions belong in this document.

The producer-consumer matrix remains the source for reviewing
candidate relationships.

Do not invent repository paths, external storage locations, delivery
channels, or evidence URLs. These must be agreed before a contract
depends on them.

Use repository-relative references where possible once the relevant
storage conventions have been approved.

## 7. Relationship to later handoff rules

This schema does not define:

- Response deadlines.
- Escalation time limits.
- Resubmission limits.
- Conflict-resolution authority beyond existing role boundaries.
- Timeout behavior.
- Deadlock resolution.

Acceptance, rejection, and resubmission procedures are defined in:

`docs/team/handoff-acceptance-rules.md`

The remaining escalation and conflict-resolution rules are addressed
in Phase 1.2.5.

## 8. Validation expectations

The handoff validator should eventually verify:

1. Handoff IDs are unique and correctly formatted.
2. Contract versions are non-empty version strings.
3. Producer and consumer roles are valid and different.
4. Producer and consumer artifact IDs exist.
5. Producer and consumer roles match their respective package ownership.
6. Relationship types use the approved vocabulary.
7. Conditional relationships declare an activation condition.
8. Purpose is non-empty.
9. Required outputs, required context, and acceptance checks follow
   their defined list rules.
10. Contract status uses the approved lifecycle vocabulary.
11. Contract relationships agree with the reviewed producer-consumer matrix.

Validator implementation and enforcement are handled in the
validation workstream, after the schema and subsequent handoff rules
have been reviewed.

## 9. Maintenance

Update the schema before changing the canonical contract structure.

When changing an existing contract:

1. Confirm the producer-consumer relationship remains valid.
2. Confirm the package owners and responsibilities remain unchanged
   or document the approved change.
3. Update the contract version when required.
4. Review affected consumers.
5. Update the canonical manifest and related documentation together.
6. Run all applicable repository validators.

Never silently change a contract in a way that alters what a consumer
is expected to receive or accept.

## 10. Relationship to acceptance rules

The schema defines what the producer must submit and what the consumer
must check.

The acceptance rules define how the consumer evaluates an individual
submission.

Every execution should preserve the distinction between:

- Contract requirements.
- Individual acceptance-check results.
- Overall handoff decisions.
- Rejection reasons and correction requests.
- Resubmission revisions.

Do not add execution decisions or rejection records as fields in
the reusable contract definition.

See:

`docs/team/handoff-acceptance-rules.md`