set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {
    'work-in-progress/animation-diagnostic/03-reviewed-workflow/prepare_normal_journey.py': '0f700854dfc608607e018776bfcb7fd7f66a3e413d4fb6ab61dc95585e215148',
    'work-in-progress/animation-diagnostic/03-reviewed-workflow/verify_normal_journey.py': '521142186545b216bab1a7fd804e7cf2e155ca1a74899bdf77e0467d14c9ad44',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 work-in-progress/animation-diagnostic/03-reviewed-workflow/prepare_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation
