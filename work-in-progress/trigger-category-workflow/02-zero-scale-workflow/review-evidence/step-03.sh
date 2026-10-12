set -euo pipefail
python3 scripts/materialize_v9.py --without-overlay 2>&1 | tee ci-trigger-category/materialize-toolchain.log
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-trigger-category/materialize-original.log
python3 scripts/assemble_artifact.py work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json 2>&1 | tee ci-trigger-category/materialize-candidate.log
python3 work-in-progress/trigger-category-workflow/02-zero-scale-workflow/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-trigger-category --materialized 2>&1 | tee ci-trigger-category/apk-preflight.log
