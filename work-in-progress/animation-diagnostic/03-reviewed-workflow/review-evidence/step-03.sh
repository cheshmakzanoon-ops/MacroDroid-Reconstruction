set -euo pipefail
python3 scripts/materialize_v9.py --without-overlay 2>&1 | tee ci-normal-animation/materialize-toolchain.log
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-normal-animation/materialize-original.log
python3 scripts/assemble_artifact.py artifacts/current/manifest.json 2>&1 | tee ci-normal-animation/materialize-candidate.log
python3 work-in-progress/animation-diagnostic/03-reviewed-workflow/prepare_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation --materialized 2>&1 | tee ci-normal-animation/apk-preflight.log
