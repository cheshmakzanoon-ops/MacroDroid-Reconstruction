#!/usr/bin/env python3
"""Preserve a frozen integration checkpoint using bounded multipart report storage."""
from __future__ import annotations
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--assembler", type=Path, required=True)
    args = parser.parse_args()
    source, dest = args.source.resolve(), args.destination.resolve()
    initial = json.loads((source / "checkpoint.json").read_text())
    assert sha(source / "checkpoint.json") == "e10642cbcc78fb0452f755b18d1b783d4c2554e2c995f664cd77e25c489f6494"
    dest.mkdir(parents=True, exist_ok=False)
    evidence = Path("docs/verification/plugin-runtime-integration")
    archived = evidence / "complete-combined-reports.tar.gz"
    baseline = {}
    for record in initial["files"]:
        path = source / record["path"]
        assert path.stat().st_size == record["bytes"] and sha(path) == record["sha256"]
        baseline[record["path"]] = record["baseline_sha256"]
        if record["path"] == str(archived):
            continue
        target = dest / record["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    parts = []
    whole = hashlib.sha256()
    with (source / archived).open("rb") as handle:
        while data := handle.read(8 * 1024 * 1024):
            relative = evidence / "complete-combined-reports.parts" / f"reports.{len(parts) + 1:04d}.part"
            target = dest / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            whole.update(data)
            parts.append({"path": str(relative), "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "git_blob_sha1": hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()})
    assert whole.hexdigest() == initial["combined_report_archive"]["archive_sha256"]
    manifest = {
        "format": "macrodroid-multipart-artifact", "format_version": 1,
        "id": "plugin-runtime-complete-combined-reports", "filename": archived.name,
        "media_type": "application/gzip", "purpose": "Exact closed five-command combined report archive; all69 members retained without alteration",
        "size_bytes": (source / archived).stat().st_size, "sha256": whole.hexdigest(), "parts": parts,
        "member_inventory": str(evidence / "complete-combined-reports-inventory.json"),
    }
    manifest_path = dest / evidence / "complete-combined-reports-manifest.json"
    save(manifest_path, manifest)
    shutil.copyfile(source / "checkpoint.json", dest / evidence / "integration/initial-freeze-checkpoint.json")
    shutil.copyfile(Path(__file__).resolve(), dest / evidence / "pack_publication.py")

    spec = importlib.util.spec_from_file_location("verify_frozen_report_assembler", args.assembler)
    assembler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(assembler)
    assembler.REPOSITORY = dest
    original_argv = sys.argv
    output = io.StringIO()
    try:
        sys.argv = [str(args.assembler), str(manifest_path), "--verify-only"]
        with contextlib.redirect_stdout(output):
            assembler.main()
    finally:
        sys.argv = original_argv
    (dest / evidence / "report-assembly-verification.log").write_text(output.getvalue())
    readme = dest / evidence / "README.md"
    text = readme.read_text()
    text = text.replace(
        "`complete-combined-reports.tar.gz` contains every closed report and command log, including the exact input snapshot.",
        "`complete-combined-reports.tar.gz` contains every closed report and command log, including the exact input snapshot. Its unchanged compressed bytes are committed as two bounded binary parts. Assemble or verify them from the repository root:\n\n```sh\npython3 scripts/assemble_artifact.py docs/verification/plugin-runtime-integration/complete-combined-reports-manifest.json\npython3 scripts/assemble_artifact.py docs/verification/plugin-runtime-integration/complete-combined-reports-manifest.json --verify-only\n```\n\nThe assembled file is placed under `workspace/artifacts/` by default.")
    text = text.replace("The exact canonical value is also machine-readable in `checkpoint.json` and the active `project/reports/release-input-snapshot.json`; use those checked values for automation.", "The same value is machine-readable in `checkpoint.json` and the active `project/reports/release-input-snapshot.json`.")
    readme.write_text(text)
    transfer = dest / "docs/TRANSFER_STATUS.md"
    text = transfer.read_text().replace("proof and active integration remain pending.", "proof and active integration were still pending at that historical freeze.")
    text = text.replace("The candidate manifest binds the new APK bytes to that input snapshot", "The candidate manifest at that historical commit binds its APK bytes to that input snapshot", 1)
    transfer.write_text(text)
    initial_sha = sha(source / "checkpoint.json")
    checkpoint = {k: v for k, v in initial.items() if k != "files"}
    checkpoint["checkpoint"] = "plugin-runtime-integration-02-publication"
    checkpoint["publication_packed_utc"] = datetime.now(timezone.utc).isoformat()
    checkpoint["initial_freeze_sha256"] = initial_sha
    checkpoint["publication_changes"] = "Exact report archive split into two parts; assembler verification and initial manifest preserved; scope documentation clarified; no build/test input or measured report changed"
    checkpoint["combined_report_archive"]["multipart_manifest"] = str(evidence / "complete-combined-reports-manifest.json")
    checkpoint["files"] = [
        {"path": str(path.relative_to(dest)), "bytes": path.stat().st_size, "sha256": sha(path), "baseline_sha256": baseline.get(str(path.relative_to(dest)))}
        for path in sorted(dest.rglob("*")) if path.is_file()
    ]
    save(dest / "checkpoint.json", checkpoint)
    save(dest / evidence / "checkpoint.json", checkpoint)
    assert sha(dest / "project/reports/release-input-snapshot.json") == initial["source_manifest_file_sha256"]
    print(json.dumps({"checkpoint": str(dest / "checkpoint.json"), "sha256": sha(dest / "checkpoint.json"), "files": len(checkpoint["files"]), "bytes": sum(f["bytes"] for f in checkpoint["files"]), "parts": parts, "source_manifest_sha256": initial["source_manifest_file_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
