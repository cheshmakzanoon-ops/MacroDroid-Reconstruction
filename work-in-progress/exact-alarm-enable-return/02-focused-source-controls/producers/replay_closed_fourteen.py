from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time

from run_host_attempt import ROOT, WORKING, inventory

RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189/extracted')
EXPECTED = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/05-fourteen-screen-device-analysis/analysis/literal-captured-comparison-replay.json')


def raw_inventory():
    result = {}
    for path in sorted(RAW.rglob('*')):
        if path.is_dir(): continue
        info = path.lstat()
        assert stat.S_ISREG(info.st_mode), str(path)
        data = path.read_bytes()
        result[str(path.relative_to(RAW))] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return result


CHILD = '''from pathlib import Path
import json, sys
out=Path(sys.argv[1]); raw=Path(sys.argv[2]); expected=Path(sys.argv[3])
sys.path[:0]=[str(out/'repository/tools/parity_journeys'),str(out/'repository/project')]
import editor_journey as runner
import exact_alarm_journey as historical
import test_editor_journey as fixture
report=json.loads((raw/'journey/journey.json').read_bytes())
with historical.configured_plan():
 result=runner.compare(raw/'journey',report,fixture.proof)
(out/'literal-captured-comparison-replay.json').write_text(json.dumps(result,indent=2)+'\\n')
assert result==json.loads(expected.read_bytes()), 'Complete old fourteen-screen verdict changed'
assert len(result['screens'])==14
assert [r['changed_pixels'] for r in result['screens']]==[0,35,0,0,0,0,0,0,0,0,0,0,0,0]
assert result['status']=='JOURNEY_DIFFERENCE' and result['journey_equal'] is False
assert result['settings_inputs']==0 and result['global_command_observations']['planned_inputs']==26
assert result['global_command_observations']['commands']==1091
assert result['full_runtime_1_to_1_established'] is False
assert 'exact_alarm_enable_return_policy' not in result
print(json.dumps({'complete_historical_object_equal':True,'screens':14,'commands':1091,
 'changed_pixels':[r['changed_pixels'] for r in result['screens']], 'historical_status':result['status'],
 'historical_journey_equal':result['journey_equal'], 'android_executed_by_replay':False}))
'''


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('name'); args = parser.parse_args()
    out = ROOT / 'source-01/reports' / args.name; out.mkdir(parents=True, exist_ok=False)
    data = EXPECTED.read_bytes()
    assert len(data) == 11519 and hashlib.sha256(data).hexdigest() == '9430048fb84042122e8eb605c7697572bb6dae90c501a873d09e5b64ef4c09b9'
    (out / 'expected-historical-comparison.json').write_bytes(data)
    before = inventory(WORKING); raw_before = raw_inventory()
    for relative, row in before.items():
        target = out / 'repository' / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(WORKING / relative, target); target.chmod(row['mode'])
    assert inventory(out / 'repository') == before
    (out / 'source-before.json').write_text(json.dumps(before, indent=2) + '\n')
    with gzip.open(out / 'raw-inputs-before.json.gz', 'wb') as stream:
        stream.write((json.dumps(raw_before, indent=2) + '\n').encode())
    (out / 'replay.py').write_text(CHILD)
    shutil.copyfile(__file__, out / 'executed-replay-wrapper.py')
    argv = [sys.executable, '-B', str(out / 'replay.py'), str(out), str(RAW), str(EXPECTED)]
    env = os.environ.copy(); env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out))
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(); start = time.monotonic()
    with (out / 'stdout.txt').open('xb') as stdout, (out / 'stderr.txt').open('xb') as stderr:
        child = subprocess.run(argv, cwd=out / 'repository', env=env, stdout=stdout, stderr=stderr, timeout=300)
    after = inventory(WORKING); executed_after = inventory(out / 'repository'); raw_after = raw_inventory()
    with gzip.open(out / 'raw-inputs-after.json.gz', 'wb') as stream:
        stream.write((json.dumps(raw_after, indent=2) + '\n').encode())
    result = {'schema': 1, 'status': 'HISTORICAL_FOURTEEN_SCREEN_REPLAY_CONTROL', 'argv': argv,
              'cwd': str(out / 'repository'), 'timeout_seconds': 300, 'returncode': child.returncode,
              'started_utc': started, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'seconds': time.monotonic() - start, 'source_files': len(before), 'raw_files': len(raw_before),
              'working_source_unchanged': before == after, 'executed_source_unchanged': before == executed_after,
              'complete_raw_artifact_unchanged': raw_before == raw_after, 'android_executed_by_replay': False,
              'actual_historical_android_run_id': 38240023189, 'actual_historical_artifact_id': 11742624179,
              'actual_historical_head_sha': '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
              'passed': child.returncode == 0 and before == after == executed_after and raw_before == raw_after}
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
