# Order Totals Proof Lab

`app/order_totals.py` provides `calculate_order_total(items, discount_percent=0)`.
Each item is a mapping with `unit_price` and `quantity`.

Prices and discounts accept `Decimal`, integer, or decimal-string values.
Booleans and floats are rejected. Prices must be finite and non-negative;
quantities must be positive integers, excluding booleans. The item list must
not be empty. Discounts must be finite and between 0 and 100 inclusive.

The function returns a dictionary with `subtotal`, `discount_amount`, and
`total`, all as `Decimal` values with two fractional digits. It rounds the
subtotal to cents first, calculates the discount from that rounded subtotal,
and rounds each monetary result using `ROUND_HALF_UP`.

Invalid input raises `TypeError` for unsupported types and `ValueError` for
missing fields or invalid numeric ranges and values.

Run the tests from this directory:

```powershell
python -m unittest discover -s tests -v
```
