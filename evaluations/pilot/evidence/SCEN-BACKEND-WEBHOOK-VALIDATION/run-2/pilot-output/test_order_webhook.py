import unittest
from decimal import Decimal

from order_webhook import validate_order_webhook


def valid_payload():
    return {
        "order_id": " order-123 ",
        "customer_email": "  Buyer@Example.COM  ",
        "currency": "USD",
        "items": [
            {
                "sku": " sku-456 ",
                "quantity": 2,
                "unit_price": "12.3400",
            }
        ],
    }


class ValidateOrderWebhookTests(unittest.TestCase):
    def assert_invalid(self, payload):
        with self.assertRaises(ValueError):
            validate_order_webhook(payload)

    def test_normalizes_valid_order_without_rounding_prices(self):
        normalized = validate_order_webhook(valid_payload())

        self.assertEqual(normalized["order_id"], "order-123")
        self.assertEqual(normalized["customer_email"], "buyer@example.com")
        self.assertEqual(normalized["currency"], "USD")
        self.assertEqual(
            normalized["items"],
            [{"sku": "sku-456", "quantity": 2, "unit_price": Decimal("12.3400")}],
        )
        self.assertEqual(normalized["items"][0]["unit_price"].as_tuple().exponent, -4)

    def test_normalizes_supported_price_types(self):
        for price, expected in (
            ("0", Decimal("0")),
            (7, Decimal("7")),
            (0.1, Decimal("0.1")),
            (Decimal("2.500"), Decimal("2.500")),
        ):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                normalized = validate_order_webhook(payload)
                self.assertEqual(normalized["items"][0]["unit_price"], expected)

    def test_rejects_non_mapping_order(self):
        for payload in (None, [], "order"):
            with self.subTest(payload=payload):
                self.assert_invalid(payload)

    def test_rejects_missing_order_fields(self):
        for field in ("order_id", "customer_email", "currency", "items"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload[field]
                self.assert_invalid(payload)

    def test_rejects_blank_or_non_string_order_id(self):
        for order_id in (" \t ", 123, None):
            with self.subTest(order_id=order_id):
                payload = valid_payload()
                payload["order_id"] = order_id
                self.assert_invalid(payload)

    def test_rejects_email_outside_the_defined_basic_shape(self):
        for email in (
            "buyer.example.com",
            "@example.com",
            "buyer@",
            "buyer@@example.com",
            "buyer@exam ple.com",
            "buyer@examplecom",
        ):
            with self.subTest(email=email):
                payload = valid_payload()
                payload["customer_email"] = email
                self.assert_invalid(payload)

    def test_rejects_non_string_email(self):
        payload = valid_payload()
        payload["customer_email"] = None
        self.assert_invalid(payload)

    def test_rejects_currency_that_is_not_three_uppercase_ascii_letters(self):
        for currency in ("usd", "US", "USDX", "ÉUR", "U D", 123):
            with self.subTest(currency=currency):
                payload = valid_payload()
                payload["currency"] = currency
                self.assert_invalid(payload)

    def test_rejects_empty_or_non_list_items(self):
        for items in ([], None, (), "item"):
            with self.subTest(items=items):
                payload = valid_payload()
                payload["items"] = items
                self.assert_invalid(payload)

    def test_rejects_non_mapping_items(self):
        payload = valid_payload()
        payload["items"] = ["not a mapping"]
        self.assert_invalid(payload)

    def test_rejects_missing_item_fields(self):
        for field in ("sku", "quantity", "unit_price"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload["items"][0][field]
                self.assert_invalid(payload)

    def test_rejects_blank_or_non_string_sku(self):
        for sku in ("  ", 42, None):
            with self.subTest(sku=sku):
                payload = valid_payload()
                payload["items"][0]["sku"] = sku
                self.assert_invalid(payload)

    def test_rejects_bool_zero_negative_and_non_integer_quantities(self):
        for quantity in (True, False, 0, -1, 1.5):
            with self.subTest(quantity=quantity):
                payload = valid_payload()
                payload["items"][0]["quantity"] = quantity
                self.assert_invalid(payload)

    def test_rejects_bool_and_unsupported_price_types(self):
        for price in (True, False, None, [], b"1.0"):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                self.assert_invalid(payload)

    def test_rejects_negative_prices(self):
        for price in ("-0.01", -1, -0.5, Decimal("-2.00")):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                self.assert_invalid(payload)

    def test_rejects_blank_and_malformed_decimal_strings(self):
        for price in ("", "  ", "not-a-price", "1.2.3"):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                self.assert_invalid(payload)

    def test_rejects_non_finite_prices(self):
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
                payload["items"][0]["unit_price"] = price
                self.assert_invalid(payload)


if __name__ == "__main__":
    unittest.main()
