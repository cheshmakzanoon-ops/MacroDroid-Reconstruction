#!/usr/bin/env python3
"""Freeze and execute constructor and Widget bitwise synthetic oracle controls."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--host-classes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    own = Path(__file__).resolve().parent
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    classes = output / "classes"
    classes.mkdir()
    names = ["tests/java/BytecodeOracle.java", "tests/java/ConstructorOracleConformance.java", "tests/java/WidgetOracleOpcodeConformance.java", "tests/fixtures/constructor-owner-opcodes.smali", "tests/fixtures/widget-bitwise-opcodes.smali"]
    inputs = []
    for name in names:
        target = output / "inputs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(own / name, target)
        inputs.append({"path": name, "bytes": target.stat().st_size, "sha256": sha(target)})
    assert inputs[0]["sha256"] == "d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56"
    result = {"status": "RUNNING", "started_utc": datetime.now(timezone.utc).isoformat(), "scope": "Synthetic host interpreter constructor boundaries and AND_INT semantics; no Widget method or Android execution", "android_executed": False, "inputs": inputs, "commands": [], "jar_sha256": sha(args.jar), "host_dependencies": [{"path": str(p.relative_to(args.host_classes)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(args.host_classes.rglob("*.class"))]}
    def save() -> None:
        (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    def run(label: str, command: list[str]) -> None:
        start = time.monotonic()
        log = output / (label + ".log")
        with log.open("w") as stream:
            stream.write(json.dumps(command) + "\n"); stream.flush()
            process = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=120)
        result["commands"].append({"label": label, "command": command, "exit_code": process.returncode, "seconds": round(time.monotonic() - start, 3), "log": log.name, "log_sha256": sha(log)})
        save()
        if process.returncode: raise RuntimeError(label + " failed")
    cp = ":".join(map(str, [classes, args.jar, args.host_classes]))
    try:
        run("compile", ["javac", "-cp", cp, "-d", str(classes)] + [str(output / "inputs" / n) for n in names if n.endswith(".java")])
        for stem, fixture, main_class, expected in [("constructor", "constructor-owner-opcodes.smali", "ConstructorOracleConformance", 16), ("widget-bitwise", "widget-bitwise-opcodes.smali", "WidgetOracleOpcodeConformance", 4546)]:
            dex = output / (stem + ".dex")
            report = output / (stem + ".json")
            run(stem + "-assemble", ["java", "-cp", str(args.jar), "com.android.tools.smali.smali.Main", "a", "--api", "23", "-o", str(dex), str(output / "inputs/tests/fixtures" / fixture)])
            run(stem + "-execute", ["java", "-cp", cp, main_class, str(dex), str(report)])
            actual = json.loads(report.read_text())
            assert actual["passed"] and actual["cases"] == expected
            result[stem] = {"passed": True, "cases": expected, "dex_sha256": sha(dex), "report_sha256": sha(report)}
        result.update(status="PASSED", passed=True, constructor_cases=16, bitwise_cases=4546)
    except BaseException as error:
        result.update(status="FAILED", passed=False, failure=repr(error))
        raise
    finally:
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
    print(json.dumps({k: v for k, v in result.items() if k not in ["inputs", "commands", "host_dependencies"]}, indent=2))


if __name__ == "__main__":
    main()
