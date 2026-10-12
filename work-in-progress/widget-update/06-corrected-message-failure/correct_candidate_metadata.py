#!/usr/bin/env python3
"""Correct only the two omitted Widget test/fixture metadata inputs after closure."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from prepare_signed_study import ORIGINAL_APK, now, record, require, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--closed-failure", type=Path, required=True)
    parser.add_argument("--frozen-failure", type=Path, required=True)
    parser.add_argument("--jdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    old = json.loads(args.preparation.read_text())
    failed = json.loads(args.closed_failure.read_text())
    frozen = json.loads(args.frozen_failure.read_text())
    require(failed["status"] == "SIGNED_WIDGET_PROOF_FAILED" and failed["passed"] is False, "Previous study is not a closed failure")
    require(frozen["status"] == "SIGNED_BUILD_CODE_RESOURCES_PASSED_HOST_METADATA_GATE_FAILED", "Original failure is not frozen")
    for entry in frozen["files"]:
        require(record(args.frozen_failure.parent / entry["path"]) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}, "Frozen failure evidence changed")
    root = Path(old["private_project"])
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    result = {"status": "WIDGET_METADATA_CORRECTION_RUNNING", "passed": False, "started_utc": now(), "private_project": str(root),
              "inherited_preparation": {"path": str(args.preparation.resolve()), **record(args.preparation)},
              "closed_initial_failure": {"path": str(args.closed_failure.resolve()), **record(args.closed_failure)},
              "frozen_failure": {"path": str(args.frozen_failure.resolve()), **record(args.frozen_failure)}, "commands": []}
    env = os.environ.copy()
    env["JAVA_HOME"] = str(args.jdk.resolve())
    env["PATH"] = str(args.jdk.resolve() / "bin") + os.pathsep + env.get("PATH", "")

    def command(label, arguments):
        logfile = output / (label + ".log")
        entry = {"label": label, "argv": [sys.executable, *arguments], "cwd": str(root), "started_utc": now()}
        start = time.monotonic()
        with logfile.open("wb") as stream:
            stream.write(("COMMAND: " + json.dumps(entry["argv"]) + "\n").encode())
            stream.flush()
            process = subprocess.run(entry["argv"], cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1200)
        entry.update(returncode=process.returncode, timed_out=False, finished_utc=now(), elapsed_seconds=round(time.monotonic()-start, 6), log={"path": logfile.name, **record(logfile)})
        result["commands"].append(entry)
        write(output / "correction.json", result)
        require(process.returncode == 0, "Metadata correction command failed: " + label)

    try:
        oldpin = json.loads((root / "reports/release-input-snapshot.json").read_text())
        require(oldpin["snapshot_sha256"] == old["candidate_inputs"]["snapshot_sha256"] == "a729f01fc4b0dc136c980501c144b43769332c324f8c6f63438107d605291691", "Wrong closed source input pin")
        command("verify-closed-inputs", ["release_integrity.py", "verify"])
        apk = root / "dist/MacroDroid-5.67.8-v9-hybrid.apk"
        apk_before = record(apk)
        require(apk_before["sha256"] == frozen["apk_sha256"], "Closed APK differs from frozen evidence")
        changes = []
        path = root / "tests/test_build.py"
        before = record(path)
        text = path.read_text()
        for previous, replacement in [
            ("def test_registry_count(self):self.assertEqual(len(self.registry),1240)", "def test_registry_count(self):self.assertEqual(len(self.registry),1241)"),
            ("def test_registered_classes_count(self):self.assertEqual(len({e['target'] for e in self.registry}),603)", "def test_registered_classes_count(self):self.assertEqual(len({e['target'] for e in self.registry}),604)"),
            ("self.assertEqual(p['methods'],1240)", "self.assertEqual(p['methods'],1241)"),
        ]:
            require(text.count(previous) == 1, "Unexpected common inventory assertion")
            text = text.replace(previous, replacement)
        path.write_text(text)
        changes.append({"path": "tests/test_build.py", "before": before, "after": record(path)})
        path = root / "tests/fixtures/provenance.json"
        before = record(path)
        provenance = json.loads(path.read_text())
        fixture = record(root / "tests/fixtures/original-methods.dex")
        require(fixture == {"bytes": old["full_original_fixture"]["bytes"], "sha256": old["full_original_fixture"]["sha256"]}, "Original extracted fixture changed")
        require(provenance["original_apk_sha256"] == ORIGINAL_APK and provenance["methods"] == 1240 and provenance["classes"] == 603, "Unexpected inherited fixture provenance")
        provenance.update(fixture_sha256=fixture["sha256"], fixture_bytes=fixture["bytes"], methods=1241, classes=604,
                          extraction="ExtractOracle executed against the unchanged original upload; exact registered WidgetUpdateManager.m added to the published 1,240-method fixture")
        write(path, provenance)
        changes.append({"path": "tests/fixtures/provenance.json", "before": before, "after": record(path)})
        result["changes"] = changes
        write(output / "correction.json", result)
        command("record-corrected-inputs", ["release_integrity.py", "record"])
        newpin = json.loads((root / "reports/release-input-snapshot.json").read_text())
        require(oldpin["entries"].keys() == newpin["entries"].keys(), "Metadata correction added or removed an input")
        changed = sorted(key for key in oldpin["entries"] if oldpin["entries"][key] != newpin["entries"][key])
        require(changed == ["tests/fixtures/provenance.json", "tests/test_build.py"], "Metadata correction affected an unrelated input")
        require(record(apk) == apk_before, "Metadata correction changed the signed artifact")
        result.update(status="WIDGET_METADATA_CORRECTED_APPLICATION_INPUTS_UNCHANGED", passed=True,
                      metadata_changed_paths=changed, application_input_changes=[], source_input_files=newpin["files"],
                      previous_input_snapshot_sha256=oldpin["snapshot_sha256"], source_input_snapshot_sha256=newpin["snapshot_sha256"], apk_unchanged=apk_before)
        prepared = copy.deepcopy(old)
        prepared.update(status=result["status"], passed=True, application_input_changes=[], metadata_changed_paths=changed,
                        metadata_correction={"path": str(output / "correction.json")}, inherited_preparation=result["inherited_preparation"],
                        candidate_inputs={key: value for key, value in newpin.items() if key != "entries"},
                        scope="Derived Widget candidate: exact application/fixture bytes unchanged; only omitted metadata/count assertions corrected after freezing initial failure")
        prepared["commands"] = result["commands"]
        prepared["input_delta"]["changed"] = sorted(set(prepared["input_delta"]["changed"]) | set(changed))
        prepared["overlays"].extend(changes)
        prepared["finished_utc"] = now()
        write(output / "preparation.json", prepared)
    except BaseException as error:
        result.update(status="WIDGET_METADATA_CORRECTION_FAILED", error=repr(error))
        raise
    finally:
        result["finished_utc"] = now()
        write(output / "correction.json", result)
        print(json.dumps({key: result.get(key) for key in ["status", "passed", "source_input_snapshot_sha256", "metadata_changed_paths", "error"]}, indent=2))


if __name__ == "__main__":
    main()
