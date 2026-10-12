#!/usr/bin/env python3
"""Generate only this owned inactive workflow and its exact runtime inventory."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
OWN = SOURCE / 'tools/indicator_sampling'
PARENT = ROOT / 'parent-inputs'
PINS = json.loads((OWN / 'pins.json').read_text())
WORKFLOW = '.github/workflows/indicator-fixed-sampling.yml'
NAMES = ['README.md', 'common.py', 'prepare.py', 'record.py', 'verify.py',
         'test_indicator_sampling.py', 'pins.json', 'protocol.json',
         'historical-coordinates.json', 'aapt2',
         'fixtures/original-intro1-preinput.xml', 'fixtures/candidate-intro1-preinput.xml',
         'fixtures/original-intro2.xml', 'fixtures/candidate-intro2.xml']


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


own = {('tools/indicator_sampling/' + name): identity(OWN / name) for name in NAMES}
parents = [row['path'] for row in PINS['parents']]
for manifest in ['vendor/original/manifest.json',
                 'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json']:
    parents.extend(row['path'] for row in json.loads((PARENT / manifest).read_text())['parts'])
assert len(parents) == len(set(parents)) == 40

template = '''name: Fixed eight-install indicator sampling diagnostic

on:
  push:
    branches: [main]
    paths:
      - '.github/workflows/indicator-fixed-sampling.yml'
      - 'tools/indicator_sampling/**'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: indicator-fixed-sampling-${{ github.ref }}
  cancel-in-progress: false

jobs:
  fixed-sampling:
    runs-on: ubuntu-24.04
    timeout-minutes: 150
    env:
      PYTHONDONTWRITEBYTECODE: '1'
    steps:
      - name: Check out this exact diagnostic source and workflow
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
          sparse-checkout-cone-mode: false
          sparse-checkout: |
            /tools/indicator_sampling/
            /.github/workflows/indicator-fixed-sampling.yml

      - name: Check out the forty immutable parent and APK-part roles
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          ref: 6331410cfd2391389270564803623079e8355ad8
          path: pinned-inputs
          persist-credentials: false
          sparse-checkout-cone-mode: false
          sparse-checkout: |
@PARENT_SPARSE@

      - name: Preserve and verify every executed diagnostic input
        shell: bash
        run: |
          set -euo pipefail
          mkdir ci-indicator
          python3 - <<'PY'
          from pathlib import Path
          import hashlib, json, os, subprocess
          expected = @OWN_JSON@
          workflow = '.github/workflows/indicator-fixed-sampling.yml'
          manifest = 'tools/indicator_sampling/runtime-files.json'
          output = Path('ci-indicator/owned-source')
          output.mkdir()
          actual = []
          for name in sorted([*expected, workflow, manifest]):
              source = Path(name)
              if source.is_symlink() or not source.is_file():
                  raise RuntimeError('Missing or linked executed source: ' + name)
              raw = source.read_bytes()
              target = output / name
              target.parent.mkdir(parents=True, exist_ok=True)
              with target.open('xb') as stream:
                  stream.write(raw)
              target.chmod(source.stat().st_mode & 0o777)
              actual.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
          Path('ci-indicator/executed-source.json').write_text(json.dumps(actual, indent=2) + '\\n')
          def git(argv):
              result = subprocess.run(['git', *argv], capture_output=True, timeout=60, check=True)
              if result.stderr.strip():
                  raise RuntimeError('Unexpected Git verification stderr')
              return result.stdout
          head = git(['rev-parse', 'HEAD']).decode().strip()
          parent = git(['-C', 'pinned-inputs', 'rev-parse', 'HEAD']).decode().strip()
          if head != os.environ['GITHUB_SHA'] or parent != '6331410cfd2391389270564803623079e8355ad8':
              raise RuntimeError('Actual source checkout identity differs')
          if git(['show', 'HEAD:' + workflow]) != Path(workflow).read_bytes():
              raise RuntimeError('Executed workflow differs from its exact checked-out commit')
          required = []
          for row in actual:
              if row['path'] in expected and {k: row[k] for k in ('bytes', 'sha256')} != expected[row['path']]:
                  raise RuntimeError('Reviewed source changed: ' + row['path'])
              if row['path'] != manifest:
                  required.append(row)
          if json.loads(Path(manifest).read_text()) != required:
              raise RuntimeError('Runtime manifest omitted, changed or reordered a required source role')
          Path('ci-indicator/source-checkout.json').write_text(json.dumps({'head': head, 'parent_head': parent,
              'workflow_matches_committed_blob': True, 'required_source_files': len(actual)}, indent=2) + '\\n')
          PY

      - name: Run and retain the bounded synthetic observation controls
        shell: bash
        run: |
          set -euo pipefail
          export INDICATOR_PARENTS="$GITHUB_WORKSPACE/pinned-inputs"
          export INDICATOR_HOST_EVIDENCE="$GITHUB_WORKSPACE/ci-indicator/host-evidence"
          timeout 900s python3 -B -m unittest discover -s tools/indicator_sampling -p 'test_*.py' -v \\
            2>&1 | tee ci-indicator/host-tests.log

      - name: Assemble and independently inspect both fixed APK inputs
        shell: bash
        run: |
          set -euo pipefail
          python3 -B tools/indicator_sampling/prepare.py \\
            --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE" \\
            --output "$GITHUB_WORKSPACE/ci-indicator/prepared" --apks "$RUNNER_TEMP/indicator-apks" \\
            2>&1 | tee ci-indicator/apk-preflight.log

      - name: Install the pinned disposable runtime and retain toolchain identities
        shell: bash
        run: |
          set -euo pipefail
          if test -e "$RUNNER_TEMP/indicator-tooling"; then
            echo 'Refusing to reuse an existing indicator runtime directory' | tee ci-indicator/bootstrap.log
            exit 1
          fi
          python3 pinned-inputs/tools/android/bootstrap_android_runtime.py \\
            --root "$RUNNER_TEMP/indicator-tooling" --create-avd 2>&1 | tee ci-indicator/bootstrap.log
          python3 - <<'PY' 2>&1 | tee ci-indicator/toolchain-metadata.log
          import hashlib, json, os
          from pathlib import Path
          root = Path(os.environ['RUNNER_TEMP']) / 'indicator-tooling'
          output = Path('ci-indicator/toolchain')
          output.mkdir()
          metadata = ['jdk21/release', 'android/platform-tools/source.properties',
              'android/emulator/source.properties',
              'android/system-images/android-35/google_apis/x86_64/source.properties',
              'android/system-images/android-35/google_apis/x86_64/build.prop',
              'android-user/avd/MacroDroid_API35_Disposable.ini',
              'android-user/avd/MacroDroid_API35_Disposable.avd/config.ini']
          binaries = ['jdk21/bin/java', 'jdk21/bin/javac', 'android/platform-tools/adb',
              'android/emulator/emulator', 'android/emulator/qemu/linux-x86_64/qemu-system-x86_64-headless']
          rows = []
          for name in metadata + binaries:
              path = root / name
              with path.open('rb') as stream:
                  digest = hashlib.file_digest(stream, 'sha256').hexdigest()
              rows.append({'path': name, 'bytes': path.stat().st_size, 'sha256': digest})
              if name in metadata:
                  target = output / name
                  target.parent.mkdir(parents=True, exist_ok=True)
                  with target.open('xb') as stream:
                      stream.write(path.read_bytes())
          (output / 'installed-inputs.json').write_text(json.dumps(rows, indent=2) + '\\n')
          print(json.dumps(rows, indent=2))
          PY

      - name: Observe the fixed A-then-B eight-install schedule on one owned AVD
        shell: bash
        run: |
          set -euo pipefail
          exec > >(tee ci-indicator/runtime-driver.log) 2>&1
          if ! test -c /dev/kvm; then
            echo 'The disposable KVM device is unavailable'
            exit 1
          fi
          sudo setfacl -m "u:$(id -un):rw" /dev/kvm
          mkdir ci-indicator/environment
          python3 -u pinned-inputs/tools/android/android_runtime_service.py \\
            --tooling "$RUNNER_TEMP/indicator-tooling" \\
            --evidence ci-indicator/environment \\
            --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \\
            > ci-indicator/service.log 2>&1 &
          indicator_service_pid=$!
          cleanup_indicator_runtime() {
            indicator_step_status=$?
            trap - EXIT INT TERM
            set +e
            timeout 30s "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb" \\
              -s emulator-5560 logcat -d -b crash -b events -v threadtime \\
              > ci-indicator/lifecycle.log 2>&1
            indicator_logcat_status=$?
            mkdir -p ci-indicator/environment/queue
            touch ci-indicator/environment/queue/STOP
            indicator_stop_status=$?
            timeout 60s tail --pid="$indicator_service_pid" -f /dev/null
            indicator_wait_status=$?
            indicator_service_status=unobserved
            if test "$indicator_wait_status" -eq 0; then
              wait "$indicator_service_pid"
              indicator_service_status=$?
            fi
            python3 - "$indicator_step_status" "$indicator_logcat_status" "$indicator_stop_status" \\
              "$indicator_wait_status" "$indicator_service_status" <<'PY'
          import json, sys
          from pathlib import Path
          names = ['diagnostic_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
                   'bounded_service_wait_exit_code', 'owned_service_exit_code']
          result = dict(zip(names, sys.argv[1:]))
          result['scope'] = 'STOP is written only to this job\\'s newly created service queue; no unrelated device or process is stopped.'
          result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
          Path('ci-indicator/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\\n')
          print(json.dumps(result, indent=2))
          PY
            indicator_cleanup_record_status=$?
            if test "$indicator_step_status" -eq 0 && { test "$indicator_stop_status" -ne 0 || test "$indicator_wait_status" -ne 0 || test "$indicator_service_status" != 0 || test "$indicator_cleanup_record_status" -ne 0; }; then
              indicator_step_status=1
            fi
            exit "$indicator_step_status"
          }
          trap cleanup_indicator_runtime EXIT
          trap 'exit 130' INT
          trap 'exit 143' TERM
          printf '%s\\n' "$indicator_service_pid" > ci-indicator/owned-service-pid.txt
          python3 pinned-inputs/tools/android/wait_android_ready.py \\
            --evidence ci-indicator/environment --timeout 900 2>&1 | tee ci-indicator/readiness.log
          python3 pinned-inputs/tools/android/runtime_job.py \\
            --queue ci-indicator/environment/queue --id indicator-radio-clock-scales --timeout 240 -- \\
            python3 "$GITHUB_WORKSPACE/pinned-inputs/tools/android/configure_capture_device.py" \\
            --adb "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb" --serial emulator-5560 \\
            --output "$GITHUB_WORKSPACE/ci-indicator/device" --demo-clock 1200 --disable-animations \\
            2>&1 | tee ci-indicator/device-job.log
          indicator_record_args=(python3 -B "$GITHUB_WORKSPACE/tools/indicator_sampling/record.py"
            --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE"
            --prepared "$GITHUB_WORKSPACE/ci-indicator/prepared"
            --adb "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb"
            --output "$GITHUB_WORKSPACE/ci-indicator/experiment" --accept-package-data-removal)
          python3 pinned-inputs/tools/android/runtime_job.py \\
            --queue ci-indicator/environment/queue --id indicator-initialize --timeout 240 -- \\
            "${indicator_record_args[@]}" --initialize --runtime "$GITHUB_WORKSPACE/ci-indicator/environment" \\
            --device "$GITHUB_WORKSPACE/ci-indicator/device" \\
            --toolchain-inputs "$GITHUB_WORKSPACE/ci-indicator/toolchain/installed-inputs.json" \\
            --tooling "$RUNNER_TEMP/indicator-tooling" 2>&1 | tee ci-indicator/initialize-job.log
          indicator_slots_status=0
          for indicator_slot in 1 2 3 4 5 6 7 8; do
            set +e
            python3 pinned-inputs/tools/android/runtime_job.py \\
              --queue ci-indicator/environment/queue --id "indicator-slot-$indicator_slot" --timeout 900 -- \\
              "${indicator_record_args[@]}" --slot "$indicator_slot" \\
              2>&1 | tee "ci-indicator/slot-$indicator_slot-job.log"
            indicator_slot_status=${PIPESTATUS[0]}
            set -e
            if test "$indicator_slot_status" -ne 0; then
              indicator_slots_status=$indicator_slot_status
              break
            fi
          done
          set +e
          python3 pinned-inputs/tools/android/runtime_job.py \\
            --queue ci-indicator/environment/queue --id indicator-finalize --timeout 900 -- \\
            "${indicator_record_args[@]}" --finish 2>&1 | tee ci-indicator/finalize-job.log
          indicator_finalize_status=${PIPESTATUS[0]}
          set -e
          if test "$indicator_slots_status" -ne 0; then
            exit "$indicator_slots_status"
          fi
          exit "$indicator_finalize_status"

      - name: Independently recheck all fixed raw frames and original live metadata
        if: always()
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p ci-indicator
          timeout 900s python3 -B tools/indicator_sampling/verify.py \\
            --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE" \\
            --prepared "$GITHUB_WORKSPACE/ci-indicator/prepared" \\
            --output "$GITHUB_WORKSPACE/ci-indicator/experiment" \\
            2>&1 | tee ci-indicator/independent-verification.log

      - name: Preserve every owned partial or complete diagnostic record
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: indicator-fixed-sampling-${{ github.sha }}
          retention-days: 30
          if-no-files-found: error
          path: ci-indicator/
          include-hidden-files: true
'''
text = template.replace('@PARENT_SPARSE@', '\n'.join('            /' + name for name in parents))
text = text.replace('@OWN_JSON@', repr(dict(sorted(own.items()))))
path = SOURCE / WORKFLOW
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(text)
rows = [{'path': name, **identity(SOURCE / name)} for name in sorted([*own, WORKFLOW])]
(OWN / 'runtime-files.json').write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps({'workflow': {'path': WORKFLOW, **identity(path)},
                  'runtime_manifest': identity(OWN / 'runtime-files.json'),
                  'source_roles': len(rows) + 1, 'parent_and_part_roles': len(parents)}, indent=2))
