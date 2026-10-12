#!/usr/bin/env python3
"""Capture scoped app surfaces and run an independent constructor probe on ART.

All three capture comparators run even after an earlier stage fails. The ART
probe uses its own DEX and the unchanged original APK; its result neither grants
capture parity nor suppresses capture. No permission choice is made here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from android_constructor_probe import (DEFAULT_AVD, EXPECTED_DEVICE, ORIGINAL_SHA256,
                                       PROBE_SHA256, verify_result)

SERIAL = 'emulator-5560'
COMPARISONS = [
    ('cold_launch', 'compare-complete-cold-captures', 'android_compare.py',
     'cold-launch-comparison.json', 'cold_launch_capture_equal', 'EXACT_COLD_LAUNCH_MATCH_ONLY'),
    ('intro', 'compare-four-intro-pages-and-transitions', 'android_intro.py',
     'intro-comparison.json', 'intro_sequence_equal', 'EXACT_FOUR_PAGE_INTRO_MATCH_ONLY'),
    ('post_intro', 'compare-first-surface-after-intro', 'android_post_intro.py',
     'post-intro-comparison.json', 'post_intro_surface_equal', 'EXACT_POST_INTRO_SURFACE_MATCH_ONLY'),
]


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run_ci(args, *, runner=None, starter=None, here=None) -> tuple[int, dict]:
    runner = runner or subprocess.run
    starter = starter or subprocess.Popen
    here = here or Path(__file__).resolve().parent
    source = args.source.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    environment, capture_device = output / 'environment', output / 'capture-device'
    capture, probe, stages = output / 'capture', output / 'constructor-probe', output / 'stages'
    capture.mkdir()
    stages.mkdir()
    original, candidate = args.original.resolve(), args.candidate.resolve()
    report = {
        'schema_version': 2,
        'scope': 'Cold launch, four English intro stills, first surface after one completion tap, and separate ART constructor allocation',
        'status': 'INCOMPLETE',
        'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'original_sha256': None, 'candidate_sha256': None,
        'serial': SERIAL, 'expected_avd': DEFAULT_AVD,
        'boot_ready': False, 'capture_device_configured': False,
        'systemui_demo_clock_requested': '1200',
        'zero_device_animation_scales_requested': True,
        'post_intro_requested': True,
        'constructor_probe_sha256': PROBE_SHA256,
        'cold_launch_capture_equal': False, 'intro_sequence_equal': False,
        'post_intro_surface_equal': False,
        'android_runtime_executed': False,
        'installed_apk_identities_verified': False,
        'complete_intro_sequences_observed': False,
        'complete_post_intro_captures_observed': False,
        'requested_capture_gate_passed': False,
        'constructor_allocation_on_art_verified': False,
        'constructor_probe_gate_passed': False,
        'all_requested_runtime_checks_passed': False,
        'animation_parity_established': False,
        'home_feature_parity_established': False,
        'full_runtime_1_to_1_established': False,
        'commands': [], 'failures': [], 'report_errors': {},
    }
    captured = None
    service = None

    def save() -> None:
        temporary = output / 'runtime-run.json.tmp'
        temporary.write_text(json.dumps(report, indent=2) + '\n')
        temporary.replace(output / 'runtime-run.json')

    def run(label: str, argv: list[str], timeout: int) -> int:
        started = time.monotonic()
        entry = {'label': label, 'argv': argv, 'timeout_seconds': timeout,
                 'exit_code': None, 'timed_out': False}
        report['commands'].append(entry)
        save()
        stdout_path, stderr_path = stages / (label + '.stdout.txt'), stages / (label + '.stderr.txt')
        with stdout_path.open('wb') as out, stderr_path.open('wb') as err:
            try:
                result = runner(argv, stdout=out, stderr=err, timeout=timeout, check=False)
                code = result.returncode
                if type(code) is not int:
                    code = 125
                    entry['error'] = 'Command did not return an integer exit code'
            except subprocess.TimeoutExpired:
                code = 124
                entry.update(timed_out=True, error='Command exceeded its recorded deadline')
            except OSError as exc:
                code = 125
                entry['error'] = str(exc)
        for key, path in [('stdout', stdout_path), ('stderr', stderr_path)]:
            entry[key] = {'path': str(path.relative_to(output)), 'bytes': path.stat().st_size,
                          'sha256': digest(path)}
        entry.update(exit_code=code, seconds=round(time.monotonic() - started, 3))
        save()
        print(json.dumps({'stage': label, 'exit_code': code}), flush=True)
        return code

    def read_report(name: str, path: Path) -> dict:
        try:
            report[name + '_report_sha256'] = digest(path)
            value = json.loads(path.read_text())
            if not isinstance(value, dict):
                raise ValueError('Report root must be a JSON object')
            report[name + '_status'] = value.get('status')
            return value
        except (OSError, ValueError) as exc:
            report['report_errors'][name] = str(exc)
            return {}

    def queue(label, script, script_args, budget):
        return run(label, [
            sys.executable, str(here / 'runtime_job.py'),
            '--queue', str(environment / 'queue'), '--timeout', str(budget),
            '--cwd', str(source), '--', sys.executable, str(script), *script_args,
        ], budget + 40)

    save()
    try:
        report['original_sha256'], report['candidate_sha256'] = digest(original), digest(candidate)
        if report['original_sha256'] != ORIGINAL_SHA256 or report['candidate_sha256'] == ORIGINAL_SHA256:
            raise ValueError('Local original/candidate identities do not describe the reconstruction comparison')
        save()
        with (output / 'service.log').open('w') as log:
            service = starter([
                sys.executable, '-u', str(here / 'android_runtime_service.py'),
                '--tooling', str(args.tooling.resolve()), '--evidence', str(environment),
                '--acceleration', args.acceleration,
            ], stdout=log, stderr=subprocess.STDOUT)
        ready = run('boot-readiness', [
            sys.executable, str(here / 'wait_android_ready.py'),
            '--evidence', str(environment), '--timeout', '900',
        ], 930)
        state = read_report('boot', environment / 'runtime-status.json')
        properties = state.get('properties', {})
        report['boot_ready'] = (ready == 0 and state.get('state') == 'ready' and
            state.get('serial') == SERIAL and state.get('avd') == DEFAULT_AVD and
            isinstance(properties, dict) and all(properties.get(k) == v for k, v in EXPECTED_DEVICE.items()
                if k != 'ro.kernel.qemu'))
        if not report['boot_ready']:
            report['failures'].append('boot-readiness')
        else:
            configured = queue('configure-and-observe-capture-device', here / 'configure_capture_device.py', [
                '--serial', SERIAL, '--output', str(capture_device),
                '--demo-clock', '1200', '--disable-animations',
            ], 240)
            configuration = read_report('capture_device', capture_device / 'capture-device.json')
            report['capture_device_configured'] = (configured == 0 and
                configuration.get('status') == 'CAPTURE_DEVICE_CONFIGURED' and
                configuration.get('serial') == SERIAL and configuration.get('expected_avd') == DEFAULT_AVD and
                configuration.get('demo_clock_requested') == '1200' and
                configuration.get('disable_animations_requested') is True and
                configuration.get('requested_animation_scales_observed') is True)
            if not report['capture_device_configured']:
                report['failures'].append('capture-device-configuration')
            else:
                probed = queue('verify-independent-constructor-allocation-on-art', here / 'android_constructor_probe.py', [
                    '--adb', str(args.tooling.resolve() / 'android/platform-tools/adb'),
                    '--serial', SERIAL, '--original', str(original),
                    '--probe', str(here / 'probes/constructor-probe.dex'),
                    '--provenance', str(here / 'probes/constructor-probe.json'),
                    '--timeout', '120', '--output', str(probe),
                ], 780)
                proof = read_report('constructor_probe', probe / 'probe-result.json')
                try:
                    report['constructor_allocation_on_art_verified'] = verify_result(probe, proof, serial=SERIAL)
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    report['report_errors']['constructor_probe_validation'] = str(exc)
                report['constructor_probe_gate_passed'] = (probed == 0 and report['constructor_allocation_on_art_verified'] and
                    proof.get('cleanup_complete') is True and proof.get('status') == 'ART_CONSTRUCTOR_ALLOCATION_VERIFIED')
                if not report['constructor_probe_gate_passed']:
                    report['failures'].append('constructor-probe')
                save()
                # ART failure is independent. Always continue to the recorder.
                captured = queue('capture-original-and-candidate', source / 'android_acceptance.py', [
                    '--serial', SERIAL, '--original', str(original), '--candidate', str(candidate),
                    '--accept-package-data-removal', '--intro-pages', '--post-intro',
                    '--install-timeout', '600', '--launch-timeout', '180', '--ui-timeout', '120',
                    '--output', str(capture),
                ], 1800)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report['failures'].append('runtime-orchestration')
        report['orchestration_error'] = str(exc)
    finally:
        # Each comparator gets its own attempt and report, even after a failed
        # boot, configuration, probe, recorder, or earlier comparator.
        for prefix, label, script, filename, flag, success_status in COMPARISONS:
            code = run(label, [sys.executable, str(source / script), str(capture)], 120)
            result = read_report(prefix + '_comparison', capture / filename)
            bound = (result.get('apk_sha256') == [report['original_sha256'], report['candidate_sha256']] and
                     isinstance(report['candidate_sha256'], str) and report['original_sha256'] == ORIGINAL_SHA256)
            executed = bound and result.get('android_runtime_executed') is True
            complete = True
            if prefix == 'cold_launch':
                report['android_runtime_executed'] = executed
                report['installed_apk_identities_verified'] = executed and result.get('installed_apk_identities_verified') is True
                complete = report['installed_apk_identities_verified']
            elif prefix == 'intro':
                complete = executed and result.get('complete_intro_sequences_observed') is True
                report['complete_intro_sequences_observed'] = complete
            else:
                complete = executed and result.get('complete_post_intro_captures_observed') is True
                report['complete_post_intro_captures_observed'] = complete
            report[flag] = (code == 0 and executed and complete and result.get(flag) is True and
                            result.get('status') == success_status)
            if not report[flag]:
                report['failures'].append(prefix + '-comparison')
            save()
        report['capture_recorder_exit_code'] = captured
        report['requested_capture_gate_passed'] = (captured == 0 and report['capture_device_configured'] and
            all(report[entry[4]] for entry in COMPARISONS))
        if not report['requested_capture_gate_passed']:
            report['failures'].append('capture-or-comparison')
        if service is not None and service.poll() is None:
            stop = environment / 'queue' / 'STOP'
            stop.parent.mkdir(parents=True, exist_ok=True)
            stop.touch()
            try:
                service.wait(timeout=20)
            except subprocess.TimeoutExpired:
                service.terminate()
                try:
                    service.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    service.kill()
                    service.wait(timeout=5)
        if service is not None:
            report['service_exit_code'] = service.returncode
            if service.returncode != 0:
                report['failures'].append('runtime-service-exit')
        boot_log = environment / 'emulator-boot.log'
        if boot_log.is_file():
            lines = boot_log.read_text(errors='replace').splitlines()
            sanitized = [line for line in lines if 'adb_auth' not in line and 'adb.pubkey' not in line
                         and 'public key' not in line.lower()]
            (output / 'emulator-diagnostics.log').write_text('\n'.join(sanitized) + '\n')
            report['emulator_log_lines_omitted'] = len(lines) - len(sanitized)
        report['all_requested_runtime_checks_passed'] = (report['requested_capture_gate_passed'] and
            report['constructor_probe_gate_passed'] and not report['failures'])
        report['status'] = ('REQUESTED_RUNTIME_SCOPES_PASSED' if report['all_requested_runtime_checks_passed']
                            else 'REQUESTED_RUNTIME_SCOPES_INCOMPLETE_OR_DIFFERENT')
        report['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        save()
    return (0 if report['all_requested_runtime_checks_passed'] else 2), report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tooling', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--acceleration', choices=['on', 'off', 'auto'], default='on')
    args = parser.parse_args()
    return run_ci(args)[0]


if __name__ == '__main__':
    raise SystemExit(main())
