"""Read-only review of the frozen corrected guard with independent synthetic controls."""
from pathlib import Path
import copy
import hashlib
import json
import os
import sys
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
SOURCE = ROOT / 'trigger-catalog-forward/checkpoints/04-chronology-host-success'
OUT = ROOT / 'trigger-category-review/corrected-guard-review'
CHECKPOINT_SHA = '8aa91588f809c8dc7bfbf88aaf6d96a130fd72502f10076e94043c6e23dc23af'
OUT.mkdir(exist_ok=False)
sys.dont_write_bytecode = True
raw = (SOURCE / 'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == CHECKPOINT_SHA
checkpoint = json.loads(raw)

def verify_inputs():
    for row in checkpoint['files']:
        path = SOURCE / row['path']
        data = path.read_bytes()
        assert not path.is_symlink() and len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path']

verify_inputs()
sys.path.insert(0, str(SOURCE / 'replay-source/tools/parity_journeys'))
import favourite_info_journey as favourite
import trigger_category_journey as category
from test_observed_journey import ObservedFixture
from test_trigger_category_journey import TwelveFixture

def save(folder, name, value):
    (folder / name).write_text(json.dumps(value, indent=2) + '\n')

def archive_inputs(folder, fixture):
    members = []
    identities = {}
    archive_path = folder / 'synthetic-inputs.zip'
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(fixture.folder.rglob('*')):
            if not path.is_file():
                continue
            assert not path.is_symlink()
            name = path.relative_to(fixture.folder).as_posix()
            data = path.read_bytes()
            meta = path.stat()
            identities.setdefault((meta.st_dev, meta.st_ino), []).append(name)
            info = zipfile.ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
            members.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    with zipfile.ZipFile(archive_path) as archive:
        assert len(archive.namelist()) == len(members)
        for row in members:
            data = archive.read(row['path'])
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    save(folder, 'synthetic-members.json', members)
    save(folder, 'hardlink-identities.json', {'scope': 'Inert identity metadata; ZIP members flatten hard links into regular bytes.',
         'shared_inode_groups': [names for names in identities.values() if len(names) > 1]})

results = []
for length, fault in ((10, 'stale-terminal'), (12, 'stale-terminal'), (10, 'hardlink-preinput'), (12, 'hardlink-preinput')):
    folder = OUT / (str(length) + '-' + fault)
    folder.mkdir()
    context = favourite.configured_plan() if length == 10 else category.configured_plan()
    with context:
        fixture = ObservedFixture() if length == 10 else TwelveFixture()
        try:
            baseline = fixture.result()
            assert baseline['journey_equal'] is True and baseline['full_runtime_1_to_1_established'] is False, baseline
            save(folder, 'baseline-result.json', baseline)
            save(folder, 'original-report.json', fixture.report)
            evidence = []
            if fault == 'stale-terminal':
                for run in fixture.report['runs']:
                    prior, terminal = run['screens'][-2:]
                    ledger_path = terminal['settling']['path']
                    event = json.loads((fixture.folder / ledger_path).read_text())
                    names = {item['path'] for frame in event['attempts'] for item in frame['artifacts'].values()} | {ledger_path}
                    for name in sorted(names):
                        path = fixture.folder / name
                        data = path.read_bytes()
                        evidence.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
                        path.unlink()
                    fixture.report['capture_events'] = [item for item in fixture.report['capture_events'] if item['path'] != ledger_path]
                    substitute = copy.deepcopy(prior)
                    substitute['name'] = terminal['name']
                    assert substitute['observation']['finished_monotonic'] < run['transitions'][-1]['command']['started_monotonic']
                    run['screens'][-1] = substitute
                assert len(evidence) == 26
            else:
                earlier, later = fixture.candidate()['transitions'][-3], fixture.candidate()['transitions'][-1]
                left_record = earlier['preinput_artifacts']['pid']
                right_record = later['preinput_artifacts']['pid']
                left = fixture.folder / left_record['path']
                right = fixture.folder / right_record['path']
                assert left.resolve() != right.resolve() and left.read_bytes() == right.read_bytes()
                before = {'left': left.stat().st_ino, 'right': right.stat().st_ino}
                right.unlink()
                os.link(left, right)
                assert left.stat().st_ino == right.stat().st_ino
                evidence = dict(earlier=left_record, later=right_record, distinct_resolved_paths=True,
                                inode_before=before, inode_after=left.stat().st_ino,
                                recorded_report_or_hashes_modified=False)
            result = fixture.result()
            if fault == 'stale-terminal':
                assert result['journey_equal'] is False and 'Accepted acquisition ledger reused' in result['reason'], result
            save(folder, 'evidence-change.json', evidence)
            save(folder, 'mutated-report.json', fixture.report)
            save(folder, 'result.json', result)
            archive_inputs(folder, fixture)
            results.append(dict(length=length, fault=fault, baseline_accepted=True,
                                mutated_accepted=result['journey_equal'], status=result['status'], reason=result.get('reason'),
                                full_runtime_1_to_1_established=result['full_runtime_1_to_1_established']))
        finally:
            fixture.close()
verify_inputs()
summary = dict(checkpoint_sha256=CHECKPOINT_SHA, exact_source_files_verified=len(checkpoint['files']),
               prior_two_terminal_false_positives_rejected=True, android_executed=False, active_or_frozen_source_modified=False,
               results=results, hardlink_metadata_required_for_hardlink_replay=True)
save(OUT, 'review-result.json', summary)
print(json.dumps(summary, indent=2))
