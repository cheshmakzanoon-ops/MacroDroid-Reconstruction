set -euo pipefail
mkdir ci-day-numeric-art
test "$(git rev-parse HEAD)" = "$GITHUB_SHA"
test "$(git -C parent-inputs rev-parse HEAD)" = fc825ede39a40249e33c8ba75b93128a98bd5e3c
python3 - <<'PY'
import hashlib
from pathlib import Path
pins = {
    'tools/day_numeric_art/preflight.py': '61ac7a308128661eda663d1c36ee47baba238c2aa8ded9e0545fe5939e3cffd5',
    'tools/day_numeric_art/runtime-files.json': 'e3e6b34e6a531c1fe1ba2d82aef1a25fbb5fbd4535028564d8e7af6c3b8b0be3',
}
for name, expected in pins.items():
    path = Path(name)
    if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise SystemExit('Exact numeric workflow entry point changed: ' + name)
print('Both exact numeric workflow entry points verified.')
PY
timeout 120s python3 -B tools/day_numeric_art/preflight.py             --current "$GITHUB_WORKSPACE" --parent "$GITHUB_WORKSPACE/parent-inputs"             --output "$GITHUB_WORKSPACE/ci-day-numeric-art/preflight-inputs" --phase inputs             2>&1 | tee ci-day-numeric-art/input-preflight.log
