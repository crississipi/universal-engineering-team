# Delivery workflow

```mermaid
flowchart TD
  A[Request / issue] --> B[Product Analyst: outcome and acceptance]
  B --> C[Solution Architect: impact and design]
  C --> D[Lead assigns specialist owners]
  D --> E[Parallel bounded implementation]
  E --> F[Cross-role contract review]
  F --> G[QA + Security + performance/accessibility as relevant]
  G --> H{Acceptance and risk gates pass?}
  H -- No --> I[Anti-stuck protocol; options and experiment]
  I --> D
  H -- Yes --> J[Release Manager + SRE readiness]
  J --> K[Docs + Obsidian + Graphify + HTML report]
  K --> L[Lead verifies consistency and closes]
```

## Change packet
Each task has: ID, objective, acceptance criteria, owner, reviewers, affected components, interfaces, test plan, documentation targets, risk, status.

## Status vocabulary
`proposed → planned → in_progress → blocked → in_review → verified → released`
Use `deferred` or `cancelled` with a reason. Never mark `verified` based on assumptions.

## Handoff format
- **Outcome / status**
- **Changed surfaces**
- **Contracts and decisions**
- **Verification**
- **Documentation updated**
- **Risks / blockers / next owner**

The handoff format above describes the summary of an individual
handoff execution. It does not replace the reusable handoff contract.

Formal handoff contracts are defined in `docs/team/ownership.yml`
according to `docs/team/handoff-contract-schema.md`.

A handoff execution should reference the applicable contract ID
and version when a formal contract exists.

## Handoff acceptance process

An individual handoff execution follows this sequence:

1. Producer submits the required outputs and supporting context.
2. Consumer identifies the applicable contract ID and version.
3. Consumer evaluates each applicable acceptance check.
4. Consumer records an overall decision:
   `accepted`, `partially_accepted`, `rejected`, or `blocked`.
5. When corrections are required, the producer submits a revised
   output referencing the previous submission.
6. Consumer reassesses the affected checks and records the new decision.
7. Handoff closure is recorded only after outstanding required work
   has been resolved.

The detailed rules are documented in:

`docs/team/handoff-acceptance-rules.md`

A submitted file or message alone does not constitute acceptance.