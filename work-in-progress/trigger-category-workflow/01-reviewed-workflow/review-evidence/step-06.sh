set -euo pipefail
mkdir -p ci-trigger-category
python3 work-in-progress/trigger-category-workflow/01-reviewed-workflow/verify_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-trigger-category 2>&1 | tee ci-trigger-category/independent-comparison.log
