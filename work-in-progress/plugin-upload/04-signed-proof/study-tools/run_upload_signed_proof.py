#!/usr/bin/env python3
"""Run signed three-path comparison, hybrid verification and all UI controls.

All application source inputs stay pinned to the inactive plugin-upload host
checkpoint. Reports are written in the existing private candidate only.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


def sha(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--signed-build-result", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    checkpoint = json.loads(args.checkpoint.read_text())
    build_result = json.loads(args.signed_build_result.read_text())
    if build_result.get("passed") is not True:
        raise RuntimeError("Signed build has not passed")
    apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    if not apk.is_file() or sha(apk) != build_result["apk"]["sha256"]:
        raise RuntimeError("Signed APK identity changed after build")
    for row in checkpoint["files"]:
        if sha(root / row["path"]) != row["sha256"]:
            raise RuntimeError("Frozen plugin-upload source changed: " + row["path"])
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk.resolve())
    env["PATH"] = str(args.jdk.resolve() / "bin") + os.pathsep + env.get("PATH", "")
    report = {
        "status": "RUNNING", "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": str(root), "checkpoint": str(args.checkpoint.resolve()), "checkpoint_sha256": sha(args.checkpoint),
        "signed_build_result_sha256": sha(args.signed_build_result), "apk": build_result["apk"],
        "source_files_verified": len(checkpoint["files"]), "build_script_sha256": sha(root / "build.py"),
        "runner_sha256": sha(Path(__file__)), "free_bytes_before": shutil.disk_usage(root).free,
        "scope": "Signed DEX/static/linkage/roundtrip and bounded original/JVM/rebuilt comparison; no Android runtime execution",
        "commands": [], "android_executed": False,
    }

    def save():
        (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")

    save()
    try:
        for label, argv, timeout in (
            ("three-path", ["python3", "test.py", "--three-way"], 2400),
            ("hybrid-verification", ["python3", "-c", "import build; build.verify('hybrid')"], 1800),
            ("all-54-ui-negative-controls", ["python3", "ui_negative_control.py"], 5400),
        ):
            started = time.monotonic()
            log = output / (label + ".log")
            with log.open("w") as stream:
                try:
                    result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
                    code = result.returncode
                except subprocess.TimeoutExpired:
                    stream.write("\nPROOF_TIMEOUT: exceeded " + str(timeout) + " seconds\n")
                    code = 124
            unchanged = all(sha(root / row["path"]) == row["sha256"] for row in checkpoint["files"])
            record = {"label": label, "argv": argv, "timeout_seconds": timeout, "returncode": code,
                      "elapsed_seconds": round(time.monotonic() - started, 3), "log": log.name,
                      "log_sha256": sha(log), "source_files_unchanged": unchanged, "apk_unchanged": sha(apk) == build_result["apk"]["sha256"]}
            report["commands"].append(record)
            save()
            print(label + " exit=" + str(code), flush=True)
            if code != 0 or not unchanged or not record["apk_unchanged"]:
                raise RuntimeError("Proof gate failed: " + label)
        parity = json.loads((root / "reports/java-all-path-parity.json").read_text())
        controls = json.loads((root / "reports/ui-negative-controls.json").read_text())
        if not (parity["passed"] and parity["methodsCovered"] == 1241 and parity["cases"] == 191147
                and parity["paths"] == 3 and parity["failedCases"] == 0 and parity["unsupportedExecutions"] == 0
                and controls["pass"] and len(controls["controls"]) == 54 and controls["positiveRestorationPassed"]
                and controls["restorationCases"] == 20832):
            raise RuntimeError("Signed proof counts or control/restoration gate disagree")
        report["parity"] = parity
        report["ui_controls"] = {"count": len(controls["controls"]), "passed": controls["pass"],
                                 "restoration_cases": controls["restorationCases"], "positive_restoration_passed": controls["positiveRestorationPassed"]}
        report["passed"] = True
        report["status"] = "SIGNED_THREE_PATH_ALL_54_UI_CONTROLS_PASSED"
    except Exception as failure:
        report["passed"] = False
        report["status"] = "SIGNED_PROOF_GATE_FAILED"
        report["error"] = type(failure).__name__ + ": " + str(failure)
    report["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report["free_bytes_after"] = shutil.disk_usage(root).free
    save()
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
