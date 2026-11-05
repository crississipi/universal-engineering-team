# Order webhook validation pilot

`webhook_validation.py` exposes `normalize_order_webhook(payload)`, a pure
Python-standard-library validator for untrusted order webhook mappings. It
returns a new normalized dictionary and raises `ValueError` for invalid input.

The validator trims nonblank order IDs and SKUs, trims and lowercases email,
requires a three-letter uppercase ASCII currency, and converts supported prices
to finite, non-negative `Decimal` values without quantizing them. It accepts
only a non-empty list of item mappings with the required fields.

## Deliberate validation boundaries

- Email validation implements only the requested basic shape; it is not RFC
  validation and does not establish that an address exists or is deliverable.
- Currency validation checks shape and ASCII uppercase letters, not whether the
  code is an assigned or supported currency.
- Unknown input keys are not copied into the normalized result.
- This module does not authenticate webhook senders, make network calls, log,
  persist data, or validate business rules beyond the specified payload shape.

## Run tests

From the repository root:

```powershell
python -m unittest discover -s pilot-output -p "test_*.py" -v
```

Tests use only the Python standard library.
