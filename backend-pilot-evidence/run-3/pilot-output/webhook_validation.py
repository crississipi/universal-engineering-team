from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class OrderItem:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class OrderWebhook:
    order_id: str
    customer_email: str
    currency: str
    items: tuple[OrderItem, ...]


def _required(mapping: Mapping[str, object], key: str, path: str) -> object:
    if key not in mapping:
        raise ValueError(f"{path}.{key} is required")
    return mapping[key]


def _trimmed_non_empty_string(value: object, path: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{path} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{path} must not be empty")
    return normalized


def _normalize_email(value: object) -> str:
    email = _trimmed_non_empty_string(value, "customer_email")
    if email.count("@") != 1 or any(character.isspace() for character in email):
        raise ValueError("customer_email has an invalid basic email shape")
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        raise ValueError("customer_email has an invalid basic email shape")
    return email.lower()


def _normalize_currency(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 3
        or any(character < "A" or character > "Z" for character in value)
    ):
        raise ValueError("currency must be exactly three uppercase ASCII letters")
    return value.upper()


def _positive_quantity(value: object, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{path} must be a positive integer")
    return value


def _non_negative_finite_decimal(value: object, path: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{path} must be a string, int, float, or Decimal")

    try:
        if isinstance(value, float):
            price = Decimal(str(value))
        else:
            price = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{path} must be a valid decimal value") from exc

    if not price.is_finite():
        raise ValueError(f"{path} must be finite")
    if price < 0:
        raise ValueError(f"{path} must not be negative")
    return price


def validate_order_webhook(payload: object) -> OrderWebhook:
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be a mapping")

    order_id = _trimmed_non_empty_string(
        _required(payload, "order_id", "payload"), "order_id"
    )
    customer_email = _normalize_email(
        _required(payload, "customer_email", "payload")
    )
    currency = _normalize_currency(_required(payload, "currency", "payload"))
    raw_items = _required(payload, "items", "payload")

    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("items must be a non-empty list")

    items: list[OrderItem] = []
    for index, raw_item in enumerate(raw_items):
        item_path = f"items[{index}]"
        if not isinstance(raw_item, Mapping):
            raise ValueError(f"{item_path} must be a mapping")

        sku = _trimmed_non_empty_string(
            _required(raw_item, "sku", item_path), f"{item_path}.sku"
        )
        quantity = _positive_quantity(
            _required(raw_item, "quantity", item_path), f"{item_path}.quantity"
        )
        unit_price = _non_negative_finite_decimal(
            _required(raw_item, "unit_price", item_path), f"{item_path}.unit_price"
        )
        items.append(OrderItem(sku=sku, quantity=quantity, unit_price=unit_price))

    return OrderWebhook(
        order_id=order_id,
        customer_email=customer_email,
        currency=currency,
        items=tuple(items),
    )
