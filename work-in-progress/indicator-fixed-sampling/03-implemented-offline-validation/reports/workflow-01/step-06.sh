set -euo pipefail
exec > >(tee ci-indicator/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-indicator/environment
python3 -u pinned-inputs/tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/indicator-tooling" \
  --evidence ci-indicator/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-indicator/service.log 2>&1 &
indicator_service_pid=$!
cleanup_indicator_runtime() {
  indicator_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
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
  python3 - "$indicator_step_status" "$indicator_logcat_status" "$indicator_stop_status" \
    "$indicator_wait_status" "$indicator_service_status" <<'PY'
import json, sys
from pathlib import Path
names = ['diagnostic_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
         'bounded_service_wait_exit_code', 'owned_service_exit_code']
result = dict(zip(names, sys.argv[1:]))
result['scope'] = 'STOP is written only to this job\'s newly created service queue; no unrelated device or process is stopped.'
result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
Path('ci-indicator/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
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
printf '%s\n' "$indicator_service_pid" > ci-indicator/owned-service-pid.txt
python3 pinned-inputs/tools/android/wait_android_ready.py \
  --evidence ci-indicator/environment --timeout 900 2>&1 | tee ci-indicator/readiness.log
python3 pinned-inputs/tools/android/runtime_job.py \
  --queue ci-indicator/environment/queue --id indicator-radio-clock-scales --timeout 240 -- \
  python3 "$GITHUB_WORKSPACE/pinned-inputs/tools/android/configure_capture_device.py" \
  --adb "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb" --serial emulator-5560 \
  --output "$GITHUB_WORKSPACE/ci-indicator/device" --demo-clock 1200 --disable-animations \
  2>&1 | tee ci-indicator/device-job.log
indicator_record_args=(python3 -B "$GITHUB_WORKSPACE/tools/indicator_sampling/record.py"
  --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE"
  --prepared "$GITHUB_WORKSPACE/ci-indicator/prepared"
  --adb "$RUNNER_TEMP/indicator-tooling/android/platform-tools/adb"
  --output "$GITHUB_WORKSPACE/ci-indicator/experiment" --accept-package-data-removal)
python3 pinned-inputs/tools/android/runtime_job.py \
  --queue ci-indicator/environment/queue --id indicator-initialize --timeout 240 -- \
  "${indicator_record_args[@]}" --initialize --runtime "$GITHUB_WORKSPACE/ci-indicator/environment" \
  --device "$GITHUB_WORKSPACE/ci-indicator/device" \
  --toolchain-inputs "$GITHUB_WORKSPACE/ci-indicator/toolchain/installed-inputs.json" \
  --tooling "$RUNNER_TEMP/indicator-tooling" 2>&1 | tee ci-indicator/initialize-job.log
indicator_slots_status=0
for indicator_slot in 1 2 3 4 5 6 7 8; do
  set +e
  python3 pinned-inputs/tools/android/runtime_job.py \
    --queue ci-indicator/environment/queue --id "indicator-slot-$indicator_slot" --timeout 900 -- \
    "${indicator_record_args[@]}" --slot "$indicator_slot" \
    2>&1 | tee "ci-indicator/slot-$indicator_slot-job.log"
  indicator_slot_status=${PIPESTATUS[0]}
  set -e
  if test "$indicator_slot_status" -ne 0; then
    indicator_slots_status=$indicator_slot_status
    break
  fi
done
set +e
python3 pinned-inputs/tools/android/runtime_job.py \
  --queue ci-indicator/environment/queue --id indicator-finalize --timeout 900 -- \
  "${indicator_record_args[@]}" --finish 2>&1 | tee ci-indicator/finalize-job.log
indicator_finalize_status=${PIPESTATUS[0]}
set -e
if test "$indicator_slots_status" -ne 0; then
  exit "$indicator_slots_status"
fi
exit "$indicator_finalize_status"
