set -euo pipefail
exec > >(tee ci-exact-alarm-enable-return/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-exact-alarm-enable-return/environment
python3 -u tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/macrodroid-exact-alarm-enable-return-tooling" \
  --evidence ci-exact-alarm-enable-return/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-exact-alarm-enable-return/service.log 2>&1 &
trigger_service_pid=$!
cleanup_trigger_runtime() {
  trigger_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/macrodroid-exact-alarm-enable-return-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
    > ci-exact-alarm-enable-return/lifecycle.log 2>&1
  trigger_logcat_status=$?
  mkdir -p ci-exact-alarm-enable-return/environment/queue
  touch ci-exact-alarm-enable-return/environment/queue/STOP
  trigger_stop_status=$?
  timeout 60s tail --pid="$trigger_service_pid" -f /dev/null
  trigger_wait_status=$?
  trigger_service_status=unobserved
  if test "$trigger_wait_status" -eq 0; then
    wait "$trigger_service_pid"
    trigger_service_status=$?
  fi
  python3 - "$trigger_step_status" "$trigger_logcat_status" "$trigger_stop_status" \
    "$trigger_wait_status" "$trigger_service_status" <<'PY'
import json, sys
from pathlib import Path
names = ['journey_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
         'bounded_service_wait_exit_code', 'owned_service_exit_code']
result = dict(zip(names, sys.argv[1:]))
result['scope'] = 'STOP is written only to this job\'s newly created service queue; no unrelated device or process is stopped.'
result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
Path('ci-exact-alarm-enable-return/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
PY
  trigger_cleanup_record_status=$?
  if test "$trigger_step_status" -eq 0 && { test "$trigger_stop_status" -ne 0 || test "$trigger_wait_status" -ne 0 || test "$trigger_service_status" != 0 || test "$trigger_cleanup_record_status" -ne 0; }; then
    trigger_step_status=1
  fi
  exit "$trigger_step_status"
}
trap cleanup_trigger_runtime EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$trigger_service_pid" > ci-exact-alarm-enable-return/owned-service-pid.txt
python3 tools/android/wait_android_ready.py --evidence ci-exact-alarm-enable-return/environment --timeout 900 \
  2>&1 | tee ci-exact-alarm-enable-return/readiness.log
python3 tools/android/runtime_job.py --queue ci-exact-alarm-enable-return/environment/queue   --id exact-alarm-enable-return-radio-clock --timeout 240 --   python3 "$GITHUB_WORKSPACE/tools/android/configure_capture_device.py"     --adb "$RUNNER_TEMP/macrodroid-exact-alarm-enable-return-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-exact-alarm-enable-return/device" --demo-clock 1200   2>&1 | tee ci-exact-alarm-enable-return/device-job.log
python3 tools/android/runtime_job.py --queue ci-exact-alarm-enable-return/environment/queue   --id exact-alarm-enable-return-settings --timeout 360 --   python3 "$GITHUB_WORKSPACE/work-in-progress/trigger-category/07-zero-animation-source/enable_still_animations.py"     --adb "$RUNNER_TEMP/macrodroid-exact-alarm-enable-return-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-exact-alarm-enable-return/animation-settings"   2>&1 | tee ci-exact-alarm-enable-return/animation-job.log
python3 tools/android/runtime_job.py --queue ci-exact-alarm-enable-return/environment/queue   --id exact-alarm-enable-return-sixteen-screen --timeout 2400 --   python3 "$GITHUB_WORKSPACE/ci-exact-alarm-enable-return/reviewed-source/tools/parity_journeys/exact_alarm_enable_return.py"     --source "$GITHUB_WORKSPACE/ci-exact-alarm-enable-return/reviewed-source/project"     --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk"     --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-day-numeric-0762aad9.apk"     --output "$GITHUB_WORKSPACE/ci-exact-alarm-enable-return/journey" --serial emulator-5560     --accept-package-data-removal --observe-denial-handoff --settle-full-frames --observe-notification-readiness   2>&1 | tee ci-exact-alarm-enable-return/journey-job.log
