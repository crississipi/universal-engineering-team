# Stage B baseline scenario author preflight

- Date: 2026-11-08
- Branch: `chore/stage-b-repository-health`
- Baseline repository context: `f7d30d8f7fd868f7154fa08cfce1a36362ecf5ff`
- Reviewer type: author-side structural and role-boundary preflight
- Independent reviewer: not performed
- Human pre-run approval: not performed
- Baseline execution: not started

## Purpose and decision boundary

This record documents an author-side preflight of the 17 draft baseline scenarios. It is not the independent scenario design review required by the baseline protocol and is not human pre-run approval. No scenario is approved by this record. All scenario files remain `status: draft` with `review_record: null`.

## Structural preflight

The 17 scenario files were inspected from the branch. The author-side checks confirmed:
- one unique scenario ID matching its canonical role;
- one canonical role ID per scenario;
- one matching requirement ID per scenario;
- five distinct rubric criteria per scenario;
- criterion weights totaling 100 points per scenario;
- every criterion references the scenario's role requirement anchor;
- a canonical skill evidence path and full 40-character Git commit reference;
- no approval metadata or post-run review record was added.

This inspection was performed against the repository text via the connected GitHub repository interface. The local Python scenario validator and complete local test suite have not been rerun against this exact 17-scenario branch revision. The user's previously shared local test run established 65/65 tests passing before these scenario files were added. A new local validation run is still required.

## Scenario-by-scenario preflight

| Role | Scenario | Role-boundary preflight | Design note for independent reviewer |
|---|---|---|---|
| Product Analyst | `SCEN-BASELINE-PRODUCT-ANALYST` | Suitable draft | Check that requirements remain tied to supplied support/operations needs and that unknown permissions, retention, filters, replay, and service targets remain decisions rather than assumptions. |
| Solution Architect | `SCEN-BASELINE-SOLUTION-ARCHITECT` | Suitable draft | Review the synchronous durable-write versus durable-queue-acceptance comparison for neutrality; do not assume a queue or choose a platform without evidence. |
| API Manager | `SCEN-BASELINE-API-MANAGER` | Suitable draft | Confirm exact raw-body HMAC semantics and that timestamp signing, retry policy, replay windows, and secret rotation remain explicitly unknown. |
| Backend Developer | `SCEN-BASELINE-BACKEND-DEVELOPER` | Suitable draft; anchor needs semantic review | The task is intentionally limited to an application service and durable repository contract; it must not claim that a fake repository proves database isolation or concurrency behavior. The existing anchor should be reviewed because its statement is framed as a broad purpose rather than a measurable requirement. |
| Frontend Developer | `SCEN-BASELINE-FRONTEND-DEVELOPER` | Suitable draft | Check that the fixture-driven view does not imply backend access, authentication, customer-facing functionality, or approved support permissions. |
| UX/UI Designer | `SCEN-BASELINE-UX-UI-DESIGNER` | Suitable draft | Check that interaction guidance is sufficiently actionable while avoiding invented brand tokens, permission decisions, retention rules, or a conformance claim. |
| Database Manager | `SCEN-BASELINE-DATABASE-MANAGER` | Suitable draft | Ensure SQL is clearly conceptual/dialect-neutral and that production migration/backfill/rollback cannot be inferred without engine, existing schema, data-volume, and operational evidence. |
| Integration Engineer | `SCEN-BASELINE-INTEGRATION-ENGINEER` | Suitable draft | Check that delivery, retry, acknowledgement, reconciliation, and replay semantics are separated and that unknown provider behavior is not invented. |
| Data Engineer | `SCEN-BASELINE-DATA-ENGINEER` | Suitable draft | Check that aggregation is deterministic, currency values are not mixed, and the source contract is marked as a proposed requirement pending confirmation from its owner. |
| QA Manager | `SCEN-BASELINE-QA-MANAGER` | Suitable draft | Ensure test cases map to approved acceptance criteria where available and that planned, executable, blocked, and unrun tests are not conflated. |
| Penetration Tester | `SCEN-BASELINE-PENETRATION-TESTER` | Suitable draft; anchor needs semantic review | The exercise is expressly static-only. Confirm that findings distinguish facts from conditional risks because no implementation or runtime controls are supplied. The existing anchor should be reviewed for a more observable statement covering evidence-based assessment and limitations. |
| DevOps/SRE | `SCEN-BASELINE-DEVOPS-SRE` | Suitable draft | Check that the task requests operational design only and does not invent a hosting platform, CI provider, SLO, RTO/RPO, traffic level, or deployment authorization. |
| Performance Engineer | `SCEN-BASELINE-PERFORMANCE-ENGINEER` | Suitable draft | Ensure workload values remain illustrative placeholders and that no baseline measurements or bottleneck claims are fabricated. |
| Accessibility Specialist | `SCEN-BASELINE-ACCESSIBILITY-SPECIALIST` | Suitable draft | Check that confirmed source-level barriers are distinguished from dynamic/runtime behavior not provided. WCAG mapping and severity should be justified, not mechanically inferred. |
| Technical Writer / Knowledge Engineer | `SCEN-BASELINE-TECHNICAL-WRITER-KNOWLEDGE-ENGINEER` | Suitable draft | Verify that each factual statement is source-traceable and that absent Obsidian/Graphify/report updates are disclosed rather than claimed. |
| Release Manager | `SCEN-BASELINE-RELEASE-MANAGER` | Suitable draft | Confirm the scenario produces an evidence-gated no-go recommendation while marking unavailable gate evidence as not verified rather than assuming approval. |
| Delivery Lead | `SCEN-BASELINE-DELIVERY-LEAD` | Suitable draft; anchor needs semantic refinement | Check all 17 activation classifications, exact single-owner artifact mapping, proposed ownership status, dependency sequencing, and no invented handoffs. The existing anchor currently describes the coordination function and may not be sufficiently observable as a requirement. |

## Cross-scenario design checks

- All scenarios use the same fictional MerchantCloud-to-OrderDesk webhook facts so the baseline task family is comparable.
- Each role has a different primary output and a role-specific failure or boundary condition.
- Implementation, planning, verification, security assessment, documentation, and release work are deliberately separated.
- Scenarios do not require live external services, credentials, production access, real network activity, or deployment.
- The three pilot roles have distinct baseline tasks; pilot outputs and pilot runs are not reused as baseline results.
- Every scenario has five criteria totaling 100 points. Critical criteria are marked separately so an average cannot conceal a critical failure.
- Prompt context includes the ownership and handoff governance boundary: artifact entries are proposed and no formal handoff contracts are declared.

## Role requirement anchor review queue

All 17 role anchors are structurally present, unique, and mapped in the baseline register. This is not semantic approval. The following legacy anchors require explicit review before the scenarios are approved:
1. `REQ-BACKEND-01`: current adjacent statement is phrased as a purpose and is broad relative to a baseline observation.
2. `REQ-APPSEC-01`: current adjacent statement broadly describes security assessment activities but does not, by itself, express evidence/uncertainty handling as an observable success condition.
3. `REQ-DELIVERY-01`: current adjacent statement describes the Delivery Lead's coordination role rather than a crisp, outcome-oriented requirement.

The other 14 anchors were introduced by PR #33. Their wording still requires role-owner/governance confirmation. No anchor is approved by this preflight.

## Required next review actions

1. Have an independent reviewer assess each scenario against the role skill, artifact ownership, activation rules, producer-consumer matrix, safety boundary, and rubric observability.
2. Record one design-review file per scenario using `docs/templates/baseline-scenario-review.template.md`. Keep recommendations advisory; do not use the word "approved" as the design-review outcome.
3. Resolve role-anchor semantic findings with the appropriate role owners/governance reviewer.
4. Revise any ambiguous or unscorable prompt/rubric and repeat structural validation.
5. Only after independent review, ask the authorized human approver to set each scenario's `status: approved` and populate `approval.approved_by` and `approval.approved_at`.
6. Do not create run records, evidence directories, or post-run reviews before actual runs occur.

## Current gate result

- Scenario drafts authored: 17/17.
- Structural author preflight: 17/17.
- Independent design reviews: 0/17.
- Human pre-run approvals: 0/17.
- Baseline runs: 0/170.
- Post-run reviews: 0/17.

**Disposition:** ready for independent design review only; not ready for human pre-run approval or baseline execution.
