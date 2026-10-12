#!/usr/bin/env python3
"""Run the isolated Widget body against a freshly extracted original-APK fixture.

The project is read only. All Java inputs are copied and hash checked into a fresh
private work directory before compilation. No APK is built, installed or changed.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import time


ORIGINAL_APK_SHA256 = "84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800"
ORIGINAL_METHOD_SHA256 = "a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34"
TARGET = "Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;"
SIGNATURE = "m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;"


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--original-apk", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--jdk", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    study = Path(__file__).resolve().parent
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix="macrodroid-widget-study-"))
    commands: list[dict] = []
    inputs: list[dict] = []
    report: dict = {
        "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "RUNNING",
        "project_read_only": str(project),
        "private_work": str(private),
        "target_method": TARGET + "->" + SIGNATURE,
        "active_registry_modified": False,
        "apk_built": False,
        "android_executed": False,
        "rebuilt_dex_compared": False,
        "mutable_hardlinks": False,
        "commands": commands,
    }
    write_json(output / "study.json", report)
    env = os.environ.copy()
    if args.jdk:
        jdk = args.jdk.resolve()
        env["JAVA_HOME"] = str(jdk)
        env["PATH"] = str(jdk / "bin") + os.pathsep + env.get("PATH", "")

    def run(label: str, command: list[str | Path], timeout: int = 300, allowed=(0,)) -> int:
        started = time.monotonic()
        argv = [str(value) for value in command]
        log = output / (label + ".log")
        with log.open("w") as stream:
            try:
                result = subprocess.run(argv, cwd=private, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT, timeout=timeout)
                code = result.returncode
            except subprocess.TimeoutExpired:
                stream.write("\nSTUDY_TIMEOUT: bounded command exceeded " + str(timeout) + " seconds\n")
                code = 124
        commands.append({"label": label, "argv": argv, "returncode": code,
                         "elapsed_seconds": round(time.monotonic() - started, 3),
                         "timeout_seconds": timeout, "log": log.name, "log_sha256": sha(log)})
        write_json(output / "study.json", report)
        if code not in allowed:
            raise RuntimeError(label + " failed with exit code " + str(code))
        return code

    def copy_input(source: Path, destination: Path, origin: str, relative: str) -> Path:
        digest = sha(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        if sha(destination) != digest:
            raise RuntimeError("Copied input hash changed: " + str(source))
        inputs.append({"path": relative, "origin": origin, "source": str(source),
                       "private_copy": str(destination.relative_to(private)),
                       "bytes": destination.stat().st_size, "sha256": digest})
        return destination

    try:
        apk = args.original_apk.resolve()
        if sha(apk) != ORIGINAL_APK_SHA256:
            raise RuntimeError("Original APK hash mismatch")
        report["original_apk"] = {"path": str(apk), "bytes": apk.stat().st_size, "sha256": ORIGINAL_APK_SHA256}
        entry = json.loads((study / "proposed-method-entry.json").read_text())
        if entry.get("target") != TARGET or entry.get("method") != SIGNATURE or entry.get("original_method_sha256") != ORIGINAL_METHOD_SHA256:
            raise RuntimeError("Unexpected proposed method or hash")
        original_entries = [row for row in json.loads((project / "source/class-index.json").read_text()).values() if row["descriptor"] == TARGET]
        if len(original_entries) != 1:
            raise RuntimeError("Original class must occur in exactly one partition")
        original_class = project / original_entries[0]["path"]
        if sha(original_class) != original_entries[0]["sha256"]:
            raise RuntimeError("Preserved original class hash mismatch")
        blocks = re.findall(r"^\.method [^\n]*\n.*?^\.end method", original_class.read_text(), re.M | re.S)
        selected = [block for block in blocks if block.splitlines()[0].split()[-1] == SIGNATURE]
        if len(selected) != 1 or hashlib.sha256(selected[0].encode()).hexdigest() != ORIGINAL_METHOD_SHA256:
            raise RuntimeError("Preserved original method hash mismatch")
        (output / "original-widget-method.smali").write_text(selected[0])
        report["preserved_original"] = {"path": str(original_class), "class_sha256": sha(original_class), "method_sha256": ORIGINAL_METHOD_SHA256}

        selected_sources: dict[str, Path] = {}
        for tree in ("source/java", "test-support/java"):
            for source in (project / tree).rglob("*.java"):
                selected_sources[source.relative_to(project).as_posix()] = source
            for source in (study / tree).rglob("*.java"):
                selected_sources[source.relative_to(study).as_posix()] = source
        copied_sources = []
        for relative, source in sorted(selected_sources.items()):
            origin = "widget-overlay" if source.is_relative_to(study) else "project"
            copied_sources.append(copy_input(source, private / "inputs" / relative, origin, relative))

        harness_sources = []
        for name in ("BytecodeOracle.java", "ParityTests.java", "UiParityTests.java", "SceneParityCases.java", "PluginParityCases.java", "WidgetParityCases.java", "WidgetParityStudy.java"):
            relative = "tests/java/" + name
            source = study / relative if (study / relative).is_file() else project / relative
            origin = "widget-overlay" if source.is_relative_to(study) else "project"
            harness_sources.append(copy_input(source, private / "inputs" / relative, origin, relative))
        extractor = copy_input(project / "tools/src/ExtractOracle.java", private / "inputs/tools/src/ExtractOracle.java", "project", "tools/src/ExtractOracle.java")
        proposal = copy_input(study / "proposed-method-entry.json", private / "proposed-method-entry.json", "widget-overlay", "proposed-method-entry.json")
        jar = project / "tools/lib/jadx-r2721.4574686-all.jar"
        report["tool_jar"] = {"path": str(jar), "bytes": jar.stat().st_size, "sha256": sha(jar)}
        report["host_java_inputs"] = len(copied_sources)
        report["overlay_java_inputs"] = sum(row["origin"] == "widget-overlay" and row["path"].startswith(("source/java/", "test-support/java/")) for row in inputs)
        write_json(output / "inputs.json", {"files": inputs, "every_private_copy_hash_verified": True, "mutable_hardlinks": False})

        host = private / "hostclasses"
        harness = private / "harnessclasses"
        tools = private / "toolclasses"
        for directory in (host, harness, tools):
            directory.mkdir()
        sources_file = private / "host-sources.args"
        sources_file.write_text("".join('"' + str(path).replace("\\", "\\\\").replace('"', '\\"') + '"\n' for path in copied_sources))
        run("compile-host", ["javac", "--release", "8", "-g:none", "-Xlint:-options", "-d", host, "@" + str(sources_file)])
        run("compile-extractor", ["javac", "-cp", jar, "-d", tools, extractor])
        run("compile-harness", ["javac", "-cp", str(jar) + os.pathsep + str(host), "-d", harness, *harness_sources])
        fixture_root = private / "fixture-project"
        (fixture_root / "source").mkdir(parents=True)
        write_json(fixture_root / "source/java-method-map.json", [entry])
        run("extract-original-fixture", ["java", "-cp", str(jar) + os.pathsep + str(tools), "ExtractOracle", fixture_root, apk])
        fixture = fixture_root / "tests/fixtures/original-methods.dex"
        shutil.copyfile(fixture, output / "original-widget-method.dex")
        report["fixture"] = {"path": "original-widget-method.dex", "bytes": fixture.stat().st_size, "sha256": sha(fixture), "source_apk_sha256": ORIGINAL_APK_SHA256, "classes": 1, "methods": 1, "test_only_not_apk_input": True}
        cp = os.pathsep.join(str(path) for path in (jar, harness, host))
        code = run("original-jvm", ["java", "-Xmx1000m", "-cp", cp, "WidgetParityStudy", proposal, fixture, output / "parity.json"], allowed=(0, 2))
        parity = json.loads((output / "parity.json").read_text())
        report["parity"] = {key: value for key, value in parity.items() if key not in {"failures", "failedCaseLabels"}}
        report["pass"] = code == 0 and parity.get("passed") is True
        report["status"] = "ORIGINAL_JVM_COVERAGE_PASSED" if report["pass"] else "ORIGINAL_JVM_GATE_FAILED"
        report["copied_inputs_unchanged_after_execution"] = all(sha(private / row["private_copy"]) == row["sha256"] for row in inputs)
        if not report["copied_inputs_unchanged_after_execution"]:
            report["pass"] = False
            report["status"] = "PRIVATE_INPUTS_CHANGED"
        archive = output / "compiled-host-harness.tar.gz"
        with tarfile.open(archive, "w:gz") as stream:
            for directory in (host, harness, tools):
                stream.add(directory, arcname=directory.name)
        report["compiled_class_archive"] = {"path": archive.name, "bytes": archive.stat().st_size, "sha256": sha(archive)}
        report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        write_json(output / "study.json", report)
        print(json.dumps({"status": report["status"], "cases": parity["cases"], "failedCases": parity["failedCases"], "unsupportedExecutions": parity["unsupportedExecutions"], "coverage": parity["instructionCoverage"], "output": str(output)}, indent=2))
        return 0 if report["pass"] else 2
    except Exception as error:
        report["status"] = "STUDY_FAILED"
        report["pass"] = False
        report["error"] = type(error).__name__ + ": " + str(error)
        report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        write_json(output / "study.json", report)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
