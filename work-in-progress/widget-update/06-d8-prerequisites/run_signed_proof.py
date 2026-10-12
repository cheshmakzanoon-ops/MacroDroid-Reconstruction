#!/usr/bin/env python3
"""Run a fresh signed Widget candidate through the five planned proof gates.

This is a complete signed/body/resource/three-path proof for the prepared input
snapshot. Deliberate-fault controls, full configured acceptance and Android
behavior have separate results and are never implied by these five commands.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

from prepare_signed_study import now, record, require, sha, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.preparation = args.preparation.resolve()
    args.jdk = args.jdk.resolve()
    args.output = args.output.resolve()
    preparation = json.loads(args.preparation.read_text())
    require(preparation["passed"] is True and preparation["status"] == "PRIVATE_WIDGET_D8_STATIC_LINKAGE_PASSED", "Widget prerequisites have not passed")
    root = Path(preparation["private_project"])
    args.output.mkdir(parents=True, exist_ok=False)
    resultpath = args.output / "result.json"
    result = {"status": "SIGNED_WIDGET_PROOF_RUNNING", "passed": False, "started_utc": now(),
              "project": str(root), "preparation": {"path": str(args.preparation), **record(args.preparation)},
              "commands": [], "scope": "Five planned host and signed-artifact gates; no full acceptance or Android feature claim"}
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk)
    env["PATH"] = str(args.jdk / "bin") + os.pathsep + env.get("PATH", "")

    def inputs():
        spec = importlib.util.spec_from_file_location("widget_private_integrity", root / "release_integrity.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.snapshot()

    def command(label, arguments):
        logfile = args.output / (label + ".log")
        value = {"label": label, "argv": [sys.executable, *arguments], "cwd": str(root), "started_utc": now(), "timeout_seconds": 1200}
        started = time.monotonic()
        with logfile.open("wb") as stream:
            stream.write(("COMMAND: " + json.dumps(value["argv"]) + "\n").encode())
            stream.flush()
            try:
                process = subprocess.run(value["argv"], cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1200)
                value.update(returncode=process.returncode, timed_out=False)
            except subprocess.TimeoutExpired:
                value.update(returncode=None, timed_out=True)
        value.update(finished_utc=now(), elapsed_seconds=round(time.monotonic()-started, 6), log={"path": logfile.name, **record(logfile)})
        value["passed"] = value["returncode"] == 0 and value["timed_out"] is False
        result["commands"].append(value)
        write(resultpath, result)
        require(value["passed"], "Signed Widget command failed: " + label)

    try:
        pin = json.loads((root / "reports/release-input-snapshot.json").read_text())
        require(pin["snapshot_sha256"] == preparation["candidate_inputs"]["snapshot_sha256"], "Prepared Widget pin changed")
        actual = inputs()
        require(actual == pin, "Private Widget inputs changed after prerequisites")
        result["source_input_snapshot_sha256"] = pin["snapshot_sha256"]
        result["source_input_files"] = pin["files"]
        result["inputs_verified_before_commands"] = True
        write(resultpath, result)
        for label, argv in [
            ("hybrid-build", ["build.py", "build", "--variant", "hybrid"]),
            ("hybrid-code", ["build.py", "verify", "--variant", "hybrid"]),
            ("hybrid-resources", ["resource_verify.py", "--variant", "hybrid"]),
            ("three-path-host-tests", ["test.py", "--three-way"]),
            ("final-input-integrity", ["release_integrity.py", "verify"]),
        ]:
            command(label, argv)
        require(inputs() == pin, "Final independent input hash recheck failed")
        reports = root / "reports"
        names = ["hybrid-build.json", "hybrid-roundtrip.json", "hybrid-resource-parity.json", "java-integration.json",
                 "migration-static-proof.json", "migration-linkage-check.json", "java-all-path-parity.json",
                 "java-ui-three-path-parity.json", "java-three-path-parity.json", "java-core-three-path-parity.json",
                 "java-environment-three-path-parity.json", "java-engine-three-path-parity.json", "oracle-semantics.json",
                 "engine-oracle-semantics.json", "ui-oracle-semantics.json", "constructor-oracle-conformance.json",
                 "widget-bitwise-oracle-conformance.json", "python-unit-tests.log"]
        result["fresh_reports"] = {name: record(reports / name) for name in names}
        parity = json.loads((reports / "java-all-path-parity.json").read_text())
        require(parity["passed"] is True and parity["paths"] == 3 and parity["cases"] == 191133 and parity["methodsCovered"] == parity["methodsExpected"] == 1241,
                "Signed Widget aggregate coverage differs from the registered suite")
        require(parity["failedCases"] == parity["unsupportedExecutions"] == 0 and parity["exactMethodKeyPartitionVerified"] is True and parity["rebuiltDexComparedToApk"] is True,
                "Aggregate failures, unsupported instructions, partition or APK identity gap")
        ui = json.loads((reports / "java-ui-three-path-parity.json").read_text())
        require(ui["passed"] is True and ui["methodsCovered"] == 9 and ui["cases"] == 20818 and ui["widgetInstructionAndConditionalCoverage"] is True,
                "Widget UI path/coverage gate failed")
        rules = []
        for name in ["java-integration.json", "migration-static-proof.json", "migration-linkage-check.json"]:
            body = json.loads((reports / name).read_text())
            if name != "java-integration.json":
                require(body["pass"] is True, "Static or linkage gate is not positive")
            corrections = body["constructor_owner_corrections"]
            require(len(corrections) == 1, "Expected exactly one mapped constructor reference")
            correction = corrections[0]
            require(correction["allocated_type"] == "Lzhh;" and correction["original_owner"] == "Lrff;" and correction["constructor"] == "<init>(ILm73;)V",
                    "Wrong constructor allocation/owner/descriptor")
            require(correction["occurrences"] == correction["owner_references_changed"] == 1 and correction["allocation_types_changed"] == correction["constructors_added"] == 0,
                    "Constructor mapping changed more than the one owner reference")
            rules.append(correction)
        require(rules[0] == rules[1] == rules[2], "Build/static/linkage constructor evidence differs")
        unit_log = (reports / "python-unit-tests.log").read_text()
        match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK\s*$", unit_log)
        require(match is not None, "Actual Python unit-test result is missing")
        apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
        apk_record = record(apk)
        require(apk_record["sha256"] == parity["apkSha256"], "Signed artifact differs from the tested DEX container")
        build_record = json.loads((reports / "hybrid-build.json").read_text())
        require(apk_record == {"bytes": build_record["bytes"], "sha256": build_record["sha256"]} and build_record["original_apk_build_input"] is False and build_record["original_dex_build_input"] is False,
                "Build artifact identity or source provenance failed")
        # Keep the exact D8 helper and transformed runtime method reviewable even
        # if the much larger closed generated cache is retired after publication.
        originals = json.loads((root / "source/class-index.json").read_text())
        target = rules[0]["target"]
        indexed = [entry for entry in originals.values() if entry["descriptor"] == target]
        require(len(indexed) == 1, "Mapped class is ambiguous")
        copied = []
        for source, relative in [
            (root / "build/java/smali/recovered/ui/WidgetUpdateMethods.smali", "compiled-helper.smali"),
            (root / indexed[0]["path"], "preserved-widget-class.smali"),
            (root / "build/hybrid-smali" / Path(indexed[0]["path"]).relative_to("source/smali"), "signed-widget-class.smali"),
        ]:
            destination = args.output / relative
            shutil.copy2(source, destination)
            require(record(source) == record(destination), "Compiled evidence copy changed")
            copied.append({"path": relative, **record(destination)})
        result.update(status="SIGNED_WIDGET_FIVE_GATES_PASSED", passed=True, inputs_verified_after_commands=True,
                      apk={"path": str(apk), **apk_record}, cases=parity["cases"], registered_methods=1241,
                      paths=3, python_tests=int(match[1]), constructor_owner_correction=rules[0], compiled_evidence=copied)
    except BaseException as error:
        result.update(status="SIGNED_WIDGET_PROOF_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now()
        write(resultpath, result)
        print(json.dumps({key: result.get(key) for key in ["status", "passed", "cases", "registered_methods", "paths", "python_tests", "apk", "error"]}, indent=2))


if __name__ == "__main__":
    main()
