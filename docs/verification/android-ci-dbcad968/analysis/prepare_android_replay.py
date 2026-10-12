#!/usr/bin/env python3
"""Bind the previously reviewed Android replay to the new dbcad raw artifact."""
import difflib
import hashlib
import json
from pathlib import Path

BASE = Path('/workspace/scratch/4130730d15aa')
PARENT = BASE / 'tooling-validation/android-run-38202401393-analysis/analyze_android_38202401393.py'
TARGET = BASE / 'ci-run-analysis/analyze_android_38214498395.py'
old = PARENT.read_text()
text = old
changes = [
    ('actual cada56c hosted capture', 'actual dbcad968 hosted capture'),
    ('38202401393', '38214498395'),
    ("OUT = BASE / 'tooling-validation/android-run-38214498395-analysis'", "OUT = BASE / 'ci-run-analysis/android-run-38214498395'"),
    ("SOURCE = BASE / 'runtime-forward'", "SOURCE = BASE / 'MacroDroid-Reconstruction'"),
    ("{'bytes': 1022164, 'sha256': '552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891'}",
     "{'bytes': 1021235, 'sha256': '46b33e5b3d22aba73644da191f60c9639fe7d600e003c1f5ce1ee471d31e7372'}"),
    ("extraction['member_count'] == 428 and len(extraction['files']) == 428", "extraction['member_count'] == 426 and len(extraction['files']) == 426"),
    ("entry['size_bytes']", "entry['bytes']"),
    ("'android_compare.py':", "'project/android_compare.py':"),
    ("'android_intro.py':", "'project/android_intro.py':"),
    ("'android_post_intro.py':", "'project/android_post_intro.py':"),
    ("[str(SOURCE), str(SOURCE / 'tools/android')]", "[str(SOURCE / 'project'), str(SOURCE / 'tools/android')]"),
    ('[0, 26, 0, 0, 0]', '[0, 35, 0, 0, 0]'),
    ('9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2', '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'),
    ("assert re.findall(r'^Ran (\\d+) tests in ([0-9.]+)s$', host_text, re.M) == [('33', '0.729')]",
     "summaries = re.findall(r'^Ran (\\d+) tests in ([0-9.]+)s$', host_text, re.M)\n    assert len(summaries) == 1 and summaries[0][0] == '33'\n    host_seconds = float(summaries[0][1])"),
    ('cada56c8a11ff5cbd892ec6d0beaeab60b3e644d', 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'),
    ("'all_archive_files_verified': 428", "'all_archive_files_verified': 426"),
    ("'seconds': 0.729", "'seconds': host_seconds"),
    ('OUT.mkdir()', 'OUT.mkdir(parents=True)'),
]
for before, after in changes:
    assert before in text, before
    text = text.replace(before, after)
text = text.replace("sys.path[:0] = [str(SOURCE / 'project'), str(SOURCE / 'tools/android')]",
                    "sys.dont_write_bytecode = True\n    sys.path[:0] = [str(SOURCE / 'project'), str(SOURCE / 'tools/android')]")
marker = "    assert [pair['changed_rgba_pixels'] for pair in pairs] == [0, 35, 0, 0, 0]"
extra = '''    indicator_frames = [np.asarray(Image.open(FOLDER / 'capture' / (v + '-intro-2.png')).convert('RGBA'))
                        for v in ('original', 'candidate')]
    yy, xx = np.where(np.any(indicator_frames[0] != indicator_frames[1], axis=2))
    indicator_pixels = [{'x': int(x), 'y': int(y), 'original_rgba': indicator_frames[0][y, x].tolist(),
                         'candidate_rgba': indicator_frames[1][y, x].tolist()} for y, x in zip(yy, xx)]
    assert len(indicator_pixels) == 35
    assert all(128 <= row['x'] < 592 and 1184 <= row['y'] < 1200 for row in indicator_pixels)
'''
assert text.count(marker) == 1
text = text.replace(marker, extra + marker)
marker = "        'full_unmasked_pairs': pairs, 'comparisons': comparisons,"
assert text.count(marker) == 1
text = text.replace(marker, marker + "\n        'all_35_intro2_differing_pixels': indicator_pixels,\n        'all_intro2_changes_inside_observed_indicator_rectangle': True,")
with TARGET.open('x') as stream:
    stream.write(text)
diff = ''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True),
    fromfile='preserved/analyze_android_38202401393.py', tofile='analyze_android_38214498395.py'))
(TARGET.parent / 'android-replay-derivation.patch').write_text(diff)
(TARGET.parent / 'android-replay-parent.json').write_text(json.dumps({
    'parent_path': str(PARENT), 'parent_sha256': hashlib.sha256(PARENT.read_bytes()).hexdigest(),
    'new_source_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    'scope': 'Same immutable source-verifier pins; new exact run/archive/member schema, APK identity, actual 35-pixel result and observed host elapsed time.'}, indent=2) + '\n')
print(TARGET)
