"""Synthetic command-verifier boundary review; no Java, D8 or Android executes."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, sys, time

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'source'))
import verify

OUTPUT = ROOT / 'evidence'
OUTPUT.mkdir(exist_ok=False)
PROJECT = OUTPUT / 'synthetic-project'
PROJECT.mkdir()
FOLDER = 'reports/day-numeric-dex-synthetic'
roles = []

def pipeline(name):
    roles.extend((name, label, 0) for label in ('d8-helper', 'disassemble-helper', 'assemble-target'))

pipeline('positive-pipeline')
roles.extend([('', 'signed-apk-instructions', 0), ('', 'positive-transplant-instructions', 0), ('positive', 'execute', 0)])
for name in ('integer-zero', 'decimal-zero'):
    pipeline(name + '-pipeline')
    roles.append((name + '-dex-fault', 'execute', 3))
roles.extend([('original-as-rebuilt-rejected', 'execute', 1), ('wrong-helper-class-rejected', 'execute', 1), ('positive-restoration', 'execute', 0)])
assert len(roles) == 17

def now():
    return datetime.now(timezone.utc).isoformat()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

started = time.time_ns()
report = dict(started_utc=now(), commands=[])
for subdir, label, code in roles:
    name = FOLDER + ('/' + subdir if subdir else '')
    prefix = PROJECT / name
    prefix.mkdir(parents=True, exist_ok=True)
    argv = ['/synthetic/pinned-java', '-XX:-OmitStackTraceInFastThrow', '-Xmx512m', '-cp', '/synthetic/frozen-classpath',
            'DayNumericControlHarness' if label == 'execute' else 'SyntheticRole.' + label,
            str(prefix / 'config.json'), str(prefix / 'result.json')]
    row = dict(name=label, argv=argv, started_utc=now(), timeout_seconds=120, returncode=code)
    tick = time.monotonic()
    for stream in ('stdout', 'stderr'):
        path = prefix / (label + '.' + stream + '.log')
        raw = ('SYNTHETIC_ENVELOPE ' + subdir + '/' + label + '/' + stream + '\n').encode()
        path.write_bytes(raw)
        row[stream] = dict(path=path.relative_to(PROJECT).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    row['duration_seconds'] = time.monotonic() - tick
    row['ended_utc'] = now()
    report['commands'].append(row)
report['finished_utc'] = now()
ended = time.time_ns()
dump(OUTPUT / 'baseline-report.json', report)

def outcome(name, value):
    artifacts = verify.Artifacts(PROJECT, started, ended)
    error = None
    try:
        verify.verify_numeric_commands(value, FOLDER, artifacts)
        accepted = True
    except Exception as exc:
        accepted = False
        error = str(exc)
    dump(OUTPUT / (name + '-report.json'), value)
    return dict(name=name, accepted=accepted, error=error,
                validated_stream_paths=len(artifacts.rows), distinct_stream_inodes=len(artifacts.physical))

results = [outcome('positive-envelope', report)]
v = copy.deepcopy(report)
v['commands'][0]['argv'] = ['/bin/true']
results.append(outcome('non-d8-executable', v))
v = copy.deepcopy(report)
v['commands'][5]['argv'].remove('-XX:-OmitStackTraceInFastThrow')
results.append(outcome('omitted-jvm-policy', v))
v = copy.deepcopy(report)
v['commands'][5]['argv'][-2:] = ['/another/config.json', '/another/result.json']
results.append(outcome('different-config-result-roles', v))
v = copy.deepcopy(report)
v['commands'][0]['argv'] = [False]
results.append(outcome('boolean-argv-element', v))
v = copy.deepcopy(report)
v['commands'][0]['argv'] = []
results.append(outcome('empty-argv-negative-control', v))
v = copy.deepcopy(report)
v['commands'][0]['returncode'] = False
results.append(outcome('boolean-returncode-negative-control', v))
v = copy.deepcopy(report)
v['commands'][1]['stdout'] = copy.deepcopy(v['commands'][0]['stdout'])
results.append(outcome('reused-stream-role-negative-control', v))
results.append(outcome('exact-positive-restoration', report))
assert all(r['accepted'] for r in results[:5])
assert all(not r['accepted'] for r in results[5:8])
assert results[-1]['accepted'] and results[-1]['validated_stream_paths'] == 34
assert (OUTPUT / 'positive-envelope-report.json').read_bytes() == (OUTPUT / 'exact-positive-restoration-report.json').read_bytes()
source = json.loads((ROOT / 'reviewed-source-identities.json').read_text())
for row in source['files']:
    raw = (ROOT / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
summary = dict(status='NUMERIC_ARGV_GUARD_FALSE_ACCEPTANCES_REPRODUCED',
               reviewed_verifier_sha256='c0ba5c0df54530eb94a293b4dae9b548e2679dd0251e77c14b3d06e7aa65708a',
               scope='Direct synthetic verify_numeric_commands boundary only; not a complete verifier or host-acceptance pass',
               commands_described=17, distinct_raw_stream_files=34,
               actual_java_or_d8_executed=False, android_executed=False,
               target_source_modified=False, reviewed_source_bytes_unchanged=True,
               wrong_acceptances=4, rejecting_negative_controls=3,
               exact_positive_restoration=True, results=results)
dump(OUTPUT / 'result.json', summary)
print(json.dumps(summary))
