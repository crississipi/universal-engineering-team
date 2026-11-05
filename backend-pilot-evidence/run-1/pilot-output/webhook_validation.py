"""Pure validation and normalization for incoming order webhook payloads."""

from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import TypedDict


class OrderItem(TypedDict):
    sku: str
    quantity: int
    unit_price: Decimal


class NormalizedOrderWebhook(TypedDict):
    order_id: str
    customer_email: str
    currency: str
    items: list[OrderItem]


def _required(mapping: Mapping[object, object], key: str, context: str) -> object:
    if key not in mapping:
        raise ValueError(f"{context}.{key} is required")
    return mapping[key]


def _mapping(value: object, context: str) -> Mapping[object, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{context} must be a mapping")
    return value


def _nonblank_string(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} must not be blank")
    return normalized


def _email(value: object) -> str:
    email = _nonblank_string(value, "customer_email")
    if email.count("@") != 1:
        raise ValueError("customer_email must contain exactly one @")
    local, domain = email.split("@")
    if (
        not local
        or not domain
        or any(character.isspace() for character in email)
        or "." not in domain
    ):
        raise ValueError("customer_email does not match the required basic shape")
    return email.lower()


def _currency(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 3
        or not all("A" <= character <= "Z" for character in value)
    ):
        raise ValueError("currency must be exactly three uppercase ASCII letters")
    return value.upper()


def _quantity(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    return value


def _unit_price(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(
        value, (str, int, float, Decimal)
    ):
        raise ValueError(f"{field} must be a string, int, float, or Decimal")
    try:
        price = Decimal(str(value)) if isinstance(value, float) else Decimal(value)
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field} must be a valid decimal") from None
    if not price.is_finite():
        raise ValueError(f"{field} must be finite")
    if price < 0:
        raise ValueError(f"{field} must not be negative")
    return price


def normalize_order_webhook(payload: object) -> NormalizedOrderWebhook:
    """Validate an untrusted order payload and return its normalized fields."""
    order = _mapping(payload, "payload")
    order_id = _nonblank_string(_required(order, "order_id", "payload"), "order_id")
    customer_email = _email(
        _required(order, "customer_email", "payload")
    )
    currency = _currency(_required(order, "currency", "payload"))

    raw_items = _required(order, "items", "payload")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("items must be a non-empty list")

    items: list[OrderItem] = []
    for index, raw_item in enumerate(raw_items):
        context = f"items[{index}]"
        item = _mapping(raw_item, context)
        sku = _nonblank_string(_required(item, "sku", context), f"{context}.sku")
        quantity = _quantity(
            _required(item, "quantity", context),
            f"{context}.quantity",
        )
        unit_price = _unit_price(
            _required(item, "unit_price", context),
            f"{context}.unit_price",
        )
        items.append(
            {"sku": sku, "quantity": quantity, "unit_price": unit_price}
        )

    return {
        "order_id": order_id,
        "customer_email": customer_email,
        "currency": currency,
        "items": items,
    }
