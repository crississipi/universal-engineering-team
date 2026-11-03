from collections.abc import Mapping
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext

_CENT = Decimal("0.01")
_ONE_HUNDRED = Decimal("100")


def _decimal_digit_upper_bound(value: int) -> int:
    # 30103 / 100000 is a rational upper bound for log10(2).
    return (value.bit_length() * 30103 + 99_999) // 100_000


def _as_decimal(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float) or not isinstance(
        value, (Decimal, int, str)
    ):
        raise TypeError(f"{field} must be a Decimal, integer, or decimal string")

    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field} must be a valid decimal") from None

    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def calculate_order_total(
    items: list[Mapping[str, object]],
    discount_percent: Decimal | int | str = 0,
) -> dict[str, Decimal]:
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    if not items:
        raise ValueError("items must not be empty")

    validated_items: list[tuple[Decimal, int]] = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise TypeError(f"items[{index}] must be a mapping")
        if "unit_price" not in item or "quantity" not in item:
            raise ValueError(
                f"items[{index}] must contain 'unit_price' and 'quantity'"
            )

        unit_price = _as_decimal(item["unit_price"], f"items[{index}].unit_price")
        if unit_price < 0:
            raise ValueError(f"items[{index}].unit_price must not be negative")

        quantity = item["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError(f"items[{index}].quantity must be an integer")
        if quantity <= 0:
            raise ValueError(f"items[{index}].quantity must be positive")

        validated_items.append((unit_price, quantity))

    discount_percent = _as_decimal(discount_percent, "discount_percent")
    if not Decimal("0") <= discount_percent <= _ONE_HUNDRED:
        raise ValueError("discount_percent must be between 0 and 100")

    nonzero_items = [(price, quantity) for price, quantity in validated_items if price]
    if nonzero_items:
        min_exponent = min(price.as_tuple().exponent for price, _ in nonzero_items)
        max_adjusted = max(
            price.adjusted() + _decimal_digit_upper_bound(quantity)
            for price, quantity in nonzero_items
        )
        subtotal_precision = max_adjusted - min(min_exponent, -2) + 1
        subtotal_precision += len(str(len(validated_items)))
    else:
        subtotal_precision = 1

    # Keep every input digit through aggregation and cent quantization.
    precision = max(
        28,
        subtotal_precision + len(discount_percent.as_tuple().digits) + 4,
    )
    with localcontext() as context:
        context.prec = precision
        context.Emax = max(context.Emax, precision)
        subtotal = sum(
            (price * quantity for price, quantity in validated_items), Decimal("0")
        ).quantize(_CENT, rounding=ROUND_HALF_UP)
        discount_amount = (subtotal * discount_percent / _ONE_HUNDRED).quantize(
            _CENT, rounding=ROUND_HALF_UP
        )
        total = (subtotal - discount_amount).quantize(
            _CENT, rounding=ROUND_HALF_UP
        )

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total": total,
    }
