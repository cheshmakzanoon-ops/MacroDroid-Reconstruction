set -euo pipefail
exec > >(tee ci-trigger-category/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-trigger-category/environment
python3 -u tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/macrodroid-trigger-category-tooling" \
  --evidence ci-trigger-category/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-trigger-category/service.log 2>&1 &
trigger_service_pid=$!
cleanup_trigger_runtime() {
  trigger_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/macrodroid-trigger-category-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
    > ci-trigger-category/lifecycle.log 2>&1
  trigger_logcat_status=$?
  mkdir -p ci-trigger-category/environment/queue
  touch ci-trigger-category/environment/queue/STOP
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
Path('ci-trigger-category/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
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
printf '%s\n' "$trigger_service_pid" > ci-trigger-category/owned-service-pid.txt
python3 tools/android/wait_android_ready.py --evidence ci-trigger-category/environment --timeout 900 \
  2>&1 | tee ci-trigger-category/readiness.log
python3 tools/android/runtime_job.py --queue ci-trigger-category/environment/queue   --id trigger-category-radio-clock --timeout 240 --   python3 "$GITHUB_WORKSPACE/tools/android/configure_capture_device.py"     --adb "$RUNNER_TEMP/macrodroid-trigger-category-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-trigger-category/device" --demo-clock 1200   2>&1 | tee ci-trigger-category/device-job.log
python3 tools/android/runtime_job.py --queue ci-trigger-category/environment/queue   --id trigger-category-settings --timeout 360 --   python3 "$GITHUB_WORKSPACE/work-in-progress/trigger-category/07-zero-animation-source/enable_still_animations.py"     --adb "$RUNNER_TEMP/macrodroid-trigger-category-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-trigger-category/animation-settings"   2>&1 | tee ci-trigger-category/animation-job.log
python3 tools/android/runtime_job.py --queue ci-trigger-category/environment/queue   --id trigger-category-twelve-screen --timeout 2400 --   python3 "$GITHUB_WORKSPACE/ci-trigger-category/reviewed-source/tools/parity_journeys/trigger_category_journey.py"     --source "$GITHUB_WORKSPACE/ci-trigger-category/reviewed-source/project"     --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk"     --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk"     --output "$GITHUB_WORKSPACE/ci-trigger-category/journey" --serial emulator-5560     --accept-package-data-removal --observe-denial-handoff --settle-full-frames   2>&1 | tee ci-trigger-category/journey-job.log
