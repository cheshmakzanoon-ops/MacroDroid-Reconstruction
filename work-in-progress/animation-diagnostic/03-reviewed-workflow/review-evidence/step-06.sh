set -euo pipefail
mkdir -p ci-normal-animation
python3 work-in-progress/animation-diagnostic/03-reviewed-workflow/verify_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation 2>&1 | tee ci-normal-animation/independent-comparison.log
