#!/usr/bin/env python3
"""Compile deliberate Widget body faults, require original/JVM rejection, then restore.

The positive checkpoint, original fixture, oracle and host boundaries stay fixed.
Only the target helper is replaced on a private classpath. This is not APK proof.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import tempfile
import time


CHECKPOINT_SHA256 = "c448b645b27f98918fab3369d9b72a408a0a16cab217f8684f2733247b6a8b1b"
HELPER_SHA256 = "dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79"
FIXTURE_SHA256 = "21fa3b34730a902713b14ee8ada375d4fdca3edf481dc3caabcd7bd1d3f22a0a"
METHOD = "Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;"
HELPER_CLASS = "recovered.ui.WidgetUpdateMethods"
CLASSES = (
    HELPER_CLASS, "BytecodeOracle", "UiParityTests", "WidgetParityCases", "WidgetParityStudy",
    "defpackage.WidgetControl", "defpackage.zhh", "defpackage.rff", "defpackage.rjb",
    "defpackage.rx6", "com.arlosoft.macrodroid.widget.custom.b",
)


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_checked(source: Path, target: Path, digest: str | None = None) -> None:
    digest = digest or sha(source)
    if sha(source) != digest:
        raise RuntimeError("Input changed: " + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if sha(target) != digest or source.stat().st_ino == target.stat().st_ino:
        raise RuntimeError("Input copy mismatch or hardlink: " + str(source))


def files_under(root: Path) -> list[dict]:
    return [{"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
            for path in sorted(root.rglob("*")) if path.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--positive-checkpoint", required=True, type=Path)
    parser.add_argument("--tool-jar", required=True, type=Path)
    parser.add_argument("--jdk", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent
    checkpoint_root = args.positive_checkpoint.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix="macrodroid-widget-mutants-"))
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk.resolve())
    env["PATH"] = str(args.jdk.resolve() / "bin") + os.pathsep + env.get("PATH", "")
    report = {
        "status": "RUNNING", "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "private_work": str(private), "positive_checkpoint": str(checkpoint_root),
        "checkpoint_sha256": CHECKPOINT_SHA256, "scope": "One-method original DEX/JVM compiled mutants; two host paths only",
        "method": METHOD, "active_source_changed": False, "apk_built": False,
        "rebuilt_dex_compared": False, "android_executed": False, "commands": [], "controls": [],
    }

    def save() -> None:
        write_json(output / "result.json", report)

    def run(label: str, argv: list[str | Path], folder: Path, timeout: int = 180) -> dict:
        folder.mkdir(parents=True, exist_ok=True)
        log = folder / (label + ".log")
        started = time.monotonic()
        command = [str(value) for value in argv]
        with log.open("w") as stream:
            try:
                value = subprocess.run(command, cwd=private, env=env, stdout=stream,
                                       stderr=subprocess.STDOUT, timeout=timeout)
                code = value.returncode
            except subprocess.TimeoutExpired:
                stream.write("\nCONTROL_TIMEOUT: exceeded " + str(timeout) + " seconds\n")
                code = 124
        result = {"label": label, "argv": command, "returncode": code,
                  "elapsed_seconds": round(time.monotonic() - started, 3), "timeout_seconds": timeout,
                  "log": log.relative_to(output).as_posix(), "log_sha256": sha(log)}
        report["commands"].append(result)
        save()
        return result

    save()
    try:
        checkpoint_file = checkpoint_root / "checkpoint.json"
        if sha(checkpoint_file) != CHECKPOINT_SHA256:
            raise RuntimeError("Unexpected positive checkpoint identity")
        checkpoint = json.loads(checkpoint_file.read_text())
        for row in checkpoint["files"]:
            if sha(checkpoint_root / row["path"]) != row["sha256"]:
                raise RuntimeError("Frozen positive source changed: " + row["path"])
        final_root = checkpoint_root / "evidence/widget-study-04-final"
        evidence_map = {row["path"]: row for row in checkpoint["evidence_files"]}
        for name in ("study.json", "parity.json", "inputs.json", "compiled-host-harness.tar.gz"):
            relative = "widget-study-04-final/" + name
            if sha(final_root / name) != evidence_map[relative]["sha256"]:
                raise RuntimeError("Frozen positive evidence changed: " + name)
        positive_study = json.loads((final_root / "study.json").read_text())
        positive_parity = json.loads((final_root / "parity.json").read_text())
        if not (positive_study["pass"] and positive_parity["passed"] and positive_parity["cases"] == 2342
                and positive_parity["failedCases"] == 0 and positive_parity["unsupportedExecutions"] == 0
                and positive_parity["independentExpectedResultChecks"] == 198
                and positive_parity["expectedResultFailures"] == 0):
            raise RuntimeError("Positive checkpoint no longer passes its exact gate")
        jar = args.tool_jar.resolve()
        if sha(jar) != positive_study["tool_jar"]["sha256"]:
            raise RuntimeError("Tool jar differs from measured positive study")
        report["tool_jar"] = {"path": str(jar), "sha256": sha(jar)}
        copy_checked(checkpoint_root / "tests/fixtures/original-widget-method.dex", private / "original-method.dex", FIXTURE_SHA256)
        fixture = private / "original-method.dex"
        copy_checked(checkpoint_root / "proposed-method-entry.json", private / "proposed-method-entry.json")
        proposal = private / "proposed-method-entry.json"
        report["fixture"] = {"sha256": sha(fixture), "bytes": fixture.stat().st_size,
                             "provenance": "Unchanged fixture from the frozen original-APK extraction", "test_only": True}

        base = private / "positive-classes"
        base.mkdir()
        with tarfile.open(final_root / "compiled-host-harness.tar.gz", "r:gz") as stream:
            names = set()
            for member in stream.getmembers():
                relative = PurePosixPath(member.name)
                if relative.is_absolute() or ".." in relative.parts or not relative.parts \
                        or relative.parts[0] not in {"hostclasses", "harnessclasses", "toolclasses"} \
                        or member.name in names:
                    raise RuntimeError("Unsafe or duplicate class archive member")
                names.add(member.name)
                destination = base / member.name
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with destination.open("xb") as handle:
                        handle.write(stream.extractfile(member).read())
                else:
                    raise RuntimeError("Class archive has a non-file/directory member")
        host = base / "hostclasses"
        harness = base / "harnessclasses"
        fixed_inventory = files_under(base)
        write_json(output / "fixed-class-inventory.json", fixed_inventory)
        copy_checked(final_root / "compiled-host-harness.tar.gz", output / "positive-classes.tar.gz")
        copy_checked(fixture, output / "original-method.dex")
        copy_checked(proposal, output / "proposed-method-entry.json")

        authored = []
        for relative in ("widget_method_negative_control.py", "widget_method_mutants.json", "tests/java/WidgetMutationLauncher.java"):
            copy_checked(source_root / relative, output / "inputs" / relative)
            authored.append({"path": relative, "sha256": sha(output / "inputs" / relative)})
        report["authored_inputs"] = authored
        catalog = json.loads((output / "inputs/widget_method_mutants.json").read_text())
        if catalog["helper_sha256"] != HELPER_SHA256 or catalog["method"] != METHOD:
            raise RuntimeError("Mutation catalog does not identify the frozen helper")
        source = (checkpoint_root / catalog["helper_path"]).read_text()
        if hashlib.sha256(source.encode()).hexdigest() != HELPER_SHA256:
            raise RuntimeError("Positive helper source hash mismatch")
        controls = catalog["controls"]
        if len(controls) != 24 or len({row["name"] for row in controls}) != 24:
            raise RuntimeError("Expected exactly the 24 uniquely named Widget controls")
        helper_relative = Path(HELPER_CLASS.replace(".", "/") + ".class")
        positive_helper_class_sha = sha(host / helper_relative)
        report["positive_helper_source_sha256"] = HELPER_SHA256
        report["positive_helper_class_sha256"] = positive_helper_class_sha
        launcher = private / "launcherclasses"
        launcher.mkdir()
        compile_launcher = run("compile-launcher", ["javac", "-cp", os.pathsep.join(map(str, (jar, harness, host))),
                                                    "-d", launcher, output / "inputs/tests/java/WidgetMutationLauncher.java"], output)
        if compile_launcher["returncode"] != 0:
            raise RuntimeError("Origin-checking launcher did not compile")
        copy_checked(launcher / "WidgetMutationLauncher.class", output / "WidgetMutationLauncher.class")

        def origin_manifest(helper_directory: Path) -> list[dict]:
            rows = []
            for name in CLASSES:
                relative = Path(name.replace(".", "/") + ".class")
                directory = helper_directory if name == HELPER_CLASS else harness if (harness / relative).is_file() else host
                path = directory / relative
                rows.append({"class": name, "path": str(path), "sha256": sha(path)})
            return rows

        def execute(label: str, helper_directory: Path, folder: Path,
                    manifest_override: list[dict] | None = None) -> tuple[dict, dict | None]:
            folder.mkdir(parents=True, exist_ok=True)
            manifest = origin_manifest(helper_directory) if manifest_override is None else manifest_override
            write_json(folder / "expected-class-origins.json", manifest)
            cp = os.pathsep.join(map(str, (jar, launcher, helper_directory, harness, host)))
            result = run(label, ["java", "-Xmx700m", "-cp", cp, "WidgetMutationLauncher",
                                 folder / "expected-class-origins.json", folder / "class-origins.json",
                                 proposal, fixture, folder / "parity.json"], folder)
            parity_path = folder / "parity.json"
            return result, json.loads(parity_path.read_text()) if parity_path.exists() else None

        before_command, before = execute("positive-before", host, output / "positive-before")
        report["positive_before"] = {"returncode": before_command["returncode"],
                                     "exact_frozen_parity_match": before == positive_parity,
                                     "passed": before_command["returncode"] == 0 and before == positive_parity}
        save()
        if not report["positive_before"]["passed"]:
            raise RuntimeError("Positive baseline no longer exactly reproduces the frozen report")

        compiled_mutants = []
        for control in controls:
            name = control["name"]
            folder = output / "controls" / name
            folder.mkdir(parents=True)
            candidate = source
            for edit in control["edits"]:
                if candidate.count(edit["find"]) != edit["count"]:
                    raise RuntimeError("Mutation anchor count mismatch for " + name)
                candidate = candidate.replace(edit["find"], edit["replace"])
            if candidate == source:
                raise RuntimeError("Mutation made no source change: " + name)
            helper_source = private / "mutants" / name / "src/recovered/ui/WidgetUpdateMethods.java"
            helper_source.parent.mkdir(parents=True)
            helper_source.write_text(candidate)
            copy_checked(helper_source, folder / "WidgetUpdateMethods.java")
            classes = private / "mutants" / name / "classes"
            classes.mkdir()
            compilation = run("compile", ["javac", "--release", "8", "-g:none", "-Xlint:-options",
                                          "-cp", host, "-d", classes, helper_source], folder)
            result = {"name": name, "reason": control["reason"],
                      "source_sha256": sha(helper_source), "compile_returncode": compilation["returncode"],
                      "expected_failure_labels": control["expected_failure_labels"], "passed": False}
            if compilation["returncode"] == 0:
                class_file = classes / helper_relative
                if [row["path"] for row in files_under(classes)] != [helper_relative.as_posix()]:
                    raise RuntimeError("Mutant compiler emitted classes outside the one target helper")
                result["class_sha256"] = sha(class_file)
                copy_checked(class_file, folder / "WidgetUpdateMethods.class")
                executed, parity = execute("original-jvm", classes, folder)
                result["execution_returncode"] = executed["returncode"]
                if parity is not None:
                    result["cases"] = parity["cases"]
                    result["failed_cases"] = parity["failedCases"]
                    result["unsupported_executions"] = parity["unsupportedExecutions"]
                    result["expected_result_failures"] = parity["expectedResultFailures"]
                    result["failed_case_labels"] = parity["failedCaseLabels"]
                    result["named_failures_observed"] = all(label in parity["failedCaseLabels"] for label in control["expected_failure_labels"])
                    result["coverage_unchanged"] = parity["instructionCoverage"] == positive_parity["instructionCoverage"]
                    result["passed"] = (executed["returncode"] == 2 and parity["passed"] is False
                                        and parity["cases"] == 2342 and parity["paths"] == 2
                                        and parity["methodKeys"] == [METHOD] and parity["failedCases"] > 0
                                        and parity["unsupportedExecutions"] == 0 and parity["expectedResultFailures"] == 0
                                        and result["named_failures_observed"] and result["coverage_unchanged"]
                                        and result["class_sha256"] != positive_helper_class_sha)
                compiled_mutants.append((control, classes))
            report["controls"].append(result)
            write_json(folder / "result.json", result)
            save()
            print(name + ": " + ("DETECTED" if result["passed"] else "CONTROL_FAILED"), flush=True)

        origin_controls = []
        wrong_hash = origin_manifest(host)
        wrong_hash[0]["sha256"] = "0" * 64
        for name, manifest, expected_error in (
            ("reject-loaded-helper-wrong-hash", wrong_hash, "Wrong loaded class hash"),
            ("reject-baseline-shadowing-mutant", origin_manifest(compiled_mutants[0][1]), "Wrong loaded class origin"),
        ):
            folder = output / "origin-controls" / name
            command, parity = execute("execute", host, folder, manifest)
            log = (folder / "execute.log").read_text()
            passed = command["returncode"] == 1 and parity is None and expected_error in log and not (folder / "class-origins.json").exists()
            origin_controls.append({"name": name, "returncode": command["returncode"], "passed": passed,
                                    "parity_was_not_executed": parity is None, "expected_error": expected_error})
        report["class_origin_controls"] = origin_controls

        restored_source = private / "restored/src/recovered/ui/WidgetUpdateMethods.java"
        copy_checked(checkpoint_root / catalog["helper_path"], restored_source, HELPER_SHA256)
        restored = private / "restored/classes"
        restored.mkdir(parents=True)
        final_folder = output / "positive-restored"
        compilation = run("compile", ["javac", "--release", "8", "-g:none", "-Xlint:-options",
                                      "-cp", host, "-d", restored, restored_source], final_folder)
        if compilation["returncode"] != 0:
            raise RuntimeError("Exact positive source restoration did not compile")
        copy_checked(restored / helper_relative, final_folder / "WidgetUpdateMethods.class")
        after_command, after = execute("original-jvm", restored, final_folder)
        report["positive_restoration"] = {
            "returncode": after_command["returncode"], "source_sha256": sha(restored_source),
            "class_sha256": sha(restored / helper_relative), "source_matches_frozen": sha(restored_source) == HELPER_SHA256,
            "class_matches_frozen": sha(restored / helper_relative) == positive_helper_class_sha,
            "exact_frozen_parity_match": after == positive_parity,
            "passed": after_command["returncode"] == 0 and after == positive_parity
                      and sha(restored / helper_relative) == positive_helper_class_sha,
        }
        report["fixed_class_inventory_unchanged"] = files_under(base) == fixed_inventory
        report["fixture_unchanged"] = sha(fixture) == FIXTURE_SHA256
        report["frozen_source_inputs_unchanged"] = all(sha(checkpoint_root / row["path"]) == row["sha256"] for row in checkpoint["files"])
        report["authored_inputs_unchanged"] = all(sha(source_root / row["path"]) == row["sha256"] for row in authored)
        report["controls_count"] = len(report["controls"])
        report["controls_detected"] = sum(row["passed"] for row in report["controls"])
        report["passed"] = (report["controls_count"] == 24 and report["controls_detected"] == 24
                            and all(row["passed"] for row in origin_controls)
                            and report["positive_restoration"]["passed"] and report["fixed_class_inventory_unchanged"]
                            and report["fixture_unchanged"] and report["frozen_source_inputs_unchanged"]
                            and report["authored_inputs_unchanged"])
        report["status"] = "ALL_24_COMPILED_MUTANTS_DETECTED_EXACT_POSITIVE_RESTORED" if report["passed"] else "METHOD_NEGATIVE_CONTROL_GATE_FAILED"
        report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save()
        print(json.dumps({key: report[key] for key in ("status", "controls_count", "controls_detected", "positive_restoration", "passed")}, indent=2))
        return 0 if report["passed"] else 2
    except Exception as failure:
        report["status"] = "METHOD_NEGATIVE_CONTROL_RUN_FAILED"
        report["passed"] = False
        report["error"] = type(failure).__name__ + ": " + str(failure)
        report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
