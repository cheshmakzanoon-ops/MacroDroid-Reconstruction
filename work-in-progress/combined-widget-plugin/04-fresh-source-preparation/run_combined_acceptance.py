#!/usr/bin/env python3
"""Run all 16 acceptance gates and independently bind the closed combined proof."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from prepare_merge_overlay import identity, require, write_json


def now():
    return datetime.now(timezone.utc).isoformat()


def verify_inputs(root, expected_pin):
    path = root / "reports/release-input-snapshot.json"
    pin = json.loads(path.read_text())
    require(pin["snapshot_sha256"] == expected_pin and pin["files"] == len(pin["entries"])
            and hashlib.sha256(json.dumps(pin["entries"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == expected_pin,
            "Combined manifest identity differs")
    for relative, expected in pin["entries"].items():
        require(identity(root / relative) == {"bytes": expected["size"], "sha256": expected["sha256"]},
                "Combined input changed: " + relative)
    return pin


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", required=True, type=Path)
    parser.add_argument("--jdk", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.preparation, args.jdk, args.output = [p.resolve() for p in (args.preparation, args.jdk, args.output)]
    preparation = json.loads(args.preparation.read_text())
    require(preparation["passed"] is True and preparation["status"] == "PRIVATE_COMBINED_SOURCE_PREPARED",
            "Combined source preparation is incomplete")
    root = Path(preparation["private_project"])
    expected_pin = preparation["candidate_inputs"]["snapshot_sha256"]
    args.output.mkdir(parents=True, exist_ok=False)
    result_path = args.output / "result.json"
    result = {"status": "RUNNING_COMBINED_ACCEPTANCE", "passed": False, "started_utc": now(),
              "preparation": {"path": str(args.preparation), **identity(args.preparation)}, "project": str(root),
              "source_input_snapshot_sha256": expected_pin, "commands": [],
              "android_executed": False, "whole_application_1_to_1_established": False}
    env = os.environ.copy(); env["JAVA_HOME"] = str(args.jdk)
    env["PATH"] = str(args.jdk / "bin") + os.pathsep + env.get("PATH", "")
    env["PYTHONUTF8"] = "1"
    try:
        pin_before = verify_inputs(root, expected_pin)
        result.update(input_files=pin_before["files"], inputs_verified_before=True)
        require(not (root / "reports/acceptance-latest.json").exists(), "Combined acceptance output is not fresh")
        command = [sys.executable, "acceptance.py"]
        log = args.output / "complete-acceptance.log"
        entry = {"argv": command, "cwd": str(root), "started_utc": now(), "timeout_seconds": 7800}
        result["commands"].append(entry); write_json(result_path, result)
        started = time.monotonic()
        with log.open("wb") as stream:
            stream.write(("COMMAND: " + json.dumps(command) + "\n").encode()); stream.flush()
            try:
                entry["returncode"] = subprocess.run(command, cwd=root, env=env, stdout=stream,
                                                      stderr=subprocess.STDOUT, timeout=7800).returncode
                entry["timed_out"] = False
            except subprocess.TimeoutExpired:
                entry.update(returncode=None, timed_out=True)
        entry.update(finished_utc=now(), elapsed_seconds=round(time.monotonic() - started, 6), log={"path": log.name, **identity(log)})
        write_json(result_path, result)
        require(entry["returncode"] == 0 and not entry["timed_out"], "Configured full acceptance failed")
        acceptance = json.loads((root / "reports/acceptance-latest.json").read_text())
        labels = ["input-integrity", "baseline-build", "hybrid-build", "baseline-code", "hybrid-code", "baseline-resources",
                  "hybrid-resources", "positive-host-tests", "reference-status", "engine-negative-controls",
                  "ui-negative-controls", "core-negative-controls", "environment-negative-controls", "legacy-negative-control",
                  "signed-source-edit", "final-positive-host-tests"]
        require(acceptance["host_acceptance_passed"] is True and acceptance["source_edit_probe_skipped"] is False
                and [row["label"] for row in acceptance["commands"]] == labels
                and all(row["passed"] is True and row["exit_code"] == 0 for row in acceptance["commands"]),
                "All 16 complete gates are required")
        require(acceptance["input_snapshot_before"] == acceptance["input_snapshot_after"] == expected_pin
                and acceptance["build_inputs_unchanged"] is True, "Acceptance input boundaries differ")
        for row in acceptance["commands"]:
            require(identity(root / row["log"])["sha256"] == row["log_sha256"], "Acceptance gate log changed")
            require(row["timeout_seconds"] == (5400 if row["label"] == "ui-negative-controls" else 1200), "Gate budget changed")
        for relative, digest in acceptance["fresh_evidence_sha256"].items():
            require(identity(root / "reports" / relative)["sha256"] == digest, "Fresh acceptance evidence changed: " + relative)
        overall = json.loads((root / "reports/java-all-path-parity.json").read_text())
        ui = json.loads((root / "reports/java-ui-three-path-parity.json").read_text())
        controls = json.loads((root / "reports/ui-negative-controls.json").read_text())
        require(overall["passed"] is True and overall["cases"] == 193489 and overall["methodsCovered"] == overall["methodsExpected"] == 1242
                and overall["paths"] == 3 and overall["failedCases"] == overall["unsupportedExecutions"] == 0
                and overall["schemaValid"] is True and overall["exactMethodKeyPartitionVerified"] is True
                and overall["rebuiltDexComparedToApk"] is True, "Combined three-path inventory or outcome differs")
        require(ui["passed"] is True and ui["cases"] == 23174 and ui["methodsCovered"] == 10 and ui["paths"] == 3
                and ui["failedCases"] == ui["unsupportedExecutions"] == ui["expectedResultFailures"] == 0
                and ui["independentExpectedResultChecks"] == 15326
                and ui["widgetInstructionAndConditionalCoverage"] is True and ui["pluginUploadInstructionAndConditionalCoverage"] is True,
                "Combined UI outcome differs")
        require(controls["pass"] is True and controls["controlsCount"] == len(controls["controls"]) == 78
                and controls["positiveRestorationPassed"] is True and controls["positiveRestorationExactBaseline"] is True
                and controls["restorationCases"] == 23174 and controls["sourceFixtureAndApkUnchanged"] is True
                and all(row["pass"] is True and row["requiredCaseRejected"] is True and row["unsupportedExecutions"] == 0
                        and row["originalCoverageAndInventoryUnchanged"] is True for row in controls["controls"]),
                "All 78 actual controls and exact positive restoration are required")
        require(re.search(r"Ran 273 tests in [\d.]+s\s+OK\s*$", (root / "reports/python-unit-tests.log").read_text()),
                "All 273 Python tests are required")
        for row in controls["controls"]:
            require(identity(root / row["retainedSource"])["sha256"] == row["mutantSourceSha256"]
                    and identity(root / row["retainedClass"])["sha256"] == row["mutantClassSha256"]
                    and row["mutantClassSha256"] != row["positiveClassSha256"], "Retained actual mutation bytes differ")
        apks = {}
        for variant, expected in acceptance["apks"].items():
            actual = identity(root / expected["path"])
            require(actual == {"bytes": expected["bytes"], "sha256": expected["sha256"]}, "Final signed APK differs")
            apks[variant] = {"path": expected["path"], **actual}
        require(apks["baseline"]["sha256"] == "aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096", "Preserved baseline changed")
        require(verify_inputs(root, expected_pin) == pin_before, "Final source inputs differ")
        result.update(status="COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED", passed=True, inputs_verified_after=True,
                      cases=193489, registered_methods=1242, registry_classes=605, paths=3, python_tests=273,
                      ui_cases=23174, ui_methods=10, independent_ui_checks=15326, ui_fault_controls=78,
                      acceptance=identity(root / "reports/acceptance-latest.json"), apks=apks,
                      gate_logs_independently_verified=16, fresh_reports_independently_verified=len(acceptance["fresh_evidence_sha256"]),
                      retained_mutant_source_and_class_pairs_verified=78)
    except BaseException as error:
        result.update(status="COMBINED_ACCEPTANCE_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now(); write_json(result_path, result)
        print(json.dumps({key: result.get(key) for key in ("status", "passed", "cases", "registered_methods", "apks", "error")}, indent=2))


if __name__ == "__main__":
    main()
