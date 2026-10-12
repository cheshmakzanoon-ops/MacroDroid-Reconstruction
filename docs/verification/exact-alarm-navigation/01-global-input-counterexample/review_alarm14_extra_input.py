"""Replay the full synthetic alarm14 report before/after one unplanned input."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import sys
import tarfile
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(exist_ok=False)
(args.output / 'temporary').mkdir()
tempfile.tempdir = str(args.output / 'temporary')
sys.dont_write_bytecode = True
sys.path[:0] = [str(args.source / 'tools/parity_journeys'), str(args.source / 'project')]


def inventory(root):
    rows = []
    for path in sorted(root.rglob('*')):
        if path.is_dir():
            continue
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode)
        data = path.read_bytes()
        rows.append(dict(path=path.relative_to(root).as_posix(), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest(), mode=stat.S_IMODE(mode)))
    return rows


def write(name, value):
    (args.output / name).write_text(json.dumps(value, indent=2) + '\n')


def archive(root, rows, filename):
    with tarfile.open(args.output / filename, 'w:gz', format=tarfile.PAX_FORMAT) as out:
        for row in rows:
            data = (root / row['path']).read_bytes()
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
            info = tarfile.TarInfo(row['path'])
            info.size = len(data)
            info.mode = row['mode']
            info.mtime = 0
            import io
            out.addfile(info, io.BytesIO(data))


source_before = inventory(args.source)
write('source-files.json', source_before)
print(json.dumps({'stage': 'source-pinned', 'files': len(source_before)}), flush=True)
import test_exact_alarm_journey as test

with test.alarm.configured_plan():
    fixture = test.FourteenFixture()
    try:
        test.add_readiness(fixture)
        original = copy.deepcopy(fixture.report)
        write('positive-report.json', original)
        positive = fixture.result()
        write('positive-comparison.json', positive)
        assert positive['journey_equal'] is True and positive['settings_inputs'] == 0
        print(json.dumps({'stage': 'positive', 'status': positive['status'], 'journey_equal': True}), flush=True)
        last = max(row['finished_monotonic'] for row in fixture.report['commands'])
        for run in fixture.report['runs']:
            for shot in run['screens']:
                last = max(last, json.loads(test.proof.artifact(fixture.folder, shot['settling']))['finished_monotonic'])
        extra = copy.deepcopy(fixture.report['commands'][-1])
        extra.update(argv=['shell', 'input tap 20 20'], returncode=0, timed_out=False,
                     started_utc='2026-10-12T10:00:00.000000+00:00',
                     started_monotonic=last + 10, finished_monotonic=last + 10.01,
                     timeout_seconds=10,
                     stdout=fixture.put('candidate-unplanned-settings-input.stdout.log', b''),
                     stderr=fixture.put('candidate-unplanned-settings-input.stderr.log', b''))
        fixture.report['commands'].append(extra)
        write('appended-input.json', extra)
        write('extra-input-report.json', fixture.report)
        mutated = fixture.result()
        write('extra-input-comparison.json', mutated)
        assert mutated['journey_equal'] is True and mutated['settings_inputs'] == 0
        assert mutated == positive
        print(json.dumps({'stage': 'counterexample', 'status': mutated['status'],
                          'journey_equal': True, 'reported_settings_inputs': mutated['settings_inputs']}), flush=True)
        # Preserve a fast rejecting control at the global-ledger boundary itself.
        malformed = copy.deepcopy(fixture.report)
        malformed['commands'][-1]['started_monotonic'] = malformed['commands'][-2]['started_monotonic'] - 1
        rejection = None
        try:
            test.ready.verify_report(fixture.folder, malformed, test.proof)
        except test.runner.JourneyError as error:
            rejection = str(error)
        assert rejection == 'Global command ledger is not chronological and nonoverlapping'
        write('chronology-negative-control.json', dict(scope='Direct readiness.verify_report boundary', rejected=True, reason=rejection))
        fixture.report = copy.deepcopy(original)
        assert fixture.report == original
        evidence = inventory(fixture.folder)
        write('artifact-members.json', evidence)
        archive(fixture.folder, evidence, 'synthetic-artifacts.tar.gz')
        summary = dict(schema=1, status='WHOLE_SYNTHETIC_REPORT_ACCEPTED_ONE_UNPLANNED_SETTINGS_INPUT',
                       completed_utc=datetime.now(timezone.utc).isoformat(),
                       plan_sha256=test.alarm.PLAN_SHA256, report_schema=test.alarm.REPORT_SCHEMA,
                       positive_status=positive['status'], positive_journey_equal=True,
                       changed_global_commands=1, command_argv=extra['argv'],
                       added_command_chronological_after_all_terminal_captures=True,
                       mutated_result_exactly_equals_positive=True,
                       reported_settings_inputs=mutated['settings_inputs'],
                       chronology_negative_control_rejected=True,
                       report_object_restored_exactly=True,
                       synthetic_artifact_members=len(evidence),
                       actual_android_or_input_executed=False,
                       full_runtime_1_to_1_established=False)
        write('result.json', summary)
    finally:
        fixture.close()
assert inventory(args.source) == source_before
archive(args.source, source_before, 'reviewed-source.tar.gz')
write('source-after-check.json', dict(files=len(source_before), exact_bytes_and_modes_unchanged=True))
(args.output / 'review_alarm14_extra_input.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(summary), flush=True)
