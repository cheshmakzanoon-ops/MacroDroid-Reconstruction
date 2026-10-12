set -euo pipefail
bash -c 'for ((n=0;n<200;n++)); do if test -e ci-normal-animation/environment/queue/STOP; then exit "$1"; fi; sleep 0.01; done; exit 99' _ 5 &
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
exit 0
