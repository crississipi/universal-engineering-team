import importlib.util
from decimal import Decimal
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("webhook_validation.py")
SPEC = (
    importlib.util.spec_from_file_location("webhook_validation", MODULE_PATH)
    if MODULE_PATH.is_file()
    else None
)
validator = None
if SPEC is not None and SPEC.loader is not None:
    validator = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(validator)


class WebhookValidationTests(unittest.TestCase):
    def test_valid_payload_is_normalized(self):
        self.assertIsNotNone(
            validator,
            "webhook_validation.py must provide the order webhook validator",
        )
        payload = {
            "order_id": "  ORD-1  ",
            "customer_email": "  Buyer@Example.COM  ",
            "currency": "USD",
            "items": [
                {"sku": "  SKU-1 ", "quantity": 2, "unit_price": "1.2300"}
            ],
        }

        result = validator.normalize_order_webhook(payload)

        self.assertEqual(
            result,
            {
                "order_id": "ORD-1",
                "customer_email": "buyer@example.com",
                "currency": "USD",
                "items": [
                    {
                        "sku": "SKU-1",
                        "quantity": 2,
                        "unit_price": Decimal("1.2300"),
                    }
                ],
            },
        )
        self.assertEqual(
            set(result),
            {"order_id", "customer_email", "currency", "items"},
        )

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_supported_price_types_are_parsed_without_rounding(self):
        payload = valid_payload()
        payload["items"] = [
            {"sku": str(index), "quantity": 1, "unit_price": value}
            for index, value in enumerate(
                ("0.10", 2, 0.3, Decimal("4.1234567890123456789"))
            )
        ]

        result = validator.normalize_order_webhook(payload)

        self.assertEqual(
            [item["unit_price"] for item in result["items"]],
            [
                Decimal("0.10"),
                Decimal("2"),
                Decimal("0.3"),
                Decimal("4.1234567890123456789"),
            ],
        )

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_basic_email_rule_is_deliberately_not_rfc_validation(self):
        payload = valid_payload()
        payload["customer_email"] = " X@D.. "

        result = validator.normalize_order_webhook(payload)

        self.assertEqual(result["customer_email"], "x@d..")

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_missing_order_fields_are_rejected(self):
        for field in ("order_id", "customer_email", "currency", "items"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload[field]
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_missing_item_fields_are_rejected(self):
        for field in ("sku", "quantity", "unit_price"):
            with self.subTest(field=field):
                payload = valid_payload()
                del payload["items"][0][field]
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_blank_order_and_sku_are_rejected(self):
        for field, value in (("order_id", " \t "), ("sku", "\n ")):
            with self.subTest(field=field):
                payload = valid_payload()
                if field == "order_id":
                    payload[field] = value
                else:
                    payload["items"][0][field] = value
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_malformed_emails_are_rejected(self):
        for email in (
            "",
            "not-an-email",
            "@example.com",
            "buyer@",
            "buyer@@example.com",
            "buyer name@example.com",
            "buyer@example .com",
            "buyer@example",
        ):
            with self.subTest(email=email):
                payload = valid_payload()
                payload["customer_email"] = email
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_non_mapping_payload_and_items_are_rejected(self):
        with self.assertRaises(ValueError):
            validator.normalize_order_webhook([])

        for item in (None, "item", 3, []):
            with self.subTest(item=item):
                payload = valid_payload()
                payload["items"] = [item]
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_items_must_be_a_non_empty_list(self):
        for items in ([], (), None):
            with self.subTest(items=items):
                payload = valid_payload()
                payload["items"] = items
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_bool_and_non_integer_quantities_are_rejected(self):
        for quantity in (True, False, 1.0, "1"):
            with self.subTest(quantity=quantity):
                payload = valid_payload()
                payload["items"][0]["quantity"] = quantity
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_zero_and_negative_quantities_are_rejected(self):
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                payload = valid_payload()
                payload["items"][0]["quantity"] = quantity
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_bool_prices_are_rejected(self):
        for price in (True, False):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_negative_prices_are_rejected(self):
        for price in ("-0.01", -1, -0.5, Decimal("-0.0001")):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_malformed_decimal_prices_are_rejected(self):
        for price in ("", " \t ", "not-money", "1.2.3"):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_non_finite_prices_are_rejected(self):
        for price in (
            "NaN",
            "Infinity",
            "-Infinity",
            Decimal("NaN"),
            Decimal("Infinity"),
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(price=price):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_unsupported_price_types_are_rejected(self):
        for price in (None, [], object()):
            with self.subTest(price_type=type(price).__name__):
                payload = valid_payload()
                payload["items"][0]["unit_price"] = price
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_malformed_currency_values_are_rejected(self):
        for currency in ("usd", "US", "USDD", "U D", "ÉUR", 840):
            with self.subTest(currency=currency):
                payload = valid_payload()
                payload["currency"] = currency
                with self.assertRaises(ValueError):
                    validator.normalize_order_webhook(payload)


def valid_payload():
    return {
        "order_id": "ORDER-1",
        "customer_email": "buyer@example.com",
        "currency": "USD",
        "items": [{"sku": "SKU-1", "quantity": 1, "unit_price": "0"}],
    }


if __name__ == "__main__":
    unittest.main()
