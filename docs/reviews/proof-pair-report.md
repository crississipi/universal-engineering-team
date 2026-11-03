# Phase 2B — Backend Developer / QA Manager Proof-Pair Report

## Status

**Implementation status:** Drafted on `phase-2b/backend-qa-proof-pair`.

**Validation status:** Repository source review completed. Local automated validation and provider/agent execution have not yet been run for this phase. This report does not claim that the proof pair has passed those checks.

## Scope

This proof pair applies the seven-part role skill contract to:

- `backend-developer` — producer and accountable owner of `ART-BACKEND`.
- `qa-manager` — owner of `ART-QUALITY-EVIDENCE` and independent quality assessor.

No role, artifact, formal handoff contract, lifecycle state, or decision authority is added by this phase.

## Repository evidence reviewed

The role skills were prepared against the current `main` versions of:

- `docs/team/expected-roles.yml` — canonical 17-role inventory.
- `docs/team/ownership.yml` — `ART-BACKEND` and `ART-QUALITY-EVIDENCE` ownership; formal handoff list currently empty.
- `docs/team/producer-consumer-matrix.md` — required backend-to-quality evidence relationship and related conditional/feedback semantics.
- `docs/team/responsibility-boundaries.md` — Backend implementation accountability and QA quality strategy/verification accountability.
- `docs/team/role-activation-rules.md` — task-scoped required, conditional, optional, and not-activated participation.
- `docs/team/execution-protocol.md` — shared execution, verification, correction, escalation, and closeout rules.
- `docs/team/workflow-lifecycle.md` — workflow stages, overall workflow status, gates, and closure distinction.
- `docs/team/blockers-replanning-and-state-transitions.md` — canonical work-item states and blocker behavior.
- `docs/team/handoff-acceptance-rules.md` — formal handoff decisions and consumer acceptance authority.
- `docs/templates/SKILL.template.md` — seven-part role skill structure.

## Proof-pair contract

### Backend Developer

Backend owns backend implementation and correction, including server-side validation, authorization enforcement, backend tests, and operational behavior. It provides QA with the exact revision, relevant requirements/contracts, reproducible setup, test results, known limitations, and risk context.

Backend does not own QA's independent verification verdict, API contract governance, database schema governance, product acceptance criteria, or risk acceptance outside its authority.

### QA Manager

QA owns test strategy, acceptance traceability, defect triage, verification evidence, and the QA assessment. It evaluates observable requirements against a specific implementation revision, preserves failing evidence, and independently re-verifies corrections.

QA does not take over backend implementation or silently redefine product requirements. A formal handoff acceptance decision, if a contract is approved in the future, remains with the accountable owner of the consumer package. QA's verification verdict and a formal handoff decision are distinct concepts.

## Required proof scenarios

The following scenarios define the evidence to collect during validation. They are test cases, not claims that an agent run or automated test has already occurred.

| ID | Scenario | Expected behavior / evidence |
|---|---|---|
| PP-01 | Required backend output | Backend produces the implementation and test evidence needed for QA to verify the implemented backend scope. |
| PP-02 | Conditional dependency inactive | A conditional input whose trigger does not apply does not block the work; the activation decision is recorded where needed. |
| PP-03 | Conditional dependency active | When its documented trigger applies, the required input is activated and blocks only dependent work until sufficiently available. |
| PP-04 | Feedback finding | QA or a specialist may provide feedback; the receiving role assesses it. Feedback does not automatically block package completion unless an approved criterion, risk decision, or gate makes it mandatory. |
| PP-05 | Independent QA rejection | QA records a reproducible failed criterion with evidence; Backend cannot overwrite the finding or self-declare the criterion passed. |
| PP-06 | Backend correction | Backend corrects the implementation within its ownership boundary, identifies the changed revision and affected tests, and submits it for re-verification. |
| PP-07 | Re-verification | QA independently reruns affected checks against the corrected revision, records actual results, and preserves prior findings/results. |
| PP-08 | Three materially different attempts | Three materially different unsuccessful corrections to the same unresolved increment trigger escalation. Rerunning the same command or unchanged approach does not count as a new attempt. |
| PP-09 | Immediate escalation | Critical security, privacy, safety, data-integrity, production-stability, permission, or authorization blockers are escalated immediately rather than waiting for three attempts. |
| PP-10 | Work-item state integrity | Review/correction uses canonical work-item states such as `in_review`, `changes_requested`, and `blocked`; handoff decisions remain separate. |
| PP-11 | Formal handoff integrity | No formal handoff is invented from a matrix relationship. If a formal contract is approved later, the consumer package owner decides acceptance; the producer cannot self-approve. |
| PP-12 | Closeout honesty | Both roles report exact checks and actual results, explicitly identify unrun checks, and do not claim completion/verification from implementation statements alone. |

## Lifecycle and state alignment

The skills use existing canonical terms:

- Workflow stages: `execution`, `integration_and_review`, `verification`, and other identifiers from `workflow-lifecycle.md`.
- Work-item states: `not_started`, `ready`, `in_progress`, `blocked`, `in_review`, `changes_requested`, `completed`, and `cancelled`, subject to the documented transition table.
- Handoff decisions: `accepted`, `partially_accepted`, `rejected`, and `blocked`.
- Acceptance-check results: `passed`, `failed`, `not_applicable`, and `not_verified`.

These vocabularies describe separate dimensions and must not be interchanged. The Closure stage does not itself close an execution; the canonical closure record governs formal closure.

## Formal handoff limitation

The current `docs/team/ownership.yml` contains no approved formal handoff contracts. The proof pair therefore demonstrates the package-level producer-to-verifier relationship and independent review behavior, but does not claim a formal contract submission/acceptance workflow is active. Creating a formal handoff requires a separate reviewed governance change.

## Validation record

### Completed in this phase

- Inspected the current governance sources listed above.
- Rewrote both role skills using the repository's seven-part template.
- Preserved the canonical role IDs and package ownership.
- Added explicit producer/verifier boundaries and independent correction/re-verification behavior.
- Aligned work-item, handoff-decision, and acceptance-check vocabulary to existing governance.
- Added this report with explicit proof scenarios and evidence requirements.

### Not yet performed

- Local unit tests and repository validators on this branch.
- Manifest/role-index/skill-policy validation of the revised skill files.
- A controlled agent execution of PP-01 through PP-12.
- A measured multi-run evaluation or provider compatibility test.

No test pass, agent run, acceptance decision, or provider compatibility result is claimed here.

## Phase gate

Phase 2B should be considered complete only after:

1. The user runs the repository validation suite on this branch and reports the actual output.
2. Any validator failures or policy/link issues are corrected.
3. The proof scenarios are exercised in a controlled run or explicitly retained as unexecuted evaluation cases with a documented reason.
4. The revised skills are reviewed for preservation of role-specific expertise and responsibility boundaries.

Do not begin rewriting the remaining 15 role skills until this proof-pair gate is reviewed and accepted.

## Final Controlled Run Outcome — 2026-11-03

### Backend–QA correction cycle

The final controlled run demonstrated the following sequence:

1. Backend submitted an implementation and supporting tests.
2. QA independently identified a Decimal overflow defect.
3. Backend corrected the Decimal precision and exponent handling.
4. QA re-verified the correction and identified an additional oversized-integer quantity defect.
5. Backend replaced integer-to-string digit counting with a `bit_length()`-based upper-bound calculation.
6. Independent QA re-verified the final implementation.

### Final verification evidence

- Backend test suite: 12 passed.
- QA test suite: 10 passed.
- Independent 5,001-digit quantity regression: passed.
- Additional Decimal, rounding, boolean rejection, and large-quantity probes: passed.
- Supplied SHA-256 fingerprints: matched the uploaded archive.

### Outcome

**The oversized-quantity defect is resolved.**

The Backend–QA proof pair successfully demonstrated independent defect identification, implementation-owner correction, and independent re-verification.

### Evidence limitations and deferred scenarios

The controlled run does not establish that the deliberately injected boolean defect was present during the initial QA review.

The following scenarios remain unverified or require separate evidence:

- Conditional dependency activation and acceptance.
- Feedback-only relationships and closure behavior.
- Three materially different correction attempts.
- Immediate escalation for critical infrastructure, permission, or authorization blockers.

No formal handoff contracts currently exist in `docs/team/ownership.yml`. This controlled run therefore demonstrates a package-level producer–verifier relationship, not formal handoff-contract execution.

**Phase 2B assessment:** The Backend–QA proof-pair correction cycle has passed. Overall Phase 2B acceptance remains subject to the remaining review and deferred scenarios.