#!/usr/bin/env python3
"""Freeze the measured 24-control method-only Widget evidence without active edits."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import tarfile


ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, target):
    digest = sha(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha(target) != digest or source.stat().st_ino == target.stat().st_ino:
        raise RuntimeError("Copy mismatch or hardlink: " + str(source))


def inventory(root):
    return [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)}
            for p in sorted(root.rglob("*")) if p.is_file()]


def main():
    measured = ROOT / "reports/widget-method-mutants-04-initial"
    result = json.loads((measured / "result.json").read_text())
    if not (result["passed"] and result["controls_count"] == 24 and result["controls_detected"] == 24
            and result["positive_before"]["passed"] and result["positive_restoration"]["passed"]
            and all(row["passed"] for row in result["class_origin_controls"])):
        raise RuntimeError("Mutant/control/restoration gate did not pass")
    for control in result["controls"]:
        parity = json.loads((measured / "controls" / control["name"] / "parity.json").read_text())
        if parity["independentExpectedResultChecks"] != 198:
            raise RuntimeError("Original independent expectation count changed")
    output = ROOT / "checkpoints/04-method-mutants"
    output.mkdir(parents=True, exist_ok=False)
    files = []
    for name in ("widget_method_negative_control.py", "widget_method_mutants.json",
                 "tests/java/WidgetMutationLauncher.java", "WIDGET_MUTANTS.md",
                 "freeze_widget_method_mutants_checkpoint.py"):
        copy(ROOT / name, output / name)
        files.append({"path": name, "bytes": (output / name).stat().st_size, "sha256": sha(output / name)})
    for row in result["authored_inputs"]:
        if sha(output / row["path"]) != row["sha256"]:
            raise RuntimeError("Executed source and checkpoint disagree")
    for source in sorted(measured.rglob("*")):
        if source.is_file():
            copy(source, output / "evidence/run" / source.relative_to(measured))
    positive = ROOT / "checkpoints/04-original-jvm"
    copy(positive / "checkpoint.json", output / "evidence/positive-checkpoint.json")
    copy(positive / "WIDGET_HARNESS.md", output / "evidence/positive-scope.md")
    copy(positive / "tests/fixtures/widget-provenance.json", output / "evidence/original-fixture-provenance.json")
    evidence = inventory(output / "evidence")
    archive = ROOT / "checkpoints/04-method-mutants-evidence.tar.gz"
    if archive.exists():
        raise RuntimeError("Evidence archive already exists")
    with tarfile.open(archive, "w:gz") as stream:
        for row in evidence:
            stream.add(output / "evidence" / row["path"], arcname=row["path"], recursive=False)
    remaining = {row["path"]: row for row in evidence}
    with tarfile.open(archive, "r:gz") as stream:
        for member in stream.getmembers():
            row = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError("Archive member mismatch: " + member.name)
    if remaining:
        raise RuntimeError("Missing archive members")
    checkpoint = {
        "status": result["status"], "frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Inactive Widget method-only compiled negative controls. Fixed original/JVM paths; no active registry/APK or rebuilt/Android claim.",
        "method": result["method"], "controls": 24, "class_origin_controls": 2,
        "cases_per_execution": 2342, "expected_checks_per_execution": 198, "paths": 2,
        "coverage_per_execution": {"instructions": 194, "visited": 194, "conditional_edges": 20, "visited_edges": 20},
        "all_mutants_zero_unsupported_and_original_expected_failures": True,
        "positive_helper_source_sha256": result["positive_helper_source_sha256"],
        "positive_helper_class_sha256": result["positive_helper_class_sha256"],
        "positive_restoration": result["positive_restoration"],
        "positive_dependency": {"path": str(positive / "checkpoint.json"), "sha256": sha(positive / "checkpoint.json")},
        "files": sorted(files, key=lambda row: row["path"]), "evidence_files": evidence,
        "evidence_bundle": {"path": str(archive), "bytes": archive.stat().st_size, "sha256": sha(archive)},
        "archive_members_hash_verified": True,
    }
    (output / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n")
    print(json.dumps({"checkpoint": str(output / "checkpoint.json"), "sha256": sha(output / "checkpoint.json"),
                      "files": len(files), "evidence_files": len(evidence), "archive": checkpoint["evidence_bundle"]}, indent=2))


if __name__ == "__main__":
    main()
