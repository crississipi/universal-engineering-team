# Independent QA Verification Report — Order Totals

**Verified:** 2026-11-03
**QA role:** QA Manager
**Scope:** Independent verification of the order-total implementation against the ten supplied requirements.

## Tested implementation state

- Repository base: `HEAD` `fb49901e8b53264d91c5d40df14268620072a909`.
- `proof-pair-lab/` was untracked during this run, so the implementation revision is identified by content rather than by a commit:
  - [`app/order_totals.py`](../app/order_totals.py) SHA-256: `5BE507DC81F4B9381112430967F8D9A3F67B1D1FC1AAB4AA5BA9A868BAB30690`
  - [`tests/test_order_totals.py`](../tests/test_order_totals.py) SHA-256: `BE64CF6E2C61115B984C3E4F38A101B95C59238245C7512AC10527F3425E8C50`
- Runtime: Python 3.11.9; Decimal context defaults observed: `Emax=999999`, `Emin=-999999`, precision 28.
- The backend implementation was not modified.

## Requirements-to-test traceability

| # | Requirement | Independent check | Result |
|---|---|---|---|
| 1 | Non-empty list of order items | `test_requires_a_non_empty_list` | **Passed** |
| 2 | Required `unit_price` and `quantity` fields | `test_requires_both_item_fields` | **Passed** |
| 3 | Finite, non-negative decimal prices | `test_accepts_finite_non_negative_decimal_prices`; `test_supports_any_finite_price_even_above_decimal_context_emax` | **Failed** — ordinary cases passed; a valid finite price at `1E+1000000` raises `decimal.Overflow`. |
| 4 | Reject floats and booleans as prices | `test_rejects_float_and_boolean_prices` | **Passed** |
| 5 | Positive integer quantities, excluding booleans | `test_requires_positive_integer_quantities_and_excludes_booleans` | **Passed** |
| 6 | Discount from 0 through 100 inclusive | `test_discount_includes_zero_and_one_hundred_but_not_outside_range` | **Passed** |
| 7 | Decimal arithmetic | `test_uses_decimal_arithmetic_for_item_extension`; `test_supports_any_finite_price_even_above_decimal_context_emax` | **Failed** — ordinary exact arithmetic passed; arithmetic overflows for the valid finite boundary input below. |
| 8 | `ROUND_HALF_UP` monetary rounding to two decimal places | `test_rounds_ties_half_up_to_two_fractional_digits` | **Passed** |
| 9 | Correct subtotal, discount amount, and final total | `test_computes_subtotal_discount_and_total` | **Passed** |
| 10 | Clear rejection of invalid input | Invalid-input assertions in the price, quantity, discount, list, and required-field checks | **Passed** for the exercised invalid inputs. |

No listed requirement is not applicable. The complete finite Decimal domain was not exhaustively tested; see **Not verified** below.

## Commands executed and results

Commands were run from `proof-pair-lab/` unless otherwise stated.

1. `python -m unittest discover -s tests -v`
   **Passed:** 10 tests, 0 failures, 0 errors.

2. `python -c "from decimal import Decimal; from app.order_totals import calculate_order_total; calculate_order_total([{'unit_price': Decimal('1e1000000'), 'quantity': 1}])"`
   **Failed as reproduced:** exit code 1; uncaught `decimal.Overflow: [<class 'decimal.Overflow'>]` at multiplication in `app/order_totals.py` lines 77–78.

3. `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s qa -v`
   **Failed:** 10 tests run; 9 passed and `test_supports_any_finite_price_even_above_decimal_context_emax` errored with the same `decimal.Overflow` at `app/order_totals.py` lines 77–78. The test file SHA-256 is `8CBB48B27D760DB41710D8B9553B5E6534B8C73E6BF2042934D8DEE001BF5D8A`.

The supplied suite passing does not cover this valid-input boundary defect.

## Defect

**QA finding — Low severity; high confidence:** valid finite prices above the active Decimal context's maximum adjusted exponent are not handled.

**Reproduction:** From `proof-pair-lab/`, call:

```python
from decimal import Decimal
from app.order_totals import calculate_order_total

calculate_order_total([{"unit_price": Decimal("1e1000000"), "quantity": 1}])
```

**Expected:** Return a result with `subtotal`, `discount_amount`, and `total`, each a `Decimal` quantized to two fractional digits. The input is finite and non-negative, and no maximum price/exponent is specified by the requirements.

**Observed:** Uncaught `decimal.Overflow` during `price * quantity`, at [`app/order_totals.py`](../app/order_totals.py#L77). The implementation sets `context.prec` but leaves the Decimal context exponent limits unchanged in the arithmetic block ([`app/order_totals.py`](../app/order_totals.py#L75)).

**Impact:** A valid input fails with an arithmetic exception rather than producing the required totals. Prices with ordinary magnitudes are unaffected by this reproduction.

## Status summary

- **Passed:** Requirements 1, 2, 4, 5, 6, 8, 9, and 10 for the exercised cases.
- **Failed:** Requirements 3 and 7 for the finite `Decimal("1e1000000")` case.
- **Not applicable:** None of the ten requirements. UI, persistence, deployment, performance, and cross-service checks are outside this isolated calculator scope.
- **Not verified:** Exhaustive Decimal exponent/coefficient combinations, behavior on other Python versions, and integration into any caller outside `proof-pair-lab/`.

## Correction requested from Backend

Adjust the arithmetic strategy so finite non-negative Decimal prices accepted by the stated input contract—including values whose adjusted exponent exceeds the default Decimal context `Emax`—produce the required cent-quantized result without uncaught `decimal.Overflow`. Add a regression test for `Decimal("1e1000000")`. Do not silently add an input ceiling; if a ceiling is intended, it requires an explicit requirements change and clear validation behavior.

## Re-verification required after correction

1. Run `python -m unittest discover -s qa -v`; all independent QA checks, including the upper-exponent regression, must pass.
2. Run `python -m unittest discover -s tests -v`; preserve the supplied suite's passing baseline.
3. Recheck representative values around the Decimal exponent boundary, tiny finite values that round to cents, and the existing subtotal/discount/total rounding cases.
4. Confirm invalid values still fail explicitly with the documented `TypeError`/`ValueError` behavior.

## Documentation and handoff status

This report is the QA evidence record requested for the isolated proof lab. No application, central system report, Obsidian note, or Graphify relationship was changed: this assessment does not change system architecture or product behavior. The repository ownership file lists no active formal handoff contracts; this report is a QA verdict, not a formal handoff acceptance decision.

**Next owner/action:** Backend Developer to correct the finite-exponent arithmetic failure and return the revised implementation for independent QA re-verification.

---

## Re-verification — corrected order totals implementation

**Verified:** 2026-11-03
**QA role:** QA Manager
**Scope:** Re-run the prior failure and the original QA and supplied test suites against the corrected file state. Backend implementation files were not modified.

### Exact tested state

The proof lab remains untracked in the repository; there is no commit identifying its contents. The repository base was `HEAD` `fb49901e8b53264d91c5d40df14268620072a909`. The tested state is identified by these SHA-256 fingerprints:

- [`app/order_totals.py`](../app/order_totals.py): `FB12951BB013E647911D29BA61D285F7E84A450D13E8086FEA4C1761DC0A42C1`
- [`qa/test_order_totals_qa.py`](./test_order_totals_qa.py): `8CBB48B27D760DB41710D8B9553B5E6534B8C73E6BF2042934D8DEE001BF5D8A`
- [`tests/test_order_totals.py`](../tests/test_order_totals.py): `6EDEEA363FE423C3EA24F566C325808E73E88C18E9B269D62B76C3AC3CD8753B`

Runtime: Python 3.11.9. The original failure and its evidence above were preserved unchanged.

### Checks and outcomes

Run from `proof-pair-lab/`:

1. `python -m unittest discover -s qa -v` — **Passed:** 10 tests, including `test_supports_any_finite_price_even_above_decimal_context_emax`.
2. `python -m unittest discover -s tests -v` — **Passed:** 11 tests.
3. Original failure reproducer:

   ```powershell
   python -c "from decimal import Decimal; from app.order_totals import calculate_order_total; result = calculate_order_total([{'unit_price': Decimal('1e1000000'), 'quantity': 1}]); print(result['subtotal'].adjusted(), result['subtotal'].as_tuple().exponent)"
   ```

   **Passed:** printed `1000000 -2`; no `decimal.Overflow`. The result is a Decimal rounded to cents as required.
4. Independent boundary probes, run via a PowerShell here-string piped to `python -`:

   ```powershell
   Set-Location .\proof-pair-lab; @'
   from decimal import Decimal
   from app.order_totals import calculate_order_total

   for price in (Decimal("1e999999"), Decimal("1e1000000"), Decimal("1e-1000000")):
       result = calculate_order_total([{"unit_price": price, "quantity": 1}])
       subtotal = result["subtotal"]
       print(f"price={price!r}; subtotal_adjusted={subtotal.adjusted()}; exponent={subtotal.as_tuple().exponent}; discount={result['discount_amount']}; total_exponent={result['total'].as_tuple().exponent}")

   try:
       calculate_order_total([{"unit_price": Decimal("1"), "quantity": 10**5000}])
   except Exception as error:
       print(f"5001-digit positive integer quantity: {type(error).__name__}: {error}")
   else:
       print("5001-digit positive integer quantity: accepted")
   '@ | python -
   ```

   **Exponent probes passed:** each returned cent-quantized totals; the tiny price rounded to `0.00`. **Quantity probe failed:** `ValueError: Exceeds the limit (4300 digits) for integer string conversion...` while the implementation estimates precision using `len(str(quantity))`.

### Acceptance criteria re-check

| # | Requirement | Re-verification |
|---|---|---|
| 1 | Non-empty item list | **Passed** in QA suite. |
| 2 | Required item fields | **Passed** in QA suite. |
| 3 | Finite, non-negative prices | **Passed** for exercised ordinary values, `1E+999999`, `1E+1000000`, and `1E-1000000`; not exhaustive. |
| 4 | Reject float and boolean prices | **Passed** in QA suite. |
| 5 | Positive integer quantities, excluding booleans | **Passed** for suite cases; **failed** for the valid positive integer `10**5000` because integer-to-string conversion hits Python's 4300-digit limit. |
| 6 | Discount from 0 through 100 inclusive | **Passed** in QA suite. |
| 7 | Decimal arithmetic | **Passed** for the supplied cases and reported large-exponent regression; exhaustive Decimal combinations not tested. |
| 8 | `ROUND_HALF_UP` to two places | **Passed** in QA suite. |
| 9 | Correct subtotal, discount, and total | **Passed** in QA suite. |
| 10 | Clear invalid-input rejection | **Passed** for the invalid cases exercised in both suites. |

### Remaining defect and unverified scope

**Low severity, high confidence:** the documented quantity contract says quantities must be positive integers and sets no maximum. A positive integer with more than 4300 decimal digits is rejected indirectly by `len(str(quantity))` in the precision-estimation path. This is separate from the corrected exponent-overflow failure. A practical quantity ceiling is not documented; either support this valid input or make an explicit contract change with deliberate validation.

Exhaustive Decimal exponent/coefficient combinations, other Python versions, and integration into callers outside this isolated proof lab were not tested. The ordinary full regression suite passed, but these results do not establish those untested areas.

### New QA assessment

**The reported Decimal overflow regression is verified as corrected. Overall result: not fully passing** because the independent positive-integer quantity probe violates the stated input contract. Do not treat this report as formal handoff acceptance: `docs/team/ownership.yml` declares `handoffs: []`.

Only this verification report was updated. No Backend implementation, Graphify relationship, Obsidian note, or central system report was changed; those are outside this isolated verification increment.

**Next action:** Backend Developer to address or explicitly constrain the oversized-quantity behavior, then request QA verification of that case. No formal handoff contract is implied.


## Final Independent QA Re-verification — Quantity Precision Correction

**Verdict:** PASS — Previously identified oversized-quantity defect resolved.

**Verification date:** 2026-11-03

### 1. Correction under review

Backend replaced the quantity digit-count calculation that previously called `len(str(quantity))` with a conservative digit-count upper bound derived from `int.bit_length()`.

The correction avoids Python's integer-to-string conversion limit without introducing a documented maximum quantity.

### 2. Independent test execution

The corrected archive was independently inspected and tested.

| Test suite | Result |
|---|---|
| Backend unit tests | 12 passed |
| QA verification tests | 10 passed |

**Environment:** Python 3.13.5

Both suites completed successfully.

### 3. Independent regression and boundary checks

The following cases were independently exercised:

- Positive integer quantity containing 5,001 decimal digits.
- Large quantity combined with fractional unit prices.
- Large quantity with percentage discount.
- Large quantities combined with large Decimal exponents.
- Tiny Decimal values.
- Multiple items with large quantities.
- Boolean quantity rejection.
- `ROUND_HALF_UP` behavior.
- Digit-count upper-bound checks.

All tested cases passed.

The original oversized-quantity failure was no longer reproducible.

### 4. Evidence integrity

The supplied SHA-256 fingerprints for the corrected implementation, Backend tests, and QA report were checked against the uploaded archive and matched.

The QA-owned report was not modified by Backend. This entry is an independent QA addition and preserves the earlier failure history.

### 5. Final QA assessment

The previously reported defect involving integer-to-string conversion during precision estimation is resolved in the reviewed implementation.

No new failure was identified in the tested cases.

**Final finding status:** Resolved
**QA verdict for this correction:** PASS

### 6. Remaining limitations

This verification does not establish:

- Cross-version compatibility across all supported Python versions.
- That the deliberately injected boolean-quantity defect was present during the initial QA review.
- Completion of the remaining controlled proof scenarios involving conditional dependencies, feedback, repeated correction attempts, and immediate escalation.

These items remain separate evaluation obligations and must not be treated as passed based on this verification.