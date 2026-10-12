"""Replay preserved session artifacts with exact external and proposed policies."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent / 'MacroDroid-Reconstruction'
OUT = ROOT / 'external474-reports/02-actual-runtime-review'
RUNS = {
    38206460588: {'head': '934c6543dce0897975f52457717b3a70bd27ce00', 'bytes': 11576977,
                  'sha256': 'd22377dacd276c2c8ab2d52bfa639a912d1871c90757ebefc71af16d106cdff6', 'members': 2034,
                  'captured_post_sha256': '1637f23d6fed1cb3a7939562b6720fa4572a07c71c68e8f2aede145d92955336'},
    38208764356: {'head': '47458097056fd023bad8b47b6464978b0d02e85c', 'bytes': 7835649,
                  'sha256': 'a1ab0fe1f622e591eba1d41b80297b9593abcad76963ef5c46097a499aa1c72f', 'members': 1408,
                  'captured_post_sha256': '1191dedd5d233b14ad89c4978ef7f8c52ee2d0c47cc8650d21f79685f8a1b7d2'},
}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def worker(source, report, output):
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(source / 'tools/parity_journeys'), str(source / 'project')]
    import android_compare as proof
    import post_onboarding as session
    from supplied_reference_journey import load_plan
    result = session.compare_session(report.parent, json.loads(report.read_bytes()), load_plan(), proof)
    output.write_text(json.dumps(result, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker-source', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker_source:
        worker(args.worker_source, args.report, args.output)
        return
    OUT.mkdir(parents=True, exist_ok=False)
    source_manifest = json.loads((ROOT / 'external474-input-manifest.json').read_bytes())
    assert source_manifest['baseline_commit'] == RUNS[38208764356]['head']
    for row in source_manifest['all_copied_files']:
        assert meta((ROOT / 'external474-inputs' / row['path']).read_bytes()) == {k: row[k] for k in ('bytes', 'sha256')}
    source_pins = {}
    for label, dirname in (('external474', 'external474-inputs'), ('proposed', 'external474-worktree')):
        source_pins[label] = {name: meta((ROOT / dirname / 'tools/parity_journeys' / name).read_bytes())
                              for name in ('post_onboarding.py', 'session_evidence.py', 'editor_journey.py', 'supplied_reference_journey.py')}
    assert source_pins['external474']['session_evidence.py'] == source_pins['proposed']['session_evidence.py']
    summaries = []
    for run_id, pin in RUNS.items():
        archived = REPO / f'docs/verification/editor-journey/run-{run_id}-attempt-1'
        case = OUT / str(run_id)
        case.mkdir()
        archive = archived / 'evidence.zip'
        assert meta(archive.read_bytes()) == {k: pin[k] for k in ('bytes', 'sha256')}
        manifest = json.loads((archived / 'manifest.json').read_bytes())
        assert manifest['head_sha'] == pin['head'] and manifest['run_id'] == run_id
        members = {row['path']: row for row in manifest['members']}
        assert len(members) == len(manifest['members']) == pin['members']
        member_total = 0
        with zipfile.ZipFile(archive) as zipped, tempfile.TemporaryDirectory(prefix='session-runtime-review-', dir=ROOT) as temp:
            temporary = Path(temp)
            for info in zipped.infolist():
                name = info.filename
                relative = PurePosixPath(name)
                assert not relative.is_absolute() and '..' not in relative.parts and not info.is_dir()
            assert len(zipped.namelist()) == len(set(zipped.namelist())) == pin['members']
            assert set(zipped.namelist()) == set(members)
            for name, row in members.items():
                data = zipped.read(name)
                assert meta(data) == {k: row[k] for k in ('bytes', 'sha256')}
                member_total += len(data)
                if name.startswith('ci-editor/journey/'):
                    path = temporary / name
                    assert path.resolve().is_relative_to(temporary.resolve())
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
            assert meta(zipped.read('tools/parity_journeys/post_onboarding.py'))['sha256'] == pin['captured_post_sha256']
            if run_id == 38208764356:
                assert meta(zipped.read('tools/parity_journeys/session_evidence.py')) == source_pins['external474']['session_evidence.py']
            folder = temporary / 'ci-editor/journey'
            assert (folder / 'journey.json').read_bytes() == (archived / 'journey.json').read_bytes()
            report = json.loads((folder / 'journey.json').read_bytes())
            results = {}
            for label, dirname in (('external474', 'external474-inputs'), ('proposed', 'external474-worktree')):
                output = case / (label + '-replay.json')
                command = [sys.executable, str(Path(__file__).resolve()), '--worker-source', str(ROOT / dirname),
                           '--report', str(folder / 'journey.json'), '--output', str(output)]
                completed = subprocess.run(command, capture_output=True, timeout=120)
                (case / (label + '-stdout.log')).write_bytes(completed.stdout)
                (case / (label + '-stderr.log')).write_bytes(completed.stderr)
                assert completed.returncode == 0, completed.stderr.decode()
                results[label] = json.loads(output.read_bytes())
            historical = json.loads((archived / 'editor-session-comparison.json').read_bytes())
            continuous = json.loads((archived / 'comparison.json').read_bytes())
            if run_id == 38206460588:
                assert results['external474']['editor_session_equal'] is True
                assert results['external474']['evidence_identity_check']['unique_observation_files'] == 294
                assert results['proposed']['status'] == 'REJECTED' and results['proposed']['reason'] == "'session_observation'"
            else:
                assert results['external474'] == historical
                assert results['external474']['status'] == results['proposed']['status'] == 'REJECTED'
                assert results['external474']['reason'] == results['proposed']['reason'] == 'Incomplete run or changed environment'
            pairs = []
            for a, b in zip(report['runs'][0]['screens'], report['runs'][1]['screens']):
                assert a['name'] == b['name']
                if run_id == 38206460588 and a['name'] not in [s[0] for s in report['plan'][6:]]:
                    continue
                images, xmls = [], []
                for shot in (a, b):
                    for role in ('screenshot', 'hierarchy'):
                        record = shot['artifacts'][role]
                        assert meta((folder / record['path']).read_bytes()) == {k: record[k] for k in ('bytes', 'sha256')}
                    images.append(np.asarray(Image.open(io.BytesIO((folder / shot['artifacts']['screenshot']['path']).read_bytes())).convert('RGBA')))
                    xmls.append((folder / shot['artifacts']['hierarchy']['path']).read_bytes())
                assert images[0].shape == images[1].shape == (1280, 720, 4)
                pair = {'name': a['name'], 'changed_full_rgba_pixels': int(np.any(images[0] != images[1], axis=2).sum()),
                        'full_xml_bytes_equal': xmls[0] == xmls[1], 'original': a['artifacts'], 'candidate': b['artifacts']}
                pairs.append(pair)
            bad_pid = [item for item in report['commands'] if item['argv'] == ['shell', 'pidof com.arlosoft.macrodroid'] and item['returncode'] != 0]
            failed_commands = []
            for command in bad_pid:
                streams = {key: (folder / command[key]['path']).read_bytes() for key in ('stdout', 'stderr')}
                for key, data in streams.items():
                    assert meta(data) == {k: command[key][k] for k in ('bytes', 'sha256')}
                    (case / command[key]['path']).write_bytes(data)
                failed_commands.append({'command': command, 'stdout_empty': not streams['stdout'], 'stderr_empty': not streams['stderr']})
            preserved = []
            for name in ('ci-editor/lifecycle.log', 'ci-editor/host-tests.log'):
                if name in members:
                    data = zipped.read(name)
                    (case / Path(name).name).write_bytes(data)
                    preserved.append({'path': name, **meta(data)})
            rows = [{'label': run['label'], 'status': run['status'], 'current_step': run.get('current_step'),
                     'reason': run.get('reason'), 'screen_names': [shot['name'] for shot in run['screens']],
                     'transition_targets': [item['to'] for item in run['transitions']],
                     'environment_after_present': 'environment_after' in run,
                     'session_observation_count': sum('session_observation' in shot for shot in run['screens'])}
                    for run in report['runs']]
            summary = {'run_id': run_id, 'head_sha': pin['head'], 'workflow_conclusion': manifest['conclusion'],
                       'archive_repository_path': str(archived.relative_to(REPO) / 'evidence.zip'),
                       'archive': meta(archive.read_bytes()), 'verified_member_count': len(members), 'verified_member_bytes': member_total,
                       'journey': meta((folder / 'journey.json').read_bytes()), 'runs': rows, 'historical_session_result': historical,
                       'unchanged_continuous_startup_result': continuous, 'replays': results,
                       'independent_full_frame_pairs': pairs, 'failed_pid_commands': failed_commands,
                       'preserved_logs': preserved, 'new_android_execution_performed': False,
                       'new_chronology_policy_passed': False, 'full_runtime_1_to_1_established': False}
            (case / 'analysis.json').write_text(json.dumps(summary, indent=2) + '\n')
            summaries.append({'run_id': run_id, 'external474_status': results['external474']['status'],
                              'proposed_status': results['proposed']['status'], 'proposed_reason': results['proposed'].get('reason'),
                              'partial_or_scoped_full_pixel_vector': [p['changed_full_rgba_pixels'] for p in pairs],
                              'source_and_all_members_verified': True})
            print(json.dumps(summaries[-1], sort_keys=True), flush=True)
    result = {'schema': 1, 'status': 'PRESERVED_DEVICE_RESULTS_REPLAYED_WITH_SEPARATE_POLICIES',
              'source_pins': source_pins, 'runs': summaries, 'new_android_execution_performed': False,
              'new_chronology_gate_runtime_result': 'PENDING_FRESH_CAPTURE', 'active_repository_modified': False}
    (OUT / 'runtime-review.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
