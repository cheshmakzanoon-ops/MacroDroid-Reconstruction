set -euo pipefail
python3 -B tools/indicator_sampling/prepare.py \
  --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE" \
  --output "$GITHUB_WORKSPACE/ci-indicator/prepared" --apks "$RUNNER_TEMP/indicator-apks" \
  2>&1 | tee ci-indicator/apk-preflight.log
