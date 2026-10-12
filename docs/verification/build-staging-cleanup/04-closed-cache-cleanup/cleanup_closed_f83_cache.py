#!/usr/bin/env python3
"""Remove only the closed private f83 build cache after durable proof publication."""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path('/tmp/macrodroid-acceptance-f83e1b-0_znx0sx/MacroDroid_v9')
TARGET = ROOT / 'build'
OUT = BASE / 'staging-cleanup/checkpoints/04-closed-cache-cleanup'
PUBLISHED = 'e1ee954d9bd57b716a3987d92a38fa79d571a280'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def meta(path):
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}


def inventory(root):
    return {path.relative_to(ROOT).as_posix(): meta(path) for path in sorted(root.rglob('*')) if path.is_file()}


def main():
    assert not OUT.exists()
    assert ROOT.resolve() == ROOT and not TARGET.is_symlink()
    assert TARGET.parent == ROOT and TARGET.name == 'build'
    frozen = BASE / 'staging-cleanup/checkpoints/03-full-acceptance'
    assert sha(frozen / 'checkpoint.json') == '2e59dbd22f8f8b0f6fdce477394fb59df078d4d4693ed7b38df77d576796ad85'
    assert sha(BASE / 'staging-cleanup/checkpoints/03-full-acceptance.zip') == '83ca0584390aa8d70b0b15f44ddf4e2c72459e3ab837e2e455fa3e883a1efd52'
    reports_before = inventory(ROOT / 'reports')
    expected_reports = json.loads((frozen / 'reports-manifest.json').read_text())['entries']
    assert reports_before == {entry['path']: {key: entry[key] for key in ['bytes', 'sha256']} for entry in expected_reports}
    apks_before = inventory(ROOT / 'dist')
    markdown_before = {path.name: meta(path) for path in sorted(ROOT.glob('*.md'))}
    result = json.loads((ROOT / 'reports/acceptance-latest.json').read_text())
    assert result['host_acceptance_passed'] is True and result['finished_utc'] == '2026-10-12T03:23:14.787813+00:00'
    ancestors = {os.getpid()}
    pid = os.getpid()
    while pid > 1:
        try:
            line = next(line for line in Path(f'/proc/{pid}/status').read_text().splitlines() if line.startswith('PPid:'))
            pid = int(line.split()[1]); ancestors.add(pid)
        except (OSError, StopIteration):
            break
    active = []
    for process in Path('/proc').iterdir():
        if not process.name.isdigit() or int(process.name) in ancestors:
            continue
        try:
            cwd = (process / 'cwd').resolve()
            arguments = (process / 'cmdline').read_bytes()
            if cwd.is_relative_to(ROOT) or str(ROOT).encode() in arguments:
                active.append({'pid': int(process.name), 'executable': (process / 'comm').read_text().strip(), 'cwd_in_private_checkout': cwd.is_relative_to(ROOT)})
        except (OSError, RuntimeError):
            continue
    assert not active, 'Private checkout still referenced by an active process: ' + str(active)
    cache = {'exists': TARGET.exists(), 'regular_files': 0, 'directories': 0, 'symlinks': 0, 'logical_file_bytes': 0}
    if TARGET.exists():
        assert TARGET.is_dir() and TARGET.resolve().is_relative_to(ROOT)
        for directory, directories, files in os.walk(TARGET, followlinks=False):
            cache['directories'] += 1
            for name in files:
                path = Path(directory) / name
                if path.is_symlink():
                    cache['symlinks'] += 1
                else:
                    cache['regular_files'] += 1
                    cache['logical_file_bytes'] += path.stat().st_size
    OUT.mkdir(parents=True)
    shutil.copyfile(Path(__file__), OUT / Path(__file__).name)
    receipt = {'status': 'CLEANUP_STARTED', 'started_utc': datetime.now(timezone.utc).isoformat(),
               'durable_proof_commit': PUBLISHED,
               'durable_proof_repository_path': 'docs/verification/build-staging-cleanup/03-full-acceptance',
               'durability_confirmation': 'Publishing agent confirmed exact fetched ZIP, all 228 members and review copies before this invocation.',
               'private_checkout': str(ROOT), 'only_deletion_target': str(TARGET),
               'active_private_checkout_processes': active, 'cache_before': cache,
               'free_filesystem_bytes_before': shutil.disk_usage(ROOT).free,
               'reports_before': reports_before, 'dist_before': apks_before, 'markdown_before': markdown_before}
    def save():
        (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    save()
    print('Removing only the closed private f83 build cache', flush=True)
    try:
        if TARGET.exists():
            shutil.rmtree(TARGET)
        assert not TARGET.exists()
        reports_after = inventory(ROOT / 'reports')
        apks_after = inventory(ROOT / 'dist')
        markdown_after = {path.name: meta(path) for path in sorted(ROOT.glob('*.md'))}
        assert reports_before == reports_after and apks_before == apks_after and markdown_before == markdown_after
        # Use the already preserved independent manifest algorithm, without
        # executing any project build/test entry point or importing app code.
        sys.path.insert(0, str(frozen))
        from freeze_full_acceptance import independent_inputs
        print('Rehashing preserved 81,212 source/test/tool/reference inputs', flush=True)
        current = independent_inputs(ROOT)
        expected = json.loads((ROOT / 'reports/release-input-snapshot.json').read_text())
        assert current == expected and current['snapshot_sha256'] == 'f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85'
        receipt.update(status='CLOSED_GENERATED_CACHE_REMOVED_INPUTS_AND_EVIDENCE_PRESERVED',
                       target_absent_after=True, input_files_rehashed=current['files'],
                       input_snapshot_sha256_after=current['snapshot_sha256'], all_input_bytes_match_manifest=True,
                       all_219_report_hashes_unchanged=True, both_dist_apk_hashes_unchanged=True,
                       all_root_markdown_hashes_unchanged=True, other_paths_deleted=[],
                       free_filesystem_bytes_after=shutil.disk_usage(ROOT).free,
                       free_space_note='Filesystem-wide observations may include concurrent unrelated work.',
                       finished_utc=datetime.now(timezone.utc).isoformat())
    except BaseException as error:
        receipt.update(status='CLEANUP_OR_PRESERVATION_CHECK_FAILED', error=type(error).__name__ + ': ' + str(error),
                       target_exists_after=TARGET.exists(), finished_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    save()
    print(json.dumps({key: value for key, value in receipt.items() if key not in ['reports_before', 'dist_before', 'markdown_before']}, indent=2))


if __name__ == '__main__':
    main()
