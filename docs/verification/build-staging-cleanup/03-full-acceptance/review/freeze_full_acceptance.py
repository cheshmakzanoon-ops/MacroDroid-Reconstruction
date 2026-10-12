#!/usr/bin/env python3
"""Freeze and independently verify the completed f83 host acceptance evidence.

This script reads the private checkout. It does not execute its source, rebuild,
install an APK, alter the checkout, or delete generated files. The output must
be a new directory. The complete reports tree is preserved without rewriting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_SNAPSHOT = "f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85"
EXPECTED_MANIFEST = "5604f592394768e2ac8183cfd767f059a87cf0507d90237cb3a949df4b4f40b3"
EXPECTED_FINISHED = "2026-10-12T03:23:14.787813+00:00"
EXPECTED_APKS = {
    "baseline": (94677674, "aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096"),
    "hybrid": (94683342, "be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce"),
}
LABELS = [
    "input-integrity", "baseline-build", "hybrid-build", "baseline-code",
    "hybrid-code", "baseline-resources", "hybrid-resources", "positive-host-tests",
    "reference-status", "engine-negative-controls", "ui-negative-controls",
    "core-negative-controls", "environment-negative-controls", "legacy-negative-control",
    "signed-source-edit", "final-positive-host-tests",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def metadata(path: Path) -> dict:
    require(path.is_file() and not path.is_symlink(), f"Expected regular file: {path}")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": path.stat().st_size, "sha256": digest}


def safe_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, f"Unsafe relative path: {relative}")
    destination = root / path
    require(destination.resolve().is_relative_to(root.resolve()), f"Escaping path: {relative}")
    return destination


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def independent_inputs(root: Path) -> dict:
    entries = {}
    for directory in ["source", "test-support", "tests", "signing", "tools", "reference"]:
        for path in sorted((root / directory).rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(root)
            if directory == "tools" and "classes" in relative.parts:
                continue
            if path.suffix in [".pyc", ".pyo"]:
                continue
            record = metadata(path)
            entries[relative.as_posix()] = {"size": record["bytes"], "sha256": record["sha256"]}
    for path in sorted(root.glob("*.py")):
        record = metadata(path)
        entries[path.relative_to(root).as_posix()] = {"size": record["bytes"], "sha256": record["sha256"]}
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return {"format": 1, "files": len(entries), "snapshot_sha256": hashlib.sha256(canonical).hexdigest(), "entries": entries}


def copy_exact(source: Path, destination: Path) -> dict:
    before = metadata(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as reader, destination.open("xb") as writer:
        shutil.copyfileobj(reader, writer)
    require(metadata(destination) == before == metadata(source), f"Copy/source changed: {source}")
    return before


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--prior-checkpoint", type=Path, required=True)
    parser.add_argument("--readme", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.source.resolve()
    out = args.output.resolve()
    archive = out.with_suffix(".zip")
    receipt = out.with_name(out.name + "-delivery.json")
    require(not out.exists() and not archive.exists() and not receipt.exists(), "Output already exists")
    report_path = root / "reports/acceptance-latest.json"
    report_before = metadata(report_path)
    result = json.loads(report_path.read_text())
    require(result["finished_utc"] == EXPECTED_FINISHED, "Unexpected acceptance run")
    require(result["host_acceptance_passed"] is True, "Host acceptance did not pass")
    require(result["source_edit_probe_skipped"] is False, "Signed source edit was skipped")
    require(result["build_inputs_unchanged"] is True, "Run inputs changed")
    require(result["input_files"] == 81212, "Unexpected input count")
    require(result["input_snapshot_before"] == result["input_snapshot_after"] == EXPECTED_SNAPSHOT, "Unexpected run input identity")
    require([item["label"] for item in result["commands"]] == LABELS, "Incomplete or unexpected gate sequence")

    gate_checks = []
    for gate in result["commands"]:
        actual = metadata(safe_path(root, gate["log"]))
        require(gate["exit_code"] == 0 and gate["passed"] is True, f"Failed gate: {gate['label']}")
        require(actual["sha256"] == gate["log_sha256"], f"Gate log hash mismatch: {gate['label']}")
        gate_checks.append({"label": gate["label"], "path": gate["log"], "exit_code": 0, **actual, "recorded_hash_matches": True})
    run_folder = Path(result["commands"][0]["log"]).parent
    require(metadata(root / run_folder / "result.json") == report_before, "Latest and final run result differ")
    evidence_checks = []
    require(len(result["fresh_evidence_sha256"]) == 19, "Unexpected fresh-evidence count")
    for name, expected in result["fresh_evidence_sha256"].items():
        actual = metadata(safe_path(root / "reports", name))
        require(actual["sha256"] == expected, f"Fresh evidence hash mismatch: {name}")
        evidence_checks.append({"path": "reports/" + name, **actual, "recorded_hash_matches": True})

    test_path = root / "reports/python-unit-tests.log"
    test_text = test_path.read_text()
    test_summaries = re.findall(r"^Ran (\d+) tests in ([0-9.]+)s$", test_text, re.M)
    ok_lines = re.findall(r"^test.* \.\.\. ok$", test_text, re.M)
    require(test_summaries == [("209", "25.161")], "Unexpected Python test summary")
    require(len(ok_lines) == 209 and test_text.rstrip().endswith("\nOK"), "Python outcomes do not confirm 209 successes")
    parity = json.loads((root / "reports/java-all-path-parity.json").read_text())
    require(parity["passed"] is True and parity["cases"] == 185738, "Unexpected bounded host cases")
    require(parity["methodsCovered"] == parity["methodsExpected"] == 1239 and parity["paths"] == 3, "Unexpected recovered-method coverage")
    require(parity["failedCases"] == parity["unsupportedExecutions"] == 0, "Host parity failures")

    apk_checks = []
    for variant, (size, digest) in EXPECTED_APKS.items():
        reported = result["apks"][variant]
        actual = metadata(safe_path(root, reported["path"]))
        require(actual == {"bytes": size, "sha256": digest}, f"Unexpected actual {variant} APK")
        require(actual == {key: reported[key] for key in ["bytes", "sha256"]}, f"Recorded {variant} APK differs")
        apk_checks.append({"variant": variant, "path": reported["path"], **actual, "recorded_hash_matches": True, "copied_into_report_capsule": False})
    require(parity["apkSha256"] == EXPECTED_APKS["hybrid"][1], "Host parity APK identity differs")

    manifest_path = root / "reports/release-input-snapshot.json"
    manifest_meta = metadata(manifest_path)
    require(manifest_meta["sha256"] == EXPECTED_MANIFEST, "Unexpected pinned input manifest bytes")
    expected_inputs = json.loads(manifest_path.read_text())
    print("Verifying all 81,212 source/test/tool/reference input files independently", flush=True)
    actual_inputs = independent_inputs(root)
    require(actual_inputs == expected_inputs, "Current inputs differ from the frozen release manifest")
    require(actual_inputs["snapshot_sha256"] == EXPECTED_SNAPSHOT, "Independent snapshot differs")
    prior = json.loads(args.prior_checkpoint.read_text())
    require(prior["source_input_snapshot_sha256"] == EXPECTED_SNAPSHOT, "Prior checkpoint input binding differs")
    require(prior["source_input_manifest_file_sha256"] == EXPECTED_MANIFEST, "Prior manifest binding differs")
    prior_checks = []
    for entry in prior["files"]:
        if entry["path"].startswith("reports/"):
            continue
        actual = metadata(safe_path(root, entry["path"]))
        require(actual == {key: entry[key] for key in ["bytes", "sha256"]}, f"Prior source changed: {entry['path']}")
        prior_checks.append({"path": entry["path"], **actual, "prior_checkpoint_matches": True})

    reports = sorted(path for path in (root / "reports").rglob("*") if path.is_file())
    require(len(reports) == 219, "Unexpected complete report count")
    patterns = {
        "private_key_pem": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "github_access_token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
        "signed_download_query": re.compile(rb"(?:X-Amz-Signature=|[?&]sig=)[A-Za-z0-9%+/]{30,}"),
    }
    scan_counts = {name: 0 for name in patterns}
    for path in reports:
        content = path.read_bytes()
        for name, pattern in patterns.items():
            scan_counts[name] += len(pattern.findall(content))
    require(not any(scan_counts.values()), "Report capsule needs key-material review")

    out.mkdir(parents=True)
    report_entries = []
    for path in reports:
        relative = path.relative_to(root).as_posix()
        record = copy_exact(path, out / relative)
        report_entries.append({"path": relative, **record})
    for name in ["acceptance.py", "release_integrity.py", "test.py"]:
        copy_exact(root / name, out / "input-binding" / name)
    copy_exact(args.prior_checkpoint, out / "input-binding/prior-checkpoint.json")
    copy_exact(Path(__file__), out / "freeze_full_acceptance.py")
    copy_exact(args.readme, out / "README.md")
    write_json(out / "reports-manifest.json", {"files": len(report_entries), "bytes": sum(entry["bytes"] for entry in report_entries), "entries": report_entries})
    verification = {
        "status": "INDEPENDENTLY_VERIFIED_COMPLETE_HOST_ACCEPTANCE",
        "verified_utc": datetime.now(timezone.utc).isoformat(),
        "source_checkout": str(root),
        "acceptance_result": {"path": "reports/acceptance-latest.json", **report_before},
        "run_result_is_identical": True,
        "started_utc": result["started_utc"],
        "finished_utc": result["finished_utc"],
        "gate_logs": gate_checks,
        "fresh_evidence": evidence_checks,
        "python_tests": {"path": "reports/python-unit-tests.log", **metadata(test_path), "actual_summary_count": 209, "individual_ok_lines": 209, "seconds": 25.161, "terminal_ok": True},
        "host_parity": parity,
        "apks": apk_checks,
        "input_binding": {"files": actual_inputs["files"], "snapshot_sha256": actual_inputs["snapshot_sha256"], "manifest": {"path": "reports/release-input-snapshot.json", **manifest_meta}, "independent_file_hashes_match_manifest": True, "before_and_after_report_match": True, "prior_source_files": prior_checks, "prior_repository_path": "work-in-progress/staging-cleanup/01-fresh-generations/checkpoint.json", "prior_published_commit": "ef1bcbd5087b4959a0bc103b5400e51cd731a095"},
        "report_copy": {"files": len(report_entries), "bytes": sum(entry["bytes"] for entry in report_entries), "all_source_and_destination_hashes_rechecked": True, "complete_reports_tree_preserved": True, "content_rewritten": False},
        "key_material_scan": {"patterns": list(patterns), "matches": scan_counts},
        "android_runtime_executed_by_this_acceptance": False,
        "android_probe_status": result["android_status"],
        "full_runtime_1_to_1_established": False,
        "cleanup_performed": False,
        "cleanup_requires_durable_publication_receipt": True,
    }
    require(result["android_runtime_executed"] is False and result["android_status"] == "BLOCKED", "Unexpected local Android scope")
    require(metadata(report_path) == report_before, "Acceptance result changed during freezing")
    write_json(out / "independent-verification.json", verification)
    all_entries = [{"path": path.relative_to(out).as_posix(), **metadata(path)} for path in sorted(out.rglob("*")) if path.is_file()]
    write_json(out / "checkpoint.json", {"status": "FROZEN_COMPLETE_HOST_ACCEPTANCE_PASSED", "scope": "All 16 configured host gates on unchanged f83 inputs; 1,239 methods and 185,738 bounded cases. No Android execution or full-app parity claim.", "input_snapshot_sha256": EXPECTED_SNAPSHOT, "finished_utc": EXPECTED_FINISHED, "files": all_entries})
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for path in sorted(out.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(path.relative_to(out).as_posix(), date_time=(2026, 10, 12, 3, 23, 14))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            target.writestr(info, path.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as source:
        require(source.testzip() is None, "Archive CRC failure")
        for info in source.infolist():
            require(source.read(info) == (out / info.filename).read_bytes(), f"Archive changed bytes: {info.filename}")
    delivery = {"checkpoint_directory": str(out), "suggested_repository_path": "docs/verification/build-staging-cleanup/03-full-acceptance", "checkpoint": metadata(out / "checkpoint.json"), "archive": {"path": str(archive), **metadata(archive)}, "archive_file_count": len(all_entries) + 1, "all_archive_bytes_match_frozen_tree": True, "cleanup_performed": False}
    write_json(receipt, delivery)
    print(json.dumps(delivery, indent=2))


if __name__ == "__main__":
    main()
