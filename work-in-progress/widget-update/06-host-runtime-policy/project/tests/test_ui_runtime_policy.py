"""Reject missing, default or ambiguous exception policy evidence."""
import unittest
import ui_runtime_policy as policy


class UiRuntimePolicyTests(unittest.TestCase):
    SAMPLE = """     bool OmitStackTraceInFastThrow = false {product} {command line}
     bool ShowCodeDetailsInExceptionMessages = true {manageable} {command line}
"""

    def test_explicit_effective_policy(self):
        self.assertEqual(policy.parse_effective_flags(self.SAMPLE), {
            "OmitStackTraceInFastThrow": False, "ShowCodeDetailsInExceptionMessages": True})

    def test_default_fast_throw_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Unexpected effective"):
            policy.parse_effective_flags(self.SAMPLE.replace("= false", "= true"))

    def test_missing_message_detail_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Unexpected effective"):
            policy.parse_effective_flags(self.SAMPLE.replace("Messages = true", "Messages = false"))

    def test_duplicate_effective_flag_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "ambiguous"):
            policy.parse_effective_flags(self.SAMPLE + self.SAMPLE.splitlines()[0] + "\n")

    def test_command_echo_is_not_effective_evidence(self):
        with self.assertRaisesRegex(RuntimeError, "Missing"):
            policy.parse_effective_flags("java " + " ".join(policy.JVM_FLAGS))

    def test_truncated_flag_inventory_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Missing"):
            policy.parse_effective_flags(self.SAMPLE.splitlines()[0] + "\n")


if __name__ == "__main__":
    unittest.main()
