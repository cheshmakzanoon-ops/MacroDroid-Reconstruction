#!/usr/bin/env python3
"""Run the disposable emulator and explicit queued commands in one exec session.

The file queue is useful when executor invocations have separate process/network
lifetimes. Requests contain argv arrays; they are never interpreted by a shell.
Keep this process in a live exec session. Stop it by creating queue/STOP.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time


def save_json(path: Path, value: object) -> None:
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)


def now() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tooling', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--avd', default='MacroDroid_API35_Disposable')
    parser.add_argument('--port', type=int, default=5560)
    parser.add_argument('--acceleration', choices=['off', 'on', 'auto'], default='off',
                        help='Use on for KVM CI runners; off preserves local software emulation')
    args = parser.parse_args()
    base = args.tooling.resolve()
    evidence = args.evidence.resolve()
    queue = evidence / 'queue'
    for path in (evidence, queue / 'requests', queue / 'responses'):
        path.mkdir(parents=True, exist_ok=True)
    stop = queue / 'STOP'
    if stop.exists():
        raise SystemExit(f'Remove the previous stop marker before starting: {stop}')
    sdk = base / 'android'
    adb = sdk / 'platform-tools/adb'
    serial = f'emulator-{args.port}'
    env = os.environ.copy()
    env.update({
        'ANDROID_HOME': str(sdk),
        'ANDROID_SDK_ROOT': str(sdk),
        'ANDROID_USER_HOME': str(base / 'android-user'),
        'ANDROID_AVD_HOME': str(base / 'android-user/avd'),
        'ANDROID_EMULATOR_HOME': str(base / 'android-user'),
        'JAVA_HOME': str(base / 'jdk21'),
    })
    if args.acceleration == 'off':
        env['ANDROID_I_WANT_MY_TCG'] = 'yes'
    else:
        env.pop('ANDROID_I_WANT_MY_TCG', None)
    env['PATH'] = os.pathsep.join([str(base / 'jdk21/bin'), str(sdk / 'platform-tools'), env['PATH']])
    subprocess.run([str(adb), 'start-server'], env=env, check=True, timeout=15)
    command = [str(sdk / 'emulator/emulator'), '-avd', args.avd,
               '-port', str(args.port), '-no-window', '-no-audio',
               '-no-boot-anim', '-no-snapshot', '-accel', args.acceleration,
               '-gpu', 'swiftshader', '-cores', '2', '-memory', '3072',
               '-camera-back', 'none', '-camera-front', 'none']
    status = {'started_utc': now(), 'state': 'booting', 'serial': serial,
              'adb_path': str(adb), 'command': command,
              'queue_path': str(queue), 'avd': args.avd,
              'ram_mb': 3072, 'virtual_cores': 2,
              'acceleration': args.acceleration}
    save_json(evidence / 'emulator-launch.json', status)
    save_json(evidence / 'runtime-status.json', status)
    log = (evidence / 'emulator-boot.log').open('ab')
    log.write(f'\n--- Queue service launch {now()} ---\n'.encode())
    log.flush()
    emulator = subprocess.Popen(command, env=env, stdin=subprocess.DEVNULL,
                                stdout=log, stderr=subprocess.STDOUT)
    print(json.dumps({'started': now(), 'serial': serial, 'queue': str(queue)}), flush=True)
    signal.signal(signal.SIGTERM, lambda *_: stop.touch())
    signal.signal(signal.SIGINT, lambda *_: stop.touch())
    next_poll = 0.0
    try:
        while not stop.exists():
            if emulator.poll() is not None:
                status.update(state='emulator_exited', exit_code=emulator.returncode,
                              updated_utc=now())
                save_json(evidence / 'runtime-status.json', status)
                return emulator.returncode or 1
            requests = sorted((queue / 'requests').glob('*.json'))
            if requests:
                request_file = requests[0]
                job_id = request_file.stem
                if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', job_id):
                    raise ValueError('Unsafe request filename')
                running = request_file.with_suffix('.running')
                request_file.rename(running)
                result = {'id': job_id, 'started_utc': now()}
                stdout_path = queue / 'responses' / (job_id + '.stdout')
                stderr_path = queue / 'responses' / (job_id + '.stderr')
                try:
                    request = json.loads(running.read_text())
                    argv = request['argv']
                    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv):
                        raise ValueError('argv must be a nonempty array of strings')
                    timeout = float(request.get('timeout_s', 120))
                    if not 0 < timeout <= 3600:
                        raise ValueError('timeout_s must be in (0, 3600]')
                    job_env = env.copy()
                    overrides = request.get('env', {})
                    if not isinstance(overrides, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in overrides.items()):
                        raise ValueError('env must map strings to strings')
                    job_env.update(overrides)
                    result.update(argv=argv, cwd=request.get('cwd'), timeout_s=timeout)
                    with stdout_path.open('wb') as out, stderr_path.open('wb') as err:
                        try:
                            run = subprocess.run(argv, cwd=request.get('cwd'), env=job_env,
                                                 stdin=subprocess.DEVNULL, stdout=out,
                                                 stderr=err, timeout=timeout)
                            result['exit_code'] = run.returncode
                        except subprocess.TimeoutExpired:
                            result.update(exit_code=124, error='command timed out')
                except Exception as exc:
                    result.update(exit_code=125, error=f'{type(exc).__name__}: {exc}')
                result.update(completed_utc=now(), stdout_path=str(stdout_path),
                              stderr_path=str(stderr_path))
                save_json(queue / 'responses' / (job_id + '.json'), result)
                running.rename(running.with_suffix('.done'))
                print(json.dumps({'job': job_id, 'exit_code': result['exit_code']}), flush=True)
                continue
            if time.monotonic() >= next_poll:
                next_poll = time.monotonic() + 10
                try:
                    p = subprocess.run([str(adb), '-s', serial, 'shell', 'getprop'],
                                       env=env, capture_output=True, timeout=6, text=True)
                    props = dict(re.findall(r'^\[([^\]]+)\]: \[(.*)\]$', p.stdout, re.MULTILINE))
                    wanted = ['sys.boot_completed', 'dev.bootcomplete',
                              'ro.build.version.sdk', 'ro.build.version.release',
                              'ro.build.fingerprint', 'ro.product.cpu.abi',
                              'ro.product.cpu.abilist', 'ro.product.cpu.abilist64',
                              'ro.dalvik.vm.native.bridge', 'ro.enable.native.bridge.exec',
                              'ro.ndk_translation.version', 'ro.berberis.version']
                    observed = {k: props.get(k, '') for k in wanted}
                    status.update(updated_utc=now(), properties=observed,
                                  adb_exit_code=p.returncode, adb_error=p.stderr.strip())
                    if observed['sys.boot_completed'] == '1':
                        status['state'] = 'ready'
                        save_json(evidence / 'runtime-properties.json', observed)
                    save_json(evidence / 'runtime-status.json', status)
                except subprocess.TimeoutExpired:
                    status.update(updated_utc=now(), adb_error='getprop timed out during boot')
                    save_json(evidence / 'runtime-status.json', status)
            time.sleep(0.2)
    finally:
        if emulator.poll() is None:
            emulator.terminate()
            try:
                emulator.wait(timeout=10)
            except subprocess.TimeoutExpired:
                emulator.kill()
                emulator.wait(timeout=5)
        log.close()
        status.update(state='stopped', updated_utc=now())
        save_json(evidence / 'runtime-status.json', status)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
