import unittest

from scripts.theme_io import strict_json


class StrictJSONTests(unittest.TestCase):
    def test_rejects_overflowed_float(self):
        for number in ("1e999", "-1e999", "1.8e308", "-1.8e308"):
            with self.subTest(number=number):
                with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                    strict_json('{"metadata": [' + number + "]}")

    def test_preserves_finite_numbers(self):
        data = strict_json('{"integer": 42, "decimal": 0.5, "exponent": 1e2}')
        self.assertEqual(data, {"integer": 42, "decimal": 0.5, "exponent": 100.0})
        self.assertIsInstance(data["integer"], int)
        self.assertIsInstance(data["exponent"], float)
