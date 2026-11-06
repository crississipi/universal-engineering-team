# Skill evaluation methodology

## Purpose

Evaluate whether role skills produce useful, correct, safe, and verifiable work.
Evaluation is rubric-based. It must not depend on exact wording or exact output
matching.

## Evaluation layers

1. Repository validation
   - Skill metadata and expected role inventory.
   - Ownership and handoff manifest structure.
   - Scenario and review-record structure.
   - Requirement anchor presence and scenario-to-skill traceability.
   - Generated instruction consistency.
2. Scenario evaluation
   - Run representative tasks using the target agent/provider.
   - Capture outputs, tool behavior, and evidence.
   - Score outputs against explicit criteria.
   - Record provider, model, version, configuration, and run number.
3. Human review
   - Review scenario specifications before execution and approve or return them
     for changes.
   - Review run outputs for correctness, completeness, safety, usefulness, and
     evidence quality.
   - Resolve ambiguous rubric outcomes.
   - Record disagreements and limitations.

Automated repository checks must not make paid model calls.

## Stage A — Pilot

Pilot scope:

- 3 roles.
- 1 representative scenario per role.
- 3 runs per scenario.
- 9 total executions.

Pilot roles:

- `backend-developer`
- `penetration-tester`
- `delivery-lead`

The pilot scenario specifications are stored in `tests/scenarios/`. They begin
with `status: draft`. A human must review each scenario before execution and
change it to `status: approved`, recording `approval.approved_by` and
`approval.approved_at`. Approval is a pre-run scenario-design decision; it is
not a model-run result.

Each run must have its own record based on
`docs/templates/pilot-run-record.template.yml`. Keep the actual prompt,
provider/model/version, non-secret configuration, run number, timestamp, skill
revision, output/evidence references, criterion scores, critical failures, and
limitations. Do not store API keys, credentials, private customer data, or
unnecessary sensitive content in evaluation records.

After the runs, create the scenario's post-run review record at the path named by
`review_record` in the scenario. This record captures the human review decision
(`pass`, `needs_changes`, or `blocked`), reviewer, and number of runs reviewed.
It is separate from the pre-run scenario approval metadata.

Pilot objectives:

- Verify that the scenario format is practical.
- Identify ambiguous or unscorable criteria.
- Measure run-to-run variation.
- Check whether evidence can be reproduced.
- Identify false positives in automated validation.
- Refine the rubric before establishing a baseline.

Do not treat pilot results as the repository-wide baseline. The pilot's 9
executions and three post-run decisions remain a separate historical sample.

## Stage B — Repository-wide baseline

The baseline is a new, controlled evaluation cohort; it must not reuse pilot run
records or count pilot executions toward the baseline sample.

- Evaluate all 17 canonical roles from `docs/team/expected-roles.yml`.
- Design one bounded, representative scenario per role.
- Obtain explicit human pre-run approval for every scenario.
- Execute 10 independent runs per approved scenario.
- The initial planned sample is 17 scenarios × 10 runs = 170 executions.
- If a role needs multiple scenarios, state the expanded sample size and approve
  each additional scenario before execution.

The baseline execution protocol, scenario register, evidence layout,
comparability rules, readiness gaps, and status counts are maintained in
`docs/evaluation/baseline/README.md`.

### Baseline readiness gates

1. Establish a role-specific requirement anchor in every canonical skill and
   trace each scenario requirement and criterion to that anchor. Do not create
   requirement IDs that are not grounded in the role's actual responsibilities.
2. Draft all 17 scenarios with explicit task scope, inputs, exclusions,
   deliverables, acceptance evidence, criteria, weights, and criticality.
3. Complete a design review against canonical skills, ownership, activation,
   responsibility boundaries, and safety constraints.
4. Obtain individual human approval for every scenario. A passing validator,
   merged pull request, or approval of another scenario is not sufficient.
5. Pin the base commit, scenario and skill revisions, prompt hash, provider,
   model/version, mode, and material settings before the first run.
6. Validate the evidence layout and baseline run-record validation/reporting
   tooling before executing the 170-run cohort.

### Independence and comparability

Each run must use a fresh agent conversation and isolated clean worktree or
equivalent checkout. Do not reuse prior run context, outputs, or corrective
hints. Keep prompt, scenario, skill revision, base commit, provider/model/version,
mode, and material settings stable within a scenario's 10-run cohort.

Use one fixed provider/model/version/configuration cohort across roles where
possible. If this cannot be maintained, separate results into explicit cohorts
and do not publish a combined headline score as though the runs were equivalent.
Record the user-visible model label separately from the underlying model
identifier/version. Record unavailable metadata as unknown; do not infer it.

Preserve the submitted prompt and SHA-256, complete transcript/session export
where available, generated artifacts, actual Git status, command outputs, tool
behavior, errors, interruptions, and metadata. Redact secrets and private data.
Do not manually repair output before preserving original evidence.

### Baseline records and review

Keep baseline evidence and records separate from `evaluations/pilot/`:

- Evidence: `evaluations/baseline/evidence/<scenario-id>/run-<n>/`.
- Run records: `evaluations/baseline/runs/<scenario-id>-run-<n>.yml`.
- Post-run reviews: `docs/reviews/scenario-<scenario-id>.yml`.

Use the existing pilot run-record template as a field reference only; baseline
records must identify their baseline track and approved baseline rubric. Add a
dedicated baseline record validator and report generator before large-scale
collection. The existing `scripts/validate-execution.py` validates operational
execution records under `executions/`; it does not validate baseline evaluation
run records.

## Stage C — Regression evaluation

Re-run affected scenarios after material skill changes.

Compare against the approved baseline using the same evaluation method wherever
possible. If the provider, model, tokenizer, rubric, scenario, or material
settings change, identify the change and avoid presenting the results as a
directly equivalent comparison.

## Rubric principles

Score observable outcomes, not stylistic similarity.

Recommended dimensions:

- Requirement understanding.
- Technical correctness.
- Scope control.
- Security and safety.
- Collaboration and handoff quality.
- Verification evidence.
- Documentation quality.

Each scenario defines criterion weights and criticality. Score each criterion
from 0 to 100 and retain a concise evidence-based rationale. Compute the
weighted score as the sum of each criterion score multiplied by its weight,
divided by the sum of criterion weights. Report critical failures separately;
a critical failure must not be hidden by a high average score. Do not calculate
an aggregate when required criterion scores are missing.

## Token measurements

Token counts are monitoring signals, not quality scores.

- Record the tokenizer and measurement method.
- Compare like-for-like measurements.
- Do not claim a universal token count across providers.
- Use baseline-relative changes.
- Do not impose hard token limits until observed size variation and false
  positives have been reviewed.

## Reporting

Every evaluation report must state:

- Scenarios and skill versions evaluated.
- Provider/model/configuration cohort.
- Run count and date.
- Rubric version.
- Per-criterion and aggregate scores, variation, and critical failures.
- Evidence locations.
- Limitations and unresolved questions.

Never claim an evaluation was performed unless its run records and evidence exist.
