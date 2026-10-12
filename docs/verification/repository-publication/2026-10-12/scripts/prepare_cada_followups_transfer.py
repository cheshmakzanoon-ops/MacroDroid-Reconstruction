from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
TOOLS = ROOT / 'tooling-validation'
EXPORT = ROOT / 'cada-followups-transfer'
EXPORT.mkdir(exist_ok=True)
paths = set()
receipts = {}
PART = 8 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()


def save(name, data, mode=0o644):
    name = safe(name)
    p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    p.chmod(mode)
    paths.add(name)


def jsave(name, value):
    save(name, (json.dumps(value, indent=2) + '\n').encode())


def checkpoint(source, prefix, expected, skip=()):
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected
    record = json.loads(raw)
    for row in record['files']:
        name = safe(row['path'])
        p = source / name
        assert not p.is_symlink()
        b = p.read_bytes()
        assert len(b) == row.get('bytes', row.get('size_bytes')) and sha(b) == row['sha256'], name
        if name not in skip:
            save(prefix + '/' + name, b, 0o755 if p.stat().st_mode & 0o111 else 0o644)
    save(prefix + '/checkpoint.json', raw)
    return record


def multipart(data, prefix, name, identity, purpose, media='application/gzip'):
    parts = []
    for i, offset in enumerate(range(0, len(data), PART), 1):
        b = data[offset:offset + PART]
        path = prefix + f'/part-{i:04d}.part'
        save(path, b)
        parts.append(dict(path=path, size_bytes=len(b), sha256=sha(b), git_blob_sha1=oid(b)))
    manifest = dict(format='macrodroid-multipart-artifact', format_version=1, id=identity,
                    filename=name, media_type=media, purpose=purpose,
                    size_bytes=len(data), sha256=sha(data), parts=parts)
    jsave(prefix + '/manifest.json', manifest)
    combined = hashlib.sha256()
    size = 0
    for row in parts:
        b = (REPO / row['path']).read_bytes()
        assert len(b) == row['size_bytes'] and sha(b) == row['sha256']
        combined.update(b); size += len(b)
    assert size == len(data) and combined.hexdigest() == sha(data)
    return manifest


union_prefix = 'work-in-progress/combined-widget-plugin/01-source-union'
union = checkpoint(ROOT / 'combined-recovery/checkpoints/01-source-union', union_prefix,
                   'ff2f4a55335a6efe4212b9a906bddd604368fb1fb76ff44c7b39d890359340fc')
assert len(union['files']) == 63 and union['active_source_changed'] is False and union['active_apk_changed'] is False
receipts['combined-source-union'] = dict(files=63, status=union['status'])

failure_source = ROOT / 'widget-recovery/checkpoints/06-corrected-message-failure'
failure_prefix = 'work-in-progress/widget-update/06-corrected-message-failure'
failure = checkpoint(failure_source, failure_prefix, '6164aeaad35d5aa02bd97f2c729fb9253ca6bbd61785c5837b31450a5429ccf3', skip=['complete-reports.tar.gz'])
archive = (failure_source / 'complete-reports.tar.gz').read_bytes()
inventory = json.loads((failure_source / 'complete-reports-inventory.json').read_text())
assert inventory['archive']['bytes'] == len(archive) and inventory['archive']['sha256'] == sha(archive)
expected = {r['path']: r for r in inventory['files']}
seen = set()
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as t:
    for m in t.getmembers():
        if m.isdir():
            continue
        assert m.isfile()
        name = safe(m.name)
        assert name in expected and name not in seen
        seen.add(name)
        b = t.extractfile(m).read()
        assert len(b) == expected[name]['bytes'] and sha(b) == expected[name]['sha256']
assert seen == set(expected) and len(seen) == 68
failure_manifest = multipart(archive, failure_prefix + '/complete-reports',
                             'Widget-06-corrected-message-failure-reports.tar.gz',
                             'widget-06-corrected-message-failure-reports',
                             'Complete unchanged reports from the failed VM-message comparison')
save(failure_prefix + '/ARCHIVE_LAYOUT.md', f'''# Exact archive publication layout

The original `checkpoint.json` is unchanged. Its declared `complete-reports.tar.gz` is preserved as two binary parts under `complete-reports/` because the exact {len(archive):,}-byte archive exceeds the connector's encoded single-request limit. Every other declared checkpoint file is copied unchanged.

The parts reconstruct SHA-256 `{sha(archive)}`. All 68 archive members were independently checked against `complete-reports-inventory.json`. The one UI message mismatch remains a failed result, with zero unsupported executions; this publication makes no active source, APK or Android change.

Verify the complete archive without creating another copy:

```bash
python3 scripts/assemble_artifact.py {failure_prefix}/complete-reports/manifest.json --verify-only
```

To materialize the exact path declared by the frozen checkpoint:

```bash
python3 scripts/assemble_artifact.py {failure_prefix}/complete-reports/manifest.json --output {failure_prefix}/complete-reports.tar.gz
```

The unchanged b79 APK is already preserved by `../06-initial-signed-failure/apk/manifest.json` at commit `5024b1b46056de6a6e76a61883b469521a89ea44`.
'''.encode())
jsave(failure_prefix + '/publication-verification.json', dict(
    frozen_checkpoint_sha256='6164aeaad35d5aa02bd97f2c729fb9253ca6bbd61785c5837b31450a5429ccf3',
    declared_files_verified=len(failure['files']), unchanged_normal_files=55,
    multipart_declared_file='complete-reports.tar.gz', multipart_manifest='complete-reports/manifest.json',
    exact_archive_size_bytes=len(archive), exact_archive_sha256=sha(archive),
    all_68_member_hashes_verified=True, duplicate_assembled_archive_created=False,
    unchanged_apk_manifest=failure['apk']['manifest_path'], unchanged_apk_commit='5024b1b46056de6a6e76a61883b469521a89ea44',
    active_source_or_apk_changed=False))
assert json.loads((REPO / failure['apk']['manifest_path']).read_text())['sha256'] == failure['apk']['sha256']
receipts['corrected-message-failure'] = dict(files=56, report_members=68, archive_bytes=len(archive), status=failure['status'])
del archive

policy_source = ROOT / 'widget-recovery/checkpoints/06-host-runtime-policy'
policy_prefix = 'work-in-progress/widget-update/06-host-runtime-policy'
policy = checkpoint(policy_source, policy_prefix, 'cc68ba264c1ac530a8a0cf536ab40e391fe489c9c084c700d06a10c9d813405a')
with tarfile.open(policy_source / 'input-snapshot.tar.gz', 'r:gz') as t:
    members = [m for m in t.getmembers() if m.isfile()]
    assert len(members) == 1 and all(m.isdir() or m.isfile() for m in t.getmembers())
    safe(members[0].name)
    b = t.extractfile(members[0]).read()
    assert len(b) == policy['input_manifest']['bytes'] and sha(b) == policy['input_manifest']['sha256']
    snapshot = json.loads(b)
    assert snapshot['snapshot_sha256'] == policy['input_snapshot_sha256'] and snapshot['files'] == len(snapshot['entries']) == 81266
receipts['host-runtime-policy'] = dict(files=25, snapshot_entries=81266, status=policy['status'])

editor_prefix = 'docs/verification/editor-journey/run-38202401351-attempt-1/analysis'
editor = checkpoint(TOOLS / 'editor-run-38202401351/analysis', editor_prefix,
                    '52e34e854596a02323f38c5d07cbe6cb3e4fea579ab328eeee360357d9ca5f74')
assert len(editor['files']) == 104
receipts['editor-analysis'] = dict(files=105, source_run=38202401351, scope=editor['scope'])

android_prefix = 'docs/verification/android-ci-cada56c'
android_folder = TOOLS / 'hosted-run-38202401393'
extraction = json.loads((TOOLS / 'hosted-run-38202401393-extraction.json').read_text())
archive = (TOOLS / 'android-cold-launch-run-38202401393.zip').read_bytes()
assert len(archive) == extraction['size_bytes'] == 1022164 and sha(archive) == extraction['sha256'] == '552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891'
expected = {r['path']: r for r in extraction['files']}
assert len(expected) == 428
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    seen = set()
    for m in z.infolist():
        if m.is_dir():
            continue
        name = safe(m.filename)
        assert name in expected and name not in seen
        seen.add(name)
        b = z.read(m)
        assert b == (android_folder / name).read_bytes()
        assert len(b) == expected[name]['size_bytes'] and sha(b) == expected[name]['sha256']
        save(android_prefix + '/' + name, b)
    assert seen == set(expected)
multipart(archive, android_prefix, 'Android-cada56c-run-38202401393.zip',
          'android-cada56c-run-38202401393', 'Exact failed Android workflow artifact, including successful cold/ART scopes', 'application/zip')
for src, dest in [('hosted-run-38202401393-extraction.json', 'extraction-receipt.json'),
                  ('hosted-run-38202401393-github-artifact.json', 'github-artifact.json'),
                  ('hosted-run-38202401393-github-job.json', 'github-job.json')]:
    save(android_prefix + '/' + dest, (TOOLS / src).read_bytes())
analysis_folder = TOOLS / 'android-run-38202401393-analysis'
analysis = json.loads((analysis_folder / 'independent-analysis.json').read_text())
assert analysis['all_archive_files_verified'] == 428 and analysis['all_three_exact_comparator_replays_match'] is True
assert [p['changed_rgba_pixels'] for p in analysis['full_unmasked_pairs']] == [0, 26, 0, 0, 0]
assert analysis['constructor_probe_independent_verify_result'] is True
assert analysis['tooling_host_tests']['count'] == analysis['tooling_host_tests']['individual_ok_lines'] == 33
analysis_paths = []
for p in sorted(analysis_folder.iterdir()):
    assert p.is_file()
    dest = android_prefix + '/analysis/' + p.name
    save(dest, p.read_bytes()); analysis_paths.append(dest)
for src, dest in [('analyze_android_38202401393-initial.py', 'initial-inline-log-parser.py'),
                  ('android-38202401393-parser-format-note.json', 'parser-format-note.json')]:
    path = android_prefix + '/analysis/' + dest
    save(path, (TOOLS / src).read_bytes()); analysis_paths.append(path)
readme = f'''# Hosted Android capture: cada56c

Run [38202401393](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38202401393) used source commit `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d`. Its Android job failed the requested capture comparison. Independent replay preserves the exact failed result while validating the successful cold-launch and standalone ART evidence.

| Measured scope | Actual result |
| --- | --- |
| Cold launch / first intro page | Exact full 720 × 1280 RGBA pixels and XML; installed APK identities verified |
| Four intro pages and three Next transitions | Complete capture; transitions agree; TRIGGERS differs by 26 pixels, the other pages by zero; strict intro gate fails |
| Post-intro notification surface | Raw PNG and XML pairs agree exactly; the aggregate post-intro gate retains its failed intro prerequisite |
| Standalone constructor allocation on ART | Passed pinned DEX/device checks, `-Xverify:all`, exact stdout marker and cleanup verification |
| Tooling host tests | 33 individual successes in 0.729 seconds |

The original installed APK is `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the candidate is the unchanged active 1,240-body build `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. The ART allocation probe is a separate prerequisite, not Widget application behavior or whole-app parity. The successful source-build job is preserved separately in [source-ci-cada56c](../source-ci-cada56c/README.md).

## Exact evidence and replay

All 428 raw artifact files are copied unchanged. The exact 1,022,164-byte GitHub artifact ZIP has SHA-256 `552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891`; `manifest.json` and `extraction-receipt.json` bind its parts and every extracted member. The raw sanitizer's recorded omissions remain part of the original evidence; publisher scanning found no private-key or token patterns.

[Independent analysis](analysis/independent-analysis.json) records all three comparator replays, {analysis['recorded_artifact_hashes_verified']['capture']} capture and {analysis['recorded_artifact_hashes_verified']['constructor']} constructor artifact paths, all six runtime-report bindings, image hashes and changed-pixel bounds. The exact ready-status JSON was recovered from captured readiness stdout and verified against its recorded hash; the final live status file correctly records the subsequent stopped state.

The replay uses four exact verifier-source hashes and full images without masks. Its executable source is [analyze_android_38202401393.py](analysis/analyze_android_38202401393.py). Five new transport tests print between their unittest headers and success markers; [the parser note](analysis/parser-format-note.json) retains the initial inline-only counting assumption and the narrow correction requiring 33 distinct headers, 33 success markers and the exact successful suite summary. No CI evidence or comparator result was changed by that adjustment.

```bash
python3 scripts/assemble_artifact.py docs/verification/android-ci-cada56c/manifest.json --verify-only
```

These measurements cover the recorded stills, transitions, controlled device state and standalone allocation probe. They do not establish runtime equality for the whole application, other device states, animations, permissions or Widget behavior.
'''
save(android_prefix + '/README.md', readme.encode()); analysis_paths.append(android_prefix + '/README.md')
jsave(android_prefix + '/analysis/checkpoint.json', dict(
    source_run=38202401393, source_commit='cada56c8a11ff5cbd892ec6d0beaeab60b3e644d',
    scope='Independent read-only replay of exact preserved hosted Android evidence',
    files=[dict(path=Path(p).relative_to(android_prefix).as_posix(), bytes=(REPO / p).stat().st_size,
                sha256=sha((REPO / p).read_bytes())) for p in analysis_paths]))

host_prefix = android_prefix + '/tooling-host-tests'
host_record = json.loads((TOOLS / 'hosted-tools-run-38202401393-extraction.json').read_text())
host_zip = (TOOLS / 'android-tooling-host-tests-run-38202401393.zip').read_bytes()
assert len(host_zip) == host_record['size_bytes'] == 1299 and sha(host_zip) == host_record['sha256']
assert len(host_record['files']) == 1
for row in host_record['files']:
    b = (TOOLS / 'hosted-tools-run-38202401393' / row['path']).read_bytes()
    assert len(b) == row['size_bytes'] and sha(b) == row['sha256']
    save(host_prefix + '/' + row['path'], b)
multipart(host_zip, host_prefix, 'Android-tooling-cada56c-run-38202401393.zip',
          'android-tooling-cada56c-run-38202401393', 'Exact 33-test tooling host log artifact', 'application/zip')
save(host_prefix + '/extraction-receipt.json', (TOOLS / 'hosted-tools-run-38202401393-extraction.json').read_bytes())
save(host_prefix + '/github-artifact.json', (TOOLS / 'hosted-tools-run-38202401393-github-artifact.json').read_bytes())
receipts['android-cada56c'] = dict(raw_members=428, comparator_replays=3, pixel_vector=[0, 26, 0, 0, 0], tooling_tests=33)

source_folder = TOOLS / 'source-run-38202401393-publication'
source_prefix = 'docs/verification/source-ci-cada56c'
verification = json.loads((source_folder / 'independent-verification.json').read_text())
assert verification['status'] == 'COMPLETE_CONFIGURED_HOST_ACCEPTANCE_VERIFIED'
assert len(verification['gate_log_checks']) == 16 and len(verification['fresh_evidence_checks']) == 19
source_readme = '''# Hosted source verification: cada56c

The source-build job in [run 38202401393](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38202401393) completed successfully at 04:21:56 UTC on 2026-10-12 for commit `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d`.

All 16 configured host acceptance gates passed. Independent artifact review verified all 16 gate-log hashes and all 19 fresh evidence hashes. The fresh reports contain 188,791 original/JVM/rebuilt cases across exactly 1,240 methods, with zero mismatches or unsupported executions, all 259 Python tests passed in 6.340 seconds, and all 37 UI fault controls rejected their required case before an 18,476-case clean restoration. Static and linkage reports record zero constructor-owner corrections for this active source.

The before/after source-input pin is unchanged: `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`, covering 81,245 files. CI performed the input verification. The publisher separately verified the exact committed manifest bytes and 81,245 entries; it did not independently rehash every materialized source input during artifact review.

The rebuilt hybrid APK is 94,683,497 bytes, SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. The baseline is 94,677,674 bytes, SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`. Both exact byte sequences are already durably represented by their multipart manifests at commit `3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677`.

## Complete artifact contents

The 127,146,419-byte GitHub source artifact has SHA-256 `6e4290fb8e54265cb441db0317a771ea9320be0b720d241b36ac6a7dc94f575f`. All 108 payloads were read and hash-verified. All 106 exact report/log files are included here; the two APK payloads map to their immutable existing manifests in [manifest.json](manifest.json). Earlier retained report directories remain historical files, and the fresh run is `reports/acceptance-20261012T040751585250Z/`.

[Independent verification](independent-verification.json) records the individual checks and preservation mappings. [The executed verifier](verify_source_38202401393.py), original GitHub job and artifact metadata are included for review. The fresh gate report is [acceptance-latest.json](reports/acceptance-latest.json).

This source job did not execute Android; its ADB capability probe reported BLOCKED. The separate Android job failed its strict intro-dependent capture gate despite exact cold launch and a successful standalone ART allocation probe. Its actual results are preserved in [android-ci-cada56c](../android-ci-cada56c/README.md). These source checks do not establish complete high-level Java/Kotlin recovery or whole-app runtime parity.
'''
assert not (source_folder / 'README.md').exists() or (source_folder / 'README.md').read_text() == source_readme
(source_folder / 'README.md').write_text(source_readme)
source_paths = []
for p in sorted(source_folder.rglob('*')):
    if p.is_file():
        path = source_prefix + '/' + p.relative_to(source_folder).as_posix()
        save(path, p.read_bytes()); source_paths.append(path)
jsave(source_prefix + '/checkpoint.json', dict(
    source_run=38202401393, source_commit='cada56c8a11ff5cbd892ec6d0beaeab60b3e644d',
    all_artifact_payloads_preserved_as_declared=True,
    files=[dict(path=Path(p).relative_to(source_prefix).as_posix(), bytes=(REPO / p).stat().st_size,
                sha256=sha((REPO / p).read_bytes())) for p in source_paths]))
receipts['source-cada56c'] = dict(report_files=106, gates=16, fresh_reports=19, cases=188791, methods=1240, python_tests=259)

for name, expected_hash, count in [
    ('02-control-preflight-failure', '8bd0cdb5e4fcc830455ae0c700b086e1591c6e573ac3419d0f74c3f739bbe63d', 70),
    ('03-control-integration', 'fb85463ed7efa33539fcbe621a21f59cb99004b2bd953f4b6ab8fed2ea21d0f1', 71),
]:
    record = checkpoint(ROOT / 'combined-recovery/checkpoints' / name,
                        'work-in-progress/combined-widget-plugin/' + name, expected_hash)
    assert len(record['files']) == count and record['compiled_mutants'] == record['executed_mutants'] == 0
    assert record['active_source_changed'] is False and record['active_apk_changed'] is False
    receipts['combined-' + name] = dict(files=count, status=record['status'], compiled_mutants=0)

art_source = ROOT / 'widget-art-probe/checkpoints/01-wrapper-review'
art_prefix = 'work-in-progress/widget-art/01-wrapper-review'
art = checkpoint(art_source, art_prefix, 'aa979100f925ba216d1a78dbb9de9c293d5b2e4b771210c2862556bf6946585a')
assert len(art['files']) == 11 and len(art['evidence_files']) == 6051 and art['android_executed'] is False
art_archive = Path(art['evidence_bundle']['path']).read_bytes()
assert len(art_archive) == art['evidence_bundle']['bytes'] == 3304547
assert sha(art_archive) == art['evidence_bundle']['sha256'] == '44b931b66f12be1cf0ee7ae14bbb691573ba5443b86a3410120e4544de736376'
expected = {r['path']: r for r in art['evidence_files']}
seen = set(); compact = []
with tarfile.open(fileobj=io.BytesIO(art_archive), mode='r:gz') as t:
    for member in t.getmembers():
        if member.isdir():
            continue
        assert member.isfile()
        name = safe(member.name)
        assert name in expected and name not in seen
        seen.add(name); data = t.extractfile(member).read()
        assert len(data) == expected[name]['bytes'] and sha(data) == expected[name]['sha256']
        if '/cases/' not in name and not name.endswith('.tar.gz'):
            save(art_prefix + '/evidence/' + name, data); compact.append(name)
assert seen == set(expected)
multipart(art_archive, art_prefix + '/evidence-archive', 'Widget-ART-01-wrapper-review-evidence.tar.gz',
          'widget-art-01-wrapper-review-evidence', 'Complete unchanged host preparation and simulated-ADB evidence; actual Android execution pending')
jsave(art_prefix + '/publication-verification.json', dict(
    frozen_checkpoint_sha256='aa979100f925ba216d1a78dbb9de9c293d5b2e4b771210c2862556bf6946585a',
    declared_source_files_verified=11, exact_archive_members_verified=6051,
    compact_review_files=compact, archive_manifest='evidence-archive/manifest.json',
    all_evidence_bytes_preserved=True, actual_android_execution=False, active_source_or_apk_changed=False))
save(art_prefix + '/PUBLICATION_LAYOUT.md', b'''# Complete immutable preparation evidence

The eleven declared source, package and documentation files and the original checkpoint are copied unchanged. All 6,051 declared evidence files are preserved in the exact archive described by `evidence-archive/manifest.json`; every member size and SHA-256 was independently verified. Compact review files are also available under `evidence/`, with their list in `publication-verification.json`.

The archive retains historical build, audit, race and packaging failures along with the successful preparation. The wrapper's 27 host controls used simulated ADB. No actual Android execution or active app/source promotion is claimed by this checkpoint.

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-art/01-wrapper-review/evidence-archive/manifest.json --verify-only
```

The exact b79 candidate APK is already preserved by `work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json` at commit `5024b1b46056de6a6e76a61883b469521a89ea44`.
''')
receipts['widget-art-wrapper'] = dict(source_files=11, evidence_members=6051, compact_review_files=len(compact), android_executed=False)

editor_policy_prefix = 'docs/verification/editor-observation-policy/01-observed-device-policy'
editor_policy = checkpoint(ROOT / 'editor-observation-forward/checkpoints/01-observed-device-policy',
                           editor_policy_prefix, '4ea8b1e06ce53ecd7c7e11786bf873196805919102a91224fde6a76996fa21f6')
save(editor_policy_prefix + '/PUBLICATION_NOTE.md', b'''# Historical reviewed preparation; activation held for a changed dependency

This capsule preserves the exact reviewed source and 76-test host result. No `active_files` from this capsule were copied to active tool or workflow paths in this publication.

Before activation, remote commit `736da1920f7dada1d0c3444032ffcf4eb8759888` changed the supplied-reference plan from fourteen to sixteen steps by recording and acknowledging the observed Favourite Triggers tip. The frozen favourite-info adapter pins the earlier plan hash and correctly rejects that changed dependency. The observed policy also bounds its accepted plan lengths. The external commit is preserved; compatibility is being reviewed in a separate follow-up checkpoint.

The original host proof remains accurate for its frozen inputs. Actual Android execution of the new policy remains pending, and this historical capsule does not establish runtime parity.
''')
receipts['editor-policy-historical'] = dict(files=len(editor_policy['files']), host_tests=76, active_files_applied=0,
                                           activation_held_for_dependency_commit='736da1920f7dada1d0c3444032ffcf4eb8759888')

baselines = {}
ignore_proc = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
                             input=b'\0'.join(p.encode() for p in sorted(paths)) + b'\0', capture_output=True)
assert ignore_proc.returncode in [0, 1]
ignored = [p.decode() for p in ignore_proc.stdout.split(b'\0') if p]
suffix = '\n# Exact inactive follow-up and hosted evidence files\n' + ''.join('!' + p + '\n' for p in sorted(ignored))
if ignored:
    p = REPO / '.gitignore'; old = p.read_bytes(); baselines['.gitignore'] = sha(old)
    p.write_bytes(old + suffix.encode()); paths.add('.gitignore')
p = REPO / '.gitattributes'; old = p.read_bytes(); baselines['.gitattributes'] = sha(old)
rules = '\n# Exact cada56 hosted artifacts and Widget follow-up reports\n' + '\n'.join([
    'docs/verification/android-ci-cada56c/*.part -text -diff -merge',
    'docs/verification/android-ci-cada56c/tooling-host-tests/*.part -text -diff -merge',
    'work-in-progress/widget-update/06-corrected-message-failure/complete-reports/*.part -text -diff -merge',
    'work-in-progress/widget-update/06-host-runtime-policy/input-snapshot.tar.gz -text -diff -merge',
    'work-in-progress/widget-art/01-wrapper-review/evidence-archive/*.part -text -diff -merge',
]) + '\n'
p.write_bytes(old + rules.encode()); paths.add('.gitattributes')

known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
manifest = []; blobs = []; texts = []
for path in sorted(paths):
    p = REPO / path; data = p.read_bytes()
    row = dict(path=path, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        text = data.decode('utf-8'); binary = '\0' in text
    except UnicodeDecodeError:
        binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blob = row | dict(known=row['git_blob_sha1'] in known)
        if not blob['known']:
            blob['encoding'] = 'base64' if binary or len(data) < 11000000 else 'utf-8'
            if blob['encoding'] == 'utf-8':
                assert data.isascii()
        blobs.append(blob)
    else:
        texts.append(dict(path=path, mode=row['mode'], type='blob', content=text))
chunks = []; chunk = []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk); chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for i, entries in enumerate(chunks):
    (EXPORT / f'text-{i:02d}.json').write_text(json.dumps(entries, ensure_ascii=False))
for name, data in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (EXPORT / name).write_text(json.dumps(data, indent=2) + '\n')
result = dict(files=len(manifest), bytes=sum(r['size_bytes'] for r in manifest), text_chunks=len(chunks), text_entries=len(texts),
              blob_paths=len(blobs), new_blob_paths=sum(not r['known'] for r in blobs),
              new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),
              new_unique_blob_bytes=sum(r['size_bytes'] for r in {r['git_blob_sha1']:r for r in blobs if not r['known']}.values()),
              baselines=baselines, ignored_exact_files_enabled=ignored, receipts=receipts)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
