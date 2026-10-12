"""Read the closed raw container's literal status without changing its members."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189')
raw = ROOT / 'extracted'
comparison = json.loads((raw / 'journey/comparison.json').read_text())
outer = json.loads((raw / 'exact-alarm-navigation-verification.json').read_text())
log = (raw / 'environment/emulator-boot.log').read_bytes()
private = re.compile(rb'^-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----\r?$|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', re.MULTILINE)
classification = {
    'schema': 1,
    'path': 'environment/emulator-boot.log',
    'sha256': hashlib.sha256(log).hexdigest(),
    'ephemeral_adb_public_key_lines': sum(b'adb.pubkey=' in line for line in log.splitlines()),
    'private_or_token_pattern_matches_in_flagged_log': len(private.findall(log)),
    'public_key_value_omitted_from_summary': True,
    'original_log_unchanged': True,
    'scope': 'Classifies the extractor finding; this is a bounded pattern scan, not an exhaustive credential audit.',
}
assert classification['ephemeral_adb_public_key_lines'] == 1
assert classification['private_or_token_pattern_matches_in_flagged_log'] == 0
summary = {
    'schema': 1,
    'scope': 'Initial immutable transport inspection; independent device replay is separate.',
    'run_id': 38240023189,
    'artifact_id': 11742624179,
    'head': '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
    'comparison_status': comparison['status'],
    'changed_pixels': [s['changed_pixels'] for s in comparison['screens']],
    'all_reported_hierarchies_equal': all(s['hierarchy_equal'] for s in comparison['screens']),
    'full_runtime_1_to_1_established': comparison['full_runtime_1_to_1_established'],
    'outer_status': outer['status'],
    'terminal_surfaces': comparison['terminal_surfaces'],
    'post_crash_continuation_observed_in_both': comparison['post_crash_continuation_observed_in_both'],
    'artifact_transformations': [],
}
assert summary['changed_pixels'] == [0, 35] + [0] * 12
assert summary['comparison_status'] == 'JOURNEY_DIFFERENCE'
assert summary['outer_status'] == 'EXACT_ALARM_NAVIGATION_FOURTEEN_SCREEN_DIFFERENCE'
assert all(s['owner'] == 'com.android.settings' and s['settings_inputs'] == 0
           and s['permission_granted'] is False for s in summary['terminal_surfaces'])
for name, value in [('key-scan-classification.json', classification),
                    ('literal-transport-observations.json', summary)]:
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': summary['comparison_status'], 'screens': len(summary['changed_pixels']),
                  'changed_pixels': summary['changed_pixels'], 'raw_mutations': 0}))
