set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {
    'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/prepare_trigger_journey.py': 'd0a421e7e106a3a5a4cd68068def7a305c4b3b491669ecfd878e021396b9b4f3',
    'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/verify_trigger_journey.py': '13eb0cd1ef23b9d20ee258282cc1e8fbef255f7462bfdc783f87c2a084e850ce',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen/prepare_trigger_journey.py --root "$GITHUB_WORKSPACE" --output ci-exact-alarm-enable-return
