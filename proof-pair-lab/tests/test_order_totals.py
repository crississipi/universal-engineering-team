import unittest
from decimal import Decimal, InvalidOperation

from app.order_totals import calculate_order_total


class CalculateOrderTotalTests(unittest.TestCase):
    def test_calculates_subtotal_discount_and_total(self):
        result = calculate_order_total(
            [
                {"unit_price": "12.50", "quantity": 2},
                {"unit_price": Decimal("3.25"), "quantity": 1},
                {"unit_price": 3, "quantity": 1},
            ],
            discount_percent="10",
        )

        self.assertEqual(
            result,
            {
                "subtotal": Decimal("31.25"),
                "discount_amount": Decimal("3.13"),
                "total": Decimal("28.12"),
            },
        )

    def test_accepts_zero_price(self):
        self.assertEqual(
            calculate_order_total([{"unit_price": "0", "quantity": 1}]),
            {
                "subtotal": Decimal("0.00"),
                "discount_amount": Decimal("0.00"),
                "total": Decimal("0.00"),
            },
        )

    def test_accepts_zero_and_full_discount_boundaries(self):
        items = [{"unit_price": Decimal("0.50"), "quantity": 2}]

        with self.subTest(discount=0):
            self.assertEqual(
                calculate_order_total(items, 0).get("total"), Decimal("1.00")
            )
        with self.subTest(discount=100):
            self.assertEqual(
                calculate_order_total(items, 100).get("total"), Decimal("0.00")
            )

    def test_rounds_money_to_cents_using_half_up(self):
        result = calculate_order_total(
            [{"unit_price": Decimal("1.005"), "quantity": 1}],
            discount_percent=50,
        )

        self.assertEqual(
            result,
            {
                "subtotal": Decimal("1.01"),
                "discount_amount": Decimal("0.51"),
                "total": Decimal("0.50"),
            },
        )

    def test_handles_amounts_larger_than_the_default_decimal_precision(self):
        try:
            result = calculate_order_total(
                [
                    {
                        "unit_price": Decimal("10000000000000000000000000000"),
                        "quantity": 10,
                    }
                ],
                discount_percent=10,
            )
        except InvalidOperation as error:
            self.fail(f"valid large amounts must be supported: {error}")

        self.assertEqual(
            result,
            {
                "subtotal": Decimal("100000000000000000000000000000.00"),
                "discount_amount": Decimal("10000000000000000000000000000.00"),
                "total": Decimal("90000000000000000000000000000.00"),
            },
        )

    def test_handles_amounts_above_the_default_decimal_context_emax(self):
        result = calculate_order_total(
            [{"unit_price": Decimal("1e1000000"), "quantity": 1}]
        )

        self.assertEqual(result["subtotal"].adjusted(), 1_000_000)
        self.assertEqual(result["subtotal"].as_tuple().exponent, -2)

    def test_requires_a_non_empty_list(self):
        with self.assertRaises(ValueError):
            calculate_order_total([])
        with self.assertRaises(TypeError):
            calculate_order_total(({"unit_price": 1, "quantity": 1},))

    def test_requires_item_fields_and_mapping_items(self):
        for item in ({"unit_price": 1}, {"quantity": 1}):
            with self.subTest(item=item), self.assertRaises(ValueError):
                calculate_order_total([item])
        with self.assertRaises(TypeError):
            calculate_order_total([("unit_price", 1)])

    def test_rejects_invalid_prices(self):
        for price in (True, 1.0):
            with self.subTest(price=price), self.assertRaises(TypeError):
                calculate_order_total([{"unit_price": price, "quantity": 1}])

        invalid_prices = (
            Decimal("-0.01"),
            Decimal("NaN"),
            Decimal("Infinity"),
            "invalid",
        )
        for price in invalid_prices:
            with self.subTest(price=price), self.assertRaises(ValueError):
                calculate_order_total([{"unit_price": price, "quantity": 1}])

    def test_requires_positive_integer_quantities_and_rejects_booleans(self):
        for quantity in (True, 1.0, "1"):
            with self.subTest(quantity=quantity), self.assertRaises(TypeError):
                calculate_order_total([{"unit_price": 1, "quantity": quantity}])

        for quantity in (0, -1):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                calculate_order_total([{"unit_price": 1, "quantity": quantity}])

    def test_accepts_quantities_with_more_than_4300_decimal_digits(self):
        quantity = 10**5000

        result = calculate_order_total(
            [{"unit_price": Decimal("1"), "quantity": quantity}]
        )

        self.assertEqual(result["subtotal"], Decimal(quantity))
        self.assertEqual(result["subtotal"].as_tuple().exponent, -2)
        self.assertEqual(result["discount_amount"], Decimal("0.00"))
        self.assertEqual(result["total"], Decimal(quantity))

    def test_rejects_invalid_discounts(self):
        items = [{"unit_price": 1, "quantity": 1}]

        for discount in (True, 1.0):
            with self.subTest(discount=discount), self.assertRaises(TypeError):
                calculate_order_total(items, discount)

        for discount in (
            Decimal("-0.01"),
            Decimal("100.01"),
            Decimal("NaN"),
            Decimal("Infinity"),
            "invalid",
        ):
            with self.subTest(discount=discount), self.assertRaises(ValueError):
                calculate_order_total(items, discount)


if __name__ == "__main__":
    unittest.main()
