# Cross-Record Reference and Consistency Validation

## 1. Purpose

This document defines deterministic checks across the ten canonical execution
record files. It supplements the record-specific specifications and
`execution-validation-architecture.md`.

The validator is read-only. It reports missing, dangling, duplicated, or
inconsistent references. It does not create records, repair references,
infer missing relationships, approve decisions, or change execution state.

## 2. Implementation

The Phase 1.4.7.3 implementation is:

`scripts/validate-execution-references.py`

Run it from the repository root:

```powershell
python scripts/validate-execution-references.py "executions/EXE-<uuid>"
```

The supplied directory must be a direct child of `executions/`. It must
contain the ten canonical YAML files and their documented top-level wrappers.
Collection files must contain arrays, including empty arrays when no records
exist. The execution and closure files must contain one mapping each.

The validator uses the existing `validation_common.py` helpers and PyYAML.
It remains independently runnable for focused development. It does not perform
JSON Schema validation or lifecycle transition validation. Use
`scripts/validate-execution.py` for the complete validation sequence.

## 3. Identity and Record Scope

The validator checks:

- The root `execution_id` is present and matches the execution directory name.
- Every child record's `execution_id` matches the root execution.
- Record IDs are present and unique within each record collection.
- Every root `record_refs` entry resolves to a record in the same execution.
- The optional root `closure_id`, when present, resolves to the canonical
  closure record.
- Canonical role-valued fields resolve to one of the role slugs in
  `docs/team/expected-roles.yml`.
- Artifact package references resolve to `docs/team/ownership.yml`.

The validator does not claim repository-wide uniqueness for project, change,
or execution identifiers when only one execution directory is supplied.

## 4. Role Activation and Work-Item References

The validator checks:

- Every work item's `activation_id` resolves to a role activation in the
  same execution.
- The activation's `role_id` matches the work item's `assigned_role`.
- Work items in execution states that establish active work
  (`in_progress`, `in_review`, or `changes_requested`) reference an
  active activation. A blocked item is not assumed to have started work.
- Not-started or ready work items may reference planned or active activations.
- Completed work items may reference active, completed, or deactivated
  activations.
- Cancelled work items may reference a planned, active, completed,
  deactivated, or not-activated activation.
- A role does not have multiple simultaneously active activation records.
- Work-item IDs listed by an activation resolve and point back to that
  activation when the optional list is supplied.

Optional activation `work_item_ids` lists are not treated as exhaustive.
The validator does not require every work item to be duplicated in that
optional index.

## 5. Dependency References and Graph

The validator checks:

- Predecessor and successor work items exist in the same execution.
- A dependency does not use the same work item as both endpoints.
- Work-item dependency references resolve and identify a dependency involving
  that work item.
- Dependency evidence, decision, blocker, and handoff references resolve.
- Handoff dependency references resolve.
- The predecessor-successor graph is acyclic.

A dependency-to-handoff relationship is not assumed to require a reciprocal
reference in every case. The record specifications make bidirectional
traceability conditional on the relationship. The validator resolves
references that are recorded but does not invent that condition.

## 6. Handoff References

The validator checks:

- Producer and consumer work items exist.
- The producer work item's assigned role matches `from_role`.
- The consumer work item's assigned role matches `to_role`.
- Producer and consumer artifact IDs resolve when present.
- A declared reusable handoff contract resolves when the contract registry
  contains contracts.
- The reusable contract is active and its applicable producer, consumer,
  and artifact fields match the execution instance.
- Submission IDs are present and unique across the execution's handoff
  records.
- Submission decision IDs and current decision IDs resolve to canonical
  `handoff_acceptance` decisions.
- Output and context reference objects resolve according to their declared
  reference type.
- `current_submission_id` identifies a submission in the same handoff and,
  when submissions exist, identifies the latest submission.
- A recorded current decision outcome agrees with the terminal current
  handoff status (`accepted`, `partially_accepted`, `rejected`, or
  `blocked`).

If handoff execution records exist while the reusable contract registry is
empty, contract-level consistency is reported as a warning, not silently
treated as verified.

## 7. Decision, Evidence, Blocker, and Replan References

The validator checks references recorded in canonical fields, including:

- Decision evidence, affected-record, supersession, and related-decision
  references.
- Evidence related-record and supersession references.
- Blocker work-item, dependency, handoff, decision, and evidence references.
- Replan work-item, dependency, role-activation, handoff, blocker, artifact,
  evidence, decision, and change-target references.
- Work-item input and output reference objects.

Internal record references must resolve within the current execution.
Artifact IDs must resolve in the artifact catalog. Explicit external
references remain external and are not incorrectly required to resolve as
execution records.

Approved, in-progress, and completed replans must identify an approved
authorizing decision. A decision reference on a proposed or under-review
replan is resolved but is not assumed to be an approval.

Decision and evidence supersession chains must not contain cycles.

## 8. Closure References

The validator checks:

- All canonical record references in `required_record_refs` resolve.
- Release references remain external to the ten canonical execution record
  files and are not incorrectly resolved as internal record IDs.
- Completion and verification work-item lists resolve.
- Every work item in the closure's in-scope work-item index appears in
  exactly one completion classification.
- Completion classifications agree with canonical work-item states:
  completed items are completed, cancelled items are cancelled, and
  outstanding items use a non-terminal work-item state.
- Completion classifications do not overlap.
- A `complete` conclusion has no outstanding work items.
- A `complete_with_exceptions` or `passed_with_exceptions` conclusion has
  at least one approved exception with an approved decision.
- A `passed` verification conclusion has no failed or not-verified work
  items.
- Verification classifications do not overlap.
- Completion and verification evidence references resolve.
- Closure-check and exception references to records and evidence resolve.
- Exception acceptance decisions resolve and are approved.
- The closure decision, when recorded, resolves to an
  `execution_closure` decision.
- A closed execution references an approved closure decision.

The validator does not determine whether evidence is persuasive, whether
verification is professionally adequate, or whether an exception is
substantively acceptable. Those conclusions remain with the authorized
reviewers.

## 9. Findings and Exit Behavior

Findings use stable `REF###` codes and are reported through the existing
shared validation reporter.

- Exit code `0`: no cross-record errors were found. Warnings may still be
  reported.
- Exit code `1`: one or more cross-record errors were found.
- Exit code `2`: the invocation or execution directory prevents reliable
  validation.

A pass from this script means only that the implemented cross-record checks
passed for the supplied directory. It does not mean JSON Schema, lifecycle,
semantic, security, or human review passed.

## 10. Explicit Non-Goals

This validator does not:

- Validate every field against JSON Schema.
- Validate all lifecycle transitions or historical chronology.
- Prove that a role has substantive expertise.
- Judge the quality of decisions or evidence.
- Infer missing optional references.
- Require reciprocal references where the governing specification makes
  them conditional.
- Validate repository-wide uniqueness from a single execution directory.
- Mutate YAML files or governance documents.

These responsibilities remain assigned to the schema, lifecycle, test,
integration, and human-review layers in Phase 1.4.7.
