# Repository-wide baseline evaluation

## Purpose and status

This directory defines the controlled Stage B baseline for the 17 canonical role
skills. It is a plan and design register, not evidence that baseline runs have
started.

- Baseline scope: 17 canonical roles.
- Planned scenario count: one approved representative scenario per role.
- Planned repetitions: 10 independent runs per scenario.
- Planned baseline executions: 170.
- Baseline executions recorded: 0.
- Baseline scenarios approved: 0.
- Pilot executions are separate and are not counted toward the baseline.

The completed pilot remains recorded under `evaluations/pilot/` and
`docs/evaluation/pilot/README.md`. Its three passing scenarios establish that
the pilot workflow is usable; they do not establish baseline results.

## Canonical role coverage and scenario design register

Every role below must have one baseline scenario with a task that exercises its
actual ownership boundary. The draft scenario files now exist for all 17
roles. Their IDs and content remain proposals until independent design review
and explicit human pre-run approval are completed.

| Canonical role | Pilot coverage | Baseline scenario ID (proposed) | Role requirement anchor | Design state |
|---|---|---|---|---|
| product-analyst | None | SCEN-BASELINE-PRODUCT-ANALYST | REQ-PRODUCT-ANALYST-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| solution-architect | None | SCEN-BASELINE-SOLUTION-ARCHITECT | REQ-SOLUTION-ARCHITECT-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| api-manager | None | SCEN-BASELINE-API-MANAGER | REQ-API-MANAGER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| backend-developer | Pilot only | SCEN-BASELINE-BACKEND-DEVELOPER | REQ-BACKEND-01 (exists; reassess baseline fit) | Drafted — anchor semantic review recommended |
| frontend-developer | None | SCEN-BASELINE-FRONTEND-DEVELOPER | REQ-FRONTEND-DEVELOPER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| ux-ui-designer | None | SCEN-BASELINE-UX-UI-DESIGNER | REQ-UX-UI-DESIGNER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| database-manager | None | SCEN-BASELINE-DATABASE-MANAGER | REQ-DATABASE-MANAGER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| integration-engineer | None | SCEN-BASELINE-INTEGRATION-ENGINEER | REQ-INTEGRATION-ENGINEER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| data-engineer | None | SCEN-BASELINE-DATA-ENGINEER | REQ-DATA-ENGINEER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| qa-manager | None | SCEN-BASELINE-QA-MANAGER | REQ-QA-MANAGER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| penetration-tester | Pilot only | SCEN-BASELINE-PENETRATION-TESTER | REQ-APPSEC-01 (exists; reassess baseline fit) | Drafted — anchor semantic review recommended |
| devops-sre | None | SCEN-BASELINE-DEVOPS-SRE | REQ-DEVOPS-SRE-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| performance-engineer | None | SCEN-BASELINE-PERFORMANCE-ENGINEER | REQ-PERFORMANCE-ENGINEER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| accessibility-specialist | None | SCEN-BASELINE-ACCESSIBILITY-SPECIALIST | REQ-ACCESSIBILITY-SPECIALIST-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| technical-writer-knowledge-engineer | None | SCEN-BASELINE-TECHNICAL-WRITER-KNOWLEDGE-ENGINEER | REQ-TECHNICAL-WRITER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| release-manager | None | SCEN-BASELINE-RELEASE-MANAGER | REQ-RELEASE-MANAGER-01 (drafted in role skill; pending review) | Drafted — author preflighted; independent review pending |
| delivery-lead | Pilot only | SCEN-BASELINE-DELIVERY-LEAD | REQ-DELIVERY-01 (exists; reassess baseline fit) | Drafted — anchor semantic refinement recommended |

Role names and order must remain aligned with `docs/team/expected-roles.yml`.
The scenario IDs and requirement IDs above are planning proposals, not
approved records. Do not create run records or mark a scenario approved merely
because it appears in this register.

## Baseline design gates

Complete these gates in order:

1. **Role requirement traceability**
   - Define one concise, observable role-level requirement anchor for each skill
     that does not already have one.
   - Keep requirement IDs stable and unique; add the exact HTML comment anchor
     to the canonical role skill.
   - Confirm that each scenario's `required_requirements` and every criterion's
     `requirement_ref` trace to the matching role skill.
   - Do not manufacture requirements solely to satisfy a validator; derive each
     anchor from the role's actual authority, responsibilities, and boundaries.
2. **Scenario specification**
   - Create one bounded, representative task for each of the 17 roles.
   - Use a shared fictional order-webhook product context where it helps
     cross-role comparability, but give each role a distinct deliverable and
     exclude work owned by other roles.
   - Include explicit inputs, constraints, exclusions, expected output,
     acceptance evidence, and role-specific failure/safety cases.
   - Define criterion IDs, weights totaling 100, criticality, and evidence-based
     score guidance. Keep scenario scope achievable in one agent session.
3. **Scenario design review**
   - Review all 17 drafts against the role skill, canonical ownership, activation
     rules, artifact catalog, producer-consumer boundaries, and safety policy.
   - Record design findings and revise ambiguous or unscorable criteria.
   - A design review is advisory and is not human approval.
4. **Human pre-run approval**
   - Each scenario must have `status: approved`, `approval.approved_by`, and
     `approval.approved_at` before any baseline execution.
   - The human reviewer may approve, request changes, or block each scenario.
   - Do not infer approval from a passing validator, merged PR, or another
     scenario's approval.
5. **Execution-readiness check**
   - Pin the repository base commit, each scenario revision, and each role skill
     revision before the first run in a cohort.
   - Confirm exact prompt bytes/hash, provider/model display label and version,
     agent mode, material settings, tool permissions, and environment.
   - Confirm the run-record template, evidence layout, and validation checks
     before generating any run records.

## Controlled execution protocol

For each approved scenario:

- Perform 10 independent runs, each in a fresh agent conversation and isolated
  worktree or equivalent clean checkout.
- Use the exact same approved prompt, scenario revision, role-skill revision,
  repository base commit, provider/model/version, mode, and material settings
  for all 10 runs in that scenario.
- Do not reuse previous run outputs, agent context, generated artifacts, or
  corrective hints between runs.
- Do not manually repair an agent's output before preserving it. If a correction
  is requested as part of the task, it must be part of the approved prompt and
  applied consistently to all runs.
- Preserve the complete original transcript/session export where available,
  submitted prompt, prompt SHA-256, output artifacts, tool-call behavior,
  actual `git status --short`, command output, errors, interruptions, and
  metadata. Record unavailable fields as `unknown`; never infer them.
- Keep all generated run artifacts within the designated run output directory.
  Store evidence outside the worktree or in a pre-agreed ignored location so
  evidence capture does not contaminate the measured change scope.
- Redact credentials, secrets, private customer data, and unnecessary sensitive
  content before committing evidence.

### Comparability rules

The primary baseline should use one fixed provider/model/version and one fixed
agent mode/settings profile across all 170 executions where the provider permits
it. If that cannot be maintained, split results into explicitly named
provider/model/configuration cohorts. Do not combine unlike cohorts into one
headline score or claim a controlled cross-role comparison.

Record the user-visible model label separately from the underlying model
identifier/version. A display label alone is not proof of the serving model.
Record unavailable settings as unknown rather than assuming defaults.

### Run evidence layout

Use a separate run directory for every actual execution:

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

The layout is a target convention, not a statement that these files or runs
already exist. A baseline run record must identify the exact scenario, role,
rubric, run number, UTC start time, provider/model/configuration, scenario and
skill revisions, prompt hash, output/transcript references, tool behavior,
scores, critical failures, limitations, and human review.

Formal post-run scenario reviews use the validator's existing canonical path:
`docs/reviews/scenario-<scenario-id>.yml`. Keep pre-run approval metadata and
post-run review records distinct.

## Scoring and reporting

- Score observable outcomes, not verbosity, style, or exact wording.
- Score every criterion from 0 to 100 with a concise rationale tied to specific
  evidence.
- Compute a weighted score only when all required criterion scores are present:
  `sum(score × weight) / sum(weights)`.
- Report critical failures separately. A critical failure cannot be hidden by a
  high weighted average.
- For each scenario, report all 10 run scores, per-criterion mean/range,
  weighted-score mean/range, critical failures, and evidence limitations.
- Report cross-role summaries only within a comparable provider/model/version/
  configuration cohort. Include role-level results; do not let an overall mean
  hide weak or unsafe individual roles.
- Keep the human reviewer responsible for the final pass/needs_changes/blocked
  decision. Automated validation checks structure and consistency, not model
  quality or approval.

## Requirement-anchor status

The 14 additional role anchors were merged to `main` in PR #33
(merge commit `39b2f9d725fc0fb805d855669ec8738f4b4ae809`). All 17 canonical
skills now contain a role-level anchor. Merge status is not human approval of
the requirement wording or evidence that each anchor is a good baseline
measurement target.

The anchors require a recorded role-owner/governance review for semantic fit,
including reassessment of the original Backend Developer, Penetration Tester,
and Delivery Lead anchors. The repository validator checks structural presence,
uniqueness, placement, and mapping to this register; it does not approve the
substantive requirement or scenario quality.

The repository currently has pilot run-record conventions and execution
lifecycle schemas, but no dedicated baseline run-record validator or baseline
report generator. Add and test those before large-scale evidence collection;
do not imply that the execution lifecycle validator already validates these
baseline evaluation records.

The scenario validator enforces that valid criterion weights are finite,
positive, and total exactly 100 (within a small floating-point tolerance).
A separate requirement-traceability validator checks that each canonical
role skill has exactly one unique, correctly placed anchor and that the same
ID appears in its baseline register row. These are structural checks, not
human design approval.

## Current baseline status

All 17 role-specific baseline scenario YAML drafts are present on branch `chore/stage-b-repository-health` under `tests/scenarios/SCEN-BASELINE-<ROLE>.yml`. Each draft is pinned to the audited baseline commit and has five criteria totaling 100 points. An author-side structural preflight found valid role IDs, scenario IDs, one matching requirement anchor per scenario, unique criterion IDs, complete criterion references, and valid 40-character evidence commit references. This preflight is not an independent design review or human approval. See `DESIGN-PREFLIGHT-2026-11-08.md` for role-by-role review notes and open issues.

- Planned roles: 17.
- Planned scenarios: 17.
- Scenario drafts authored: 17.
- Scenario drafts structurally preflighted: 17.
- Independent scenario design reviews completed: 0.
- Scenarios approved: 0.
- Planned runs per scenario: 10.
- Planned executions: 170.
- Baseline executions recorded: 0.
- Baseline post-run reviews: 0.

Update these counts only from committed scenario approvals, actual run evidence,
and formal review records.


## Second-pass design review — 2026-11-08

An AI-assisted second-pass review of all 17 scenario drafts is recorded in
`DESIGN-REVIEW-2026-11-08.md`. It inspected the task prompts, rubric criteria,
canonical role identity/boundary sections, artifact ownership, activation rules,
and producer-consumer relationships.

A subsequent AI-assisted design audit is recorded in
`AI-DESIGN-AUDIT-2026-11-08.md`. The user explicitly waived the independent
human design-review step for this stage. That waiver is recorded as a waiver,
not as a completed independent review. The AI audit is advisory and does not
replace the separate human pre-run approval gate.

The review identified required cross-scenario corrections before approval:
- Add the missing canonical artifact package ID and owner to each scenario.
- Connect the daily operational summary requirement to its intended consumer.
- Distinguish provider event occurrence time from receiver receipt time.
- Define duplicate delivery-attempt auditability and daily duplicate-count semantics.
- Clarify the Backend Developer rejection path without inventing domain policy.
- Complete semantic review of the Backend Developer, Penetration Tester, and
  Delivery Lead requirement anchors.
- Add criterion-specific scoring anchors and preserve the unknown delay threshold.

This AI-assisted review is not an independent human review and does not satisfy
the independent human design-review gate. Therefore:
- Independent human scenario design reviews completed: 0 (waived by user for this stage; not performed).
- AI-assisted design audit completed: 17/17; advisory only.
- Human pre-run approvals: 0/17.
- Baseline executions: 0/170.

The user reported that after pulling commit
`0ff6f9c968404489f2e83cc062531f495ff1b4f7`, the full local unit suite passed
65/65 tests, the requirement and scenario validators passed, and
`git diff --check` reported no errors. These are user-reported local results;
they are not a GitHub Actions result or an independently reproduced run.

Do not change scenario statuses or create pre-run approval metadata based on
this review. Resolve the findings, obtain the required human review and
scenario-by-scenario approval, and complete execution-readiness tooling before
starting baseline runs.


## Scenario remediation status — 2026-11-08

The second-pass findings have been addressed in the draft scenario definitions. The detailed change record is in
`DESIGN-REVIEW-2026-11-08.md`, section 8.

- All 17 scenarios now identify their canonical artifact package ID and accountable owner. Package status remains proposed; no handoffs are declared.
- Product, UX, frontend, data, and QA prompts now share a proposed support-facing daily summary contract.
- Event occurrence time (`occurred_at`) is distinguished from receiver receipt time (`received_at`).
- Delivery attempt identity (`delivery_attempt_id`) is distinguished from event identity (`event_id`) and order identity (`order_id`).
- The proposed summary counts eligible delivery attempts; accepted/rejected/duplicate are terminal-outcome subtotals and may be lower than received while attempts remain in flight. A repeat event_id is duplicate only after a durable terminal event outcome exists. Product/Operations confirmation remains required for metric inclusion and reporting timezone.
- Backend domain rejection is handled through an injected policy decision; the scenario does not authorize Backend to invent domain rules.
- All 85 criteria have absent/partial/core/complete score anchors.
- Backend Developer, Penetration Tester, and Delivery Lead requirement statements were refined while retaining their stable requirement IDs; the consolidated role-skill file and scenario evidence pins were updated.
- Delayed/not-yet-visible behavior does not use an invented numeric threshold.

The scenario validator now checks baseline artifact package ownership and the presence of all four score anchors. Unit tests were added for these checks.

**Verification is pending:** the latest remediation commit series has not yet been pulled and validated locally. The previously reported 65/65 full-suite result predates these latest changes and must not be reused as evidence for this revision.

Gate status remains:
- Draft scenarios: 17/17.
- Independent human design reviews: 0/17.
- Human pre-run approvals: 0/17.
- Baseline executions: 0/170.

Do not change scenario status to approved or start baseline runs until the latest local checks pass, remaining Product/Operations decisions are confirmed or explicitly retained as open/non-scored, an independent human review is recorded, each scenario receives human pre-run approval, and execution-readiness tooling is complete.
