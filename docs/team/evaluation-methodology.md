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

Do not treat pilot results as the repository-wide baseline.

## Stage B — Baseline

After the pilot rubric is reviewed:

- Evaluate all 17 roles.
- Use 10 runs per role/scenario.
- Keep scenario inputs and evaluation settings stable within a comparison.
- Record the exact provider, model, model version, and relevant settings.
- Report per-criterion scores, aggregate scores, variation, and failures.

The initial planned baseline therefore contains 170 executions if each role
has one approved representative scenario.

If a role requires multiple scenarios, report the expanded sample size explicitly.

## Stage C — Regression evaluation

Re-run affected scenarios after material skill changes.

Compare against the approved baseline using the same evaluation method wherever
possible. If the provider, model, tokenizer, or scoring rubric changes, identify
the change and avoid presenting the results as a directly equivalent comparison.

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
- Provider/model/configuration.
- Run count and date.
- Rubric version.
- Per-criterion and aggregate scores, variation, and critical failures.
- Evidence locations.
- Limitations and unresolved questions.

Never claim an evaluation was performed unless its run records and evidence exist.
