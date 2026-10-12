#!/usr/bin/env python3
"""Create the separate diagnostic workflow from the reviewed owned-service steps."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--widget-workflow', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.widget_workflow.read_bytes()
    if hashlib.sha256(raw).hexdigest() != 'f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba':
        raise ValueError('Reviewed owned-service workflow identity changed')
    old = yaml.load(raw, Loader=yaml.BaseLoader)
    steps = old['jobs']['widget-method-probe']['steps']
    bootstrap = next(step['run'] for step in steps if step['name'] == 'Install the checksum-pinned disposable Android runtime')
    runtime = next(step['run'] for step in steps if step['name'] == 'Run both exact APKs through the independent Widget method probe')
    for before, after in [('ci-widget-method', 'ci-exact-alarm-navigation'),
                          ('macrodroid-widget-tooling', 'macrodroid-exact-alarm-navigation-tooling'),
                          ('widget_', 'trigger_'), ('Widget runtime', 'Day/Time readiness runtime'),
                          ('probe_step_exit_code', 'journey_step_exit_code')]:
        bootstrap, runtime = bootstrap.replace(before, after), runtime.replace(before, after)
    boundary = 'python3 tools/android/runtime_job.py --queue ci-exact-alarm-navigation/environment/queue'
    if runtime.count(boundary) != 1:
        raise ValueError('Reviewed runtime command boundary changed')
    runtime = runtime.split(boundary, 1)[0] + '''python3 tools/android/runtime_job.py --queue ci-exact-alarm-navigation/environment/queue \
  --id exact-alarm-navigation-radio-clock --timeout 240 -- \
  python3 "$GITHUB_WORKSPACE/tools/android/configure_capture_device.py" \
    --adb "$RUNNER_TEMP/macrodroid-exact-alarm-navigation-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-exact-alarm-navigation/device" --demo-clock 1200 \
  2>&1 | tee ci-exact-alarm-navigation/device-job.log
python3 tools/android/runtime_job.py --queue ci-exact-alarm-navigation/environment/queue \
  --id exact-alarm-navigation-settings --timeout 360 -- \
  python3 "$GITHUB_WORKSPACE/work-in-progress/trigger-category/07-zero-animation-source/enable_still_animations.py" \
    --adb "$RUNNER_TEMP/macrodroid-exact-alarm-navigation-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-exact-alarm-navigation/animation-settings" \
  2>&1 | tee ci-exact-alarm-navigation/animation-job.log
python3 tools/android/runtime_job.py --queue ci-exact-alarm-navigation/environment/queue \
  --id exact-alarm-navigation-fourteen-screen --timeout 2400 -- \
  python3 "$GITHUB_WORKSPACE/ci-exact-alarm-navigation/reviewed-source/tools/parity_journeys/exact_alarm_journey.py" \
    --source "$GITHUB_WORKSPACE/ci-exact-alarm-navigation/reviewed-source/project" \
    --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk" \
    --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk" \
    --output "$GITHUB_WORKSPACE/ci-exact-alarm-navigation/journey" --serial emulator-5560 \
    --accept-package-data-removal --observe-denial-handoff --settle-full-frames --observe-notification-readiness \
  2>&1 | tee ci-exact-alarm-navigation/journey-job.log
'''
    home = Path(__file__).resolve().parent
    def sha(name):
        return hashlib.sha256((home / name).read_bytes()).hexdigest()
    package = 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'
    preflight = f'''set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {{
    '{package}/prepare_trigger_journey.py': '{sha('prepare_trigger_journey.py')}',
    '{package}/verify_trigger_journey.py': '{sha('verify_trigger_journey.py')}',
}}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 {package}/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-navigation
'''
    host = '''set -euo pipefail
python3 -B -m unittest discover -s tools/android -p 'test_download_retry.py' -v 2>&1 | tee ci-exact-alarm-navigation/download-tests.log
python3 -B -m unittest discover -s ci-exact-alarm-navigation/reviewed-source/tools/parity_journeys -p 'test_*.py' -v 2>&1 | tee ci-exact-alarm-navigation/journey-host-tests.log
python3 -B -m unittest discover -s work-in-progress/trigger-category/07-zero-animation-source -p 'test_enable_still_animations.py' -v 2>&1 | tee ci-exact-alarm-navigation/animation-host-tests.log
'''
    materialize = f'''set -euo pipefail
python3 scripts/materialize_v9.py --without-overlay 2>&1 | tee ci-exact-alarm-navigation/materialize-toolchain.log
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-exact-alarm-navigation/materialize-original.log
python3 scripts/assemble_artifact.py work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json 2>&1 | tee ci-exact-alarm-navigation/materialize-candidate.log
python3 {package}/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-navigation --materialized 2>&1 | tee ci-exact-alarm-navigation/apk-preflight.log
'''
    final = f'''set -euo pipefail
mkdir -p ci-exact-alarm-navigation
python3 {package}/verify_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-navigation 2>&1 | tee ci-exact-alarm-navigation/independent-comparison.log
'''
    document = '''name: Independent exact-alarm fourteen-screen comparison with bounded notification readiness

on:
  push:
    branches: [main]
    paths:
      - '.github/workflows/editor-exact-alarm-navigation.yml'
      - 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen/**'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: editor-exact-alarm-navigation-${{ github.ref }}
  cancel-in-progress: false

jobs:
  editor-exact-alarm-navigation:
    runs-on: ubuntu-24.04
    timeout-minutes: 75
    env:
      PYTHONDONTWRITEBYTECODE: '1'
    steps:
      - name: Check out the exact reviewed inputs
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
'''
    for title, script, always in [
            ('Verify and copy the frozen exact-alarm guard and fourteen-screen source', preflight, False),
            ('Run the frozen capture, animation and downloader host controls', host, False),
            ('Inspect both exact APKs using the preserved AAPT2 tool', materialize, False),
            ('Install the pinned disposable runtime and preserve toolchain identities', bootstrap, False),
            ('Observe the fourteen declared screens with bounded notification readiness', runtime, False),
            ('Recheck raw readiness, animation settings, ordered captures and exact pixels', final, True)]:
        document += '\n      - name: ' + title + '\n'
        if always:
            document += '        if: always()\n'
        document += '        shell: bash\n        run: |\n'
        document += ''.join('          ' + line + '\n' for line in script.splitlines())
    document += '''
      - name: Preserve the complete owned diagnostic evidence
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: editor-exact-alarm-navigation-${{ github.sha }}
          retention-days: 30
          if-no-files-found: error
          path: ci-exact-alarm-navigation/
          include-hidden-files: true
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        stream.write(document)
    print(hashlib.sha256(args.output.read_bytes()).hexdigest(), args.output)


if __name__ == '__main__':
    main()
