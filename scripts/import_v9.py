#!/usr/bin/env python3
"""Safely expand the pinned v9 source and toolchain archives to a LOCAL workspace.

This script does not upload anything, install an APK, publish third-party code,
or imply that 1:1 Android parity has been established.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

ARCHIVES = {
    "source": ("MacroDroid_v9_Source.zip", "c11f2d4727a6882943ffccbd81fa45dc738b6fe9c1c5a1c620564e90d8824e01"),
    "toolchain": ("MacroDroid_v9_Toolchain.zip", "ffb8ea58d6f44dc3b70064a58fc36ead75833d2a2bc14690708248e5640de68d"),
}
ROOT = "MacroDroid_v9"

def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_member(member: zipfile.ZipInfo) -> Path:
    path = PurePosixPath(member.filename)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError("Unsafe ZIP path: " + member.filename)
    if not path.parts or path.parts[0] != ROOT:
        raise ValueError("Unexpected archive root: " + member.filename)
    if "\\" in member.filename or ":" in member.filename:
        raise ValueError("Nonportable ZIP path: " + member.filename)
    unix_mode = member.external_attr >> 16
    if stat.S_ISLNK(unix_mode):
        raise ValueError("Symlink member is not allowed: " + member.filename)
    return Path(*path.parts)

def unpack(name: str, file: Path, destination: Path) -> int:
    expected_filename, expected_hash = ARCHIVES[name]
    if file.name != expected_filename:
        print("Note: checking the bytes despite noncanonical filename:", file.name)
    if sha256_file(file) != expected_hash:
        raise ValueError("SHA-256 mismatch: " + str(file))
    n = 0
    with zipfile.ZipFile(file) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP CRC mismatch: " + str(file))
        for member in archive.infolist():
            rel = verify_member(member)
            target = destination / rel
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError("Member escapes output directory: " + member.filename)
            if member.is_dir():
                if target.exists() and not target.is_dir():
                    raise ValueError("Cannot replace file with directory: " + str(target))
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if not target.is_file() or sha256_file(target) != hashlib.sha256(archive.read(member)).hexdigest():
                    raise ValueError("Refusing to overwrite a differing file: " + str(target))
                continue
            temporary = target.with_name(target.name + ".import-partial")
            try:
                with archive.open(member) as src, temporary.open("xb") as dst:
                    while True:
                        chunk = src.read(1024 * 1024)
                        if not chunk:
                            break
                        dst.write(chunk)
                os.replace(temporary, target)
                n += 1
            finally:
                if temporary.exists():
                    temporary.unlink()
    return n

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--toolchain", type=Path, required=True)
    parser.add_argument("--destination", type=Path, default=Path("workspace"))
    args = parser.parse_args()
    dest = args.destination.resolve()
    if dest == Path("/"):
        raise ValueError("Refusing to extract to filesystem root")
    if not args.source.is_file() or not args.toolchain.is_file():
        raise FileNotFoundError("Both v9 archives are required")
    dest.mkdir(parents=True, exist_ok=True)
    for name, file in (("source", args.source), ("toolchain", args.toolchain)):
        print("Verifying and extracting", name, flush=True)
        count = unpack(name, file, dest)
        print("Extracted", count, "new files", flush=True)
    print("Ready locally:", dest / ROOT)
    print("No files were pushed to GitHub. Third-party rights must be respected.")

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
