
## Artifact Package Ownership

The engineering team uses a single accountable owner model with
package-level artifact granularity.

Each of the 17 specialist roles is accountable for one primary
artifact package. The accountable owner is also the primary producer.

Other roles may contribute to a package when their expertise is
relevant. Contributor participation does not transfer accountability
or create shared ownership.

The canonical artifact records are maintained in:

`docs/team/ownership.yml`

The detailed package definitions and lifecycle rules are documented in:

`docs/team/artifact-catalog.md`

### Ownership rules

1. Each package has one accountable owner.
2. The accountable owner and primary producer must match.
3. Contributors provide support without becoming co-owners.
4. Artifact consumers do not automatically become contributors.
5. Handoffs transfer defined deliverables, not permanent ownership.
6. The Delivery Lead coordinates work but does not replace specialist
   accountability.
7. Artifact records remain proposed until their ownership and scope
   have been reviewed.

### Package-level granularity

Related deliverables are grouped into a package when they share
the same owner and engineering responsibility.

For example, API schemas, examples, authentication requirements,
and compatibility notes belong to the API and Event Contract Package.

Individual components may receive separate artifact IDs in the
future when independent tracking or approval is necessary.

See `docs/team/artifact-catalog.md` for the full catalog rules.


## Responsibility Boundaries

The responsibility boundaries and decision authority of all 17 roles
are documented in:

`docs/team/responsibility-boundaries.md`

This document supplements the individual specialist skills and
artifact ownership catalog.

It defines:

- Primary accountability for each role.
- Decision authority within each engineering domain.
- Explicit boundaries between overlapping roles.
- Cross-role decision rules.
- Escalation procedures.

Responsibility boundaries do not create additional artifact owners
or transfer ownership between roles.

Escalation and conflict-resolution procedures are documented in:

`docs/team/handoff-escalation-rules.md`

The canonical artifact ownership source remains:

`docs/team/ownership.yml`

Formal producer-consumer handoffs are defined separately and must not
be inferred from contributor lists or collaboration descriptions.
