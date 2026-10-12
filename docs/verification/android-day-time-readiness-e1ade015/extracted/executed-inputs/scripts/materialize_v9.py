#!/usr/bin/env python3
"""Verify the committed v9 snapshot, extract it, then apply the current project overlay."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
import zipfile

from import_v9 import ARCHIVES, ROOT, unpack

REPOSITORY = Path(__file__).resolve().parents[1]
MANIFEST = REPOSITORY / "vendor" / "v9" / "manifest.json"


def checked_path(value: str) -> Path:
    """Only allow regular archive parts inside this repository's v9 snapshot."""
    path = PurePosixPath(value)
    if (path.is_absolute() or ".." in path.parts or "\\" in value
            or path.parts[:2] != ("vendor", "v9")):
        raise ValueError("Invalid archive-part path: " + value)
    target = REPOSITORY.joinpath(*path.parts)
    if target.is_symlink() or not target.resolve().is_relative_to(
            (REPOSITORY / "vendor" / "v9").resolve()):
        raise ValueError("Archive part escapes the snapshot: " + value)
    if not target.is_file():
        raise FileNotFoundError("Missing committed archive part: " + value)
    return target


def verify_archive(archive: dict, output: Path | None) -> None:
    """Check every part and the exact original ZIP byte stream while assembling."""
    identifier = archive["id"]
    expected_filename, expected_sha256 = ARCHIVES[identifier]
    if archive["filename"] != expected_filename or archive["sha256"] != expected_sha256:
        raise ValueError("Manifest does not match the pinned v9 " + identifier + " archive")
    combined = hashlib.sha256()
    total = 0
    stream = output.open("xb") if output is not None else None
    try:
        for part in archive["parts"]:
            path = checked_path(part["path"])
            checksum = hashlib.sha256()
            size = 0
            with path.open("rb") as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    size += len(chunk)
                    checksum.update(chunk)
                    combined.update(chunk)
                    if stream is not None:
                        stream.write(chunk)
            if size != part["size_bytes"] or checksum.hexdigest() != part["sha256"]:
                raise ValueError("Archive-part integrity failure: " + part["path"])
            total += size
        if total != archive["size_bytes"] or combined.hexdigest() != expected_sha256:
            raise ValueError("Combined archive integrity failure: " + identifier)
    finally:
        if stream is not None:
            stream.close()
    print("Verified", identifier, total, "bytes;", len(archive["parts"]), "parts", flush=True)


def apply_overlay(overlay: Path, target: Path) -> int:
    if not overlay.exists():
        return 0
    if not overlay.is_dir() or overlay.is_symlink():
        raise ValueError("The project overlay must be a regular directory")
    count = 0
    for path in sorted(overlay.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symlinks are not allowed in the project overlay: " + str(path))
        if not path.is_file():
            continue
        relative = path.relative_to(overlay)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=REPOSITORY / "workspace",
                        help="Parent of the new MacroDroid_v9 working directory")
    parser.add_argument("--overlay", type=Path, default=REPOSITORY / "project",
                        help="Current source files to copy over the historical snapshot")
    parser.add_argument("--without-overlay", action="store_true",
                        help="Extract the exact historical v9 snapshot only")
    parser.add_argument("--verify-only", action="store_true",
                        help="Check every part and full archive SHA-256 without extracting")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    if (manifest.get("format") != "macrodroid-v9-multipart"
            or manifest.get("format_version") != 1 or manifest.get("archive_root") != ROOT):
        raise ValueError("Unsupported snapshot manifest")
    archives = manifest["archives"]
    if len(archives) != 2 or {entry["id"] for entry in archives} != set(ARCHIVES):
        raise ValueError("Exactly the pinned source and toolchain archives are required")
    if args.verify_only:
        for archive in archives:
            verify_archive(archive, None)
        print("All committed v9 archive bytes match the original delivered ZIPs.")
        return

    destination = args.destination.resolve()
    target = destination / ROOT
    if target.exists() or target.is_symlink():
        raise FileExistsError("Refusing to overwrite an existing workspace: " + str(target)
                              + ". Choose a fresh --destination to preserve local edits.")
    destination.mkdir(parents=True, exist_ok=True)
    # Build in a disposable staging tree. A failed check never publishes a partial workspace.
    with tempfile.TemporaryDirectory(prefix=".materialize-v9-", dir=destination) as temporary:
        staging = Path(temporary)
        for archive in archives:
            assembled = staging / archive["filename"]
            verify_archive(archive, assembled)
            count = unpack(archive["id"], assembled, staging)
            print("Extracted", count, archive["id"], "files", flush=True)
            assembled.unlink()
        overlay_count = 0 if args.without_overlay else apply_overlay(args.overlay, staging / ROOT)
        os.rename(staging / ROOT, target)
    print("Applied", overlay_count, "current project overlay files")
    print("Ready:", target)
    print("Archive integrity is verified. Android runtime parity is a separate acceptance gate.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
