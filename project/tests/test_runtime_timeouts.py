"""Recorder budgets must remain bounded and never imply Android execution."""
import argparse
import unittest

from android_acceptance import PROPERTIES, positive_timeout


class RuntimeTimeoutTests(unittest.TestCase):
    def test_accepts_bounded_integer_seconds(self):
        for text, expected in [('1', 1), ('90', 90), ('900', 900), ('1800', 1800)]:
            with self.subTest(text=text):
                self.assertEqual(positive_timeout(text), expected)

    def test_rejects_unbounded_and_invalid_waits(self):
        for text in ['0', '-1', '1801', '1.5', 'inf', 'nan', 'timeout']:
            with self.subTest(text=text):
                with self.assertRaises(argparse.ArgumentTypeError):
                    positive_timeout(text)

    def test_records_native_translation_environment(self):
        self.assertIn('ro.product.cpu.abi', PROPERTIES)
        self.assertIn('ro.dalvik.vm.native.bridge', PROPERTIES)
        self.assertIn('ro.dalvik.vm.isa.arm64', PROPERTIES)


if __name__ == '__main__':
    unittest.main()
