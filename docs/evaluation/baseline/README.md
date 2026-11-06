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
actual ownership boundary. Scenario IDs are proposed identifiers until the
scenario files exist and receive human pre-run approval.

| Canonical role | Pilot coverage | Baseline scenario ID (proposed) | Role requirement anchor | Design state |
|---|---|---|---|---|
| product-analyst | None | SCEN-BASELINE-PRODUCT-ANALYST | REQ-PRODUCT-ANALYST-01 (drafted in role skill; pending review) | Not designed |
| solution-architect | None | SCEN-BASELINE-SOLUTION-ARCHITECT | REQ-SOLUTION-ARCHITECT-01 (drafted in role skill; pending review) | Not designed |
| api-manager | None | SCEN-BASELINE-API-MANAGER | REQ-API-MANAGER-01 (drafted in role skill; pending review) | Not designed |
| backend-developer | Pilot only | SCEN-BASELINE-BACKEND-DEVELOPER | REQ-BACKEND-01 (exists; reassess baseline fit) | Not designed |
| frontend-developer | None | SCEN-BASELINE-FRONTEND-DEVELOPER | REQ-FRONTEND-DEVELOPER-01 (drafted in role skill; pending review) | Not designed |
| ux-ui-designer | None | SCEN-BASELINE-UX-UI-DESIGNER | REQ-UX-UI-DESIGNER-01 (drafted in role skill; pending review) | Not designed |
| database-manager | None | SCEN-BASELINE-DATABASE-MANAGER | REQ-DATABASE-MANAGER-01 (drafted in role skill; pending review) | Not designed |
| integration-engineer | None | SCEN-BASELINE-INTEGRATION-ENGINEER | REQ-INTEGRATION-ENGINEER-01 (drafted in role skill; pending review) | Not designed |
| data-engineer | None | SCEN-BASELINE-DATA-ENGINEER | REQ-DATA-ENGINEER-01 (drafted in role skill; pending review) | Not designed |
| qa-manager | None | SCEN-BASELINE-QA-MANAGER | REQ-QA-MANAGER-01 (drafted in role skill; pending review) | Not designed |
| penetration-tester | Pilot only | SCEN-BASELINE-PENETRATION-TESTER | REQ-APPSEC-01 (exists; reassess baseline fit) | Not designed |
| devops-sre | None | SCEN-BASELINE-DEVOPS-SRE | REQ-DEVOPS-SRE-01 (drafted in role skill; pending review) | Not designed |
| performance-engineer | None | SCEN-BASELINE-PERFORMANCE-ENGINEER | REQ-PERFORMANCE-ENGINEER-01 (drafted in role skill; pending review) | Not designed |
| accessibility-specialist | None | SCEN-BASELINE-ACCESSIBILITY-SPECIALIST | REQ-ACCESSIBILITY-SPECIALIST-01 (drafted in role skill; pending review) | Not designed |
| technical-writer-knowledge-engineer | None | SCEN-BASELINE-TECHNICAL-WRITER-KNOWLEDGE-ENGINEER | REQ-TECHNICAL-WRITER-01 (drafted in role skill; pending review) | Not designed |
| release-manager | None | SCEN-BASELINE-RELEASE-MANAGER | REQ-RELEASE-MANAGER-01 (drafted in role skill; pending review) | Not designed |
| delivery-lead | Pilot only | SCEN-BASELINE-DELIVERY-LEAD | REQ-DELIVERY-01 (exists; reassess baseline fit) | Not designed |

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

## Known repository readiness gap

At the start of Stage B, only the Backend Developer, Penetration Tester, and
Delivery Lead skills contained explicit requirement anchors. This branch adds
one draft role-level anchor to each of the other 14 canonical skills. These
anchors remain pending review and repository validation; they are not scenario
approvals. The traceability gate is not complete until the anchors are reviewed,
merged, and validated against scenario requirements and criterion references.

The repository currently has pilot run-record conventions and execution
lifecycle schemas, but no dedicated baseline run-record validator or baseline
report generator. Add and test those before large-scale evidence collection;
do not imply that the execution lifecycle validator already validates these
baseline evaluation records.

## Current baseline status

- Planned roles: 17.
- Planned scenarios: 17.
- Scenarios designed: 0.
- Scenarios approved: 0.
- Planned runs per scenario: 10.
- Planned executions: 170.
- Baseline executions recorded: 0.
- Baseline post-run reviews: 0.

Update these counts only from committed scenario approvals, actual run evidence,
and formal review records.
