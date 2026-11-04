# Run 2 evidence summary

Run 2 produced order_webhook.py, test_order_webhook.py, and README.md. validate_order_webhook accepts a Mapping and returns a typed dictionary; invalid inputs raise ValueError. It validates required fields, basic email shape, uppercase ASCII currency, non-empty item mappings, positive non-bool integer quantities, and permitted price types. Prices are parsed through Decimal (float via str), finite and non-negative, without quantization. Standard library only; no external side effects. Focused tests cover positive and negative cases including unsupported and non-finite prices. Syntax check passed. The full original Copilot conversation was not supplied; transcript is a summary.

## Files reported as created

- `pilot-output/order_webhook.py`
- `pilot-output/test_order_webhook.py`
- `pilot-output/README.md`

## Test command and reported result

```text
python -m unittest discover -s pilot-output -p test_order_webhook.py
17 tests, OK (0.005s). python -m compileall -q pilot-output exited 0 with no output. Test-first attempt before implementation failed with ModuleNotFoundError, as expected. Full repository suite, linting, and static type checking were not run.
```

## Evidence provenance

The original code, tests, and README files are preserved in the user-supplied evidence archive
(`backend-pilot-evidence.zip`, SHA-256: `336588aad5dc3bc55ece2a7bb2da9f249b7491b1d95301d55abc45846442a5a0`). The archive itself is not embedded
in this repository. The exact prompt is committed at
`evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/prompt-used.md`.
