# Pilot evaluation execution guide

This directory documents the pilot workflow. No provider calls or evaluation
results are created by repository validation.

## Scenarios

The pilot contains one scenario for each of the three methodology roles:

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

| Scenario | Role | Required runs | Recorded runs |
|---|---|---:|---:|
| SCEN-BACKEND-WEBHOOK-VALIDATION | backend-developer | 3 | 3 |
| SCEN-APPSEC-STATIC-WEBHOOK-REVIEW | penetration-tester | 3 | 3 |
| SCEN-DELIVERY-CROSSROLE-WEBHOOK | delivery-lead | 3 | 3 |
| **Total** | | **9** | **3** |

For each run:

1. Use the approved scenario prompt without silently changing its requirements.
2. Load the matching canonical role skill and record its exact commit.
3. Record the provider, exact model and version, relevant settings, and UTC
   start time. If unavailable, record unknown; do not infer it.
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

## Remaining pilot execution prompts

The two remaining approved scenarios have exact reusable run prompts committed
at:

- `evaluations/pilot/evidence/SCEN-APPSEC-STATIC-WEBHOOK-REVIEW/prompt-used.md`
- `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md`

For each scenario, start three independent fresh GitHub Copilot Agent
conversations. Submit the corresponding prompt unchanged. Keep provider, model,
mode, and material settings stable across the three runs for that scenario;
record actual values and preserve unknowns rather than guessing. Do not reuse
prior run outputs or context. Preserve the complete conversation export,
`pilot-output/` artifacts, and actual `git status --short` output for each
run before making any manual changes.

The Penetration Tester prompt is strictly static/documentation-only. The
Delivery Lead prompt is strictly planning/orchestration-only. Do not create run
records until the corresponding executions have actually occurred and their
evidence is available.

## Backend Developer pilot evidence

Three GitHub Copilot Agent-mode runs were reported for the approved Backend
Developer scenario. Run records and prompt/transcript summaries are committed
under `evaluations/pilot/`.

The exact submitted prompt is stored at
`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`.
Its SHA-256 is
`c4dd687677a7ae8ab92d1870d001e60b7cc5fb98b14481a33d821b74076efe2c`.

The implementation, focused tests, and per-run README files are committed
under `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-<n>/pilot-output/`.
The run-level `README.md`, `metadata.md`, and `transcript.md` files sit beside
each `pilot-output/` directory. The original files were moved from the temporary
root-level `backend-pilot-evidence/` directory into this canonical evidence
location without changing their contents. The transcript files are summaries,
not full original Copilot conversation exports.

All three run records preserve unavailable metadata as unknown:
- UTC start timestamps were not captured.
- The exact underlying model version was not captured; `GPT-6-Luna` is the
  reported display label.
- Temperature and reasoning effort were not captured.

Focused tests reported by the runs were independently reproduced against the
uploaded archive during evidence review: 17, 17, and 20 tests passed
respectively. These are artifact verification results, not proof that every
repository check passed. Runs 1 and 3 also reported a repository test attempt
with 40 tests and two import errors because `jsonschema` was unavailable.
Run 2 did not report a repository-wide test run.

The evidence-based review proposal is retained at
`docs/reviews/backend-developer-pilot-review.md` as the detailed analysis.
Following explicit human approval, the formal post-run decision is recorded at
`docs/reviews/scenario-SCEN-BACKEND-WEBHOOK-VALIDATION.yml`. The approved
decision is `pass`; the three run records contain the approved criterion
scores, weighted scores, reviewer, and review date. The scenario's
`review_record` points to the formal record. Original implementation,
test, metadata, and transcript-summary evidence remains unchanged.

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

- Scenario specifications: rubric version `pilot-v2`.
  - `SCEN-BACKEND-WEBHOOK-VALIDATION`: approved by `crississipi` on
    2026-11-03T15:10:45Z.
  - `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`: approved by `crississipi` on
    2026-11-06T03:55:05Z.
  - `SCEN-DELIVERY-CROSSROLE-WEBHOOK`: approved by `crississipi` on
    2026-11-06T03:55:05Z.
- Model executions: 9 of 9 recorded.
- Post-run scenario reviews: 3 of 3 formally recorded.
  - `SCEN-BACKEND-WEBHOOK-VALIDATION`: `pass`, reviewed by `crississipi`
    on 2026-11-06 (3 runs; mean weighted score 96.53/100).
  - `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`: `pass`, reviewed by `crississipi`
    on 2026-11-06 (3 runs; mean weighted score 98.57/100).
  - `SCEN-DELIVERY-CROSSROLE-WEBHOOK`: `pass`, reviewed by `crississipi`
    on 2026-11-06 (3 runs; mean weighted score 99.90/100).
- Evaluation conclusions: all three pilot scenarios are formally recorded as
  `pass`. These are pilot results, not the repository-wide 17-role baseline.

These counts describe repository records only. They must be updated from actual
evidence, never inferred from planned work.
