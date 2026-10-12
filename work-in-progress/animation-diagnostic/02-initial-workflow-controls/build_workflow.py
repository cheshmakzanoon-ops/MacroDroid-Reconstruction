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
    for before, after in [('ci-widget-method', 'ci-normal-animation'),
                          ('macrodroid-widget-tooling', 'macrodroid-normal-animation-tooling'),
                          ('widget_', 'normal_'), ('Widget runtime', 'normal-animation runtime'),
                          ('probe_step_exit_code', 'journey_step_exit_code')]:
        bootstrap, runtime = bootstrap.replace(before, after), runtime.replace(before, after)
    boundary = 'python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue'
    if runtime.count(boundary) != 1:
        raise ValueError('Reviewed runtime command boundary changed')
    runtime = runtime.split(boundary, 1)[0] + '''python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue \
  --id normal-animation-radio-clock --timeout 240 -- \
  python3 "$GITHUB_WORKSPACE/tools/android/configure_capture_device.py" \
    --adb "$RUNNER_TEMP/macrodroid-normal-animation-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-normal-animation/device" --demo-clock 1200 \
  2>&1 | tee ci-normal-animation/device-job.log
python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue \
  --id normal-animation-settings --timeout 360 -- \
  python3 "$GITHUB_WORKSPACE/work-in-progress/animation-diagnostic/01-normal-animation-source/enable_normal_animations.py" \
    --adb "$RUNNER_TEMP/macrodroid-normal-animation-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-normal-animation/animation-settings" \
  2>&1 | tee ci-normal-animation/animation-job.log
python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue \
  --id normal-animation-ten-screen --timeout 2400 -- \
  python3 "$GITHUB_WORKSPACE/ci-normal-animation/reviewed-source/tools/parity_journeys/favourite_info_journey.py" \
    --source "$GITHUB_WORKSPACE/ci-normal-animation/reviewed-source/project" \
    --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk" \
    --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk" \
    --output "$GITHUB_WORKSPACE/ci-normal-animation/journey" --serial emulator-5560 \
    --accept-package-data-removal --observe-denial-handoff --settle-full-frames \
  2>&1 | tee ci-normal-animation/journey-job.log
'''
    home = Path(__file__).resolve().parent
    def sha(name):
        return hashlib.sha256((home / name).read_bytes()).hexdigest()
    package = 'work-in-progress/animation-diagnostic/02-reviewed-workflow'
    preflight = f'''set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {{
    '{package}/prepare_normal_journey.py': '{sha('prepare_normal_journey.py')}',
    '{package}/verify_normal_journey.py': '{sha('verify_normal_journey.py')}',
}}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 {package}/prepare_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation
'''
    host = '''set -euo pipefail
python3 -B -m unittest discover -s tools/android -p 'test_download_retry.py' -v 2>&1 | tee ci-normal-animation/download-tests.log
python3 -B -m unittest discover -s ci-normal-animation/reviewed-source/tools/parity_journeys -p 'test_*.py' -v 2>&1 | tee ci-normal-animation/journey-host-tests.log
python3 -B -m unittest discover -s work-in-progress/animation-diagnostic/01-normal-animation-source -p 'test_enable_normal_animations.py' -v 2>&1 | tee ci-normal-animation/animation-host-tests.log
'''
    materialize = f'''set -euo pipefail
python3 scripts/materialize_v9.py --without-overlay 2>&1 | tee ci-normal-animation/materialize-toolchain.log
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-normal-animation/materialize-original.log
python3 scripts/assemble_artifact.py artifacts/current/manifest.json 2>&1 | tee ci-normal-animation/materialize-candidate.log
python3 {package}/prepare_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation --materialized 2>&1 | tee ci-normal-animation/apk-preflight.log
'''
    final = f'''set -euo pipefail
mkdir -p ci-normal-animation
python3 {package}/verify_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation 2>&1 | tee ci-normal-animation/independent-comparison.log
'''
    document = '''name: Independent normal-animation ten-screen comparison

on:
  push:
    branches: [main]
    paths:
      - '.github/workflows/editor-normal-animation.yml'
      - 'work-in-progress/animation-diagnostic/02-reviewed-workflow/**'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: editor-normal-animation-${{ github.ref }}
  cancel-in-progress: false

jobs:
  editor-normal-animation:
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
            ('Verify and copy the frozen ten-screen guard and diagnostic source', preflight, False),
            ('Run the frozen capture, animation and downloader host controls', host, False),
            ('Inspect both exact APKs using the preserved AAPT2 tool', materialize, False),
            ('Install the pinned disposable runtime and preserve toolchain identities', bootstrap, False),
            ('Observe the same ten screens with normal animation scales', runtime, False),
            ('Recheck raw animation settings, ordered captures and exact pixels', final, True)]:
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
          name: editor-normal-animation-${{ github.sha }}
          retention-days: 30
          if-no-files-found: error
          path: ci-normal-animation/
          include-hidden-files: true
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        stream.write(document)
    print(hashlib.sha256(args.output.read_bytes()).hexdigest(), args.output)


if __name__ == '__main__':
    main()
