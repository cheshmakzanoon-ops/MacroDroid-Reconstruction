set -euo pipefail
exec > >(tee ci-widget-method/runtime-driver.log) 2>&1
if ! test -c /dev/kvm; then
  echo 'The disposable KVM device is unavailable'
  exit 1
fi
sudo setfacl -m "u:$(id -un):rw" /dev/kvm
mkdir ci-widget-method/environment
python3 -u tools/android/android_runtime_service.py \
  --tooling "$RUNNER_TEMP/macrodroid-widget-tooling" \
  --evidence ci-widget-method/environment \
  --avd MacroDroid_API35_Disposable --port 5560 --acceleration on \
  > ci-widget-method/service.log 2>&1 &
widget_service_pid=$!
cleanup_widget_runtime() {
  widget_step_status=$?
  trap - EXIT INT TERM
  set +e
  timeout 30s "$RUNNER_TEMP/macrodroid-widget-tooling/android/platform-tools/adb" \
    -s emulator-5560 logcat -d -b crash -b events -v threadtime \
    > ci-widget-method/lifecycle.log 2>&1
  widget_logcat_status=$?
  mkdir -p ci-widget-method/environment/queue
  touch ci-widget-method/environment/queue/STOP
  widget_stop_status=$?
  timeout 60s tail --pid="$widget_service_pid" -f /dev/null
  widget_wait_status=$?
  widget_service_status=unobserved
  if test "$widget_wait_status" -eq 0; then
    wait "$widget_service_pid"
    widget_service_status=$?
  fi
  python3 - "$widget_step_status" "$widget_logcat_status" "$widget_stop_status" \
    "$widget_wait_status" "$widget_service_status" <<'PY'
import json, sys
from pathlib import Path
names = ['probe_step_exit_code', 'diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
         'bounded_service_wait_exit_code', 'owned_service_exit_code']
result = dict(zip(names, sys.argv[1:]))
result['scope'] = 'STOP is written only to this job\'s newly created service queue; no unrelated device or process is stopped.'
result['service_cleanup_confirmed'] = sys.argv[3:] == ['0', '0', '0']
Path('ci-widget-method/runtime-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
PY
  widget_cleanup_record_status=$?
  if test "$widget_step_status" -eq 0 && { test "$widget_stop_status" -ne 0 || test "$widget_wait_status" -ne 0 || test "$widget_service_status" != 0 || test "$widget_cleanup_record_status" -ne 0; }; then
    widget_step_status=1
  fi
  exit "$widget_step_status"
}
trap cleanup_widget_runtime EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$widget_service_pid" > ci-widget-method/owned-service-pid.txt
python3 tools/android/wait_android_ready.py --evidence ci-widget-method/environment --timeout 900 \
  2>&1 | tee ci-widget-method/readiness.log
python3 tools/android/runtime_job.py --queue ci-widget-method/environment/queue \
  --id widget-method-art --timeout 720 -- \
  python3 "$GITHUB_WORKSPACE/work-in-progress/widget-art/04-avd-parser-fix/android_widget_method_probe.py" \
    --adb "$RUNNER_TEMP/macrodroid-widget-tooling/android/platform-tools/adb" \
    --serial emulator-5560 --avd MacroDroid_API35_Disposable \
    --original "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-original.apk" \
    --candidate "$GITHUB_WORKSPACE/workspace/artifacts/MacroDroid-5.67.8-widget-update-06.apk" \
    --probe "$GITHUB_WORKSPACE/work-in-progress/widget-art/04-avd-parser-fix/probes/widget-method-probe.dex" \
    --provenance "$GITHUB_WORKSPACE/work-in-progress/widget-art/04-avd-parser-fix/probes/widget-method-probe.json" \
    --output "$GITHUB_WORKSPACE/ci-widget-method/probe" --timeout 120 \
  2>&1 | tee ci-widget-method/runtime-job.log
