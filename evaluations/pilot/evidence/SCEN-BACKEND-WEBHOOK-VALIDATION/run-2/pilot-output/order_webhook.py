from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import TypedDict


class NormalizedItem(TypedDict):
    sku: str
    quantity: int
    unit_price: Decimal


class NormalizedOrder(TypedDict):
    order_id: str
    customer_email: str
    currency: str
    items: list[NormalizedItem]


def _required(mapping: Mapping[str, object], field: str, path: str) -> object:
    try:
        return mapping[field]
    except KeyError:
        raise ValueError(f"{path}.{field} is required") from None


def _normalize_price(value: object, path: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{path} must be a string, integer, float, or Decimal")

    try:
        if isinstance(value, Decimal):
            price = value
        elif isinstance(value, float):
            price = Decimal(str(value))
        else:
            price = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"{path} must be a valid decimal") from None

    if not price.is_finite():
        raise ValueError(f"{path} must be finite")
    if price < 0:
        raise ValueError(f"{path} must be non-negative")
    return price


def validate_order_webhook(payload: Mapping[str, object]) -> NormalizedOrder:
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be a mapping")

    order_id = _required(payload, "order_id", "order")
    if not isinstance(order_id, str) or not order_id.strip():
        raise ValueError("order.order_id must be a non-empty string")

    customer_email = _required(payload, "customer_email", "order")
    if not isinstance(customer_email, str):
        raise ValueError("order.customer_email must be a string")
    customer_email = customer_email.strip()
    if (
        customer_email.count("@") != 1
        or any(character.isspace() for character in customer_email)
    ):
        raise ValueError("order.customer_email has an invalid basic email shape")
    local, domain = customer_email.split("@")
    if not local or not domain or "." not in domain:
        raise ValueError("order.customer_email has an invalid basic email shape")

    currency = _required(payload, "currency", "order")
    if not isinstance(currency, str) or len(currency) != 3 or not all(
        "A" <= character <= "Z" for character in currency
    ):
        raise ValueError("order.currency must be three uppercase ASCII letters")

    items = _required(payload, "items", "order")
    if not isinstance(items, list) or not items:
        raise ValueError("order.items must be a non-empty list")

    normalized_items: list[NormalizedItem] = []
    for index, item in enumerate(items):
        item_path = f"order.items[{index}]"
        if not isinstance(item, Mapping):
            raise ValueError(f"{item_path} must be a mapping")

        sku = _required(item, "sku", item_path)
        if not isinstance(sku, str) or not sku.strip():
            raise ValueError(f"{item_path}.sku must be a non-empty string")

        quantity = _required(item, "quantity", item_path)
        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            raise ValueError(f"{item_path}.quantity must be a positive integer")

        unit_price = _normalize_price(
            _required(item, "unit_price", item_path),
            f"{item_path}.unit_price",
        )
        normalized_items.append(
            {"sku": sku.strip(), "quantity": quantity, "unit_price": unit_price}
        )

    return {
        "order_id": order_id.strip(),
        "customer_email": customer_email.lower(),
        "currency": currency,
        "items": normalized_items,
    }
