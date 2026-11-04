# Pilot evaluation execution guide

This directory documents the pilot workflow. It does not contain completed
model runs. No provider calls or evaluation results are created by repository
validation.

## Scenarios

The pilot contains one scenario for each of the three methodology roles:

- `SCEN-BACKEND-WEBHOOK-VALIDATION`
- `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`
- `SCEN-DELIVERY-CROSSROLE-WEBHOOK`

The current scenario rubric version is `pilot-v2`. A scenario is eligible for
execution only after human approval is recorded in its scenario file.

## Execution matrix

| Scenario | Role | Required runs | Recorded runs |
|---|---|---:|---:|
| SCEN-BACKEND-WEBHOOK-VALIDATION | backend-developer | 3 | 3 |
| SCEN-APPSEC-STATIC-WEBHOOK-REVIEW | penetration-tester | 3 | 0 |
| SCEN-DELIVERY-CROSSROLE-WEBHOOK | delivery-lead | 3 | 0 |
| **Total** | | **9** | **3** |

## Backend Developer pilot evidence

Three GitHub Copilot Agent-mode runs were reported for the approved Backend
Developer scenario. Run records and prompt/transcript summaries are committed
under `evaluations/pilot/`.

The exact submitted prompt is stored at
`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`.
Its SHA-256 is
`c4dd687677a7ae8ab92d1870d001e60b7cc5fb98b14481a33d821b74076efe2c`.

The evidence archive supplied for review was
`backend-pilot-evidence.zip` (SHA-256:
`336588aad5dc3bc55ece2a7bb2da9f249b7491b1d95301d55abc45846442a5a0`). Its
implementation, test, and README files are referenced by the run records but
the archive bytes are not committed to this repository. The transcript files
are summaries, not full original Copilot conversation exports.

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

Criterion scores remain null pending human post-run scoring. No scenario-level
post-run decision has been made. The evidence review did not identify a
critical implementation defect, but this is not a final `pass` decision.

## Review and reporting

After all three runs for a scenario are reviewed, create
`docs/reviews/scenario-<scenario-id>.yml` with a human decision of
`pass`, `needs_changes`, or `blocked`. This is separate from pre-run
scenario approval.

Do not calculate weighted scores while required criterion scores are missing.
Do not treat pilot results as the repository-wide baseline.
