#!/usr/bin/env python3
"""Freeze the first 39-control pass and its subsequently identified limitation."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import stat

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
STAGE = ROOT / 'source-01'
OUTPUT = ROOT / 'checkpoints/02-first-source-and-host-attempt'

def copy_tree(source, target):
    for path in sorted(source.rglob('*')):
        if path.is_dir(): continue
        if not stat.S_ISREG(path.lstat().st_mode) or path.is_symlink():
            raise RuntimeError('Nonregular source')
        dest = target / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)

def main():
    attempt = STAGE / 'attempts/01-focused-first'
    result = json.loads((attempt / 'result.json').read_bytes())
    replay = json.loads((STAGE / 'completed-schema5-replay/result.json').read_bytes())
    assert result['status'] == 'PASS' and result['source_files'] == 98 and result['source_unchanged']
    assert 'Ran 39 tests' in (attempt / 'stderr.log').read_text()
    assert replay['status'] == 'EXACT_HISTORICAL_RESULT_UNCHANGED'
    assert replay['complete_comparison_object_equal'] and replay['raw_files_unchanged']
    OUTPUT.mkdir(exist_ok=False)
    copy_tree(attempt, OUTPUT / 'attempt')
    copy_tree(STAGE / 'completed-schema5-replay', OUTPUT / 'completed-schema5-replay')
    copy_tree(STAGE / 'derivation', OUTPUT / 'derivation')
    shutil.copy2(STAGE / 'source-before.json', OUTPUT / 'source-before.json')
    for name in ('create_source_stage.py', 'derive_shared_source.py', 'run_host_attempt.py',
                 'replay_completed_readiness.py', 'freeze_first_attempt.py'):
        shutil.copy2(ROOT / name, OUTPUT / name)
    (OUTPUT / 'README.md').write_text('''# First exact-alarm navigation source and host attempt

This is an inactive first draft, preserved before a confirmed independent verifier correction. It must not activate a workflow or receive Android parity credit.

The complete98-file source set derives from the exact81-file closed readiness source and both observed exact-alarm dialog artifact sets. Two existing shared modules change; the original notification-readiness module remains byte-identical. New schema6, the complete fourteen-screen plan, the actual dialog contract and the single Settings terminal role are explicit. The new readiness module keeps all thirteen non-binding functions identical as parsed Python ASTs; only its plan/policy bindings differ.

The first focused attempt ran39 tests successfully in157.468 seconds (wrapper159.196 seconds), preserving literal output, syntax checks and complete before/after source inventories. The controls include both actual dialog geometries, all nine positive-button ancestor roles, the real recorder path on virtual ADB, full-frame process/component failures, Settings-owner confinement, paired authored reports and the established readiness controls under the new plan. No new Android execution occurred. The synthetic Settings destination is explicitly authored and makes no claim about the actual destination class or controls.

The complete existing schema5 report from Android run38230072388 was separately replayed under these shared modules. Its entire comparison object remained identical, including thirteen screens, pixel differences[0,26,0,0,0,0,0,0,0,0,0,0,0], all hierarchies equal, the known recorded process-boundary outcome and failed exact visual equality. All3,258 raw artifact files and all98 source files remained unchanged.

## Confirmed limitation found after the first pass

Independent review reproduced a whole-report false acceptance: a unique chronological global `shell input tap20 20` command appended after the terminal captures left the complete comparison object unchanged and still claimed zero Settings inputs. The first39 controls did not cover this global command ownership gap. The independent counterexample and its complete synthetic artifacts are preserved in a separate publisher-owned review capsule. The first passing test result therefore does not authorize this draft's activation.

The successor will explicitly account for every planned input and every other global device command using the exact recorder command grammar, confine all state-changing commands to their declared run roles, retain all rejected attempts, and keep old schemas unchanged. It will be separately frozen and reviewed before any new workflow is activated.

The actual terminal control remains the observed enabled OK button at(560,809). No Settings control, permission grant, confirmed trigger configuration, saved macro or executed macro is established by this checkpoint.
''')
    files = []
    for path in sorted(OUTPUT.rglob('*')):
        if path.is_dir(): continue
        data = path.read_bytes(); info = path.stat()
        files.append({'path': path.relative_to(OUTPUT).as_posix(), 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(),
                      'mode': '100755' if info.st_mode & 0o111 else '100644'})
    checkpoint = {'schema': 1, 'status': 'FIRST_HOST_PASS_WITH_CONFIRMED_GLOBAL_INPUT_GAP',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'work-in-progress/exact-alarm-navigation/02-first-source-and-host-attempt',
                  'host_tests_passed': 39, 'subsequent_independent_false_accept_confirmed': True,
                  'complete_historical_schema5_verdict_unchanged': True,
                  'active_changes': False, 'android_executed': False,
                  'full_runtime_1_to_1_established': False, 'files': files}
    path = OUTPUT / 'checkpoint.json'; path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'bytes': path.stat().st_size,
                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files)}))

if __name__ == '__main__':
    main()
