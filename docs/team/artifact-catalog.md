
# Engineering Team Artifact Catalog

## Purpose

This catalog defines the authoritative artifact packages owned by the
Universal Engineering Team's 17 specialist roles.

The canonical machine-readable source is:

`docs/team/ownership.yml`

This document explains the ownership model, package structure,
classification, lifecycle, and maintenance rules.

## 1. Ownership model

The team uses single accountable ownership.

Every artifact package must have:

- One accountable owner.
- One primary producer.
- Zero or more eligible contributors.
- A defined purpose.
- A list of expected deliverables.
- A classification.
- A lifecycle status.
- Repository paths when those paths have been approved.

The accountable owner and primary producer must be the same role
under the current ownership model.

Contributors can provide information, implementation, consultation,
or review. Their participation does not transfer accountability.

No artifact may have multiple accountable owners.

## 2. Package-level granularity

The catalog uses package-level granularity.

An artifact package groups related deliverables that share:

- A common engineering responsibility.
- A single accountable owner.
- A coherent purpose.
- Related consumers or downstream uses.

For example, the API and Event Contract Package can contain:

- OpenAPI specifications.
- AsyncAPI specifications.
- Request and response schemas.
- Error conventions.
- Authentication requirements.
- Compatibility notes.

These components do not each require a separate ownership record.

An individual component may receive its own artifact ID later if
independent ownership, versioning, approval, or handoff tracking becomes
necessary.

Do not create separate artifact IDs merely because a package contains
multiple files.

## 3. Ownership fields

### id

A stable, unique identifier for the package.

Example: `ART-API-CONTRACT`

IDs should not change when filenames or repository locations change.

### name

The human-readable package name.

### owner

The single role accountable for the package's correctness,
completeness, and maintenance.

### primary_producer

The role responsible for producing and updating the package.

For this ownership model, it must match `owner`.

### contributors

Roles that may contribute when relevant to the task.

Contributor participation is conditional. Listing a role does not mean
it must be activated for every project or change.

### classification

Allowed values:

- `internal`: Primarily supports internal coordination or team operation.
- `shared`: Intended to be consumed by multiple roles.
- `external_input`: An input originating outside the engineering team.
- `terminal_output`: A final deliverable intended for an external recipient.

An artifact's classification does not change its accountable owner.

### status

Allowed values:

- `proposed`: Defined but not formally activated.
- `active`: Approved for use and governed by this catalog.
- `deprecated`: Retained for historical reference but no longer the
  preferred package.

### purpose

A concise statement explaining why the package exists.

### deliverables

The expected contents of the package.

These describe package scope, not necessarily separate artifact records.

### paths

Approved repository-relative paths associated with the package.

Use an empty list until the storage location has been agreed and
verified.

Never invent paths to satisfy validation.

## 4. Ownership rules

1. Every package has exactly one accountable owner.
2. The owner is also the primary producer.
3. Contributors do not become co-owners.
4. The owner remains accountable when work is delegated.
5. A package may be consumed by many roles without changing ownership.
6. A handoff transfers a defined output, not ownership of the source package.
7. Changes to ownership require an explicit review and manifest update.
8. Ownership must not be inferred solely from role names or informal
   collaboration descriptions.

## 5. Artifact lifecycle

### Proposed

The package has been identified and its initial ownership assigned.

It may not yet have an approved storage location, acceptance criteria,
or downstream handoff contracts.

### Active

The package has been reviewed and approved for operational use.

Before activation, confirm:

- Owner and primary producer.
- Package purpose and deliverables.
- Contributor boundaries.
- Storage location.
- Required quality or acceptance expectations.
- Known consumers.

### Deprecated

The package is no longer the preferred source of truth.

Its replacement or migration path should be documented when applicable.

Do not delete historical records merely because a package is deprecated.

## 6. Relationship to handoffs

Artifact ownership and handoff contracts are separate concerns.

The artifact catalog establishes:

- Who owns the source package.
- Who produces it.
- Who may contribute.
- What the package contains.

The producer-consumer matrix identifies candidate package relationships.

The formal handoff contract catalog establishes:

- Which producer role supplies an output.
- Which consumer role receives it.
- Which producer and consumer packages are involved.
- What specific outputs must be transferred.
- What context must accompany the outputs.
- What checks the consumer uses to assess the submission.

The canonical handoff definitions are maintained in:

`docs/team/ownership.yml`

Their required structure is documented in:

`docs/team/handoff-contract-schema.md`

Do not infer formal handoffs from contributor lists or role names.

A producer-consumer relationship must be reviewed and approved before
it becomes an active handoff contract.

A handoff transfers defined outputs, not ownership of the source package.

Acceptance, rejection, resubmission, and escalation procedures are
defined separately from the contract schema.

## 7. Relationship to the Delivery Lead

The Delivery Lead coordinates:

- Work breakdown.
- Role activation.
- Task assignment.
- Dependency order.
- Blocker escalation.
- Delivery closure.

The Delivery Lead does not replace the accountable owner of
a specialist artifact package.

Specialist owners remain responsible for the technical correctness
and completeness of their outputs.

## 8. Maintenance

Update `docs/team/ownership.yml` first.

Then update this document only when its explanatory rules or
catalog structure change.

Run:

`python scripts/validate-artifacts.py`

before submitting changes.

Ownership changes should include a concise rationale in the relevant
pull request or architecture decision record.
