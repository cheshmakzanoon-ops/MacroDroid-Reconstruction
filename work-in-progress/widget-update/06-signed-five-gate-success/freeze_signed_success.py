#!/usr/bin/env python3
"""Freeze the closed Widget five-gate proof and every exact source/report input."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

from prepare_signed_study import BASE_MANIFEST, BASE_PIN, copy_checked, now, record, require, sha, write

FINAL_PIN = "00634710968ddf2fcd7400699ea3c1bb179209ff13e8062d28e64dc098fd7c99"
APK = {"bytes": 94683439, "sha256": "b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f"}
PART_BYTES = 8 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--preparation", required=True, type=Path)
    parser.add_argument("--proof", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    proof = json.loads(args.proof.read_text())
    preparation = json.loads(args.preparation.read_text())
    root = Path(preparation["private_project"])
    require(proof["status"] == "SIGNED_WIDGET_FIVE_GATES_PASSED" and proof["passed"] is True,
            "Expected the closed positive proof")
    labels = ["hybrid-build", "hybrid-code", "hybrid-resources", "three-path-host-tests", "final-input-integrity"]
    require([row["label"] for row in proof["commands"]] == labels
            and all(row["returncode"] == 0 and not row["timed_out"] and row["passed"] for row in proof["commands"]),
            "Five gate outcomes differ")
    require((proof["cases"], proof["registered_methods"], proof["paths"], proof["python_tests"]) == (191133, 1241, 3, 265),
            "Different test inventory")
    require(proof["inputs_verified_before_commands"] is True and proof["inputs_verified_after_commands"] is True,
            "Proof did not verify both input boundaries")
    pin_path = root / "reports/release-input-snapshot.json"
    pin = json.loads(pin_path.read_text())
    require(pin["snapshot_sha256"] == FINAL_PIN and pin["files"] == len(pin["entries"]) == 81266
            and hashlib.sha256(json.dumps(pin["entries"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == FINAL_PIN,
            "Different final input manifest")
    for relative, expected in pin["entries"].items():
        require(record(root / relative) == {"bytes": expected["size"], "sha256": expected["sha256"]},
                "Final input changed before freezing: " + relative)
    baseline_path = args.base / "reports/release-input-snapshot.json"
    require(sha(baseline_path) == BASE_MANIFEST, "Unexpected baseline manifest bytes")
    baseline = json.loads(baseline_path.read_text())
    require(baseline["snapshot_sha256"] == BASE_PIN, "Unexpected baseline pin")
    require(not (baseline["entries"].keys() - pin["entries"].keys()), "Inputs unexpectedly removed")
    for relative, expected in proof["fresh_reports"].items():
        require(record(root / "reports" / relative) == expected, "Closed fresh report changed: " + relative)
    ui = json.loads((root / "reports/java-ui-three-path-parity.json").read_text())
    require(ui["passed"] is True and ui["cases"] == 20818 and ui["methodsCovered"] == 9 and ui["paths"] == 3
            and ui["failedCases"] == ui["unsupportedExecutions"] == ui["expectedResultFailures"] == 0,
            "UI outcome changed")
    require(re.search(r"Ran 265 tests in [\d.]+s\s+OK\s*$", (root / "reports/python-unit-tests.log").read_text()),
            "All 265 Python tests did not pass")
    require(record(root / "dist/MacroDroid-5.67.8-v9-hybrid.apk") == APK, "Signed APK changed")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    files = []

    def add(path, relative):
        files.append({"path": relative, **copy_checked(path, output / relative)})

    add(args.preparation.resolve(), "preparation.json")
    add(args.proof.resolve(), "result.json")
    for row in proof["commands"]:
        path = args.proof.parent / row["log"]["path"]
        require(record(path) == {"bytes": row["log"]["bytes"], "sha256": row["log"]["sha256"]}, "Command log changed")
        add(path, "commands/" + path.name)
    for row in proof["compiled_evidence"]:
        path = args.proof.parent / row["path"]
        require(record(path) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "Compiled evidence changed")
        add(path, "compiled-evidence/" + path.name)
    changed = [relative for relative, expected in pin["entries"].items() if baseline["entries"].get(relative) != expected]
    for relative in changed:
        add(root / relative, "project/" + relative)
    for relative in proof["fresh_reports"]:
        add(root / "reports" / relative, "reviewable/" + relative)
    for name in ("prepare_signed_study.py", "correct_candidate_metadata.py", "install_runtime_policy.py",
                 "run_signed_proof.py", "freeze_signed_success.py"):
        add(Path(__file__).resolve().parent / name, name)

    inventory = []
    archive = output / "complete-reports.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=6) as target:
        for path in sorted((root / "reports").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
                require(not path.is_symlink(), "Report symlink")
                relative = path.relative_to(root / "reports").as_posix()
                expected = record(path)
                inventory.append({"path": relative, **expected})
                target.add(path, arcname=relative, recursive=False)
                require(record(path) == expected, "Report changed while archiving")
    with tarfile.open(archive, "r:gz") as target:
        members = target.getmembers()
        require(len(members) == len(inventory), "Archive inventory differs")
        for member, expected in zip(members, inventory):
            require(member.isfile() and member.name == expected["path"] and member.size == expected["bytes"]
                    and hashlib.sha256(target.extractfile(member).read()).hexdigest() == expected["sha256"],
                    "Archived report bytes differ")
    archive_identity = record(archive)
    parts = []
    joined = hashlib.sha256()
    joined_bytes = 0
    with archive.open("rb") as stream:
        while chunk := stream.read(PART_BYTES):
            name = f"complete-reports.tar.gz.part{len(parts) + 1:02d}"
            path = output / name
            path.write_bytes(chunk)
            actual = record(path)
            require(actual == {"bytes": len(chunk), "sha256": hashlib.sha256(chunk).hexdigest()}, "Archive part differs")
            joined.update(path.read_bytes())
            joined_bytes += actual["bytes"]
            parts.append({"path": name, **actual})
            files.append(parts[-1])
    require({"bytes": joined_bytes, "sha256": joined.hexdigest()} == archive_identity, "Multipart reconstruction differs")
    archive.unlink()
    write(output / "complete-reports-manifest.json", {"filename": "complete-reports.tar.gz", **archive_identity,
                                                      "parts": parts, "files": inventory, "file_count": len(inventory),
                                                      "all_archive_members_verified": True, "parts_join_verified": True})
    files.append({"path": "complete-reports-manifest.json", **record(output / "complete-reports-manifest.json")})
    (output / "README.md").write_text("""# Widget signed candidate: five planned gates passed

The private Widget candidate passes the signed hybrid build, complete code
round trip, resource comparison, three-path host tests and final source integrity
check. All 191,133 cases across 1,241 registered methods and all three execution
paths pass; all 265 Python tests pass. The UI group executes 20,818 cases across
nine methods, including all 194 instructions and 20 conditional edges of Widget
`m`, with no mismatches, unsupported executions or independent-result failures.

The earlier metadata omission and one-message HotSpot failure remain preserved
in their original numbered checkpoints. This run uses the explicitly verified
host exception policy; the application method and its message normalizer have
not been changed to hide those failures. The signed APK is the same 94,683,439
byte `b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`
artifact already retained in `06-initial-signed-failure/apk/manifest.json`.

All 81,266 final input files were independently rehashed before freezing. This
capsule contains every delta input, all five command logs, the actual compiled
helper and signed Widget smali, fresh reviewable results, and every closed report
including the complete input manifest. Join the ordered parts in
`complete-reports-manifest.json` to recover the exact verified report archive.

These five gates are separate from the complete configured acceptance suite and
the actual Android Widget method probe, which remain pending for this isolated
checkpoint. It does not promote the active source or APK, and it does not claim
complete high-level source recovery or whole-application 1:1 parity.
""")
    files.append({"path": "README.md", **record(output / "README.md")})
    checkpoint = {"status": "SIGNED_WIDGET_FIVE_GATES_PASSED", "frozen_utc": now(), "passed": True,
                  "input_snapshot_sha256": FINAL_PIN, "input_manifest": record(pin_path),
                  "input_files_rehashed": 81266, "changed_input_files": len(changed),
                  "cases": 191133, "registered_methods": 1241, "paths": 3, "python_tests": 265,
                  "ui_cases": 20818, "ui_methods": 9, "mismatches": 0, "unsupported_executions": 0,
                  "complete_report_count": len(inventory), "report_archive": archive_identity,
                  "apk": {**APK, "manifest_path": "work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json"},
                  "full_acceptance_executed": False, "android_executed": False,
                  "active_source_changed": False, "active_apk_changed": False, "files": files}
    write(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **record(output / "checkpoint.json"),
                      "files": len(files), "reports": len(inventory), "changed_inputs": len(changed)}, indent=2))


if __name__ == "__main__":
    main()
