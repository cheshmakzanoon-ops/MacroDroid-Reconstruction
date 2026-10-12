set -euo pipefail
python3 -m unittest discover -s tools/android -p 'test_download_retry.py' -v 2>&1 | tee ci-widget-method/download-tests.log
export WIDGET_PROBE_CONTROL_EVIDENCE="$GITHUB_WORKSPACE/ci-widget-method/host-control-evidence"
python3 -m unittest discover -s work-in-progress/widget-art/04-avd-parser-fix -p 'test_android_widget_method_probe.py' -v 2>&1 | tee ci-widget-method/wrapper-tests.log
