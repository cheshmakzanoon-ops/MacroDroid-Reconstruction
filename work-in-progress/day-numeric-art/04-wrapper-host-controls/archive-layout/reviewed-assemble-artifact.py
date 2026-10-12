#!/usr/bin/env python3
"""Reassemble a checksum-pinned repository artifact without changing its bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def part_path(name: str) -> Path:
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or "\\" in name:
        raise ValueError("Invalid artifact-part path: " + name)
    path = REPOSITORY.joinpath(*relative.parts)
    if path.is_symlink() or not path.resolve().is_relative_to(REPOSITORY):
        raise ValueError("Artifact part escapes the repository: " + name)
    if not path.is_file():
        raise FileNotFoundError("Missing committed artifact part: " + name)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Pinned multipart artifact manifest")
    parser.add_argument("--output", type=Path,
                        help="Output file; defaults to workspace/artifacts/<filename>")
    parser.add_argument("--verify-only", action="store_true",
                        help="Verify all bytes without creating an output file")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if (manifest.get("format") != "macrodroid-multipart-artifact"
            or manifest.get("format_version") != 1):
        raise ValueError("Unsupported multipart artifact manifest")
    filename = manifest["filename"]
    if not filename or PurePosixPath(filename).name != filename or "\\" in filename:
        raise ValueError("Artifact filename must be a plain basename")
    parts = manifest["parts"]
    if not parts or len({part["path"] for part in parts}) != len(parts):
        raise ValueError("Artifact parts must be nonempty and unique")
    output = args.output or REPOSITORY / "workspace" / "artifacts" / filename
    existing = output.exists() or output.is_symlink()
    if not args.verify_only and existing:
        if (output.is_symlink() or not output.is_file()
                or output.stat().st_size != manifest["size_bytes"]
                or digest(output) != manifest["sha256"]):
            raise FileExistsError("Refusing to replace a differing output: " + str(output))

    temporary = None
    destination = None
    combined = hashlib.sha256()
    total = 0
    try:
        if not args.verify_only and not existing:
            output.parent.mkdir(parents=True, exist_ok=True)
            destination = tempfile.NamedTemporaryFile(prefix=".artifact-", dir=output.parent,
                                                       delete=False)
            temporary = Path(destination.name)
        for part in parts:
            checksum = hashlib.sha256()
            size = 0
            with part_path(part["path"]).open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    checksum.update(block)
                    combined.update(block)
                    size += len(block)
                    if destination is not None:
                        destination.write(block)
            if size != part["size_bytes"] or checksum.hexdigest() != part["sha256"]:
                raise ValueError("Artifact-part integrity failure: " + part["path"])
            total += size
        if total != manifest["size_bytes"] or combined.hexdigest() != manifest["sha256"]:
            raise ValueError("Combined artifact integrity failure")
        if destination is not None:
            destination.close()
            destination = None
            if output.exists() or output.is_symlink():
                raise FileExistsError("Output appeared during assembly: " + str(output))
            os.rename(temporary, output)
            temporary = None
    finally:
        if destination is not None:
            destination.close()
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print("Verified", filename, total, "bytes;", len(parts), "parts")
    print("SHA-256:", combined.hexdigest())
    if not args.verify_only:
        print("Ready:", output)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
