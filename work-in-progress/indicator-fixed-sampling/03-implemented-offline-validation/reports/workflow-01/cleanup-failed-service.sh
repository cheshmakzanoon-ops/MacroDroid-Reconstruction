set -euo pipefail
bash -c 'for ((n=0;n<200;n++)); do if test -e ci-indicator/environment/queue/STOP; then exit "$1"; fi; sleep 0.01; done; exit 99' _ 5 &
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
exit 0
