set -euo pipefail
bash -c 'for ((n=0;n<200;n++)); do if test -e ci-trigger-category/environment/queue/STOP; then exit "$1"; fi; sleep 0.01; done; exit 99' _ 0 &
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
exit 0
