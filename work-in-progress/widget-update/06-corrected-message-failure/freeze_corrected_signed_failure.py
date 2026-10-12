#!/usr/bin/env python3
"""Preserve the corrected inventory and actual one-message three-way failure."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

from prepare_signed_study import BASE_PIN, copy_checked, now, record, require, sha, write


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
    require(proof["status"] == "SIGNED_WIDGET_PROOF_FAILED" and proof["passed"] is False,
            "Expected the closed corrected failure")
    require([(row["label"], row["returncode"]) for row in proof["commands"]] == [
        ("hybrid-build", 0), ("hybrid-code", 0), ("hybrid-resources", 0), ("three-path-host-tests", 1)],
        "Different gate outcome")
    ui = json.loads((root / "reports/java-ui-three-path-parity.json").read_text())
    require(ui["passed"] is False and ui["cases"] == 20818 and ui["methodsCovered"] == 9
            and ui["failedCases"] == 1 and ui["unsupportedExecutions"] == ui["expectedResultFailures"] == 0
            and ui["failedCaseLabels"] == ["widget-saved-cast:1:3:false"] and ui["paths"] == 3,
            "UI failure differs from the reviewed message-only result")
    unit = (root / "reports/python-unit-tests.log").read_text()
    require(re.search(r"Ran 259 tests in [\d.]+s\s+OK\s*$", unit), "Expected all 259 Python tests to pass")
    pin = json.loads((root / "reports/release-input-snapshot.json").read_text())
    require(pin["snapshot_sha256"] == "46c68873d3ff573da2d6676507b2dd6e82e7077c9ed7bcac422e45b0939a8659"
            and pin["files"] == len(pin["entries"]) == 81264, "Wrong corrected input inventory")
    for relative, expected in pin["entries"].items():
        require(record(root / relative) == {"bytes": expected["size"], "sha256": expected["sha256"]},
                "Corrected input changed before freezing: " + relative)
    baseline = json.loads((args.base / "reports/release-input-snapshot.json").read_text())
    require(baseline["snapshot_sha256"] == BASE_PIN, "Wrong baseline for source delta")
    apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    require(record(apk) == {"bytes": 94683439, "sha256": "b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f"},
            "Candidate APK changed")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    files = []

    def add(source, relative):
        files.append({"path": relative, **copy_checked(source, output / relative)})

    add(args.preparation.resolve(), "preparation.json")
    add(args.proof.resolve(), "result.json")
    for row in proof["commands"]:
        log = args.proof.parent / row["log"]["path"]
        require(record(log) == {"bytes": row["log"]["bytes"], "sha256": row["log"]["sha256"]}, "Closed command log changed")
        add(log, "commands/" + log.name)
    for source in sorted(args.preparation.parent.rglob("*")):
        if source.is_file():
            add(source, "metadata-correction/" + source.relative_to(args.preparation.parent).as_posix())
    changed = [relative for relative, value in pin["entries"].items() if baseline["entries"].get(relative) != value]
    require(len(changed) == 32 and not (baseline["entries"].keys() - pin["entries"].keys()), "Unexpected corrected delta")
    for relative in changed:
        add(root / relative, "project/" + relative)
    add(root / "reports/release-input-snapshot.json", "project/reports/release-input-snapshot.json")
    for name in ("java-ui-three-path-parity.json", "python-unit-tests.log", "hybrid-roundtrip.json",
                 "hybrid-resource-parity.json", "migration-static-proof.json", "migration-linkage-check.json"):
        add(root / "reports" / name, "reviewable/" + name)
    for name in ("prepare_signed_study.py", "run_signed_proof.py", "correct_candidate_metadata.py",
                 "freeze_corrected_signed_failure.py"):
        add(Path(__file__).resolve().parent / name, name)

    inventory = []
    archive = output / "complete-reports.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=6) as target:
        for path in sorted((root / "reports").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in (".pyc", ".pyo"):
                require(not path.is_symlink(), "Unexpected report symlink")
                relative = path.relative_to(root / "reports").as_posix()
                inventory.append({"path": relative, **record(path)})
                target.add(path, arcname=relative, recursive=False)
    with tarfile.open(archive, "r:gz") as target:
        require(len(target.getmembers()) == len(inventory), "Report archive inventory differs")
        for member, expected in zip(target.getmembers(), inventory):
            require(member.isfile() and member.name == expected["path"] and member.size == expected["bytes"]
                    and hashlib.sha256(target.extractfile(member).read()).hexdigest() == expected["sha256"],
                    "Report archive bytes differ")
    files.append({"path": archive.name, **record(archive)})
    write(output / "complete-reports-inventory.json", {"files": inventory, "file_count": len(inventory),
                                                     "archive": record(archive), "all_archive_members_verified": True})
    files.append({"path": "complete-reports-inventory.json", **record(output / "complete-reports-inventory.json")})
    (output / "README.md").write_text("""# Corrected Widget inventory: one-message host failure preserved

The metadata correction changes only the two omitted count/provenance inputs.
All 259 Python tests now pass. The hybrid build, complete code round trip and
resource comparison pass again with the identical signed APK (`b79b0010…`).
That APK is retained in the adjacent `06-initial-signed-failure/apk/` multipart
artifact; this checkpoint does not create another APK copy or promote it.

The actual three-way UI run executes 20,818 cases across nine methods and finds
exactly one mismatch, `widget-saved-cast:1:3:false`. All Widget instructions and
conditional edges are visited, with zero unsupported executions or independent
expected-result failures. The original and rebuilt DEX paths produce a literal
null exception-message log; the direct Java path produces the helpful JVM null
receiver text already handled by the narrowly scoped normalizer. Their remaining
observations are identical. The complete failed JSON is retained unchanged.

The default JDK fast-throw optimization is a candidate explanation, to be tested
in a separate unchanged-classpath experiment. This checkpoint does not expand
message normalization, assert a passing three-way result, or claim Android parity.
All 81,264 corrected input files were rehashed before freezing. The 32 exact
delta inputs, complete input manifest, corrected scripts, every closed report,
all command logs, and metadata-correction history are preserved with hashes.
""")
    files.append({"path": "README.md", **record(output / "README.md")})
    checkpoint = {"status": "CORRECTED_METADATA_PASSED_ONE_VM_MESSAGE_UI_MISMATCH_PRESERVED",
                  "frozen_utc": now(), "input_snapshot_sha256": pin["snapshot_sha256"], "input_files_rehashed": pin["files"],
                  "changed_input_files": len(changed), "python_tests_passed": 259,
                  "ui_cases": ui["cases"], "ui_failed_cases": 1, "unsupported_executions": 0,
                  "expected_result_failures": 0, "method_instruction_and_branch_coverage": True,
                  "apk": {**record(apk), "manifest_path": "work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json"},
                  "active_source_changed": False, "active_apk_changed": False,
                  "three_path_passed": False, "android_executed": False,
                  "complete_report_count": len(inventory), "files": files}
    write(output / "checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), **record(output / "checkpoint.json"),
                      "files": len(files), "reports": len(inventory)}, indent=2))


if __name__ == "__main__":
    main()
