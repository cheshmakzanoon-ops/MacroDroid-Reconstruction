#!/usr/bin/env python3
"""Measure the unchanged complete UI suite with HotSpot fast-throw omission disabled."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import time

from prepare_signed_study import now, record, require, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project, jdk, output = [p.resolve() for p in (args.project, args.jdk, args.output)]
    output.mkdir(parents=True, exist_ok=False)
    result = {"status": "JVM_EXCEPTION_FLAG_STUDY_RUNNING", "passed": False, "started_utc": now(),
              "scope": "Unchanged full UI harness and signed DEX, one explicit HotSpot runtime flag; no Android execution",
              "project": str(project), "commands": []}

    def inventory():
        paths = [project / "dist/MacroDroid-5.67.8-v9-hybrid.apk",
                 project / "tests/fixtures/original-methods.dex",
                 project / "tools/lib/jadx-r2721.4574686-all.jar",
                 project / "source/ui-methods.json",
                 project / "source/java/recovered/ui/WidgetUpdateMethods.java",
                 project / "tests/java/BytecodeOracle.java",
                 project / "tests/java/WidgetParityCases.java",
                 project / "tests/java/UiParityTests.java"]
        for folder in (project / "build/java/hostclasses", project / "tools/classes"):
            paths.extend(p for p in folder.rglob("*") if p.is_file())
        paths.extend((project / "build/hybrid").glob("*.dex"))
        return {p.relative_to(project).as_posix(): record(p) for p in sorted(set(paths))}

    def command(label, argv, timeout):
        log = output / (label + ".log")
        started = time.monotonic()
        with log.open("w") as stream:
            stream.write("COMMAND: " + json.dumps(list(map(str, argv))) + "\n")
            stream.flush()
            value = subprocess.run(list(map(str, argv)), cwd=project, stdout=stream,
                                   stderr=subprocess.STDOUT, timeout=timeout)
        row = {"label": label, "argv": list(map(str, argv)), "returncode": value.returncode,
               "elapsed_seconds": round(time.monotonic() - started, 6), "log": {"path": log.name, **record(log)}}
        result["commands"].append(row)
        write(output / "result.json", result)
        return row

    try:
        failed_path = project / "reports/java-ui-three-path-parity.json"
        failed = json.loads(failed_path.read_text())
        require(failed["passed"] is False and failed["failedCases"] == 1
                and failed["failedCaseLabels"] == ["widget-saved-cast:1:3:false"]
                and failed["cases"] == 20818 and failed["paths"] == 3
                and failed["unsupportedExecutions"] == failed["expectedResultFailures"] == 0,
                "The precondition is not the closed one-message UI failure")
        result["closed_failure"] = {"path": str(failed_path), **record(failed_path)}
        write(output / "closed-ui-failure.json", failed)
        before = inventory()
        write(output / "inputs-before.json", before)
        result["bound_input_files"] = len(before)
        result["java_binary"] = record(jdk / "bin/java")
        flags = command("effective-flags", [jdk / "bin/java", "-XX:-OmitStackTraceInFastThrow", "-XX:+PrintFlagsFinal", "-version"], 30)
        flag_text = (output / "effective-flags.log").read_text()
        require(flags["returncode"] == 0 and "OmitStackTraceInFastThrow                = false" in flag_text
                and "ShowCodeDetailsInExceptionMessages       = true" in flag_text,
                "The requested exception-message runtime policy did not take effect")
        cp = os.pathsep.join(str(project / p) for p in (
            "tools/lib/jadx-r2721.4574686-all.jar", "build/java/hostclasses", "tools/classes"))
        run = command("full-ui-without-fast-throw-omission", [jdk / "bin/java", "-XX:-OmitStackTraceInFastThrow", "-Xmx1000m",
                      "-Dui.report=" + str(output / "ui-result.json"), "-cp", cp,
                      "UiParityTests", project, project / "build/hybrid"], 300)
        observed = json.loads((output / "ui-result.json").read_text())
        after = inventory()
        write(output / "inputs-after.json", after)
        same_keys = ["cases", "paths", "methodsCovered", "methodKeys", "methods", "instructionCoverage",
                     "independentExpectedResultChecks", "expectedResultFailures", "unsupportedExecutions"]
        result["same_execution_inventory_and_original_coverage"] = all(observed[k] == failed[k] for k in same_keys)
        result["inputs_unchanged"] = before == after
        result["ui_report"] = record(output / "ui-result.json")
        result["generated_message_exclusions"] = observed.get("widgetGeneratedNullMessageExclusions")
        result["cases"] = observed["cases"]
        result["failed_cases"] = observed["failedCases"]
        result["passed"] = (run["returncode"] == 0 and observed["passed"] is True and observed["failedCases"] == 0
                            and result["same_execution_inventory_and_original_coverage"] and result["inputs_unchanged"])
        result["status"] = "UNCHANGED_UI_PASSED_WITH_EXPLICIT_EXCEPTION_RUNTIME_POLICY" if result["passed"] else "EXCEPTION_FLAG_DID_NOT_RESOLVE_UI_FAILURE"
    except BaseException as error:
        result.update(status="JVM_EXCEPTION_FLAG_STUDY_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now()
        write(output / "result.json", result)
    print(json.dumps({k: result[k] for k in ("status", "passed", "cases", "failed_cases", "inputs_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
