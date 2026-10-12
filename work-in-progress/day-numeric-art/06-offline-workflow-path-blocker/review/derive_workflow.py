#!/usr/bin/env python3
"""Generate a numeric workflow from the exact retained Widget service lifecycle."""
import hashlib
import json
from pathlib import Path
import textwrap

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')


def indent(value, spaces=10):
    return textwrap.indent(value.rstrip() + '\n', ' ' * spaces)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(data)


def make_workflow(preflight_sha, manifest_sha):
    parent = (ROOT / 'inputs/parent/.github/workflows/widget-method-probe.yml').read_text()
    bootstrap = parent.split('      - name: Install the checksum-pinned disposable Android runtime\n', 1)[1].split('\n      - name: Run both exact APKs', 1)[0]
    runtime = parent.split('      - name: Run both exact APKs through the independent Widget method probe\n', 1)[1].split('\n      - name: Preserve complete probe', 1)[0]
    bootstrap = bootstrap.replace('ci-widget-method', 'ci-day-numeric-art').replace('macrodroid-widget-tooling', 'macrodroid-numeric-art-tooling').replace('Widget runtime', 'numeric ART runtime').replace('python3 tools/android/', 'python3 parent-inputs/tools/android/')
    runtime = runtime.replace('ci-widget-method', 'ci-day-numeric-art').replace('macrodroid-widget-tooling', 'macrodroid-numeric-art-tooling').replace('widget_', 'numeric_').replace('cleanup_widget_runtime', 'cleanup_numeric_runtime')
    runtime = runtime.replace('python3 -u tools/android/', 'python3 -u parent-inputs/tools/android/').replace('python3 tools/android/', 'python3 parent-inputs/tools/android/')
    runtime = runtime.replace('--id widget-method-art', '--id day-numeric-method-art')
    runtime = runtime.replace('$GITHUB_WORKSPACE/work-in-progress/widget-art/04-avd-parser-fix/', '$GITHUB_WORKSPACE/tools/day_numeric_art/')
    runtime = runtime.replace('android_widget_method_probe.py', 'android_day_numeric_method_probe.py').replace('widget-method-probe.dex', 'day-numeric-method-probe.dex').replace('widget-method-probe.json', 'day-numeric-method-probe.json')
    runtime = runtime.replace('$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk', '$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-original.apk')
    runtime = runtime.replace('$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-widget-update-06.apk', '$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-day-numeric-0762aad9.apk')
    pin_script = f'''python3 - <<'PY'
import hashlib
from pathlib import Path
pins = {{
    'tools/day_numeric_art/preflight.py': '{preflight_sha}',
    'tools/day_numeric_art/runtime-files.json': '{manifest_sha}',
}}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise SystemExit('Exact numeric workflow entry point changed: ' + name)
print('Both exact numeric workflow entry points verified.')
PY'''
    base = '''name: Neutral original and candidate DayTrigger numeric ART method probe

on:
  push:
    branches: [main]
    paths:
      - '.github/workflows/day-numeric-method-probe.yml'
      - 'tools/day_numeric_art/**'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: day-numeric-method-probe-${{ github.ref }}
  cancel-in-progress: false

jobs:
  day-numeric-method-probe:
    runs-on: ubuntu-24.04
    timeout-minutes: 60
    env:
      PYTHONDONTWRITEBYTECODE: '1'
    steps:
      - name: Check out the exact reviewed numeric tools
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
          sparse-checkout-cone-mode: false
          sparse-checkout: |
            .github/workflows/day-numeric-method-probe.yml
            tools/day_numeric_art

      - name: Check out the immutable runtime and fixed APK parts
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          ref: fc825ede39a40249e33c8ba75b93128a98bd5e3c
          path: parent-inputs
          persist-credentials: false
          sparse-checkout-cone-mode: false
          sparse-checkout: |
            .github/workflows/widget-method-probe.yml
            scripts/assemble_artifact.py
            tools/android/bootstrap_android_runtime.py
            tools/android/android-toolchain-pins.json
            tools/android/android_runtime_service.py
            tools/android/runtime_job.py
            tools/android/wait_android_ready.py
            tools/android/test_download_retry.py
            vendor/original
            work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact

      - name: Pin all numeric source, runtime and multipart input roles
        shell: bash
        run: |
          set -euo pipefail
          mkdir ci-day-numeric-art
          test "$(git rev-parse HEAD)" = "$GITHUB_SHA"
          test "$(git -C parent-inputs rev-parse HEAD)" = fc825ede39a40249e33c8ba75b93128a98bd5e3c
'''
    base += indent(pin_script)
    base += '''          timeout 120s python3 -B tools/day_numeric_art/preflight.py \
            --current "$GITHUB_WORKSPACE" --parent "$GITHUB_WORKSPACE/parent-inputs" \
            --output "$GITHUB_WORKSPACE/ci-day-numeric-art/preflight-inputs" --phase inputs \
            2>&1 | tee ci-day-numeric-art/input-preflight.log

      - name: Run the six downloader and all forty-two simulated wrapper controls
        shell: bash
        run: |
          set -euo pipefail
          timeout 120s python3 -B -m unittest discover -s parent-inputs/tools/android \
            -p 'test_download_retry.py' -v 2>&1 | tee ci-day-numeric-art/download-tests.log
          export NUMERIC_PROBE_CONTROL_EVIDENCE="$GITHUB_WORKSPACE/ci-day-numeric-art/host-control-evidence"
          timeout 240s python3 -B -m unittest discover -s tools/day_numeric_art \
            -p 'test_android_day_numeric_method_probe.py' -v 2>&1 | tee ci-day-numeric-art/wrapper-tests.log
          python3 - <<'PY'
          import json, re
          from pathlib import Path
          rows = []
          for name, expected in [('download-tests.log', 6), ('wrapper-tests.log', 42)]:
              raw = (Path('ci-day-numeric-art') / name).read_text()
              summaries = re.findall(r'^Ran (\\d+) tests in ([0-9.]+)s$', raw, re.M)
              if len(summaries) != 1 or int(summaries[0][0]) != expected or not raw.rstrip().endswith('OK'):
                  raise SystemExit('The exact full host control inventory did not pass: ' + name)
              rows.append({'log': name, 'tests': expected, 'seconds': summaries[0][1]})
          Path('ci-day-numeric-art/host-control-summary.json').write_text(json.dumps(rows, indent=2) + '\\n')
          PY

      - name: Assemble only the fixed original and accepted numeric candidate APKs
        shell: bash
        run: |
          set -euo pipefail
          timeout 120s python3 -B parent-inputs/scripts/assemble_artifact.py \
            parent-inputs/vendor/original/manifest.json \
            2>&1 | tee ci-day-numeric-art/materialize-original.log
          timeout 120s python3 -B parent-inputs/scripts/assemble_artifact.py \
            parent-inputs/work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json \
            2>&1 | tee ci-day-numeric-art/materialize-numeric.log

      - name: Recheck all source and actual APK inputs before starting Android
        shell: bash
        run: |
          set -euo pipefail
'''
    base += indent(pin_script)
    base += '''          timeout 120s python3 -B tools/day_numeric_art/preflight.py \
            --current "$GITHUB_WORKSPACE" --parent "$GITHUB_WORKSPACE/parent-inputs" \
            --output "$GITHUB_WORKSPACE/ci-day-numeric-art/preflight-apks" --phase apks \
            2>&1 | tee ci-day-numeric-art/apk-preflight.log

      - name: Install the checksum-pinned disposable Android runtime
'''
    base += bootstrap
    base += '''
      - name: Run the neutral probe once per exact APK with verification enabled
'''
    base += runtime
    base += '''
      - name: Recheck final fixed inputs and the complete real probe evidence
        if: always()
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p ci-day-numeric-art
'''
    base += indent(pin_script)
    base += '''          timeout 120s python3 -B tools/day_numeric_art/preflight.py \
            --current "$GITHUB_WORKSPACE" --parent "$GITHUB_WORKSPACE/parent-inputs" \
            --output "$GITHUB_WORKSPACE/ci-day-numeric-art/final-verification" --phase final \
            --probe-result "$GITHUB_WORKSPACE/ci-day-numeric-art/probe" \
            2>&1 | tee ci-day-numeric-art/final-verification.log

      - name: Preserve complete raw, partial, executed-source and host-control evidence
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: day-numeric-method-probe-${{ github.sha }}
          retention-days: 30
          if-no-files-found: error
          path: ci-day-numeric-art/
          include-hidden-files: true
'''
    if 'widget_service' in base or '04-avd-parser-fix' in base or 'b79b0010' in base:
        raise ValueError('Unexpected obsolete Widget execution role remains')
    return base


def main():
    target = ROOT / 'source-01'
    preflight = target / 'tools/day_numeric_art/preflight.py'
    manifest = target / 'tools/day_numeric_art/runtime-files.json'
    output = make_workflow(hashlib.sha256(preflight.read_bytes()).hexdigest(),
                           hashlib.sha256(manifest.read_bytes()).hexdigest())
    path = target / '.github/workflows/day-numeric-method-probe.yml'
    write(path, output)
    print(json.dumps({'path': str(path), 'bytes': len(output.encode()),
                      'sha256': hashlib.sha256(output.encode()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
