"""Release scope boundary controls; no app or network execution."""
import unittest
import stage_lookup_acceptance as stage


class ReleaseInputTests(unittest.TestCase):
    def test_overlay_scope_matches_release_integrity_not_root_prose(self):
        for name in ('build.py', 'source/a.md', 'tests/input.json', 'test-support/A.java',
                     'signing/test.keystore', 'tools/lib/a.jar', 'reference/a.smali'):
            with self.subTest(name=name): self.assertTrue(stage.release_input(name))
        for name in ('README.md', 'RECONSTRUCTION_STATUS.md', 'reports/result.json',
                     'dist/candidate.apk', 'tools/classes/A.class', 'tests/__pycache__/a.pyc',
                     'source/cached.pyc', 'tools/deep/classes/A.class'):
            with self.subTest(name=name): self.assertFalse(stage.release_input(name))


if __name__ == '__main__': unittest.main()
