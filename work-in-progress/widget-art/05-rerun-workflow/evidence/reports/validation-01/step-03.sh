set -euo pipefail
python3 scripts/assemble_artifact.py vendor/original/manifest.json 2>&1 | tee ci-widget-method/materialize-original.log
python3 scripts/assemble_artifact.py work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json 2>&1 | tee ci-widget-method/materialize-widget.log
