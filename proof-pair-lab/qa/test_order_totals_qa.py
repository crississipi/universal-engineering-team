import unittest
from decimal import Decimal

from app.order_totals import calculate_order_total


class OrderTotalsIndependentVerificationTests(unittest.TestCase):
    def test_requires_a_non_empty_list(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            calculate_order_total([])
        with self.assertRaisesRegex(TypeError, "must be a list"):
            calculate_order_total(())

    def test_requires_both_item_fields(self):
        for item in ({"quantity": 1}, {"unit_price": "1.00"}):
            with self.subTest(item=item), self.assertRaisesRegex(
                ValueError, "unit_price.*quantity"
            ):
                calculate_order_total([item])

    def test_accepts_finite_non_negative_decimal_prices(self):
        for price in (Decimal("0"), Decimal("1.234"), 2, "3.45"):
            with self.subTest(price=price):
                result = calculate_order_total([{"unit_price": price, "quantity": 1}])
                self.assertIsInstance(result["subtotal"], Decimal)
        for price in (Decimal("-0.01"), Decimal("NaN"), Decimal("Infinity"), "bad"):
            with self.subTest(price=price), self.assertRaises((ValueError, TypeError)):
                calculate_order_total([{"unit_price": price, "quantity": 1}])

    def test_rejects_float_and_boolean_prices(self):
        for price in (1.0, True, False):
            with self.subTest(price=price), self.assertRaisesRegex(
                TypeError, "unit_price"
            ):
                calculate_order_total([{"unit_price": price, "quantity": 1}])

    def test_requires_positive_integer_quantities_and_excludes_booleans(self):
        for quantity in (1.0, "1", True, False):
            with self.subTest(quantity=quantity), self.assertRaisesRegex(
                TypeError, "quantity"
            ):
                calculate_order_total([{"unit_price": "1.00", "quantity": quantity}])
        for quantity in (0, -1):
            with self.subTest(quantity=quantity), self.assertRaisesRegex(
                ValueError, "must be positive"
            ):
                calculate_order_total([{"unit_price": "1.00", "quantity": quantity}])

    def test_discount_includes_zero_and_one_hundred_but_not_outside_range(self):
        item = [{"unit_price": "1.00", "quantity": 1}]
        self.assertEqual(calculate_order_total(item, 0)["total"], Decimal("1.00"))
        self.assertEqual(calculate_order_total(item, 100)["total"], Decimal("0.00"))
        for discount in (-1, "100.01", "NaN", "Infinity"):
            with self.subTest(discount=discount), self.assertRaisesRegex(
                ValueError, "discount_percent"
            ):
                calculate_order_total(item, discount)
        for discount in (True, 1.0):
            with self.subTest(discount=discount), self.assertRaisesRegex(
                TypeError, "discount_percent"
            ):
                calculate_order_total(item, discount)

    def test_uses_decimal_arithmetic_for_item_extension(self):
        result = calculate_order_total(
            [
                {"unit_price": "0.10", "quantity": 3},
                {"unit_price": Decimal("0.20"), "quantity": 1},
            ]
        )
        self.assertEqual(result["subtotal"], Decimal("0.50"))
        self.assertEqual(result["subtotal"].as_tuple().exponent, -2)

    def test_rounds_ties_half_up_to_two_fractional_digits(self):
        result = calculate_order_total(
            [{"unit_price": "1.005", "quantity": 1}], discount_percent="50"
        )
        self.assertEqual(result, {
            "subtotal": Decimal("1.01"),
            "discount_amount": Decimal("0.51"),
            "total": Decimal("0.50"),
        })
        self.assertTrue(all(value.as_tuple().exponent == -2 for value in result.values()))

    def test_computes_subtotal_discount_and_total(self):
        result = calculate_order_total(
            [
                {"unit_price": "12.50", "quantity": 2},
                {"unit_price": Decimal("3.25"), "quantity": 1},
                {"unit_price": 3, "quantity": 1},
            ],
            discount_percent="10",
        )
        self.assertEqual(result["subtotal"], Decimal("31.25"))
        self.assertEqual(result["discount_amount"], Decimal("3.13"))
        self.assertEqual(result["total"], Decimal("28.12"))

    def test_supports_any_finite_price_even_above_decimal_context_emax(self):
        result = calculate_order_total(
            [{"unit_price": Decimal("1e1000000"), "quantity": 1}]
        )
        self.assertEqual(result["subtotal"].adjusted(), 1_000_000)
        self.assertEqual(result["subtotal"].as_tuple().exponent, -2)


if __name__ == "__main__":
    unittest.main()
