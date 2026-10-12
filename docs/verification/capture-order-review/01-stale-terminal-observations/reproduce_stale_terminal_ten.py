"""Reproduce a stale post-input observation for the existing ten-screen policy using only frozen synthetic tests."""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys

ROOT = Path('/workspace/scratch/4130730d15aa')
SOURCE = ROOT / 'trigger-catalog-forward/checkpoints/02-reviewed-host-success'
OUT = ROOT / 'trigger-category-review/ten-screen'
OUT.mkdir(exist_ok=False)
sys.dont_write_bytecode = True
raw = (SOURCE / 'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '4e3d1ec8d3eec36d6db4685fef8d827c84b4c38e2c550e4a9896fba46eb90f92'
cp = json.loads(raw)
for row in cp['files']:
    data = (SOURCE / row['path']).read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
sys.path.insert(0, str(SOURCE / 'replay-source/tools/parity_journeys'))
import favourite_info_journey as category
from test_observed_journey import ObservedFixture

with category.configured_plan():
    fixture = ObservedFixture()
    try:
        baseline = fixture.result()
        assert baseline['journey_equal'] is True, baseline
        original = copy.deepcopy(fixture.report)
        removed = []
        chronology = []
        for run in fixture.report['runs']:
            prior, terminal = run['screens'][-2], run['screens'][-1]
            ledger_path = terminal['settling']['path']
            ledger = json.loads((fixture.folder / ledger_path).read_text())
            old_paths = {row['path'] for frame in ledger['attempts'] for row in frame['artifacts'].values()}
            old_paths.add(ledger_path)
            for name in sorted(old_paths):
                path = fixture.folder / name
                data = path.read_bytes()
                removed.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
                path.unlink()
            fixture.report['capture_events'] = [row for row in fixture.report['capture_events'] if row['path'] != ledger_path]
            substitute = copy.deepcopy(prior)
            substitute['name'] = terminal['name']
            run['screens'][-1] = substitute
            tap = run['transitions'][-1]['command']
            chronology.append(dict(label=run['label'], reused_observation_finished=substitute['observation']['finished_monotonic'],
                                   terminal_input_started=tap['started_monotonic'], terminal_input_finished=tap['finished_monotonic']))
            assert substitute['observation']['finished_monotonic'] < tap['started_monotonic']
        result = fixture.result()
        assert result['journey_equal'] is True, result
        assert result['status'] == 'EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY', result
        assert all(item['surface_after_one_observed_ok'] is True for item in result['terminal_surfaces'])
        (OUT / 'original-synthetic-report.json').write_text(json.dumps(original, indent=2) + '\n')
        (OUT / 'mutated-synthetic-report.json').write_text(json.dumps(fixture.report, indent=2) + '\n')
        (OUT / 'mutated-result.json').write_text(json.dumps(result, indent=2) + '\n')
        (OUT / 'removed-post-input-artifacts.json').write_text(json.dumps(removed, indent=2) + '\n')
        shutil.copytree(fixture.folder, OUT / 'synthetic-artifacts')
        summary = dict(status='STALE_POST_INPUT_TERMINAL_FALSE_POSITIVE_REPRODUCED',
                       frozen_source_checkpoint_sha256=hashlib.sha256(raw).hexdigest(),
                       source_files_verified=len(cp['files']), baseline_accepted=True,
                       mutated_comparator_accepted=True, original_terminal_artifacts_removed=len(removed),
                       chronology=chronology, android_executed=False, active_source_modified=False,
                       reason='Both terminal frames and acquisition ledgers are reused from before the final OK tap. The comparator does not require unique capture use or a post-input observation timestamp.')
        (OUT / 'review-result.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary, indent=2))
    finally:
        fixture.close()
for row in cp['files']:
    data = (SOURCE / row['path']).read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
