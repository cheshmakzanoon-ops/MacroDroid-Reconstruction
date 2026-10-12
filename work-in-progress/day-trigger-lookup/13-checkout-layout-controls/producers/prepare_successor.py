from __future__ import annotations

import ast
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat

ROOT = Path(__file__).resolve().parent
PARENT = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls')
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/combined-run-38245093369/extracted')


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(path.stat().st_mode)}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    capsule = PARENT / 'checkpoint.json'
    assert identity(capsule)['sha256'] == '4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88'
    checkpoint = json.loads(capsule.read_bytes())
    before = {}
    source = ROOT / 'stage-01/repository'
    source.mkdir(parents=True, exist_ok=False)
    for row in checkpoint['files']:
        if not row['path'].startswith('source/'): continue
        relative = row['path'].removeprefix('source/')
        origin = PARENT / row['path']
        assert identity(origin) == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
        raw_source = RAW / 'job-source' / relative
        assert raw_source.read_bytes() == origin.read_bytes(), relative
        target = source / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target); target.chmod(row['mode'])
        before[relative] = identity(origin)
    assert len(before) == 9
    write(ROOT / 'stage-01/source-before.json', before)
    path = source / 'tools/day_trigger_acceptance/test_day_trigger_acceptance.py'
    old = path.read_text()
    marker = '\n\nclass CombinedWorkflowControls(unittest.TestCase):\n'
    assert old.count(marker) == 1
    definitions = '''

COMBINED_JOB_PATHS = {
    '.github/workflows/day-trigger-wip-acceptance.yml',
    *('tools/day_trigger_acceptance/' + name for name in (
        'README.md', 'inputs.py', 'pins.json', 'prepare.py', 'run_acceptance.py',
        'runtime-files.json', 'test_day_trigger_acceptance.py', 'verify.py')),
}


def assert_declared_combined_job_files(case, repository):
    """The job owns nine paths, not the enclosing checkout's unrelated files."""
    workflow = (repository / '.github/workflows/day-trigger-wip-acceptance.yml').read_text()
    line = next(value for value in workflow.splitlines() if 'DAY_TRIGGER_RUNTIME_MANIFEST_SHA256:' in value)
    digest = line.split("'")[1]
    with patch.object(inputs, 'HERE', repository / 'tools/day_trigger_acceptance'):
        value = inputs.verify_runtime_manifest(digest)
    case.assertEqual(7, len(value['files']))
    declared = {'.github/workflows/day-trigger-wip-acceptance.yml',
                'tools/day_trigger_acceptance/runtime-files.json',
                *('tools/day_trigger_acceptance/' + row['path'] for row in value['files'])}
    case.assertEqual(COMBINED_JOB_PATHS, declared)
    for relative in sorted(declared):
        inputs.regular(repository, relative)
    return value


class CombinedCheckoutLayoutControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.checkout = self.root / 'checkout'
        origin = Path(__file__).resolve().parents[2]
        for relative in sorted(COMBINED_JOB_PATHS):
            self.put('checkout/' + relative, (origin / relative).read_bytes())
        # These inert bytes represent unrelated checkout content, not real Git
        # credentials or a working Git repository. Runtime siblings stay exact.
        self.metadata = {
            'README.md': b'Unrelated repository readme\\n',
            'docs/unrelated.txt': b'Unrelated documentation\\n',
            '.git/HEAD': b'ref: refs/heads/synthetic-layout-only\\n',
            '.git/config': b'[core]\\n    repositoryformatversion = 0\\n',
            '.git/info/sparse-checkout': b'/tools/day_trigger_acceptance/\\n',
        }
        for relative, data in self.metadata.items():
            self.put('checkout/' + relative, data)

    def test_unrelated_root_and_git_style_metadata_do_not_change_the_nine_path_scope(self):
        self.assertEqual(14, sum(path.is_file() for path in self.checkout.rglob('*')))
        self.assertEqual(7, len(assert_declared_combined_job_files(self, self.checkout)['files']))
        for relative, data in self.metadata.items():
            self.assertEqual(data, (self.checkout / relative).read_bytes())

    def test_extra_runtime_sibling_is_rejected_even_with_allowed_checkout_metadata(self):
        self.put('checkout/tools/day_trigger_acceptance/unexpected_helper.py', b'# Unbound runtime sibling\\n')
        with self.assertRaisesRegex(ValueError, 'Hosted runtime source inventory differs'):
            assert_declared_combined_job_files(self, self.checkout)
'''
    new = old.replace(marker, definitions + marker)
    old_test = '''        line = next(value for value in self.workflow.splitlines() if 'DAY_TRIGGER_RUNTIME_MANIFEST_SHA256:' in value)
        digest = line.split("'")[1]
        value = inputs.verify_runtime_manifest(digest)
        self.assertEqual(7, len(value['files']))
        self.assertEqual(9, sum(p.is_file() for p in self.root.rglob('*')))
'''
    replacement = '''        assert_declared_combined_job_files(self, self.root)
'''
    assert new.count(old_test) == 1
    new = new.replace(old_test, replacement)
    ast.parse(new); path.write_text(new)
    tools = source / 'tools/day_trigger_acceptance'
    manifest = tools / 'runtime-files.json'
    rows = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': identity(p)['sha256']}
            for p in sorted(tools.iterdir()) if p.is_file() and p.name != 'runtime-files.json']
    assert len(rows) == 7
    old_manifest = json.loads(manifest.read_bytes())
    assert old_manifest['schema'] == 1
    old_manifest['files'] = rows
    write(manifest, old_manifest)
    digest = identity(manifest)['sha256']
    workflow = source / '.github/workflows/day-trigger-wip-acceptance.yml'
    text, count = re.subn(r"DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '[0-9a-f]{64}'",
        "DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '" + digest + "'", workflow.read_text())
    assert count == 1; workflow.write_text(text)
    after = {relative: identity(source / relative) for relative in before}
    changes = {relative for relative in before if before[relative] != after[relative]}
    assert changes == {'tools/day_trigger_acceptance/test_day_trigger_acceptance.py',
                       'tools/day_trigger_acceptance/runtime-files.json',
                       '.github/workflows/day-trigger-wip-acceptance.yml'}
    patch_text = ''.join(''.join(difflib.unified_diff((PARENT / 'source' / relative).read_text().splitlines(True),
        (source / relative).read_text().splitlines(True), fromfile='parent/' + relative, tofile='candidate/' + relative))
        for relative in sorted(changes))
    (ROOT / 'stage-01/three-path-derivation.patch').write_text(patch_text)
    write(ROOT / 'stage-01/source-after.json', after)
    def methods(text):
        result = {}
        for node in ast.parse(text).body:
            if isinstance(node, ast.ClassDef):
                for method in node.body:
                    if isinstance(method, ast.FunctionDef) and method.name.startswith('test_'):
                        result[node.name + '.' + method.name] = ast.dump(method, include_attributes=False)
        return result
    a, b = methods(old), methods(new)
    modified = {name for name in a if a[name] != b.get(name)}
    added = set(b) - set(a)
    assert len(a) == 153 and len(b) == 155
    assert modified == {'CombinedWorkflowControls.test_workflow_runtime_pin_binds_all_seven_actual_runtime_siblings'}
    assert added == {'CombinedCheckoutLayoutControls.test_unrelated_root_and_git_style_metadata_do_not_change_the_nine_path_scope',
                     'CombinedCheckoutLayoutControls.test_extra_runtime_sibling_is_rejected_even_with_allowed_checkout_metadata'}
    value = {'schema': 1, 'status': 'TEST_ONLY_CHECKOUT_LAYOUT_SUCCESSOR_AUTHORED_NOT_YET_EXECUTED',
             'parent_checkpoint_sha256': identity(capsule)['sha256'], 'failed_actual_run': 38245093369,
             'failed_actual_job': 114796870050, 'actual_artifact_id': 11744651182,
             'actual_artifact_sha256': 'cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833',
             'nine_sources_match_actual_archived_runtime_before_change': True,
             'unchanged_test_method_bodies': 152, 'modified_test_method': sorted(modified), 'added_tests': sorted(added),
             'new_declared_tests': 155, 'changed_paths': sorted(changes),
             'production_inputs_prepare_run_verify_pins_readme_unchanged': True,
             'source_before': before, 'source_after': after,
             'runtime_manifest': identity(manifest), 'workflow': identity(workflow),
             'application_execution': False, 'android_execution': False, 'active_source_mutated': False}
    write(ROOT / 'stage-01/derivation.json', value)
    print(json.dumps({k: value[k] for k in ('status','unchanged_test_method_bodies','new_declared_tests',
        'changed_paths','runtime_manifest','workflow')}))


if __name__ == '__main__':
    main()
