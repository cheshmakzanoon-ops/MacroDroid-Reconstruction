"""Derive the same strict archive-mapping publication path for Numeric ART04 only."""
from pathlib import Path
import difflib, hashlib, json
BASE=Path('/dev/shm/macrodroid-transfer-space-20261012')
old=(BASE/'prepare_settings03_capsules.py').read_text()
pairs=[
 ('6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051','14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb'),
 ('work-in-progress/exact-alarm-enable-return/03-source-and-host-controls','work-in-progress/day-numeric-art/04-wrapper-host-controls'),
 ("row['bytes'] == 13014001","row['bytes'] == 16898593"),
 ('51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755','56e15009933932b5f197d4f985f4cd7677116b74bf5b3484a36fcbb4088ee47f'),
 ("len(transport['parts']) == 2 and len({x['path'] for x in transport['parts']}) == 2",
  "len(transport['parts']) == 3 and len({x['path'] for x in transport['parts']}) == 3"),
 ('direct_original_payloads=180','direct_original_payloads=25'),
]
new=old
for before,after in pairs:
    assert new.count(before)==1,before
    new=new.replace(before,after)
with (BASE/'prepare_numeric_art04_capsules.py').open('x') as f:f.write(new)
with (BASE/'numeric-art04-publication-preparer.patch').open('x') as f:
    f.write(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),
     fromfile='prepare_settings03_capsules.py',tofile='prepare_numeric_art04_capsules.py')))
result=dict(before_sha256=hashlib.sha256(old.encode()).hexdigest(),after_sha256=hashlib.sha256(new.encode()).hexdigest(),
            substitutions=len(pairs),original_preserved=(BASE/'prepare_settings03_capsules.py').read_text()==old,
            only_exact_closed_archive_identity_and_counts_changed=True)
with (BASE/'numeric-art04-publication-preparer-derivation.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

