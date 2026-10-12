#!/usr/bin/env python3
"""Set and observe a fixed cellular signal on the disposable capture emulator.

Uses real emulator modem controls, then waits for the Android telephony registry
to report the same primary radio at computed level 4 for at least 15 seconds.
Raw measurements may vary within that level and are retained in the evidence.
An optional --demo-clock HHMM fixes only the requested SystemUI clock display;
enabling SystemUI demo mode can also hold other status indicators at entry.
Optional --disable-animations sets Android's three animation scales to zero for
still-frame captures. This excludes animation timing and motion from validation.
Battery, wall clock, APK/resources, screenshots, and comparison rules are not edited.

Run inside the runtime service queue, where the genuine ADB server is reachable.
Allow about 180 seconds for the queue command. Evidence is written even on failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


SOURCES = [
    'https://developer.android.com/studio/run/emulator-console#telephony-emulation',
    'https://android.googlesource.com/platform/external/qemu/+/refs/heads/emu-master-dev/android/android-emu/android/console.cpp',
    'https://android.googlesource.com/platform/external/qemu/+/refs/heads/emu-master-dev/android/emu/telephony/src/android/telephony/modem.c',
    'https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/telephony/java/android/telephony/SignalStrength.java',
    'https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/telephony/java/android/telephony/CellSignalStrengthLte.java',
    'https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/packages/SystemUI/docs/demo_mode.md',
    'https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/packages/SystemUI/src/com/android/systemui/demomode/DemoModeController.kt',
    'https://developer.android.com/reference/android/provider/Settings.Global#ANIMATOR_DURATION_SCALE',
    'https://developer.android.com/reference/android/provider/Settings.Global#WINDOW_ANIMATION_SCALE',
    'https://developer.android.com/reference/android/provider/Settings.Global#TRANSITION_ANIMATION_SCALE',
]

ANIMATION_SCALE_KEYS = ('animator_duration_scale', 'window_animation_scale',
                        'transition_animation_scale')


def now() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def primary_signals(dump: str) -> list[dict]:
    """Read current registry entries, excluding historical notification logs."""
    signals = []
    for line in dump.splitlines():
        if not line.strip().startswith('mSignalStrength=SignalStrength:{'):
            continue
        primary = re.search(r',primary=(CellSignalStrength\w+)\}', line)
        if primary is None:
            continue
        section = re.search(re.escape(primary[1]) + r':(.*?)(?=,m\w+=|,primary=)', line)
        level = re.search(r'\blevel\s*=\s*([0-4])\b', section[1]) if section else None
        signals.append({'primary': primary[1], 'level': int(level[1]) if level else None,
                        'primary_measurements': section[1].strip() if section else None,
                        'registry_line': line.strip()})
    return signals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--serial', default='emulator-5560')
    parser.add_argument('--avd', default='MacroDroid_API35_Disposable')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--signal-timeout', type=float, default=90)
    parser.add_argument('--demo-clock', metavar='HHMM',
                        help='Explicitly enable documented SystemUI demo mode and fix its clock')
    parser.add_argument('--disable-animations', action='store_true',
                        help='Set Android animation scales to zero for declared still-frame captures')
    args = parser.parse_args()
    if not re.fullmatch(r'emulator-[0-9]+', args.serial):
        parser.error('Select an explicit emulator serial')
    if not 20 <= args.signal_timeout <= 180:
        parser.error('--signal-timeout must be between 20 and 180 seconds')
    if args.demo_clock is not None and not re.fullmatch(r'(?:[01][0-9]|2[0-3])[0-5][0-9]', args.demo_clock):
        parser.error('--demo-clock must be a four-digit 24-hour time')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {'started_utc': now(), 'status': 'CONFIGURING', 'serial': args.serial,
              'expected_avd': args.avd, 'requested_signal_profile': 4,
              'required_stable_seconds': 15, 'signal_timeout_seconds': args.signal_timeout,
              'signal_stability_fields': ['primary', 'level'],
              'demo_clock_requested': args.demo_clock, 'systemui_demo_mode_requested': args.demo_clock is not None,
              'disable_animations_requested': args.disable_animations,
              'animation_scales_requested': {key: '0' for key in ANIMATION_SCALE_KEYS} if args.disable_animations else None,
              'requested_animation_scales_observed': False,
              'animation_timing_and_motion_parity_tested': False,
              'battery_modified': False, 'device_wall_clock_modified': False,
              'app_apk_modified': False, 'app_resources_modified': False,
              'screenshots_modified': False,
              'full_runtime_1_to_1_established': False, 'sources': SOURCES,
              'commands': [], 'signal_observations': []}

    def save() -> None:
        temp = output / 'capture-device.json.tmp'
        temp.write_text(json.dumps(report, indent=2) + '\n')
        temp.replace(output / 'capture-device.json')

    def run(label: str, command: list[str], *, console: bool = False) -> str:
        argv = [args.adb, '-s', args.serial, *command]
        entry = {'label': label, 'argv': argv, 'started_utc': now()}
        report['commands'].append(entry)
        started = time.monotonic()
        try:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=15, check=False)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as exc:
            code = 124
            stdout = exc.stdout or b''
            stderr = exc.stderr or b''
            stdout = stdout.decode(errors='replace') if isinstance(stdout, bytes) else stdout
            stderr = stderr.decode(errors='replace') if isinstance(stderr, bytes) else stderr
            entry['error'] = 'ADB command exceeded its 15-second deadline'
        except OSError as exc:
            code, stdout, stderr = 127, '', str(exc)
        for stream, content in [('stdout', stdout), ('stderr', stderr)]:
            name = f'{len(report["commands"]):03d}-{label}.{stream}.txt'
            raw = content.encode()
            (output / name).write_bytes(raw)
            entry[stream] = {'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        entry.update(exit_code=code, seconds=round(time.monotonic() - started, 3))
        save()
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        if code or (console and (not lines or lines[-1] != 'OK' or re.search(r'(?m)^\s*KO:', stdout + '\n' + stderr))):
            raise RuntimeError(f'{label} failed; see recorded command output')
        return stdout

    def observe(label: str) -> dict:
        return {
            'gsm_status': run(label + '-gsm', ['emu', 'gsm', 'status'], console=True),
            'power_state': run(label + '-power', ['emu', 'power', 'display'], console=True),
            'android_battery': run(label + '-battery', ['shell', 'dumpsys', 'battery']),
            'device_utc': run(label + '-clock', ['shell', 'date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).strip(),
            'sysui_demo_allowed': run(label + '-demo-allowed', ['shell', 'settings', 'get', 'global', 'sysui_demo_allowed']).strip(),
            'sysui_tuner_demo_on': run(label + '-demo-on', ['shell', 'settings', 'get', 'global', 'sysui_tuner_demo_on']).strip(),
            'animation_scales': {key: run(label + '-' + key, ['shell', 'settings', 'get', 'global', key]).strip()
                                 for key in ANIMATION_SCALE_KEYS},
        }

    save()
    try:
        if run('emulator-check', ['shell', 'getprop', 'ro.kernel.qemu']).strip() != '1':
            raise RuntimeError('The selected device did not identify itself as an emulator')
        if run('boot-check', ['shell', 'getprop', 'sys.boot_completed']).strip() != '1':
            raise RuntimeError('Android boot is incomplete')
        avd = run('avd-name', ['emu', 'avd', 'name'], console=True).splitlines()
        if not avd or avd[0].strip() != args.avd:
            raise RuntimeError('AVD name differs from the explicitly selected disposable AVD')
        report['before'] = observe('before')
        report['before']['primary_signals'] = primary_signals(run('before-telephony', ['shell', 'dumpsys', 'telephony.registry']))
        run('signal-profile-help', ['emu', 'help', 'gsm', 'signal-profile'], console=True)
        run('voice-home', ['emu', 'gsm', 'voice', 'home'], console=True)
        run('data-home', ['emu', 'gsm', 'data', 'home'], console=True)
        run('signal-profile-four', ['emu', 'gsm', 'signal-profile', '4'], console=True)
        deadline = time.monotonic() + args.signal_timeout
        stable_since = None
        previous = None
        while time.monotonic() < deadline:
            dump = run('telephony', ['shell', 'dumpsys', 'telephony.registry'])
            signals = primary_signals(dump)
            observation = {'observed_utc': now(), 'signals': signals}
            report['signal_observations'].append(observation)
            # Android derives the displayed strength from the primary radio's level.
            # Raw RSSI/RSRP can vary within one level; keep those readings as evidence.
            current = [(x['primary'], x['level']) for x in signals]
            # The pinned disposable AVD has one modem. Do not accept another SIM's level.
            strong = len(signals) == 1 and signals[0]['level'] == 4
            measured = time.monotonic()
            if strong and current == previous:
                if stable_since is not None and measured - stable_since >= 15:
                    report['signal_stable_seconds'] = round(measured - stable_since, 3)
                    report['confirmed_primary_signal'] = signals[0]
                    break
            else:
                stable_since = measured if strong else None
            previous = current
            save()
            print(json.dumps({'signal_levels': [x['level'] for x in signals], 'observed_utc': now()}), flush=True)
            time.sleep(min(5, max(0, deadline - time.monotonic())))
        else:
            raise RuntimeError('One primary radio type and computed level 4 did not remain stable for 15 seconds within the deadline')
        status = run('confirmed-gsm', ['emu', 'gsm', 'status'], console=True)
        if not all(re.search(r'gsm ' + kind + r' state:\s*home\b', status) for kind in ('voice', 'data')):
            raise RuntimeError('Emulator did not confirm home voice and data registration')
        if args.disable_animations:
            for key in ANIMATION_SCALE_KEYS:
                run('disable-' + key, ['shell', 'settings', 'put', 'global', key, '0'])
        if args.demo_clock is not None:
            run('allow-demo', ['shell', 'settings', 'put', 'global', 'sysui_demo_allowed', '1'])
            run('start-demo', ['shell', 'settings', 'put', 'global', 'sysui_tuner_demo_on', '1'])
            demo_deadline = time.monotonic() + 20
            while time.monotonic() < demo_deadline:
                state = run('demo-controller', ['shell', 'dumpsys', 'activity', 'service',
                            'com.android.systemui/.SystemUIService', 'DemoModeController'])
                if re.search(r'\bisInDemoMode=true\b', state) and re.search(r'\bisDemoModeAllowed=true\b', state):
                    report['systemui_demo_mode_observed'] = True
                    break
                time.sleep(1)
            else:
                raise RuntimeError('SystemUI did not report active, allowed demo mode')
            run('demo-clock', ['shell', 'am', 'broadcast', '-a', 'com.android.systemui.demo',
                               '-e', 'command', 'clock', '-e', 'hhmm', args.demo_clock])
            time.sleep(1)
        report['after'] = observe('after')
        final_signals = primary_signals(run('after-telephony', ['shell', 'dumpsys', 'telephony.registry']))
        report['after']['primary_signals'] = final_signals
        if len(final_signals) != 1 or (final_signals[0]['primary'], final_signals[0]['level']) != (report['confirmed_primary_signal']['primary'], 4):
            raise RuntimeError('Primary radio type or computed level changed at configuration completion')
        if args.demo_clock is not None and (report['after']['sysui_demo_allowed'] != '1' or report['after']['sysui_tuner_demo_on'] != '1'):
            raise RuntimeError('Requested SystemUI demo settings were not observed')
        if args.disable_animations:
            try:
                scales_zero = all(float(report['after']['animation_scales'][key]) == 0.0
                                  for key in ANIMATION_SCALE_KEYS)
            except (TypeError, ValueError):
                scales_zero = False
            if not scales_zero:
                raise RuntimeError('Requested zero animation scales were not observed at configuration completion')
            report['requested_animation_scales_observed'] = True
        report['status'] = 'CAPTURE_DEVICE_CONFIGURED'
        return 0
    except RuntimeError as exc:
        report.update(status='CAPTURE_DEVICE_CONFIGURATION_FAILED', failure=str(exc))
        print(str(exc), flush=True)
        return 2
    finally:
        report['finished_utc'] = now()
        save()


if __name__ == '__main__':
    raise SystemExit(main())
