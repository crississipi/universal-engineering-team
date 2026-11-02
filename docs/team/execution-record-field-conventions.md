# Execution Record Field Conventions

## 1. Purpose

This document establishes shared serialization and field conventions for
the ten canonical execution record files.

It supplements the individual record specifications. It does not replace
their field definitions, lifecycle rules, authority boundaries, or
cross-record governance.

If a record-specific specification defines a more specific field shape,
that specification remains authoritative. Any conflict must be reconciled
before schemas or validators are changed.

## 2. Canonical YAML Document Wrappers

Each execution directory contains the following YAML documents:

| File | Required top-level key | Value |
|---|---|---|
| `execution.yml` | `execution` | One mapping |
| `work-items.yml` | `work_items` | Array of work-item mappings |
| `role-activations.yml` | `role_activations` | Array of role-activation mappings |
| `dependencies.yml` | `dependencies` | Array of dependency mappings |
| `handoff-executions.yml` | `handoff_executions` | Array of handoff-execution mappings |
| `decisions.yml` | `decisions` | Array of decision mappings |
| `evidence.yml` | `evidence` | Array of evidence mappings |
| `blockers.yml` | `blockers` | Array of blocker mappings |
| `replans.yml` | `replans` | Array of re-planning mappings |
| `closure.yml` | `closure` | One mapping |

Collection wrappers must be present even when the collection is empty.
A missing collection file is not equivalent to an empty collection.
The root and closure files must contain their single required mapping.

No additional top-level keys are permitted unless a future governance
change explicitly introduces them.

## 3. Omission, Null, and Empty-Collection Policy

1. Required fields must be present and contain a value of the documented
   type.
2. Optional fields must be omitted when they do not apply or are not known.
3. Conditional fields must be present only when their documented
   condition applies; otherwise they must be omitted.
4. The YAML null value is not a valid substitute for an omitted optional
   or conditional field.
5. Required arrays must be present. They may be empty only when the
   record-specific specification permits an empty collection.
6. A required array must not be populated with placeholders, fabricated
   references, or empty strings to satisfy validation.
7. An empty array means that no entries are currently recorded. It does
   not mean that an unresolved requirement has been satisfied.
8. Required strings must not be blank or whitespace-only unless a
   record-specific specification explicitly permits an empty string.

The closure-record example currently contains null placeholders for
conditional fields. Those placeholders are illustrative legacy notation;
actual records and schemas must follow this document's omission policy.

## 4. Identifiers

Canonical identifiers use the prefixes and entity-specific formats
defined by their governing record specifications:

| Entity | Prefix |
|---|---|
| Project | `PRJ` |
| Change | `CHG` |
| Execution | `EXE` |
| Role activation | `ACT` |
| Work item | `WI` |
| Dependency | `DEP` |
| Handoff execution | `HEX` |
| Handoff submission | `SUB` |
| Decision | `DEC` |
| Evidence | `EVD` |
| Blocker | `BLK` |
| Replan | `RPL` |
| Closure | `CLS` |

UUID suffixes use lowercase canonical UUID format with hyphens.
Schemas validate identifier syntax. Validators enforce uniqueness and
reference resolution at the appropriate repository or execution scope.

Other identifiers such as closure-check IDs, exception IDs, and history
event IDs follow the specific stable-identifier rules in their record
specification. They must not be incorrectly validated as UUID-prefixed
record IDs.

## 5. Timestamps

Timestamp fields use RFC 3339 date-time strings normalized to UTC and
ending in `Z`, for example:

```text
2026-11-02T12:30:00Z
```

Timestamps must include seconds and must not be timezone-naive.
Schemas validate the date-time format. Cross-field validators check
chronology and lifecycle consistency where required.

A timestamp records an actual event. Do not invent timestamps for events
that have not occurred.

## 6. Canonical Role Identifiers

Role-valued fields use the canonical role slugs from
`docs/team/expected-roles.yml`.

Do not use display names, titles, email addresses, usernames, or
free-form role labels in fields that require a role identifier.

A syntactically valid string is not sufficient: validators must confirm
that the role exists in the canonical role manifest.

## 7. Record Histories

Every record type that requires `history` must provide it as an array.
The record-specific specification determines the exact history-entry
shape.

History structures are intentionally not forced into one universal
schema. Existing record specifications use different field names and
event details appropriate to their lifecycle. A schema must preserve
those documented differences rather than silently rename fields.

Across all record types:

- History entries must be chronological where the specification
  requires chronology.
- Material changes must be traceable to an actor or responsible role.
- Reasons must be recorded where required.
- Current fields remain the authoritative current state.
- Historical entries must not be silently overwritten or deleted.
- History must not fabricate events or imply an unperformed action.

## 8. References

References must use canonical identifiers for internal records and
artifact packages. External resources must use the explicitly documented
external-reference structures.

A reference must not be replaced with a title, role display name, path,
or URL when a canonical identifier is required.

JSON Schema validates local shape and identifier syntax. The Python
cross-record validator resolves references, checks execution boundaries,
and enforces bidirectional relationships where the governing
specification requires them.

A reference to a release record is an external/governed reference; the
release record is not one of the ten canonical execution YAML files and
must not be required to resolve as one of those ten record types.

## 9. Collection and Uniqueness Rules

- Each collection wrapper contains mappings of one record type only.
- Record IDs must be unique within the scope defined by that record's
  specification.
- Submission IDs must be unique within their governed execution scope.
- References between records must remain within the same execution
  unless an explicit cross-execution reference is defined.
- Empty collection files are valid when no records of that type exist.
- Duplicate records must not be used to represent history; material
  changes belong in the record's history or append-only submission list.

## 10. Schema and Validator Boundaries

JSON Schema Draft 2020-12 is responsible for:

- Required properties and data types.
- Enumerated values.
- Identifier and timestamp syntax.
- Nested object and array structure.
- Conditional field presence based on fields within one document.
- Rejection of undocumented properties.

Deterministic Python validation is responsible for:

- Uniqueness across records and files.
- Reference existence and execution boundaries.
- Role-manifest membership.
- Directory and root execution identity consistency.
- Bidirectional references.
- Dependency graph acyclicity.
- Lifecycle transitions requiring historical comparison.
- Authority and consistency rules requiring multiple records.
- Chronology and cross-record lifecycle consistency.

Schemas and validators must remain read-only. They report invalid
records and must not create, repair, infer, or approve execution data.

## 11. Maintenance

Any change to these conventions must be reconciled with all ten
record specifications and the schema-validation architecture before
implementation.

A field rename or wrapper change requires an explicit migration plan
for existing records. Validators must not silently accept undocumented
aliases as a migration mechanism.
