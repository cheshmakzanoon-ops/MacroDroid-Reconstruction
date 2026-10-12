#!/usr/bin/env python3
"""Replay the exact failed hosted policy and its surviving evidence, without ADB."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True

HEAD = '3edcddd86660ea10c8aff71b651b446f86412525'
PACKAGE = 'work-in-progress/animation-diagnostic/03-reviewed-workflow'
SOURCE_PINS = {
    '.github/workflows/editor-normal-animation.yml': '5bcd73aa15e5ad05de1fbcdf6252292249bf48458520bd6866477cd343af7047',
    PACKAGE + '/prepare_normal_journey.py': '0f700854dfc608607e018776bfcb7fd7f66a3e413d4fb6ab61dc95585e215148',
    PACKAGE + '/verify_normal_journey.py': '521142186545b216bab1a7fd804e7cf2e155ca1a74899bdf77e0467d14c9ad44',
}
APKS = [
    ('MacroDroid-5.67.8-original.apk', 95725918, '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    ('MacroDroid-5.67.8-current-hybrid.apk', 94683497, '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'),
]


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def verify_inventory(folder, receipt):
    expected = {row['path']: {key: row[key] for key in ('bytes', 'sha256')} for row in receipt['files']}
    assert len(expected) == 952
    actual = {p.relative_to(folder).as_posix(): identity(p) for p in folder.rglob('*') if p.is_file()}
    assert actual == expected
    assert all(not p.is_symlink() for p in folder.rglob('*'))
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    artifact = args.artifact.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, output / 'executed-replay-script.py')
    started = datetime.now(timezone.utc).isoformat()
    receipt = json.loads(args.receipt.read_text())
    assert receipt['run_id'] == 38212813248 and receipt['head_sha'] == HEAD
    inventory = verify_inventory(artifact, receipt)
    apks = [args.original.resolve(), args.candidate.resolve()]
    for path, (_, size, digest) in zip(apks, APKS):
        assert identity(path) == {'bytes': size, 'sha256': digest}
    for name, digest in SOURCE_PINS.items():
        assert identity(artifact / 'executed-inputs' / name)['sha256'] == digest

    # The literal verifier writes one result. A private hardlink tree keeps all
    # inputs exact while that one destination is an independent copied inode.
    # No file in the downloaded artifact or application source tree is opened
    # for writing; only this invocation's temporary directory is removed.
    with tempfile.TemporaryDirectory(prefix='macrodroid-normal03-replay-') as temporary:
        root = Path(temporary) / 'root'
        shadow = Path(temporary) / 'artifact'
        for source in (artifact / 'executed-inputs').rglob('*'):
            if source.is_file():
                target = root / source.relative_to(artifact / 'executed-inputs')
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(source, target)
        for source in artifact.rglob('*'):
            if source.is_file():
                target = shadow / source.relative_to(artifact)
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.relative_to(artifact).as_posix() == 'normal-animation-verification.json':
                    shutil.copyfile(source, target)
                else:
                    os.link(source, target)
        for path, (name, _, _) in zip(apks, APKS):
            target = root / 'workspace/artifacts' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(path, target)

        sys.path[:0] = [str(root / PACKAGE)]
        import prepare_normal_journey as preparation
        import verify_normal_journey as normal
        preflight = json.loads((shadow / 'input-preflight.json').read_text())
        expected_inputs = preparation.verify_prepared_inputs(root, shadow, preflight)
        assert len(expected_inputs) == 190 and preflight['github_sha'] == HEAD
        write(output / 'independently-reconstructed-190-inputs.json', expected_inputs)

        literal = normal.verify(root, shadow)
        captured_normal = json.loads((artifact / 'normal-animation-verification.json').read_text())
        without_time = lambda value: {k: v for k, v in value.items() if k != 'verified_at_utc'}
        assert without_time(literal) == without_time(captured_normal)
        assert literal['status'] == 'NORMAL_ANIMATION_EVIDENCE_INCOMPLETE'
        assert literal['reason'] == 'ValueError: Configuration and complete journey are not in order'
        write(output / 'literal-normal-verifier-replay.json', literal)

        import enable_normal_animations as scales
        import favourite_info_journey as favourite
        import editor_journey as runner
        import observed_journey as observed
        import android_compare as proof

        settings = json.loads((shadow / 'animation-settings/animation-scales.json').read_text())
        assert scales.verify_report(shadow / 'animation-settings', settings) == {key: '1' for key in scales.SCALES}
        assert len(settings['commands']) == 19 and settings['android_executed'] is True
        journey_folder = shadow / 'journey'
        report = json.loads((journey_folder / 'journey.json').read_text())
        with favourite.configured_plan():
            replayed = runner.compare(journey_folder, report, proof)
            assert replayed == json.loads((artifact / 'journey/comparison.json').read_text())
            assert replayed['status'] == 'REJECTED' and not replayed['journey_equal']
            write(output / 'literal-journey-comparison-replay.json', replayed)
            snapshots, states, identities, used = [], [], [], set()
            # Failure remains a failure. These checks account for the exact
            # earlier observation/input records without fabricating completion.
            for run in report['runs']:
                label = run['label']
                code, out, err = proof.command_output(journey_folder, run['absence'])
                assert proof.absence_ok(code, out, err)
                assert proof.install_ok(*proof.command_output(journey_folder, run['install']))
                installed_path = proof.installed_path(*proof.command_output(journey_folder, run['installed_path']))
                installed = proof.installed_digest(*proof.command_output(journey_folder, run['installed_checksum']), installed_path)
                assert installed == run['apk_sha256']
                code, out, err = proof.command_output(journey_folder, run['launch'])
                assert not err.strip() and proof.launch_ok(code, out)
                prior = run['screens'][0]
                transition = run['transitions'][0]
                states.append(observed.stable_snapshot(journey_folder, prior, proof, label))
                expected_component = observed.input_identity(journey_folder, prior, transition['before'],
                    transition['action'], transition['to'], proof, label)
                observed.verify_preinput(journey_folder, transition, proof)
                runner.evidence_command(journey_folder, transition['command'], proof, clean=True)
                assert prior['observation']['started_monotonic'] > run['launch']['finished_monotonic']
                assert transition['before']['observation']['started_monotonic'] > prior['observation']['finished_monotonic']
                tap_end = transition['command']['finished_monotonic']
                observed_ids = set()
                for event in report['capture_events']:
                    if not event['path'].startswith(label + '-'):
                        continue
                    ledger = json.loads(proof.artifact(journey_folder, event))
                    for attempt in ledger['attempts']:
                        state, pid, front = observed.observation(journey_folder, attempt, proof)
                        assert front == expected_component
                        observed_ids.add((pid, front))
                        for record in attempt['artifacts'].values():
                            path = (journey_folder / record['path']).resolve()
                            stat = path.stat()
                            token = (stat.st_dev, stat.st_ino)
                            assert token not in used
                            used.add(token)
                        if event['path'] == label + '-intro-2-acquisition-1-settling.json':
                            assert attempt['observation']['started_monotonic'] > tap_end
                        snapshots.append({'label': label, 'ledger': event['path'],
                            'screenshot': attempt['artifacts']['screenshot'], 'pid': pid,
                            'component': front, 'observation': attempt['observation'],
                            'width': state[1], 'height': state[2]})
                assert len(observed_ids) == 1
                identities.append({'label': label, 'installed_sha256': installed,
                    'installed_path': installed_path, 'observed_pid': next(iter(observed_ids))[0],
                    'observed_component': expected_component, 'input_command': transition['command']['argv'],
                    'input_freshness_seconds': transition['precondition_age_seconds']})
            assert len(snapshots) == 19 and len(used) == 114
            assert states[0] == states[1]
            write(output / 'verified-partial-observations.json', {'snapshots': snapshots,
                'identities': identities, 'physical_observation_files': len(used),
                'accepted_intro1_full_state_equal': True, 'ten_screen_run_complete': False})

        device = json.loads((shadow / 'device/capture-device.json').read_text())
        device_commands = []
        for command in device['commands']:
            assert command['exit_code'] == 0
            for stream in ('stdout', 'stderr'):
                proof.artifact(shadow / 'device', command[stream])
            device_commands.append({'label': command['label'], 'argv': command['argv'],
                                    'exit_code': command['exit_code'], 'seconds': command['seconds']})
        assert len(device_commands) == 37
        write(output / 'verified-configuration-summary.json', {
            'normal_animation_commands_verified': 19, 'normal_animation_streams_verified': 38,
            'observed_scales': settings['observed_scales'], 'device_commands_verified': device_commands,
            'device_configuration_status': device['status'], 'demo_clock_requested': device['demo_clock_requested'],
            'confirmed_primary_signal': device['confirmed_primary_signal'],
            'signal_stable_seconds': device['signal_stable_seconds'],
            'systemui_demo_mode_observed': device['systemui_demo_mode_observed'],
            'environment_pair_equal_before_capture': report['runs'][0]['environment'] == report['runs'][1]['environment'],
            'environment_after_not_captured': all('environment_after' not in run for run in report['runs']),
        })

        host = []
        for name, count in [('journey-host-tests.log', 130), ('animation-host-tests.log', 9), ('download-tests.log', 6)]:
            log = (artifact / name).read_text()
            summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', log, re.MULTILINE)
            tests = re.findall(r'^test_\S+ \(.*\) \.\.\. ', log, re.MULTILINE)
            successes = len(re.findall(r'(?:\.\.\. |^)ok$', log, re.MULTILINE))
            assert len(summaries) == 1 and int(summaries[0][0]) == len(tests) == successes == count
            assert log.rstrip().endswith('\nOK')
            host.append({'path': name, **identity(artifact / name), 'tests': count,
                         'seconds': float(summaries[0][1]), 'individual_successes': successes})
        write(output / 'verified-host-test-summaries.json', host)
        imported = {}
        for module in (preparation, normal, scales, favourite, runner, observed, proof):
            path = Path(module.__file__).resolve()
            relative = str(path.relative_to(root)) if path.is_relative_to(root) else 'artifact/' + str(path.relative_to(shadow))
            imported[module.__name__] = {'private_replay_path': relative, **identity(path)}

    assert verify_inventory(artifact, receipt) == inventory
    for path, (_, size, digest) in zip(apks, APKS):
        assert identity(path) == {'bytes': size, 'sha256': digest}
    result = {'schema': 1, 'status': 'EXACT_FAILED_NORMAL03_EVIDENCE_REPLAYED',
        'run_id': 38212813248, 'head_sha': HEAD, 'started_utc': started,
        'finished_utc': datetime.now(timezone.utc).isoformat(), 'raw_files_verified_unchanged': 952,
        'independently_reconstructed_pinned_inputs': 190, 'source_pins': SOURCE_PINS,
        'imported_modules': imported, 'literal_normal_verifier_result_reproduced_except_replay_timestamp': True,
        'literal_journey_comparison_object_reproduced': True, 'observations_verified': 19,
        'distinct_physical_observation_artifacts': 114, 'fresh_inputs_verified': 2,
        'normal_animation_commands_verified': 19, 'device_configuration_command_streams_verified': 74,
        'host_tests_already_executed_on_runner': sum(row['tests'] for row in host),
        'new_host_tests_run': 0, 'android_commands_executed_by_replay': 0,
        'raw_artifacts_or_application_inputs_modified': False, 'temporary_replay_tree_removed': True,
        'recorded_incomplete_result_retained': True, 'ten_screen_parity_established': False,
        'animation_timing_parity_established': False, 'full_runtime_1_to_1_established': False}
    write(output / 'replay-result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_pins', 'imported_modules')}, indent=2))


if __name__ == '__main__':
    main()
