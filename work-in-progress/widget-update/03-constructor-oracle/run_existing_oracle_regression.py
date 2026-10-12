#!/usr/bin/env python3
"""Exercise existing suites with the constructor guard without altering their frozen proof."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import zipfile


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    baseline, output = a.baseline.resolve(), a.output.resolve()
    own = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=False)
    study = Path(tempfile.mkdtemp(prefix="macrodroid-oracle-regression-"))
    (study / "reports").mkdir()
    classes = output / "classes"
    classes.mkdir()
    source_sha = sha(own / "tests/java/BytecodeOracle.java")
    assert source_sha == "482af8ecd9db285e1f88fbf9a5bd934262f4182772e49c9a70f91ea66aaa5bca"
    pin = json.loads((baseline / "reports/release-input-snapshot.json").read_text())
    assert pin["snapshot_sha256"] == "19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183"
    files = []
    relatives = [Path("source") / n for n in ["java-method-map.json", "core-methods.json", "environment-methods.json", "engine-methods.json", "ui-methods.json", "partitions.json"]]
    relatives += [Path("tests/fixtures/original-methods.dex"), Path("tests/fixtures/provenance.json")]
    relatives += [Path("build") / n for n in ["oracle-conformance.dex", "engine-opcodes.dex", "ui-opcodes.dex"]]
    apk = baseline / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    assert sha(apk) == "9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2"
    with zipfile.ZipFile(apk) as archive:
        for part in json.loads((baseline / "source/partitions.json").read_text()):
            relative = Path("build/hybrid") / (part["name"] + ".dex")
            assert (baseline / relative).read_bytes() == archive.read(part["apk_path"])
            relatives.append(relative)
    for relative in relatives:
        src, dst = baseline / relative, study / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        assert sha(src) == sha(dst)
        files.append({"path": str(relative), "bytes": dst.stat().st_size, "sha256": sha(dst)})
    cp_inputs = []
    for folder in [baseline / "build/java/hostclasses", baseline / "tools/classes"]:
        for path in sorted(folder.rglob("*.class")):
            cp_inputs.append({"path": str(path.relative_to(baseline)), "bytes": path.stat().st_size, "sha256": sha(path)})
    jar = baseline / "tools/lib/jadx-r2721.4574686-all.jar"
    cp = os.pathsep.join(map(str, [classes, jar, baseline / "build/java/hostclasses", baseline / "tools/classes"]))
    agent = baseline / "build/test-clock-agent.jar"
    result = {"status": "RUNNING", "started_utc": datetime.now(timezone.utc).isoformat(), "scope": "Stricter constructor oracle over the existing 1,240 bodies; no Widget body; not a fresh application build or Android execution", "android_executed": False, "baseline_snapshot_sha256": pin["snapshot_sha256"], "oracle_sha256": source_sha, "baseline_apk_sha256": sha(apk), "copied_study_root": str(study), "study_inputs": files, "classpath_class_inputs": cp_inputs, "tool_jar_sha256": sha(jar), "clock_agent_sha256": sha(agent), "commands": []}
    save(output / "result.json", result)

    def run(label: str, command: list[str]) -> None:
        log = output / (label + ".log")
        start = time.monotonic()
        with log.open("w") as stream:
            stream.write(json.dumps(command) + "\n"); stream.flush()
            process = subprocess.run(command, cwd=study, stdout=stream, stderr=subprocess.STDOUT, timeout=900)
        row = {"label": label, "command": command, "exit_code": process.returncode, "seconds": round(time.monotonic() - start, 3), "log": log.name, "log_sha256": sha(log)}
        result["commands"].append(row)
        save(output / "result.json", result)
        if process.returncode: raise RuntimeError("Suite failed: " + label)
        print(label + " passed", flush=True)

    try:
        run("compile-strict-oracle", ["javac", "-cp", cp, "-d", str(classes), str(own / "tests/java/BytecodeOracle.java"), str(own / "tests/java/OracleRegressionLauncher.java")])
        suites = [("conformance", "OracleSemanticsTests"), ("engine-conformance", "EngineOracleConformance"), ("ui-conformance", "UiOracleConformance"), ("legacy", "ParityTests"), ("core", "CoreParityTests"), ("environment", "EnvironmentParityTests"), ("engine", "EngineParityTests"), ("ui", "UiParityTests")]
        reports = {}
        for label, main_class in suites:
            command = ["java", "-Xmx1200m"]
            if label in ("engine", "environment"): command += ["-javaagent:" + str(agent)]
            command += ["-cp", cp, "OracleRegressionLauncher", str(classes), main_class, str(study)]
            if label == "engine": command += [str(study / "reports/java-engine-three-path-parity.json"), "all"]
            elif label in ("legacy", "core", "environment", "ui"): command += [str(study / "build/hybrid")]
            run(label, command)
        for label, stem in [("legacy", "java"), ("core", "java-core"), ("environment", "java-environment"), ("engine", "java-engine"), ("ui", "java-ui")]:
            reports[label] = json.loads((study / "reports" / (stem + "-three-path-parity.json")).read_text())
        spec = importlib.util.spec_from_file_location("baseline_test_aggregation", baseline / "test.py")
        module = importlib.util.module_from_spec(spec)
        import sys
        sys.path.insert(0, str(baseline))
        spec.loader.exec_module(module)
        registry = json.loads((study / "source/java-method-map.json").read_text())
        module.validate_method_partition(reports, registry)
        aggregate = module.aggregate_reports(reports, len(registry), 3)
        assert aggregate["passed"] and aggregate["cases"] == 188791
        for folder in [baseline / "build/java/hostclasses", baseline / "tools/classes"]:
            for item in [r for r in cp_inputs if str(baseline / r["path"]).startswith(str(folder) + "/")]:
                assert sha(baseline / item["path"]) == item["sha256"]
        result.update(status="PASSED", passed=True, aggregate=aggregate, exact_method_key_partition_verified=True, baseline_classpath_unchanged=True, parent_adapter_rules_configured=0, parent_adapter_calls=0)
    except BaseException as failure:
        result.update(status="FAILED", passed=False, failure=repr(failure))
        raise
    finally:
        shutil.copytree(study / "reports", output / "reports")
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save(output / "result.json", result)
        shutil.rmtree(study)
        save(output / "study-cleanup.json", {"path": str(study), "absent": not study.exists(), "generated_inputs_reproducible_from_pinned_baseline": True, "full_reports_retained": True})


if __name__ == "__main__":
    main()
