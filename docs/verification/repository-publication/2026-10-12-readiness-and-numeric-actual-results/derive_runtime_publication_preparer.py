"""Derive exact closed-evidence preparation with the single reviewed README edit."""
from pathlib import Path
import difflib

root=Path('/dev/shm/macrodroid-transfer-space-20261012')
source=(root/'prepare_standard_capsules.py').read_text()
changed=source.replace('names, prefixes, checks, baselines = set(), [], {}, {}','names, prefixes, checks, baselines = set(), [], {}, {}\nreadme_activated = False')
changed=changed.replace('def staged(source, name):','def staged(source, name, active=False):')
changed=changed.replace("assert name.startswith(('docs/', 'work-in-progress/')) and name not in names", "assert (name.startswith(('docs/', 'work-in-progress/')) or (active and name == 'README.md')) and name not in names")
changed=changed.replace("    assert not cp.get('active_files') and not cp.get('active_changes') and not cp.get('android_executed_here')", '''    activate = item.get('activate_readme') is True
    assert not cp.get('active_changes') and not cp.get('android_executed_here')
    if activate:
        assert item['checkpoint_sha256'] == '29a2d7983b2672f8880ae7b8d934528413fc356de4b54e92b0dc520ae1c1dad7'
        assert not readme_activated and len(cp['active_files']) == 1
    else:
        assert not cp.get('active_files')''')
changed=changed.replace("    prefixes.append(prefix)\n    checks[prefix]", '''    if activate:
        row = cp['active_files'][0]
        assert row['path'] == row['source'] == 'README.md' and row['mode'] == '100644'
        before = git('show', parent + ':README.md')
        assert row['baseline'] == {'bytes': len(before), 'sha256': sha(before)}
        assert sha(before) == '3ae619d100d212572703ec51feae2e23fd70e35a8e301e361141e2cee63cc209'
        raw = (source / row['source']).read_bytes()
        assert row['candidate'] == {'bytes': len(raw), 'sha256': sha(raw)}
        assert sha(raw) == '5cb418202d6cf6898e29e61ebb29d3c0971022d62b4c1d9e1209213324074c63'
        baselines['README.md'] = sha(before)
        staged(source / row['source'], row['path'], active=True)
        readme_activated = True
    prefixes.append(prefix)
    checks[prefix]''')
changed=changed.replace("ops = cfg['operations_prefix']", "assert readme_activated\nops = cfg['operations_prefix']")
changed=changed.replace("ops + '/prepare_standard_capsules.py'", "ops + '/prepare_closed_runtime_publication.py'")
changed=changed.replace('active_source_apk_or_workflow_changed=False)', 'active_source_apk_or_workflow_changed=False, reviewed_root_readme_updated=readme_activated)')
compile(changed,'prepare_closed_runtime_publication.py','exec')
(root/'prepare_closed_runtime_publication.py').write_text(changed)
(root/'runtime-publication-preparer.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True),changed.splitlines(True),fromfile='published/prepare_standard_capsules.py',tofile='prepare_closed_runtime_publication.py')))
print('Derived exact closed-runtime preparer with the approved README baseline guard')
