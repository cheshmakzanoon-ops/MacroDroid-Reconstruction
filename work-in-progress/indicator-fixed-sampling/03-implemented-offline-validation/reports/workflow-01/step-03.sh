set -euo pipefail
export INDICATOR_PARENTS="$GITHUB_WORKSPACE/pinned-inputs"
export INDICATOR_HOST_EVIDENCE="$GITHUB_WORKSPACE/ci-indicator/host-evidence"
timeout 900s python3 -B -m unittest discover -s tools/indicator_sampling -p 'test_*.py' -v \
  2>&1 | tee ci-indicator/host-tests.log
