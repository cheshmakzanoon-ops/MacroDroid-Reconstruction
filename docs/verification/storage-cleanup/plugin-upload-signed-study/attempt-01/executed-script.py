#!/usr/bin/env python3
"""Retire only the closed upload build after fetched final-proof verification."""
from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import uuid


PROJECT = Path('/tmp/macrodroid-plugin-upload-tynqcwun/MacroDroid_v9')
COMMIT = '075cdcb5b5e7309057acdac63a097ac48dbbd545'
REMOTE_CHECKPOINT = 'work-in-progress/plugin-upload/04-signed-proof/checkpoint.json'
CHECKPOINT_SHA = 'd9c1e3f02e43546b07336ded7099e8bfe0c19a97b56ab5f0b4c6b79b0f8eac48'
ARCHIVE_SHA = '1644a034c9890edb8aeb6b84e928d1032d0153887d59826be1f691445e200295'
APK_SHA = 'e4643b554429743703bed5c1aa5e3541dbfc0705d9fd87c353bd968f348baf80'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    output = args.output.resolve()
    result = {'status': 'CHECKING_CLOSED_UPLOAD_CACHE', 'started_at_utc': now(),
              'project': str(PROJECT), 'proof_commit': COMMIT,
              'proof_checkpoint_sha256': CHECKPOINT_SHA, 'files_deleted': 0,
              'free_bytes_before': shutil.disk_usage(PROJECT).free,
              'scope': 'Only this private build directory; all source, tests, reports, APKs and frozen evidence retained.'}
    retired = None
    try:
        require(PROJECT.resolve() == PROJECT and not PROJECT.is_symlink(), 'Wrong private project identity')
        require(not output.is_relative_to(PROJECT), 'Receipt must be outside the retired project')
        script = Path(__file__).resolve()
        shutil.copyfile(script, output / 'executed-script.py')
        result['script_sha256'] = sha(script)
        fetched = subprocess.run(['git', 'show', COMMIT + ':' + REMOTE_CHECKPOINT],
                                 cwd=args.repository, capture_output=True, check=True, timeout=30)
        (output / 'fetched-checkpoint.json').write_bytes(fetched.stdout)
        (output / 'fetched-checkpoint.stderr.txt').write_bytes(fetched.stderr)
        require(hashlib.sha256(fetched.stdout).hexdigest() == CHECKPOINT_SHA, 'Fetched immutable final proof differs')
        checkpoint = json.loads(fetched.stdout)
        require(checkpoint['status'] == 'SIGNED_THREE_PATH_CODE_RESOURCE_ALL_54_CONTROLS_AND_RESTORATION_PASSED', 'Final proof incomplete')
        require(checkpoint['signed_proof']['passed'] is True and checkpoint['resource_proof']['passed'] is True,
                'Signed/resource gates are not closed passes')
        require(checkpoint['negative_controls']['total_ui_controls'] == 54 and
                checkpoint['positive_restoration']['passed'] is True, 'Full control/restoration proof required')
        archive = Path(checkpoint['evidence_bundle']['path'])
        require(checkpoint['evidence_bundle']['sha256'] == ARCHIVE_SHA and sha(archive) == ARCHIVE_SHA,
                'Exact verified complete evidence archive is unavailable')
        for item in checkpoint['files']:
            require(sha(PROJECT / item['path']) == item['sha256'], 'Frozen candidate source changed: ' + item['path'])
        apk = Path(checkpoint['apk']['path'])
        require(apk == PROJECT / 'dist/MacroDroid-5.67.8-v9-hybrid.apk' and sha(apk) == APK_SHA,
                'Exact retained signed APK changed')
        for item in checkpoint['evidence_files']:
            if item['path'].startswith('generated-ui-controls/'):
                path = PROJECT / 'build/negative-ui' / item['path'].removeprefix('generated-ui-controls/')
                require(path.is_file() and sha(path) == item['sha256'], 'Executed mutant archive binding differs')

        # procfs exposes outer PIDs here, while os.getpid() uses an inner namespace.
        proc_pid = int(Path('/proc/self').resolve().name)
        ancestors, excluded = [], set()
        current = proc_pid
        while current > 0 and current not in excluded:
            excluded.add(current)
            lines = (Path('/proc') / str(current) / 'status').read_text().splitlines()
            parent = int(next(x for x in lines if x.startswith('PPid:')).split()[1])
            ancestors.append({'pid': current, 'parent_pid': parent})
            current = parent
        result['process_identity'] = {'inner_pid': os.getpid(), 'procfs_pid': proc_pid, 'excluded_call_ancestry': ancestors}

        def live_references():
            found = []
            for entry in Path('/proc').iterdir():
                if not entry.name.isdigit() or int(entry.name) in excluded:
                    continue
                try:
                    command = (entry / 'cmdline').read_bytes()
                    cwd = (entry / 'cwd').resolve()
                    reasons = []
                    if cwd == PROJECT or PROJECT in cwd.parents:
                        reasons.append('cwd is inside project')
                    if str(PROJECT).encode() in command:
                        reasons.append('command references project')
                    for fd in (entry / 'fd').iterdir():
                        try:
                            target = fd.resolve()
                            if target == PROJECT / 'build' or PROJECT / 'build' in target.parents:
                                reasons.append('open descriptor references generated build')
                                break
                        except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
                            continue
                    if reasons:
                        found.append({'pid': int(entry.name), 'argv0': command.split(b'\0', 1)[0].decode(errors='replace'),
                                      'cwd': str(cwd), 'reasons': reasons})
                except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
                    continue
            return found

        def retained_inventory():
            rows = []
            for parent, directories, files in os.walk(PROJECT, topdown=True, followlinks=False):
                parent = Path(parent)
                if parent == PROJECT:
                    directories[:] = [d for d in directories if d != 'build' and not d.startswith('.retired-upload-build-')]
                for name in sorted(directories + files):
                    path = parent / name
                    if path.is_symlink():
                        rows.append({'path': path.relative_to(PROJECT).as_posix(), 'kind': 'symlink', 'target': os.readlink(path)})
                    elif path.is_file():
                        rows.append({'path': path.relative_to(PROJECT).as_posix(), 'kind': 'file',
                            'bytes': path.stat().st_size, 'sha256': sha(path), 'mode': stat.S_IMODE(path.stat().st_mode)})
            return sorted(rows, key=lambda x: x['path'])

        references = live_references()
        result['initial_live_references'] = references
        require(not references, 'Retirement blocked: another process references the closed project')
        build = PROJECT / 'build'
        require(build.is_dir() and not build.is_symlink() and build.resolve().parent == PROJECT, 'Unsafe generated build path')
        generated = list(build.rglob('*'))
        require(all(not p.is_symlink() for p in generated), 'Unexpected generated-cache symlink')
        generated_files = [p for p in generated if p.is_file()]
        result['generated_cache'] = {'path': str(build), 'files': len(generated_files),
                                     'bytes': sum(p.stat().st_size for p in generated_files)}
        before = retained_inventory()
        before_bytes = json.dumps(before, sort_keys=True, separators=(',', ':')).encode()
        with gzip.GzipFile(str(output / 'retained-inventory-before.json.gz'), 'wb', mtime=0) as stream:
            stream.write(before_bytes)
        result['retained_inventory_before_sha256'] = hashlib.sha256(before_bytes).hexdigest()
        result['retained_files'] = len(before)
        result['pre_retirement_live_references'] = live_references()
        require(not result['pre_retirement_live_references'], 'A process started using the closed project')
        write(output / 'result.json', result)
        retired = PROJECT / ('.retired-upload-build-' + uuid.uuid4().hex)
        require(not retired.exists(), 'Retirement name already exists')
        build.rename(retired)
        result['retired_generated_path'] = str(retired)
        write(output / 'result.json', result)
        shutil.rmtree(retired)
        require(not retired.exists() and not build.exists(), 'Generated cache survived or reappeared')
        result['files_deleted'] = len(generated_files)
        after = retained_inventory()
        after_bytes = json.dumps(after, sort_keys=True, separators=(',', ':')).encode()
        with gzip.GzipFile(str(output / 'retained-inventory-after.json.gz'), 'wb', mtime=0) as stream:
            stream.write(after_bytes)
        require(before == after, 'A retained source, test, report, APK or tool changed during cache retirement')
        require(sha(apk) == APK_SHA and sha(archive) == ARCHIVE_SHA, 'Retained APK or complete proof archive changed')
        result['final_live_references'] = live_references()
        require(not result['final_live_references'], 'A process started using the retired project')
        result.update(status='CLOSED_UPLOAD_BUILD_RETIRED_ALL_RETAINED_FILES_IDENTICAL',
            retained_inventory_after_sha256=hashlib.sha256(after_bytes).hexdigest(),
            signed_apk_sha256_before_and_after=APK_SHA, complete_proof_archive_sha256_before_and_after=ARCHIVE_SHA,
            all_retained_files_unchanged=True, generated_cache_absent=True)
    except Exception as error:
        result.update(status='RETIREMENT_BLOCKED_OR_FAILED', error=type(error).__name__ + ': ' + str(error),
                      retirement_path_exists=bool(retired and retired.exists()))
        raise
    finally:
        result['finished_at_utc'] = now()
        result['free_bytes_after'] = shutil.disk_usage(PROJECT).free
        write(output / 'result.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
