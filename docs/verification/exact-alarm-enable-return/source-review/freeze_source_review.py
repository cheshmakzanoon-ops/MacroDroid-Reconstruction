#!/usr/bin/env python3
"""Freeze the independently closed Settings source review and both earlier attempts."""
import hashlib
import json
from pathlib import Path
import shutil
import stat

BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
OUT = BASE / 'source-review-checkpoint-01'


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(path.stat().st_mode)}


def main():
    final = json.loads((BASE / 'source-review-03/result.json').read_bytes())
    assert final['passed'] is True and final['all_inputs_unchanged'] is True
    assert final['named_host_successes'] == 259 and final['historical_raw_files'] == 3507
    OUT.mkdir(exist_ok=False)
    selected = [BASE / name for name in (
        'review_closed_source.py', 'review_closed_source_02.py', 'review_closed_source_03.py',
        'source-review-parent-role-correction.patch', 'source-review-parent-role-correction.json',
        'source-review-historical-input-role-correction.patch', 'source-review-historical-input-role-correction.json',
        'freeze_source_review.py')]
    for folder in ('source-review-01', 'source-review-02', 'source-review-03'):
        selected.extend(p for p in (BASE / folder).rglob('*') if p.is_file())
    before = {str(path): identity(path) for path in selected}
    for path in selected:
        relative = path.relative_to(BASE)
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(before[str(path)]['mode'])
        assert identity(target) == before[str(path)]
    (OUT / 'README.md').write_text('''# Independent Settings source and historical replay review

The closed review in `source-review-03/result.json` passes. It independently hashes all 181 payloads of the exact `6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051` source capsule, streams and verifies all 353 evidence archive members, and binds the exact 102 source files used by the disjoint 50-test and 209-test executions. Every one of the 259 test names is a literal successful result, with no failures, errors, skips or duplicate credit.

The complete source delta is two dispatcher files plus four new files; 96 parent files and 37 recorded definitions remain byte-exact. The global command classifier is also AST-exact. The embedded Settings contract is the exact 140,449-byte observed design contract with SHA-256 `379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07`.

All 3,507 files of the actual fourteen-screen artifact were rehashed. The archived replay using these 102 source files is exactly equal to the earlier complete comparison object: all fourteen XML pairs match; only the TRIGGERS introduction image differs by 35 pixels; all other images match. The 1,091 commands retain 26 planned inputs, six setup mutations and zero Settings inputs. Known startup crashes and continuation are preserved in that unchanged result. This review does not claim full runtime parity.

The two unsuccessful read-only review attempts are retained with their exact executed sources, traces and unchanged-input receipts. Attempt 01 incorrectly assumed the copied command classifier had the same filename in the parent. Attempt 02 incorrectly assumed the parent's executed inventory omitted its two historical ZIP inputs. Attempt 03 names the exact copied classifier role and binds exactly those two historical ZIP identities, their before/after inventories and their archived executed copies. No application, recorder, test or evidence source was changed to satisfy the review.

No host suite, APK build, new device replay or Android operation was executed by this review. The future sixteen-screen plan is still inactive here. Its predicted enabled Settings state has not previously been observed on Android; that remains the purpose of the bounded device experiment.
''')
    assert before == {str(path): identity(path) for path in selected}
    rows = [{'path': p.relative_to(OUT).as_posix(), **identity(p)}
            for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': 'SETTINGS_SOURCE_HOST_AND_HISTORICAL_EVIDENCE_REVIEW_PASSED',
        'repo_target': 'docs/verification/exact-alarm-enable-return/source-review',
        'active_files': [], 'reviewed_source_checkpoint_sha256': '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051',
        'source_files': 102, 'distinct_host_successes': 259, 'historical_raw_files_rehashed': 3507,
        'complete_historical_comparison_unchanged': True, 'review_attempts_preserved': 3,
        'all_review_inputs_unchanged': True, 'android_executed': False,
        'new_host_suite_executed': False, 'full_runtime_1_to_1_established': False, 'files': rows}
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), **identity(path), 'payloads': len(rows),
                      'payload_bytes': sum(row['bytes'] for row in rows)}, indent=2))


if __name__ == '__main__':
    main()
