"""Generated staging must be removed fully before reuse; no Android is executed."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build


class StagingCleanupTests(unittest.TestCase):
    def test_old_generated_outputs_are_removed_before_reuse(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'old-stage'
            (target / 'nested').mkdir(parents=True)
            (target / 'nested/stale.dex').write_bytes(b'old output')
            build.remove_generated_directory(target)
            self.assertFalse(target.exists())
            build.remove_generated_directory(target)
            target.mkdir()
            self.assertEqual(list(target.iterdir()), [])

    def test_removal_error_keeps_its_actual_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'stage'
            target.mkdir()
            failure = PermissionError('Synthetic removal failure')
            with patch('build.shutil.rmtree', side_effect=failure), self.assertRaises(PermissionError) as caught:
                build.remove_generated_directory(target)
            self.assertIs(caught.exception, failure)

    def test_hybrid_cleanup_failure_prevents_any_source_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / 'hybrid-smali').mkdir()
            failure = OSError('Synthetic partial staging cleanup failure')
            with patch.object(build, 'WORK', work), patch('build.shutil.rmtree', side_effect=failure), \
                 patch('build.shutil.copytree') as copy, self.assertRaises(OSError) as caught:
                build.hybrid_source(work / 'unused-java')
            self.assertIs(caught.exception, failure)
            copy.assert_not_called()

    def test_fresh_java_generation_cannot_reuse_old_compiler_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / 'build'
            old = work / 'java'
            (old / 'dex').mkdir(parents=True)
            (old / 'dex/classes.dex').write_bytes(b'old dex')
            (old / 'hostclasses').mkdir()
            (old / 'hostclasses/stale.class').write_bytes(b'old class')
            reports = root / 'reports'
            reports.mkdir()
            observed = []
            def compiler(main, *args, **kwargs):
                if main.endswith('.D8'):
                    folder = Path(args[args.index('--output') + 1])
                    self.assertNotEqual(folder.parent, old)
                    self.assertEqual(list(folder.iterdir()), [])
                    self.assertEqual((old / 'dex/classes.dex').read_bytes(), b'old dex')
                    (folder / 'classes.dex').write_bytes(b'fresh dex')
                    observed.append(folder.parent)
                else:
                    output = Path(args[args.index('-o') + 1])
                    output.mkdir()
                    (output / 'fresh.smali').write_text('synthetic generated body')
            with patch.object(build, 'ROOT', root), patch.object(build, 'WORK', work), patch.object(build, 'REPORTS', reports), \
                 patch('build.run'), patch('build.java', side_effect=compiler), patch('build.dex_integrity', return_value='synthetic-verified-dex'):
                self.assertEqual(build.compile_java(), old)
            self.assertEqual(len(observed), 1)
            self.assertFalse(observed[0].exists())
            self.assertEqual((old / 'dex/classes.dex').read_bytes(), b'fresh dex')
            self.assertFalse((old / 'hostclasses/stale.class').exists())

    def test_failed_new_compile_preserves_last_completed_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / 'build'
            old = work / 'java'
            old.mkdir(parents=True)
            (old / 'completed.txt').write_text('last complete generation')
            with patch.object(build, 'ROOT', root), patch.object(build, 'WORK', work), \
                 patch('build.run', side_effect=RuntimeError('Synthetic javac failure')), self.assertRaisesRegex(RuntimeError, 'javac failure'):
                build.compile_java()
            self.assertEqual((old / 'completed.txt').read_text(), 'last complete generation')

    def test_zero_exit_without_valid_dex_cannot_replace_completed_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / 'build'
            old = work / 'java'
            old.mkdir(parents=True)
            (old / 'completed.txt').write_text('last complete generation')
            with patch.object(build, 'ROOT', root), patch.object(build, 'WORK', work), \
                 patch('build.run'), patch('build.java'), self.assertRaises(FileNotFoundError):
                build.compile_java()
            self.assertEqual((old / 'completed.txt').read_text(), 'last complete generation')


if __name__ == '__main__':
    unittest.main()
