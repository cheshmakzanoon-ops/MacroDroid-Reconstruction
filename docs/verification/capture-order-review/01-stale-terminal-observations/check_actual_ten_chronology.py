"""Read-only narrow chronology audit of the unchanged actual ten-screen ZIP."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
ZIP = ROOT / 'MacroDroid-Reconstruction/docs/verification/editor-journey/run-38205737183-attempt-1/evidence.zip'
OUT = ROOT / 'trigger-category-review/actual-ten-chronology.json'
raw = ZIP.read_bytes()
assert len(raw) == 15156144 and hashlib.sha256(raw).hexdigest() == 'f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca'
with zipfile.ZipFile(ZIP) as archive:
    report_name = next(name for name in archive.namelist() if name.endswith('/journey/journey.json'))
    folder = str(PurePosixPath(report_name).parent)
    report_raw = archive.read(report_name)
    report = json.loads(report_raw)
    def artifact(record):
        name = PurePosixPath(record['path'])
        assert not name.is_absolute() and '..' not in name.parts
        data = archive.read(folder + '/' + name.as_posix())
        assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
        return data
    ledgers = set()
    observations = set()
    transitions = []
    for run in report['runs']:
        assert len(run['screens']) == 10 and len(run['transitions']) == 9 and run['status'] == 'COMPLETE'
        for shot in run['screens'] + [transition['before'] for transition in run['transitions']]:
            path = PurePosixPath(shot['settling']['path']).as_posix()
            assert path not in ledgers
            ledgers.add(path)
            event = json.loads(artifact(shot['settling']))
            for observation in event['attempts']:
                for record in observation['artifacts'].values():
                    path = PurePosixPath(record['path']).as_posix()
                    artifact(record)
                    assert path not in observations
                    observations.add(path)
        for transition, shot in zip(run['transitions'], run['screens'][1:]):
            ledger = json.loads(artifact(shot['settling']))
            finished = transition['command']['finished_monotonic']
            started = ledger['started_monotonic']
            assert finished <= started
            transitions.append(dict(label=run['label'], target=shot['name'], input_finished=finished,
                                    next_acquisition_started=started, elapsed_seconds=started-finished))
result = dict(scope='Only actual capture uniqueness and post-input ordering; no new comparator or Android execution',
              run_id=38205737183, archive_sha256=hashlib.sha256(raw).hexdigest(),
              journey_sha256=hashlib.sha256(report_raw).hexdigest(), accepted_ledgers=38,
              unique_observation_artifact_paths=len(observations), transitions_checked=len(transitions),
              all_accepted_ledgers_unique=len(ledgers)==38,
              all_next_captures_started_after_input_completed=True,
              rows=transitions, historical_comparison_unchanged='JOURNEY_DIFFERENCE',
              android_executed_by_audit=False, full_runtime_1_to_1_established=False)
OUT.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key:value for key,value in result.items() if key != 'rows'}, indent=2))
