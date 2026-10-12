#!/usr/bin/env python3
"""Prepare a reviewable union of two isolated recoveries without changing the app.

The output is a small inactive source overlay. The full original fixture must be
extracted again after applying it to a fresh, fully verified project copy.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

BASE_PIN = "19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183"
BASE_MANIFEST = "713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883"
WIDGET_CHECKPOINT = "c448b645b27f98918fab3369d9b72a408a0a16cab217f8684f2733247b6a8b1b"
WIDGET_D8 = "2c5557427602bac7d3154d17f127499e8f785cd9f5a0dd73c299d3e6854f938b"
ORACLE_CHECKPOINT = "8029598a231875b00c11f9a78be92c8ceb13b0b0618989babd1333705315ed28"
UPLOAD_CHECKPOINT = "9d7e23db50e3fa9e478ca0c1a37589454a5e8939193214974085a1340d6139f9"
UI_BASE = "19801e55118a23ce12218f77a162e61300bb044036c8fc1b9356cb2898911779"


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def identity(path):
    return {"bytes": path.stat().st_size, "sha256": sha(path)}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def load_checkpoint(root, digest):
    require(sha(root / "checkpoint.json") == digest, "Wrong checkpoint identity: " + str(root))
    value = json.loads((root / "checkpoint.json").read_text())
    for row in value["files"]:
        require(identity(root / row["path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]},
                "Frozen checkpoint member differs: " + row["path"])
    return value


def replace_once(text, old, new, label):
    require(text.count(old) == 1, "Unexpected merge anchor: " + label)
    return text.replace(old, new)


def controls(text):
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "CONTROLS" for t in n.targets))
    return ast.literal_eval(node.value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--widget", required=True, type=Path)
    parser.add_argument("--upload", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.base, args.widget, args.upload, args.output = [
        p.resolve() for p in (args.base, args.widget, args.upload, args.output)]
    args.output.mkdir(parents=True, exist_ok=False)
    project = args.output / "project"
    result = {"status": "PREPARING_INACTIVE_MERGE", "passed": False,
              "started_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Small source overlay only; no build, combined parity or Android claim",
              "application_modified": False, "files": [], "merge_operations": []}
    try:
        require(sha(args.base / "reports/release-input-snapshot.json") == BASE_MANIFEST,
                "Unexpected active input manifest")
        base = json.loads((args.base / "reports/release-input-snapshot.json").read_text())
        require(base["snapshot_sha256"] == BASE_PIN and base["files"] == len(base["entries"]) == 81245
                and hashlib.sha256(json.dumps(base["entries"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == BASE_PIN,
                "Invalid baseline canonical pin")
        result["baseline"] = {"input_pin": BASE_PIN, "manifest_sha256": BASE_MANIFEST,
                              "files": 81245, "verification_scope": "Manifest plus every overlaid baseline file; fresh whole-copy verification is pending"}
        wroot = args.widget / "checkpoints/04-original-jvm"
        oroot = args.widget / "checkpoints/05-oracle-regression"
        droot = args.widget / "checkpoints/06-d8-prerequisites"
        kroot = args.upload / "checkpoints/02-original-jvm"
        w = load_checkpoint(wroot, WIDGET_CHECKPOINT)
        o = load_checkpoint(oroot, ORACLE_CHECKPOINT)
        d = load_checkpoint(droot, WIDGET_D8)
        k = load_checkpoint(kroot, UPLOAD_CHECKPOINT)
        result["input_checkpoints"] = {
            "widget": WIDGET_CHECKPOINT, "widget_d8": WIDGET_D8,
            "oracle_regression": ORACLE_CHECKPOINT, "plugin_upload": UPLOAD_CHECKPOINT}
        baseline_files = {}

        def base_identity(relative):
            source = args.base / relative
            expected = base["entries"].get(relative)
            if expected is None:
                require(not source.exists(), "Unpinned baseline file exists: " + relative)
                baseline_files[relative] = None
                return None
            observed = identity(source)
            require(observed == {"bytes": expected["size"], "sha256": expected["sha256"]},
                    "Baseline source changed: " + relative)
            baseline_files[relative] = observed
            return observed

        def copy(source, relative, checkpoint):
            require(not (project / relative).exists(), "Overlapping overlay requires explicit merge: " + relative)
            previous = base_identity(relative)
            before = identity(source)
            dest = project / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
            require(identity(source) == before == identity(dest), "Copy changed input: " + relative)
            result["merge_operations"].append({"path": relative, "operation": "copy exact checkpoint file",
                                                "source_checkpoint": checkpoint, "before": previous, "after": before})

        for row in w["files"]:
            relative = row["path"]
            if relative.startswith(("source/java/", "test-support/java/")) or relative in (
                    "tests/java/BytecodeOracle.java", "tests/java/WidgetParityCases.java"):
                copy(wroot / relative, relative, WIDGET_CHECKPOINT)
        for relative in ("tests/java/ConstructorOracleConformance.java", "tests/java/WidgetOracleOpcodeConformance.java",
                         "tests/fixtures/constructor-owner-opcodes.smali", "tests/fixtures/widget-bitwise-opcodes.smali"):
            require(any(row["path"] == relative for row in o["files"]), "Missing conformance checkpoint member")
            copy(oroot / relative, relative, ORACLE_CHECKPOINT)
        require(any(row["path"] == "project/test.py" for row in d["files"]), "Missing reviewed explicit conformance driver")
        copy(droot / "project/test.py", "test.py", WIDGET_D8)
        for row in k["files"]:
            relative = row["path"]
            if relative.startswith(("source/java/", "test-support/java/")) or relative == "tests/java/PluginUploadParityCases.java":
                previous = base_identity(relative)
                require((previous or {}).get("sha256") == row["baseline_sha256"],
                        "Plugin input has a different reviewed baseline: " + relative)
                copy(kroot / relative, relative, UPLOAD_CHECKPOINT)

        relative = "tests/java/UiParityTests.java"
        require(base_identity(relative)["sha256"] == UI_BASE, "Wrong shared UI baseline")
        ui = (wroot / relative).read_text()
        merge = subprocess.run(["git", "merge-file", "-p", str(wroot / relative), str(args.base / relative), str(kroot / relative)],
                               capture_output=True, text=True)
        require(0 <= merge.returncode <= 127, "Three-way merge command failed")
        (args.output / "ui-three-way-unresolved.txt").write_text(merge.stdout)
        (args.output / "ui-three-way-stderr.txt").write_text(merge.stderr)
        operations = [
            ("PluginParityCases.current=null;WidgetControl.reset();", "PluginParityCases.current=null;PluginUploadControl.reset();PluginUploadParityCases.current=null;WidgetControl.reset();", "reset both controls"),
            ("key.equals(WidgetParityCases.KEY)?WidgetParityCases.execute(path,args):call(key,path,args)",
             "key.equals(PluginUploadParityCases.KEY)?PluginUploadParityCases.execute(path,args):key.equals(WidgetParityCases.KEY)?WidgetParityCases.execute(path,args):call(key,path,args)", "dispatch both methods"),
            ("if(key.equals(PluginParityCases.KEY))PluginControl.returned=value;", "if(key.equals(PluginParityCases.KEY)||key.equals(PluginUploadParityCases.KEY))PluginControl.returned=value;", "observe upload return"),
            ("if(key.equals(PluginParityCases.KEY))PluginControl.escaped=e;", "if(key.equals(PluginParityCases.KEY)||key.equals(PluginUploadParityCases.KEY))PluginControl.escaped=e;", "observe upload escape"),
            ("if(key.equals(WidgetParityCases.KEY))WidgetParityCases.observe(args,result);", "if(key.equals(PluginUploadParityCases.KEY))PluginUploadParityCases.observe(args,result);\n        if(key.equals(WidgetParityCases.KEY))WidgetParityCases.observe(args,result);", "observe both states"),
            ("SceneParityCases.run();PluginParityCases.run();", "SceneParityCases.run();PluginParityCases.run();PluginUploadParityCases.run();", "run both case families"),
            ("pluginBranchesCovered=false,widgetBranchesCovered=", "pluginBranchesCovered=false,uploadBranchesCovered=false,widgetBranchesCovered=", "track both branch gates"),
            ("if(key.equals(WidgetParityCases.KEY))widgetBranchesCovered=unseen.isEmpty()&&missingEdges.isEmpty();", "if(key.equals(PluginUploadParityCases.KEY))uploadBranchesCovered=unseen.isEmpty()&&missingEdges.isEmpty();\n            if(key.equals(WidgetParityCases.KEY))widgetBranchesCovered=unseen.isEmpty()&&missingEdges.isEmpty();", "calculate both coverage gates"),
            ("report.addProperty(\"widgetInstructionAndConditionalCoverage\",widgetBranchesCovered);", "report.addProperty(\"pluginUploadInstructionAndConditionalCoverage\",uploadBranchesCovered);\n        report.addProperty(\"pluginUploadInvalidLabelReturnUsesInjectedReturningBoundary\",true);\n        report.addProperty(\"widgetInstructionAndConditionalCoverage\",widgetBranchesCovered);", "report both coverage gates"),
            ("!pluginBranchesCovered||!widgetBranchesCovered)", "!pluginBranchesCovered||!uploadBranchesCovered||!widgetBranchesCovered)", "require both coverage gates"),
        ]
        for old, new, label in operations:
            ui = replace_once(ui, old, new, label)
        require("<<<<<<<" not in ui and "NoSuchElementException" in ui and "IllegalArgumentException" in ui,
                "Incomplete shared UI resolution")
        (project / relative).parent.mkdir(parents=True, exist_ok=True)
        (project / relative).write_text(ui)
        (args.output / "ui-union.patch").write_text("".join(difflib.unified_diff((args.base / relative).read_text().splitlines(True),
                                                                                ui.splitlines(True), fromfile="a/"+relative, tofile="b/"+relative)))
        result["merge_operations"].append({"path": relative, "operation": "reviewed exact-anchor union",
                                           "three_way_returncode": merge.returncode, "resolved_anchors": [x[2] for x in operations],
                                           "before": baseline_files[relative], "after": identity(project / relative)})

        proposal = json.loads((wroot / "proposed-method-entry.json").read_text())
        for relative, expected in (("source/java-method-map.json", 1240), ("source/ui-methods.json", 8)):
            base_identity(relative)
            original = json.loads((args.base / relative).read_text())
            upload = json.loads((kroot / relative).read_text())
            require(len(original) == expected and len(upload) == expected + 1 and upload[:-1] == original,
                    "Plugin registry change is not an exact one-entry append")
            merged = original + [upload[-1], proposal]
            keys = [entry["target"] + "->" + entry["method"] for entry in merged]
            require(len(set(keys)) == len(keys), "Merged registry duplicates a method")
            write_json(project / relative, merged)
            result["merge_operations"].append({"path": relative, "operation": "append exact plugin and Widget entries",
                                               "count": len(merged), "after": identity(project / relative)})

        for relative, replacements in (
            ("tests/test_build.py", [
                ("len(self.registry),1240)", "len(self.registry),1242)"),
                ("len({e['target'] for e in self.registry}),603)", "len({e['target'] for e in self.registry}),605)"),
                ("self.assertEqual(p['methods'],1240)", "self.assertEqual(p['methods'],1242)")]),
            ("tests/test_v9.py", [("def test_exact_eight_methods_and_classes(self):self.assertEqual((len(self.entries),len({e['target'] for e in self.entries})),(8,8))",
                                   "def test_exact_ten_methods_and_classes(self):self.assertEqual((len(self.entries),len({e['target'] for e in self.entries})),(10,10))")]),
        ):
            base_identity(relative)
            content = (args.base / relative).read_text()
            for old, new in replacements:
                content = replace_once(content, old, new, relative)
            (project / relative).parent.mkdir(parents=True, exist_ok=True)
            (project / relative).write_text(content)
            result["merge_operations"].append({"path": relative, "operation": "exact combined inventory assertions",
                                               "before": baseline_files[relative], "after": identity(project / relative)})

        relative = "ui_negative_control.py"
        base_identity(relative)
        shutil.copyfile(args.base / relative, project / relative)
        applied = subprocess.run(["patch", "--batch", "--forward", "-p1", "--input", str(kroot / "merge-patches/ui-negative-control.patch")],
                                 cwd=project, capture_output=True, text=True)
        (args.output / "plugin-controls-patch.log").write_text(applied.stdout + applied.stderr)
        require(applied.returncode == 0, "Plugin control patch failed")
        merged_controls = controls((project / relative).read_text())
        require(len(merged_controls) == 54 and merged_controls[:37] == controls((args.base / relative).read_text())
                and merged_controls == controls((kroot / relative).read_text()), "Plugin control inventory changed")
        result["merge_operations"].append({"path": relative, "operation": "apply 17 plugin controls while retaining current runner",
                                           "before": baseline_files[relative], "after": identity(project / relative), "controls": 54})
        for relative, before in baseline_files.items():
            require((identity(args.base / relative) if (args.base / relative).exists() else None) == before,
                    "Baseline changed during merge preparation: " + relative)
        for path in sorted(project.rglob("*")):
            if path.is_file():
                result["files"].append({"path": path.relative_to(args.output).as_posix(), **identity(path)})
        result.update(status="INACTIVE_SOURCE_UNION_PREPARED", passed=True,
                      registry_methods=1242, registry_classes=605, ui_methods=10,
                      expected_combined_cases=193489, expected_ui_cases=23174,
                      expected_ui_independent_checks=15326,
                      pending=["integrate 24 Widget fault controls without weakening 54 existing controls",
                               "fresh complete input copy and original fixture extraction with exact provenance",
                               "combined compilation, full signed artifact checks, host parity and actual fault controls",
                               "Android Widget probe and editor journey measurements"],
                      baseline_files_rechecked=len(baseline_files), baseline_inputs_unchanged=True)
    except BaseException as error:
        result.update(status="INACTIVE_MERGE_PREPARATION_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_json(args.output / "result.json", result)


if __name__ == "__main__":
    main()
