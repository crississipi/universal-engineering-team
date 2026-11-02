# Project, Change, and Execution Identity and Traceability

## 1. Purpose

This document defines the canonical identity model for projects, changes, and execution instances within the Universal Engineering Team.

It establishes how execution records are uniquely identified, how they relate to one another, and how work can be traced across projects, changes, role activations, work items, dependencies, handoffs, decisions, evidence, blockers, replanning, and closure.

This document supplements `execution-record-model.md`. It does not replace existing artifact ownership, responsibility boundaries, workflow governance, or handoff contracts.

## 2. Governing Principles

1. Every project, change, and execution must have a stable identifier.
2. Identifiers must remain unchanged throughout the lifetime of the entity.
3. Identifiers must not depend on mutable titles, descriptions, branch names, or directory names.
4. A project may contain multiple changes.
5. A change may have multiple execution instances.
6. Each execution instance must have its own execution directory.
7. Execution records must identify their parent project and change.
8. Child records must be traceable to their execution.
9. External identifiers may supplement internal identifiers but must not silently replace them.
10. Historical records must not be rewritten merely because project names, change descriptions, or external references change.
11. An identifier must never be reassigned to a different entity.
12. No project, change, or execution record may be fabricated to make the repository appear complete.

## 3. Identity Hierarchy

The canonical hierarchy is:

```text
Project
+-- Change
    +-- Execution 1
    |   +-- Work items
    |   +-- Role activations
    |   +-- Dependencies
    |   +-- Handoff executions
    |   +-- Decisions
    |   +-- Evidence
    |   +-- Blockers
    |   +-- Replans
    |   +-- Closure
    |
    +-- Execution 2
        +-- ...
```

### 3.1 Project

A project represents a broader product, system, initiative, or engineering effort.

A project:

- Has one stable project identifier.
- May contain multiple changes.
- May span multiple repositories when explicitly documented.
- May continue across multiple execution instances.
- Is not equivalent to a single development task or execution.

### 3.2 Change

A change represents a bounded unit of work within a project.

Examples include:

- A new feature.
- A defect correction.
- A security remediation.
- A performance improvement.
- A technical migration.
- A documentation or operational improvement.

A change:

- Has one stable change identifier.
- Belongs to exactly one project.
- May have multiple execution instances.
- Must have a sufficiently clear scope to distinguish it from other changes.
- Must not be created solely to represent an individual role's work item.

### 3.3 Execution

An execution represents one actual coordinated attempt to perform work for a change.

An execution:

- Has one globally unique execution identifier.
- Belongs to exactly one project and one change.
- Has its own execution record directory.
- Contains the records for the work performed during that execution.
- Must not be confused with a workflow stage, work item, role activation, or handoff.

A new execution identifier is appropriate when a distinct execution instance is intentionally started. Resuming work within the same execution does not automatically require a new execution identifier.

## 4. Identifier Format and Generation

Use the following identifier prefixes:

| Entity | Prefix | Format |
|---|---|---|
| Project | `PRJ` | `PRJ-<UUID>` |
| Change | `CHG` | `CHG-<UUID>` |
| Execution | `EXE` | `EXE-<UUID>` |

`<UUID>` is a newly generated UUID in lowercase canonical format, including hyphens.

Examples below are illustrative only:

```text
PRJ-8f3b2c1a-7d4e-4a91-9b62-0a1c2d3e4f50
CHG-2a7c9e10-5b3d-4f81-8c62-1d2e3f4a5b60
EXE-6c1d8e20-9a4b-4f73-8d51-2e3f4a5b6c70
```

Generate UUIDs using a trusted UUID generator. In PowerShell:

```powershell
"PRJ-$((New-Guid).Guid.ToLower())"
"CHG-$((New-Guid).Guid.ToLower())"
"EXE-$((New-Guid).Guid.ToLower())"
```

Generate each identifier once and retain it. Do not generate a replacement merely because an entity is renamed, moved, resumed, or assigned a different external reference.

Identifiers must be unique within the engineering team's governed record space. Before registering an identifier, check that it has not already been assigned.

## 5. Required Identity Relationships

The root `execution.yml` record must identify:

- `project_id`
- `change_id`
- `execution_id`

### 5.1 Canonical Execution Record Fields

The root file uses one top-level `execution` mapping containing the
following canonical fields.

| Field | Requirement | Definition |
|---|---|---|
| `project_id` | Required | Stable parent project identifier. |
| `change_id` | Required | Stable parent change identifier. |
| `execution_id` | Required | Stable execution identifier; must match the directory name. |
| `title` | Required | Short human-readable execution title. |
| `description` | Required | Brief explanation of the execution context. |
| `intended_outcome` | Required | Observable outcome the execution is intended to achieve. |
| `scope` | Required | Scope object defined below. |
| `workflow_stage` | Required | Current workflow stage identifier. |
| `workflow_status` | Required | Current overall workflow status. |
| `coordination` | Required | Coordination object defined below. |
| `record_refs` | Required | Index of supporting record identifiers. |
| `created_at` | Required | UTC timestamp when the execution record was created. |
| `updated_at` | Required | UTC timestamp of the latest material update. |
| `history` | Required | Chronological history of material root-record changes. |
| `external_references` | Optional | References to external systems or records. |
| `source_control` | Optional | Source-control traceability information when applicable. |
| `final_disposition` | Conditional | Final overall disposition when the execution reaches a terminal workflow outcome. |

#### Scope object

The required `scope` object contains:

- `in_scope`: array of strings describing included work.
- `out_of_scope`: array of strings describing explicit exclusions.
- `constraints`: array of strings describing known constraints.

Each array may be empty when no entries are known or applicable. Empty arrays must not be used to conceal unresolved scope questions.

#### Workflow stage identifiers

The `workflow_stage` field uses these stable identifiers, corresponding
to the stage names in `workflow-lifecycle.md`:

- `intake`
- `qualification`
- `solution_framing`
- `planning`
- `execution`
- `integration_and_review`
- `verification`
- `release_readiness_and_release`
- `closure`

The `workflow_status` field uses only the canonical overall workflow
statuses defined in `workflow-lifecycle.md`:

- `proposed`
- `planned`
- `in_progress`
- `blocked`
- `in_review`
- `verified`
- `released`
- `deferred`
- `cancelled`

Workflow stage and workflow status are independent fields and must
not be substituted for one another.

#### Coordination object

The required `coordination` object contains:

- `coordinator_role`: canonical role identifier responsible for coordinating this execution.
- `coordination_notes`: optional explanatory text.

The coordinator coordinates execution-level work. This field does not
grant artifact ownership, specialist approval authority, or universal
decision authority. The Delivery Lead is not automatically the
coordinator for every execution.

#### Supporting record reference index

The required `record_refs` object contains arrays for:

- `work_item_ids`
- `activation_ids`
- `dependency_ids`
- `handoff_execution_ids`
- `decision_ids`
- `evidence_ids`
- `blocker_ids`
- `replan_ids`

It may contain `closure_id` when the canonical closure record exists.
Arrays must be present even when empty. The index is a navigation and
traceability aid; the supporting files remain authoritative for their
record contents. Validators must check that indexed identifiers resolve
and that the index does not claim nonexistent records.

#### History entries

Each root history entry contains:

- `changed_at`: UTC timestamp.
- `changed_by_role`: canonical role identifier.
- `change_type`: concise description of the change.
- `reason`: explanation for the change.
- `previous_values`: optional object containing prior values.
- `new_values`: optional object containing resulting values.
- `related_record_ids`: optional array of related canonical IDs.

History entries must be chronological. The initial entry records
creation. History is an audit of material changes, not a substitute
for the current field values.

#### Final disposition

When present, `final_disposition` is an object containing:

- `status`: one of `verified`, `released`, `deferred`, or `cancelled`.
- `summary`: concise explanation of the disposition.
- `recorded_at`: UTC timestamp.

Its status must agree with the terminal overall workflow status at the
time the disposition is recorded. The canonical closure record remains
authoritative for formal execution closure and closure authorization.

#### Optional external and source-control references

Each `external_references` entry contains:

- `provider`: external system or provider name.
- `reference_type`: type of external resource.
- `relationship`: how the resource relates to the execution.
- At least one of `identifier` or `uri`.

The optional `source_control` object may contain `repository`,
`branch`, `base_commit`, `commit_refs`, `pull_request_refs`, and
`resulting_commit`. Values must be recorded only when known; no
placeholder hashes or inferred references are permitted.

### 5.2 YAML Document Shape

The root file must use this wrapper:

```yaml
execution:
  project_id: "PRJ-<UUID>"
  change_id: "CHG-<UUID>"
  execution_id: "EXE-<UUID>"
```

The example is a structural excerpt, not a complete valid execution
record. All required fields defined in this section must be present
in an actual record.

Every supporting record must explicitly identify its `execution_id`.
Project and change context is inherited from the root execution record
and must not conflict with it.

The following relationships are mandatory:

| Record | Required identity relationship |
|---|---|
| Execution | Project, change, and execution IDs |
| Work item | Execution ID; project and change context inherited from its execution |
| Role activation | Execution ID; project and change context inherited from its execution |
| Dependency | Execution ID; referenced work-item identities |
| Handoff execution | Execution ID; handoff contract ID and producer/consumer context |
| Decision | Execution ID |
| Evidence | Execution ID |
| Blocker | Execution ID |
| Replan | Execution ID |
| Closure | Execution ID |

Child records must not introduce conflicting project or change identities.

Where a child record needs to reference another execution, it must use
the exact execution identifier rather than relying on a title or
directory name.

## 6. Execution Directory Convention

The execution directory remains:

```text
executions/
+-- <execution-id>/
    +-- execution.yml
    +-- work-items.yml
    +-- role-activations.yml
    +-- dependencies.yml
    +-- handoff-executions.yml
    +-- decisions.yml
    +-- evidence.yml
    +-- blockers.yml
    +-- replans.yml
    +-- closure.yml
```

The directory name must exactly match the `execution_id` in `execution.yml`.

Project and change IDs are recorded in `execution.yml`; they do not need to be repeated in directory names.

Multiple execution directories may reference the same project and change IDs.

## 7. External References

An execution may be associated with external systems, including:

- Issue trackers.
- Project management systems.
- Source-control repositories.
- Pull requests and merge requests.
- CI/CD runs.
- Deployment systems.
- External change requests.

External references are supplementary traceability information.

When recorded, an external reference should identify:

- The external system or provider.
- The reference type.
- The external identifier or URL.
- Its relationship to the project, change, or execution.

External references must not contain credentials, access tokens, private keys, or other secrets.

An external ticket number or pull request number must not be treated as the internal project, change, or execution identifier.

## 8. Source-Control Traceability

When source control is relevant, execution records should capture available references to:

- Repository.
- Branch.
- Base commit.
- Relevant commit(s).
- Pull request or merge request.
- Resulting commit or merge commit.

These fields are optional when the execution does not use source control or the information is not yet available.

Do not invent commit hashes, branch names, pull request numbers, or repository references.

If a value changes during execution, preserve the relevant history according to the execution record model.

## 9. Renaming and Scope Changes

Project and change identifiers remain stable when names or descriptions change.

A change that materially expands beyond its original scope must be reviewed to determine whether it remains the same change or should be separated into a distinct change.

Do not silently reuse an existing change identifier for unrelated work.

When a new change is created:

- Assign a new change identifier.
- Associate it with the correct project.
- Preserve references to related changes where relevant.
- Keep previous execution records intact.

A new execution may be created for a new coordinated attempt without changing the parent project or change identifiers.

## 10. Cross-Execution Traceability

When work depends on another execution, record an explicit reference to the source execution and the relevant artifact, decision, or evidence.

Cross-execution references must identify:

- Source execution ID.
- Referenced record or artifact ID, where available.
- Purpose of the reference.
- Relevant version, commit, or timestamp when necessary.

Do not copy historical records into a new execution and present them as newly produced evidence.

Previously produced outputs may be reused only when their origin and applicability are clear.

## 11. Identity Integrity

The following conditions must be treated as identity-integrity violations:

- Duplicate project, change, or execution IDs.
- An execution associated with more than one project or change.
- A change associated with more than one project.
- An execution directory that does not match its execution ID.
- A child record referencing a nonexistent execution.
- A child record associated with a conflicting execution.
- An identifier reassigned to a different entity.
- An external identifier incorrectly substituted for an internal identifier.

These conditions should be detected through validation where practical.

Validation must not automatically invent, replace, or repair identifiers. Ambiguous or conflicting identity relationships must be reported for human resolution.

## 12. Relationship to Future Schemas and Validators

This document defines the identity and traceability policy.

The exact YAML field schemas, reference-integrity checks, uniqueness checks, directory checks, and automated test coverage will be implemented in Phase 1.4.7.

Until then, records must follow this policy manually and must not be represented as schema-validated.

## 13. Maintenance

Changes to the identity model must preserve existing identifiers and historical references.

Any future changes to identifier formats or relationship rules must define migration and backward-compatibility requirements before implementation.

The execution record model and this document must remain consistent.