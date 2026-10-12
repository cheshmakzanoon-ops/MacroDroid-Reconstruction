#!/usr/bin/env python3
"""Reference two exact immutable archive fixtures without copying their payloads."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PINS = {
    'docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip': 'abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e',
    'docs/verification/editor-journey/run-38202401351-attempt-1/evidence.zip': 'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee',
}


def main():
    entries = []
    for relative, expected in PINS.items():
        source = ROOT.parent / 'MacroDroid-Reconstruction' / relative
        data = source.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected
        target = ROOT / 'worktree' / relative
        assert not target.exists() and not target.is_symlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)
        assert target.resolve() == source.resolve()
        assert hashlib.sha256(target.read_bytes()).hexdigest() == expected
        entries.append({'repository_path': relative, 'bytes': len(data), 'sha256': expected,
                        'method': 'read-only test use through a local symlink; archive bytes unchanged'})
    report = {'schema': 1, 'fixture_archives': entries, 'copied_archive_payload_bytes': 0,
              'source_files_modified': False, 'active_repository_modified': False}
    (ROOT / 'fixture-references.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
