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
