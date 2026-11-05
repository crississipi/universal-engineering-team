# Run 3 evidence summary

Run 3 produced webhook_validation.py, test_webhook_validation.py, and README.md. validate_order_webhook returns frozen OrderWebhook and OrderItem dataclasses; invalid inputs raise ValueError. It validates and normalizes order ID, SKU, email, currency, item mappings, quantities, and finite non-negative Decimal prices. Standard library only; no network/database/logging/authentication/persistence. Focused tests cover valid normalization, missing fields, malformed email/currency, invalid collections, blank identifiers, invalid quantities, and boolean/unsupported/negative/malformed/non-finite prices. Reported git status was only ?? pilot-output/. No linter/type checker/build. Full conversation was not supplied; transcript is a summary.

## Files reported as created

- `pilot-output/webhook_validation.py`
- `pilot-output/test_webhook_validation.py`
- `pilot-output/README.md`

## Test command and reported result

```text
python -m unittest discover -s pilot-output -p "test_*.py" -q
20 tests, OK (0.005s). Repository suite: 40 tests attempted; 2 import errors because jsonschema was unavailable (no packages installed).
```

## Evidence provenance

The original code, tests, and README files are preserved in the user-supplied evidence archive
(`backend-pilot-evidence.zip`, SHA-256: `336588aad5dc3bc55ece2a7bb2da9f249b7491b1d95301d55abc45846442a5a0`). The archive itself is not embedded
in this repository. The exact prompt is committed at
`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`.
