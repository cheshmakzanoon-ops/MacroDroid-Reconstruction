#!/usr/bin/env python3
"""Create a private Widget candidate from exact published inputs and frozen proof.

Only this private candidate is edited. The uploaded APK supplies a test-only
original-method fixture and is never a build input. All source copies are hashed,
mutable inputs are not hardlinked, and failures retain their own result/logs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

BASE_PIN = "19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183"
BASE_MANIFEST = "713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883"
WIDGET_CHECKPOINT = "c448b645b27f98918fab3369d9b72a408a0a16cab217f8684f2733247b6a8b1b"
ORACLE_CHECKPOINT = "8029598a231875b00c11f9a78be92c8ceb13b0b0618989babd1333705315ed28"
ORIGINAL_APK = "84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800"
UI_BASE = "19801e55118a23ce12218f77a162e61300bb044036c8fc1b9356cb2898911779"


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def record(path):
    return {"bytes": path.stat().st_size, "sha256": sha(path)}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def copy_checked(source, destination, expected=None):
    require(source.is_file() and not source.is_symlink(), "Invalid source input: " + str(source))
    before = record(source)
    if expected is not None:
        require(before["sha256"] == expected["sha256"] and before["bytes"] == expected.get("size", expected.get("bytes")),
                "Source differs from pinned input: " + str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    require(record(destination) == before and record(source) == before, "Input changed while copying: " + str(source))
    require(source.stat().st_ino != destination.stat().st_ino or source.stat().st_dev != destination.stat().st_dev,
            "Mutable source was hardlinked: " + str(source))
    return before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--widget", type=Path, required=True)
    parser.add_argument("--original-apk", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.project, args.widget, args.original_apk, args.jdk, args.output = [
        value.resolve() for value in (args.project, args.widget, args.original_apk, args.jdk, args.output)]
    args.output.mkdir(parents=True, exist_ok=False)
    result = {"status": "PREPARING", "passed": False, "started_utc": now(), "commands": [],
              "scope": "Private Widget source preparation and D8/static/linkage prerequisites; no APK or Android claim"}
    resultpath = args.output / "preparation.json"
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk)
    env["PATH"] = str(args.jdk / "bin") + os.pathsep + env.get("PATH", "")

    def command(label, argv, cwd, timeout=1200):
        log = args.output / (label + ".log")
        value = {"label": label, "argv": list(map(str, argv)), "cwd": str(cwd), "started_utc": now(), "timeout_seconds": timeout}
        started = time.monotonic()
        with log.open("wb") as stream:
            stream.write(("COMMAND: " + json.dumps(value["argv"]) + "\n").encode())
            stream.flush()
            try:
                completed = subprocess.run(value["argv"], cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
                value["returncode"] = completed.returncode
                value["timed_out"] = False
            except subprocess.TimeoutExpired:
                value["returncode"] = None
                value["timed_out"] = True
        value.update(finished_utc=now(), elapsed_seconds=round(time.monotonic()-started, 6), log={"path": log.name, **record(log)})
        result["commands"].append(value)
        write(resultpath, result)
        require(value["returncode"] == 0 and not value["timed_out"], "Preparation command failed: " + label)

    try:
        baseline = args.project / "reports/release-input-snapshot.json"
        require(sha(baseline) == BASE_MANIFEST, "Active input manifest is not the reviewed published version")
        pin = json.loads(baseline.read_text())
        canonical = json.dumps(pin["entries"], sort_keys=True, separators=(",", ":")).encode()
        require(pin["snapshot_sha256"] == BASE_PIN and hashlib.sha256(canonical).hexdigest() == BASE_PIN and pin["files"] == len(pin["entries"]) == 81245,
                "Baseline canonical manifest is inconsistent")
        require(sha(args.original_apk) == ORIGINAL_APK, "Wrong supplied original APK")
        widget = args.widget / "checkpoints/04-original-jvm"
        oracle = args.widget / "checkpoints/05-oracle-regression"
        require(sha(widget / "checkpoint.json") == WIDGET_CHECKPOINT, "Widget checkpoint changed")
        require(sha(oracle / "checkpoint.json") == ORACLE_CHECKPOINT, "Oracle checkpoint changed")
        widgetmanifest = json.loads((widget / "checkpoint.json").read_text())
        oraclemanifest = json.loads((oracle / "checkpoint.json").read_text())
        for folder, manifest in ((widget, widgetmanifest), (oracle, oraclemanifest)):
            for entry in manifest["files"]:
                path = folder / entry["path"]
                require(record(path) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}, "Frozen checkpoint member changed: " + str(path))
        private = Path(tempfile.mkdtemp(prefix="macrodroid-widget-signed-")) / "MacroDroid_v9"
        private.mkdir()
        result.update(private_project=str(private), baseline_project=str(args.project), baseline_input_pin=BASE_PIN,
                      baseline_manifest_sha256=BASE_MANIFEST, widget_checkpoint_sha256=WIDGET_CHECKPOINT,
                      oracle_checkpoint_sha256=ORACLE_CHECKPOINT, original_apk={"path": str(args.original_apk), **record(args.original_apk)})
        write(resultpath, result)
        total = 0
        for relative, expected in pin["entries"].items():
            path = Path(relative)
            require(not path.is_absolute() and ".." not in path.parts, "Invalid pinned relative path")
            copy_checked(args.project / path, private / path, expected)
            total += expected["size"]
        # Documentation is outside build inputs; preserve the visible baseline copy.
        docs = []
        for source in sorted(args.project.glob("*.md")):
            docs.append({"path": source.name, **copy_checked(source, private / source.name)})
        result["source_copy"] = {"files": len(pin["entries"]), "bytes": total, "all_source_and_destination_hashes_verified": True,
                                 "hardlinked_inputs": 0, "generated_caches_copied": 0, "documentation": docs}
        require(sha(private / "tests/java/UiParityTests.java") == UI_BASE, "Widget UI patch baseline is different")
        selected = [entry for entry in widgetmanifest["files"]
                    if entry["path"].startswith(("source/java/", "test-support/java/"))
                    or entry["path"] in ("tests/java/BytecodeOracle.java", "tests/java/UiParityTests.java", "tests/java/WidgetParityCases.java")]
        overlays = []
        for entry in selected:
            destination = private / entry["path"]
            previous = record(destination) if destination.exists() else None
            copied = copy_checked(widget / entry["path"], destination, entry)
            overlays.append({"path": entry["path"], "before": previous, "after": copied, "source_checkpoint": WIDGET_CHECKPOINT})
        for relative in ["tests/java/ConstructorOracleConformance.java", "tests/java/WidgetOracleOpcodeConformance.java",
                         "tests/fixtures/constructor-owner-opcodes.smali", "tests/fixtures/widget-bitwise-opcodes.smali"]:
            entry = next(item for item in oraclemanifest["files"] if item["path"] == relative)
            copied = copy_checked(oracle / relative, private / relative, entry)
            overlays.append({"path": relative, "before": None, "after": copied, "source_checkpoint": ORACLE_CHECKPOINT})
        proposed = json.loads((widget / "proposed-method-entry.json").read_text())
        key = proposed["target"] + "->" + proposed["method"]
        for relative, count in [("source/java-method-map.json", 1240), ("source/ui-methods.json", 8)]:
            path = private / relative
            before = record(path)
            entries = json.loads(path.read_text())
            require(len(entries) == count and all(item["target"] + "->" + item["method"] != key for item in entries), "Unexpected registry before Widget registration")
            entries.append(proposed)
            path.write_text(json.dumps(entries, indent=2) + "\n")
            overlays.append({"path": relative, "before": before, "after": record(path), "operation": "Append exactly one frozen Widget entry"})
        path = private / "tests/test_build.py"
        text = path.read_text()
        before = record(path)
        for old, new in [
            ("def test_registry_count(self):self.assertEqual(len(self.registry),1240)",
             "def test_registry_count(self):self.assertEqual(len(self.registry),1241)"),
            ("def test_registered_classes_count(self):self.assertEqual(len({e['target'] for e in self.registry}),603)",
             "def test_registered_classes_count(self):self.assertEqual(len({e['target'] for e in self.registry}),604)"),
            ("self.assertEqual(p['methods'],1240)", "self.assertEqual(p['methods'],1241)"),
        ]:
            require(text.count(old) == 1, "Unexpected common registry/fixture-count test baseline")
            text = text.replace(old, new)
        path.write_text(text)
        overlays.append({"path": "tests/test_build.py", "before": before, "after": record(path), "operation": "Require the exact new 1,241-method / 604-class registry and fixture inventory"})
        path = private / "tests/test_v9.py"
        old = "def test_exact_eight_methods_and_classes(self):self.assertEqual((len(self.entries),len({e['target'] for e in self.entries})),(8,8))"
        new = "def test_exact_nine_methods_and_classes(self):self.assertEqual((len(self.entries),len({e['target'] for e in self.entries})),(9,9))"
        text = path.read_text()
        require(text.count(old) == 1, "Unexpected UI registry-count test baseline")
        before = record(path)
        path.write_text(text.replace(old, new))
        overlays.append({"path": "tests/test_v9.py", "before": before, "after": record(path), "operation": "Require exactly 9 registered UI methods and classes"})
        path = private / "test.py"
        text = path.read_text()
        anchor = "    apk=None\n"
        require(text.count(anchor) == 1, "Unexpected test driver baseline")
        addition = '''    # These fixtures take explicit DEX/report paths, not the app root used above.
    # The constructor reflection adapter remains host-only; ART proof is separate.
    for fixture, output, mainclass, stem, expected_cases in [
        ('constructor-owner-opcodes.smali','constructor-owner-opcodes.dex','ConstructorOracleConformance','constructor-oracle',16),
        ('widget-bitwise-opcodes.smali','widget-bitwise-opcodes.dex','WidgetOracleOpcodeConformance','widget-bitwise-oracle',4546)]:
        fixture_path=build.ROOT/'tests/fixtures'/fixture
        dex_path=build.WORK/output
        report_path=build.REPORTS/(stem+'-conformance.json')
        report_path.unlink(missing_ok=True)
        build.java('com.android.tools.smali.smali.Main','a','--api','23','-o',dex_path,fixture_path,log=stem+'-assemble.log')
        build.run(['java','-Xmx500m','-cp',cp,mainclass,dex_path,report_path],stem+'-run.log')
        conformance=json.loads(report_path.read_text())
        if conformance.get('passed') is not True or type(conformance.get('cases')) is not int or conformance['cases']!=expected_cases or conformance.get('androidRuntime') is not False:
            raise RuntimeError('Incomplete explicit host conformance: '+stem)
        conformance.update(fixtureSourceSha256=hashlib.sha256(fixture_path.read_bytes()).hexdigest(),fixtureDexSha256=hashlib.sha256(dex_path.read_bytes()).hexdigest())
        report_path.write_text(json.dumps(conformance,indent=2)+'\\n')
'''
        before = record(path)
        path.write_text(text.replace(anchor, addition + anchor))
        overlays.append({"path": "test.py", "before": before, "after": record(path), "operation": "Execute pinned constructor and numeric conformance with fresh explicit report gates"})
        result["overlays"] = overlays
        write(resultpath, result)
        command("bootstrap-extractor", [sys.executable, "-c", "import build; build.bootstrap()"], private)
        command("extract-full-original-fixture", [args.jdk / "bin/java", "-Xmx1200m", "-cp", os.pathsep.join(map(str, [private / "tools/lib/jadx-r2721.4574686-all.jar", private / "tools/classes"])),
                                                 "ExtractOracle", private, args.original_apk], private)
        result["full_original_fixture"] = {"path": "tests/fixtures/original-methods.dex", **record(private / "tests/fixtures/original-methods.dex"), "test_only_not_apk_input": True}
        extraction = (args.output / "extract-full-original-fixture.log").read_text()
        require("Test-only original fixture: classes=604 methods=1241" in extraction, "Fresh extractor inventory differs from the registered fixture")
        provenance_path = private / "tests/fixtures/provenance.json"
        previous = record(provenance_path)
        provenance = json.loads(provenance_path.read_text())
        require(provenance["original_apk_sha256"] == ORIGINAL_APK and provenance["methods"] == 1240 and provenance["classes"] == 603,
                "Unexpected original fixture provenance baseline")
        provenance.update(fixture_sha256=result["full_original_fixture"]["sha256"], fixture_bytes=result["full_original_fixture"]["bytes"],
                          methods=1241, classes=604,
                          extraction="ExtractOracle executed against the unchanged original upload; exact registered WidgetUpdateManager.m added to the published 1,240-method fixture")
        write(provenance_path, provenance)
        overlays.append({"path": "tests/fixtures/provenance.json", "before": previous, "after": record(provenance_path),
                         "operation": "Bind the actually extracted full original fixture hash, size and inventory"})
        command("pin-private-inputs", [sys.executable, "release_integrity.py", "record"], private)
        candidate_pin = json.loads((private / "reports/release-input-snapshot.json").read_text())
        old, new = pin["entries"], candidate_pin["entries"]
        result["candidate_inputs"] = {key: value for key, value in candidate_pin.items() if key != "entries"}
        result["input_delta"] = {"added": sorted(new.keys()-old.keys()), "removed": sorted(old.keys()-new.keys()), "changed": sorted(key for key in old.keys() & new.keys() if old[key] != new[key])}
        expected_delta = {entry["path"] for entry in overlays} | {"tests/fixtures/original-methods.dex"}
        actual_delta = set(result["input_delta"]["added"] + result["input_delta"]["changed"])
        require(not result["input_delta"]["removed"] and actual_delta == expected_delta, "Candidate input delta contains an unreviewed path")
        write(resultpath, result)
        command("compile-widget-d8", [sys.executable, "-c", "import build; build.compile_java()"], private)
        command("widget-static-migration", [sys.executable, "validate_migration.py"], private)
        command("widget-linkage", [sys.executable, "linkage_verify.py"], private)
        result.update(status="PRIVATE_WIDGET_D8_STATIC_LINKAGE_PASSED", passed=True)
    except BaseException as error:
        result.update(status="PRIVATE_WIDGET_PREPARATION_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now()
        write(resultpath, result)
        print(json.dumps({key: result.get(key) for key in ("status", "passed", "private_project", "candidate_inputs", "error")}, indent=2))


if __name__ == "__main__":
    main()
