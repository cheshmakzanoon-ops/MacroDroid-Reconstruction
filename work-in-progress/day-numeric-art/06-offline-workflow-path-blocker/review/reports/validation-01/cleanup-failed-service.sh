set -euo pipefail
bash -c 'for ((n=0;n<200;n++)); do if test -e ci-day-numeric-art/environment/queue/STOP; then exit "$1"; fi; sleep 0.01; done; exit 99' _ 5 &
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
exit 0
