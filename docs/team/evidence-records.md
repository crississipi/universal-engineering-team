# Evidence Records

## 1. Purpose

Evidence records preserve verifiable information supporting execution claims, work-item completion, acceptance checks, dependency satisfaction, decisions, and execution closure.

Evidence must allow an authorized reviewer to determine:

- What was demonstrated or verified.
- Which source supports the claim.
- Who produced or captured the evidence.
- When the evidence was captured.
- Whether it was independently verified.
- Which execution records depend on it.

An assertion without a verifiable source reference must not be treated as sufficient evidence.

Evidence records do not independently authorize work completion, handoff acceptance, dependency satisfaction, release, or closure. The applicable acceptance and approval authority remains responsible for those determinations.

## 2. Canonical Location

**File:** `evidence.yml`

**Location:** `executions/<execution-id>/evidence.yml`

Each record belongs to exactly one execution.

## 3. Evidence Identifier

Evidence identifiers must use:

`EVD-<UUID>`

Each evidence identifier must be unique across the repository.

An existing evidence identifier must never be reassigned to another evidence item.

## 4. Canonical Evidence Record

Each evidence record must contain the following fields:

| Field | Required | Description |
|---|---|---|
| `evidence_id` | Yes | Unique evidence identifier |
| `execution_id` | Yes | Parent execution identifier |
| `evidence_type` | Yes | Controlled evidence classification |
| `title` | Yes | Short descriptive title |
| `description` | Yes | What the evidence demonstrates |
| `source_type` | Yes | Origin of the evidence |
| `source_ref` | Yes | Specific location or reference to the source |
| `produced_by_role` | Conditional | Role responsible for producing the evidence |
| `verified_by_role` | Conditional | Role responsible for verification |
| `verification_status` | Yes | Current verification state |
| `verification_notes` | Conditional | Explanation of verification or invalidation |
| `related_record_refs` | Optional | Related execution record identifiers |
| `captured_at` | Yes | When the evidence was captured |
| `created_at` | Yes | Record creation timestamp |
| `updated_at` | Yes | Last material update timestamp |
| `supersedes_evidence_id` | Optional | Previous evidence record replaced by this record |
| `history` | Yes | Material change history |

Conditional fields must be populated when their applicable state requires them.

Optional fields must be omitted when they do not apply. Do not invent placeholder references.

## 5. Evidence Types

Use the following controlled vocabulary:

| Type | Description |
|---|---|
| `test_result` | Unit, integration, end-to-end, or other test results |
| `build_result` | Build, compilation, or packaging results |
| `security_result` | Security assessment, vulnerability scan, or penetration-test results |
| `performance_result` | Benchmark, load-test, or profiling results |
| `accessibility_result` | Accessibility assessment or test results |
| `review_record` | Code, design, architecture, or formal review records |
| `approval_record` | Authorized approval or sign-off evidence |
| `implementation_artifact` | Source code, configuration, migration, or implementation artifact |
| `operational_record` | Deployment, monitoring, incident, or operational evidence |
| `documentation` | Technical documentation or knowledge artifact |
| `external_reference` | External system record or authoritative external document |
| `other` | Evidence that does not fit another approved category |

The `other` classification requires a meaningful description.

New evidence types must be introduced through governance review rather than created arbitrarily for individual records.

## 6. Source Types

Use the following controlled vocabulary:

- `execution_artifact`
- `repository_reference`
- `tool_output`
- `external_system`
- `document`
- `human_observation`
- `other`

The `source_ref` must identify a specific source that an authorized reviewer can locate or inspect.

Examples include:

- Repository path and commit identifier.
- Test report reference.
- Build output reference.
- External issue or transaction identifier.
- Document reference.
- Approved evidence storage location.

Do not store passwords, access tokens, private keys, credentials, or unnecessary sensitive information in evidence records.

A source reference must not be presented as proof that the source was inspected unless inspection actually occurred.

## 7. Verification Status

Use the following statuses:

| Status | Description |
|---|---|
| `unverified` | Evidence has been recorded but has not been verified |
| `verified` | Evidence has been checked and found valid for its stated purpose |
| `invalid` | Evidence is inaccurate, corrupted, unsupported, or otherwise unusable |
| `superseded` | A newer evidence record has replaced this record for the applicable purpose |

### 7.1 Verification Requirements

Evidence verification must establish that:

- The referenced source exists or is accessible.
- The source corresponds to the stated description.
- The evidence is relevant to the claim it supports.
- The evidence has sufficient integrity for its intended use.
- Any applicable limitations are documented.

The verifier must be an appropriately authorized role.

A producer must not automatically be treated as an independent verifier.

A `verified` status does not automatically approve the work, decision, handoff, or release supported by that evidence.

### 7.2 Verification Notes

`verification_notes` must explain material verification findings.

For `verified`, notes should explain what was checked.

For `invalid`, notes must explain why the evidence cannot be relied upon.

For `unverified`, verification notes may be omitted until an actual verification attempt occurs.

For `superseded`, the replacement evidence must be identified through `supersedes_evidence_id` on the newer record.

## 8. Evidence Integrity and Supersession

Evidence records must preserve historical traceability.

The following rules apply:

1. Every evidence item receives its own stable identifier.
2. Captured evidence references must not be silently replaced.
3. Corrections or replacements require a new evidence record.
4. A new record must reference the previous record through `supersedes_evidence_id` when it replaces that record.
5. The earlier record must remain available.
6. The earlier record's verification history must be preserved.
7. Invalid evidence must not be deleted merely because it failed verification.
8. Supersession must not imply that the previous evidence was invalid unless that was actually established.
9. Material changes must be recorded in `history`.

An evidence record marked `superseded` must identify a valid replacement record.

A replacement record must not supersede itself.

## 9. Related Record References

Evidence may support other execution records.

Use `related_record_refs` to reference applicable canonical record identifiers.

Possible references include:

- Work items: `WI-<UUID>`
- Decisions: `DEC-<UUID>`
- Dependencies: `DEP-<UUID>`
- Handoff executions: `HEX-<UUID>`
- Blockers: `BLK-<UUID>`
- Re-planning records: `RPL-<UUID>`

Artifact package references use the canonical artifact identifiers
defined in `docs/team/ownership.yml`. Artifact package identifiers
are not execution record identifiers and are not required to belong
to the execution-specific record collections.

Validation must resolve artifact package references against the
canonical ownership catalog rather than treating them as
execution-scoped records.

All referenced records must belong to the same execution.

Evidence records must not duplicate the full content of the records they support.

The record containing the claim or decision remains responsible for its own status and acceptance determination.

## 10. History Requirements

The `history` collection preserves material changes to the evidence record.

Each history entry must support:

| Field | Required | Description |
|---|---|---|
| `changed_at` | Yes | Timestamp of the change |
| `changed_by_role` | Yes | Role responsible for the change |
| `change_type` | Yes | Classification of the change |
| `reason` | Yes | Explanation for the change |
| `previous_status` | Conditional | Previous verification status |
| `new_status` | Conditional | New verification status |
| `changed_fields` | Optional | Other materially changed fields |

History must preserve:

- Record creation.
- Verification.
- Invalidation.
- Supersession.
- Material corrections.
- Changes to related references.

Historical information must not be erased to make the current record appear valid.

## 11. Illustrative YAML Structure

The following example is illustrative only. It is not an actual execution record.

```yaml
evidence:
  - evidence_id: "EVD-<UUID>"
    execution_id: "EXE-<UUID>"

    evidence_type: "test_result"
    title: "Backend integration test results"

    description: >
      Integration tests executed against the backend API
      to verify the required response behavior.

    source_type: "repository_reference"
    source_ref: "tests/reports/backend-integration-results.xml"

    produced_by_role: "qa-manager"
    verified_by_role: "qa-manager"

    verification_status: "verified"

    verification_notes: >
      The referenced report was inspected and its
      results were confirmed for the stated test scope.

    related_record_refs:
      - "WI-<UUID>"
      - "ART-QUALITY-EVIDENCE"

    captured_at: "2026-11-02T10:00:00Z"
    created_at: "2026-11-02T10:05:00Z"
    updated_at: "2026-11-02T10:05:00Z"

    history:
      - changed_at: "2026-11-02T10:05:00Z"
        changed_by_role: "qa-manager"
        change_type: "created"
        reason: "Evidence record created."
```

The identifiers and source path above are placeholders. Actual records must use real identifiers and verifiable sources.

## 12. Validation Requirements

The future evidence validator must enforce:

1. Evidence identifiers are unique.
2. Evidence identifiers follow `EVD-<UUID>`.
3. Every evidence record references an existing execution.
4. Evidence types use the approved vocabulary.
5. Source types use the approved vocabulary.
6. Required fields are present.
7. Conditional fields are present when required by the verification state.
8. Referenced roles are valid for the execution.
9. Related record references resolve to existing records.
10. Related records belong to the same execution.
11. Verification statuses use the approved vocabulary.
12. A verified record identifies an authorized verifier.
13. Invalid evidence includes a meaningful verification explanation.
14. Superseded evidence references a valid replacement.
15. Supersession relationships are consistent and do not form cycles.
16. Historical changes preserve the previous and new verification states.
17. A source reference is not automatically treated as proof of inspection.
18. Evidence records do not independently authorize acceptance or completion.
19. Historical records are not silently overwritten or deleted.

## 13. Relationship to Other Execution Records

Evidence records provide supporting information to other canonical execution records.

- Work items may reference evidence supporting completion.
- Decisions may reference evidence supporting authorization.
- Dependencies may reference evidence supporting satisfaction.
- Handoff submissions may reference evidence supporting acceptance checks.
- Blockers may reference evidence supporting their identification or resolution.
- Re-planning records may reference evidence supporting the need for change.
- Closure records may reference evidence supporting final verification.

Evidence references must use canonical IDs.

Evidence verification must not replace the acceptance, approval, or closure responsibilities defined by the applicable governance documents.

## 14. Implementation Boundary

This specification defines the evidence record structure and governance requirements.

It does not introduce:

- Automated evidence collection.
- Automatic verification of evidence.
- A separate evidence approval authority.
- A replacement for work-item acceptance.
- A replacement for handoff acceptance.
- A replacement for dependency evaluation.
- A replacement for execution closure.

Schemas and automated validation are deferred to Phase 1.4.7.

## 15. Acceptance Criteria

- Evidence identifiers and execution ownership are explicit.
- Evidence types and source types use controlled vocabularies.
- Evidence provenance is traceable.
- Verification status and accountability are defined.
- Supersession preserves historical records.
- Related execution records use canonical references.
- Sensitive credentials and secrets are excluded.
- Evidence does not independently authorize acceptance or completion.
- History requirements are explicit.
- Validation requirements are documented.
- Examples are clearly illustrative.
