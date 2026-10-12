"""Adversarial checks for exact multi-occurrence Widget fault preparation."""
from pathlib import Path
import tempfile
import unittest

import ui_mutation_catalog as catalog


class UiMutationCatalogTests(unittest.TestCase):
    def test_every_declared_occurrence_is_changed(self):
        self.assertEqual(catalog.apply_edits("cast(A); cast(A);", [
            {"find": "cast(A)", "replace": "identity(A)", "count": 2}]), "identity(A); identity(A);")

    def test_multiple_edits_form_one_mutant(self):
        self.assertEqual(catalog.apply_edits("log(message);", [
            {"find": "log(", "replace": "try { log(", "count": 1},
            {"find": ");", "replace": "); } catch (Exception ignored) {}", "count": 1}]),
            "try { log(message); } catch (Exception ignored) {}")

    def test_occurrence_drift_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "occurrence"):
            catalog.apply_edits("cast(A);", [{"find": "cast(A)", "replace": "identity(A)", "count": 2}])

    def test_boolean_count_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Invalid"):
            catalog.apply_edits("old", [{"find": "old", "replace": "new", "count": True}])

    def test_no_effect_edit_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Invalid"):
            catalog.apply_edits("old", [{"find": "old", "replace": "old", "count": 1}])

    def test_empty_anchor_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Invalid"):
            catalog.apply_edits("old", [{"find": "", "replace": "new", "count": 1}])

    def test_exact_real_catalog_prepares_all_24_faults(self):
        root = Path(__file__).resolve().parents[1]
        original = (root / catalog.HELPER_PATH).read_text()
        jobs = catalog.load_widget_mutations(root)
        self.assertEqual(len(jobs), 24)
        self.assertEqual(len({job["name"] for job in jobs}), 24)
        self.assertTrue(all(job["mutant"] != original and job["required_cases"] for job in jobs))
        self.assertEqual((root / catalog.HELPER_PATH).read_text(), original)

    def test_another_positive_helper_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            private = Path(folder)
            (private / catalog.CATALOG_PATH).parent.mkdir(parents=True)
            (private / catalog.CATALOG_PATH).write_bytes((root / catalog.CATALOG_PATH).read_bytes())
            (private / catalog.HELPER_PATH).parent.mkdir(parents=True)
            (private / catalog.HELPER_PATH).write_text("changed helper")
            with self.assertRaisesRegex(RuntimeError, "positive source"):
                catalog.load_widget_mutations(private)


if __name__ == "__main__":
    unittest.main()
