set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {
    'work-in-progress/trigger-category-workflow/01-reviewed-workflow/prepare_trigger_journey.py': '9111bd7ce1e5556c068f148882d81048f54650dee94bdf4fc22179137022ef76',
    'work-in-progress/trigger-category-workflow/01-reviewed-workflow/verify_trigger_journey.py': '211651584053c4961281812ce9f66d236bd66249229ab1d099aac8431e1a7b38',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 work-in-progress/trigger-category-workflow/01-reviewed-workflow/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-trigger-category
