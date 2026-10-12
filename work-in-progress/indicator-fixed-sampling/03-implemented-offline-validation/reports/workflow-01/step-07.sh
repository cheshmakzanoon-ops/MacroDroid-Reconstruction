set -euo pipefail
mkdir -p ci-indicator
timeout 900s python3 -B tools/indicator_sampling/verify.py \
  --parents "$GITHUB_WORKSPACE/pinned-inputs" --source-root "$GITHUB_WORKSPACE" \
  --prepared "$GITHUB_WORKSPACE/ci-indicator/prepared" \
  --output "$GITHUB_WORKSPACE/ci-indicator/experiment" \
  2>&1 | tee ci-indicator/independent-verification.log
