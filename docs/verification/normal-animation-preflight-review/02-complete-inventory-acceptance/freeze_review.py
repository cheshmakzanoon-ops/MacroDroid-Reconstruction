from pathlib import Path
import ast
import hashlib
import json

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoint'
SOURCE = BASE / 'animation-diagnostic/checkpoints/03-reviewed-workflow'
VALIDATION = BASE / 'animation-diagnostic/workflow-03/reports/validation-01'
REPO = BASE / 'MacroDroid-Reconstruction'
OUT.mkdir(exist_ok=False)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, data):
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

def jsave(name, value):
    write(name, (json.dumps(value, indent=2) + '\n').encode())

raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(raw) == '194ee4ddb8cbd31738f6f326b7e00365e0b0dafb99956708913cdb3327c1e172'
review = json.loads((ROOT / 'reports/01-corrected-preflight-replay/review-result.json').read_text())
assert len(review['cases']) == 4 and review['cases'][0]['materialized_passed'] is True
assert all(not row['materialized_passed'] and row['final_entry_rejected'] and not row['false_acceptance'] for row in review['cases'][1:])
assert review['all_eleven_frozen_files_unchanged'] and not review['android_executed']

archive_manifest = json.loads((SOURCE / 'offline-evidence-manifest.json').read_text())
frozen_files = {row['path']: row for row in archive_manifest['files']}
retained = json.loads((ROOT / 'reports/01-corrected-preflight-replay/retained-inputs-before.json').read_text())
bindings = []
for name, identity in retained.items():
    relative = Path(name).relative_to(VALIDATION).as_posix()
    bound = frozen_files[relative]
    assert identity == {key: bound[key] for key in ('bytes', 'sha256')}, name
    bindings.append(dict(review_source_path=name, frozen_evidence_path=relative, **identity,
        archive_member=bound.get('archive_member'), external_input_sha256=bound.get('external_input_sha256')))
jsave('frozen-baseline-bindings.json', dict(parent_checkpoint_sha256=sha(raw),
    evidence_manifest_sha256=sha((SOURCE / 'offline-evidence-manifest.json').read_bytes()),
    bindings=bindings, all_baseline_sources_bound_to_frozen_parent_evidence=True))

syntax = ast.parse((SOURCE / 'prepare_normal_journey.py').read_text())
namespace = {}
for node in syntax.body:
    if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in ('GUARD', 'ANIMATION', 'PINS') for target in node.targets):
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<frozen-pin-literals>', 'exec'), {}, namespace)
pins = []
for name, expected in namespace['PINS'].items():
    data = (REPO / name).read_bytes()
    assert sha(data) == expected
    pins.append(dict(path=name, bytes=len(data), sha256=expected))
assert len(pins) == 15 and not (REPO / '.github/workflows/editor-normal-animation.yml').exists()
jsave('repository-dependency-check.json', dict(expected_active_input='9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2',
    all_fifteen_current_source_pins_match=True, active_workflow_path_absent=True, files=pins))

for name in ('prepare_normal_journey.py', 'verify_normal_journey.py', '.github/workflows/editor-normal-animation.yml', 'checkpoint.json'):
    write('reviewed-inputs/' + name, (SOURCE / name).read_bytes())
for path in sorted((ROOT / 'reports').rglob('*')):
    if path.is_dir():
        continue
    assert path.is_file() and not path.is_symlink()
    write(path.relative_to(ROOT).as_posix(), path.read_bytes())
write('replay_preflight_omission.py', (ROOT / 'replay_preflight_omission.py').read_bytes())
write('freeze_review.py', Path(__file__).read_bytes())
write('README.md', b'''# Independent review of complete diagnostic input binding

The frozen Normal03 preparer and final verifier were reviewed without modifying their source. The full ordered expected input list is reconstructed from pinned repository source, the exact Trigger05 and animation checkpoints, historical fixture identities, and the two literal helper hashes in the separately reviewed workflow. The reported input list must exactly equal that expected list, and both originals and every executed copy are rehashed before copied-code imports.

The original omission reproducer was rerun against these exact corrected files. Its unchanged 190-row baseline passed real offline AAPT2 inspection of the pinned original and current 9108 APKs. The changed-bootstrap controls with 190 retained rows, 189 rows after omission, and zero rows all rejected. Each invalid input was separately supplied to both the materialized preflight and final verifier; all six entry-point checks rejected before a copied AAPT2 file or copied-code execution. No Android command was run. A complete positive final Android result was neither simulated nor claimed.

All eleven frozen Normal03 files and all protected source, tool, APK and copied-input hashes remained unchanged. The baseline-binding manifest maps every retained review input back to the immutable Normal03 evidence inventory and its archived or already published payload. Private hardlink fixtures were unlinked before the deliberate comment mutation, preserving all original bytes. The actual three mutations, reports, command arguments, outputs and verifier results are included.

The reviewer approves the specific complete-inventory correction and exact proposed normal-animation workflow for the authorized separate diagnostic. All fifteen current repository pins match, and the workflow path was absent during the review. The diagnostic must start from its reviewed commit while artifacts/current still binds the 9108 APK; subsequent combined promotion is separate. Historical Normal02 false passes and the old 26-pixel runtime difference remain unchanged. These host results do not establish animation parity or whole-app 1:1.
''')
rows = []
for path in sorted(OUT.rglob('*')):
    if not path.is_file():
        continue
    data = path.read_bytes()
    rows.append(dict(path=path.relative_to(OUT).as_posix(), bytes=len(data), sha256=sha(data)))
checkpoint = dict(status='INDEPENDENT_NORMAL03_COMPLETE_INVENTORY_REVIEW_PASSED', active_files=[], android_executed=False,
    parent_checkpoint_sha256=sha(raw), reviewed_workflow_sha256='5bcd73aa15e5ad05de1fbcdf6252292249bf48458520bd6866477cd343af7047',
    positive_materialized_cases=1, original_mutated_cases=3, negative_entry_point_checks=6,
    baseline_inventory_rows=190, frozen_parent_files_unchanged=11, files=rows)
data = (json.dumps(checkpoint, indent=2) + '\n').encode()
(OUT / 'checkpoint.json').write_bytes(data)
print(json.dumps(dict(path=str(OUT / 'checkpoint.json'), files=len(rows), bytes=sum(row['bytes'] for row in rows), sha256=sha(data))))
