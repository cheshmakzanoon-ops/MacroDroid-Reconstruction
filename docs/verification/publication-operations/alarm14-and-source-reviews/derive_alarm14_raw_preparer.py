"""Derive a single-run raw preservation recipe from the preserved prior recipe."""
import ast
from pathlib import Path
import pprint

base = Path('/dev/shm/macrodroid-transfer-space-20261012')
old = (base / 'prepare_closed_artifact_capsules.py').read_text()
node = next(n for n in ast.parse(old).body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'SPECS' for t in n.targets))
spec = {
    'name': 'alarm14', 'folder': 'alarm14-run-38240023189', 'run': 38240023189,
    'artifact': 11742624179, 'head': '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
    'bytes': 46626337, 'sha256': 'c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04',
    'members': 3507, 'expanded_bytes': 74601455,
    'prefix': 'docs/verification/android-exact-alarm-navigation-3f0ebc9',
    'title': 'Actual fourteen-screen exact-alarm navigation difference',
    'outcome': 'The observation and independent comparison steps failed after both fourteen-screen journeys completed. The literal reports record 35 differing pixels on intro-2, zero on the other thirteen screen pairs, and equal hierarchies. Both variants reached the Settings-owned surface after the observed explanation OK; no Settings input or permission grant occurred. Known post-crash continuations remain in the reports. These are the original reported outcomes; independent replay is preserved separately. Setup, all host controls, APK checks, runtime installation and complete evidence upload passed.',
}
lines = old.splitlines(keepends=True)
new = ''.join(lines[:node.lineno - 1]) + 'SPECS = ' + pprint.pformat([spec], sort_dicts=False) + '\n' + ''.join(lines[node.end_lineno:])
changes = {
    'Preserve two closed CI containers and every unchanged extracted member.': 'Preserve the closed Alarm14 CI container and every unchanged extracted member.',
    "archive = original / (spec['folder'] + '.zip')": "archive = original / 'artifact.zip'",
    "'github-run.json', 'key-scan-classification.json'": "'github-run.json', 'key-scan-classification.json', 'initial-transport-observations.json', 'literal-transport-observations.json'",
    "['extract_artifact.py', 'download_verified_artifact.py']": "['extract_artifact.py', 'download_verified_artifact.py', 'inspect_alarm14_transport.py']",
    "if spec['name'] == 'readiness'": "if spec['name'] == 'alarm14'",
    "'closed-artifact-capsules.json'": "'alarm14-closed-artifact-capsules.json'",
}
for before, after in changes.items():
    assert new.count(before) == 1, before
    new = new.replace(before, after)
ast.parse(new)
(base / 'prepare_alarm14_raw_capsule.py').write_text(new)
print('Single-run raw preservation recipe derived; no raw member changed.')
