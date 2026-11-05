1. Files created
All changes are confined to pilot-output/; the pre-existing untracked pilot-output.zip was left untouched.

webhook_validation.py — typed, framework-independent validator and normalizer.
test_webhook_validation.py — focused standard-library tests.
README.md — usage and validation boundaries.
2–3. Implementation and behavior
normalize_order_webhook(payload) returns a new typed structure and raises ValueError for invalid input. It trims order IDs and SKUs, trims and lowercases email, requires exactly three uppercase ASCII currency letters, and converts accepted prices to finite, non-negative Decimal values without rounding. Boolean quantities and prices are rejected.

Validation is limited to the requested email shape—not full RFC validation or deliverability—and currency shape, not whether a code is assigned. Unknown input keys are omitted from the result. The function performs no network, authentication, logging, or persistence operations.

4–5. Tests and results
The 17 tests cover valid normalization; missing fields; malformed email; non-mapping payloads/items; empty or non-list items; boolean, zero, negative, and non-integer quantities; supported and unsupported price types; negative, malformed, and non-finite prices; and malformed currencies.

Focused command and actual output:
python -m unittest discover -s pilot-output -p "test_*.py"

.................
----------------------------------------------------------------------
Ran 17 tests in 0.005s

OK

The repository suite was also attempted:
python -m unittest discover -s tests -p "test_*.py"

Ran 40 tests in 0.849s
FAILED (errors=2)

The two import errors were caused by missing jsonschema in test_validate_execution and test_validate_manifest. I did not install packages, per the constraint.

6–7. Limitations and decisions
No type checker, linter, or integration test was run. The implementation was exercised on Python 3.11.9; no broader version-support claim is made. It uses only the standard library and does not contact external services.

Invalid inputs consistently raise ValueError; extra input fields are ignored in the returned structure. Documentation is included in the pilot README. Canonical project-context, Graphify, Obsidian, and central-report files were not changed, respecting the output-only constraint.