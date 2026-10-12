#!/usr/bin/env python3
"""Retain the exact source union and add the measured runtime policy and 78 faults."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

from prepare_merge_overlay import BASE_PIN, controls, identity, load_checkpoint, require, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--widget", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base, widget, output = [p.resolve() for p in (args.base, args.widget, args.output)]
    source = Path(__file__).resolve().parent
    union = source / "checkpoints/01-source-union"
    policy = widget / "checkpoints/06-host-runtime-policy"
    mutants = widget / "checkpoints/04-method-mutants"
    output.mkdir(parents=True, exist_ok=False)
    project = output / "project"
    result = {"status": "PREPARING_COMBINED_CONTROL_OVERLAY", "passed": False,
              "started_utc": datetime.now(timezone.utc).isoformat(), "commands": [],
              "scope": "Inactive source/runtime/fault preparation; no combined Java compilation, fault execution or Android claim"}
    try:
        um = load_checkpoint(union, "ff2f4a55335a6efe4212b9a906bddd604368fb1fb76ff44c7b39d890359340fc")
        pm = load_checkpoint(policy, "cc68ba264c1ac530a8a0cf536ab40e391fe489c9c084c700d06a10c9d813405a")
        mm = load_checkpoint(mutants, "8cf5608ff10873eb558d74d347eb89dc7363da2ca838be78f935dca9c4927965")
        baseline = json.loads((base / "reports/release-input-snapshot.json").read_text())
        require(baseline["snapshot_sha256"] == BASE_PIN, "Different active baseline")
        result["input_checkpoints"] = {"source_union": identity(union / "checkpoint.json"),
                                       "host_runtime_policy": identity(policy / "checkpoint.json"),
                                       "widget_mutations": identity(mutants / "checkpoint.json")}
        copied = []

        def copy(path, relative, origin):
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            before = identity(path)
            old = identity(target) if target.exists() else None
            shutil.copyfile(path, target)
            require(identity(path) == before == identity(target), "Copied overlay changed")
            copied.append({"path": relative, "origin": origin, "before": old, "after": before})

        for row in um["files"]:
            if row["path"].startswith("project/"):
                copy(union / row["path"], row["path"], "source-union")
        for row in pm["files"]:
            if row["path"].startswith("project/") and row["path"] != "project/ui_negative_control.py":
                copy(policy / row["path"], row["path"], "measured-host-runtime-policy")
        for relative in ("ui_mutation_catalog.py", "tests/test_ui_mutation_catalog.py"):
            copy(source / "control-inputs" / relative, "project/" + relative, "combined-control-inputs")
        require(any(row["path"] == "widget_method_mutants.json" for row in mm["files"]), "Missing frozen Widget catalog")
        copy(mutants / "widget_method_mutants.json", "project/tests/fixtures/widget-method-mutants.json", "exact-24-compiled-mutant-catalog")
        path = project / "ui_negative_control.py"
        previous = path.read_text()
        anchor = "def sha(path:Path)->str:"
        require(previous.count(anchor) == 1 and previous.count("import build\n") == 1, "Unexpected current control runner")
        prefix = previous[:previous.index(anchor)].replace("import build\n", "import build\nimport ui_runtime_policy\nimport ui_mutation_catalog\n")
        combined = prefix + (source / "control-inputs/ui_control_runner.pyfrag").read_text()
        ast.parse(combined)
        require(controls(combined) == controls(previous) and len(controls(combined)) == 54,
                "Existing 54 control definitions changed")
        path.write_text(combined)
        (output / "ui-control-integration.patch").write_text("".join(difflib.unified_diff(previous.splitlines(True), combined.splitlines(True),
                                                                                       fromfile="a/ui_negative_control.py", tofile="b/ui_negative_control.py")))
        # Preflight every legacy anchor using the exact overlay or its pinned
        # baseline source. Actual compilation/detection remains a later gate.
        source_bindings = {}
        for name, classname, old, new, case in controls(combined):
            relative = "source/java/recovered/ui/" + classname + ".java"
            actual = project / relative if (project / relative).is_file() else base / relative
            if actual.is_relative_to(base):
                expected = baseline["entries"][relative]
                require(identity(actual) == {"bytes": expected["size"], "sha256": expected["sha256"]}, "Baseline mutation source changed")
            text = actual.read_text()
            count = text.count(old)
            require(count >= 1 and (name == "parcel-nonzero-boolean" or count == 1), "Existing mutation anchor changed: " + name)
            require(text.replace(old, new, 1) != text and case, "Existing mutation is empty")
            source_bindings[relative] = identity(actual)
        spec = importlib.util.spec_from_file_location("prepared_widget_mutations", project / "ui_mutation_catalog.py")
        catalog = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(catalog)
        jobs = catalog.load_widget_mutations(project)
        require(len(jobs) == 24, "Widget mutation preparation incomplete")
        for path in project.rglob("*.py"):
            ast.parse(path.read_text())
        log = output / "runtime-and-mutation-policy-tests.log"
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ui_*.py", "-v"]
        with log.open("w") as stream:
            stream.write("COMMAND: " + json.dumps(command) + "\n")
            stream.flush()
            done = subprocess.run(command, cwd=project, stdout=stream, stderr=subprocess.STDOUT, timeout=60)
        result["commands"].append({"argv": command, "cwd": str(project), "returncode": done.returncode, "log": identity(log)})
        require(done.returncode == 0 and "Ran 14 tests" in log.read_text(), "Runtime/mutation policy controls failed")
        result.update(status="INACTIVE_COMBINED_CONTROL_OVERLAY_PREPARED", passed=True, source_copies=copied,
                      existing_control_definitions_unchanged=54, widget_control_definitions=24, total_prepared_mutations=78,
                      policy_adversarial_tests_passed=14, mutation_source_bindings=source_bindings,
                      actual_mutants_compiled_here=0, actual_mutants_executed_here=0,
                      registered_methods=1242, registered_classes=605, ui_methods=10,
                      expected_full_python_tests=273, expected_all_cases=193489, expected_ui_cases=23174,
                      expected_ui_independent_checks=15326, active_project_changed=False,
                      pending=["fresh full source copy and combined original fixture/provenance",
                               "combined signed build and all host suites", "actual 78 fault detections and exact positive restoration",
                               "full configured acceptance and Android execution"])
        result["files"] = [{"path": p.relative_to(output).as_posix(), **identity(p)}
                           for p in sorted(project.rglob("*")) if p.is_file() and "__pycache__" not in p.parts]
    except BaseException as error:
        result.update(status="COMBINED_CONTROL_OVERLAY_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_json(output / "result.json", result)
    print(json.dumps({k: result[k] for k in ("status", "passed", "total_prepared_mutations", "policy_adversarial_tests_passed")}, indent=2))


if __name__ == "__main__":
    main()
