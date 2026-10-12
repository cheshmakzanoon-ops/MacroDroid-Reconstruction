#!/usr/bin/env python3
"""Measure old/new VariableValue encodings using unchanged production host tests."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

BASE = Path(__file__).resolve().parent
PROJECT = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
OUT = BASE / 'reports/01-host-contract'
JDK = BASE.parent / 'tooling/jdk21/bin'
JAR = BASE.parent / 'current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar'
VARIABLE = 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): {'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    assert not OUT.exists()
    assert sha(JAR) == '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'
    before = {stem: inventory(PROJECT / stem) for stem in ('build/java/hostclasses', 'tools/classes')}
    OUT.mkdir(parents=True)
    (OUT / 'executed-driver.py').write_bytes(Path(__file__).read_bytes())
    (OUT / 'classpath-before.json').write_text(json.dumps(before, indent=2) + '\n')
    started = datetime.now(timezone.utc).isoformat()
    logs = []

    def run(name, argv, expected=0):
        at = datetime.now(timezone.utc).isoformat(); tick = time.monotonic()
        done = subprocess.run([str(s) for s in argv], cwd=OUT, capture_output=True, timeout=120)
        stdout, stderr = OUT / (name + '.stdout.log'), OUT / (name + '.stderr.log')
        stdout.write_bytes(done.stdout); stderr.write_bytes(done.stderr)
        row = {'name': name, 'argv': [str(s) for s in argv], 'started_utc': at,
               'ended_utc': datetime.now(timezone.utc).isoformat(), 'duration_seconds': time.monotonic() - tick,
               'timeout_seconds': 120, 'returncode': done.returncode,
               'stdout': {'path': stdout.name, 'bytes': stdout.stat().st_size, 'sha256': sha(stdout)},
               'stderr': {'path': stderr.name, 'bytes': stderr.stat().st_size, 'sha256': sha(stderr)}}
        logs.append(row)
        (OUT / 'commands.json').write_text(json.dumps(logs, indent=2) + '\n')
        assert done.returncode == expected, name + ': ' + done.stderr.decode(errors='replace')[-1000:]
        return done

    baseline = (BASE / 'overlay-01/baseline' / VARIABLE).read_bytes()
    candidate = (BASE / 'overlay-01/project' / VARIABLE).read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == '5953b3925539d215d3f32546d97280ed4403feeb5907909236ced0c5267831a1'
    variants = {'baseline': baseline, 'candidate': candidate,
                'nontransient-control': candidate.replace(b'private transient final', b'private final'),
                'wrong-alias-control': candidate.replace(b'intValue=v;', b'intValue=v+1;')}
    assert all(raw != candidate for name, raw in variants.items() if name != 'candidate')
    common = OUT / 'common'; common.mkdir()
    source_pins = {}
    for name in ('ParityTests', 'CoreParityTests', 'UiParityTests'):
        source = PROJECT / 'tests/java' / (name + '.java')
        target = common / source.name; shutil.copyfile(source, target)
        source_pins[str(source)] = sha(source)
    shutil.copyfile(BASE / 'VariableValueContractProbe.java', common / 'VariableValueContractProbe.java')
    common_classes = OUT / 'common-classes'; common_classes.mkdir()
    base_cp = ':'.join(map(str, [JAR, PROJECT / 'build/java/hostclasses', PROJECT / 'tools/classes']))
    run('compile-unchanged-encoders-and-probe', [JDK / 'javac', '-g:none', '-cp', base_cp, '-d', common_classes, *sorted(common.glob('*.java'))])
    for name, raw in variants.items():
        root = OUT / name; source = root / 'source/com/arlosoft/macrodroid/variables/VariableValue.java'
        source.parent.mkdir(parents=True); source.write_bytes(raw)
        classes = root / 'classes'; classes.mkdir()
        run(name + '-compile', [JDK / 'javac', '-g:none', '-d', classes, source])
        cp = ':'.join(map(str, [classes, common_classes, JAR, PROJECT / 'build/java/hostclasses', PROJECT / 'tools/classes']))
        check_aliases = name in ('candidate', 'wrong-alias-control')
        done = run(name + '-execute', [JDK / 'java', '-Xverify:all', '-Xmx500m', '-cp', cp,
                    'VariableValueContractProbe', root / 'contract.json', root / 'aliases.json', classes,
                    str(check_aliases).lower()], 1 if name == 'wrong-alias-control' else 0)
        if name == 'wrong-alias-control':
            assert b'Integer alias value drift' in done.stderr
    old = (OUT / 'baseline/contract.json').read_bytes()
    new = (OUT / 'candidate/contract.json').read_bytes()
    assert old == new
    assert (OUT / 'nontransient-control/contract.json').read_bytes() != old
    assert (OUT / 'wrong-alias-control/contract.json').read_bytes() == old
    assertions = json.loads((OUT / 'candidate/aliases.json').read_text())
    assert assertions == {'requested': True, 'checks': 21, 'passed': True}
    observed = json.loads(new)
    assert all(observed['existingIdentityContracts'].values())
    after = {stem: inventory(PROJECT / stem) for stem in before}
    assert after == before
    assert all(sha(Path(p)) == expected for p, expected in source_pins.items())
    (OUT / 'source-bindings.json').write_text(json.dumps(source_pins, indent=2) + '\n')
    report = {'schema': 1, 'status': 'VARIABLE_HOST_CONTRACT_REGRESSION_PASSED', 'passed': True,
              'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
              'baseline_source_sha256': hashlib.sha256(baseline).hexdigest(),
              'candidate_source_sha256': hashlib.sha256(candidate).hexdigest(),
              'encoding_files_byte_equal': True, 'encoding_sha256': hashlib.sha256(new).hexdigest(),
              'value_cases': observed['valueCases'], 'encoder_observations': observed['encoderObservations'],
              'alias_assertions': assertions['checks'], 'existing_identity_contracts': observed['existingIdentityContracts'],
              'nontransient_serialization_control_rejected': True,
              'wrong_alias_control_rejected_despite_equal_legacy_encoding': True,
              'commands': len(logs), 'classpath_files_rehashed_unchanged': sum(map(len, before.values())),
              'active_files_changed': [], 'scope': 'Existing constructors/public fields/identity equality, unchanged legacy/core/UI encoders, Gson and actual host event recorder; no Android object construction claim.'}
    (OUT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
