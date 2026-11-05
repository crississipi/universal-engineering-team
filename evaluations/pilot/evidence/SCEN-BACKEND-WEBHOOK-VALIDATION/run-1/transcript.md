# Run 1 evidence summary

Run 1 produced webhook_validation.py, test_webhook_validation.py, and README.md. normalize_order_webhook returns a typed normalized structure; invalid inputs raise ValueError. It trims order IDs/SKUs, trims and lowercases email, enforces the specified basic email shape and uppercase ASCII currency, and parses allowed prices to finite non-negative Decimal without rounding. Tests cover valid input, missing fields, malformed email/currency, invalid collections/items, boolean/non-positive quantities, and supported/unsupported, negative, malformed, and non-finite prices. Python 3.11.9. No type checker, linter, or integration test. Full repository test attempt had two import errors due to missing jsonschema. Transcript supplied is a run summary, not a full original Copilot conversation export.

## Files reported as created

- `pilot-output/webhook_validation.py`
- `pilot-output/test_webhook_validation.py`
- `pilot-output/README.md`

## Test command and reported result

```text
python -m unittest discover -s pilot-output -p "test_*.py"
17 tests, OK (0.005s). Repository suite: 40 tests attempted; 2 import errors because jsonschema was unavailable (no packages installed).
```

## Evidence provenance

The original code, tests, and README files are preserved in the user-supplied evidence archive
(`backend-pilot-evidence.zip`, SHA-256: `336588aad5dc3bc55ece2a7bb2da9f249b7491b1d95301d55abc45846442a5a0`). The archive itself is not embedded
in this repository. The exact prompt is committed at
`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`.
