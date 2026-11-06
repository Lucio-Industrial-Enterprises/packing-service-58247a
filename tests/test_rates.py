import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service)

    def test_explicit_standard_preserves_quotes(self):
        for zone, expected in (("local", 6.85), ("regional", 9.85)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(1.234, zone), expected)
                self.assertEqual(shipping_quote(1.234, zone, "standard"), expected)

    def test_express_rates(self):
        for zone, expected in (("local", 15.0), ("regional", 18.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, service="express"), expected)

    def test_express_fractional_weight(self):
        self.assertEqual(shipping_quote(1.234, "local", "express"), 13.85)
        self.assertEqual(shipping_quote(1.234, "regional", "express"), 16.85)

    def test_unknown_service(self):
        for service in ("overnight", "", "Express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service)

    def test_unknown_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service)
