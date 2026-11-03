# Pilot evaluation execution guide

This directory documents the pilot workflow. It does not contain completed
model runs. No provider calls or evaluation results are created by repository
validation.

## Scenarios

The pilot contains one draft scenario for each of the three methodology roles:

- `SCEN-BACKEND-WEBHOOK-VALIDATION`
- `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`
- `SCEN-DELIVERY-CROSSROLE-WEBHOOK`

The current scenario rubric version is `pilot-v2`. Review each prompt and its
criteria before running it. A scenario is eligible for execution only after a
human reviewer changes its status to `approved` and records
`approval.approved_by` and `approval.approved_at`. Do not mark a scenario
approved merely because its YAML validates or because an automated design review
recommends approval.

The three scenarios received a design review recorded in
`docs/reviews/pilot-scenario-design-review.md`. That review is advisory and
does not substitute for the required human approval.

## Execution matrix

| Scenario | Role | Required runs |
|---|---|---:|
| SCEN-BACKEND-WEBHOOK-VALIDATION | backend-developer | 3 |
| SCEN-APPSEC-STATIC-WEBHOOK-REVIEW | penetration-tester | 3 |
| SCEN-DELIVERY-CROSSROLE-WEBHOOK | delivery-lead | 3 |
| **Total** | | **9** |

For each run:

1. Use the approved scenario prompt without silently changing its requirements.
2. Load the matching canonical role skill and record its exact commit.
3. Record the provider, exact model and version, relevant settings, and UTC
   start time.
4. Preserve the prompt hash, output/transcript reference, generated artifacts,
   tool behavior, and any interruption.
5. Score every scenario criterion from 0 to 100 with a concise rationale tied
   to observable output/evidence. Use these common anchors: 0 = absent or
   directly contradicted; 25 = major omissions or unsafe handling; 50 = partial
   completion with material gaps; 75 = substantially meets the criterion with
   limited omissions; 100 = fully meets the criterion with clear evidence.
   Use intermediate scores only with a specific evidence-based explanation.
6. Record critical failures separately. Do not let a weighted average hide one.
7. Redact secrets, credentials, private customer data, and unnecessary
   sensitive content before storing evidence.

Copy `docs/templates/pilot-run-record.template.yml` to
`evaluations/pilot/runs/<scenario-id>-run-<n>.yml` for each actual execution.
Use a separate record for each of the nine runs. Do not create placeholder run
records to make the count appear complete.

## Review and reporting

After all three runs for a scenario are reviewed, create
`docs/reviews/scenario-<scenario-id>.yml` with:

```yaml
scenario_id: SCEN-REPLACE-WITH-SCENARIO-ID
decision: pass
reviewer: HUMAN-REVIEWER
runs: 3
```

Use only `pass`, `needs_changes`, or `blocked` for the decision. The
review record is a post-run evaluation review; it is not the pre-run scenario
approval. Set the scenario's `review_record` field to that exact path when
the review record exists.

Report results per scenario and across the pilot: per-criterion scores,
weighted score, run-to-run range/variation, critical failures, evidence paths,
provider/model/configuration, and limitations. The weighted score is:

`sum(criterion score × criterion weight) / sum(criterion weights)`

Do not calculate an aggregate for a run with missing criterion scores. State
the rubric version and do not compare runs as equivalent when provider, model,
version, or material settings differ.

## Current status

- Scenario specifications: reviewed as designs, rubric version `pilot-v2`,
  still draft and awaiting human approval.
- Model executions: 0 of 9 recorded.
- Post-run scenario reviews: 0 of 3 recorded.
- Evaluation conclusions: none.

These counts describe repository records only. They must be updated from actual
evidence, never inferred from planned work.
