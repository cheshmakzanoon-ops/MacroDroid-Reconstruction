set -euo pipefail
timeout 120s python3 -B parent-inputs/scripts/assemble_artifact.py             parent-inputs/vendor/original/manifest.json             2>&1 | tee ci-day-numeric-art/materialize-original.log
timeout 120s python3 -B parent-inputs/scripts/assemble_artifact.py             parent-inputs/work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json             2>&1 | tee ci-day-numeric-art/materialize-numeric.log
