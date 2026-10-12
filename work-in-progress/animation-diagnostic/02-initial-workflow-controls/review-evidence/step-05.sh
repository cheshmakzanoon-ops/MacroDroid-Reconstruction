set -euo pipefail
exec > >(tee ci-normal-animation/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-normal-animation/environment
python3 -u tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/macrodroid-normal-animation-tooling" \
  --evidence ci-normal-animation/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-normal-animation/service.log 2>&1 &
normal_service_pid=$!
cleanup_normal_runtime() {
  normal_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/macrodroid-normal-animation-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
    > ci-normal-animation/lifecycle.log 2>&1
  normal_logcat_status=$?
  mkdir -p ci-normal-animation/environment/queue
  touch ci-normal-animation/environment/queue/STOP
  normal_stop_status=$?
  timeout 60s tail --pid="$normal_service_pid" -f /dev/null
  normal_wait_status=$?
  normal_service_status=unobserved
  if test "$normal_wait_status" -eq 0; then
    wait "$normal_service_pid"
    normal_service_status=$?
  fi
  python3 - "$normal_step_status" "$normal_logcat_status" "$normal_stop_status" \
    "$normal_wait_status" "$normal_service_status" <<'PY'
import json, sys
from pathlib import Path
names = ['journey_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
         'bounded_service_wait_exit_code', 'owned_service_exit_code']
result = dict(zip(names, sys.argv[1:]))
result['scope'] = 'STOP is written only to this job\'s newly created service queue; no unrelated device or process is stopped.'
result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
Path('ci-normal-animation/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
PY
  normal_cleanup_record_status=$?
  if test "$normal_step_status" -eq 0 && { test "$normal_stop_status" -ne 0 || test "$normal_wait_status" -ne 0 || test "$normal_service_status" != 0 || test "$normal_cleanup_record_status" -ne 0; }; then
    normal_step_status=1
  fi
  exit "$normal_step_status"
}
trap cleanup_normal_runtime EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$normal_service_pid" > ci-normal-animation/owned-service-pid.txt
python3 tools/android/wait_android_ready.py --evidence ci-normal-animation/environment --timeout 900 \
  2>&1 | tee ci-normal-animation/readiness.log
python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue   --id normal-animation-radio-clock --timeout 240 --   python3 "$GITHUB_WORKSPACE/tools/android/configure_capture_device.py"     --adb "$RUNNER_TEMP/macrodroid-normal-animation-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-normal-animation/device" --demo-clock 1200   2>&1 | tee ci-normal-animation/device-job.log
python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue   --id normal-animation-settings --timeout 360 --   python3 "$GITHUB_WORKSPACE/work-in-progress/animation-diagnostic/01-normal-animation-source/enable_normal_animations.py"     --adb "$RUNNER_TEMP/macrodroid-normal-animation-tooling/android/platform-tools/adb"     --serial emulator-5560 --output "$GITHUB_WORKSPACE/ci-normal-animation/animation-settings"   2>&1 | tee ci-normal-animation/animation-job.log
python3 tools/android/runtime_job.py --queue ci-normal-animation/environment/queue   --id normal-animation-ten-screen --timeout 2400 --   python3 "$GITHUB_WORKSPACE/ci-normal-animation/reviewed-source/tools/parity_journeys/favourite_info_journey.py"     --source "$GITHUB_WORKSPACE/ci-normal-animation/reviewed-source/project"     --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk"     --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk"     --output "$GITHUB_WORKSPACE/ci-normal-animation/journey" --serial emulator-5560     --accept-package-data-removal --observe-denial-handoff --settle-full-frames   2>&1 | tee ci-normal-animation/journey-job.log
