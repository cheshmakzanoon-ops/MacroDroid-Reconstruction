set -euo pipefail
mkdir -p ci-exact-alarm-enable-return
python3 work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/verify_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-enable-return 2>&1 | tee ci-exact-alarm-enable-return/independent-comparison.log
