#!/usr/bin/env python3
"""Prepare both recovered methods in a fresh, independently copied source tree.

The original APK is used only to extract the original-method test fixture. This
does not activate the project or build an APK, and all pending gates stay pending.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from prepare_merge_overlay import BASE_MANIFEST, BASE_PIN, identity, load_checkpoint, replace_once, require, sha, write_json

CONTROL_CHECKPOINT = "fb85463ed7efa33539fcbe621a21f59cb99004b2bd953f4b6ab8fed2ea21d0f1"
ORIGINAL_APK = "84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800"
K_TIMING = "50fcecef6b378c0377c4fad6cf65f87b77167145e51bf408df78c7d15370da49"
K_TIMING_LOG = "d01f2ee585fec74861bd59f616f4aee6dd94b94f79a434ce123b2d5669c9dfc1"


def now():
    return datetime.now(timezone.utc).isoformat()


def copy_checked(source, destination, expected=None):
    require(source.is_file() and not source.is_symlink(), "Nonregular input: " + str(source))
    before = identity(source)
    if expected is not None:
        require(before == {"bytes": expected.get("bytes", expected.get("size")), "sha256": expected["sha256"]},
                "Input hash differs: " + str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    require(identity(source) == before == identity(destination), "Input changed while copying: " + str(source))
    require((source.stat().st_dev, source.stat().st_ino) != (destination.stat().st_dev, destination.stat().st_ino),
            "Mutable source is hardlinked")
    return before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--original-apk", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--timing-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for key, value in vars(args).items():
        setattr(args, key, value.resolve())
    args.output.mkdir(parents=True, exist_ok=False)
    result = {"status": "PREPARING_PRIVATE_COMBINED_SOURCE", "passed": False, "started_utc": now(),
              "commands": [], "active_source_changed": False, "active_apk_changed": False,
              "compiled": False, "android_executed": False}
    result_path = args.output / "preparation.json"
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk)
    env["PATH"] = str(args.jdk / "bin") + os.pathsep + env.get("PATH", "")

    def command(label, argv, cwd, timeout=1200):
        log = args.output / (label + ".log")
        row = {"label": label, "argv": list(map(str, argv)), "cwd": str(cwd), "timeout_seconds": timeout, "started_utc": now()}
        started = time.monotonic()
        with log.open("wb") as stream:
            stream.write(("COMMAND: " + json.dumps(row["argv"]) + "\n").encode()); stream.flush()
            try:
                row["returncode"] = subprocess.run(row["argv"], cwd=cwd, env=env, stdout=stream,
                                                   stderr=subprocess.STDOUT, timeout=timeout).returncode
                row["timed_out"] = False
            except subprocess.TimeoutExpired:
                row.update(returncode=None, timed_out=True)
        row.update(finished_utc=now(), elapsed_seconds=round(time.monotonic() - started, 6),
                   log={"path": log.name, **identity(log)})
        result["commands"].append(row); write_json(result_path, result)
        require(row["returncode"] == 0 and not row["timed_out"], "Preparation command failed: " + label)

    try:
        manifest = args.base / "reports/release-input-snapshot.json"
        require(sha(manifest) == BASE_MANIFEST, "Baseline manifest changed")
        base = json.loads(manifest.read_text())
        require(base["snapshot_sha256"] == BASE_PIN and base["files"] == len(base["entries"]) == 81245
                and hashlib.sha256(json.dumps(base["entries"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == BASE_PIN,
                "Baseline canonical pin is inconsistent")
        require(sha(args.original_apk) == ORIGINAL_APK, "Different supplied APK")
        overlay = load_checkpoint(args.overlay, CONTROL_CHECKPOINT)
        require(overlay["preparation_passed"] is True and overlay["compiled_mutants"] == overlay["executed_mutants"] == 0,
                "Unexpected source-overlay scope")
        require(sha(args.timing_result) == K_TIMING, "Measured K gate record changed")
        timing = json.loads(args.timing_result.read_text())
        measured = next(row for row in timing["commands"] if row["label"] == "all-54-ui-negative-controls")
        require(timing["passed"] is True and measured["returncode"] == 0 and measured["elapsed_seconds"] == 1962.871
                and measured["log_sha256"] == K_TIMING_LOG, "Different measured UI timing")
        timing_log = args.timing_result.parent / measured["log"]
        require(sha(timing_log) == K_TIMING_LOG, "Measured K gate log changed")
        copy_checked(args.timing_result, args.output / "budget-evidence/k54-result.json")
        copy_checked(timing_log, args.output / "budget-evidence/k54-ui.log")
        private = Path(tempfile.mkdtemp(prefix="macrodroid-widget-plugin-combined-")) / "MacroDroid_v9"
        private.mkdir()
        result.update(private_project=str(private), baseline_project=str(args.base), baseline_input_pin=BASE_PIN,
                      baseline_manifest_sha256=BASE_MANIFEST, overlay_checkpoint_sha256=CONTROL_CHECKPOINT,
                      original_apk={"path": str(args.original_apk), **identity(args.original_apk)})
        write_json(result_path, result)
        total = 0
        for relative, expected in base["entries"].items():
            path = Path(relative)
            require(not path.is_absolute() and ".." not in path.parts, "Unsafe manifest path")
            copy_checked(args.base / path, private / path, expected)
            total += expected["size"]
        documentation = []
        for path in sorted(args.base.glob("*.md")):
            documentation.append({"path": path.name, **copy_checked(path, private / path.name)})
        result["source_copy"] = {"files": 81245, "bytes": total, "hardlinked_inputs": 0,
                                 "generated_caches_copied": 0, "all_source_and_destination_hashes_verified": True,
                                 "documentation": documentation}
        changes = []
        for row in overlay["files"]:
            if not row["path"].startswith("project/"):
                continue
            relative = row["path"][len("project/"):]
            path = private / relative
            previous = identity(path) if path.exists() else None
            copied = copy_checked(args.overlay / row["path"], path, row)
            changes.append({"path": relative, "before": previous, "after": copied, "source_checkpoint": CONTROL_CHECKPOINT})
        # The review found the last clean UI execution had no per-child bound.
        path = private / "ui_negative_control.py"
        before_text = path.read_text()
        old = """        build.run([policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1000m','-Dui.report='+str(positive),
                   '-cp',cp,'UiParityTests',build.ROOT,build.WORK/'hybrid'],'ui-positive-restoration.log')"""
        new = """        command=[policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1000m','-Dui.report='+str(positive),
                 '-cp',cp,'UiParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
        with (build.REPORTS/'ui-positive-restoration.log').open('w') as stream:
            stream.write('COMMAND: '+json.dumps(command)+'\\n');stream.flush()
            code=subprocess.run(command,cwd=build.ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
        if code!=0:raise RuntimeError('Positive restoration exited unsuccessfully: '+str(code))"""
        path.write_text(replace_once(before_text, old, new, "bounded final positive UI execution"))
        runner_diff = "".join(difflib.unified_diff(before_text.splitlines(True), path.read_text().splitlines(True),
                                                fromfile="checkpoint-03/ui_negative_control.py", tofile="combined/ui_negative_control.py"))
        (args.output / "positive-restoration-timeout.patch").write_text(runner_diff)
        next(row for row in changes if row["path"] == "ui_negative_control.py").update(
            after=identity(path), followup="Explicitly log and bound the final positive UI child to 300 seconds")
        path = private / "acceptance.py"
        before_text = path.read_text()
        text = replace_once(before_text,
                            "        entry={'label':label,'command':command,'log':logfile.relative_to(ROOT).as_posix()}",
                            "        timeout_seconds=5400 if label=='ui-negative-controls' else 1200\n"
                            "        entry={'label':label,'command':command,'log':logfile.relative_to(ROOT).as_posix(),'timeout_seconds':timeout_seconds}",
                            "record measured per-gate budgets")
        text = replace_once(text, "stderr=subprocess.STDOUT,timeout=1200)",
                            "stderr=subprocess.STDOUT,timeout=timeout_seconds)", "apply measured UI budget")
        path.write_text(text)
        (args.output / "acceptance-budget.patch").write_text("".join(difflib.unified_diff(
            before_text.splitlines(True), text.splitlines(True), fromfile="checkpoint-03/acceptance.py", tofile="combined/acceptance.py")))
        next(row for row in changes if row["path"] == "acceptance.py").update(
            after=identity(path), followup="Measured UI suite budget 5400 seconds; all other existing gate budgets remain 1200")
        result["execution_budget"] = {"measured_k54_seconds": 1962.871, "measurement_sha256": K_TIMING,
                                      "ui_suite_seconds": 5400, "other_gate_seconds": 1200,
                                      "every_ui_execution_seconds": 300, "source_ci_minutes": 120}
        # Stage the workflow only. Publication must accompany the verified combined APK.
        workflow_path = args.repository / ".github/workflows/reconstruction.yml"
        workflow_before = workflow_path.read_text()
        workflow = replace_once(workflow_before, "    timeout-minutes: 90\n", "    timeout-minutes: 120\n", "source CI job budget")
        report_start = "            workspace/MacroDroid_v9/reports/acceptance-latest.json\n"
        report_end = "            workspace/MacroDroid_v9/reports/android-runtime/result.json\n"
        require(workflow.count(report_start) == workflow.count(report_end) == 1, "Unexpected report-upload block")
        start, end = workflow.index(report_start), workflow.index(report_end) + len(report_end)
        workflow = workflow[:start] + "            workspace/MacroDroid_v9/reports/\n" + workflow[end:]
        staged_workflow = args.output / "repository-overlay/.github/workflows/reconstruction.yml"
        staged_workflow.parent.mkdir(parents=True); staged_workflow.write_text(workflow)
        result["repository_overlay"] = [{"path": ".github/workflows/reconstruction.yml", "before": identity(workflow_path),
                                          "after": identity(staged_workflow), "activate_only_with_verified_combined_candidate": True}]
        for relative, methods, classes in (("source/java-method-map.json", 1242, 605), ("source/ui-methods.json", 10, 10)):
            entries = json.loads((private / relative).read_text())
            require(len(entries) == methods and len({entry["target"] for entry in entries}) == classes,
                    "Combined registry inventory differs: " + relative)
        result["overlays"] = changes
        write_json(result_path, result)
        command("bootstrap-extractor", [sys.executable, "-c", "import build; build.bootstrap()"], private)
        command("extract-full-original-fixture", [args.jdk / "bin/java", "-Xmx1200m", "-cp",
                os.pathsep.join(map(str, [private / "tools/lib/jadx-r2721.4574686-all.jar", private / "tools/classes"])),
                "ExtractOracle", private, args.original_apk], private)
        require("Test-only original fixture: classes=605 methods=1242" in (args.output / "extract-full-original-fixture.log").read_text(),
                "Combined original fixture has a different inventory")
        fixture = private / "tests/fixtures/original-methods.dex"
        result["full_original_fixture"] = {"path": "tests/fixtures/original-methods.dex", **identity(fixture), "test_only_not_apk_input": True}
        provenance_path = private / "tests/fixtures/provenance.json"
        previous = identity(provenance_path)
        provenance = json.loads(provenance_path.read_text())
        require(provenance["original_apk_sha256"] == ORIGINAL_APK and provenance["methods"] == 1240 and provenance["classes"] == 603,
                "Different fixture provenance baseline")
        provenance.update(fixture_sha256=sha(fixture), fixture_bytes=fixture.stat().st_size, methods=1242, classes=605,
                          extraction="Fresh ExtractOracle run against the unchanged original upload; exact registered plugin upload and Widget methods added to the published 1,240-method fixture")
        write_json(provenance_path, provenance)
        changes.append({"path": "tests/fixtures/provenance.json", "before": previous, "after": identity(provenance_path),
                        "operation": "Pin the actually extracted combined original fixture"})
        command("pin-private-inputs", [sys.executable, "release_integrity.py", "record"], private)
        candidate = json.loads((private / "reports/release-input-snapshot.json").read_text())
        old, new = base["entries"], candidate["entries"]
        delta = {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
                 "changed": sorted(key for key in old.keys() & new.keys() if old[key] != new[key])}
        expected_delta = {row["path"] for row in changes if row["before"] != row["after"]} | {"tests/fixtures/original-methods.dex"}
        require(not delta["removed"] and set(delta["added"] + delta["changed"]) == expected_delta,
                "Unreviewed combined source input delta")
        result.update(candidate_inputs={key: value for key, value in candidate.items() if key != "entries"},
                      input_delta=delta, registry_methods=1242, registry_classes=605, ui_methods=10,
                      expected_cases=193489, expected_ui_cases=23174, expected_ui_independent_checks=15326,
                      expected_python_tests=273, expected_ui_controls=78,
                      status="PRIVATE_COMBINED_SOURCE_PREPARED", passed=True)
    except BaseException as error:
        result.update(status="PRIVATE_COMBINED_SOURCE_PREPARATION_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now(); write_json(result_path, result)
        print(json.dumps({key: result.get(key) for key in ("status", "passed", "private_project", "candidate_inputs", "error")}, indent=2))


if __name__ == "__main__":
    main()
