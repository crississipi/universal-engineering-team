# Backend Developer pilot — post-run evidence review

> **Review status: proposed; human decision pending.** This document records an independent evidence review and proposed rubric scores. It is not the final human post-run review record. The three run records remain unscored, and the scenario's `review_record` remains `null` until the reviewer approves a final decision.

## 1. Scope and evidence reviewed

- Scenario: `SCEN-BACKEND-WEBHOOK-VALIDATION`
- Role: `backend-developer`
- Rubric: `pilot-v2`
- Approved scenario revision: `a975fb3404c9da1323a7c11baa54b880204d7726`
- Backend skill evidence revision: `e86d6910b4c4fa754058d6113bc9ecf4e30da147`
- Prompt SHA-256: `c4dd687677a7ae8ab92d1870d001e60b7cc5fb98b14481a33d821b74076efe2c`
- Provider reported for all runs: GitHub Copilot, Agent mode
- Model display label reported: `GPT-6-Luna`; exact underlying model version is unknown.

Reviewed the canonical implementation, focused tests, per-run README, metadata, transcript summary, and run record for each execution under `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/` and `evaluations/pilot/runs/`.

The original Copilot conversation exports were not supplied; the committed transcript files are summaries. UTC start times, exact underlying model version, temperature, and reasoning effort remain unknown. These omissions are recorded as evidence limitations rather than inferred.

## 2. Executive findings

All three implementations satisfy the task's core functional and scope requirements on source inspection. No implementation defect or critical failure was identified in the reviewed source.

Common strengths:
- Standard-library-only, framework-independent implementations.
- Pure validation/normalization; no network, persistence, logging, authentication, or database behavior.
- Required order and item fields are checked; invalid structures raise `ValueError`.
- Identifiers are trimmed; email is trimmed/lowercased and follows the exact deliberately limited shape; currency must be three uppercase ASCII letters.
- Quantities are positive integers with booleans rejected.
- Prices accept only the requested types, reject booleans and unsupported values, parse floats through `str(value)`, and reject malformed, negative, or non-finite values without rounding or quantization.
- Unknown input fields are not copied into the normalized output.

Implementation differences are acceptable under the scenario; it does not prescribe a particular return container:
- **Run 1:** typed dictionary result, helper-based validation, `normalize_order_webhook`.
- **Run 2:** typed dictionary result, field-path error messages, `validate_order_webhook`.
- **Run 3:** frozen dataclasses and tuple items, `validate_order_webhook`. This gives the returned structure stronger immutability, but is not inherently more correct for this scenario.

Do not force the three implementations to converge solely for stylistic consistency.

## 3. Focused test and requirement coverage

The table assesses the committed test source, not just the reported test counts. “Covered” means there is an explicit focused test for the stated behavior. Source code may correctly handle a case even where its test is absent.

| Requirement / boundary | Run 1 | Run 2 | Run 3 | Review note |
|---|---|---|---|---|
| Valid payload and normalized output | Covered | Covered | Covered | All assert normalized values and Decimal precision/scale. |
| Missing order and item fields | Covered | Covered | Covered | Each tests required-field rejection. |
| Non-mapping order and item values | Covered | Covered | Covered | Run 1 and Run 2 include several invalid order shapes; all cover invalid item values. |
| Blank order ID and SKU | Covered | Covered | Covered | All reject whitespace-only identifiers. |
| Non-string order ID, email, and SKU | Not explicit | Covered | Not explicit | Run 2 has direct non-string cases for all three. Runs 1 and 3 reject these in implementation, but do not assert each boundary directly. |
| Defined basic email rule | Covered | Covered | Covered | The rule is intentionally not full RFC validation. Run 2 explicitly tests non-string email. |
| Uppercase ASCII currency | Covered | Covered | Covered | Invalid case, length, whitespace, and/or non-ASCII cases are present. |
| Non-empty list and mapping items | Covered | Covered | Covered | Invalid empty/non-list collections and invalid item values are tested. |
| Positive integer quantity; bool, zero, negative, non-integer rejection | Covered | Covered | Covered | Run 3 includes boolean and non-integer cases. |
| Bool and unsupported price types | Covered | Covered | Partial | Run 3 explicitly tests `True`; implementation rejects both booleans. Runs 1 and 2 test both `True` and `False`. |
| Supported price types and no rounding | Covered | Covered | Covered | All exercise string, int, float, and Decimal input. |
| Negative and malformed prices | Covered | Covered | Covered | Negative values and malformed/blank decimal strings are asserted. |
| Non-finite positive and negative prices | Covered | Partial | Partial | Run 1 explicitly tests float negative infinity as well as string negative infinity. Runs 2 and 3 test string `-Infinity`, float NaN/+Infinity, and Decimal NaN/+Infinity, but omit explicit float `-inf` and Decimal `-Infinity` cases. Their implementations reject these via `is_finite()`. |
| No prohibited side effects / scope expansion | Source-reviewed | Source-reviewed | Source-reviewed | No prohibited behavior found in the implementation files. |

### Test execution evidence

| Run | Focused tests reported | Additional reported check | Repository-wide test attempt |
|---|---:|---|---|
| 1 | 17 passed | None reported for type/lint checks | 40 attempted; 2 import errors because `jsonschema` was unavailable |
| 2 | 17 passed | `python -m compileall -q pilot-output` exited 0; initial test-first import failure occurred before implementation | Not run |
| 3 | 20 passed | Reported `git status --short` showed only `?? pilot-output/` | 40 attempted; 2 import errors because `jsonschema` was unavailable |

The focused tests were independently reproduced against the user-supplied evidence archive before relocation: 17, 17, and 20 passed respectively; `compileall` exited 0 for all three artifacts. These are independent checks of the uploaded archive, not a post-relocation test run. The relocation PR did not change source or test contents. No linter, static type checker, or integration test result is available.

## 4. Proposed criterion scores

These are **review recommendations**, not final scores. They use the scenario's weights and the common anchors in the pilot guide. The run-record score fields are intentionally left `null` pending human approval.

| Criterion (weight) | Run 1 | Run 2 | Run 3 | Rationale |
|---|---:|---:|---:|---|
| SCOPE-CONTROL (15) | 100 | 100 | 100 | All implementations remain pure, small, typed, standard-library-only validators with no prohibited side effects or unrelated abstractions. |
| INPUT-VALIDATION (20) | 95 | 100 | 95 | Run 2 has the strongest explicit test evidence for non-string identifiers/email/SKU. Runs 1 and 3 implement the type checks correctly but do not directly test all those input-type boundaries. |
| NUMERIC-SAFETY (20) | 100 | 95 | 95 | All implementations correctly enforce the numeric rules. Runs 2 and 3 omit explicit float negative-infinity and Decimal negative-infinity test cases; Run 1 explicitly covers float negative infinity. |
| NORMALIZATION (10) | 100 | 100 | 100 | All apply the requested trimming, email lowercasing, currency constraint, and exact Decimal preservation without rounding. |
| TEST-COVERAGE (20) | 98 | 95 | 90 | Run 1 covers the enumerated scenario cases and most additional boundaries; Run 2 has strong identifier coverage but misses some non-finite type variants; Run 3 has the same non-finite variants plus fewer direct non-string/bool-price assertions. |
| EVIDENCE-AND-ACCURACY (15) | 90 | 95 | 95 | All report limitations honestly. Run 1 has no independently supplied repository-scope status output; Run 2 records compileall and the expected test-first failure; Run 3 records repository-scope status. All lack full conversation exports and exact model/configuration metadata. |

Weighted scores (using the scenario formula):

| Run | Proposed weighted score |
|---|---:|
| 1 | 97.10 / 100 |
| 2 | 97.25 / 100 |
| 3 | 95.25 / 100 |
| **Mean** | **96.53 / 100** |
| **Range** | **2.00 points** |

The small numeric range is descriptive only. With the exact underlying model version and several configuration values unknown, these runs should not be presented as a controlled model-version benchmark or as proof of general performance across providers.

## 5. Follow-up test improvements

These are proportionate test-strengthening actions, not confirmed implementation defects:

1. Add direct non-string `order_id`, `customer_email`, and `sku` cases to Runs 1 and 3's *separate regression suite*.
2. Add explicit `float("-inf")` and `Decimal("-Infinity")` price cases to Runs 2 and 3's *separate regression suite*.
3. Add `False` to Run 3's boolean-price cases for symmetry with Run 1 and Run 2.
4. Keep original pilot artifacts immutable. Do not edit the submitted run outputs to make them appear to have contained later-added tests.

A shared regression suite can be added later to verify these edge cases against all three implementations, using small adapters for their different public function names and return types. That suite should be labeled as a post-run review check, not part of the original Copilot runs.

## 6. Proposed post-run decision

**Proposed decision: `pass`, subject to human review and approval.**

Reasoning:
- No critical implementation defect was found.
- All three implementations meet the core functional behavior on source inspection.
- All three focused test suites were reported and independently reproduced as passing against the submitted archive.
- The identified issues are test-evidence gaps for additional boundary variants, not observed implementation failures.
- The repository-wide test errors in Runs 1 and 3 are attributable in the supplied records to the unavailable `jsonschema` dependency; Run 2 did not claim a repository-wide test run. No dependency was installed in violation of the task constraints.

This recommendation does not constitute the formal scenario decision. A human reviewer should confirm or change the proposed scores and decision. Until that happens:
- Keep all three run-record score values and review fields unchanged (`null`).
- Keep `review_record: null` in the scenario.
- Do not count this proposed report as a completed post-run review.

## 7. Evidence paths

- Scenario: `tests/scenarios/SCEN-BACKEND-WEBHOOK-VALIDATION.yml`
- Skill: `skills/backend-developer/SKILL.md`
- Prompt: `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`
- Run 1: `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-1/`
- Run 2: `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-2/`
- Run 3: `evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-3/`
- Run records: `evaluations/pilot/runs/SCEN-BACKEND-WEBHOOK-VALIDATION-run-{1,2,3}.yml`
