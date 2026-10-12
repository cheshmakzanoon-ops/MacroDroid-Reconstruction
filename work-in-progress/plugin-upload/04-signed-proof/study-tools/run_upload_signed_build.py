#!/usr/bin/env python3
"""Build the frozen plugin-upload candidate and preserve the actual bounded result."""
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
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    checkpoint = json.loads(args.checkpoint.read_text())
    failures = [row["path"] for row in checkpoint["files"]
                if not (root / row["path"]).is_file() or sha(root / row["path"]) != row["sha256"]]
    if failures:
        raise RuntimeError("Frozen plugin-upload input mismatch: " + repr(failures))
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk.resolve())
    env["PATH"] = str(args.jdk.resolve() / "bin") + os.pathsep + env.get("PATH", "")
    argv = ["python3", "build.py", "build", "--variant", "hybrid"]
    report = {
        "status": "RUNNING", "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": str(root), "argv": argv, "timeout_seconds": 2400,
        "checkpoint": str(args.checkpoint.resolve()), "checkpoint_sha256": sha(args.checkpoint),
        "source_files_verified": len(checkpoint["files"]), "build_script_sha256": sha(root / "build.py"),
        "runner_sha256": sha(Path(__file__)), "free_bytes_before": shutil.disk_usage(root).free,
        "scope": "Signed build only; rebuilt parity, static/linkage/roundtrip and deliberate-fault execution are separate gates",
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    started = time.monotonic()
    with (output / "build.log").open("w") as stream:
        try:
            result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=2400)
            code = result.returncode
        except subprocess.TimeoutExpired:
            stream.write("\nBUILD_TIMEOUT: exceeded 2400 seconds\n")
            code = 124
    report.update(returncode=code, elapsed_seconds=round(time.monotonic() - started, 3),
                  finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  log_sha256=sha(output / "build.log"), free_bytes_after=shutil.disk_usage(root).free)
    report["source_files_unchanged_after_build"] = all(sha(root / row["path"]) == row["sha256"] for row in checkpoint["files"])
    apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
    report["passed"] = code == 0 and report["source_files_unchanged_after_build"] and apk.is_file()
    report["status"] = "SIGNED_BUILD_PASSED" if report["passed"] else "SIGNED_BUILD_FAILED"
    if apk.is_file():
        report["apk"] = {"path": str(apk), "bytes": apk.stat().st_size, "sha256": sha(apk)}
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
