# Order webhook validation pilot

This directory is a standalone, framework-independent implementation of the
approved `SCEN-BACKEND-WEBHOOK-VALIDATION` scenario. It uses only Python's
standard library and does not change or integrate with canonical repository
files.

## API

`order_webhook.validate_order_webhook(payload)` accepts an order mapping and
returns a `NormalizedOrder` dictionary. Invalid inputs raise `ValueError` with
a field path where available and a concise reason.

The normalized result contains only `order_id`, `customer_email`, `currency`,
and `items`. Each normalized item contains only `sku`, `quantity`, and
`unit_price`.

## Validation and normalization

- The order and each item must be mappings with all required fields.
- `order_id` and each `sku` must be non-empty strings after trimming.
- Email is trimmed and lowercased; validity is limited to the scenario's
  stated shape: one `@`, non-empty local and domain parts, no whitespace, and
  at least one period in the domain. This is not RFC validation.
- Currency must already be exactly three uppercase ASCII letters.
- `items` must be a non-empty list. Item quantities must be positive integers;
  booleans are rejected even though Python treats them as integers.
- Prices accept only strings, integers, floats, or `Decimal` values.
  Booleans and other types are rejected. Floats are parsed through their string
  representation. Prices must parse as finite, non-negative `Decimal` values;
  precision and scale are preserved without quantization.
- Unrecognized input fields are ignored and are not copied into the result.

The function performs no network, database, authentication, logging, or
persistence operations.

## Tests

Run from the repository root with Python 3:

```powershell
python -m unittest discover -s evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-2/pilot-output -p "test_order_webhook.py"```

The tests cover valid normalization and supported price types; invalid order
and item mappings; missing and blank fields; the defined email and currency
rules; item collection shape; positive-integer quantity rules; and invalid,
negative, non-finite, boolean, or unsupported prices.

## Repository and documentation boundary

Repository discovery shows this is a stack-agnostic engineering-team skills
and governance package with Python validation scripts and tests. The pilot is
isolated test output, not an integrated service. Per the task constraint, no
canonical project files were modified; the repository's Obsidian notes,
Graphify graph, and central HTML report were not updated.

## Assumptions and limitations

- The normalized structure is a typed dictionary because the scenario does
  not prescribe a serialization or model framework.
- Validation follows only the deliberately limited email rule in the task;
  it does not establish mailbox existence or broader email validity.
- The caller remains responsible for any webhook authentication, transport
  limits, persistence, or application-specific handling outside this pure
  validator.
