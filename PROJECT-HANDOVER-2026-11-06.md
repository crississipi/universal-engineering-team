# Current-state addendum — repository health pass

> This addendum supersedes conflicting status statements in the historical handover below. It is based on the repository state audited at main commit `f7d30d8f7fd868f7154fa08cfce1a36362ecf5ff` on 2026-11-06. Update this addendum when the stabilization PR and baseline-design work are merged or materially changed.

## Verified current state

- PR #33 was merged to `main` as `39b2f9d725fc0fb805d855669ec8738f4b4ae809`. Its 14 role-specific requirement anchors are now part of the canonical skills. Merge does not equal semantic approval.
- Stage B remains in baseline design/preparation. There are 17 planned role scenarios, 10 independent runs per scenario, 170 planned executions, 0 approved baseline scenarios, 0 baseline executions, and 0 baseline post-run reviews.
- The separate pilot remains complete: 3 scenarios, 9 pilot run records, and 3 post-run reviews. Pilot results are not baseline evidence.
- PR #10 merged blocker lifecycle alignment. Canonical blocker records, lifecycle guidance, and JSON Schema now share eight statuses: `open`, `in_progress`, `blocked`, `escalated`, `deferred`, `resolved`, `closed`, and `cancelled`. Historical Phase 2B reports are being amended to distinguish the resolved vocabulary issue from still-unverified live persistence/routing.
- `docs/team/ownership.yml` still declares artifact packages as proposed and has no formal handoff contracts. Do not claim formal producer/consumer handoff execution.
- The baseline run-record schema/validator, cohort checks, and report generator remain unimplemented. Do not start the 170-run cohort until scenario design, human approvals, evidence tooling, and configuration pinning are complete.
- CI runs #97, #98, and #99 were failures. The GitHub connector exposed the failed job but not usable step logs, so the precise historical failure cause is not established by this audit.

## Stabilization work in progress

Branch: `chore/stage-b-repository-health`.

The branch adds:
- finite-positive criterion weight validation and a 100-point total check;
- regression tests for incorrect totals and non-finite weights;
- a role requirement-anchor validator checking one anchor per canonical skill, global uniqueness, placement in Identity and boundaries, an adjacent requirement statement, and exact mapping to the baseline register;
- unit tests for the traceability validator;
- a CI step invoking the new validator;
- baseline and Phase 2B documentation corrections.

The generated `ALL-ROLE-SKILLS.md` must be regenerated from canonical skill files and checked before this stabilization can be called complete. No baseline scenarios have been authored or approved in this pass. Human review of anchor meaning remains outstanding.

## Required local verification before merge

Run from the repository root in PowerShell:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build-all-role-skills.py --write
python scripts/build-all-role-skills.py --check
python scripts/validate-execution.py --check-schemas
python scripts/validate-skills.py
python scripts/validate-requirements.py
python scripts/validate-manifest.py
python scripts/validate-artifacts.py
python scripts/validate-handoffs.py
python scripts/validate-scenarios.py
python scripts/build-agents-section.py --check
git diff --check
```

Do not report a command as passed unless its output has been inspected. If the generated consolidated skill file changes, include that generated output in the PR.


## Baseline scenario design update — 2026-11-08

Branch `chore/stage-b-repository-health` now contains one draft scenario YAML file for every canonical role under `tests/scenarios/SCEN-BASELINE-<ROLE>.yml`. Each file is marked `status: draft`, uses `review_record: null`, contains five criteria totaling 100 points, maps every criterion to the role's requirement anchor, and pins the associated canonical skill revision in its evidence entry.

An author-side structural preflight is recorded at `docs/evaluation/baseline/DESIGN-PREFLIGHT-2026-11-08.md`. It is not an independent design review and does not approve scenario content. Independent review records remain 0/17; human scenario approvals remain 0/17; baseline executions remain 0/170. The preflight flags the legacy Backend Developer, Penetration Tester, and Delivery Lead requirement wording for explicit semantic review.

The next gate is independent design review and role-anchor semantic review. Do not begin baseline runs or create run-record/evidence files until explicit human pre-run approvals and dedicated baseline validation/reporting tools exist. The branch's 17 draft files have not yet been validated by a local run of `scripts/validate-scenarios.py`; rerun the full local validation suite after pulling the latest branch.

## Next sequence after stabilization

1. Complete generated-file synchronization and obtain a green full CI run.
2. Record semantic review of all 17 requirement anchors, including the original three.
3. Design 17 distinct baseline scenarios with criteria totaling 100 and evidence guidance.
4. Conduct independent scenario design review and record findings.
5. Obtain explicit human pre-run approval for each scenario.
6. Implement and test dedicated baseline run-record validation, evidence integrity checks, cohort comparability checks, and reporting.
7. Pin repository/scenario/skill revisions, prompt bytes/hash, provider/model/version, mode, settings, and tools.
8. Only then perform 10 fresh independent runs per approved scenario and complete human post-run reviews.

---

# Universal Engineering Team — Complete Project Handover

> **Repository:** https://github.com/crississipi/universal-engineering-team  
> **Handover date:** 2026-11-06  
> **Purpose:** Preserve the system's history, architecture, governance, implementation state, evaluation evidence, validation workflow, unfinished work, and continuation rules for future ChatGPT sessions and human contributors.

---

## 1. Executive summary

The Universal Engineering Team repository has evolved from a collection of role-specific AI engineering skills into a governed, provider-neutral, multi-agent engineering system.

Its purpose is to make AI engineering roles collaborate through explicit responsibilities, artifact ownership, validated handoffs, evidence-based execution, and independently assessed evaluation scenarios.

### Current system state

- 17 canonical engineering roles: 16 specialist roles and one Delivery Lead.
- Standardized seven-part role skill contracts.
- Centralized `skills/manifest.yml`.
- Canonical role inventory, artifact ownership, producer-consumer relationships, and handoff governance.
- Shared execution, acceptance, blocker, escalation, and lifecycle rules.
- Automated structural validators, unit tests, generated-file consistency checks, and token-size reporting.
- A completed three-scenario pilot: 9 executions, all three formal reviews passed.
- A repository-wide baseline evaluation framework targeting 17 scenarios × 10 runs = 170 executions.
- Baseline execution has **not** started. The nine pilot executions must remain separate from the baseline cohort.

### Immediate status at handover

- PR #32, **Establish repository-wide baseline evaluation framework**, has been merged into `main`.
- PR #33, **Add role requirement anchors for baseline traceability**, is open on branch `baseline/role-requirement-anchors`.
- PR #33 adds draft requirement anchors to 14 role skills that previously lacked them. These are not yet approved and the branch has not completed the full local validation sequence.
- The next action is to validate PR #33, review the 14 requirement anchors against the role skills and governance, then merge only after validation and human review.

---

## 2. Canonical role inventory

The canonical role list is `docs/team/expected-roles.yml`. Do not invent, rename, or casually reorder role IDs.

1. `product-analyst`
2. `solution-architect`
3. `api-manager`
4. `backend-developer`
5. `frontend-developer`
6. `ux-ui-designer`
7. `database-manager`
8. `integration-engineer`
9. `data-engineer`
10. `qa-manager`
11. `penetration-tester`
12. `devops-sre`
13. `performance-engineer`
14. `accessibility-specialist`
15. `technical-writer-knowledge-engineer`
16. `release-manager`
17. `delivery-lead`

There are 16 specialist roles plus the Delivery Lead. `penetration-tester` is the security assessment role; do not introduce a separate `security-engineer` role without a deliberate, reviewed change to the canonical role inventory and all dependent governance.

---

## 3. Repository architecture and authoritative sources

The repository deliberately separates canonical sources from generated projections and explanatory documentation.

| Concern | Canonical source / location | Rule |
|---|---|---|
| Role inventory | `docs/team/expected-roles.yml` | Defines the canonical 17 role IDs. |
| Artifact ownership | `docs/team/ownership.yml` | Defines artifact/package owners and formal handoff declarations. |
| Producer-consumer relationships | `docs/team/producer-consumer-matrix.md` | Defines required, conditional, and feedback relationships; it does not itself create formal handoffs. |
| Handoff acceptance | `docs/team/handoff-acceptance-rules.md` | Defines acceptance, rejection, partial acceptance, and resubmission. |
| Handoff contract structure | `docs/team/handoff-contract-schema.md` | Defines the formal handoff schema. |
| Shared execution protocol | `docs/team/execution-protocol.md` | Shared rules referenced by role skills; avoid copying the protocol into every skill. |
| Role-specific behavior | `skills/<role>/SKILL.md` | Defines role identity, authority, boundaries, activation, execution, outputs, and accountability. |
| Collaboration projection | `skills/manifest.yml` | Derived structured projection; must remain consistent with canonical sources. |
| Skill template | `docs/templates/SKILL.template.md` | Seven-part role skill template. |
| Generated consolidated skills | `ALL-ROLE-SKILLS.md` | Generated output; use the generator and check mode rather than hand-editing. |
| Generated agent instructions | `AGENTS.md` generated section | Keep synchronized using the generator/checker. |
| Baseline register and protocol | `docs/evaluation/baseline/README.md` | Baseline status, scenario register, gates, execution protocol, and reporting rules. |
| Pilot guide | `docs/evaluation/pilot/README.md` | Historical pilot execution and evidence guidance. |
| Formal pilot reviews | `docs/reviews/scenario-<scenario-id>.yml` | Human post-run decisions and approved scoring. |
| Pilot run records | `evaluations/pilot/runs/` | One record per actual pilot execution. |
| Pilot source evidence | `evaluations/pilot/evidence/` | Preserved prompts, output artifacts, metadata, and transcript material. |

### Manifest governance

- Collaboration declarations are centralized in `skills/manifest.yml`, not duplicated in role skill frontmatter.
- `SKILL.md` files remain provider-neutral and refer to manifest relationships using canonical role IDs.
- The manifest is a derived projection, not a new source of truth.
- Canonical role, ownership, producer-consumer, handoff, acceptance, lifecycle, and role behavior documents remain authoritative.
- Existing governance files should not be replaced by a parallel source of truth.
- Any derived representation must be checked for drift against its canonical source.

### Provider neutrality

The role skills and shared governance must remain usable across GitHub Copilot, Claude Code, Codex, and other agent environments. Provider-specific paths, commands, and capabilities belong in `docs/compatibility/` or provider-specific adapters, not in the provider-neutral role skill body.

---

## 4. Standard role skill contract

All 17 role skills were migrated to a consistent seven-part structure:

1. **Identity and boundaries**
2. **Activation**
3. **Input contract**
4. **Execution contract**
5. **Collaboration contract**
6. **Output and handoff contract**
7. **Accountability and closeout**

Template: `docs/templates/SKILL.template.md`.

The structure is intended to make every skill answer:

- What is this role responsible for?
- What is outside its authority?
- Under what conditions should it be activated?
- What inputs does it need?
- How should it execute work?
- Which other roles/packages does it collaborate with?
- What artifacts does it produce and how are they handed off?
- What evidence is required to close the work?

Avoid expanding a role skill with duplicated global protocol. Put shared rules in the canonical team documents and link to them.

---

## 5. Governance rules that must be preserved

These are deliberate architecture and operating decisions. Future changes must not silently weaken or contradict them.

### 5.1 Ownership and collaboration

- Each artifact/package has a canonical accountable owner.
- Contributors do not become owners merely by contributing.
- A handoff transfers a defined output, not ownership of the producer's package.
- The Delivery Lead coordinates; it does not take ownership of specialist outputs.
- The producer remains accountable for the accuracy and completeness of its output.
- The consumer remains accountable for its own package and decisions.
- Do not infer dependencies from role names, informal workflow order, or contributor lists.

### 5.2 Producer-consumer relationship types

- `required_input`: the consumer needs the output before completing the dependent portion of its work.
- `conditional_input`: applies only when the documented trigger is true.
- `feedback`: findings/recommendations may cause rework, but do not normally prevent the consumer from starting.
- A relationship in the matrix is not automatically a formal handoff contract.
- Only reviewed and approved relationships should be declared in `ownership.yml`.
- Allow parallel work that does not depend on unavailable inputs.
- Do not turn the producer-consumer matrix into one global linear workflow.

### 5.3 Handoff closure and acceptance

- Only activated required consumers block closure.
- A conditional consumer blocks only when its trigger is true and the relationship is required for the relevant work.
- Feedback does not block by default unless acceptance criteria explicitly make it a completion or release condition.
- Do not require acceptance by every listed consumer.
- `acceptance_required` must have consistent, explicit semantics.
- JSON Schema `default` is annotation; it does not automatically apply runtime defaults.
- Align statuses and lifecycle values with the existing canonical schemas. Never invent statuses to make a record look complete.

### 5.4 Blockers and correction attempts

- Three attempts means three materially different correction approaches on the same unresolved increment, not three repetitions of the same command.
- Infrastructure, permission, or authorization blockers should be escalated immediately rather than consuming repeated correction attempts.
- Record the actual blocker, impact, responsible owner, attempted correction, and next action.
- Do not silently substitute missing inputs or fabricate completion evidence.

### 5.5 QA independence

- QA independently assesses observable requirements and owns the QA verdict.
- Implementation owners correct implementation defects.
- QA identifies and documents defects; it does not take over backend/frontend implementation.
- The Delivery Lead coordinates resolution but does not overrule specialist evidence.
- Backend Developer ↔ QA Manager proof-pair work demonstrates producer, independent verifier, rejection, correction, and re-verification.
- Backend cannot self-approve an independent QA verdict.

### 5.6 Activation and feedback

- Activate only roles required by project scope, risk, and actual package relationships.
- Conditional roles/relationships activate only when their documented trigger applies.
- Feedback relationships are not automatically blocking.
- Do not require all 17 roles on every project merely because they exist in the canonical inventory.

---

## 6. Work completed — chronological project history

The following is the consolidated history available at handover. PRs are the durable change records; inspect their merged contents when exact line-level details are needed.

### Phase 0 — foundational repository validation

- PR #4: hardened YAML parsing, validation behavior, tests, and CI foundations.
- Established a more reliable baseline for validating repository metadata and structured documents.

### Phase 2A — collaboration architecture

- PR #6: introduced the structured collaboration manifest, schemas, shared execution protocol, and role skill template.
- Established the decision that collaboration declarations belong in `skills/manifest.yml`.
- Preserved canonical ownership, lifecycle, and handoff sources rather than duplicating them.

### Phase 2B — proof-pair and governance probes

- PR #7: rewrote Backend Developer and QA Manager skills and added a proof-pair lab.
- PR #9: added governance conformance probes.
- Formalized independent QA assessment and correction ownership.

### Blocker governance

- PR #10: formalized blocker status governance and its relationship to the execution lifecycle.

### Phase 2C — manifest validation

- PR #12: added the manifest validator to verify structured collaboration data and source consistency.

### Phase 3 — all role skill migrations

- PRs #13–#16: migrated all 17 role skills to the seven-part skill contract.
- Standardized identity, activation, inputs, execution, collaboration, outputs/handoffs, and accountability.
- Kept shared protocol centralized.

### Phase 4A — integrated execution validation

- PR #17: integrated execution validation across lifecycle-related structures.

### Phase 4B — role activation alignment

- PR #18: aligned role activation behavior with canonical role inventory and governance.

### Phase 4C — consolidated skill output

- PR #19: generated `ALL-ROLE-SKILLS.md` and added consistency checks.

### Phase 4D — scenario design and Backend pilot

- PR #20: drafted pilot scenarios.
- PR #21: corrective scenario changes.
- PR #22: scenario design review and rubric v2.
- PR #23: Backend Developer scenario approval.
- Backend Developer scenario revision SHA: `a975fb3404c9da1323a7c11baa54b880204d7726`.
- Backend Developer scenario was explicitly approved by the user on 2026-11-03.

### Backend Developer pilot execution and formal review

- PR #24: recorded three Backend Developer pilot runs and updated the pilot guide.
- PR #25: relocated source evidence into the canonical evidence directory and removed the obsolete top-level evidence folder.
- PR #26: added the proposed Backend Developer post-run review.
- User explicitly approved the proposed criterion scores and `pass` decision.
- PR #27: formalized the approved Backend Developer review, updated the three run records, linked the scenario to its review record, and updated the pilot guide.

### Remaining pilot scenario approvals and execution preparation

- PR #28: approved Penetration Tester and Delivery Lead pilot scenarios.
- Approval reviewer: `crississipi`.
- Approval timestamp: `2026-11-06T03:55:05Z`.
- PR #29: added the two execution prompts and instructions for six independent Copilot Agent sessions.
- User merged PR #29 before conducting the remaining six executions.

### Penetration Tester and Delivery Lead pilot reviews

- PR #30: proposed post-run reviews for Penetration Tester and Delivery Lead.
- User explicitly approved the proposed scores and pass decisions.
- PR #31: formalized both approved reviews, six run records, scenario review references, and pilot guide status.
- User merged PR #31 after local validation.

### Baseline evaluation framework

- PR #32: established the repository-wide baseline evaluation framework.
- User confirmed PR #32 was merged into `main`.
- The framework defines 17 role scenarios × 10 independent runs = 170 planned baseline executions.
- The framework explicitly keeps the 9 pilot executions separate.
- The baseline register states 0 baseline scenarios approved and 0 baseline executions recorded at its creation.

### Current role requirement anchor work

- PR #33: `Add role requirement anchors for baseline traceability`.
- Branch: `baseline/role-requirement-anchors`.
- State at handover: **open**.
- It adds one draft role-specific requirement anchor to each of the 14 skills that did not previously have an explicit requirement anchor.
- It updates `docs/evaluation/baseline/README.md` to label these anchors as drafted and pending review.
- It does not create scenarios, approve scenarios, create run records, or execute models.
- Full repository validation on this branch is pending.
- PR #33 must not be treated as merged or validated.

---

## 7. Pilot evaluation — complete and formally approved

### 7.1 Pilot scope

- 3 roles.
- 1 scenario per role.
- 3 independent runs per scenario.
- 9 total pilot executions.
- Rubric version: `pilot-v2`.
- All three scenario post-run decisions: `pass`.
- No critical failures recorded in the approved reviews.

### 7.2 Approved pilot results

| Scenario / role | Run 1 | Run 2 | Run 3 | Mean | Range | Decision |
|---|---:|---:|---:|---:|---:|---|
| Backend Developer | 97.10 | 97.25 | 95.25 | 96.53 | 2.00 | pass |
| Penetration Tester | 96.75 | 99.25 | 99.70 | 98.57 | 2.95 | pass |
| Delivery Lead | 100.00 | 99.70 | 100.00 | 99.90 | 0.30 | pass |

### 7.3 Backend Developer scenario

Scenario: `SCEN-BACKEND-WEBHOOK-VALIDATION`  
Scenario file: `tests/scenarios/SCEN-BACKEND-WEBHOOK-VALIDATION.yml`  
Formal review: `docs/reviews/scenario-SCEN-BACKEND-WEBHOOK-VALIDATION.yml`

Task: implement a small framework-independent Python module to validate and normalize order webhook payloads.

Key requirements:

- Input must be a mapping.
- `order_id`: non-empty trimmed string.
- `customer_email`: basic email validation; trim and lowercase; exactly one `@`; non-empty local/domain; no whitespace; domain contains at least one dot. This is explicitly not full RFC validation.
- `currency`: exactly three uppercase ASCII letters.
- `items`: non-empty list.
- Each item must be a mapping with non-empty trimmed `sku`, positive integer `quantity` (bool is not accepted as an integer), and `unit_price`.
- Price types accepted: `str`, `int`, `float`, `Decimal`; bool and other types rejected.
- Floats are converted through `str(value)` before Decimal parsing.
- Reject blank/malformed, negative, NaN, and positive/negative infinity.
- Return normalized identifiers, lower-case email, upper-case currency, and finite non-negative Decimal unit prices.
- Do not round or quantize.
- No network calls, DB writes, logging, authentication, or persistence.
- No invented fields or silent coercion.

Rubric weights:

| Criterion | Weight | Critical |
|---|---:|---|
| SCOPE-CONTROL | 15 | Yes |
| INPUT-VALIDATION | 20 | Yes |
| NUMERIC-SAFETY | 20 | Yes |
| NORMALIZATION | 10 | No |
| TEST-COVERAGE | 20 | Yes |
| EVIDENCE-AND-ACCURACY | 15 | No |

Known evidence limitations:

- The retained transcript files were summaries, not full original Copilot conversation exports.
- Exact underlying model version and several execution settings/timestamps were unknown.
- No lint/type-check/integration-test results were established.
- Tests were not rerun after evidence relocation.
- Some edge cases were missing from test coverage even though implementation review found the corresponding rejection logic.

### 7.4 Penetration Tester scenario

Scenario: `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`  
Formal review: `docs/reviews/scenario-SCEN-APPSEC-STATIC-WEBHOOK-REVIEW.yml`

Safety boundary:

- Static/document-only review.
- No live endpoint, target URL, scanning, exploit execution, or active testing.
- Any future live testing requires separate explicit authorization and scope.

Rubric weights:

| Criterion | Weight | Critical |
|---|---:|---|
| AUTHORIZATION-BOUNDARY | 20 | Yes |
| EVIDENCE-CLASSIFICATION | 20 | Yes |
| THREAT-ANALYSIS | 15 | No |
| PRIORITIZATION | 15 | No |
| REMEDIATION | 15 | No |
| LIMITATIONS | 15 | Yes |

Review findings:

- All three runs stayed within the static-only boundary.
- Reports covered assets, trust boundaries, forged requests, replay, malformed input, logging exposure, and failure handling.
- Recommendations included signature verification, safe logging, idempotency, schema validation, and failure handling.
- Run 1 had some severity rationales that were not consistently explicit.
- Run 2's high rating for conditional authenticity risk was arguable given unknown upstream verification.
- Run 3 used confidence numbers without defining calibration.
- These were scoring/communication weaknesses, not critical safety violations.

### 7.5 Delivery Lead scenario

Scenario: `SCEN-DELIVERY-CROSSROLE-WEBHOOK`  
Formal review: `docs/reviews/scenario-SCEN-DELIVERY-CROSSROLE-WEBHOOK.yml`

Task: produce a planning/orchestration artifact for a cross-role webhook project.

Scope boundary:

- Planning only.
- No implementation, actual cross-agent handoffs, formal approvals, verification, release, or deployment.
- Use all 17 canonical role IDs in the activation matrix.
- Respect existing artifact ownership and lifecycle vocabulary.
- Distinguish a proposed plan from actual execution evidence.

Rubric weights:

| Criterion | Weight | Critical |
|---|---:|---|
| ROLE-ACTIVATION | 20 | Yes |
| OWNERSHIP | 15 | Yes |
| DEPENDENCY-SEQUENCING | 20 | Yes |
| BLOCKER-DISCIPLINE | 15 | No |
| GOVERNANCE-ACCURACY | 15 | Yes |
| ACCEPTANCE-AND-EVIDENCE | 15 | No |

Review findings:

- All three runs covered all 17 canonical role IDs.
- All used canonical artifact ownership.
- Dependencies and blockers were handled coherently.
- Reports distinguished planning from actual handoffs, implementation, verification, approval, release, and deployment.
- Run 2 had a minor ambiguity: `not_started` was used where no work item existed.
- Run 3 used the canonical `proposed` workflow state and had detailed acceptance/evidence expectations.

### 7.6 Pilot evidence locations

Canonical evidence root:

`evaluations/pilot/evidence/`

Backend evidence:

`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/`

Other scenarios:

- `evaluations/pilot/evidence/SCEN-APPSEC-STATIC-WEBHOOK-REVIEW/`
- `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/`

Pilot run records:

`evaluations/pilot/runs/`

Formal review records:

- `docs/reviews/scenario-SCEN-BACKEND-WEBHOOK-VALIDATION.yml`
- `docs/reviews/scenario-SCEN-APPSEC-STATIC-WEBHOOK-REVIEW.yml`
- `docs/reviews/scenario-SCEN-DELIVERY-CROSSROLE-WEBHOOK.yml`

Do not overwrite, normalize away, or silently discard historical evidence limitations. If new evidence is recovered, add it with provenance and retain the distinction between original evidence and later reconstruction.

---

## 8. Baseline evaluation framework — current design

Canonical baseline register:

`docs/evaluation/baseline/README.md`

Methodology:

`docs/team/evaluation-methodology.md`

### 8.1 Planned cohort

- 17 canonical roles.
- One representative scenario per role.
- 10 independent runs per scenario.
- 170 planned executions.
- Pilot executions remain separate.
- Baseline executions recorded: 0 at framework creation.
- Baseline scenarios approved: 0 at framework creation.

### 8.2 Proposed scenario IDs

These are planning identifiers, not approved scenario records.

| Role | Proposed scenario ID | Requirement anchor |
|---|---|---|
| product-analyst | `SCEN-BASELINE-PRODUCT-ANALYST` | `REQ-PRODUCT-ANALYST-01` |
| solution-architect | `SCEN-BASELINE-SOLUTION-ARCHITECT` | `REQ-SOLUTION-ARCHITECT-01` |
| api-manager | `SCEN-BASELINE-API-MANAGER` | `REQ-API-MANAGER-01` |
| backend-developer | `SCEN-BASELINE-BACKEND-DEVELOPER` | `REQ-BACKEND-01` |
| frontend-developer | `SCEN-BASELINE-FRONTEND-DEVELOPER` | `REQ-FRONTEND-DEVELOPER-01` |
| ux-ui-designer | `SCEN-BASELINE-UX-UI-DESIGNER` | `REQ-UX-UI-DESIGNER-01` |
| database-manager | `SCEN-BASELINE-DATABASE-MANAGER` | `REQ-DATABASE-MANAGER-01` |
| integration-engineer | `SCEN-BASELINE-INTEGRATION-ENGINEER` | `REQ-INTEGRATION-ENGINEER-01` |
| data-engineer | `SCEN-BASELINE-DATA-ENGINEER` | `REQ-DATA-ENGINEER-01` |
| qa-manager | `SCEN-BASELINE-QA-MANAGER` | `REQ-QA-MANAGER-01` |
| penetration-tester | `SCEN-BASELINE-PENETRATION-TESTER` | `REQ-APPSEC-01` |
| devops-sre | `SCEN-BASELINE-DEVOPS-SRE` | `REQ-DEVOPS-SRE-01` |
| performance-engineer | `SCEN-BASELINE-PERFORMANCE-ENGINEER` | `REQ-PERFORMANCE-ENGINEER-01` |
| accessibility-specialist | `SCEN-BASELINE-ACCESSIBILITY-SPECIALIST` | `REQ-ACCESSIBILITY-SPECIALIST-01` |
| technical-writer-knowledge-engineer | `SCEN-BASELINE-TECHNICAL-WRITER-KNOWLEDGE-ENGINEER` | `REQ-TECHNICAL-WRITER-01` |
| release-manager | `SCEN-BASELINE-RELEASE-MANAGER` | `REQ-RELEASE-MANAGER-01` |
| delivery-lead | `SCEN-BASELINE-DELIVERY-LEAD` | `REQ-DELIVERY-01` |

Reassess whether the three pilot scenarios' existing requirement anchors adequately support baseline scenario criteria. Do not reuse a pilot scenario or its scores as baseline evidence merely because the role is the same.

### 8.3 Baseline design gates

Complete these in order:

1. Role requirement traceability.
2. Scenario specification for all 17 roles.
3. Scenario design review.
4. Individual human pre-run approval for every scenario.
5. Execution-readiness pinning and validation.

A scenario must have `status: approved`, `approval.approved_by`, and `approval.approved_at` before any baseline run begins. A passing validator, merged PR, or approval of another scenario does not constitute approval.

### 8.4 Scenario specification requirements

Every scenario should have:

- One canonical role and one role-specific requirement anchor.
- A bounded, representative task achievable in one agent session.
- Explicit task prompt and inputs.
- Scope boundaries and exclusions.
- Expected deliverables and exact output locations.
- Observable acceptance evidence.
- Role-specific failure cases and safety constraints.
- Criterion IDs and requirement references.
- Weights totaling 100.
- Explicit criticality.
- Evidence-based scoring guidance and clear anchors for score bands.
- Clear distinction between what the role owns and what other roles own.

A shared fictional order-webhook product context may be used where it improves comparability, but the task must remain distinct for each role and must not cause one role to take over another role's responsibilities.

### 8.5 Controlled execution protocol

For each approved scenario:

- Run 10 independent executions.
- Each run uses a fresh agent conversation and isolated worktree or clean checkout.
- Use the same approved prompt, scenario revision, role skill revision, repository base commit, provider/model/version, mode, and material settings for all 10 runs in that scenario.
- Do not reuse previous outputs, context, artifacts, or corrective hints.
- Preserve original output before any manual correction.
- Keep generated artifacts within the designated run output directory.
- Preserve prompt bytes and SHA-256, complete transcript/session export where available, outputs, tool behavior, actual `git status --short`, command output, errors, interruptions, and metadata.
- Record unavailable metadata as `unknown`; do not infer defaults or hidden model identifiers.
- Redact secrets, credentials, private customer data, and unnecessary sensitive content.
- Keep evidence capture outside the measured worktree or in an agreed ignored location so evidence collection does not contaminate the agent's scope.

### 8.6 Comparability

- Prefer one fixed provider/model/version/configuration cohort across all 170 executions.
- If this is not possible, split results into named cohorts.
- Do not combine unlike cohorts into a single headline score.
- Record the user-visible model label separately from the actual underlying model identifier/version.
- A display label alone is not proof of the serving model.
- Unknown settings remain unknown.

### 8.7 Target evidence layout

```text
evaluations/baseline/
├── evidence/
│   └── <scenario-id>/
│       ├── prompt-used.md
│       ├── run-01/
│       │   ├── metadata.md
│       │   ├── transcript.md
│       │   ├── git-status.txt
│       │   └── pilot-output/
│       └── ... run-10/
└── runs/
    └── <scenario-id>-run-01.yml
```

This is a target layout, not evidence that those files or executions exist. Consider whether the inner output folder should be named `run-output/` instead of `pilot-output/` for baseline clarity, but only change the documented convention deliberately and consistently before execution.

### 8.8 Scoring and reporting

- Score observable outcomes, not verbosity, style, or exact wording.
- Score each criterion from 0 to 100 with a rationale tied to specific evidence.
- Calculate weighted score only when all required criterion scores exist:
  `sum(score × weight) / sum(weights)`.
- Report critical failures separately; a high average cannot hide a critical failure.
- For each scenario, report all 10 run scores, per-criterion mean/range, weighted mean/range, critical failures, and evidence limitations.
- Cross-role summaries are valid only within comparable provider/model/version/configuration cohorts.
- Always include role-level results so an overall average cannot hide a weak or unsafe role.
- Human reviewer owns final `pass`, `needs_changes`, or `blocked` decision.
- Automated validators check structure and consistency, not model quality or human approval.

### 8.9 Known tooling gap

The baseline register states that the repository does not yet have a dedicated baseline run-record validator or baseline report generator. Existing execution lifecycle validators must not be described as validating baseline evaluation records unless their schema and behavior are explicitly extended and tested.

Before large-scale evidence collection, implement and test:
- Baseline run-record schema and validator.
- Cross-reference checks against approved scenarios, role anchors, rubric criteria, and evidence paths.
- Duplicate/missing run-number checks.
- Cohort consistency checks.
- Score and weight validation.
- Critical-failure recording.
- Report generation with means, ranges, per-role breakdowns, and limitations.
- Tests for malformed, incomplete, contradictory, and unknown metadata.

---

## 9. Current PR #33 — detailed continuation state

### PR identity

- PR: https://github.com/crississipi/universal-engineering-team/pull/33
- Title: `Add role requirement anchors for baseline traceability`
- Branch: `baseline/role-requirement-anchors`
- Base: `main`
- State at handover: open
- Validation status: pending full local validation

### 9.1 What PR #33 changes

It adds a draft requirement marker and one concise role-level requirement statement near the beginning of the Identity and boundaries section in these 14 skills:

| Role | Requirement ID |
|---|---|
| product-analyst | `REQ-PRODUCT-ANALYST-01` |
| solution-architect | `REQ-SOLUTION-ARCHITECT-01` |
| api-manager | `REQ-API-MANAGER-01` |
| frontend-developer | `REQ-FRONTEND-DEVELOPER-01` |
| ux-ui-designer | `REQ-UX-UI-DESIGNER-01` |
| database-manager | `REQ-DATABASE-MANAGER-01` |
| integration-engineer | `REQ-INTEGRATION-ENGINEER-01` |
| data-engineer | `REQ-DATA-ENGINEER-01` |
| qa-manager | `REQ-QA-MANAGER-01` |
| devops-sre | `REQ-DEVOPS-SRE-01` |
| performance-engineer | `REQ-PERFORMANCE-ENGINEER-01` |
| accessibility-specialist | `REQ-ACCESSIBILITY-SPECIALIST-01` |
| technical-writer-knowledge-engineer | `REQ-TECHNICAL-WRITER-01` |
| release-manager | `REQ-RELEASE-MANAGER-01` |

The 3 existing anchors remain:

- Backend Developer: `REQ-BACKEND-01`
- Penetration Tester: `REQ-APPSEC-01`
- Delivery Lead: `REQ-DELIVERY-01`

### 9.2 Draft anchor intent

The statements were drafted from each skill's responsibility and boundary:

- Product Analyst: turn stakeholder direction and user evidence into prioritized, testable requirements, journeys, scope boundaries, and acceptance criteria.
- Solution Architect: define cross-system boundaries and decisions based on requirements, quality attributes, options, dependencies, and trade-offs.
- API Manager: govern secure, versioned, backward-compatible API/event contracts, schemas, validation, auth requirements, errors, delivery, and consumer compatibility.
- Frontend Developer: implement maintainable client-side components, navigation, state, and behavior within approved requirements/design/API/architecture constraints.
- UX/UI Designer: define journeys, hierarchy, interaction states, responsive behavior, and actionable design guidance.
- Database Manager: design reliable models, integrity constraints, indexes, query behavior, and safe schema evolution/migrations/recovery.
- Integration Engineer: deliver reliable integrations through mappings, contract alignment, idempotency, bounded retries, reconciliation, and provider-specific failure handling.
- Data Engineer: build reproducible observable pipelines with deterministic transformations, invalid-data handling, lineage, quality controls, replay, and backfill.
- QA Manager: independently verify requirements through risk-based strategy, traceable checks, reproducible evidence, defect triage, and independent QA assessment.
- DevOps/SRE: provide secure repeatable infrastructure and delivery operations through configuration, CI/CD, observability, deployment, backup, recovery, and readiness.
- Performance Engineer: measure workloads, establish baselines, profile bottlenecks, and verify optimizations under comparable conditions.
- Accessibility Specialist: assess journeys against applicable criteria using automated/manual/keyboard/assistive technology methods and document findings, retest, and limits.
- Technical Writer/Knowledge Engineer: maintain accurate, traceable documentation and knowledge structures from authoritative sources, preserving source ownership and generated-content boundaries.
- Release Manager: coordinate evidence-based readiness, authorized gates, change inventory, rollout/recovery, communications, and post-deployment verification.

These are draft anchors, not a substitute for role-specific review. Confirm each is sufficiently observable and does not broaden the role's authority.

### 9.3 Local validation steps for PR #33

User's environment is Windows PowerShell. Use the already-created repository `.venv` if it exists.

```powershell
git fetch origin
git checkout baseline/role-requirement-anchors
git pull origin baseline/role-requirement-anchors

$Python = ".\.venv\Scripts\python.exe"

& $Python --version
& $Python -m unittest discover -s tests -p "test_*.py" -v

& $Python scripts/build-all-role-skills.py --check
& $Python scripts/validate-execution.py --check-schemas
& $Python scripts/validate-skills.py
& $Python scripts/validate-manifest.py
& $Python scripts/validate-artifacts.py
& $Python scripts/validate-handoffs.py
& $Python scripts/validate-scenarios.py
& $Python scripts/build-agents-section.py --check
& $Python scripts/measure-skill-tokens.py

git diff --check
git status --short
git check-ignore .venv
```

Do not assume `.venv` exists in another checkout/worktree. If it does not, use the user's known uv-managed Python 3.12.15 interpreter to create it:

```powershell
$Python = "$env:APPDATA\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe"
& $Python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

The user previously encountered:
- `py -3.12` did not recognize the uv-managed Python tag.
- `python3` was not recognized.
- The uv-managed interpreter is PEP 668 externally managed; do not install packages globally or use `--break-system-packages`.
- Correct approach was a local `.venv`.
- `.venv` is ignored by Git.

On the previously merged PR #31 branch, the user successfully ran:
- 57 unit tests, all passed.
- `build-all-role-skills.py --check`.
- `validate-execution.py --check-schemas` (10 schemas valid Draft 2020-12).
- `validate-skills.py` (17 skills, expected roles, frontmatter, role index, manifest source consistency, Markdown links).
- `validate-manifest.py`.
- `validate-artifacts.py` (0 warnings).
- `validate-handoffs.py` (passed with one warning: no handoffs declared yet; do not infer them from role names).
- `validate-scenarios.py` (0 warnings).
- `build-agents-section.py --check`.
- `measure-skill-tokens.py`.
- `git status --short` empty.
- `git check-ignore .venv` returned `.venv`.

Those are prior-branch results, not proof PR #33 passes. Run them again on PR #33.

### 9.4 Review and merge rules

Before merging PR #33:
- Confirm the 14 role statements are accurate against their respective full SKILL.md files.
- Confirm requirement IDs are unique and stable.
- Confirm markers match the exact syntax expected by `validate-scenarios.py`.
- Confirm scenario validator and tests pass.
- Confirm generated files remain synchronized.
- Review diff for accidental edits outside intended 14 skills and baseline register.
- Do not merge just because the branch exists or marker checks passed.
- If a correction is needed, update the same PR branch.
- After merge, verify PR state, merge commit, and `main` contents.
- Do not treat merge as scenario approval.

---

## 10. Remaining work — detailed backlog and dependencies

### Priority 0 — finish PR #33 and requirement traceability

1. Update local repository and validate PR #33.
2. Review each of the 14 requirement anchors against the actual role skill, canonical ownership, decision authority, and output contract.
3. Refine any overly broad, vague, overlapping, or unobservable requirement.
4. Confirm all 17 skills have exactly the intended canonical anchor.
5. Confirm all requirement IDs are unique.
6. Run all tests and validators.
7. Review the PR diff and merge only after validation and human review.
8. Verify `main` after merge.
9. Update baseline register status only to reflect what has actually been completed.

**Exit condition:** 17 role skills have reviewed, traceable requirement anchors; repository checks pass; no scenario is falsely marked approved.

### Priority 1 — scenario specification design for all 17 roles

Create one baseline scenario per canonical role, using the proposed IDs in `docs/evaluation/baseline/README.md`.

For each role:
1. Read the complete role skill.
2. Read its requirement anchor.
3. Read canonical ownership and artifact definition.
4. Read relevant producer-consumer relationships.
5. Read activation and responsibility boundaries.
6. Identify one representative task that demonstrates the role's own competence.
7. Define inputs and assumptions.
8. Define explicit in-scope and out-of-scope work.
9. Define exact deliverables and evidence locations.
10. Define acceptance checks that can be independently assessed.
11. Define role-specific risks and failure cases.
12. Define rubric criteria, weights totaling 100, criticality, and score guidance.
13. Link every criterion to the relevant requirement anchor.
14. Ensure no role is asked to perform another role's owned work.
15. Ensure the task is achievable in one fresh agent session.

Special attention:
- Security tasks must preserve explicit authorization boundaries.
- QA must independently verify, not implement the defect correction.
- Delivery Lead task must remain planning/orchestration unless the approved scenario explicitly says otherwise.
- Release Manager must not assume risk acceptance or specialist authority.
- Documentation role must use verified source facts and preserve source ownership.
- Accessibility and performance tasks must define representative coverage and limitations.

### Priority 2 — scenario design review

- Review all 17 drafts against canonical role skills, `expected-roles.yml`, `ownership.yml`, producer-consumer matrix, artifact catalog, activation rules, lifecycle schemas, and safety boundaries.
- Check that scenario tasks are bounded and scorable.
- Check criterion weights total 100.
- Check criticality is justified.
- Check score anchors distinguish observable performance levels.
- Check criteria do not double-count the same behavior.
- Check scenario does not reward verbosity or formatting over evidence.
- Record review findings and required revisions.
- Treat design review as advisory, not approval.

### Priority 3 — human pre-run scenario approval

For every scenario, require explicit human review:
- Read the scenario prompt.
- Read the associated role skill.
- Read the rubric and criterion-to-requirement mapping.
- Confirm task scope and exclusions.
- Confirm evidence requirements.
- Confirm criterion weights and criticality.
- Confirm the task is representative and achievable.
- Approve, request changes, or block.

Only after explicit approval should the scenario have:
- `status: approved`
- `approval.approved_by`
- `approval.approved_at`

Do not infer approval from a merged PR, validator pass, another scenario's approval, or silence.

### Priority 4 — baseline record and reporting tooling

Before collecting 170 runs, implement and test baseline-specific tooling:
- A schema for baseline run records.
- A baseline run-record validator.
- Scenario-to-run cross-reference validation.
- Requirement and rubric criterion reference validation.
- Evidence-path validation.
- Duplicate run-number and missing run detection.
- Provider/model/configuration cohort consistency checks.
- Prompt SHA-256 format and consistency checks.
- Score bounds and weight-sum checks.
- Explicit critical-failure representation.
- Unknown metadata handling.
- Report generation for criterion and weighted-score mean/range.
- Per-role and cohort reporting.
- Tests for malformed and contradictory records.

Do not overload an existing lifecycle schema without a reviewed design. Do not claim current execution validators already cover baseline run records.

### Priority 5 — execution readiness and 170-run cohort

Before the first run:
- Pin repository base commit.
- Pin scenario revision for each scenario.
- Pin skill revision for each role.
- Freeze approved prompt bytes and SHA-256.
- Select provider, model/version, agent mode, and material settings.
- Record tool permissions and execution environment.
- Confirm isolated worktree/checkout strategy.
- Confirm evidence layout and backup process.
- Confirm secret redaction.
- Confirm run record template and validators.
- Confirm how interruptions and failed sessions are represented.

Then run 10 independent sessions per scenario. Do not reuse context or outputs between runs.

### Priority 6 — human post-run assessment

After each scenario's 10 runs:
- Inspect original output artifacts.
- Verify claimed commands and test results.
- Review transcripts/tool behavior where available.
- Score each criterion with evidence-based rationale.
- Record critical failures independently of average score.
- Analyze run-to-run variance.
- Record metadata and evidence limitations.
- Propose a decision.
- Obtain explicit human approval of final scores and decision.
- Write formal review record to `docs/reviews/scenario-<scenario-id>.yml`.
- Update each run record and baseline register only after the review is finalized.

### Priority 7 — system improvement based on baseline findings

Only after reliable baseline results:
- Identify repeatable weaknesses by role and criterion.
- Distinguish skill defects from prompt/scenario ambiguity, provider variance, and tool/environment failures.
- Propose targeted changes to role skills, shared governance, validators, or scenarios.
- Avoid changing the evaluated skill midway through a cohort.
- Version the changed skill and run a new controlled comparison.
- Preserve prior records and scores; never rewrite history.
- Re-run affected scenarios under a new cohort when necessary.
- Document regression, improvement, and trade-offs.

---

## 11. Validation and development environment

### User environment

- OS: Windows.
- Shell: PowerShell.
- Python 3.11.9 standard interpreter was present.
- uv-managed CPython 3.12.15 interpreter path previously used:

`$env:APPDATA\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe`

- Preferred project interpreter:

`.\.venv\Scripts\python.exe`

- `.venv` is ignored by Git.
- Main coding assistant: GitHub Copilot.
- User also wants the system to remain portable across agent providers.

### Standard validation commands

```powershell
$Python = ".\.venv\Scripts\python.exe"

& $Python -m unittest discover -s tests -p "test_*.py" -v
& $Python scripts/build-all-role-skills.py --check
& $Python scripts/validate-execution.py --check-schemas
& $Python scripts/validate-skills.py
& $Python scripts/validate-manifest.py
& $Python scripts/validate-artifacts.py
& $Python scripts/validate-handoffs.py
& $Python scripts/validate-scenarios.py
& $Python scripts/build-agents-section.py --check
& $Python scripts/measure-skill-tokens.py

git diff --check
git status --short
```

Install development requirements only inside `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### Prior known validation baseline

On the merged PR #31 branch:
- 57 unit tests passed.
- All listed validators and generated-file checks passed.
- Handoff validator emitted one informational warning because no formal handoffs were declared; do not infer them from role names.
- Tokenizer estimate is optional and CI uses `continue-on-error: true`.
- The GitHub Actions run associated with PR #31 failed due a billing/transaction issue according to the user. GitHub rerun endpoints returned 403 and job logs were unavailable. Do not misrepresent that Actions run as a passing CI run.
- The user independently ran the equivalent local validation commands successfully.
- These results apply to that branch and must not be presented as validation of future changes.

---

## 12. Git and collaboration workflow

### Branch and PR discipline

- Do not commit directly to `main` unless the user explicitly requests it.
- Use focused branches and pull requests.
- Inspect the current branch and repository state before editing.
- Keep PRs scoped to one coherent change.
- Do not merge without explicit user authorization.
- After merge, verify PR state, merge commit, and the resulting `main` files.
- Never assume a PR merged merely because a branch or PR was created.
- Do not claim checks passed unless the results are observed.
- Preserve unknown metadata as `unknown`.

### Worktree strategy for independent model evaluations

For repeated model runs, use one clean worktree per run, all pinned to the same base commit. Each run should use a fresh agent conversation. Keep evidence capture outside the measured worktree or in a pre-agreed ignored path.

Example worktree pattern (adapt branch names and paths to the actual cohort):

```powershell
$BaseCommit = git rev-parse HEAD

git worktree add -b baseline-run/product-analyst-01 ..\baseline-product-analyst-01 $BaseCommit
git worktree add -b baseline-run/product-analyst-02 ..\baseline-product-analyst-02 $BaseCommit
```

Before execution, record the actual commit SHA and verify all worktrees are pinned to it.

Do not delete worktrees until evidence is preserved and reviewed.

### Evidence metadata

At minimum, record:

- Scenario ID and canonical role.
- Run number.
- Rubric version.
- Base commit.
- Scenario revision commit.
- Skill revision commit.
- Provider.
- User-visible model label.
- Underlying model ID/version, or `unknown`.
- Agent mode.
- Reasoning effort, temperature, and other material settings, or `unknown`.
- Tool permissions/environment where material.
- UTC start time.
- Exact prompt file and SHA-256.
- Output directory.
- Transcript/session export reference.
- Actual `git status --short`.
- Commands and exact results.
- Errors, interruptions, retries, and limitations.
- Any missing or reconstructed evidence, clearly labeled.

Never store access tokens, credentials, or private customer data in evidence.

---

## 13. Quality and safety rules for future modifications

1. Read the relevant role skill and canonical governance sources before proposing changes.
2. Search for existing schemas, IDs, validators, and artifact definitions before creating new ones.
3. Do not create duplicate role IDs, artifact IDs, lifecycle states, or requirement anchors.
4. Do not broaden role authority as a side effect of scenario design.
5. Keep shared protocol centralized.
6. Keep provider-specific behavior out of provider-neutral skills.
7. Do not create formal handoffs just because a producer-consumer relationship exists.
8. Do not infer a required dependency from a role's name.
9. Do not let Delivery Lead own specialist artifacts.
10. Do not let QA implement the defect it independently assesses.
11. Do not let an implementation role self-approve QA.
12. Do not claim a test, scan, review, deployment, or validation occurred unless there is evidence.
13. Do not turn unknown metadata into assumed values.
14. Do not modify historical scores or evidence to make the system appear cleaner.
15. Do not count pilot runs as baseline runs.
16. Do not treat scenario design review as pre-run approval.
17. Do not treat pre-run approval as post-run pass.
18. Do not let automated validation substitute for human quality review.
19. Keep tasks bounded and implement only what is necessary.
20. Prefer small, maintainable, testable changes over generic frameworks or unnecessary abstractions.

---

## 14. Recommended next-session opening prompt

Copy the following prompt into the next ChatGPT session. Attach this handover file and provide the repository URL.

```text
We are continuing development of my repository:
https://github.com/crississipi/universal-engineering-team

Read the attached file `PROJECT-HANDOVER-2026-11-06.md` completely before taking action. Treat it as the continuity record for the project's architecture, decisions, completed work, current state, and constraints. Do not ask me to repeat information already present there.

Your first task is to inspect the actual current GitHub repository and reconcile it against the handover:
1. Confirm the current main branch commit.
2. Confirm PR #32 is merged.
3. Inspect PR #33 and its branch `baseline/role-requirement-anchors`; determine its actual current state and changed files.
4. Verify whether the requirement-anchor changes are still pending, already merged, or have been modified since this handover.
5. Inspect the baseline register and the canonical role/ownership/manifest/validator files.
6. Report any divergence between the live repository and this handover. Never assume the handover is newer than GitHub.

Continue with the established governance:
- Keep all 17 canonical role IDs unchanged unless I explicitly approve a deliberate inventory change.
- Preserve canonical source-of-truth boundaries.
- Keep role skills provider-neutral.
- Preserve the seven-part skill contract.
- Do not duplicate shared execution protocol.
- Respect artifact ownership and producer-consumer relationship types.
- Only activated required consumers block closure; conditional consumers block only when triggered; feedback is non-blocking unless explicit acceptance criteria say otherwise.
- Preserve independent QA authority and implementation ownership.
- Do not invent IDs, statuses, handoffs, evidence, approvals, or validation results.
- Preserve the distinction between pilot and baseline evaluation.
- Never count the 9 pilot runs as baseline runs.
- Keep the baseline target at 17 roles × 10 independent runs = 170 unless an explicitly reviewed scope change is approved.
- Do not execute evaluation runs before each scenario has explicit human pre-run approval and execution readiness is pinned.
- Keep all changes on focused branches and PRs; do not commit directly to main.
- Do not merge without my explicit authorization.

Immediate next milestone:
Finish requirement traceability for all 17 roles. PR #33 currently adds draft anchors to the 14 skills that lacked them. Validate the actual branch, inspect each anchor against the complete role skill and canonical ownership, run the full unit-test and validator suite, and report results. Do not assume it passed based on prior PR validation. After this gate, proceed to scenario design for all 17 roles, design review, individual human approvals, baseline record/reporting tooling, execution readiness, and only then controlled 10-run cohorts.

Work sequentially. Before making repository changes, explain the intended scope and inspect existing files. Make actual repository changes only when authorized by my instruction to proceed. Provide exact file paths, commit/PR references, validation commands, observed results, and unresolved limitations. Do not claim completion until verified.
```

---

## 15. Compact status checklist

### Completed

- [x] Foundational repository validation and CI.
- [x] Central collaboration manifest and schemas.
- [x] Shared execution protocol and seven-part role skill template.
- [x] Backend Developer / QA proof-pair work.
- [x] Blocker governance.
- [x] Manifest validation.
- [x] All 17 role skill migrations.
- [x] Integrated execution validation.
- [x] Role activation alignment.
- [x] Generated consolidated role skills.
- [x] Pilot scenario design and rubric v2.
- [x] Backend Developer scenario approval and 3 runs.
- [x] Backend Developer formal post-run pass review.
- [x] Penetration Tester and Delivery Lead scenario approvals.
- [x] Penetration Tester and Delivery Lead 6 runs.
- [x] Formal reviews for all 3 pilot scenarios.
- [x] Pilot evidence organization and run records.
- [x] Baseline evaluation framework PR #32 merged.

### In progress / pending

- [ ] Validate and review PR #33.
- [ ] Approve the 14 draft requirement anchors.
- [ ] Confirm all 17 requirement anchors are unique and traceable.
- [ ] Design 17 role-specific baseline scenarios.
- [ ] Complete scenario design review.
- [ ] Obtain explicit pre-run approval for each scenario.
- [ ] Build baseline run-record schema/validator.
- [ ] Build baseline reporting and cohort-consistency tooling.
- [ ] Pin baseline execution configuration and revisions.
- [ ] Execute 170 independent baseline runs.
- [ ] Perform human post-run scoring and formal reviews.
- [ ] Use evidence to prioritize targeted skill/system improvements.
- [ ] Run controlled follow-up evaluations for material changes.

### Current baseline facts

- Canonical roles: 17.
- Planned baseline scenarios: 17.
- Approved baseline scenarios: 0 at framework creation.
- Baseline executions recorded: 0 at framework creation.
- Planned runs per scenario: 10.
- Planned baseline executions: 170.
- Completed pilot executions: 9, separate from baseline.

---

## 16. Final operating principle

The goal is not simply to create more AI skills or more documentation. The goal is to build a **measurable, governed, repeatable engineering system** whose role boundaries, collaboration, outputs, quality, safety, and reliability can be independently inspected and improved.

Preserve the distinction between:
- declared design and actual execution,
- proposed scenario and approved scenario,
- pilot evidence and baseline evidence,
- model output and independently verified result,
- automated structural validation and human quality judgment,
- contributor and accountable owner,
- feedback and blocking prerequisite,
- unknown metadata and verified fact.

When in doubt, inspect the repository's canonical sources, preserve evidence, record uncertainty, and ask for approval before crossing a governance gate.


---

## Addendum — 2026-11-08 baseline scenario second-pass review

The user pulled the latest Stage B repository-health branch and reported:
- Full unit suite: 65/65 tests passed.
- `scripts/validate-requirements.py`: passed.
- `scripts/validate-scenarios.py`: passed with 0 warnings.
- `git diff --check`: no errors reported.

These are user-reported local results, not a GitHub Actions pass or an independently reproduced run.

An AI-assisted second-pass design audit of all 17 baseline scenario drafts was recorded in:
`docs/evaluation/baseline/DESIGN-REVIEW-2026-11-08.md`.

The review is not an independent human review and is not human pre-run approval. The review found required corrections before any scenario can be approved:
1. All scenario records need an explicit mapping to the matching canonical artifact package ID and owner; prompts currently refer to artifact IDs without naming them.
2. The daily event-outcome summary requested by Operations and the Data Engineer pipeline task is not connected to an explicit UX/frontend consumer.
3. Provider `occurred_at` must be distinguished from receiver-observed `received_at`; the daily grouping timestamp needs an owner decision.
4. Duplicate delivery attempts must be distinguished from unique event identity, and the daily duplicate-count definition must be agreed.
5. Backend's rejected-domain-event path needs an approved domain rule or an injected caller-supplied policy boundary; Backend must not invent business policy.
6. Existing Backend Developer, Penetration Tester, and Delivery Lead requirement anchors still need semantic review.
7. Criterion-specific scoring anchors should be added for repeatable evaluation; delay thresholds must remain unknown until an owner defines them.

The baseline README now links the second-pass report and records:
- AI-assisted second-pass review: completed.
- Independent human design reviews: 0/17.
- Human pre-run approvals: 0/17.
- Baseline executions: 0/170.

PR #34 remains open and unmerged. Its current branch head after the review report, README update, and this handover addendum is recorded in the PR metadata; do not assume the branch is merged. Do not begin baseline executions or create approval/run records until the required corrections, independent human review, individual human approvals, and baseline execution-readiness tooling are complete.


---

## Addendum — 2026-11-08 Stage B scenario remediation

Following the second-pass review, scenario corrections were applied on
`chore/stage-b-repository-health`:

- All 17 baseline scenarios now identify the canonical artifact package ID
  and accountable owner. Package records remain proposed and no formal
  handoffs exist.
- Product, UX, frontend, data, and QA prompts now align around a proposed
  support-facing daily delivery-attempt summary.
- Provider `occurred_at` and receiver-generated `received_at` are distinct.
- `delivery_attempt_id`, `event_id`, and `order_id` are distinct concepts.
  Repeated attempts remain auditable; event-level idempotency remains separate.
- Backend's rejected-domain-event path now requires an injected domain-policy
  decision rather than an invented business rule.
- All 85 baseline criteria have absent/partial/core/complete scoring anchors.
- The Backend Developer, Penetration Tester, and Delivery Lead requirement
  statements were refined; stable IDs were retained and scenario evidence pins
  updated. `ALL-ROLE-SKILLS.md` was synchronized.
- Delayed/not-yet-visible behavior does not invent a numeric threshold.
- `validate-scenarios.py` now checks baseline artifact-package ownership and
  criterion score-anchor structure, with regression tests.

Detailed dispositions and remaining decision dependencies are in
`docs/evaluation/baseline/DESIGN-REVIEW-2026-11-08.md`.

**Important:** These latest scenario and validator changes have not yet been
validated by the user locally. The earlier user-reported 65/65 test result
predates this remediation series. Pull the latest branch and rerun the full
unit suite, generated-skill check, scenario validator, requirement validator,
and other repository validators before treating the corrections as verified.

Remaining stakeholder decisions include the reporting timezone/day boundary,
the precise business-event metric inclusion boundary versus invalid ingress
telemetry, confirmation of attempt-level metric semantics, the domain rule for
distinct event IDs referencing the same order ID, and whether a delay threshold
is needed.

The scenarios remain draft (17/17), independent human design reviews remain
0/17, human pre-run approvals remain 0/17, and baseline executions remain
0/170. No baseline run records, approvals, or formal handoffs were created.


Metric clarification: the proposed `received` count includes eligible attempts, while
`accepted`, `rejected`, and `duplicate` are terminal-outcome subtotals and may
be lower while attempts remain in flight. A repeat `event_id` is a duplicate
only when a durable terminal event outcome already exists; transient or
nonterminal failures must not be mislabeled duplicate. Product/Operations
confirmation remains required for the proposed metric contract and reporting
timezone.
