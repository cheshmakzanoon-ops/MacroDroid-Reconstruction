"""Derive a guarded preparer for the nine expressly approved new numeric paths."""
from pathlib import Path
import difflib

root = Path('/dev/shm/macrodroid-transfer-space-20261012')
source = (root / 'prepare_standard_capsules.py').read_text()
changed = source.replace('names, prefixes, checks, baselines = set(), [], {}, {}', '''names, prefixes, checks, baselines = set(), [], {}, {}
ACTIVE_PATHS = {
    '.github/workflows/day-numeric-wip-acceptance.yml',
    *{'tools/day_numeric_acceptance/' + name for name in (
        'README.md', 'inputs.py', 'pins.json', 'prepare.py', 'run_acceptance.py',
        'runtime-files.json', 'test_day_numeric_acceptance.py', 'verify.py')},
}
activation_verified = []''')
changed = changed.replace('def staged(source, name):', 'def staged(source, name, active=False):')
changed = changed.replace("assert name.startswith(('docs/', 'work-in-progress/')) and name not in names", "assert (name.startswith(('docs/', 'work-in-progress/')) or (active and name in ACTIVE_PATHS)) and name not in names")
changed = changed.replace("    assert not cp.get('active_files') and not cp.get('active_changes') and not cp.get('android_executed_here')", '''    activate = item.get('activate_new_paths') is True
    assert not cp.get('active_changes') and not cp.get('android_executed_here')
    if activate:
        assert item['checkpoint_sha256'] == '994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473'
        assert not activation_verified and len(cp['active_files']) == 9
        assert {row['path'] for row in cp['active_files']} == ACTIVE_PATHS
    else:
        assert not cp.get('active_files')''')
changed = changed.replace("    prefixes.append(prefix)\n    checks[prefix]", '''    if activate:
        for row in cp['active_files']:
            name = safe(row['path'])
            assert row['baseline'] is None and row['must_be_absent'] is True
            check = subprocess.run(['git', '--git-dir=' + str(a.git_dir), 'cat-file', '-e', parent + ':' + name], capture_output=True)
            assert check.returncode != 0, 'Approved new path is no longer absent: ' + name
            local = source / safe(row['source'])
            raw = local.read_bytes()
            assert row['candidate'] == {'bytes': len(raw), 'sha256': sha(raw)}
            assert row['mode'] == '100644' and stat.S_IMODE(local.lstat().st_mode) == 0o644
            staged(local, name, active=True)
            activation_verified.append(dict(path=name, mode=row['mode'], **row['candidate'], parent_path_absent=True))
    prefixes.append(prefix)
    checks[prefix]''')
changed = changed.replace("ops = cfg['operations_prefix']", "assert len(activation_verified) == 9\nops = cfg['operations_prefix']")
changed = changed.replace("ops + '/prepare_standard_capsules.py'", "ops + '/prepare_numeric_hosted_publication.py'")
changed = changed.replace("('.gitattributes', ''.join(n + '/** -text\\n' for n in prefixes))", "('.gitattributes', ''.join(n + '/** -text\\n' for n in prefixes) + ''.join(n + ' -text\\n' for n in sorted(ACTIVE_PATHS)))")
changed = changed.replace('active_source_apk_or_workflow_changed=False)', 'active_application_source_or_apk_changed=False, approved_additive_tool_workflow_paths=activation_verified)')
assert changed != source and 'assert len(activation_verified) == 9' in changed
compile(changed, 'prepare_numeric_hosted_publication.py', 'exec')
(root / 'prepare_numeric_hosted_publication.py').write_text(changed)
(root / 'numeric-publication-preparer.patch').write_text(''.join(difflib.unified_diff(
    source.splitlines(True), changed.splitlines(True),
    fromfile='published/prepare_standard_capsules.py', tofile='prepare_numeric_hosted_publication.py')))
print('Derived exact guarded nine-new-path preparer; syntax valid')
