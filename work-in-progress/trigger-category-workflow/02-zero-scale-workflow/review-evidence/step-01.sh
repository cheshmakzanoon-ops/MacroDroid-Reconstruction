set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {
    'work-in-progress/trigger-category-workflow/02-zero-scale-workflow/prepare_trigger_journey.py': 'd4f33a794cbe6b03d6e456e9a7731e016b4d5d4620f90d6397fa615fd94a1a3d',
    'work-in-progress/trigger-category-workflow/02-zero-scale-workflow/verify_trigger_journey.py': '83b23a8c2c5bd33f7629aec343e13630f1b3dcab7b2ca2f3d9bd28f3828cc406',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 work-in-progress/trigger-category-workflow/02-zero-scale-workflow/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-trigger-category
