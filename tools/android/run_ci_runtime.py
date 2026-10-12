#!/usr/bin/env python3
"""Capture and compare the original and candidate on a fresh disposable AVD.

This measures cold launches and four English intro page stills, with three
observed Next transitions. The device's three animation scales are explicitly
set to zero; motion parity is not measured. Each stage retains its own evidence
and exit code. No account or permission prompts are accepted here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tooling', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--acceleration', choices=['on', 'off', 'auto'], default='on')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = args.source.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    environment = output / 'environment'
    capture_device = output / 'capture-device'
    capture = output / 'capture'
    original, candidate = args.original.resolve(), args.candidate.resolve()
    report = {
        'scope': 'Exact cold launch, four English intro page stills, and three observed Next transitions only',
        'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'original_sha256': digest(original),
        'candidate_sha256': digest(candidate),
        'capture_device_configured': False,
        'systemui_demo_clock_requested': '1200',
        'zero_device_animation_scales_requested': True,
        'cold_launch_capture_equal': False,
        'intro_sequence_equal': False,
        'android_runtime_executed': False,
        'complete_intro_sequences_observed': False,
        'animation_parity_established': False,
        'full_runtime_1_to_1_established': False,
        'commands': [],
    }

    def save() -> None:
        (output / 'runtime-run.json').write_text(json.dumps(report, indent=2) + '\n')

    def run(label: str, argv: list[str], timeout: int) -> int:
        started = time.monotonic()
        entry = {'label': label, 'argv': argv}
        report['commands'].append(entry)
        try:
            result = subprocess.run(argv, timeout=timeout, check=False)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
            entry['error'] = 'Command exceeded its recorded deadline'
        entry.update(exit_code=code, seconds=round(time.monotonic() - started, 3))
        save()
        return code

    save()
    service = None
    try:
        with (output / 'service.log').open('w') as log:
            service = subprocess.Popen([
                sys.executable, '-u', str(here / 'android_runtime_service.py'),
                '--tooling', str(args.tooling.resolve()),
                '--evidence', str(environment), '--acceleration', args.acceleration,
            ], stdout=log, stderr=subprocess.STDOUT)
            ready = run('boot-readiness', [
                sys.executable, str(here / 'wait_android_ready.py'),
                '--evidence', str(environment), '--timeout', '900',
            ], 930)
            if ready:
                report['failure'] = 'boot-readiness'
                return ready
            configured = run('configure-and-observe-capture-device', [
                sys.executable, str(here / 'runtime_job.py'),
                '--queue', str(environment / 'queue'), '--timeout', '240',
                '--cwd', str(source), '--',
                sys.executable, str(here / 'configure_capture_device.py'),
                '--serial', 'emulator-5560', '--output', str(capture_device),
                '--demo-clock', '1200', '--disable-animations',
            ], 280)
            configuration_path = capture_device / 'capture-device.json'
            if configuration_path.is_file():
                configuration = json.loads(configuration_path.read_text())
                report['capture_device_configured'] = configuration.get('status') == 'CAPTURE_DEVICE_CONFIGURED'
                report['capture_device_status'] = configuration.get('status')
                report['capture_device_report_sha256'] = digest(configuration_path)
            save()
            if configured or not report['capture_device_configured']:
                report['failure'] = 'capture-device-configuration'
                return configured or 2
            captured = run('capture-original-and-candidate', [
                sys.executable, str(here / 'runtime_job.py'),
                '--queue', str(environment / 'queue'), '--timeout', '1800',
                '--cwd', str(source), '--',
                sys.executable, str(source / 'android_acceptance.py'),
                '--serial', 'emulator-5560', '--original', str(original),
                '--candidate', str(candidate), '--accept-package-data-removal',
                '--intro-pages',
                '--install-timeout', '600', '--launch-timeout', '180',
                '--ui-timeout', '120', '--output', str(capture),
            ], 1840)
            compared = run('compare-complete-captures', [
                sys.executable, str(source / 'android_compare.py'), str(capture),
            ], 120)
            comparison_path = capture / 'cold-launch-comparison.json'
            if comparison_path.is_file():
                comparison = json.loads(comparison_path.read_text())
                report['cold_launch_capture_equal'] = comparison.get('cold_launch_capture_equal') is True
                report['cold_launch_comparison_status'] = comparison.get('status')
                report['android_runtime_executed'] = comparison.get('android_runtime_executed') is True
                report['cold_launch_comparison_sha256'] = digest(comparison_path)
            intro_compared = run('compare-four-intro-pages-and-transitions', [
                sys.executable, str(source / 'android_intro.py'), str(capture),
            ], 120)
            intro_path = capture / 'intro-comparison.json'
            if intro_path.is_file():
                intro = json.loads(intro_path.read_text())
                report['intro_sequence_equal'] = intro.get('intro_sequence_equal') is True
                report['intro_comparison_status'] = intro.get('status')
                report['complete_intro_sequences_observed'] = intro.get('complete_intro_sequences_observed') is True
                report['intro_comparison_sha256'] = digest(intro_path)
            if captured or compared or intro_compared or not report['cold_launch_capture_equal'] or not report['intro_sequence_equal']:
                report['failure'] = 'capture-or-comparison'
                return captured or compared or intro_compared or 2
            return 0
    finally:
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
        # The emulator emits a transient ADB public key. Publish diagnostics with
        # just that key-bearing line omitted; never publish the AVD/ADB key files.
        boot_log = environment / 'emulator-boot.log'
        if boot_log.is_file():
            lines = boot_log.read_text(errors='replace').splitlines()
            sanitized = [line for line in lines
                         if 'adb_auth' not in line and 'adb.pubkey' not in line
                         and 'public key' not in line.lower()]
            (output / 'emulator-diagnostics.log').write_text('\n'.join(sanitized) + '\n')
            report['emulator_log_lines_omitted'] = len(lines) - len(sanitized)
        report['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        save()


if __name__ == '__main__':
    raise SystemExit(main())
