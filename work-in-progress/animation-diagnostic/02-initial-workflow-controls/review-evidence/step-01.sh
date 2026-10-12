set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import hashlib
pins = {
    'work-in-progress/animation-diagnostic/02-reviewed-workflow/prepare_normal_journey.py': '0f0c022f556f9798afd886e1943f6e2fc63e35dc0498abe1e6db2b53fce72129',
    'work-in-progress/animation-diagnostic/02-reviewed-workflow/verify_normal_journey.py': '47137b6f86a95e42ae55aa1d5362e471139436b714c88a07e047bfc17b04b03c',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Reviewed diagnostic helper changed: ' + name)
PY
python3 work-in-progress/animation-diagnostic/02-reviewed-workflow/prepare_normal_journey.py --root "$GITHUB_WORKSPACE" --output ci-normal-animation
