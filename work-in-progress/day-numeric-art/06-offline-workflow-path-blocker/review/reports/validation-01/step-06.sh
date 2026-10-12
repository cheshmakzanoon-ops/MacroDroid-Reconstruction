set -euo pipefail
exec > >(tee ci-day-numeric-art/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-day-numeric-art/environment
python3 -u parent-inputs/tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/macrodroid-numeric-art-tooling" \
  --evidence ci-day-numeric-art/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-day-numeric-art/service.log 2>&1 &
numeric_service_pid=$!
cleanup_numeric_runtime() {
  numeric_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/macrodroid-numeric-art-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
    > ci-day-numeric-art/lifecycle.log 2>&1
  numeric_logcat_status=$?
  mkdir -p ci-day-numeric-art/environment/queue
  touch ci-day-numeric-art/environment/queue/STOP
  numeric_stop_status=$?
  timeout 60s tail --pid="$numeric_service_pid" -f /dev/null
  numeric_wait_status=$?
  numeric_service_status=unobserved
  if test "$numeric_wait_status" -eq 0; then
    wait "$numeric_service_pid"
    numeric_service_status=$?
  fi
  python3 - "$numeric_step_status" "$numeric_logcat_status" "$numeric_stop_status" \
    "$numeric_wait_status" "$numeric_service_status" <<'PY'
import json, sys
from pathlib import Path
names = ['probe_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
         'bounded_service_wait_exit_code', 'owned_service_exit_code']
result = dict(zip(names, sys.argv[1:]))
result['scope'] = 'STOP is written only to this job\'s newly created service queue; no unrelated device or process is stopped.'
result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
Path('ci-day-numeric-art/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
PY
  numeric_cleanup_record_status=$?
  if test "$numeric_step_status" -eq 0 && { test "$numeric_stop_status" -ne 0 || test "$numeric_wait_status" -ne 0 || test "$numeric_service_status" != 0 || test "$numeric_cleanup_record_status" -ne 0; }; then
    numeric_step_status=1
  fi
  exit "$numeric_step_status"
}
trap cleanup_numeric_runtime EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$numeric_service_pid" > ci-day-numeric-art/owned-service-pid.txt
python3 parent-inputs/tools/android/wait_android_ready.py --evidence ci-day-numeric-art/environment --timeout 900 \
  2>&1 | tee ci-day-numeric-art/readiness.log
python3 parent-inputs/tools/android/runtime_job.py --queue ci-day-numeric-art/environment/queue \
  --id day-numeric-method-art --timeout 720 -- \
  python3 "$GITHUB_WORKSPACE/tools/day_numeric_art/android_numeric_method_probe.py" \
    --adb "$RUNNER_TEMP/macrodroid-numeric-art-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --avd MacroDroid_API35_Disposable \
    --original "$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-original.apk" \
    --candidate "$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-day-numeric-0762aad9.apk" \
    --probe "$GITHUB_WORKSPACE/tools/day_numeric_art/probes/day-numeric-method-probe.dex" \
    --provenance "$GITHUB_WORKSPACE/tools/day_numeric_art/probes/day-numeric-method-probe.json" \
    --output "$GITHUB_WORKSPACE/ci-day-numeric-art/probe" --timeout 120 \
  2>&1 | tee ci-day-numeric-art/runtime-job.log
