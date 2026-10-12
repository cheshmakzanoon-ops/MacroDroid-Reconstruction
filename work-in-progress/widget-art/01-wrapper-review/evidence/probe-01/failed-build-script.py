#!/usr/bin/env python3
"""Compile a standalone reflection-only Widget ART probe and bind both APKs.

No application or Android host stubs are compilation inputs. No Android device
is accessed. The generated DEX is a standalone tool, never an APK build input.
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
import time
import zipfile


ROOT = Path(__file__).resolve().parent
ORIGINAL_SHA256 = "84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800"
CANDIDATE_SHA256 = "b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f"
ORIGINAL_BYTES = 95_725_918
CANDIDATE_BYTES = 94_683_439
ORIGINAL_CLASS_SHA256 = "3ad59b363eaf1f1816d31a951867dcbf202702152148f6404d3426a8ed68818d"
ORIGINAL_METHOD_SHA256 = "a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34"
TOOL_JAR_SHA256 = "354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e"
PROBE_CLASS = "Lrecovered/probe/WidgetMethodProbe;"
MAIN_CLASS = "recovered.probe.WidgetMethodProbe"
TARGET_METHOD = "Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;"
CASES = [
    "fresh-empty-unit-identity", "reused-label-zero-empty", "resumed-label-two-empty",
    "invalid-label-exact-exception", "label-two-dead-cast-L7", "label-two-dead-cast-L4",
    "label-two-dead-cast-L1", "null-list-exception-type",
]
EXPECTED_STDOUT = ["WIDGET_ART_CASE_OK " + case for case in CASES] + ["WIDGET_METHOD_ART_OK cases=8"]


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--original-apk", required=True, type=Path)
    parser.add_argument("--candidate-apk", required=True, type=Path)
    parser.add_argument("--jdk", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk.resolve())
    env["PATH"] = str(args.jdk.resolve() / "bin") + os.pathsep + env.get("PATH", "")
    report = {
        "status": "RUNNING", "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Reflection-only standalone probe compilation and APK identity binding; no ART execution",
        "android_executed": False, "app_apk_modified": False, "app_installed": False,
        "target_method": TARGET_METHOD, "runtime_cases": CASES, "commands": [],
    }

    def save() -> None:
        (output / "build-result.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label: str, argv: list[str | Path]) -> None:
        command = [str(item) for item in argv]
        started = time.monotonic()
        try:
            result = subprocess.run(command, cwd=output, env=env, capture_output=True, timeout=180)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as failure:
            code, stdout, stderr = 124, failure.stdout or b"", failure.stderr or b""
        out = output / (label + ".stdout.txt")
        err = output / (label + ".stderr.txt")
        out.write_bytes(stdout)
        err.write_bytes(stderr)
        report["commands"].append({"label": label, "argv": command, "returncode": code,
                                   "timeout_seconds": 180, "elapsed_seconds": round(time.monotonic() - started, 3),
                                   "stdout": {"path": out.name, "bytes": len(stdout), "sha256": sha(out)},
                                   "stderr": {"path": err.name, "bytes": len(stderr), "sha256": sha(err)}})
        save()
        if code != 0:
            raise RuntimeError("Probe build command failed: " + label)

    save()
    try:
        apk_inputs = {}
        for key, path, expected, size in (
            ("original", args.original_apk.resolve(), ORIGINAL_SHA256, ORIGINAL_BYTES),
            ("candidate", args.candidate_apk.resolve(), CANDIDATE_SHA256, CANDIDATE_BYTES),
        ):
            if path.stat().st_size != size or sha(path) != expected:
                raise RuntimeError("Pinned " + key + " APK differs")
            with zipfile.ZipFile(path) as stream:
                names = stream.namelist()
                if len(names) != len(set(names)) or "classes.dex" not in names:
                    raise RuntimeError("Invalid APK DEX classpath structure")
            apk_inputs[key] = {"path": str(path), "bytes": size, "sha256": expected}
        report["apks"] = apk_inputs
        preserved = project / "source/smali/classes/67/WidgetUpdateManager_6791e8994482f6df.smali"
        if sha(preserved) != ORIGINAL_CLASS_SHA256:
            raise RuntimeError("Preserved original Widget class differs")
        signature = TARGET_METHOD.split("->", 1)[1]
        blocks = re.findall(r"^\.method [^\n]*\n.*?^\.end method", preserved.read_text(), re.M | re.S)
        selected = [block for block in blocks if block.splitlines()[0].split()[-1] == signature]
        if len(selected) != 1 or hashlib.sha256(selected[0].encode()).hexdigest() != ORIGINAL_METHOD_SHA256:
            raise RuntimeError("Preserved target method differs")
        (output / "original-widget-method.smali").write_text(selected[0])
        report["original_method_sha256"] = ORIGINAL_METHOD_SHA256
        source = ROOT / "source/recovered/probe/WidgetMethodProbe.java"
        source_copy = output / "source/recovered/probe/WidgetMethodProbe.java"
        source_copy.parent.mkdir(parents=True)
        shutil.copyfile(source, source_copy)
        if sha(source_copy) != sha(source) or source_copy.stat().st_ino == source.stat().st_ino:
            raise RuntimeError("Probe source copy changed or is hardlinked")
        report["source"] = {"path": str(source), "copied_path": str(source_copy), "sha256": sha(source_copy)}
        jar = project / "tools/lib/jadx-r2721.4574686-all.jar"
        if sha(jar) != TOOL_JAR_SHA256:
            raise RuntimeError("D8/baksmali tool JAR differs")
        report["tool_jar"] = {"path": str(jar), "sha256": sha(jar)}
        classes = output / "classes"
        classes.mkdir()
        run("javac", ["javac", "--release", "8", "-g:none", "-d", classes, source_copy])
        compiled = sorted(classes.rglob("*.class"))
        if [p.relative_to(classes).as_posix() for p in compiled] != ["recovered/probe/WidgetMethodProbe.class"]:
            raise RuntimeError("Unexpected additional compiled probe classes")
        inputs = output / "probe-inputs.jar"
        with zipfile.ZipFile(inputs, "w") as stream:
            stream.write(compiled[0], "recovered/probe/WidgetMethodProbe.class")
        dex = output / "dex"
        dex.mkdir()
        run("d8", ["java", "-cp", jar, "com.android.tools.r8.D8", "--release", "--no-desugaring",
                   "--min-api", "23", "--output", dex, inputs])
        if [p.name for p in dex.iterdir()] != ["classes.dex"]:
            raise RuntimeError("Probe must emit exactly one DEX")
        smali = output / "smali"
        run("disassemble", ["java", "-cp", jar, "com.android.tools.smali.baksmali.Main", "d",
                            "--api", "23", "--use-locals", "-o", smali, dex / "classes.dex"])
        disassembled = list(smali.rglob("*.smali"))
        if len(disassembled) != 1:
            raise RuntimeError("Unexpected runtime definition or host stub in probe DEX")
        body = disassembled[0].read_text()
        if body.splitlines()[0] != ".class public final " + PROBE_CLASS:
            raise RuntimeError("Wrong standalone probe class")
        referenced_types = sorted(set(re.findall(r"L[^;\s\"']+;", body)))
        unexpected = [name for name in referenced_types if not name.startswith("Ljava/") and name != PROBE_CLASS]
        if unexpected:
            raise RuntimeError("Probe directly references non-JDK, non-probe classes: " + repr(unexpected))
        probe = output / "widget-method-probe.dex"
        shutil.copyfile(dex / "classes.dex", probe)
        roundtrip = output / "roundtrip.dex"
        run("reassemble", ["java", "-cp", jar, "com.android.tools.smali.smali.Main", "a", "--api", "23",
                            "-o", roundtrip, smali])
        roundtrip_smali = output / "roundtrip-smali"
        run("roundtrip-disassemble", ["java", "-cp", jar, "com.android.tools.smali.baksmali.Main", "d",
                                      "--api", "23", "--use-locals", "-o", roundtrip_smali, roundtrip])
        restored = list(roundtrip_smali.rglob("*.smali"))
        if len(restored) != 1 or restored[0].read_text() != body:
            raise RuntimeError("Standalone probe DEX roundtrip changed its instructions")
        probe_info = {"path": str(probe), "bytes": probe.stat().st_size, "sha256": sha(probe),
                      "runtime_class_count": 1, "runtime_class": PROBE_CLASS,
                      "android_or_application_host_stub_definitions": 0,
                      "direct_android_or_application_type_references": 0,
                      "typed_references": referenced_types}
        provenance = {
            "schema_version": 1, "main_class": MAIN_CLASS, "probe": probe_info,
            "apks": apk_inputs, "target_method": TARGET_METHOD,
            "original_method_sha256": ORIGINAL_METHOD_SHA256,
            "candidate_helper_sha256": "dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79",
            "runtime_cases": CASES, "expected_stdout_lines": EXPECTED_STDOUT,
            "scope": "Eight service-free entry/restoration/type-check paths using real APK classes; no nonempty-widget or rendering-path claim",
            "android_runtime_executed_during_preparation": False,
        }
        (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        report.update(probe=probe_info, source_unchanged=sha(source) == sha(source_copy),
                      apks_unchanged=all(sha(Path(row["path"])) == row["sha256"] for row in apk_inputs.values()),
                      disassembled_roundtrip_byte_identical=True, expected_stdout_lines=EXPECTED_STDOUT,
                      provenance_sha256=sha(output / "provenance.json"))
        report["passed"] = report["source_unchanged"] and report["apks_unchanged"]
        report["status"] = "STANDALONE_PROBE_COMPILED_AND_BOUND_ART_NOT_EXECUTED"
    except Exception as failure:
        report["passed"] = False
        report["status"] = "PROBE_PREPARATION_FAILED"
        report["error"] = type(failure).__name__ + ": " + str(failure)
    report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save()
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
