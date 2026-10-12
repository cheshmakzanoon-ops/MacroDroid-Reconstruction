#!/usr/bin/env python3
"""Retire only a closed Widget generated cache after its proof is durable."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from prepare_signed_study import now, record, require, write

CHECKPOINT = "51091cf5f03ff60306fccbbb1b8f612c582aa2de489a42bed73a91676662656e"
COMMIT = "a17e119f90418fb642aea4777c0f920bbf9fb92c"
REMOTE_PATH = "work-in-progress/widget-update/06-signed-five-gate-success/checkpoint.json"
PIN = "00634710968ddf2fcd7400699ea3c1bb179209ff13e8062d28e64dc098fd7c99"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    require(root == Path("/tmp/macrodroid-widget-signed-eti67161/MacroDroid_v9"), "Wrong closed project")
    require(not args.output.exists(), "Retirement receipt already exists")
    remote = subprocess.run(["git", "show", COMMIT + ":" + REMOTE_PATH], cwd=args.repository, capture_output=True, check=True).stdout
    require(hashlib.sha256(remote).hexdigest() == CHECKPOINT, "Durable fetched proof differs")
    checkpoint = json.loads(remote)
    require(checkpoint["passed"] is True and checkpoint["input_snapshot_sha256"] == PIN, "Wrong durable proof state")
    pin = json.loads((root / "reports/release-input-snapshot.json").read_text())
    require(pin["snapshot_sha256"] == PIN, "Closed source pin changed")

    def preserved():
        rows = {}
        for relative, expected in pin["entries"].items():
            actual = record(root / relative)
            require(actual == {"bytes": expected["size"], "sha256": expected["sha256"]}, "Preserved source input differs: " + relative)
            rows[relative] = actual
        for folder in (root / "reports", root / "dist"):
            for path in sorted(folder.rglob("*")):
                if path.is_file():
                    require(not path.is_symlink(), "Unexpected evidence symlink")
                    rows[path.relative_to(root).as_posix()] = record(path)
        for path in sorted(root.glob("*.md")):
            rows[path.name] = record(path)
        return rows

    def live_references():
        found = []
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit() or int(entry.name) in {os.getpid(), os.getppid()}:
                continue
            try:
                command = (entry / "cmdline").read_bytes()
                cwd = (entry / "cwd").resolve()
                if cwd == root or root in cwd.parents or (str(root).encode() in command and command.split(b"\0", 1)[0].split(b"/")[-1] in {b"java", b"javac", b"python3", b"python"}):
                    status = (entry / "status").read_text().splitlines()
                    parent = int(next(line for line in status if line.startswith("PPid:")).split()[1])
                    found.append({"pid": int(entry.name), "parent_pid": parent,
                                  "comm": (entry / "comm").read_text().strip(), "cwd": str(cwd),
                                  "argv0": command.split(b"\0", 1)[0].decode(errors="replace"),
                                  "cwd_inside_project": cwd == root or root in cwd.parents,
                                  "command_references_project": str(root).encode() in command})
            except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
                continue
        return found

    references = live_references()
    if references:
        ancestors = []
        current = os.getpid()
        while current > 0:
            status = (Path("/proc") / str(current) / "status").read_text().splitlines()
            parent = int(next(line for line in status if line.startswith("PPid:")).split()[1])
            ancestors.append({"pid": current, "parent_pid": parent})
            current = parent
        write(args.output, {"status": "RETIREMENT_BLOCKED_BY_LIVE_PROCESS_GUARD", "files_deleted": 0,
                            "observed_utc": now(), "references": references, "own_ancestry": ancestors})
    require(not references, "The closed project still has a running process")
    result = {"status": "CHECKING_CLOSED_GENERATED_CACHE", "started_utc": now(), "project": str(root),
              "proof_commit": COMMIT, "proof_checkpoint_sha256": CHECKPOINT, "input_snapshot_sha256": PIN,
              "active_process_references": references, "free_bytes_before": shutil.disk_usage(root).free}
    before = preserved()
    write(args.output, result)
    removed = []
    for path in (root / "build", root / "tools/classes"):
        require(path.is_dir() and not path.is_symlink() and root in path.resolve().parents, "Unsafe generated cache path")
        files = [p for p in path.rglob("*") if p.is_file()]
        require(all(not p.is_symlink() for p in path.rglob("*")), "Generated cache contains a symlink")
        row = {"path": str(path), "files": len(files), "bytes": sum(p.stat().st_size for p in files)}
        require(not live_references(), "A process started using the closed project")
        shutil.rmtree(path)
        require(not path.exists(), "Generated cache remains")
        removed.append(row)
    after = preserved()
    require(before == after, "Source, reports, signed APK or documentation changed during retirement")
    require(not live_references(), "A process started using the retired project")
    result.update(status="CLOSED_GENERATED_CACHE_RETIRED_PRESERVED_INPUTS_UNCHANGED", completed_utc=now(),
                  removed=removed, preserved_files=len(before),
                  preserved_inventory_sha256=hashlib.sha256(json.dumps(before, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                  source_files_verified_before_and_after=pin["files"], source_reports_apk_docs_unchanged=True,
                  free_bytes_after=shutil.disk_usage(root).free,
                  scope="Only regenerated build and tools/classes outputs removed; all source, reports, APKs and frozen proof remain")
    write(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
