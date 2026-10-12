#!/usr/bin/env python3
"""Preserve the initial signed Widget result and its exact metadata failure."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

from prepare_signed_study import copy_checked, now, record, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preparation = json.loads(args.preparation.read_text())
    proof = json.loads(args.proof.read_text())
    root = Path(preparation["private_project"])
    require(proof["status"] == "SIGNED_WIDGET_PROOF_FAILED" and proof["passed"] is False, "Expected the closed initial failure")
    require([(step["label"], step["returncode"]) for step in proof["commands"]] == [
        ("hybrid-build", 0), ("hybrid-code", 0), ("hybrid-resources", 0), ("three-path-host-tests", 1)], "Unexpected closed gate sequence")
    unit = (root / "reports/python-unit-tests.log").read_text()
    failures = re.findall(r"^FAIL: (\w+) ", unit, re.M)
    require(sorted(failures) == ["test_fixture_provenance", "test_registered_classes_count", "test_registry_count"], "Unit failure is different from the reviewed omission")
    require(re.search(r"Ran 259 tests in [\d.]+s\s+FAILED \(failures=3\)\s*$", unit), "Missing exact failed unit summary")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    prefix = "work-in-progress/widget-update/06-initial-signed-failure"
    files = []

    def add(path, relative):
        value = copy_checked(path, output / relative)
        files.append({"path": relative, **value})

    def multipart(path, directory, name, identifier, media_type, purpose):
        directory = output / directory
        directory.mkdir(parents=True, exist_ok=False)
        parts = []
        combined = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            number = 0
            while block := stream.read(8 * 1024 * 1024):
                number += 1
                part = directory / ("part-%04d.bin" % number)
                part.write_bytes(block)
                value = record(part)
                combined.update(block)
                size += len(block)
                relative = part.relative_to(output).as_posix()
                parts.append({"path": prefix + "/" + relative, "size_bytes": len(block), "sha256": value["sha256"]})
                files.append({"path": relative, **value})
        require(size == path.stat().st_size and combined.hexdigest() == sha(path), "Multipart source identity changed")
        manifest = {"format": "macrodroid-multipart-artifact", "format_version": 1, "id": identifier,
                    "filename": name, "media_type": media_type, "purpose": purpose,
                    "size_bytes": size, "sha256": combined.hexdigest(), "parts": parts}
        if media_type == "application/vnd.android.package-archive":
            manifest.update(recovered_method_bodies=1241, recovered_classes=604, full_functional_parity_established=False,
                            source_input_snapshot_sha256=preparation["candidate_inputs"]["snapshot_sha256"],
                            validation_at_publication={"hybrid_build": "passed", "full_code_comparison": "passed", "resources": "passed", "host_suite": "blocked by 3 exact registry/fixture metadata unit failures"})
        path = directory / "manifest.json"
        write(path, manifest)
        files.append({"path": path.relative_to(output).as_posix(), **record(path)})
        return manifest

    add(args.preparation.resolve(), "preparation.json")
    add(args.proof.resolve(), "result.json")
    for command in proof["commands"]:
        path = args.proof.parent / command["log"]["path"]
        require(record(path) == {"bytes": command["log"]["bytes"], "sha256": command["log"]["sha256"]}, "Closed outer command log differs")
        add(path, "commands/" + path.name)
    add(args.preparation.parent / "metadata-omission-review.json", "metadata-omission-review.json")
    for name in ["hybrid-build.json", "hybrid-roundtrip.json", "hybrid-resource-parity.json", "java-integration.json", "python-unit-tests.log"]:
        add(root / "reports" / name, "reviewable/" + name)
    for name in ["tests/test_build.py", "tests/fixtures/provenance.json"]:
        add(root / name, "initial-inputs/" + name)
    add(Path(__file__).resolve(), "freeze_initial_signed_failure.py")
    archive = output.parent / "06-initial-signed-failure-reports.tar.gz"
    require(not archive.exists(), "Complete reports archive already exists")
    inventory = []
    with tarfile.open(archive, "w:gz", compresslevel=6) as target:
        for path in sorted((root / "reports").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in (".pyc", ".pyo"):
                require(not path.is_symlink(), "Unexpected report symlink")
                relative = path.relative_to(root / "reports").as_posix()
                inventory.append({"path": relative, **record(path)})
                target.add(path, arcname=relative, recursive=False)
    with tarfile.open(archive, "r:gz") as target:
        require(len(target.getmembers()) == len(inventory), "Archive file inventory differs")
        for item, entry in zip(target.getmembers(), inventory):
            require(item.isfile() and item.name == entry["path"] and item.size == entry["bytes"], "Archive member schema differs")
            require(hashlib.sha256(target.extractfile(item).read()).hexdigest() == entry["sha256"], "Archive member bytes differ")
    archive_manifest = multipart(archive, "complete-reports", "Widget-06-initial-signed-failure-reports.tar.gz", "widget-06-initial-signed-failure-reports", "application/gzip", "Complete closed reports, including correctly failed metadata checks")
    write(output / "complete-reports-inventory.json", {"files": inventory, "file_count": len(inventory), "archive_bytes": archive_manifest["size_bytes"], "archive_sha256": archive_manifest["sha256"]})
    files.append({"path": "complete-reports-inventory.json", **record(output / "complete-reports-inventory.json")})
    apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    apk_manifest = multipart(apk, "apk", "MacroDroid-5.67.8-widget-update-06.apk", "widget-update-06-hybrid", "application/vnd.android.package-archive", "Inactive initial Widget candidate; full code/resources pass but host acceptance failed on registry and fixture metadata")
    readme = """# Initial signed Widget study: metadata failure preserved

The actual hybrid assembly, complete bytecode round trip and resource comparison
passed. The host stage then ran all 259 Python tests and correctly failed exactly
three: the common method count still expected 1,240, the class count still expected
603, and the original-fixture provenance still named the preceding fixture hash.
The candidate actually contains 1,241 bodies in 604 classes and a freshly extracted
full original-method fixture. The implementation and D8/static/linkage prerequisites
retain their independently recorded results; no three-path host pass is claimed.

This checkpoint preserves every closed report, all four outer gate logs, the
initial omitted metadata/test inputs, the exact signed APK and each archive/part
hash. The APK is 94,683,439 bytes, SHA-256
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`.
The source pin is `a729f01fc4b0dc136c980501c144b43769332c324f8c6f63438107d605291691`.
The original extraction, 30 source/test changes and exact D8 prerequisites are
retained in the adjacent immutable `06-d8-prerequisites` checkpoint.

A numbered follow-up corrects only the two omitted metadata/test files, records a
new input pin and reruns the full signed study. This failed result is never changed
into a passing result. The method remains inactive in the published application.
"""
    (output / "README.md").write_text(readme)
    files.append({"path": "README.md", **record(output / "README.md")})
    checkpoint = {"status": "SIGNED_BUILD_CODE_RESOURCES_PASSED_HOST_METADATA_GATE_FAILED", "frozen_utc": now(),
                  "source_input_snapshot_sha256": preparation["candidate_inputs"]["snapshot_sha256"],
                  "source_prerequisite_checkpoint_sha256": "2c5557427602bac7d3154d17f127499e8f785cd9f5a0dd73c299d3e6854f938b",
                  "gate_results": [{"label": item["label"], "returncode": item["returncode"]} for item in proof["commands"]],
                  "python_tests": 259, "python_failures": failures, "apk_sha256": apk_manifest["sha256"],
                  "complete_report_count": len(inventory), "files": files}
    write(output / "checkpoint.json", checkpoint)
    for entry in files:
        require(record(output / entry["path"]) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}, "Frozen file differs")
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **record(output / "checkpoint.json"), "files": len(files), "reports": len(inventory)}, indent=2))


if __name__ == "__main__":
    main()
