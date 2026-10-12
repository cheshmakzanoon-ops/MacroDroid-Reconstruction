#!/usr/bin/env python3
"""Check only design consistency and freeze its small immutable review capsule."""
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def save(name, value):
    with (ROOT / name).open('xb') as stream:
        stream.write(json.dumps(value, indent=2).encode() + b'\n')


def main():
    protocol = json.loads((ROOT / 'protocol.json').read_bytes())
    assert protocol['active_files'] == []
    assert protocol['android_execution_authorized_by_this_capsule'] is False
    assert [(s['condition'], s['apk'], s['animator_duration_scale']) for s in protocol['slots']] == [
        ('A', 'original', '0'), ('A', 'candidate', '0'), ('A', 'candidate', '0'), ('A', 'original', '0'),
        ('B', 'original', '1'), ('B', 'candidate', '1'), ('B', 'candidate', '1'), ('B', 'original', '1')]
    assert [s['index'] for s in protocol['slots']] == list(range(1, 9))
    schedule = protocol['schedule']
    assert schedule['sample_indices'] == list(range(5))
    assert schedule['post_input_wait_ns'] == 2_000_000_000
    assert schedule['inter_observation_wait_ns'] == 1_000_000_000
    assert schedule['gap_origin'] == 'previous_full_observation_completion'
    assert schedule['post_tap_full_frame_count'] == 8 * 5 == 40
    roles = protocol['comparison_roles']
    assert roles['per_condition_slot_pairs'] == [list(x) for x in itertools.combinations(range(4), 2)]
    assert roles['cross_run_pair_count'] == 2 * 5 * 6 == 60
    assert roles['temporal_sample_pairs'] == [[i, i + 1] for i in range(4)]
    assert roles['temporal_pair_count'] == 8 * 4 == 32
    assert roles['total_predetermined_pair_count'] == 60 + 32 == 92
    histories = json.loads((ROOT / 'evidence/fixed-historical-capture-bindings.json').read_bytes())
    assert [(x['run_id'], x['changed_pixels']) for x in histories] == [
        (38216299675, 5), (38221713675, 0), (38230072388, 26)]
    for h in histories:
        for obs in h['observations']:
            assert obs['tap']['argv'] == ['shell', 'input tap 640 1152']
            assert obs['tap']['returncode'] == 0 and obs['tap']['timed_out'] is False
            title = next(n for n in obs['intro2_nodes'] if n['resource-id'].endswith('/titleText'))
            assert title['text'] == 'TRIGGERS'
    for x in protocol['slots']:
        assert protocol['fixed_settings']['window_animation_scale'] == '0'
        assert protocol['fixed_settings']['transition_animation_scale'] == '0'
    older = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction/docs/verification/editor-journey/run-38205737183-attempt-1/analysis')
    older_cp = json.loads((older / 'checkpoint.json').read_bytes())
    declared = next(row for row in older_cp['files'] if row['path'] == 'README.md')
    old_readme = (older / 'README.md').read_bytes()
    assert identity(old_readme) == {key: declared[key] for key in ['bytes', 'sha256']}
    old_candidate = re.search(rb'candidate installed APK hash is `([0-9a-f]{64})`', old_readme)[1].decode()
    assert old_candidate == '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'
    read_verification = json.loads((ROOT / 'evidence/read-only-input-verification.json').read_bytes())
    for row in read_verification['files']:
        assert identity(Path(row['path']).read_bytes()) == {key: row[key] for key in ['bytes', 'sha256']}
    save('design-consistency.json', {
        'status': 'DESIGN_INVENTORY_AND_RECORDED_COORDINATES_CHECKED',
        'finished_utc': datetime.now(timezone.utc).isoformat(),
        'checks_are_implementation_tests': False, 'android_executed': False,
        'source_or_apk_changed': False, 'full_runtime_1_to_1_established': False,
        'planned_slots': 8, 'planned_post_tap_frames': 40,
        'planned_pair_comparisons': 92, 'observed_tap_coordinate': [640, 1152],
        'exact_read_inputs_rechecked': len(read_verification['files']),
        'additional_older_readme_binding': {'path': str(older / 'README.md'), **identity(old_readme)},
        'older_run_id': 38205737183, 'older_candidate_apk_sha256': old_candidate,
    })
    files = []
    for path in sorted(ROOT.rglob('*')):
        if path.is_dir():
            continue
        assert path.is_file() and not path.is_symlink()
        name = path.relative_to(ROOT).as_posix()
        assert name != 'checkpoint.json'
        files.append({'path': name, **identity(path.read_bytes()), 'mode': '100644'})
    save('checkpoint.json', {
        'schema': 1,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'FROZEN_DESIGN_ONLY_NO_ANDROID_ACTIVATION',
        'repo_target': 'work-in-progress/indicator-fixed-sampling/01-bounded-design',
        'active_files': [], 'new_android_execution': False,
        'new_apk_or_application_source': False, 'new_runtime_parity_credit': 0,
        'dossier_sha256': '00cde07343d7d7a106171070b462b4b2879705d3f926f6f22abcaae90a97fce3',
        'fixed_runtime_parent_commit': '6331410cfd2391389270564803623079e8355ad8',
        'files': files, 'file_count': len(files),
        'payload_bytes': sum(x['bytes'] for x in files),
    })
    cp = ROOT / 'checkpoint.json'
    print(json.dumps({'path': str(cp), **identity(cp.read_bytes()), 'files': len(files),
                      'payload_bytes': sum(x['bytes'] for x in files)}))


if __name__ == '__main__':
    main()
