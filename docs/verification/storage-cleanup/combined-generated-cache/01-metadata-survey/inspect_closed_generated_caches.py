"""Read-only metadata survey of eight explicitly named, closed build caches.

This is not an eligibility or retirement operation. It records every file's
physical identity and size without reading payloads or following symlinks.
Canonical inputs, recovered classes, Java/negative controls, reports and APKs
remain outside any proposed mutation. Later eligibility needs exact byte proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import collections
import gzip
import hashlib
import json
import os
import shutil
import stat

ROOT = Path('/workspace/scratch/4130730d15aa/combined-cache-inventory')
BUILD = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/build')
NAMES = ('baseline', 'hybrid', 'hybrid-smali', 'resources',
         'resource-verify-baseline', 'resource-verify-hybrid',
         'signed-edit-probe', 'assembly-cache')
LIMIT = 500000


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    ROOT.mkdir(exist_ok=True)
    output = ROOT / 'metadata-inventory.jsonl.gz'
    assert not output.exists(), 'Do not replace an earlier observed inventory'
    result = dict(status='READ_ONLY_METADATA_IN_PROGRESS', started_utc=now(),
                  build=str(BUILD), selected_directories=list(NAMES),
                  payloads_read=False, payloads_modified=False,
                  retirement_authorized_by_this_survey=False,
                  exact_duplicate_eligibility_established=False,
                  free_bytes_before=shutil.disk_usage(ROOT).free,
                  source_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    total = 0
    summaries = []
    with output.open('xb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as zipped:
            for name in NAMES:
                base = BUILD / name
                assert base.is_dir() and not base.is_symlink(), str(base)
                counts = collections.Counter()
                extensions = {}
                samples = []
                physical = set()
                stack = [base]
                while stack:
                    directory = stack.pop()
                    with os.scandir(directory) as entries:
                        ordered = sorted(entries, key=lambda entry: entry.name)
                    for entry in ordered:
                        p = Path(entry.path)
                        s = p.lstat()
                        if stat.S_ISDIR(s.st_mode):
                            stack.append(p)
                            counts['directories'] += 1
                            continue
                        assert total < LIMIT, 'Bounded file inventory exceeded'
                        total += 1
                        kind = 'file' if stat.S_ISREG(s.st_mode) else 'symlink' if stat.S_ISLNK(s.st_mode) else 'other'
                        row = dict(path=p.relative_to(BUILD).as_posix(), kind=kind,
                                   bytes=s.st_size, allocated_bytes=s.st_blocks * 512,
                                   device=s.st_dev, inode=s.st_ino, links=s.st_nlink,
                                   mode=s.st_mode & 0o7777, mtime_ns=s.st_mtime_ns,
                                   ctime_ns=s.st_ctime_ns)
                        zipped.write((json.dumps(row, sort_keys=True) + '\n').encode())
                        counts[kind + 's'] += 1
                        if kind == 'file':
                            counts['logical_bytes'] += s.st_size
                            counts['allocated_bytes_per_path'] += s.st_blocks * 512
                            key = (s.st_dev, s.st_ino)
                            if key not in physical:
                                physical.add(key)
                                counts['allocated_bytes_unique_inodes'] += s.st_blocks * 512
                            ext = p.suffix or '(none)'
                            counter = extensions.setdefault(ext, collections.Counter())
                            counter['files'] += 1
                            counter['logical_bytes'] += s.st_size
                            counter['allocated_bytes'] += s.st_blocks * 512
                            if len(samples) < 12:
                                samples.append(dict(path=row['path'], bytes=s.st_size))
                summaries.append(dict(directory=name, counts=dict(counts),
                                      extensions={k: dict(v) for k, v in extensions.items()},
                                      samples=samples))
    result.update(status='READ_ONLY_METADATA_SURVEY_COMPLETE', finished_utc=now(),
                  total_observed_non_directory_paths=total, directories=summaries,
                  inventory=dict(path=output.name, bytes=output.stat().st_size,
                                 sha256=hashlib.sha256(output.read_bytes()).hexdigest()),
                  free_bytes_after=shutil.disk_usage(ROOT).free)
    (ROOT / 'metadata.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'total_observed_non_directory_paths',
                                           'inventory', 'free_bytes_after')}))
    for summary in summaries:
        print(json.dumps(dict(directory=summary['directory'], counts=summary['counts'],
                              extensions=summary['extensions'])))


if __name__ == '__main__':
    main()
