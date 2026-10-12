#!/usr/bin/env python3
"""Read exact APK/source/capture inputs into a bounded indicator diagnosis.

This does not rebuild/install an APK, run Android, alter a frame, normalize smali,
or decide visual parity. Every disassembled class must equal preserved source.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
PROJECT = BASE / 'current/MacroDroid_v9'
OLD = BASE / 'indicator-diagnosis/checkpoints/01-preserved-source-audit'
RAW = BASE / 'ci-run-analysis/zero12-run-38216299675-extracted'
ARCHIVE = BASE / 'ci-run-analysis/zero12-run-38216299675.zip'
OUT = BASE / 'ink-indicator-study/reports/01-exact-input-and-path-observations'
JAVA = BASE / 'tooling/jdk21/bin/java'
JAR = PROJECT / 'tools/lib/jadx-r2721.4574686-all.jar'
APKS = {
    'original': (BASE / 'recovered/automation android app',
                 '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800', 95725918),
    'candidate': (Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk'),
                  '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182', 94683119),
}
EXTRA = {
    'Lagency/tango/materialintroscreen/widgets/InkPageIndicator$SavedState;': 'Saved selected-page state',
    'Lagency/tango/materialintroscreen/widgets/a;': 'Saved-state Parcelable creator',
    'Loe3;': 'Actual data-set observer arm 1',
    'Lt2h;': 'Actual page-scroll color callback',
    'Llt1;': 'Actual next-page click callback',
    'Lq77;': 'Float-expression helper used in retreat threshold',
    'Lagency/tango/materialintroscreen/R$styleable;': 'Actual attribute index array',
    'Landroidx/viewpager/widget/ViewPager;': 'Page-selection and page-scroll dispatcher',
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise AssertionError(f'Regular input required: {path}')
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': h.hexdigest()}


def exact(path: Path, sha: str, size: int | None = None) -> dict:
    row = identity(path)
    if row['sha256'] != sha or (size is not None and row['bytes'] != size):
        raise AssertionError(f'Input identity changed: {row}')
    return row


def save(name: str, data: object) -> None:
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main() -> None:
    if OUT.exists():
        raise AssertionError('Use a fresh evidence output directory')
    if shutil.disk_usage(BASE).free < 96 * 1024 * 1024:
        raise AssertionError('At least 96 MiB free required for bounded disassembly')
    OUT.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    before = []
    old_cp = OLD / 'checkpoint.json'
    before.append(exact(old_cp, '8792b2936e0d2832361c98699b707ceb7982373cbb661048b549bedfcce174ab'))
    old = json.loads(old_cp.read_text())
    for row in old['files']:
        before.append(exact(OLD / row['path'], row['sha256'], row['bytes']))
    if len(old['files']) != 28:
        raise AssertionError('Historical capsule membership changed')
    idx_path = PROJECT / 'source/class-index.json'
    before.append(identity(idx_path))
    idx = json.loads(idx_path.read_text())
    sources = []
    for row in old['files']:
        prefix = 'preserved-source/'
        if row['path'].startswith(prefix):
            sources.append((row['path'][len(prefix):], 'Exact historical eighteen-class audit member'))
    if len(sources) != 18:
        raise AssertionError('Historical class scope changed')
    for desc, reason in EXTRA.items():
        rows = [r for r in idx.values() if r['descriptor'] == desc]
        if len(rows) != 1:
            raise AssertionError(f'Expected unique class {desc}')
        sources.append((rows[0]['path'], reason))
    selected = []
    for rel, reason in sources:
        p = PROJECT / rel
        ident = identity(p)
        text = p.read_text()
        desc = next(l.rsplit(' ', 1)[-1] for l in text.splitlines() if l.startswith('.class '))
        partition = Path(rel).parts[2]
        row = idx[partition + ':' + desc]
        if ident['sha256'] != row['sha256']:
            raise AssertionError(f'Preserved class differs from canonical index: {desc}')
        before.append(ident)
        target = OUT / 'preserved-source' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
        selected.append({'descriptor': desc, 'partition': partition, 'source': rel,
                         'sha256': ident['sha256'], 'bytes': ident['bytes'], 'reason': reason})
    if len({r['descriptor'] for r in selected}) != len(selected):
        raise AssertionError('Duplicate selected descriptor')
    before.append(exact(JAR, '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e', 80076986))
    before.append(identity(JAVA))
    before.append(identity(Path(__file__).resolve()))
    commands = []
    class_results = []
    dex_entries = []
    for label, (apk, sha, size) in APKS.items():
        before.append(exact(apk, sha, size))
        with zipfile.ZipFile(apk) as z:
            for partition in sorted({r['partition'] for r in selected}):
                entry = partition + '.dex'
                with z.open(entry) as f:
                    h = hashlib.sha256()
                    count = 0
                    for b in iter(lambda: f.read(1024 * 1024), b''):
                        h.update(b)
                        count += len(b)
                dex_entries.append({'variant': label, 'entry': entry, 'bytes': count,
                                    'sha256': h.hexdigest()})
                rows = [r for r in selected if r['partition'] == partition]
                target = OUT / 'disassembled' / label / partition
                args = [str(JAVA), '-Xmx512m', '-cp', str(JAR),
                        'com.android.tools.smali.baksmali.Main', 'd', '--api', '23',
                        '--use-locals', '-j', '2', '--classes',
                        ','.join(r['descriptor'] for r in rows), '-o', str(target),
                        str(apk) + '/' + entry]
                t0 = time.monotonic()
                try:
                    proc = subprocess.run(args, capture_output=True, timeout=300, check=False)
                except subprocess.TimeoutExpired as e:
                    (OUT / f'{label}-{partition}-stdout.bin').write_bytes(e.stdout or b'')
                    (OUT / f'{label}-{partition}-stderr.bin').write_bytes(e.stderr or b'')
                    save('failure.json', {'status': 'DISASSEMBLY_TIMEOUT', 'argv': args,
                                         'elapsed_seconds': time.monotonic() - t0})
                    raise
                stdout = OUT / f'{label}-{partition}-stdout.bin'
                stderr = OUT / f'{label}-{partition}-stderr.bin'
                stdout.write_bytes(proc.stdout)
                stderr.write_bytes(proc.stderr)
                command = {'argv': args, 'returncode': proc.returncode, 'timeout_seconds': 300,
                           'elapsed_seconds': time.monotonic() - t0,
                           'stdout': identity(stdout), 'stderr': identity(stderr)}
                commands.append(command)
                save('commands.json', commands)
                if proc.returncode:
                    raise AssertionError(f'Disassembly failed: {label}/{partition}')
                actual = list(target.rglob('*.smali'))
                if len(actual) != len(rows):
                    raise AssertionError(f'Disassembled class set differs: {label}/{partition}')
                for row in rows:
                    f = target / (row['descriptor'][1:-1] + '.smali')
                    observed = identity(f)
                    equals = observed['sha256'] == row['sha256'] and observed['bytes'] == row['bytes']
                    class_results.append({**row, 'variant': label, 'output': observed,
                                          'complete_smali_bytes_equal': equals})
                save('class-byte-results.json', class_results)
    if not all(r['complete_smali_bytes_equal'] for r in class_results):
        raise AssertionError('At least one exact selected class differs; retain the observation')
    before.append(exact(ARCHIVE, '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3', 42199893))
    journey_path = RAW / 'journey/journey.json'
    before.append(exact(journey_path, 'a6253dfea14353a2d8fe552e3772e4fe5e58a693e2339bafcce9f0d008a61409', 839255))
    journey = json.loads(journey_path.read_text())
    if [r['apk_sha256'] for r in journey['runs']] != [APKS[k][1] for k in ('original', 'candidate')]:
        raise AssertionError('Captured APK bindings differ')
    names = ['intro-2-acquisition-1-frame-1', 'intro-2-acquisition-1-frame-2',
             'intro-3-before-acquisition-1-frame-1', 'intro-3-before-acquisition-1-frame-2']
    images = {}
    frame_rows = []
    with zipfile.ZipFile(ARCHIVE) as z:
        if len(z.namelist()) != 2944 or len(z.namelist()) != len(set(z.namelist())):
            raise AssertionError('Historical archive membership changed')
        for label in APKS:
            for name in names:
                stem = label + '-' + name
                for ext in ('png', 'xml'):
                    member = 'journey/' + stem + '.' + ext
                    p = RAW / member
                    row = identity(p)
                    if p.read_bytes() != z.read(member):
                        raise AssertionError(f'Raw frame differs from exact original ZIP: {member}')
                    before.append(row)
                    frame_rows.append({**row, 'archive_member': member})
                images[stem] = np.asarray(Image.open(RAW / ('journey/' + stem + '.png')).convert('RGBA'))
    pairs = []
    for left, right in itertools.combinations(sorted(images), 2):
        a, b = images[left], images[right]
        if a.shape != (1280, 720, 4) or b.shape != a.shape:
            raise AssertionError('Raw capture geometry changed')
        positions = np.argwhere(np.any(a != b, axis=2))
        pixels = [{'x': int(x), 'y': int(y), 'left_rgba': a[y, x].tolist(),
                   'right_rgba': b[y, x].tolist()} for y, x in positions]
        pairs.append({'left': left, 'right': right, 'different_pixels': len(pixels),
                      'entire_frame_compared': True, 'pixels': pixels})
    within = [p for p in pairs if p['left'].split('-')[0] == p['right'].split('-')[0]]
    cross = [p for p in pairs if p not in within]
    if len(within) != 12 or len(cross) != 16:
        raise AssertionError('Frame-pair scope changed')
    if any(p['different_pixels'] != 0 for p in within) or any(p['different_pixels'] != 5 for p in cross):
        raise AssertionError('Raw frame-pair observations differ from recorded five-pixel outcome')
    indicators = []
    for label in APKS:
        p = RAW / f'journey/{label}-intro-2-acquisition-1-frame-2.xml'
        nodes = [n for n in ET.fromstring(p.read_bytes()).iter('node')
                 if n.get('resource-id') == 'com.arlosoft.macrodroid:id/indicator']
        if len(nodes) != 1:
            raise AssertionError('Indicator selector is not unique')
        indicators.append({'variant': label, 'attributes': dict(nodes[0].attrib)})
    for row in before:
        if identity(Path(row['path'])) != row:
            raise AssertionError(f'Input changed during read-only study: {row["path"]}')
    save('input-identities-before-after.json', {'all_unchanged': True, 'inputs': before})
    save('selected-class-inventory.json', selected)
    save('apk-dex-bindings.json', dex_entries)
    save('raw-frame-inputs.json', frame_rows)
    save('all28-exact-full-frame-pairs.json', pairs)
    save('indicator-xml-observations.json', indicators)
    save('captured-environments.json', [
        {'variant': r['label'], 'before': r['environment'], 'after': r['environment_after']}
        for r in journey['runs']])
    save('result.json', {
        'status': 'EXACT_SOURCE_AND_RAW_FRAME_OBSERVATIONS_VERIFIED',
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
        'historical_class_scope': 18, 'additional_classes': len(EXTRA),
        'selected_classes': len(selected), 'apk_class_comparisons': len(class_results),
        'complete_smali_bytes_equal': all(r['complete_smali_bytes_equal'] for r in class_results),
        'raw_trigger_frames_per_apk': 4, 'within_apk_pairs': len(within),
        'within_apk_different_pixels': [p['different_pixels'] for p in within],
        'cross_apk_pairs': len(cross),
        'cross_apk_different_pixels': [p['different_pixels'] for p in cross],
        'input_files_unchanged': len(before), 'all_inputs_unchanged': True,
        'new_android_execution': False, 'apk_or_app_source_modified': False,
        'mask_tolerance_or_frame_selection': False,
        'cause_proven': False,
    })
    print(json.dumps(json.loads((OUT / 'result.json').read_text()), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.is_dir():
            save('failure.json', {'status': 'STUDY_FAILED', 'type': type(exc).__name__,
                                  'message': str(exc)})
        raise
