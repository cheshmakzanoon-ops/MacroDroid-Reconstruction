#!/usr/bin/env python3
"""Apply the measured host UI VM policy to the exact, preserved failed candidate."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

from prepare_signed_study import copy_checked, now, record, require, sha, write

EXPECTED_PATHS = ["acceptance.py", "test.py", "tests/test_ui_runtime_policy.py", "ui_negative_control.py", "ui_runtime_policy.py"]


def once(text, old, new):
    require(text.count(old) == 1, "Unexpected runtime policy patch anchor: " + old)
    return text.replace(old, new)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.preparation, args.jdk, args.output = [p.resolve() for p in (args.preparation, args.jdk, args.output)]
    source = Path(__file__).resolve().parent
    previous = json.loads(args.preparation.read_text())
    root = Path(previous["private_project"])
    args.output.mkdir(parents=True, exist_ok=False)
    result = {"status": "INSTALLING_HOST_UI_RUNTIME_POLICY", "passed": False, "started_utc": now(), "commands": [],
              "inherited_preparation": {"path": str(args.preparation), **record(args.preparation)},
              "scope": "Host runtime/test policy only; exact application sources and APK retained"}
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk)
    env["PATH"] = str(args.jdk / "bin") + os.pathsep + env.get("PATH", "")

    def snapshot():
        spec = importlib.util.spec_from_file_location("widget_policy_integrity", root / "release_integrity.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.snapshot()

    def command(label, argv):
        log = args.output / (label + ".log")
        with log.open("w") as stream:
            stream.write("COMMAND: " + json.dumps(list(map(str, argv))) + "\n")
            stream.flush()
            done = subprocess.run(list(map(str, argv)), cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=120)
        row = {"label": label, "argv": list(map(str, argv)), "returncode": done.returncode, "log": {"path": log.name, **record(log)}}
        result["commands"].append(row)
        write(args.output / "result.json", result)
        require(done.returncode == 0, "Runtime policy installation command failed: " + label)

    try:
        failed = source / "checkpoints/06-corrected-message-failure/checkpoint.json"
        require(sha(failed) == "6164aeaad35d5aa02bd97f2c729fb9253ca6bbd61785c5837b31450a5429ccf3",
                "The prior full failure is not frozen")
        experiment_path = source / "reports/jvm-exception-flag-01/result.json"
        experiment = json.loads(experiment_path.read_text())
        require(experiment["passed"] is True and experiment["inputs_unchanged"] is True
                and experiment["same_execution_inventory_and_original_coverage"] is True
                and experiment["cases"] == 20818 and experiment["failed_cases"] == 0,
                "The unchanged UI runtime experiment did not pass")
        result["frozen_failure"] = record(failed)
        result["measured_flag_experiment"] = {"path": str(experiment_path), **record(experiment_path)}
        before = snapshot()
        require(before["snapshot_sha256"] == "46c68873d3ff573da2d6676507b2dd6e82e7077c9ed7bcac422e45b0939a8659"
                and before == json.loads((root / "reports/release-input-snapshot.json").read_text()), "Candidate inputs changed")
        apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
        apk_before = record(apk)
        require(apk_before["sha256"] == "b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f", "Wrong candidate APK")
        for relative in ("ui_runtime_policy.py", "tests/test_ui_runtime_policy.py"):
            require(not (root / relative).exists(), "Policy input already exists")
            copy_checked(source / "runtime-policy-inputs" / relative, root / relative)
        path = root / "test.py"
        text = once(path.read_text(), "import build\n", "import build\nimport ui_runtime_policy\n")
        text = once(text, "        argv=['java','-Xmx1200m']\n", "        argv=['java','-Xmx1200m']\n        if key=='ui':\n            policy=ui_runtime_policy.verify(build.REPORTS)\n            argv=[policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1200m']\n")
        path.write_text(text)
        path = root / "ui_negative_control.py"
        text = once(path.read_text(), "import build\n", "import build\nimport ui_runtime_policy\n")
        text = once(text, "    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]));records=[]\n",
                    "    policy=ui_runtime_policy.verify(build.REPORTS)\n    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]));records=[]\n")
        require(text.count("['java','-Xmx1000m'") == 2, "Both UI fault/restoration launchers were not found")
        text = text.replace("['java','-Xmx1000m'", "[policy['java_executable'],*ui_runtime_policy.JVM_FLAGS,'-Xmx1000m'")
        path.write_text(text)
        path = root / "acceptance.py"
        text = once(path.read_text(), "'migration-static-proof.json','migration-linkage-check.json','reference-failures-status-v9.json']",
                    "'migration-static-proof.json','migration-linkage-check.json','reference-failures-status-v9.json',\n           'constructor-oracle-conformance.json','widget-bitwise-oracle-conformance.json','ui-runtime-policy.json']")
        path.write_text(text)
        command("runtime-policy-adversarial-tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ui_runtime_policy.py", "-v"])
        command("effective-runtime-policy", [sys.executable, "-c", "from pathlib import Path; import ui_runtime_policy; ui_runtime_policy.verify(Path('reports'))"])
        command("record-runtime-policy-inputs", [sys.executable, "release_integrity.py", "record"])
        after = snapshot()
        actual = sorted(p for p, entry in after["entries"].items() if before["entries"].get(p) != entry)
        require(actual == EXPECTED_PATHS and not (before["entries"].keys() - after["entries"].keys()), "Runtime correction changed an unreviewed input")
        require(record(apk) == apk_before, "Runtime policy installation changed the signed APK")
        result.update(status="HOST_UI_RUNTIME_POLICY_INSTALLED", passed=True, changed_paths=actual,
                      input_snapshot_before=before["snapshot_sha256"], input_snapshot_after=after["snapshot_sha256"],
                      application_input_changes=[], apk_unchanged=True, apk=apk_before,
                      changed_inputs=[{"path": p, "before": before["entries"].get(p), "after": after["entries"][p]} for p in actual])
        preparation = dict(previous)
        preparation.update(status="WIDGET_UI_RUNTIME_POLICY_INSTALLED_APPLICATION_INPUTS_UNCHANGED", passed=True,
                           candidate_inputs={k: v for k, v in after.items() if k != "entries"},
                           inherited_preparation=result["inherited_preparation"], inherited_commands=previous["commands"],
                           commands=result["commands"], runtime_policy_changed_paths=actual, application_input_changes=[],
                           runtime_policy_correction={"path": str(args.output / "result.json")}, expected_python_tests=265)
        write(args.output / "preparation.json", preparation)
    except BaseException as error:
        result.update(status="HOST_UI_RUNTIME_POLICY_INSTALLATION_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now()
        write(args.output / "result.json", result)
    print(json.dumps({k: result[k] for k in ("status", "passed", "input_snapshot_after", "changed_paths", "apk_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
