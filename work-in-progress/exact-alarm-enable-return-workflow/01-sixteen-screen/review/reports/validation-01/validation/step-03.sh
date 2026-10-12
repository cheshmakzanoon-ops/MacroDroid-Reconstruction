set -euo pipefail
python3 scripts/materialize_v9.py --without-overlay 2>&1 | tee ci-exact-alarm-enable-return/materialize-toolchain.log
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-exact-alarm-enable-return/materialize-original.log
python3 scripts/assemble_artifact.py work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json 2>&1 | tee ci-exact-alarm-enable-return/materialize-candidate.log
python3 work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-enable-return --materialized 2>&1 | tee ci-exact-alarm-enable-return/apk-preflight.log
