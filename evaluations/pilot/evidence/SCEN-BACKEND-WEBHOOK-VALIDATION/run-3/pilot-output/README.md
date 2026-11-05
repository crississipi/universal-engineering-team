# Order webhook validation

`webhook_validation.py` provides a pure, framework-independent validator. It
accepts an untrusted mapping and returns frozen `OrderWebhook` and `OrderItem`
dataclasses; invalid input raises `ValueError` with the field path.

The validator trims the order ID and SKU, trims and lowercases email, requires
currency to already be exactly three uppercase ASCII letters, and converts
accepted prices to finite, non-negative `Decimal` values without quantizing or
rounding. Float input is parsed from its string representation.

The email check intentionally implements only the requested basic shape:
exactly one `@`, non-empty local and domain parts, no whitespace, and at least
one dot in the domain. It is not full RFC validation and does not establish
deliverability. Extra mapping keys are ignored and are not included in the
normalized result. The item collection must be a non-empty `list`.

Run the focused tests from the repository root with:

```powershell
python -m unittest discover -s evaluations/pilot/evidence/SCEN-BACKEND-WEBHOOK-VALIDATION/run-3/pilot-output -p "test_*.py"
```


Focused test result:

```text
----------------------------------------------------------------------
Ran 20 tests in 0.005s

OK
```

The repository-wide `python -m unittest discover -s tests -p "test_*.py"`
suite was also attempted. Two test modules could not import because `jsonschema`
is not installed in the environment. No dependencies were installed.
