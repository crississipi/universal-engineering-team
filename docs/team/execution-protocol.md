# Shared Execution Protocol

## Purpose and authority

This document defines the shared execution sequence used by the Universal Engineering Team. It is a concise operating protocol, not a replacement for role expertise or the canonical governance documents.

The structured collaboration index is `skills/manifest.yml`. It is a derived view only. Its source-of-truth documents are declared in that manifest; do not resolve conflicts by treating the manifest as authoritative.

Use this protocol with:
- `AGENTS.md` for repository-wide instructions.
- `docs/team/expected-roles.yml` for canonical role IDs.
- `docs/team/ownership.yml` for artifact ownership and approved formal handoff contracts.
- `docs/team/producer-consumer-matrix.md` for candidate package relationships.
- `docs/team/role-activation-rules.md` for role activation.
- `docs/team/workflow-lifecycle.md` and `docs/team/blockers-replanning-and-state-transitions.md` for workflow and work-item states.
- `docs/team/handoff-contract-schema.md`, `docs/team/handoff-acceptance-rules.md`, and `docs/team/handoff-escalation-rules.md` for formal handoff governance.
- `docs/team/execution-record-model.md` and its referenced specifications for execution records.

## 1. Intake and task framing

Before work begins, establish the available facts:
- Objective and intended outcome.
- Scope and explicit exclusions.
- Acceptance criteria and observable evidence.
- Constraints, assumptions, risks, and unresolved decisions.
- Relevant repository paths, interfaces, systems, and data.
- Accountable owner and coordinating lead.

Use a proportionate change packet. Do not invent missing requirements, approvals, stack details, or evidence; record unknowns and ask only for decisions that materially block safe progress.

## 2. Select and activate roles

1. Identify the affected artifact packages and their accountable owners in `docs/team/ownership.yml`.
2. Select only roles whose responsibilities, decision authority, required inputs, or specialist verification apply.
3. Apply the activation classifications and triggers in `docs/team/role-activation-rules.md`. Required participation must not be silently omitted; conditional activation must record whether its trigger applies.
4. Load only the selected role skills from `ROLE-INDEX.md` or `SKILLS-RESOLVER.md`.
5. Assign one accountable owner to each work item. Role activation and work assignment do not transfer artifact ownership.

## 3. Map collaboration and dependencies

Use the producer-consumer matrix as package-level guidance:
- `required_input`: the dependent work cannot be finalized until the needed accepted input is available; unrelated work may continue.
- `conditional_input`: activate only when its documented condition applies.
- `feedback`: findings or recommendations may cause reassessment or rework, but do not automatically block the receiving package from starting or completing.

A relationship is not automatically a blocking dependency or a formal handoff. Record actual execution dependencies in the canonical execution records. Keep the dependency graph acyclic; feedback paths may be cyclic.

Create a formal handoff only when an approved contract exists under `handoffs` in `docs/team/ownership.yml`. A candidate matrix relationship does not itself authorize a formal handoff. A `proposed` contract is not an active delivery requirement.

## 4. Plan bounded work

For each work item, identify:
- Unique work-item reference and objective.
- One assigned role and accountable package owner.
- Required inputs and activated conditions.
- Files, interfaces, and boundaries owned.
- Acceptance criteria and verification method.
- Dependencies, risks, and parallel work that is safe to continue.
- Documentation and knowledge artifacts affected.

Coordinate shared-file edits before parallel execution. Specialists retain authority over their own domains; the Delivery Lead coordinates cross-role delivery but does not replace specialist decisions.

## 5. Execute and verify

- Inspect existing implementation, conventions, tests, and documentation before changing files.
- Make the smallest coherent change within the assigned ownership boundary.
- Preserve contracts, data integrity, security, privacy, accessibility, and operational constraints.
- Add or update proportionate tests and evidence.
- Run targeted checks first, then relevant regression checks.
- Report exact commands and actual results. Distinguish passed, failed, blocked, and not-run checks.
- Do not claim completion or verification from an implementation statement, an unrun test, or the existence of an artifact alone.

## 6. Submit and accept formal handoffs

For an approved formal contract:
1. The producer submits immutable output references, revision context, and required evidence.
2. The consumer evaluates the submission against the contract version and its observable acceptance checks.
3. The consumer records the canonical decision; the producer must not self-approve.
4. Use only the governed decisions: `accepted`, `partially_accepted`, `rejected`, or `blocked`.
5. A required check that is `not_verified` prevents full acceptance. Partial acceptance is allowed only for independently usable, safe portions.
6. A rejected or partially accepted submission returns the affected work to correction and re-verification. Preserve prior submissions and decisions; never overwrite history.
7. Feedback does not block by default. It becomes a completion or release condition only when an approved requirement, risk decision, or acceptance criterion makes it one.

The consumer package owner is accountable for the acceptance decision. The Delivery Lead coordinates delivery impact and escalation but cannot override specialist acceptance findings.

## 7. Correct, unblock, and escalate

- Correct the specific unresolved increment identified by evidence; do not repeat an unchanged failed approach.
- Count a correction attempt only when it is a materially different correction to the same unresolved increment, not when a command is merely rerun.
- After three materially different unsuccessful correction attempts on that increment, escalate with the evidence, attempts, impact, and smallest decision needed.
- Escalate critical security, privacy, safety, data-integrity, production-stability, permission, or authorization blockers immediately; do not wait for the correction-attempt threshold.
- Block only the work and progression gates that actually depend on the unresolved condition. Continue safe independent work.
- Use only lifecycle states defined by the applicable canonical record specification. Workflow status, work-item state, dependency status, handoff decision, and blocker status are separate dimensions.

## 8. Closeout

Before closing assigned work, report:
- Outcome and acceptance criteria addressed.
- Changed files and artifact references.
- Verification commands, actual results, and unrun checks.
- Handoff decisions and unresolved dependencies, if applicable.
- Risks, blockers, assumptions, and follow-up owner/action.
- Applicable documentation, diagrams, Obsidian, Graphify, and central report updates, or why they are not applicable.

Execution completion, verification, and formal closure are distinct. Follow the canonical closure record and authority rules; never infer closure from completed work items alone.
