import unittest
from decimal import Decimal

from webhook_validation import OrderItem, OrderWebhook, validate_order_webhook


def valid_payload() -> dict[str, object]:
    return {
        "order_id": "  order-123  ",
        "customer_email": "  Alice@EXAMPLE.COM ",
        "currency": "USD",
        "items": [
            {
                "sku": "  SKU-1  ",
                "quantity": 2,
                "unit_price": "12.34567890123456789",
            }
        ],
    }


class ValidateOrderWebhookTests(unittest.TestCase):
    def test_normalizes_valid_payload_without_rounding_prices(self) -> None:
        normalized = validate_order_webhook(valid_payload())

        self.assertEqual(
            normalized,
            OrderWebhook(
                order_id="order-123",
                customer_email="alice@example.com",
                currency="USD",
                items=(
                    OrderItem(
                        sku="SKU-1",
                        quantity=2,
                        unit_price=Decimal("12.34567890123456789"),
                    ),
                ),
            ),
        )

    def test_accepts_all_supported_price_types_and_parses_float_through_string(self) -> None:
        payload = valid_payload()
        payload["items"] = [
            {"sku": "a", "quantity": 1, "unit_price": "1.25"},
            {"sku": "b", "quantity": 1, "unit_price": 2},
            {"sku": "c", "quantity": 1, "unit_price": 0.1},
            {"sku": "d", "quantity": 1, "unit_price": Decimal("3.50")},
        ]

        normalized = validate_order_webhook(payload)

        self.assertEqual(
            [item.unit_price for item in normalized.items],
            [Decimal("1.25"), Decimal("2"), Decimal("0.1"), Decimal("3.50")],
        )

    def test_accepts_zero_price(self) -> None:
        payload = valid_payload()
        payload["items"][0]["unit_price"] = 0  # type: ignore[index]

        normalized = validate_order_webhook(payload)

        self.assertEqual(normalized.items[0].unit_price, Decimal("0"))

    def test_rejects_non_mapping_order_payload(self) -> None:
        with self.assertRaises(ValueError):
            validate_order_webhook(None)  # type: ignore[arg-type]

    def test_rejects_each_missing_order_field(self) -> None:
        for field in ("order_id", "customer_email", "currency", "items"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload[field]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_blank_order_id(self) -> None:
        payload = valid_payload()
        payload["order_id"] = " \t "

        with self.assertRaises(ValueError):
            validate_order_webhook(payload)

    def test_rejects_email_outside_the_defined_basic_shape(self) -> None:
        malformed_emails = (
            "alice.example.com",
            "alice@@example.com",
            "@example.com",
            "alice@",
            "alice@localhost",
            "alice @example.com",
            "alice@example .com",
        )
        for email in malformed_emails:
            with self.subTest(email=email):
                payload = valid_payload()
                payload["customer_email"] = email
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_blank_email(self) -> None:
        payload = valid_payload()
        payload["customer_email"] = "   "

        with self.assertRaises(ValueError):
            validate_order_webhook(payload)

    def test_rejects_malformed_currency(self) -> None:
        for currency in ("usd", "US", "USDD", "U$D", "ÜSD", "123"):
            with self.subTest(currency=currency):
                payload = valid_payload()
                payload["currency"] = currency
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_empty_or_non_list_items(self) -> None:
        for items in ([], ({"sku": "a", "quantity": 1, "unit_price": 1},)):
            with self.subTest(items=items):
                payload = valid_payload()
                payload["items"] = items
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_non_mapping_items(self) -> None:
        for item in ("not-an-item", 4, None):
            with self.subTest(item=item):
                payload = valid_payload()
                payload["items"] = [item]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_each_missing_item_field(self) -> None:
        for field in ("sku", "quantity", "unit_price"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload["items"][0][field]  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_blank_sku(self) -> None:
        payload = valid_payload()
        payload["items"][0]["sku"] = " \t "  # type: ignore[index]

        with self.assertRaises(ValueError):
            validate_order_webhook(payload)

    def test_rejects_boolean_and_non_integer_quantities(self) -> None:
        for quantity in (True, False, 1.0, "1"):
            with self.subTest(quantity=quantity):
                payload = valid_payload()
                payload["items"][0]["quantity"] = quantity  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_zero_and_negative_quantities(self) -> None:
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                payload = valid_payload()
                payload["items"][0]["quantity"] = quantity  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_boolean_price(self) -> None:
        payload = valid_payload()
        payload["items"][0]["unit_price"] = True  # type: ignore[index]

        with self.assertRaises(ValueError):
            validate_order_webhook(payload)

    def test_rejects_unsupported_price_types(self) -> None:
        for price in (None, [], object()):
            with self.subTest(price_type=type(price).__name__):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_negative_prices(self) -> None:
        for price in ("-0.01", -1, -0.5, Decimal("-2")):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_blank_and_malformed_decimal_strings(self) -> None:
        for price in ("", "  ", "not-a-price", "1.2.3"):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)

    def test_rejects_non_finite_prices(self) -> None:
        for price in (
            "NaN",
            "Infinity",
            "-Infinity",
            float("nan"),
            float("inf"),
            Decimal("NaN"),
            Decimal("Infinity"),
        ):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price  # type: ignore[index]
                with self.assertRaises(ValueError):
                    validate_order_webhook(payload)


if __name__ == "__main__":
    unittest.main()
