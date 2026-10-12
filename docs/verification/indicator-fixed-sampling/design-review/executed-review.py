#!/usr/bin/env python3
"""Bounded independent review of the frozen fixed indicator sampling design."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import stat
import xml.etree.ElementTree as ET

SOURCE = Path('/dev/shm/ink-indicator-fixed-sampling-design')
OUTPUT = Path('/dev/shm/macrodroid-indicator-design-review')
CHECKPOINT_SHA = 'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec'
PACKAGE = 'com.arlosoft.macrodroid'


def require(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'Input must be a regular non-symlink file: ' + str(path))
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': st.st_size, 'sha256': digest}


def save(name, value):
    path = OUTPUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def scan_source(checkpoint):
    records = []
    for row in checkpoint['files']:
        path = SOURCE / row['path']
        require(path.resolve().is_relative_to(SOURCE), 'Escaping design path')
        got = identity(path)
        mode = '100755' if path.stat().st_mode & 0o111 else '100644'
        require(got == {key: row[key] for key in ('bytes', 'sha256')} and mode == row['mode'],
                'Frozen design changed: ' + row['path'])
        records.append({'path': row['path'], 'mode': mode, **got})
    actual = sorted(p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file())
    require(actual == sorted(['checkpoint.json'] + [row['path'] for row in records]),
            'Unlisted design payload')
    require(len(records) == checkpoint['file_count'] == 15
            and sum(row['bytes'] for row in records) == checkpoint['payload_bytes'] == 172648,
            'Design payload inventory changed')
    return records


def main():
    OUTPUT.mkdir(exist_ok=False)
    shutil.copyfile(Path(__file__), OUTPUT / 'executed-review.py')
    started = datetime.now(timezone.utc).isoformat()
    cp_before = identity(SOURCE / 'checkpoint.json')
    require(cp_before == {'bytes': 3453, 'sha256': CHECKPOINT_SHA}, 'Design checkpoint changed')
    checkpoint = json.loads((SOURCE / 'checkpoint.json').read_text())
    before = scan_source(checkpoint)
    save('design-payloads-before.json', before)
    expected_reads = json.loads((SOURCE / 'evidence/read-only-input-verification.json').read_text())['files']
    read_before = []
    for row in expected_reads:
        got = identity(Path(row['path']))
        require(got == {key: row[key] for key in ('bytes', 'sha256')}, 'Changed bound read input: ' + row['path'])
        read_before.append({'path': row['path'], **got})
    require(len(read_before) == 69, 'Read-input inventory count changed')
    save('bound-read-inputs-before.json', read_before)
    protocol = json.loads((SOURCE / 'protocol.json').read_text())
    slots = protocol['slots']
    expected = [{'index': i + 1, 'condition': 'A' if i < 4 else 'B',
                 'apk': ('original', 'candidate', 'candidate', 'original')[i % 4],
                 'animator_duration_scale': '0' if i < 4 else '1'} for i in range(8)]
    require(slots == expected, 'The fixed installation sequence differs')
    timing = protocol['schedule']
    require(timing == {
        'post_launch_wait_ns': 4000000000, 'initial_observations_per_slot': 1,
        'fresh_preinput_observations_per_slot': 1, 'post_input_wait_ns': 2000000000,
        'post_input_wait_origin': 'tap_command_return', 'sample_indices': [0, 1, 2, 3, 4],
        'inter_observation_wait_ns': 1000000000,
        'gap_origin': 'previous_full_observation_completion',
        'actual_wait_and_operation_endpoints_retained': True,
        'image_dependent_selection_or_retry': False, 'post_tap_full_frame_count': 40},
        'Fixed capture schedule differs')
    roles = protocol['comparison_roles']
    require(roles['per_condition_slot_pairs'] == [list(x) for x in itertools.combinations(range(4), 2)]
            and roles['condition_slot_indices'] == {'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8]}
            and roles['temporal_sample_pairs'] == [[i, i + 1] for i in range(4)],
            'Predetermined comparison roles differ')
    cross = [{'condition': condition, 'sample': sample, 'slots': [left, right]}
             for condition, indices in roles['condition_slot_indices'].items()
             for sample in timing['sample_indices'] for left, right in itertools.combinations(indices, 2)]
    temporal = [{'slot': row['index'], 'samples': [i, i + 1]} for row in slots for i in range(4)]
    require(len(cross) == roles['cross_run_pair_count'] == 60
            and len(temporal) == roles['temporal_pair_count'] == 32
            and len(cross) + len(temporal) == roles['total_predetermined_pair_count'] == 92,
            'Comparison role counts differ')
    require(roles['whole_rgba_and_xml'] is True and roles['pixel_masks_or_tolerance'] is False
            and roles['additional_indicator_arrays_supply_parity_credit'] is False,
            'Design weakens exact comparison')
    save('independently-enumerated-pair-roles.json', {'cross_run': cross, 'temporal': temporal})
    observed = []
    for label in ('original', 'candidate'):
        path = SOURCE / ('evidence/observed-xml/' + label + '-intro1-preinput.xml')
        tree = ET.fromstring(path.read_bytes())
        nodes = list(tree.iter('node'))
        matches = [node for node in nodes if node.get('resource-id') == PACKAGE + ':id/button_next']
        require(len(matches) == 1, 'NEXT is not unique in the bound observation')
        node = matches[0]
        for key, value in {'class': 'android.widget.ImageButton', 'package': PACKAGE,
                           'content-desc': 'Next', 'clickable': 'true', 'enabled': 'true',
                           'bounds': '[592,1104][688,1200]'}.items():
            require(node.get(key) == value, 'Observed NEXT identity differs: ' + key)
        nums = [int(n) for n in re.findall(r'\d+', node.get('bounds'))]
        center = [(nums[0] + nums[2]) // 2, (nums[1] + nums[3]) // 2]
        require(center == protocol['single_input']['observed_center'] == [640, 1152], 'Observed center differs')
        require(any(n.get('text') == 'MACRODROID' and n.get('resource-id') == PACKAGE + ':id/titleText'
                    for n in nodes), 'Observed initial title differs')
        parents = {child: parent for parent in tree.iter() for child in parent}
        chain, current = [], node
        while current in parents:
            current = parents[current]
            chain.append({'tag': current.tag, 'attributes': dict(current.attrib)})
        observed.append({'label': label, 'xml': identity(path), 'node': dict(node.attrib),
                         'derived_center': center, 'ancestors': chain})
    save('independently-parsed-observed-next.json', observed)
    parent = json.loads((SOURCE / 'evidence/parent-bindings.json').read_text())
    require(parent['fetched_git_commit'] == '6331410cfd2391389270564803623079e8355ad8'
            and len(parent['files']) == len({r['path'] for r in parent['files']}) == 16
            and all(r['commit'] == parent['fetched_git_commit'] for r in parent['files']),
            'Parent pin declaration differs')
    require(checkpoint['active_files'] == [] and checkpoint['new_android_execution'] is False
            and protocol['android_execution_authorized_by_this_capsule'] is False,
            'Inactive design scope differs')
    after = scan_source(checkpoint)
    read_after = [{'path': r['path'], **identity(Path(r['path']))} for r in expected_reads]
    require(before == after and read_before == read_after and identity(SOURCE / 'checkpoint.json') == cp_before,
            'Reviewed inputs changed')
    save('design-payloads-after.json', after)
    save('bound-read-inputs-after.json', read_after)
    result = {'status': 'BOUNDED_INDICATOR_DESIGN_REVIEW_PASSED', 'passed': True,
              'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'reviewed_checkpoint': cp_before, 'payloads_rehashed': 15, 'bound_reads_rehashed': 69,
              'original_candidate_observed_targets_independently_parsed': 2,
              'planned_fresh_installs': 8, 'planned_full_post_input_frames': 40,
              'independently_enumerated_cross_run_roles': 60, 'independently_enumerated_temporal_roles': 32,
              'fixed_parent_pin_declarations_checked': 16, 'fetched_parent_blobs_reexecuted_by_this_review': False,
              'android_executed': False, 'implementation_controls_executed': False,
              'new_full_journey_or_pixel_comparisons_executed': False,
              'cause_or_universal_parity_established': False, 'all_reviewed_inputs_unchanged': True}
    save('review-result.json', result)
    (OUTPUT / 'README.md').write_text('# Independent fixed indicator design review\n\n'
        'The frozen eight-install design passes this bounded read-only review. The review rehashed all 15 design '
        'payloads and 69 bound local inputs before and after inspection; independently parsed both observed NEXT '
        'targets and their full ancestor chains; reconstructed the O/C/C/O order for scales 0 then 1; and '
        'enumerated all 60 cross-run and 32 temporal comparison roles. It checked the fixed completion-gap schedule '
        'and the 16 parent pin declarations. The agent\'s earlier fetched-Git verification remains the evidence '
        'for those parent blobs; this review did not fetch them again.\n\n'
        'This is a design review. It runs no Android actions, tests no future implementation, and makes no new '
        'pixel-parity or causal claim. The separate original and candidate full frames, failed slots, actual '
        'latencies, and all differences must remain visible in the eventual fixed diagnostic. The user\'s '
        'existing instruction authorizes the next inactive implementation and its disposable CI verification.\n')
    rows = []
    for path in sorted(OUTPUT.rglob('*')):
        if path.is_file():
            rows.append({'path': path.relative_to(OUTPUT).as_posix(), 'mode': '100644', **identity(path)})
    save('checkpoint.json', {'schema': 1, 'status': result['status'], 'repo_target':
         'docs/verification/indicator-fixed-sampling/design-review', 'files': rows,
         'file_count': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows),
         'active_files': [], 'new_android_execution': False})
    print(json.dumps({'output': str(OUTPUT), 'checkpoint': identity(OUTPUT / 'checkpoint.json'),
                      'files': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows), 'passed': True}))


if __name__ == '__main__':
    main()
